from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.fund_api import router as fund_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fund_router, prefix="/api")
