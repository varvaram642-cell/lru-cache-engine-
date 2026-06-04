import time
from typing import Any, Optional
from cache import LRUCache

class SlowDatabase:
    """
    Имитация реальной базы данных (например, PostgreSQL), 
    которая работает медленно из-за сетевых задержек или тяжелых запросов.
    """
    def __init__(self):
        self.storage: dict[str, Any] = {}

    def get(self, key: str) -> Optional[Any]:
        time.sleep(0.5)
        return self.storage.get(key)

    def put(self, key: str, value: Any) -> None:
        time.sleep(0.1)
        self.storage[key] = value


class CachedDatabaseProxy:
    """
    Паттерн 'Proxy'. Перехватывает запросы к базе данных и 
    возвращает данные из кэша, если они там есть.
    """
    def __init__(self, db: SlowDatabase, cache_capacity: int):
        self.db = db
        self.cache = LRUCache(cache_capacity)

    def get(self, key: str) -> Optional[Any]:
        start_time = time.perf_counter()
        value = self.cache.get(key)
        
        if value is not None:
            end_time = time.perf_counter()
            print(f"[CACHE HIT] Ключ '{key}' найден в кэше. Время: {end_time - start_time:.5f} сек.")
            return value

        print(f"[CACHE MISS] Ключа '{key}' нет в кэше. Обращаюсь к базе данных...")
        start_time = time.perf_counter()
        value = self.db.get(key)
        
        if value is not None:
            self.cache.put(key, value)
        
        end_time = time.perf_counter()
        print(f"[DB FETCH] Данные получены из БД. Время: {end_time - start_time:.5f} сек.")
        return value


if __name__ == "__main__":
    real_db = SlowDatabase()
    cached_service = CachedDatabaseProxy(real_db, cache_capacity=2)

    real_db.put("user_1", {"name": "Alice", "balance": 1000})
    real_db.put("user_2", {"name": "Bob", "balance": 500})

    print("--- Первый запрос (медленный) ---")
    print("Результат:", cached_service.get("user_1"))

    print("\n--- Второй запрос того же ключа (мгновенный) ---")
    print("Результат:", cached_service.get("user_1"))

    print("\n--- Запрос другого ключа (медленный) ---")
    print("Результат:", cached_service.get("user_2"))

    print("\n--- Вытеснение из кэша (LRU в действии) ---")
    real_db.put("user_3", {"name": "Charlie", "balance": 700})
    cached_service.get("user_3")

    print("\n--- Проверка вытесненного ключа user_2 (снова будет медленно) ---")
    print("Результат:", cached_service.get("user_2"))
