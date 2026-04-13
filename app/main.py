"""FastAPI启动入口。"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.db import init_db
from app.config.settings import get_settings
from app.utils.seed_data import seed_if_needed

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Ticket Triage Agent")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


@app.on_event("startup")
def startup_event():
    init_db()
    seed_if_needed()
    settings = get_settings()
    logging.info("当前配置: %s", settings.masked_config())
