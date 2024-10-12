from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import BaseModel
from sqlalchemy.orm import relationship

class CategoryFeatureModel(BaseModel):
    __tablename__ = 'category_features'

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)  # Add ForeignKey
    feature_start_date = Column(DateTime, nullable=False)
    feature_end_date = Column(DateTime, nullable=True)  # Optional end date for featuring

    # Audit fields
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    category = relationship("CategoryModel", back_populates="features")  # Assuming CategoryModel has 'features' relationship
