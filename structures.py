from typing import Any, Optional


class Node:
    """
    Узел двусвязного списка.
    Хранит ключ, значение и ссылки на предыдущий и следующий узлы.
    """

    def __init__(self, key: Any, value: Any):
        self.key: Any = key
        self.value: Any = value
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None

    def __repr__(self) -> str:
        return f"Node(key={self.key}, value={self.value})"


class DoublyLinkedList:
    """
    Двусвязный список для поддержки операций за O(1).
    Используется в LRU-кэше для быстрого перемещения и удаления элементов.
    """

    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None

    def is_empty(self) -> bool:
        """Проверяет, пуст ли список."""
        return self.head is None

    def add_to_front(self, node: Node) -> None:
        """
        Добавляет новый узел в начало списка. Временная сложность: O(1).
        """
        # Сбрасываем старые связи узла перед добавлением
        node.prev = None
        node.next = None

        if self.head is None:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node

    def move_to_front(self, node: Node) -> None:
        """
        Перемещает существующий узел в начало списка. Временная сложность: O(1).
        """
        if node == self.head:
            return

        # Извлекаем узел из текущей позиции
        if node.next is None:  # Если узел — это хвост (tail)
            self.tail = node.prev
            if self.tail:
                self.tail.next = None
        else:  # Если узел в середине списка
            if node.prev:
                node.prev.next = node.next
            if node.next:
                node.next.prev = node.prev

        # Вставляем узел в начало
        node.next = self.head
        node.prev = None
        if self.head:
            self.head.prev = node
        self.head = node

    def remove_tail(self) -> Optional[Node]:
        """
        Удаляет узел с конца списка (как самый неиспользуемый) и возвращает его.
        Временная сложность: O(1).
        """
        if self.head is None:
            return None

        removed = self.tail
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            if self.tail and self.tail.prev:
                self.tail = self.tail.prev
                self.tail.next = None
        
        if removed:
            removed.prev = None
            removed.next = None
            
        return removed
