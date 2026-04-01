from sqlalchemy.orm import Session

from app.models import News


def seed_news(db: Session):
    existing = db.query(News).count()
    if existing > 0:
        return

    items = [
        News(
            title="Rambler launches new media feature",
            content="A new content block was added to the media platform.",
            source="Rambler",
            tag="media",
        ),
        News(
            title="Sports digest of the day",
            content="Latest updates from the sports section.",
            source="Championat",
            tag="sport",
        ),
        News(
            title="Afisha weekend guide",
            content="Top events and recommendations for the weekend.",
            source="Afisha",
            tag="lifestyle",
        ),
    ]

    for item in items:
        db.add(item)

    db.commit()