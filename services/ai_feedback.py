import requests
# from services.gpt_feedback import generate_gpt_feedback

def generate_ai_feedback(prompt: str) -> str:
    """
    GPT 우선 → 실패 시 Ollama 사용
    """
    # try:
    #     # 1차 GPT 사용
    #     return generate_gpt_feedback(prompt)
    # except:
    #     print("⚠️ GPT 실패 → Ollama로 대체 시도")

    try:
        response = requests.post(
            "http://localhost:11434/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": "llama3",
                "messages": [
                    {"role": "system", "content": "당신은 전문 드라이빙 코치이며 항상 한국어로 작성합니다."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }
        )
        result = response.json()
        feedback = result["choices"][0]["message"]["content"].strip()
        return feedback, "olama"
    except Exception as e:
        print(f"❌ Olama 피드백 생성 실패: {e}")
        return "⚠️ AI 피드백 생성 실패", "error"