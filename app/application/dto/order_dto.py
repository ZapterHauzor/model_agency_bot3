from dataclasses import dataclass
from typing import Optional

@dataclass
class CreateOrderDTO:
    """DTO для создания заказа"""
    user_id: int
    model_id: int
    duration: str  # "1hour", "2hours", "day"
    price: int
    promo_code: Optional[str] = None