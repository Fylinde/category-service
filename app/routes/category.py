from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud.category import create_category, get_category, get_categories, update_category, delete_category, ai_suggested_category, get_category_by_id, save_suggested_category, list_all_categories
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse, MoveCategoryRequest, CategorySuggestionResponse, CategoryWithSubcategories
from typing import List
from app.database import get_db
from app.crud import category as crud
#from app.models.category import CategoryModel
#from app.utils.slug_utils import generate_slug
from app.services.ai import ai_model
from app.schemas.user_data import UserDataCreate
router = APIRouter()



@router.post("/", response_model=CategoryResponse)
def create_new_category(category: CategoryCreate, db: Session = Depends(get_db)):
    if category.is_suggested:
        suggested_category = ai_suggested_category(db=db, category=category)
        if not suggested_category:
            raise HTTPException(status_code=400, detail="AI suggested category validation failed")
        return suggested_category

    return create_category(db=db, category=category)

@router.get("/categories/{category_id}", response_model=CategoryWithSubcategories)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = get_category_with_subcategories(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    updated_category = crud.update_category(db, category_id, category)
    if updated_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category

@router.delete("/{category_id}", response_model=CategoryResponse)
def delete_existing_category(category_id: int, db: Session = Depends(get_db)):
    db_category = delete_category(db=db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.get("/{category_id}/subcategories", response_model=CategoryResponse)
def get_category_with_subcategories(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category_with_subcategories(db, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category_with_subcategories(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}/move", response_model=CategoryResponse)
def move_category(category_id: int, move_request: MoveCategoryRequest, db: Session = Depends(get_db)):
    moved_category = crud.move_category(db, category_id, move_request.new_parent_id)
    if not moved_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return moved_category

@router.get("/tree/{category_id}", response_model=CategoryResponse)
def get_category_tree(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category_with_subcategories(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/slug/{slug}", response_model=CategoryResponse)
def get_category_by_slug(slug: str, db: Session = Depends(get_db)):
    category = crud.get_category_by_slug(db, slug)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/suggest/", response_model=CategorySuggestionResponse)
def suggest_category(user_data_create: UserDataCreate, db: Session = Depends(get_db)):
    # Pass user_id along with user_data to the AI model
    suggested_data = ai_model.suggest_category(db, user_data_create.user_id)

    if not suggested_data:
        raise HTTPException(status_code=404, detail="Category not found")
    return suggested_data



@router.post("/validate/{id}")
async def validate_category(id: int, validation_status: bool, db: Session = Depends(get_db)):
    category = get_category_by_id(db, id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    # Perform validation logic here
    return {"status": "success"}


@router.get("/", response_model=List[CategoryResponse])
def list_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return list_all_categories(db, skip=skip, limit=limit)


