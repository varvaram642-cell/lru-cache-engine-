# lru-cache-engine-
Высокопроизводительная система кэширования в памяти, реализованная на Python с фокусом на алгоритмическую эффективность и принципы ООП.

 # Ключевые особенности
•   Алгоритм LRU (O(1)): Собственная реализация структуры данных Doubly Linked List в связке с хэш-таблицей обеспечивает константное время выполнения операций get и set.
•   Архитектура (ООП): Использование абстрактных базовых классов (ABC), строгая типизация и соблюдение принципов SOLID.
•   SQL Persistence: Интеграция с PostgreSQL для автоматического сохранения данных при вытеснении из кэша (Write-behind logic).
•   Инфраструктура: Полная контейнеризация через Docker и автоматизация рутинных задач (бэкап, тесты) через Bash.

 # Технологический стек
- Python 3.10+ (Typing, ABC)
- PostgreSQL (Database layer)
- Docker & Compose (Containerization)
- Bash (Automation scripts)
- Pytest (Unit testing)

 # Структура проекта
- /src — логика кэша, кастомные структуры данных и работа с БД.
- /scripts — Bash-скрипты для запуска бенчмарков и инициализации окружения.
- /tests — покрытие логики вытеснения данных Unit-тестами.

 # Быстрый запуск
 Клонировать и запустить всю инфраструктуру
git clone https://github.com/your-username/smart-lru-cache-engine.git
docker-compose up --build

# Запустить встроенный бенчмарк (Bash)
chmod +x scripts/benchmark.sh
./scripts/benchmark.sh


 
