from pydantic import BaseModel

class CategoryTagBase(BaseModel):
    category_id: int
    tag: str

class CategoryTagCreate(CategoryTagBase):
    pass

class CategoryTagDelete(CategoryTagBase):
    pass
