from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func
from src.db.database import get_db
from src.db.models import Ingredient, IngredientSize
from src.middleware.jwt_methods import get_current_user
from src.nutritracker.schemas import (
    NutritionCalculateRequest,
    NutritionCalculateResponse,
    NutritionItemResult
)

router = APIRouter(
    prefix="/nutrition",
    tags=["Nutrition"]
)
@router.post(
    "/calculate",
    response_model=NutritionCalculateResponse,
    status_code=status.HTTP_201_CREATED
)
async def calculate_nutrition(
    payload: NutritionCalculateRequest,
    session: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    total_calories = 0.0
    results_map = {}

    for item in payload.items:
        result = await session.execute(
            select(Ingredient).where(
                func.lower(Ingredient.name) == item.ingredient_name.lower(),
                Ingredient.is_active == True
            )
        )
        ingredient = result.scalar_one_or_none()

        if not ingredient:
            raise HTTPException(
                status_code=404,
                detail=f"Ingredient '{item.ingredient_name}' not found"
            )

        calories = 0.0
        if item.weight_g is not None:
            calories = (item.weight_g * ingredient.calories_per_100g) / 100
        elif item.count is not None and item.size_label is not None:
            size_result = await session.execute(
                select(IngredientSize).where(
                    IngredientSize.ingredient_id == ingredient.id,
                    func.lower(IngredientSize.label) == item.size_label.lower()
                )
            )
            size = size_result.scalar_one_or_none()
            if not size:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid size '{item.size_label}' for {ingredient.name}"
                )

            calories = (
                item.count * size.weight_g * ingredient.calories_per_100g
            ) / 100
        else:
            raise HTTPException(
                status_code=400,
                detail="Provide weight_g or count + size_label"
            )

        calories = round(calories, 2)
        total_calories += calories
        if ingredient.name in results_map:
            results_map[ingredient.name] += calories
        else:
            results_map[ingredient.name] = calories

    return NutritionCalculateResponse(
        total_calories=round(total_calories, 2),
        items=results_map
    )
