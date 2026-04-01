from datetime import datetime

from pydantic import BaseModel


class NewsCreate(BaseModel):
    title: str
    content: str
    source: str
    tag: str | None = None


class NewsUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    source: str | None = None
    tag: str | None = None


class NewsOut(BaseModel):
    id: int
    title: str
    content: str
    source: str
    tag: str | None
    created_at: datetime

    class Config:
        from_attributes = True