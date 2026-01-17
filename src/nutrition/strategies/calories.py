from src.nutrition.enums import NutritionType
from .base import NutritionCalculatorStrategy

class CaloriesCalculator(NutritionCalculatorStrategy):

    def nutrition_type(self) -> NutritionType:
        return NutritionType.CALORIES

    def calculate(self, ingredient, weight_g: float) -> float:
        if not ingredient.calories_per_100g:
            return 0.0
        return (weight_g * ingredient.calories_per_100g) / 100
