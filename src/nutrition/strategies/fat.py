from .base import NutritionCalculatorStrategy
from src.nutrition.enums import NutritionType

class FatCalculator(NutritionCalculatorStrategy):

    def nutrition_type(self) -> NutritionType:
        return NutritionType.FAT

    def calculate(self, ingredient, weight_g: float) -> float:
        if not ingredient.fat_per_100g:
            return 0.0
        return (weight_g * ingredient.fat_per_100g) / 100
