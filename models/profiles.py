from decimal import Decimal
from enum import StrEnum

from sqlalchemy import BigInteger, Enum, String, Numeric, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config import BaseORM


class SexEnum(StrEnum):
    MALE = "male"
    FEMALE = "female"


class User(BaseORM):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    username: Mapped[str] = mapped_column(unique=True, comment="Логин пользователя")

    first_name: Mapped[str] = mapped_column(String(30), comment="Имя пользователя")
    last_name: Mapped[str | None] = mapped_column(String(30), comment="Фамилия пользователя")

    weight: Mapped[Decimal] = mapped_column(Numeric(4, 1), comment="Вес пользователя в кг")
    height: Mapped[int] = mapped_column(SmallInteger, comment="Рост пользователя в см")
    age: Mapped[int] = mapped_column(SmallInteger, comment="Возраст пользователя")
    sex: Mapped[SexEnum] = mapped_column(
        Enum(SexEnum, name="sex_choices", length=10, inherit_schema=True),
        comment="Пол пользователя",
    )
    activity_min: Mapped[int] = mapped_column(SmallInteger, comment="Количество минут активности в день")
    city: Mapped[str] = mapped_column(String(50), comment="Город пользователя")

    calories_goal: Mapped[int] = mapped_column(SmallInteger, comment="Количество калорий в день")
    water_goal: Mapped[int] = mapped_column(SmallInteger, comment="Количество калорий в день")

    # Relationships
    meals: Mapped[list["UserMeal"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    