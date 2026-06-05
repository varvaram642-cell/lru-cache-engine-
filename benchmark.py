import time
import random
from database import SlowDatabase, CachedDatabaseProxy

# Настройки
UNIQUE_KEYS = 100
TOTAL_REQUESTS = 500
CACHE_SIZE = 50

# Инициализация
db = SlowDatabase()
for i in range(UNIQUE_KEYS):
    db.put(f"key_{i}", f"value_{i}")

# Генерация запросов (80% попадают в первые 40 ключей)
hot_keys = [f"key_{i}" for i in range(40)]
all_keys = [f"key_{i}" for i in range(UNIQUE_KEYS)]
requests = [random.choice(hot_keys if random.random() < 0.8 else all_keys) for _ in range(TOTAL_REQUESTS)]

# Тест без кэша
print("Запуск теста без кэша...")
start = time.perf_counter()
for key in requests:
    db.get(key)
no_cache_time = time.perf_counter() - start

# Тест с кэшем
print("Запуск теста с кэшем...")
proxy = CachedDatabaseProxy(db, CACHE_SIZE)
start = time.perf_counter()
for key in requests:
    proxy.get(key)
with_cache_time = time.perf_counter() - start

# Итоги
print("-" * 30)
print(f"Время без кэша: {no_cache_time:.2f}s")
print(f"Время с кэшем:  {with_cache_time:.2f}s")
print(f"Ускорение:      {no_cache_time / with_cache_time:.1f}x")
print("-" * 30)
