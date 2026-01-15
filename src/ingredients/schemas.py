from typing import List, Optional
from pydantic import BaseModel
from src.ingredients.input_mode import InputMode

class IngredientSizeCreate(BaseModel):
    label: str
    weight_g: float

class IngredientSizeRead(BaseModel):
    id: int
    label: str
    weight_g: float

    class Config:
        from_attributes = True

class IngredientSizeUpdate(BaseModel):
    label: Optional[str] = None
    weight_g: Optional[float] = None

class IngredientCreate(BaseModel):
    name: str
    calories_per_100g: Optional[float] = None
    input_mode: InputMode
    is_active: bool = True
    sizes: List[IngredientSizeCreate] = []

class IngredientUpdate(BaseModel):
    name: Optional[str] = None
    calories_per_100g: Optional[float] = None
    input_mode: Optional[InputMode] = None
    is_active: Optional[bool] = None
    sizes: Optional[List[IngredientSizeCreate]] = None

class IngredientRead(BaseModel):
    id: int
    name: str
    calories_per_100g: Optional[float]
    input_mode: InputMode
    is_active: bool

    class Config:
        from_attributes = True
