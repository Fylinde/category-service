from sqlalchemy.orm import Session
from app.models.category_tag import CategoryTagModel
from app.schemas.category_tag import CategoryTagCreate, CategoryTagDelete

def add_category_tag(db: Session, category_tag: CategoryTagCreate):
    db_category_tag = CategoryTagModel(**category_tag.dict())
    db.add(db_category_tag)
    db.commit()
    db.refresh(db_category_tag)
    return db_category_tag

def remove_category_tag(db: Session, category_tag: CategoryTagDelete):
    db_category_tag = db.query(CategoryTagModel).filter_by(category_id=category_tag.category_id, tag=category_tag.tag).first()
    if db_category_tag:
        db.delete(db_category_tag)
        db.commit()
    return db_category_tag
