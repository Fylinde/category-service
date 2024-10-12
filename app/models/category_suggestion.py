from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from datetime import datetime
from app.database import BaseModel
from sqlalchemy.orm import relationship


class CategorySuggestionModel(BaseModel):
    __tablename__ = 'category_suggestions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    trending_score = Column(Float, default=0.0)
    suggested_by_ai = Column(Boolean, default=True)  # Whether this category was suggested by AI
    status = Column(String(50), default='pending')  # pending, approved, or rejected

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
