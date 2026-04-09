import asyncio
from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from app.core.config import settings
from app.presentation.bot.dialogs.booking_dialog import booking_dialog
from app.presentation.bot.handlers.start import router as start_router

async def main():
    # ✅ Правильно:直接用 settings.bot_token
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    
    # Регистрируем диалог
    dp.include_router(booking_dialog)

    # Регистрируем обработчики
    dp.include_router(start_router)
    
    # Включаем поддержку диалогов
    setup_dialogs(dp)
    
    print(f"🤖 Бот успешно запущен!")
    print(f"📨 Оператор: {settings.operator_chat_id}")
    print(f"💰 Кошелёк: {settings.usdt_wallet}")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())