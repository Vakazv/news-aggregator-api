import time

from fastapi import FastAPI
from sqlalchemy import text

from app.db import Base, SessionLocal, engine
from app.routes.health import router as health_router
from app.routes.news import router as news_router
from app.seed import seed_news


def wait_for_db(max_retries: int = 10, delay: int = 2):
    for attempt in range(max_retries):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return
        except Exception:
            if attempt == max_retries - 1:
                raise
            time.sleep(delay)


wait_for_db()
Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    seed_news(db)

app = FastAPI(title="News Aggregator API")

app.include_router(news_router, prefix="/news", tags=["news"])
app.include_router(health_router, prefix="/health", tags=["health"])


@app.get("/health")
def health():
    return {"status": "ok"}