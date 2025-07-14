from fastapi import UploadFile, Form, File, APIRouter
from fastapi.responses import JSONResponse
from io import StringIO
import pandas as pd
import hashlib

from utils.supabase_client import supabase
from utils.sanitize import sanitize_for_json
from utils.calculate import calculate_distance, convert_speed_to_kmph
from utils.corner_exit_analysis import analyze_corner_exit_and_feedback
from services.purification import remove_straight_sections, correct_autoblip_throttle
from services.insert import extract_value, chunked_insert, chunked_insert_lap_raw, fetch_all_controls, fetch_all_vehicle_status
from services.analyze_sector_times import upload_sector_results, get_sector_summary


router = APIRouter()

def deduplicate_columns(columns):
    seen = {}
    result = []
    for col in columns:
        col_lower = col.strip().lower()
        if col_lower in seen:
            seen[col_lower] += 1
            col_lower = f"{col_lower}_{seen[col_lower]}"
        else:
            seen[col_lower] = 0
        result.append(col_lower)
    return result

def generate_lap_hash(df: pd.DataFrame) -> str:
    data_str = df.to_csv(index=False)
    return hashlib.sha256(data_str.encode()).hexdigest()

@router.post("/analyze-motec-csv")
async def analyze_motec_csv(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    save: bool = Form(False),
    weather: str = Form(None),
    air_temp: float = Form(None),
    track_temp: float = Form(None)
):
    try:
        content = await file.read()
        text = content.decode("utf-8", errors="ignore")
        lines = text.splitlines()
        if len(lines) > 15:
            lines.pop(15)

        track_name = extract_value(lines, "Venue")
        car_name = extract_value(lines, "Vehicle")

        df = pd.read_csv(StringIO("\n".join(lines[14:])), on_bad_lines="skip", low_memory=False)
        df.columns = deduplicate_columns(df.columns)

        if "time" not in df.columns:
            return JSONResponse(status_code=400, content={"error": "'time' 열이 없음"})

        for col in df.columns:
            df[col] = df[col].astype(str).str.replace(r"[a-zA-Z%/]+", "", regex=True)

        df = df.apply(pd.to_numeric, errors="coerce").dropna()
        df = df[[col for col in df.columns if not col.startswith("time_")]]

        if 'distance' not in df.columns:
            df = calculate_distance(df)

        df = convert_speed_to_kmph(df)

        # ✅ 여기서 분리
        control_cols = ["time", "throttle", "brake", "steerangle", "speed", "rpms", "gear", "distance"]
        control_cols = [col for col in control_cols if col in df.columns]
        control_df = df[control_cols].copy()

        vehicle_cols = ["time"] + [col for col in df.columns if col not in control_cols and col != "time"]
        vehicle_df = df[vehicle_cols].copy()



        df, fixed_count = correct_autoblip_throttle(df)
        print(f"🛠️ 오토블립 또는 브레이크 100 조건으로 스로틀 보정된 행 수: {fixed_count}")
        df = remove_straight_sections(df)

        if not isinstance(df, pd.DataFrame):
            raise ValueError(f"remove_straight_sections() 결과 오류: {df}")

        if "gear" in df.columns:
            df["gear"] = pd.to_numeric(df["gear"], errors="coerce").fillna(0).astype(int)

        graph_keys = ["time", "throttle", "brake", "steerangle", "gear", "speed"]
        graph_data = df[[key for key in graph_keys if key in df.columns]].to_dict(orient="records")
        sector_results = get_sector_summary(df)

        # ✅ 중복 확인
        lap_hash = generate_lap_hash(df)

        if save:
            existing = supabase.table("lap_meta").select("id").eq("hash", lap_hash).execute()
            if existing.data:
                return JSONResponse(status_code=409, content={"error": "❌ 중복된 랩 데이터입니다."})

            meta_resp = supabase.table("lap_meta").insert({
                "user_id": user_id,
                "track": track_name,
                "car": car_name,
                "weather": weather,
                "air_temp": air_temp,
                "track_temp": track_temp,
                "hash": lap_hash
            }).execute()
            lap_id = meta_resp.data[0]["id"]

            control_cols = ["time", "throttle", "brake", "steerangle", "speed", "rpms", "gear", "distance"]
            control_cols = [col for col in control_cols if col in df.columns]
            df["lap_id"] = lap_id

            chunked_insert("lap_controls", df[control_cols + ["lap_id"]].to_dict(orient="records"))

            print(f"🔎 전체 레코드 수: {len(df)}")
            inserted = supabase.table("lap_controls").select("id").eq("lap_id", lap_id).execute()
            print(f"✅ 저장된 lap_controls 수: {len(inserted.data) if inserted.data else 0}")

            vehicle_cols = [col for col in df.columns if col not in control_cols + ["lap_id", "time"]]
            chunked_insert("lap_vehicle_status", df[["time"] + vehicle_cols + ["lap_id"]].to_dict(orient="records"))

            chunked_insert_lap_raw(lap_id, df)

            upload_sector_results(supabase, lap_id, user_id, track_name, df)

            # ✅ 코너 탈출 구간 분석
            exit_segments = analyze_corner_exit_and_feedback(control_df, vehicle_df)

            return {
                "status": "✅ 분석 및 저장 완료",
                "track": track_name,
                "car": car_name,
                "data": graph_data,
                "sector_results": sector_results,
                "corner_exit_analysis": exit_segments
            }

        return {
            "status": "✅ 분석 완료 (저장 안 함)",
            "track": track_name,
            "car": car_name,
            "data": graph_data,
            "sector_results": sector_results,
            "corner_exit_analysis": exit_segments
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"분석 실패: {repr(e)}"})

@router.get("/lap/{lap_id}")
def get_lap_data(lap_id: str):
    # lap_meta 정보 조회
    meta = supabase.table("lap_meta").select("*").eq("id", lap_id).single().execute().data
    if not meta:
        return JSONResponse(status_code=404, content={"error": "랩 정보를 찾을 수 없습니다."})

    # lap_controls 가져오기
    controls = fetch_all_controls(lap_id)
    vehicle = fetch_all_vehicle_status(lap_id)

    try:
        sector_results = supabase.table("sector_results").select("*").eq("lap_id", lap_id).execute().data
    except Exception as e:
        print(f"❌ sector_results 조회 실패: {repr(e)}")
        sector_results = []

    # ✅ 자연어 피드백 추가 처리
    try:
        df_controls = pd.DataFrame(controls)
        df_vehicle = pd.DataFrame(vehicle)

        df = pd.merge(df_controls, df_vehicle, on="time", how="inner")

        required_columns = [
            "steerangle", "throttle",
            "wheel_speed_lf", "wheel_speed_rf",
            "wheel_speed_lr", "wheel_speed_rr"
        ]

        if all(col in df.columns for col in required_columns):
            corner_feedback = analyze_corner_exit_and_feedback(controls, vehicle)
        else:
            print("⚠️ 코너 분석에 필요한 컬럼이 부족함: {[col for col in required_columns if col not in df.columns]}")
            corner_feedback = []
    except Exception as e:
        print(f"❌ 코너 피드백 분석 실패: {repr(e)}")
        corner_feedback = []

    return sanitize_for_json({
        "track": meta["track"],
        "car": meta["car"],
        "data": controls,
        "sector_results": sector_results,
        "corner_exit_analysis": corner_feedback
    })

