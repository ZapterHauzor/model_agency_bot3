from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from app.core.config import settings
from app.infrastructure.dependencies.container import create_container
from app.presentation.bot.dialogs.booking_dialog import booking_dialog
from app.presentation.bot.middlewares.edit_mode import EditModeMiddleware

async def main():
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    
    # Мидлварь для edit_mode
    dp.message.middleware(EditModeMiddleware())
    dp.callback_query.middleware(EditModeMiddleware())
    
    # Регистрируем диалоги
    dp.include_router(booking_dialog)
    
    # Включаем поддержку диалогов
    setup_dialogs(dp)
    
    await dp.start_polling(bot)