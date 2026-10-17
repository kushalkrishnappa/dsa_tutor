"""Trie Data Structure."""

import string

class TrieNode:

    def __init__(self):
        self.val = [None] * 26
        self.flag = False

class Trie:

    def __init__(self):
        self.root = TrieNode()
        self.hm = {letter: idx for idx, letter in enumerate(string.ascii_lowercase)}

    def insert(self, word: str) -> None:
        ptr = self.root
        for letter in word:
            letter_idx = self.hm[letter]
            if ptr.val[letter_idx] is None:
                ptr.val[letter_idx] = TrieNode()
            ptr = ptr.val[letter_idx]
        ptr.flag = True

    def search(self, word: str) -> bool:
        ptr = self.root
        for letter in word:
            letter_idx = self.hm[letter]
            if ptr.val[letter_idx] is None:
                return False
            ptr = ptr.val[letter_idx]
        return ptr.flag

    def startsWith(self, prefix: str) -> bool:
        ptr = self.root
        for letter in prefix:
            letter_idx = self.hm[letter]
            if ptr.val[letter_idx] is None:
                return False
            ptr = ptr.val[letter_idx]
        return True


trie = Trie()

trie.insert("apple")
print(trie.search("app"))       # expect: False  (path exists, but no word ends at 'p')
print(trie.startsWith("app"))   # expect: True   (path exists — that's all startsWith needs)


# insert
trie.insert("ab")
trie.insert("kushal")

# search
print(trie.search("ab"))
print(trie.search("kushal"))
print(trie.search("nakkan"))

# prefix search
print(trie.startsWith("a"))
print(trie.startsWith("kush"))
print(trie.startsWith("kusm"))
