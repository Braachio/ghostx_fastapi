from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os


# API 모듈 import
from api.analyze import router as analyze_router
from api.motec import router as motec_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# 라우터 등록
app.include_router(analyze_router, prefix="/api")
app.include_router(motec_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))  # Render는 기본적으로 10000
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)