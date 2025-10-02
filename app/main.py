# app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
from app.db import init_db, SessionLocal, Article
from app.scheduler import schedule_jobs

app = FastAPI()
init_db()
schedule_jobs()

env = Environment(loader=FileSystemLoader("app/templates"))

@app.get("/", response_class=HTMLResponse)
def index():
    db = SessionLocal()
    items = db.query(Article).order_by(Article.published_at.desc()).limit(50).all()
    db.close()
    template = env.get_template("index.html")
    return template.render(items=items)

@app.get("/api/summaries")
def summaries():
    db = SessionLocal()
    rows = db.query(Article).order_by(Article.published_at.desc()).limit(100).all()
    db.close()
    return [{"id":r.id,"title":r.title,"summary":r.summary,"url":r.url,"source":r.source,"published_at":r.published_at.isoformat() if r.published_at else None} for r in rows]
