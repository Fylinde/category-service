from sqlalchemy.orm import Session
from app.models.category import CategoryModel
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.utils.slug_utils import generate_slug
from app.models.category_analytics import CategoryAnalyticsModel
from fastapi import HTTPException
import requests


BRAND_SERVICE_URL = "http://brand-service:8010/brands"


def validate_brand_id(brand_id: int):
    """
    Validate if a brand exists by making an API call to brand-service.
    :param brand_id: The ID of the brand to validate.
    :return: True if the brand exists, otherwise raises HTTPException.
    """
    if brand_id:
        response = requests.get(f"{BRAND_SERVICE_URL}/{brand_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Brand with ID {brand_id} not found.")
    return True
def create_category(db: Session, category_data: dict, slug: str):
    """
    Create a new category in the database.
    """
    category_data["slug"] = slug
    new_category = CategoryModel(**category_data)
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return new_category

def get_category(db: Session, category_id: int):
    return db.query(CategoryModel).filter(CategoryModel.id == category_id).first()

def update_category(db: Session, category_id: int, category_data: dict):
    """
    Update an existing category by its ID.
    """
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in category_data.items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)

    return category

def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category

def get_categories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(CategoryModel).offset(skip).limit(limit).all()

def get_category_with_subcategories(db: Session, category_id: int):
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    return category

def move_category(db: Session, category_id: int, new_parent_id: int):
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if category:
        category.parent_id = new_parent_id
        db.commit()
        db.refresh(category)
    return category

def get_category_by_slug(db: Session, slug: str) -> CategoryModel:
    return db.query(CategoryModel).filter(CategoryModel.slug == slug).first()


def ai_suggested_category(db: Session, category: CategoryCreate) -> CategoryModel:
    # Implement any additional validation logic here
    new_category = CategoryModel(name=category.name, description=category.description, parent_id=category.parent_id)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def save_suggested_category(db: Session, category_data: dict) -> CategoryModel:
    new_category = CategoryModel(**category_data)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

def get_category_by_id(db: Session, category_id: int):
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

def get_category_with_brand(db: Session, category_id: int):
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    brand = None
    if category.brand_id:
        # Make an API call to the brand-service to fetch brand details
        response = requests.get(f"{BRAND_SERVICE_URL}/brands/{category.brand_id}")
        if response.status_code == 200:
            brand = response.json()
        else:
            brand = None  # Return None if brand is not found

    return {
        "category": category,
        "brand": brand  # This will be None if brand is not found or not provided
    }


def list_all_categories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(CategoryModel).offset(skip).limit(limit).all()

