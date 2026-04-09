# В самом верху файла убери эти строки:
# from app.application.services.booking_service import BookingService
# from app.application.dto.order_dto import CreateOrderDTO
# from app.infrastructure.database.repositories.model_repo import get_models_by_city, get_model_by_id
# from app.infrastructure.database.repositories.city_repo import get_all_cities

# Импортируем только то, что точно есть
from typing import Dict, Any, Optional
from enum import Enum

from aiogram.types import CallbackQuery, Message
from aiogram.filters.state import State, StatesGroup
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import (
    Button, Back, Cancel, Column, Select, Row, Start, ScrollingGroup
)
from aiogram_dialog.widgets.text import Const, Format, Multi, List, Jinja
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.api.entities import ShowMode

from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.core.config import settings

# --- 1. Определяем состояния (шаги) диалога ---
class BookingSG(StatesGroup):
    select_city = State()
    select_model = State()
    model_details = State()
    select_duration = State()
    confirm = State()
    payment = State()
    promo = State()

# --- 2. Вспомогательные функции (геттеры) с внутренними импортами ---

async def cities_getter(dialog_manager: DialogManager, **kwargs):
    """Получает список городов из БД"""
    # 🔥 Импортируем внутри функции, чтобы избежать ошибки импорта
    from app.infrastructure.database.repositories.city_repo import get_all_cities
    cities = await get_all_cities()
    return {"cities": cities, "count": len(cities)}

async def models_getter(dialog_manager: DialogManager, **kwargs):
    """Получает список моделей для выбранного города"""
    from app.infrastructure.database.repositories.model_repo import get_models_by_city
    city_id = dialog_manager.dialog_data.get("city_id")
    if not city_id:
        return {"models": [], "city_name": "Не выбран"}
    models = await get_models_by_city(city_id)
    city_name = dialog_manager.dialog_data.get("city_name", "")
    return {"models": models, "city_name": city_name}

async def model_details_getter(dialog_manager: DialogManager, **kwargs):
    """Получает детальную информацию о модели для анкеты"""
    from app.infrastructure.database.repositories.model_repo import get_model_by_id
    model_id = dialog_manager.dialog_data.get("model_id")
    if not model_id:
        return {"photo": None, "caption": "Модель не найдена"}
    
    model = await get_model_by_id(model_id)
    if not model:
        return {"photo": None, "caption": "Модель не найдена"}
    
    caption = (
        f"📸 <b>{model.name}</b>\n\n"
        f"📍 <b>Город:</b> {model.city.name}\n"
        f"🎂 <b>Возраст:</b> {model.age} лет\n"
        f"📏 <b>Рост:</b> {model.height} см\n"
        f"⚖️ <b>Вес:</b> {model.weight} кг\n\n"
        f"💰 <b>Стоимость съёмки:</b>\n"
        f"• 1 час — {model.price_hour} USDT\n"
        f"• 2 часа — {model.price_2hours} USDT\n"
        f"• Весь день — {model.price_day} USDT"
    )
    return {"photo": model.photo_file_id, "caption": caption}

async def duration_getter(dialog_manager: DialogManager, **kwargs):
    """Получает цены для выбранной модели"""
    from app.infrastructure.database.repositories.model_repo import get_model_by_id
    model_id = dialog_manager.dialog_data.get("model_id")
    model = await get_model_by_id(model_id)
    if not model:
        return {"price_hour": 0, "price_2hours": 0, "price_day": 0}
    
    dialog_manager.dialog_data["price_hour"] = model.price_hour
    dialog_manager.dialog_data["price_2hours"] = model.price_2hours
    dialog_manager.dialog_data["price_day"] = model.price_day
    
    return {
        "price_hour": model.price_hour,
        "price_2hours": model.price_2hours,
        "price_day": model.price_day,
    }

async def confirm_getter(dialog_manager: DialogManager, **kwargs):
    """Получает данные для подтверждения заказа"""
    duration_key = dialog_manager.dialog_data.get("duration")
    price = dialog_manager.dialog_data.get("price")
    model_name = dialog_manager.dialog_data.get("model_name")
    
    duration_text = {
        "1hour": "1 час",
        "2hours": "2 часа",
        "day": "Весь день"
    }.get(duration_key, "Не выбрано")
    
    return {
        "model_name": model_name,
        "duration": duration_text,
        "price": price
    }

async def payment_getter(dialog_manager: DialogManager, **kwargs):
    """Получает данные для финального экрана оплаты"""
    duration_key = dialog_manager.dialog_data.get("duration")
    price = dialog_manager.dialog_data.get("price")
    
    duration_text = {
        "1hour": "1 час",
        "2hours": "2 часа",
        "day": "Весь день"
    }.get(duration_key, "Не выбрано")
    
    return {
        "duration": duration_text,
        "price": price,
        "wallet": settings.USDT_WALLET
    }

# --- 3. Обработчики нажатий на кнопки ---

async def on_city_selected(callback: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    """Обработчик выбора города"""
    selected_city = widget.get_item(int(item_id))
    manager.dialog_data["city_id"] = int(item_id)
    manager.dialog_data["city_name"] = selected_city.name
    await manager.next()

async def on_model_selected(callback: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    """Обработчик выбора модели"""
    selected_model = widget.get_item(int(item_id))
    manager.dialog_data["model_id"] = int(item_id)
    manager.dialog_data["model_name"] = selected_model.name
    await manager.next()

async def on_duration_selected(callback: CallbackQuery, widget: Button, manager: DialogManager):
    """Обработчик выбора длительности съемки"""
    widget_id = widget.widget_id
    duration_map = {
        "duration_1hour": ("1hour", "price_hour"),
        "duration_2hours": ("2hours", "price_2hours"),
        "duration_day": ("day", "price_day")
    }
    
    if widget_id not in duration_map:
        return
    
    duration_key, price_key = duration_map[widget_id]
    price = manager.dialog_data.get(price_key)
    
    manager.dialog_data["duration"] = duration_key
    manager.dialog_data["price"] = price
    
    await manager.next()

async def on_confirm_yes(callback: CallbackQuery, widget: Button, manager: DialogManager):
    """Обработчик подтверждения заказа"""
    # 🔥 Временная заглушка без сервиса
    await callback.answer("✅ Заказ создан! Переходим к оплате...")
    await manager.next()

async def on_confirm_no(callback: CallbackQuery, widget: Button, manager: DialogManager):
    """Обработчик кнопки 'Изменить' - возвращает к выбору длительности"""
    await manager.back()

async def on_send_receipt(callback: CallbackQuery, widget: Button, manager: DialogManager):
    """Обработчик кнопки 'Отправить чек оператору'"""
    await callback.message.answer(
        "📞 Связь с оператором\n\n"
        "Пожалуйста, отправьте скриншот чека об оплате сюда.\n"
        "Наш менеджер свяжется с вами в ближайшее время."
    )
    await manager.done()

# --- 4. Окна диалога ---

city_window = Window(
    Multi(
        Const("🏙 <b>Добро пожаловать в модельное агентство!</b>\n\n"),
        Const("Выберите город, в котором ищете модель:"),
        Const("\n📌 <i>Доступно {count} городов</i>"),
        sep=""
    ),
    ScrollingGroup(
        Select(
            Format("{item.name}"),
            id="city_select",
            item_id_getter=lambda x: x.id,
            items="cities",
            on_click=on_city_selected,
        ),
        height=5,
        id="cities_scroll",
    ),
    Row(
        Cancel(Const("❌ Закрыть")),
    ),
    state=BookingSG.select_city,
    getter=cities_getter,
    parse_mode="HTML",
)

models_window = Window(
    Multi(
        Const("📍 <b>Город:</b> {city_name}\n"),
        Const("👇 <b>Выберите модель:</b>\n\n"),
    ),
    ScrollingGroup(
        Select(
            Format("👤 {item.name} | {item.age} лет"),
            id="model_select",
            item_id_getter=lambda x: x.id,
            items="models",
            on_click=on_model_selected,
        ),
        height=8,
        id="models_scroll",
    ),
    Row(
        Back(Const("◀️ Назад")),
        Cancel(Const("❌ Отмена")),
    ),
    state=BookingSG.select_model,
    getter=models_getter,
    parse_mode="HTML",
)

model_details_window = Window(
    Const("{caption}"),
    Row(
        Button(Const("📝 Оформить"), id="proceed_booking", on_click=lambda c, w, m: m.next()),
        Back(Const("◀️ Назад")),
    ),
    Row(
        Cancel(Const("❌ Отмена")),
    ),
    state=BookingSG.model_details,
    getter=model_details_getter,
    parse_mode="HTML",
)

duration_window = Window(
    Multi(
        Const("⏰ <b>Выберите длительность съёмки:</b>\n\n"),
        Const("• <b>1 час</b> — {price_hour} USDT\n"),
        Const("• <b>2 часа</b> — {price_2hours} USDT\n"),
        Const("• <b>Весь день</b> — {price_day} USDT\n"),
        Const("\n🎟 <i>Есть промокод? Нажмите кнопку ниже</i>"),
    ),
    Column(
        Button(Const("🕐 1 час"), id="duration_1hour", on_click=on_duration_selected),
        Button(Const("🕑 2 часа"), id="duration_2hours", on_click=on_duration_selected),
        Button(Const("🌞 Весь день"), id="duration_day", on_click=on_duration_selected),
        Button(Const("🎟 Применить промокод"), id="apply_promo"),
    ),
    Row(
        Back(Const("◀️ Назад")),
        Cancel(Const("❌ Отмена")),
    ),
    state=BookingSG.select_duration,
    getter=duration_getter,
    parse_mode="HTML",
)

confirm_window = Window(
    Multi(
        Const("✅ <b>Подтвердите заказ:</b>\n\n"),
        Const("👤 <b>Модель:</b> {model_name}\n"),
        Const("⏰ <b>Длительность:</b> {duration}\n"),
        Const("💰 <b>Сумма:</b> {price} USDT\n\n"),
        Const("Всё верно?"),
    ),
    Row(
        Button(Const("✅ Подтвердить"), id="confirm_yes", on_click=on_confirm_yes),
        Button(Const("✏️ Изменить"), id="confirm_no", on_click=on_confirm_no),
    ),
    Row(
        Cancel(Const("❌ Отмена")),
    ),
    state=BookingSG.confirm,
    getter=confirm_getter,
    parse_mode="HTML",
)

payment_window = Window(
    Multi(
        Const("💳 <b>Оплата в USDT (TRC-20)</b>\n\n"),
        Const("📅 <b>Съёмка:</b> {duration}\n"),
        Const("💰 <b>К оплате:</b> {price} USDT\n\n"),
        Const("📮 <b>Кошелёк TRC-20:</b>\n"),
        Const("<code>{wallet}</code>\n\n"),
        Const("⚠️ <b>После оплаты отправьте чек (скриншот) оператору</b>\n"),
        Const("Нажмите кнопку ниже для связи с поддержкой."),
    ),
    Row(
        Button(Const("📤 Отправить чек оператору"), id="send_receipt", on_click=on_send_receipt),
    ),
    Row(
        Cancel(Const("❌ Закрыть")),
    ),
    state=BookingSG.payment,
    getter=payment_getter,
    parse_mode="HTML",
)

# --- 5. Главный объект диалога ---
booking_dialog = Dialog(
    city_window,
    models_window,
    model_details_window,
    duration_window,
    confirm_window,
    payment_window,
)