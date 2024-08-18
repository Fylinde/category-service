from pydantic import BaseModel, Field, field_validator,ValidationError
from typing import Optional, List, Union


class UserData(BaseModel):
    search_history: List[str]
    interactions: List[str]    

class InteractionDict(BaseModel):
    category_id: int
    interaction_type: str

class UserDataCreate(BaseModel):
    user_id: int
    search_history: Optional[List[str]] = None
    interactions: Optional[List[Union[str, InteractionDict]]] = None

    class Config:
        from_attributes = True  # This replaces `orm_mode` in Pydantic v2
        
class UserDataResponse(BaseModel):
    id: int  # The ID of the user data entry
    user_id: int  # The ID of the user
    search_history: Optional[List[str]] = None  # Optional list of search history strings
    interactions: Optional[List[str]] = None  # Optional list of interaction strings

    class Config:
        orm_mode = True
        