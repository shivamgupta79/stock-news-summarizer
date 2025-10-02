
import aiohttp, feedparser, hashlib
from datetime import datetime
from app.db import SessionLocal, Article

def hash_url(url):
    return hashlib.sha256(url.encode()).hexdigest()

async def fetch_rss_and_store(feed_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(feed_url, timeout=20) as resp:
            text = await resp.text()
    feed = feedparser.parse(text)
    db = SessionLocal()
    added = 0
    for entry in feed.entries:
        url = entry.get('link') or entry.get('id')
        if not url:
            continue
        # dedupe by url
        exists = db.query(Article).filter(Article.url==url).first()
        if exists:
            continue
        content = entry.get('summary') or entry.get('content', [{}])[0].get('value','')
        art = Article(
            title = entry.get('title','')[:500],
            url = url,
            source = feed.feed.get('title','rss'),
            published_at = datetime(*entry.published_parsed[:6]) if 'published_parsed' in entry else None,
            content = content
        )
        db.add(art); added += 1
    db.commit(); db.close()
    return added
