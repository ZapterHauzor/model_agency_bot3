from typing import List
from dataclasses import dataclass

# Простой dataclass вместо SQLAlchemy модели для тестов
@dataclass
class CityTest:
    id: int
    name: str

async def get_all_cities() -> List[CityTest]:
    """Вернуть список всех городов (тестовые данные без SQLAlchemy)"""
    return [
        CityTest(id=1, name="Москва"),
        CityTest(id=2, name="Санкт-Петербург"),
        CityTest(id=3, name="Казань"),
        CityTest(id=4, name="Новосибирск"),
        CityTest(id=5, name="Екатеринбург"),
    ]