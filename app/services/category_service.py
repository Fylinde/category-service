from sqlalchemy.orm import Session
from app.models.category import CategoryModel
from app.models.category_analytics import CategoryAnalyticsModel
from app.models.user_data import UserDataModel

def recalculate_trending_scores(db: Session):
    """
    Recalculate the trending score for all categories based on user engagement.
    """
    categories = db.query(CategoryModel).all()
    for category in categories:
        # Fetch analytics data for this category
        analytics = db.query(CategoryAnalyticsModel).filter(CategoryAnalyticsModel.category_id == category.id).one_or_none()

        if analytics:
            # Simple formula: Engagement Rate * Clicks + Impressions * 0.1
            category.trending_score = (analytics.engagement_rate * analytics.clicks) + (analytics.impressions * 0.1)

        db.commit()

def calculate_user_interest_score(user_id: int, db: Session):
    """
    Calculate interest score for a user based on their interaction and purchase history.
    """
    user_data = db.query(UserDataModel).filter(UserDataModel.user_id == user_id).one_or_none()

    if not user_data:
        return []

    interest_scores = {}
    # Analyze search history and interactions
    search_terms = user_data.search_history.split(',') if user_data.search_history else []
    interactions = user_data.interactions.split(',') if user_data.interactions else []

    for term in search_terms:
        categories = db.query(CategoryModel).filter(CategoryModel.name.ilike(f'%{term}%')).all()
        for category in categories:
            if category.id not in interest_scores:
                interest_scores[category.id] = 0
            interest_scores[category.id] += 1  # Increase score based on search term match

    for interaction in interactions:
        category = db.query(CategoryModel).filter(CategoryModel.name.ilike(f'%{interaction}%')).one_or_none()
        if category:
            if category.id not in interest_scores:
                interest_scores[category.id] = 0
            interest_scores[category.id] += 2  # Interactions carry more weight

    return sorted(interest_scores.items(), key=lambda x: x[1], reverse=True)

def increment_category_impression(category_id: int, db: Session):
    """
    Increment the impression count for a given category.
    """
    analytics = db.query(CategoryAnalyticsModel).filter(CategoryAnalyticsModel.category_id == category_id).one_or_none()
    if analytics:
        analytics.impressions += 1
    else:
        new_analytics = CategoryAnalyticsModel(category_id=category_id, impressions=1)
        db.add(new_analytics)
    
    db.commit()

def increment_category_clicks(category_id: int, db: Session):
    """
    Increment the click count for a given category.
    """
    analytics = db.query(CategoryAnalyticsModel).filter(CategoryAnalyticsModel.category_id == category_id).one_or_none()
    if analytics:
        analytics.clicks += 1
    else:
        new_analytics = CategoryAnalyticsModel(category_id=category_id, clicks=1)
        db.add(new_analytics)
    
    db.commit()
