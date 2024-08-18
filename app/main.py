from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.routes.category import router as category_router
from app.database import get_db, engine, BaseModel
from app.models.category import CategoryModel
from app.models.user_data import UserDataModel

# Initialize FastAPI with metadata for Swagger
app = FastAPI(
    title="Category Service API",
    description="API documentation for the Category Service, which manages categories and related user data.",
    version="1.0.0",
    openapi_tags=[
        {"name": "categories", "description": "Operations related to product categories"},
        {"name": "user_data", "description": "Operations related to user data management"},
    ],
)

# Initialize database
BaseModel.metadata.create_all(bind=engine)

# Register routers
app.include_router(category_router, prefix="/categories", tags=["categories"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Category Service"}

# Add the dummy data creation route
@app.post("/create_dummy_user_data/", tags=["user_data"])
def create_dummy_user_data(db: Session = Depends(get_db)):
    # Create dummy data for user_id = 1
    dummy_data = UserDataModel(
        user_id=1,
        search_history=["laptops", "smartphones"],
        interactions=["clicked on laptops", "viewed smartphones"]
    )
    db.add(dummy_data)
    db.commit()
    db.refresh(dummy_data)
    return {"status": "success", "data": dummy_data}
