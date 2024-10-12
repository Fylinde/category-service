import logging
from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app.models.user_data import UserDataModel
from app.models.category import CategoryModel

logger = logging.getLogger(__name__)

class AIModel:
    def preprocess_data(self, user_data: UserDataModel) -> Dict[str, Any]:
        """
        Preprocess user data to make it usable for the AI recommendation system.
        This includes search history, interactions, and engagement metrics.
        """
        try:
            search_history = user_data.search_history.split(',') if user_data.search_history else []
            interactions = user_data.interactions.split(',') if user_data.interactions else []

            engagement_score = len(search_history) + len(interactions) * 2  # Engagement calculation
            processed_data = {
                "search_history": search_history,
                "interactions": interactions,
                "engagement_score": engagement_score
            }
            return processed_data
        except Exception as e:
            logger.error(f"Error during preprocessing user data: {str(e)}")
            return {
                "search_history": [],
                "interactions": [],
                "engagement_score": 0
            }

    def suggest_category(self, db: Session, user_id: int) -> Dict[str, Any]:
        """
        Suggest categories based on the user data by analyzing search history,
        interaction patterns, and past behaviors.
        """
        try:
            user_data = db.query(UserDataModel).filter(UserDataModel.user_id == user_id).first()

            if not user_data:
                logger.warning(f"No user data found for user_id: {user_id}")
                return {
                    "name": "Default Category",
                    "description": "No user data found, showing default category",
                    "suggested_tags": []
                }

            # Preprocess user data
            processed_data = self.preprocess_data(user_data)

            # Calculate category scores
            category_scores = self.calculate_category_scores(
                db, 
                processed_data["search_history"], 
                processed_data["interactions"], 
                processed_data["engagement_score"]
            )

            top_category = max(category_scores, key=category_scores.get) if category_scores else None

            if top_category:
                return {
                    "name": top_category.name,
                    "description": top_category.description,
                    "suggested_tags": [tag.tag for tag in top_category.tags]  # Assuming CategoryModel has tags
                }

            # Fallback to general recommendation
            return {
                "name": "General Technology",
                "description": "Suggested based on general tech interest",
                "suggested_tags": ["tech", "gadgets"]
            }
        except Exception as e:
            logger.error(f"Error suggesting category for user_id: {user_id}, Error: {str(e)}")
            return {
                "name": "Default Category",
                "description": "An error occurred, showing default category",
                "suggested_tags": []
            }

    def calculate_category_scores(self, db: Session, search_history: List[str], interactions: List[str], engagement_score: int) -> Dict[CategoryModel, float]:
        """
        Calculate a score for each category based on search history, interactions, and engagement.
        """
        category_scores = {}
        try:
            categories = db.query(CategoryModel).all()

            for category in categories:
                score = 0.0

                # Match with search history
                for search in search_history:
                    if search.lower() in category.name.lower() or search.lower() in category.description.lower():
                        score += 2

                # Match with interactions
                for interaction in interactions:
                    if interaction.lower() in category.name.lower() or interaction.lower() in category.description.lower():
                        score += 3

                # Boost score for trending and popular categories
                score += category.trending_score * 0.5
                score += category.popularity_index * 0.5

                # Engagement influence
                score += engagement_score * 0.1

                category_scores[category] = score

            return category_scores
        except Exception as e:
            logger.error(f"Error calculating category scores: {str(e)}")
            return {}

    def recommend_top_categories(self, db: Session, user_id: int, top_n: int = 5) -> List[Dict[str, Any]]:
        """
        Recommend the top N categories for the user based on their behavior and engagement.
        """
        try:
            user_data = db.query(UserDataModel).filter(UserDataModel.user_id == user_id).first()

            if not user_data:
                return []

            processed_data = self.preprocess_data(user_data)
            category_scores = self.calculate_category_scores(
                db, 
                processed_data["search_history"], 
                processed_data["interactions"], 
                processed_data["engagement_score"]
            )

            # Sort the categories by score and pick the top N
            sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
            top_categories = sorted_categories[:top_n]

            return [
                {
                    "name": category.name,
                    "description": category.description,
                    "suggested_tags": [tag.tag for tag in category.tags]
                }
                for category, score in top_categories
            ]
        except Exception as e:
            logger.error(f"Error recommending top categories for user_id: {user_id}, Error: {str(e)}")
            return []
