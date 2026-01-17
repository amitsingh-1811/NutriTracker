async def resolve_weight(item, ingredient, session):
    if item.weight_g is not None:
        return item.weight_g

    if item.count is not None and item.size_label:
        from src.db.models import IngredientSize
        from sqlalchemy import select, func

        result = await session.execute(
            select(IngredientSize).where(
                IngredientSize.ingredient_id == ingredient.id,
                func.lower(IngredientSize.label) == item.size_label.lower()
            )
        )
        size = result.scalar_one_or_none()
        if not size:
            return None

        return item.count * size.weight_g

    return None
