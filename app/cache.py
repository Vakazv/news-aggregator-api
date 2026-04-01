import json

import redis

from app.config import REDIS_URL

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)


def get_cached_news(key: str):
    data = r.get(key)
    if not data:
        return None
    return json.loads(data)


def set_cached_news(key: str, value, ttl: int = 120):
    r.setex(key, ttl, json.dumps(value, default=str))


def invalidate_news_cache():
    for key in r.scan_iter("news:*"):
        r.delete(key)