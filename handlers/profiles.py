from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states.profiles import ProfileForm


router = Router(name="profile")


@router.message(Command("set_profile"))
async def cmd_set_profile(message: Message, state: FSMContext):
    await message.answer("Введите ваш вес (кг):")
    await state.set_state(ProfileForm.weight)


@router.message(ProfileForm.weight)
async def process_weight(message: Message, state: FSMContext):
    try:
        weight = float(message.text)
        if weight < 30 or weight > 300:
            raise ValueError
        await state.update_data(weight=weight)
        await message.answer("Введите ваш рост (см):")
        await state.set_state(ProfileForm.height)
    except:
        await message.answer("Пожалуйста, введите число от 30 до 300 кг")


@router.message(ProfileForm.height)
async def process_height(message: Message, state: FSMContext):
    try:
        height = float(message.text)
        if height < 100 or height > 250:
            raise ValueError
        await state.update_data(height=height)
        await message.answer("Введите ваш возраст:")
        await state.set_state(ProfileForm.age)
    except:
        await message.answer("Рост — число от 100 до 250 см")


@router.message(ProfileForm.age)
async def process_age(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        if age < 10 or age > 120:
            raise ValueError
        await state.update_data(age=age)
        await message.answer("Сколько минут физической активности у вас в день в среднем?")
        await state.set_state(ProfileForm.activity)
    except:
        await message.answer("Возраст — целое число от 10 до 120")


@router.message(ProfileForm.activity)
async def process_activity(message: Message, state: FSMContext):
    try:
        activity = int(message.text)
        if activity < 0 or activity > 1440:
            raise ValueError
        await state.update_data(activity_min=activity)
        await message.answer("В каком городе вы находитесь? (на русском или английском)")
        await state.set_state(ProfileForm.city)
    except:
        await message.answer("Введите целое число минут (0–1440)")


@router.message(ProfileForm.city)
async def process_city_and_finish(message: Message, state: FSMContext):
    city = message.text.strip()
    if len(city) < 2:
        await message.answer("Название города слишком короткое. Попробуйте ещё раз.")
        return

    data = await state.get_data()
    user_id = message.from_user.id

    users[user_id] = {
        "weight": data["weight"],
        "height": data["height"],
        "age": data["age"],
        "activity_min": data["activity_min"],
        "city": city,
        "logged_water": 0,
        "logged_calories": 0.0,
        "burned_calories": 0.0,
    }

    # Сразу считаем нормы
    await recalculate_goals(user_id)

    await message.answer(
        f"Профиль сохранён!\n"
        f"Вес: {data['weight']} кг\n"
        f"Рост: {data['height']} см\n"
        f"Возраст: {data['age']} лет\n"
        f"Активность: {data['activity_min']} мин/день\n"
        f"Город: {city}\n\n"
        f"Используйте /check_progress чтобы увидеть нормы и прогресс."
    )
    await state.clear()


async def recalculate_goals(user_id: int):
    if user_id not in users:
        return

    u = users[user_id]

    # Вода
    base_water = u["weight"] * 30
    activity_bonus = (u["activity_min"] // 30) * 500
    water_goal = base_water + activity_bonus  # потом добавим погоду

    # Погода — асинхронно, но для простоты считаем здесь
    # (в идеале лучше вынести в отдельную задачу по таймеру или при /check_progress)
    temp = await get_current_temp(u["city"])
    if temp is not None and temp > 25:
        water_goal += 750  # среднее между 500–1000

    u["water_goal"] = round(water_goal)

    # Калории — Mifflin-St Jeor для мужчин (для простоты)
    # Можно спросить пол, но в задании не обязательно
    bmr = 10 * u["weight"] + 6.25 * u["height"] - 5 * u["age"] + 5
    activity_factor = 1.2 + (u["activity_min"] / 60) * 0.3  # грубо
    calorie_goal = round(bmr * activity_factor)

    u["calorie_goal"] = calorie_goal