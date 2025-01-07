
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class URLItem(Base):
    __tablename__ = "short_urls"

    id = Column(Integer, primary_key=True, index=True)
    short_id = Column(String, unique=True, index=True)
    full_url = Column(String)
    clicks = Column(Integer, default=0)  # Поле для подсчета кликов
    created_at = Column(DateTime, default=datetime.utcnow)  # Время создания
    expires_at = Column(DateTime)  # Время истечения
