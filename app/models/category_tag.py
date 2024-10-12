from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import BaseModel

class CategoryTagModel(BaseModel):
    __tablename__ = 'category_tags'

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    tag = Column(String(50), nullable=False, index=True)
    tag_weight = Column(Float, default=0.0)  # Tag weight for prioritizing

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("CategoryModel", back_populates="tags")
