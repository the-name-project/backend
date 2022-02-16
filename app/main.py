import logging

import click
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlmodel import SQLModel
from app.DB_session import engine

from app.api import router

logger = logging.getLogger("uvicorn")
logger.info(
    "Application Environment: %s",
    'production',
    extra={
        "color_message": f'Application Environment: {click.style("%s", fg="green")}'
    },
)


app = FastAPI(
    title= "temper",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    SQLModel.metadata.create_all(bind=engine)


@app.get("/", response_class=RedirectResponse)
def root() -> str:
    return "/docs"


app.include_router(router)