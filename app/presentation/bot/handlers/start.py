from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from app.presentation.bot.dialogs.booking_dialog import BookingSG

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, dialog_manager: DialogManager):
    """Обработчик команды /start - запускает диалог выбора города"""
    await dialog_manager.start(
        BookingSG.select_city,
        mode=StartMode.RESET_STACK
    )