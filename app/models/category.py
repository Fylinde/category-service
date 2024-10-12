from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import BaseModel
from app.models.category_tag import CategoryTagModel
import enum


class CategoryType(enum.Enum):
    STANDARD = "standard"
    TRENDING = "trending"
    AI_RECOMMENDED = "ai_recommended"  # For categories generated based on recommendations


class CategoryModel(BaseModel):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    description = Column(String(500), nullable=True)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    brand_id = Column(Integer, nullable=True)
    trending_score = Column(Float, default=0.0)
    popularity_index = Column(Float, default=0.0)
    user_interest_score = Column(Float, default=0.0)
    is_validated = Column(Boolean, default=False)
    is_suggested = Column(Boolean, default=False)
    category_type = Column(Enum(CategoryType), default=CategoryType.STANDARD)  # Category type

    # New Fields
    auto_generated = Column(Boolean, default=False)  # Indicates if AI generated the category
    dynamic_rank = Column(Integer, default=1000)  # Real-time rank, updated by analytics or AI
    external_trend_data = Column(String, nullable=True)  # Could store trend data in JSON format
    
    meta_title = Column(String(255), nullable=True)
    meta_description = Column(String(255), nullable=True)
    meta_keywords = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    features = relationship("CategoryFeatureModel", back_populates="category", cascade="all, delete-orphan")
    analytics = relationship("CategoryAnalyticsModel", back_populates="category", cascade="all, delete-orphan")
    parent = relationship("CategoryModel", remote_side=[id], backref="subcategories")
    tags = relationship("CategoryTagModel", back_populates="category", cascade="all, delete-orphan")
    products = relationship("ProductModel", back_populates="category")

    def __repr__(self):
        return f'<Category {self.name}>'
