from fastapi import FastAPI
from app.routes.news import router as news_router

app = FastAPI(title="News Aggregator API")

app.include_router(news_router, prefix="/news", tags=["news"])


@app.get("/health")
def health():
    return {"status": "ok"}