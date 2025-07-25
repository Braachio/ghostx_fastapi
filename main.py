from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# API 모듈 import
from api.upload import router as upload_router
from api.get_lap import router as get_lap_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "🚀 GhostX API is running!"}

# ✅ CORS 수정: allow_credentials=True일 때 "*" 금지
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ghostx.site",           # 🔒 운영 도메인
        "http://localhost:3000"          # 💻 개발용 도메인
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(upload_router, prefix="/api")
app.include_router(get_lap_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
