from sqlalchemy.orm import Session
from app.models import CategoryModel
#from app.utils.slug import generate_slug
from app.utils.slug_utils import generate_slug
from app.database import SessionLocal
import os

# Manually override the DATABASE_URL for local testing
os.environ['DATABASE_URL'] = "postgresql://fylinde:Sylvian@localhost:5432/category_service_db"

# Create a new database session
db = SessionLocal()

def resolve_duplicate_slugs(db: Session):
    categories = db.query(CategoryModel).order_by(CategoryModel.id).all()
    slug_counter = {}

    for category in categories:
        original_slug = generate_slug(category.name)
        slug = original_slug

        count = slug_counter.get(original_slug, 0)
        while db.query(CategoryModel).filter(CategoryModel.slug == slug).first():
            count += 1
            slug = f"{original_slug}-{count}"

        slug_counter[original_slug] = count
        category.slug = slug

    db.commit()

# Run this function before applying the migration
try:
    resolve_duplicate_slugs(db)
finally:
    db.close()
