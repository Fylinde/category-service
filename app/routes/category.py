from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse, MoveCategoryRequest, CategorySuggestionResponse, CategoryWithSubcategories
from typing import List
from app.crud import category as category_crud
from app.services.ai import AIModel
from app.services.category_service import recalculate_trending_scores, calculate_user_interest_score, increment_category_clicks, increment_category_impression
from app.models.category import CategoryModel
from app.utils.slug_utils import generate_slug
import requests
from app.schemas.user_data import UserDataCreate
from app.crud.category import get_category_with_brand
from app.schemas.category import CategoryWithBrandResponse

router = APIRouter()

BRAND_SERVICE_URL = "http://brand-service:8010/brands"
SEARCH_SERVICE_URL = "http://search-service:8011"

# Helper function to validate brand existence via Brand-Service API
def validate_brand(brand_id: int):
    if brand_id:
        response = requests.get(f"{BRAND_SERVICE_URL}/{brand_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Brand with ID {brand_id} not found.")
    return True

def create_unique_slug(db: Session, name: str) -> str:
    """
    Generates a unique slug for the category by checking for existing slugs in the database.
    """
    base_slug = generate_slug(name)
    slug = base_slug
    counter = 1
    while db.query(CategoryModel).filter_by(slug=slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    # Generate slug from category name
    slug = generate_slug(category.name)
    
    # Create the category in the database
    new_category = category_crud.create_category(db, {**category.dict(), "slug": slug})
    
    # After the category is created, index it in the search-service
    try:
        requests.post(f"{SEARCH_SERVICE_URL}/index", json={
            "id": new_category.id,
            "name": new_category.name,
            "description": new_category.description,
            "slug": new_category.slug,  # Include slug
            # Add other fields as needed
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error indexing category in search: {str(e)}")
    
    return new_category


@router.get("/{category_id}", response_model=CategoryWithSubcategories)
def read_category(category_id: int, db: Session = Depends(get_db)):
    """
    Read a specific category with its subcategories.
    """
    db_category = category_crud.get_category_with_subcategories(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    category_data = category.dict(exclude_unset=True)
    
    # If the name is updated, generate a new slug
    if "name" in category_data:
        category_data["slug"] = generate_slug(category_data["name"])
    
    # Update the category in the database
    updated_category = category_crud.update_category(db, category_id, category_data)
    
    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Update the index in search-service
    try:
        requests.post(f"{SEARCH_SERVICE_URL}/index", json={
            "id": updated_category.id,
            "name": updated_category.name,
            "description": updated_category.description,
            "slug": updated_category.slug,  # Include slug in the search index update
            # Add other fields as needed
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating category index in search: {str(e)}")
    
    return updated_category

@router.delete("/{category_id}", response_model=CategoryResponse)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    deleted_category = category_crud.delete_category(db, category_id)
    
    if not deleted_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Remove from the search index
    try:
        requests.delete(f"{SEARCH_SERVICE_URL}/index/{category_id}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting category from search index: {str(e)}")
    
    return deleted_category

@router.get("/", response_model=List[CategoryResponse])
def list_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    List all categories.
    """
    return category_crud.list_all_categories(db, skip=skip, limit=limit)

@router.put("/{category_id}/move", response_model=CategoryResponse)
def move_category(category_id: int, move_request: MoveCategoryRequest, db: Session = Depends(get_db)):
    """
    Move a category under a new parent category.
    """
    moved_category = category_crud.move_category(db, category_id, move_request.new_parent_id)
    if not moved_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return moved_category

@router.get("/tree/{category_id}", response_model=CategoryResponse)
def get_category_tree(category_id: int, db: Session = Depends(get_db)):
    """
    Get a category tree including subcategories.
    """
    category = category_crud.get_category_with_subcategories(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/slug/{slug}", response_model=CategoryResponse)
def get_category_by_slug(slug: str, db: Session = Depends(get_db)):
    """
    Get a category by its slug.
    """
    category = category_crud.get_category_by_slug(db, slug)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/suggest/", response_model=CategorySuggestionResponse)
def suggest_category(user_data_create: UserDataCreate, db: Session = Depends(get_db)):
    """
    Suggest categories based on user data using the AI model.
    """
    suggested_data = AIModel.suggest_category(db, user_data_create.user_id)

    if not suggested_data:
        raise HTTPException(status_code=404, detail="Category not found")
    return suggested_data

@router.post("/validate/{id}")
async def validate_category(id: int, validation_status: bool, db: Session = Depends(get_db)):
    """
    Validate a category.
    """
    category = category_crud.get_category_by_id(db, id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"status": "success"}

@router.post("/recalculate-trending/")
def recalculate_trending(db: Session = Depends(get_db)):
    """
    Recalculate the trending score for all categories.
    """
    recalculate_trending_scores(db)
    return {"message": "Trending scores recalculated."}

@router.get("/personalized/{user_id}")
def get_personalized_categories(user_id: int, db: Session = Depends(get_db)):
    """
    Get personalized categories based on user behavior.
    """
    scores = calculate_user_interest_score(user_id, db)
    personalized_categories = [db.query(CategoryModel).get(score[0]) for score in scores]
    return personalized_categories

@router.post("/{category_id}/view")
def track_category_view(category_id: int, db: Session = Depends(get_db)):
    """
    Track a category impression (view).
    """
    increment_category_impression(category_id, db)
    return {"message": "Impression recorded."}

@router.post("/{category_id}/click")
def track_category_click(category_id: int, db: Session = Depends(get_db)):
    """
    Track when a category is clicked.
    """
    increment_category_clicks(category_id, db)
    return {"message": "Click recorded."}

@router.get("/{parent_id}/subcategories")
def get_subcategories(parent_id: int, db: Session = Depends(get_db)):
    """
    Fetch all subcategories for a given parent category.
    """
    subcategories = db.query(CategoryModel).filter(CategoryModel.parent_id == parent_id).all()
    return subcategories

@router.get("/{category_id}/seo")
def get_seo_data(category_id: int, db: Session = Depends(get_db)):
    """
    Get SEO data for a category.
    """
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return {
        "meta_title": category.meta_title,
        "meta_description": category.meta_description,
        "meta_keywords": category.meta_keywords
    }

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    category = category_crud.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category_with_brand_endpoint(category_id: int, db: Session = Depends(get_db)):
    return get_category_with_brand(db, category_id)

@router.get("/search", response_model=List[CategoryResponse])
def search_categories(query: str):
    try:
        response = requests.get(f"{SEARCH_SERVICE_URL}/search", params={"q": query})
        response.raise_for_status()
        return response.json()  # Assuming search-service returns category-like JSON
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching categories: {str(e)}")
