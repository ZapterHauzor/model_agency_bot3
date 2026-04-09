from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.infrastructure.database.base import Base

class Payment(Base):
    __tablename__ = "payments"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    screenshot_file_id: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(default="pending")  # pending, verified, rejected
    operator_message_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)