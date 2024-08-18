from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from app.database import BaseModel
from app.models.category_tag import CategoryTagModel

class CategoryModel(BaseModel):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    trending_score = Column(Float, default=0.0)  # Dynamic scoring field
    popularity_index = Column(Float, default=0.0)  # AI-driven popularity index
    user_interest_score = Column(Float, default=0.0)  # Based on user behavior
    is_validated = Column(Boolean, default=False)  # New field for validation status

    parent = relationship("CategoryModel", remote_side=[id], backref="subcategories")
    #products = relationship("ProductModel", back_populates="category")

    # Add the relationship to CategoryTagModel
    tags = relationship("CategoryTagModel", back_populates="category", cascade="all, delete-orphan")
