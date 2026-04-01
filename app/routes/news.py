from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.cache import get_cached_news, invalidate_news_cache, set_cached_news
from app.db import get_db
from app.schemas import NewsCreate, NewsOut, NewsUpdate

router = APIRouter()


@router.get("/", response_model=list[NewsOut])
def get_news(
    tag: str | None = Query(default=None),
    source: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    cache_key = f"news:list:{tag}:{source}"
    cached = get_cached_news(cache_key)
    if cached:
        return cached

    items = crud.get_news_list(db, tag=tag, source=source)
    serialized = [NewsOut.model_validate(item).model_dump(mode="json") for item in items]
    set_cached_news(cache_key, serialized, ttl=120)
    return serialized


@router.get("/{news_id}", response_model=NewsOut)
def get_news_by_id(news_id: int, db: Session = Depends(get_db)):
    item = crud.get_news_by_id(db, news_id)
    if not item:
        raise HTTPException(status_code=404, detail="News not found")
    return item


@router.post("/", response_model=NewsOut)
def create_news(payload: NewsCreate, db: Session = Depends(get_db)):
    item = crud.create_news(db, payload)
    invalidate_news_cache()
    return item


@router.patch("/{news_id}", response_model=NewsOut)
def patch_news(news_id: int, payload: NewsUpdate, db: Session = Depends(get_db)):
    item = crud.update_news(db, news_id, payload)
    if not item:
        raise HTTPException(status_code=404, detail="News not found")
    invalidate_news_cache()
    return item


@router.delete("/{news_id}")
def remove_news(news_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_news(db, news_id)
    if not ok:
        raise HTTPException(status_code=404, detail="News not found")
    invalidate_news_cache()
    return {"status": "deleted"}