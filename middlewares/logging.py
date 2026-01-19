import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User, Message, CallbackQuery

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user: User | None = None

        if isinstance(event, Message):
            user = event.from_user
            text = event.text or event.caption or "[no text]"
            logger.info(
                "MSG | user=%s (%s) | chat=%s | text=%s",
                user.id if user else "???", 
                user.username if user else "???",
                event.chat.id,
                text[:100] + "..." if len(text) > 100 else text
            )
        elif isinstance(event, CallbackQuery):
            user = event.from_user
            logger.info(
                "CBQ | user=%s (%s) | data=%s",
                user.id if user else "???",
                user.username if user else "???",
                event.data
            )

        return await handler(event, data)