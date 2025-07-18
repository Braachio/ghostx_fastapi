from fastapi import UploadFile, Form, File, APIRouter
from fastapi.responses import JSONResponse
from io import StringIO
import pandas as pd

from utils.supabase_client import supabase

from utils.calculate import calculate_distance
from utils.analysis.corner_exit_analysis import analyze_corner_exit_and_feedback
from utils.analysis.corner_entry_analysis import analyze_corner_entry_and_feedback
from services.purification import remove_straight_sections, correct_autoblip_throttle
from services.insert import extract_value, chunked_insert, chunked_insert_lap_raw
from services.analyze_sector_times import upload_sector_results, get_sector_summary
from services.upload_lap_data import generate_lap_hash

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

        lap_time = extract_value(lines, "Duration")
        # 🔢 랩타임 파싱 (예: "100.21 s" → 100.21)
        try:
            lap_time_value = float(lap_time.strip().split()[0])
        except Exception:
            lap_time_value = None        
            
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
        # df = convert_speed_to_kmph(df)

        # 정제 및 보정
        df, _ = correct_autoblip_throttle(df)
        df = remove_straight_sections(df)

        # 인덱스 초기화 → 분석 및 시각화 인덱스 정렬 보장
        df = df.reset_index(drop=True)

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


        sector_results = get_sector_summary(df)

        # ✅ 중복 확인
        lap_hash = generate_lap_hash(df)

        # ✅ 코너 진입 구간 분석
        entry_segments = analyze_corner_entry_and_feedback(control_df)

        # ✅ 코너 탈출 구간 분석
        exit_segments = analyze_corner_exit_and_feedback(control_df, vehicle_df)

        graph_keys = ["time", "throttle", "brake", "steerangle", "gear", "speed", "distance"]
        graph_data = df[[key for key in graph_keys if key in df.columns]].to_dict(orient="records")

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
                "hash": lap_hash,
                "lap_time": lap_time_value
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

            return {
                "status": "✅ 분석 및 저장 완료",
                "track": track_name,
                "car": car_name,
                "lap_time": lap_time_value,
                "data": graph_data,
                "sector_results": sector_results,
                "corner_exit_analysis": exit_segments or [],
                "corner_entry_analysis": entry_segments or []
            }

        return {
            "status": "✅ 분석 완료 (저장 안 함)",
            "track": track_name,
            "car": car_name,
            "lap_time": lap_time_value,
            "data": graph_data,
            "sector_results": sector_results,
            "corner_exit_analysis": exit_segments or [],
            "corner_entry_analysis": entry_segments or []
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"분석 실패: {repr(e)}"})
