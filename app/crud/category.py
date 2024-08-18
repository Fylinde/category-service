from sqlalchemy.orm import Session
from app.models.category import CategoryModel
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.utils.slug_utils import generate_slug

def create_category(db: Session, category: CategoryCreate) -> CategoryModel:
    # Generate initial slug
    slug = generate_slug(category.name)

    # Ensure the slug is unique
    existing_slug = db.query(CategoryModel).filter(CategoryModel.slug == slug).first()
    count = 1
    while existing_slug:
        count += 1
        slug = f"{generate_slug(category.name)}-{count}"
        existing_slug = db.query(CategoryModel).filter(CategoryModel.slug == slug).first()

    # Create the category with a unique slug
    db_category = CategoryModel(
        name=category.name,
        description=category.description,
        parent_id=category.parent_id,
        slug=slug,
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_category(db: Session, category_id: int):
    return db.query(CategoryModel).filter(CategoryModel.id == category_id).first()

def update_category(db: Session, category_id: int, category: CategoryUpdate):
    db_category = get_category(db, category_id)
    if db_category:
        for key, value in category.dict(exclude_unset=True).items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
    return db_category

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

def get_category_by_id(db: Session, category_id: int) -> CategoryModel:
    return db.query(CategoryModel).filter(CategoryModel.id == category_id).first()


def list_all_categories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(CategoryModel).offset(skip).limit(limit).all()