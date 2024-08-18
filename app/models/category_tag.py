from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import BaseModel

class CategoryTagModel(BaseModel):
    __tablename__ = 'category_tags'

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    tag = Column(String(50), nullable=False, index=True)

    category = relationship("CategoryModel", back_populates="tags")
