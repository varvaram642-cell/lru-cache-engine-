from typing import Any, Optional
from abc import ABC, abstractmethod
from .structures import DoublyLinkedList, Node  # Точечная нотация для модулей внутри пакета

class BaseCache(ABC):
    """
    Абстрактный интерфейс для систем кэширования.
    Позволяет легко заменить LRU на другую стратегию (например, LFU).
    """
    @abstractmethod
    def get(self, key: Any) -> Optional[Any]:
        pass

    @abstractmethod
    def put(self, key: Any, value: Any) -> None:
        pass

    @abstractmethod
    def size(self) -> int:
        pass


class LRUCache(BaseCache):
    """
    Реализация Least Recently Used (LRU) кэша.
    Сложность операций get и put — O(1).
    """
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer")
            
        self.capacity = capacity
        # Хэш-таблица для быстрого доступа к узлам по ключу
        self.cache: dict[Any, Node] = {}
        # Список для отслеживания порядка использования
        self.linked_list = DoublyLinkedList()

    def get(self, key: Any) -> Optional[Any]:
        """
        Получает значение из кэша. Если ключ найден, помечает его как 
        самый недавно использованный.
        """
        if key in self.cache:
            node = self.cache[key]
            self.linked_list.move_to_front(node)
            return node.value
        return None

    def put(self, key: Any, value: Any) -> None:
        """
        Добавляет или обновляет значение в кэше. 
        При превышении лимита удаляет наименее используемый элемент.
        """
        if key in self.cache:
            # Обновляем существующее значение
            node = self.cache[key]
            node.value = value
            self.linked_list.move_to_front(node)
        else:
            # Создаем новый узел
            new_node = Node(key, value)
            
            # Проверка переполнения ПЕРЕД добавлением нового (или ПОСЛЕ, зависит от политики)
            # В данном случае удаляем, если достигли лимита
            if self.size() >= self.capacity:
                removed_node = self.linked_list.remove_tail()
                if removed_node:
                    del self.cache[removed_node.key]

            self.linked_list.add_to_front(new_node)
            self.cache[key] = new_node

    def size(self) -> int:
        """Возвращает текущее количество элементов в кэше."""
        return len(self.cache)

    def __repr__(self) -> str:
        return f"LRUCache(capacity={self.capacity}, current_size={self.size()})"
