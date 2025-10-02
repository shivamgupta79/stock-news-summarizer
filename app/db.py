
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

DB_URL = "sqlite:///./data.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, unique=True, index=True)
    source = Column(String)
    published_at = Column(DateTime)
    content = Column(Text)
    summary = Column(Text)
    summary_generated_at = Column(DateTime)

def init_db():
    Base.metadata.create_all(bind=engine)
