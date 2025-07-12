from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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