from sqlalchemy import String, Integer, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.base import Base

class Model(Base):
    __tablename__ = "models"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    age: Mapped[int]
    height: Mapped[int]
    weight: Mapped[int]
    photo_file_id: Mapped[str] = mapped_column(Text)  # Telegram file_id
    price_hour: Mapped[int]  # в USDT (цент)
    price_2hours: Mapped[int]
    price_day: Mapped[int]
    is_active: Mapped[bool] = mapped_column(default=True)
    
    city = relationship("City", back_populates="models")