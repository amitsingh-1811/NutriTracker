from pydantic import BaseModel
from typing import Optional, List, Dict

class NutritionItemInput(BaseModel):
    ingredient_name: str
    weight_g: Optional[float] = None
    count: Optional[int] = None
    size_label: Optional[str] = None

class NutritionCalculateRequest(BaseModel):
    items: List[NutritionItemInput]

class NutritionItemResult(BaseModel):
    ingredient_name: str
    calories: float

class NutritionCalculateResponse(BaseModel):
    total_calories: float
    items: Dict[str, float]
