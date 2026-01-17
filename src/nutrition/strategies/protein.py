from .base import NutritionCalculatorStrategy
from src.nutrition.enums import NutritionType

class ProteinCalculator(NutritionCalculatorStrategy):

    def nutrition_type(self) -> NutritionType:
        return NutritionType.PROTEIN

    def calculate(self, ingredient, weight_g: float) -> float:
        if not ingredient.protein_per_100g:
            return 0.0
        return (weight_g * ingredient.protein_per_100g) / 100
