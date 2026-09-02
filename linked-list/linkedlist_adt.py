"""Linked List Abstract Data Type Implementation."""


class ListNode:
    def __init__(self, val: int = 0, next: ListNode = None):
        self.val = val
        self.next = next


class LinkedList:
    """Linked List: Linear data structure where every element is connected
    by a pointer. Unline arrays, memory is not contiguous and nodes can be
    placed anywhere with pointer reference.
    """

    def __init__(self):
        self.sentinel = ListNode(val=-1, next=None)
        self.tail = self.sentinel
        self.size = 0

    # insert a node
    def insert(self, val: int):
        self.insert_at(idx=self.size, val=val)

    # insert node at index
    def insert_at(self, idx: int, val: int):
        new_node = ListNode(val=val, next=None)
        if idx >= self.size:
            self.tail.next = new_node
            self.tail = self.tail.next
        else:
            temp = self.sentinel
            for _ in range(idx):
                temp = temp.next
            nxt = temp.next
            temp.next, new_node.next = new_node, nxt
        self.size += 1

    # delete a node
    def delete(self) -> bool:
        return self.remove_at(idx=self.size - 1)

    # remove node at index
    def remove_at(self, idx: int) -> bool:
        if idx >= self.size or idx < 0:
            return False
        temp = self.sentinel
        for _ in range(idx):
            temp = temp.next
        nxt = temp.next.next
        temp.next = nxt
        self.size -= 1
        return True

    # get node at index
    def get_val(self, idx: int) -> int | None:
        if idx >= self.size or idx < 0:
            return
        temp = self.sentinel
        for _ in range(idx + 1):
            temp = temp.next
        return temp.val

    # check for val
    def search(self, target: int) -> int | None:
        temp = self.sentinel
        idx_count = 0
        while temp.next:
            if temp.next.val == target:
                return idx_count
            temp = temp.next
            idx_count += 1
