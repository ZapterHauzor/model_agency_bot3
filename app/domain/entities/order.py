from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

@dataclass
class OrderEntity:
    user_id: int
    model_id: int
    duration: str
    price: int
    status: OrderStatus
    promo_code: str | None = None
    id: int | None = None
    created_at: datetime | None = None