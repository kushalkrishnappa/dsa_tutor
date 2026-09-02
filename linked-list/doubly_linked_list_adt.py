"""Doubly Linked List Abstract Data Type Implementation."""


class DLLNode:
    """DLLNode contains node value pointers to its neighbors."""

    def __init__(self, val: int = 0, next: DLLNode = None, prev: DLLNode = None):
        self.val = val
        self.next = next
        self.prev = prev


class DoublyLinkedList:
    """Doubly Linked List: Linear data structure where every element is connected
    by two pointers, next and prev. Unline arrays, memory is not contiguous and
    nodes can be placed anywhere with pointer reference.
    """

    def __init__(self):
        self.stl_head = DLLNode(val=-1, next=None)
        self.stl_tail = DLLNode(val=-1, next=None)
        self.stl_head.next, self.stl_tail.prev = self.stl_tail, self.stl_head
        self.size = 0

    # insert a node
    def insert(self, val: int):
        self.insert_at(idx=self.size, val=val)

    # insert node at index
    def insert_at(self, idx: int, val: int):
        new_node = DLLNode(val=val, next=None)
        if idx >= self.size:
            prev_node = self.stl_tail.prev
            self.stl_tail.prev = new_node
            prev_node.next = new_node
            new_node.next, new_node.prev = self.stl_tail, prev_node
        else:
            temp = self.stl_head
            for _ in range(idx):
                temp = temp.next
            nxt = temp.next
            temp.next, new_node.next = new_node, nxt
            nxt.prev, new_node.prev = new_node, temp
        self.size += 1

    # delete a node
    def delete(self) -> bool:
        last_node = self.stl_tail.prev.prev
        last_node.next = self.stl_tail
        self.stl_tail.prev = last_node
        self.size -= 1

    # remove node at index
    def remove_at(self, idx: int) -> bool:
        if idx >= self.size or idx < 0:
            return False
        temp = self.stl_head
        for _ in range(idx):
            temp = temp.next
        nxt = temp.next.next
        temp.next = nxt
        nxt.prev = temp
        self.size -= 1
        return True

    # get node at index
    def get_val(self, idx: int) -> int | None:
        if idx >= self.size or idx < 0:
            return
        temp = self.stl_head
        for _ in range(idx + 1):
            temp = temp.next
        return temp.val

    # check for val
    def search(self, target: int) -> int | None:
        temp = self.stl_head
        idx_count = 0
        while temp.next and temp.next != self.stl_tail:
            if temp.next.val == target:
                return idx_count
            temp = temp.next
            idx_count += 1
