from pydantic import BaseModel
from typing import Optional, List

class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None
    is_suggested: Optional[bool] = False  # Indicates if the category is AI-suggested

class CategoryUpdate(CategoryBase):
    parent_id: Optional[int] = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    subcategories: List['CategoryResponse'] = []
    trending_score: Optional[float] = None
    popularity_index: Optional[float] = None
    user_interest_score: Optional[float] = None

    class Config:
        orm_mode = True

class MoveCategoryRequest(BaseModel):
    new_parent_id: int
    
class CategorySuggestionResponse(BaseModel):
    name: str
    description: str
    suggested_tags: List[str]

    class Config:
        orm_mode = True    
        
class Category(CategoryBase):
    id: int
    parent_id: Optional[int] = None
    trending_score: Optional[float] = None
    popularity_index: Optional[float] = None
    user_interest_score: Optional[float] = None
    tags: List[str] = []  # List of tags associated with the category

    class Config:
        orm_mode = True          
    
class CategoryWithSubcategories(Category):
    subcategories: List['CategoryWithSubcategories'] = []

    class Config:
        orm_mode = True
