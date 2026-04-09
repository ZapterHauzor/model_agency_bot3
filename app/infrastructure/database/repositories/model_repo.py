from typing import List, Optional
from app.infrastructure.database.models.model import Model
from app.infrastructure.database.models.city import City

# Временная заглушка без БД
async def get_models_by_city(city_id: int) -> List[Model]:
    """Вернуть список моделей для города (тестовые данные)"""
    # TODO: Заменить на реальный запрос к БД
    
    # Создаём тестовые модели
    models_data = {
        1: [  # Москва
            Model(
                id=1, name="Анна", 
                city=City(id=1, name="Москва"), 
                age=22, height=175, weight=55,
                photo_file_id="AgACAgIAAxkBAAIBBGcBLAABTt8AAUffP1MAAWrhAALM3nEAAyqgAAElAALk6AABAg", 
                price_hour=5000, price_2hours=9000, price_day=25000
            ),
            Model(
                id=2, name="Елена", 
                city=City(id=1, name="Москва"), 
                age=25, height=170, weight=52,
                photo_file_id="AgACAgIAAxkBAAIBBGcBLAABTt8AAUffP1MAAWrhAALM3nEAAyqgAAElAALk6AABAg", 
                price_hour=5500, price_2hours=10000, price_day=28000
            ),
            Model(
                id=3, name="Ольга", 
                city=City(id=1, name="Москва"), 
                age=23, height=172, weight=54,
                photo_file_id="AgACAgIAAxkBAAIBBGcBLAABTt8AAUffP1MAAWrhAALM3nEAAyqgAAElAALk6AABAg", 
                price_hour=5200, price_2hours=9500, price_day=26000
            ),
        ],
        2: [  # Санкт-Петербург
            Model(
                id=4, name="Мария", 
                city=City(id=2, name="Санкт-Петербург"), 
                age=24, height=168, weight=50,
                photo_file_id="AgACAgIAAxkBAAIBBGcBLAABTt8AAUffP1MAAWrhAALM3nEAAyqgAAElAALk6AABAg", 
                price_hour=4800, price_2hours=8500, price_day=23000
            ),
        ],
        3: [  # Казань
            Model(
                id=5, name="Екатерина", 
                city=City(id=3, name="Казань"), 
                age=21, height=170, weight=53,
                photo_file_id="AgACAgIAAxkBAAIBBGcBLAABTt8AAUffP1MAAWrhAALM3nEAAyqgAAElAALk6AABAg", 
                price_hour=4500, price_2hours=8000, price_day=22000
            ),
        ],
    }
    return models_data.get(city_id, [])

async def get_model_by_id(model_id: int) -> Optional[Model]:
    """Вернуть модель по ID (тестовые данные)"""
    # Собираем все модели из всех городов
    all_models = []
    for city_id in [1, 2, 3]:
        models = await get_models_by_city(city_id)
        all_models.extend(models)
    
    for model in all_models:
        if model.id == model_id:
            return model
    return None