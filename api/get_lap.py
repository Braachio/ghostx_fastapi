from fastapi import APIRouter
from fastapi.responses import JSONResponse
import pandas as pd

from utils.supabase_client import supabase
from utils.sanitize import sanitize_for_json
from utils.analysis.corner_exit_analysis import analyze_corner_exit_and_feedback
from utils.analysis.corner_entry_analysis import analyze_corner_entry_and_feedback
from services.insert import fetch_all_controls, fetch_all_vehicle_status
from services.lap_data import fetch_lap_meta_and_data

router = APIRouter()

@router.get("/lap/{lap_id}")
def get_lap_data(lap_id: str):
    lap = fetch_lap_meta_and_data(lap_id)

    # lap_meta 정보 조회
    meta = supabase.table("lap_meta").select("*").eq("id", lap_id).single().execute().data
    if not meta:
        return JSONResponse(status_code=404, content={"error": "랩 정보를 찾을 수 없습니다."})
    
    controls = lap["controls"]
    vehicle = lap["vehicle"]
    meta = lap["meta"]
    sector_results = lap["sector_results"]

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

    # ✅ 트레일 브레이킹 분석 추가
    try:
        df_controls = pd.DataFrame(controls)
        entry_segments = analyze_corner_entry_and_feedback(df_controls)
    except Exception as e:
        print(f"❌ 트레일 브레이킹 분석 실패: {repr(e)}")
        entry_segments = []

    return sanitize_for_json({
        "track": meta["track"],
        "car": meta["car"],
        "data": controls,
        "sector_results": sector_results,
        "corner_exit_analysis": corner_feedback or [],
        "corner_entry_analysis": entry_segments or []
    })
