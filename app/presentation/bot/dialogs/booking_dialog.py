from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Column, Start, Row
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.common import Whenable
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.application.services.booking_service import BookingService
from app.domain.entities.order import OrderStatus

# ID для диалогов
class BookingSG(StateGroup):
    select_city = State()
    select_model = State()
    model_details = State()
    select_duration = State()
    confirm = State()
    payment = State()

async def get_cities():
    # Получить список городов из БД
    pass

# Диалог выбора города
city_dialog = Dialog(
    Window(
        Const("🏙 Добро пожаловать! Выберите город:"),
        Column(
            Button(Const("{city.name}"), id="city_{city.id}", on_click=select_city),
            id="city_list"
        ),
        state=BookingSG.select_city,
        getter=get_cities
    )
)

# Диалог выбора модели
model_dialog = Dialog(...)

# Главный диалог бронирования
booking_dialog = Dialog(
    Window(
        Const("Выберите модель:"),
        # ...
    )
)