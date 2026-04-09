from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram_dialog.manager.manager import DialogManagerImpl
from aiogram_dialog.manager.update import DialogUpdate

class EditModeMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        # Принудительно включаем edit_mode для всех диалогов
        if "dialog_manager" in data:
            dialog_manager: DialogManagerImpl = data["dialog_manager"]
            if hasattr(dialog_manager, "update"):
                dialog_manager.update.edit_mode = True
        return await handler(event, data)