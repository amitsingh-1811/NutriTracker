from abc import ABC, abstractmethod
from src.nutrition.enums import NutritionType

class NutritionCalculatorStrategy(ABC):

    @abstractmethod
    def nutrition_type(self) -> NutritionType:
        pass

    @abstractmethod
    def calculate(self, ingredient, weight_g: float) -> float:
        pass
