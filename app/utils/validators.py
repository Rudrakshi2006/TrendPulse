from app.models.analysis_models import UserInput
from pydantic import ValidationError
from typing import Optional

def validate_user_input(data: dict) -> Optional[UserInput]:
    try:
        user_input = UserInput(**data)
        return user_input
    except ValidationError as e:
        return None
