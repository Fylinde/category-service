from pydantic import BaseModel
from typing import Optional, List

class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    brand_id: Optional[int] = None  # Optional brand reference


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None
    is_suggested: Optional[bool] = False  # Indicates if the category is AI-suggested
    brand_id: Optional[int] = None  # Make this field optional

    class Config:
        orm_mode = True
        
class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
    brand_id: Optional[int] = None
    trending_score: Optional[float] = None
    popularity_index: Optional[float] = None

    class Config:
        orm_mode = True

class BrandResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        
class CategoryWithBrandResponse(BaseModel):
    id: int
    name: str
    description: str
    brand: Optional[BrandResponse]  # Make brand optional

    class Config:
        orm_mode = True        
        
class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    subcategories: List['CategoryResponse'] = []
    trending_score: Optional[float] = None
    popularity_index: Optional[float] = None
    user_interest_score: Optional[float] = None
   #brand: Optional[BrandResponse]
    
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
