from sqlalchemy import Column, Integer, String
from app.database import BaseModel

class UserDataModel(BaseModel):
    __tablename__ = 'user_data'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # Just storing user_id
    search_history = Column(String, nullable=True)
    interactions = Column(String, nullable=True)

    # No relationship with UserModel since we're not defining it in this service
