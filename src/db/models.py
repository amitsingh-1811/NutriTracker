from sqlalchemy import Column, Integer, String, Boolean, Float, Enum as SqlEnum, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from ..accounts.user_roles import UserRole
from sqlalchemy import Enum as SqlEnum
from ..ingredients.input_mode import InputMode

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    role = Column(SqlEnum(UserRole), default=UserRole.USER)

class Ingredient(Base):
    __tablename__ = "ingredient"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    calories_per_100g = Column(Float, nullable=True)
    input_mode = Column(SqlEnum(InputMode), nullable=False)
    is_active = Column(Boolean, default=True)
    # ORM relationship (not DB column)
    sizes = relationship(
        "IngredientSize",
        back_populates="ingredient",
        cascade="all, delete-orphan"
    )

class IngredientSize(Base):
    __tablename__ = "ingredient_size"

    id = Column(Integer, primary_key=True)
    ingredient_id = Column(
        Integer,
        ForeignKey("ingredient.id", ondelete="CASCADE"),
        nullable=False
    )
    label = Column(String, nullable=False)      # SMALL / MEDIUM / LARGE
    weight_g = Column(Float, nullable=False)    # grams for that size
    # ORM relationship (not DB column)
    ingredient = relationship(
        "Ingredient",
        back_populates="sizes"
    )