# services/analysis/brake_analysis.py

import pandas as pd

def detect_trail_braking(
    df: pd.DataFrame,
    brake_col: str = "brake",
    steer_col: str = "steerangle",
    time_col: str = "time",
    brake_thresh: float = 0.05,
    steer_thresh: float = 2.0,  # 조향 시작 기준
) -> list[dict]:
    """
    트레일 브레이킹 구간을 감지한다.
    브레이크를 밟은 상태에서 조향이 시작된 구간을 감지.

    Returns:
        [{'start_idx': int, 'end_idx': int, 'start_time': float, 'end_time': float}, ...]
    """
    in_trail = False
    trail_start = None
    trail_zones = []

    for i in range(len(df)):
        brake_val = df.iloc[i][brake_col]
        steer_val = abs(df.iloc[i][steer_col])  # 좌우 조향 모두 고려

        # 트레일 브레이크 시작 조건: 조향 시작 + 브레이크 유지
        if not in_trail and brake_val > brake_thresh and steer_val > steer_thresh:
            in_trail = True
            trail_start = i

        # 트레일 브레이크 종료 조건: 조향 또는 브레이크 종료
        elif in_trail and (brake_val <= brake_thresh or steer_val <= steer_thresh):
            trail_end = i - 1
            trail_zones.append({
                'start_idx': trail_start,
                'end_idx': trail_end,
                'start_time': df.iloc[trail_start][time_col],
                'end_time': df.iloc[trail_end][time_col],
            })
            in_trail = False

    # 마지막까지 이어진 경우 처리
    if in_trail:
        trail_end = len(df) - 1
        trail_zones.append({
            'start_idx': trail_start,
            'end_idx': trail_end,
            'start_time': df.iloc[trail_start][time_col],
            'end_time': df.iloc[trail_end][time_col],
        })

    return trail_zones
