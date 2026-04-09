from typing import Optional
from app.application.dto.order_dto import CreateOrderDTO

class BookingService:
    """Сервис для управления бронированиями"""
    
    async def create_order(self, dto: CreateOrderDTO) -> int:
        """Создать новый заказ и вернуть его ID"""
        # TODO: Реализовать сохранение в БД
        print(f"📦 Создан заказ: {dto}")
        return 1  # Временный ID
    
    async def apply_promo(self, code: str, price: int) -> tuple[int, str]:
        """Применить промокод (заглушка)"""
        # TODO: Реализовать логику промокодов
        if code == "TEST10":
            discount = int(price * 0.1)
            return price - discount, f"✅ Промокод применён! Скидка 10%"
        return price, "❌ Промокод не найден"