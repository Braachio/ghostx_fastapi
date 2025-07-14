import pandas as pd
from typing import List, Dict

from utils.feedback_prompt import build_feedback_prompt
from services.ai_feedback import generate_ai_feedback

def detect_trail_braking(
    df: pd.DataFrame,
    brake_col: str = "brake",
    steer_col: str = "steerangle",
    time_col: str = "time",
    steer_thresh: float = 10.0,
    brake_slope_thresh: float = -0.01,  # 기울기 음수 조건
) -> List[Dict]:
    """
    브레이크가 줄어들고 조향이 유지되는 트레일 브레이킹 구간 감지 + GPT 피드백 생성
    """
    df = df.copy().reset_index(drop=True)
    df["brake_diff"] = df[brake_col].diff().fillna(0)

    in_trail = False
    trail_start = None
    trail_zones = []

    for i in range(1, len(df)):  # brake_diff는 1행부터 의미 있음
        brake_gradient = df.at[i, "brake_diff"]
        steer_val = abs(df.at[i, steer_col])

        if not in_trail and brake_gradient < brake_slope_thresh and steer_val > steer_thresh:
            in_trail = True
            trail_start = i

        elif in_trail and (brake_gradient >= 0 or steer_val <= steer_thresh):
            trail_end = i - 1
            zone = {
                'start_idx': trail_start,
                'end_idx': trail_end,
                'start_time': df.at[trail_start, time_col],
                'end_time': df.at[trail_end, time_col],
            }
            trail_zones.append(zone)
            in_trail = False

    if in_trail:
        trail_end = len(df) - 1
        zone = {
            'start_idx': trail_start,
            'end_idx': trail_end,
            'start_time': df.at[trail_start, time_col],
            'end_time': df.at[trail_end, time_col],
        }
        trail_zones.append(zone)

    # ✅ GPT 피드백 생성
    for idx, segment in enumerate(trail_zones):
        try:
            duration = segment["end_time"] - segment["start_time"]
            steer_slice = df.iloc[segment["start_idx"]:segment["end_idx"] + 1][steer_col]
            avg_steer_variability = steer_slice.diff().abs().mean()
            avg_deceleration = df.iloc[segment["start_idx"]:segment["end_idx"] + 1]["speed"].diff().mean() * -1

            segment["duration"] = duration
            segment["steer_variability"] = avg_steer_variability
            segment["avg_deceleration"] = avg_deceleration

            prompt = build_feedback_prompt(segment, idx, mode="braking", driver_level="beginner")
            feedback, _ = generate_ai_feedback(prompt)

        except Exception as e:
            print(f"❌ 브레이크 피드백 생성 실패 (구간 {idx + 1}): {repr(e)}")
            feedback = "⚠️ 현재 AI 피드백 서버에 연결할 수 없습니다.\n기본 분석 결과만 제공됩니다."

        segment["feedback"] = feedback

    return trail_zones
