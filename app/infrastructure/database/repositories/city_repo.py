from typing import List
from app.infrastructure.database.models.city import City

# Временная заглушка без БД
async def get_all_cities() -> List[City]:
    """Вернуть список всех городов (пока тестовые данные)"""
    # TODO: Заменить на реальный запрос к БД
    return [
        City(id=1, name="Москва"),
        City(id=2, name="Санкт-Петербург"),
        City(id=3, name="Казань"),
        City(id=4, name="Новосибирск"),
        City(id=5, name="Екатеринбург"),
    ]