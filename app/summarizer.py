# app/summarizer.py
from transformers import pipeline
from app.db import SessionLocal, Article
from datetime import datetime

# load a small summarizer (takes some time)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_pending():
    db = SessionLocal()
    pending = db.query(Article).filter(Article.summary == None).limit(20).all()
    for a in pending:
        text = (a.title + ". " + (a.content or ""))[:4000]  # limit token length
        res = summarizer(text, max_length=80, min_length=20, truncation=True)
        a.summary = res[0]['summary_text']
        a.summary_generated_at = datetime.utcnow()
        db.add(a)
    db.commit(); db.close()
    return len(pending)
