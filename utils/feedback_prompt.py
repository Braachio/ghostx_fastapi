# utils/feedback_prompt.py
from typing import Dict

def build_feedback_prompt(segment: Dict, corner_index: int, driver_level: str = "beginner") -> str:
    """
    운전자 수준(beginner, intermediate, advanced)에 따라 피드백 프롬프트 생성
    """
    base_data = f"""
- Maximum slip ratio: {segment['max_slip_ratio']:.2f}
- Average throttle gradient: {segment['avg_throttle_gradient']:.3f}
- Steering stability (mean change in steering angle): {segment['steer_variability']:.2f}
- Left-right wheel speed difference: {segment['wheel_slip_lr']:.2f}
- Front-rear wheel speed difference: {segment['wheel_slip_fb']:.2f}
"""

    if driver_level == "beginner":
        return f"""
You are a kind and friendly racing coach guiding a beginner driver.

Below is the analysis result for corner exit {corner_index + 1}:
{base_data}

Please write 1–2 short and easy-to-understand sentences,  
with a mix of **praise and advice**, so that a beginner can follow and improve their driving habits.
"""

    elif driver_level == "intermediate":
        # TODO: 추후 중급자용 프롬프트 작성
        return "중급자용 프롬프트는 추후 추가 예정입니다."

    elif driver_level == "advanced":
        # TODO: 추후 고급자용 프롬프트 작성
        return "고급자용 프롬프트는 추후 추가 예정입니다."

    else:
        raise ValueError("지원하지 않는 운전자 수준입니다.")
