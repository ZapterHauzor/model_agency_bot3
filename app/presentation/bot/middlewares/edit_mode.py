from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

class EditModeMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        # Включаем edit_mode через dialog_data
        if "dialog_manager" in data:
            dialog_manager = data["dialog_manager"]
            # Устанавливаем флаг edit_mode в текущем контексте
            if hasattr(dialog_manager, "current_context"):
                context = dialog_manager.current_context()
                if context:
                    context.dialog_data["_edit_mode"] = True
        
        return await handler(event, data)