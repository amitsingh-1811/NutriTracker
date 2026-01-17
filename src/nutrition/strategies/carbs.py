from .base import NutritionCalculatorStrategy
from src.nutrition.enums import NutritionType

class CarbsCalculator(NutritionCalculatorStrategy):

    def nutrition_type(self) -> NutritionType:
        return NutritionType.CARBS

    def calculate(self, ingredient, weight_g: float) -> float:
        if not ingredient.carbs_per_100g:
            return 0.0
        return (weight_g * ingredient.carbs_per_100g) / 100
