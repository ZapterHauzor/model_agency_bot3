from sqlalchemy import String, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import enum
from app.infrastructure.database.base import Base

class OrderStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

class Duration(enum.Enum):
    ONE_HOUR = "1_hour"
    TWO_HOURS = "2_hours"
    FULL_DAY = "full_day"

class Order(Base):
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    model_id: Mapped[int] = mapped_column(ForeignKey("models.id"))
    duration: Mapped[Duration] = mapped_column(Enum(Duration))
    price: Mapped[int]  # в USDT (цент)
    promo_code: Mapped[Optional[str]] = mapped_column(String(50))
    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)