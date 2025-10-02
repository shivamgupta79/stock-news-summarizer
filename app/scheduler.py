# app/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
from app.fetcher import fetch_rss_and_store
from app.summarizer import summarize_pending

scheduler = BackgroundScheduler()

def schedule_jobs():
    # example RSS list
    feeds = [
        "https://finance.yahoo.com/rss/",
        "https://www.reuters.com/finance/rss"
    ]
    async def job():
        added_total = 0
        for f in feeds:
            added = await fetch_rss_and_store(f)
            added_total += added
        summarize_pending()
        print("ingest job done, added:", added_total)

    def wrapper():
        asyncio.run(job())

    scheduler.add_job(wrapper, "interval", minutes=30, id="ingest_job")
    scheduler.start()
