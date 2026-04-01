from sqlalchemy.orm import Session

from app.models import News
from app.schemas import NewsCreate, NewsUpdate


def get_news_list(db: Session, tag: str | None = None, source: str | None = None):
    query = db.query(News)

    if tag:
        query = query.filter(News.tag == tag)

    if source:
        query = query.filter(News.source == source)

    return query.order_by(News.created_at.desc()).all()


def get_news_by_id(db: Session, news_id: int):
    return db.query(News).filter(News.id == news_id).first()


def create_news(db: Session, payload: NewsCreate):
    item = News(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_news(db: Session, news_id: int, payload: NewsUpdate):
    item = get_news_by_id(db, news_id)
    if not item:
        return None

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item


def delete_news(db: Session, news_id: int):
    item = get_news_by_id(db, news_id)
    if not item:
        return False

    db.delete(item)
    db.commit()
    return True