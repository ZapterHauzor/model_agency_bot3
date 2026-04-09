from sqlalchemy import BigInteger, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.infrastructure.database.base import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[Optional[str]] = mapped_column(String(100))
    full_name: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)