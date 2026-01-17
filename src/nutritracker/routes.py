from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func
from src.db.database import get_db
from src.db.models import Ingredient, IngredientSize
from src.middleware.jwt_methods import get_current_user
from src.nutritracker.schemas import (
    NutritionCalculateRequest,
    NutritionCalculateResponse
)
from src.nutrition.utils import resolve_weight
from src.nutrition.strategies.calories import CaloriesCalculator
from src.nutrition.strategies.protein import ProteinCalculator
from src.nutrition.strategies.fat import FatCalculator
from src.nutrition.strategies.carbs import CarbsCalculator
from src.nutrition.strategies.fiber import FiberCalculator

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

    strategies = [
        CaloriesCalculator(),
        ProteinCalculator(),
        FatCalculator(),
        CarbsCalculator(),
        FiberCalculator(),
    ]

    totals = {}
    items = {}

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

        weight_g = await resolve_weight(item, ingredient, session)
        if not weight_g:
            raise HTTPException(
                status_code=400,
                detail="Provide weight_g or count + size_label"
            )

        name = ingredient.name
        items.setdefault(name, {})

        for strategy in strategies:
            value = round(strategy.calculate(ingredient, weight_g), 2)
            key = strategy.nutrition_type().value

            items[name][key] = (
                items[name].get(key, 0) + value
            )

            totals[key] = totals.get(key, 0) + value

    return NutritionCalculateResponse(
        totals={k: round(v, 2) for k, v in totals.items()},
        items=items
    )
