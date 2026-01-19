import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from config import settings
from handlers import profiles_router


bot = Bot(token=settings.bot.BOT_TOKEN)

dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Ну что, покушаем кал сегодня?")


dp.include_router(profiles_router)


@dp.message(Command("help"))
async def cmd_start(message: Message):
    await message.answer(
"""
/start - начать работу с ботом
/help - получить справку по командам
"""
)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
