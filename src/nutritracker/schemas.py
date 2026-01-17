from pydantic import BaseModel
from typing import Optional, List, Dict

class NutritionItemInput(BaseModel):
    ingredient_name: str
    weight_g: Optional[float] = None
    count: Optional[int] = None
    size_label: Optional[str] = None

class NutritionCalculateRequest(BaseModel):
    items: List[NutritionItemInput]

class NutritionCalculateResponse(BaseModel):
    totals: Dict[str, float]  # calories, protein, fat, etc.
    items: Dict[str, Dict[str, float]]