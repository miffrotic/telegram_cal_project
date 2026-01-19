from aiogram.fsm.state import State, StatesGroup


class ProfileForm(StatesGroup):
    first_name = State()
    last_name = State()

    weight = State()
    height = State()
    age = State()
    sex = State()

    activity = State()
    city = State()

    target = State()
