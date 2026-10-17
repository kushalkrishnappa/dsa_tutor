"""Anagram Dictionary.

Input:  word = "race"
        dictionary = ["bat", "acer", "caer", "apple"]

Output: ["acer", "caer"]
"""

"""
    Questions:
    - is word itself present in the dictionary?
    - the list can be empty if there are no anagram matches. Is that okay?
    - if dictionary is emptry the result will be empty list? Is that okay?
    - What can be the maximum size of dictionary?
    - I am assuming that the elements in dictionary are always strings based
    on the function definition.
    - if word is empty, I will match it with empty string in dictionary and
    return [""]. Is that okay?
    - Is dictionay fixed or can it be modified dynamically?
    --------------------------------------------------------------------------
    Approach: Hashmap + one pass
    - create hashmap of tuple of chrs count on [0] * 26 array as key and increment 
    if ch in present in the string.
    - append to result array (value in the dictionary) if there is a match
    - return hm.values()
    Time: O(N)
    Space: O(N * 26)
    --------------------------------------------------------------------------
    word = "race"
    dictionary = ["bat", "acer", "caer", "apple"]

    hm[(0, 0 .... 1 ..... 1)] = []

    "bat" -> will not match

    "acer" == (0, 0 .... 1 ..... 1) => hm[(0, 0 .... 1 ..... 1)].append("acer")
    hm[(0, 0 .... 1 ..... 1)] = ["acer"]

    "caer" == (0, 0 .... 1 ..... 1) => hm[(0, 0 .... 1 ..... 1)].append("caer")
    hm[(0, 0 .... 1 ..... 1)] = ["acer", "caer"]

    "apple" -> will not match

    return -> hm.values() == ["acer", "caer"]
    """

def buildWordSig(word: str) -> tuple:
    """
    Time: O(k), where k = size of word
    Space: O(26)
    """
    signature = [0] * 26
    for ch in word:
        signature[ord(ch) - ord('a')] += 1
    return tuple(signature)

def anagram_dictionary(word: str, dictionary: list[str]) -> list:
    """
    Time: O(k * N), k = size of word, N = size of dictionary
    Space: O(1) auxillary space
    """
    result = []
    signature = buildWordSig(word=word)
    for curr_word in dictionary:
        if len(curr_word) != len(word):
            continue
        word_signature = buildWordSig(curr_word)
        if word_signature == signature:
            result.append(curr_word)
    return result


if __name__ == "__main__":
    # test
    print(anagram_dictionary(word="race", dictionary=["bat", "acer", "caer", "apple"]))
