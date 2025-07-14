import pandas as pd
from typing import List, Dict

from utils.feedback_prompt import build_feedback_prompt
from services.ai_feedback import generate_ai_feedback  # GPT 호출 함수

def detect_trail_braking(
    df: pd.DataFrame,
    brake_col: str = "brake",
    steer_col: str = "steerangle",
    time_col: str = "time",
    brake_thresh: float = 0.05,
    steer_thresh: float = 10.0,
) -> List[Dict]:
    """
    트레일 브레이킹 구간을 감지하고, 각 구간에 대해 GPT 피드백을 생성한다.

    Returns:
        [{
            'start_idx': int,
            'end_idx': int,
            'start_time': float,
            'end_time': float,
            'feedback': str
        }, ...]
    """
    in_trail = False
    trail_start = None
    trail_zones = []

    for i in range(len(df)):
        brake_val = df.iloc[i][brake_col]
        steer_val = abs(df.iloc[i][steer_col])

        if not in_trail and brake_val > brake_thresh and steer_val > steer_thresh:
            in_trail = True
            trail_start = i

        elif in_trail and (brake_val <= brake_thresh or steer_val <= steer_thresh):
            trail_end = i - 1
            zone = {
                'start_idx': trail_start,
                'end_idx': trail_end,
                'start_time': df.iloc[trail_start][time_col],
                'end_time': df.iloc[trail_end][time_col],
            }
            trail_zones.append(zone)
            in_trail = False


    # 마지막까지 이어진 경우 처리
    if in_trail:
        trail_end = len(df) - 1
        zone = {
            'start_idx': trail_start,
            'end_idx': trail_end,
            'start_time': df.iloc[trail_start][time_col],
            'end_time': df.iloc[trail_end][time_col],
        }
        trail_zones.append(zone)

    # ✅ 각 구간에 대해 GPT 피드백 생성
    for idx, segment in enumerate(trail_zones):
        try:
            # 분석 지표 계산 (간단 예시, 필요시 개선 가능)
            duration = segment["end_time"] - segment["start_time"]
            steer_slice = df.iloc[segment["start_idx"]:segment["end_idx"] + 1][steer_col]
            avg_steer_variability = steer_slice.diff().abs().mean()
            avg_deceleration = df.iloc[segment["start_idx"]:segment["end_idx"] + 1]["speed"].diff().mean() * -1

            segment["duration"] = duration
            segment["steer_variability"] = avg_steer_variability
            segment["avg_deceleration"] = avg_deceleration

            # 🧠 프롬프트 생성 및 GPT 호출
            prompt = build_feedback_prompt(segment, idx, mode="braking", driver_level="beginner")
            feedback, _ = generate_ai_feedback(prompt)

        except Exception as e:
            print(f"❌ 브레이크 피드백 생성 실패 (구간 {idx + 1}): {repr(e)}")
            feedback = "⚠️ 현재 AI 피드백 서버에 연결할 수 없습니다.\n기본 분석 결과만 제공됩니다."

        segment["feedback"] = feedback

    return trail_zones
