from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app.models.user_data import UserDataModel
from app.models.category import CategoryModel

# UserDataModel defined as SQLAlchemy model
# Assuming UserDataModel is already defined

# Assuming this is your AI model's suggest_category method
class AIModel:
    def preprocess_data(self, user_data: UserDataModel) -> Dict[str, Any]:
        # Example preprocessing logic
        processed_data = {
            "user_interests": user_data.interests or [],
            "search_history": user_data.search_history or [],
            "interaction_count": len(user_data.interactions) if user_data.interactions else 0,
        }
        return processed_data

    def suggest_category(self, db: Session, user_id: int) -> Dict[str, Any]:
        # Fetch the user data from the database
        user_data = db.query(UserDataModel).filter(UserDataModel.user_id == user_id).first()

        if not user_data:
            print(f"No user data found for user_id: {user_id}")
            return {
                "name": "Default Category",
                "description": "No user data found, showing default category",
                "suggested_tags": []
            }

        # Process interactions that can be either strings or dictionaries
        processed_interactions = []
        if user_data.interactions:
            for interaction in user_data.interactions:
                if isinstance(interaction, str):
                    processed_interactions.append(interaction)
                elif isinstance(interaction, dict):
                    interaction_type = interaction.get("interaction_type", "")
                    category_id = interaction.get("category_id", "")
                    processed_interactions.append(f"{interaction_type} on category {category_id}")

        # Use processed_interactions for further logic
        if "laptops" in user_data.search_history:
            return {
                "name": "Laptops & Accessories",
                "description": "Suggested based on your interest in laptops",
                "suggested_tags": ["laptops", "accessories"]
            }
        
        return {
            "name": "General Technology",
            "description": "Suggested based on general tech interest",
            "suggested_tags": ["tech", "gadgets"]
        }


# Initialize the AI model
ai_model = AIModel()
