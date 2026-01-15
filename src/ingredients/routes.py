from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from src.db.database import get_db
from src.accounts.user_roles import UserRole
from src.db.models import Ingredient, IngredientSize
from .schemas import (
    IngredientCreate,
    IngredientUpdate,
    IngredientRead
)
from src.middleware.jwt_methods import get_current_user
router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients"]
)
@router.post(
    "/create",
    response_model=IngredientRead,
    status_code=status.HTTP_201_CREATED
)
async def create_ingredient(
    payload: IngredientCreate,
    session: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    result = await session.execute(
        select(Ingredient).where(
            func.lower(Ingredient.name) == payload.name.lower()
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail="Ingredient already exists"
        )
    ingredient = Ingredient(
        name=payload.name.strip().lower(),
        calories_per_100g=payload.calories_per_100g,
        input_mode=payload.input_mode,
        is_active=payload.is_active,
    )
    session.add(ingredient)
    await session.flush()

    for size in payload.sizes:
        session.add(
            IngredientSize(
                ingredient_id=ingredient.id,
                label=size.label,
                weight_g=size.weight_g
            )
        )
    await session.commit()
    await session.refresh(ingredient)
    return ingredient

@router.put(
    "/{ingredient_id}",
    response_model=IngredientRead
)
async def update_ingredient(
    ingredient_id: int,
    payload: IngredientUpdate,
    session: AsyncSession = Depends(get_db),
    admin=Depends(get_current_user)
):
    if admin.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")

    ingredient = await session.get(Ingredient, ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field != "sizes":
            setattr(ingredient, field, value)
    if "sizes" in update_data:
        await session.execute(
            delete(IngredientSize).where(
                IngredientSize.ingredient_id == ingredient_id
            )
        )
        for size in update_data["sizes"] or []:
            session.add(
                IngredientSize(
                    ingredient_id=ingredient_id,
                    label=size["label"],
                    weight_g=size["weight_g"]
                )
            )
    await session.commit()
    await session.refresh(ingredient)
    return ingredient
