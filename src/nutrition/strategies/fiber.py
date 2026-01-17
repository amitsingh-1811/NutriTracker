from .base import NutritionCalculatorStrategy
from src.nutrition.enums import NutritionType

class FiberCalculator(NutritionCalculatorStrategy):

    def nutrition_type(self) -> NutritionType:
        return NutritionType.FIBER

    def calculate(self, ingredient, weight_g: float) -> float:
        if not ingredient.fiber_per_100g:
            return 0.0
        return (weight_g * ingredient.fiber_per_100g) / 100
