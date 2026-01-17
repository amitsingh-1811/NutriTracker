from enum import Enum

class NutritionType(str, Enum):
    CALORIES = "calories"
    PROTEIN = "protein"
    FAT = "fat"
    CARBS = "carbs"
    FIBER = "fiber"
