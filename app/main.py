from fastapi import FastAPI

from app.db import Base, SessionLocal, engine
from app.routes.health import router as health_router
from app.routes.news import router as news_router
from app.seed import seed_news

Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    seed_news(db)

app = FastAPI(title="News Aggregator API")

app.include_router(news_router, prefix="/news", tags=["news"])
app.include_router(health_router, prefix="/health", tags=["health"])


@app.get("/health")
def health():
    return {"status": "ok"}