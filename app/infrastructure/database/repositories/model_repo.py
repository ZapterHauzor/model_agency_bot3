from typing import List, Optional
from dataclasses import dataclass

@dataclass
class CityTest:
    id: int
    name: str

@dataclass
class ModelTest:
    id: int
    name: str
    city: CityTest
    age: int
    height: int
    weight: int
    photo_file_id: str
    price_hour: int
    price_2hours: int
    price_day: int

async def get_models_by_city(city_id: int) -> List[ModelTest]:
    """Вернуть список моделей для города (тестовые данные)"""
    
    cities = {
        1: CityTest(id=1, name="Москва"),
        2: CityTest(id=2, name="Санкт-Петербург"),
        3: CityTest(id=3, name="Казань"),
    }
    
    models_data = {
        1: [  # Москва
            ModelTest(id=1, name="Анна", city=cities[1], age=22, height=175, weight=55,
                     photo_file_id="test_photo_1", price_hour=5000, price_2hours=9000, price_day=25000),
            ModelTest(id=2, name="Елена", city=cities[1], age=25, height=170, weight=52,
                     photo_file_id="test_photo_2", price_hour=5500, price_2hours=10000, price_day=28000),
        ],
        2: [  # СПБ
            ModelTest(id=3, name="Мария", city=cities[2], age=23, height=172, weight=54,
                     photo_file_id="test_photo_3", price_hour=4800, price_2hours=8500, price_day=23000),
        ],
    }
    return models_data.get(city_id, [])

async def get_model_by_id(model_id: int) -> Optional[ModelTest]:
    """Вернуть модель по ID (тестовые данные)"""
    for city_id in [1, 2]:
        for model in await get_models_by_city(city_id):
            if model.id == model_id:
                return model
    return None