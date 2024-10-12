from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from datetime import datetime
from app.database import BaseModel
from sqlalchemy.orm import relationship

class CategoryAnalyticsModel(BaseModel):
    __tablename__ = 'category_analytics'

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)

    # New Real-Time Analytics
    real_time_trending_score = Column(Float, default=0.0)
    social_media_trend_score = Column(Float, default=0.0)  # Trends from external sources

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("CategoryModel", back_populates="analytics")
