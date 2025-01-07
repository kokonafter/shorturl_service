import string
import random
from typing import Optional
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
from models import URLItem
from datetime import datetime, timedelta

Base.metadata.create_all(bind=engine)

app = FastAPI()

class URLCreate(BaseModel):
    url: HttpUrl

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.post("/shorten")
def shorten_url(item: URLCreate, db: Session = Depends(get_db)):
    expires_at = datetime.utcnow() + timedelta(days=7)  # Срок действия 7 дней
    for _ in range(10):
        short_id = generate_short_id()
        existing = db.query(URLItem).filter(URLItem.short_id == short_id).first()
        if not existing:
            new_item = URLItem(
                short_id=short_id,
                full_url=str(item.url),
                expires_at=expires_at
            )
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
            return {
                "short_url": f"http://localhost:8000/{short_id}",
                "expires_at": expires_at
            }
    raise HTTPException(status_code=500, detail="Не удалось сгенерировать короткую ссылку")

@app.get("/{short_id}")
def redirect_to_full(short_id: str, db: Session = Depends(get_db)):
    url_item = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")
    # Проверяем, истек ли срок действия
    if url_item.expires_at and url_item.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Срок действия ссылки истек")
    # Увеличиваем счетчик кликов
    url_item.clicks += 1
    db.commit()
    return RedirectResponse(url=url_item.full_url)

@app.get("/stats/{short_id}")
def get_stats(short_id: str, db: Session = Depends(get_db)):
    url_item = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")
    return {
        "short_id": url_item.short_id,
        "full_url": url_item.full_url
    }

@app.get("/stats")
def get_all_stats(db: Session = Depends(get_db)):
    links = db.query(URLItem).all()
    return [
        {
            "short_id": link.short_id,
            "full_url": link.full_url,
            "clicks": link.clicks,
            "created_at": link.created_at,
            "expires_at": link.expires_at
        }
        for link in links
    ]

@app.get("/")
def read_root():
    return {"message": "Welcome to the Short URL service!"}

@app.delete("/cleanup")
def cleanup_expired_links(db: Session = Depends(get_db)):
    expired_links = db.query(URLItem).filter(URLItem.expires_at < datetime.utcnow()).all()
    for link in expired_links:
        db.delete(link)
    db.commit()
    return {"message": f"{len(expired_links)} истекших ссылок удалено"}
