from decimal import Decimal
from enum import StrEnum

from datetime import date

from sqlalchemy import BigInteger, Enum, String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config import BaseORM


class MealEnum(StrEnum):
    BREAKFAST = "Завтрак"
    SECOND_BREAKFAST = "Второй завтрак"
    LUNCH = "Обед"
    AFTERNOON_SNACK = "Полдник"
    DINNER = "Ужин"
    SECOND_DINNER = "Второй ужин"


class UserMeal(BaseORM):
    __tablename__ = "users_meals"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    meal_date: Mapped[date] = mapped_column(index=True, comment="Дата приема продукта")
    meal_type: Mapped[MealEnum] = mapped_column(
        Enum(MealEnum, name="meal_choices", length=16, inherit_schema=True),
        index=True,
        comment="Тип приема пищи",
    )

    food_name: Mapped[str] = mapped_column(String(100), comment="Название продукта")
    amount: Mapped[Decimal] = mapped_column(
        Numeric(6, 2),
        server_default="0.00",
        comment="Количество продукта в граммах",
    )
    calories: Mapped[Decimal] = mapped_column(
        Numeric(6, 2),
        server_default="0.00",
        comment="Количество калорий",
    )
    protein: Mapped[Decimal] = mapped_column(
        Numeric(6, 2),
        server_default="0.00",
        comment="Количество белков",
    )
    carbs: Mapped[Decimal] = mapped_column(
        Numeric(6, 2),
        server_default="0.00",
        comment="Количество углеводов",
    )
    fat: Mapped[Decimal] = mapped_column(
        Numeric(6, 2),
        server_default="0.00",
        comment="Количество жиров",
    )
    fiber: Mapped[Decimal] = mapped_column(
        Numeric(6, 2),
        server_default="0.00",
        comment="Количество клетчатки",
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        comment="ID пользователя",
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="meals")
    