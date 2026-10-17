"""
Questions:
- if the list is empty, I will return an empty dict.
- I will assume all the values are english alphabets
- What can be the minimum/maximum size of interests array?
- What can be the minimum/maximum size of employee records?
- Do you want the result interest to be in sorted order of the 
employee record or is it fine to be unordered?
- Do you want the keys to be sorted in alphabetical order in the
result dict?
"""

from collections import defaultdict

def parse_interest(interest: str) -> str:
    return interest.strip().lower()

def find_employees(employees: list[dict]) -> dict[str, set[int]]:
    """
    Test:
    employees = [
    {'id': 1, 'name': 'Alice',   'interests': ['basketball', 'coding']},
    {'id': 2, 'name': 'Bob',     'interests': ['basketball', 'music']},
    {'id': 3, 'name': 'Charlie', 'interests': ['coding', 'music']},
    {'id': 4, 'name': 'David',   'interests': ['music']},
    ]
    == {
        'basketball': {1, 2},
        'coding':     {1, 3},
        'music':      {2, 3, 4},
    }

    Approach:
    - traverse the employees
    - get the id, interests from each employee
    - for interest in interests:
        - parse the interest -> clean + normalize = parsed_interest
        - if parsed_interest in result dict
        - add id to set. Use defaultdict(set) incase to handle 
        first occurance of interest.
    - return result

    Time: O(N * k * max(len(interest))) -> N records, k interests
    Space: O(1) without result, O(N * k) with result.
    """
    result = defaultdict(set)
    for emp in employees:
        emp_id, interests = emp["id"], emp["interests"]
        for interest in interests:
            interest = parse_interest(interest=interest)
            if interest:
                result[interest].add(emp_id)
    return dict(result)

employees = [
    {'id': 1, 'name': 'Alice',   'interests': ['basketball', 'coding']},
    {'id': 2, 'name': 'Bob',     'interests': ['basketball', 'music']},
    {'id': 3, 'name': 'Charlie', 'interests': ['coding', 'music']},
    {'id': 4, 'name': 'David',   'interests': ['music']},
]

# groups = find_employees(employees)


def find_pairs(employees: list[dict]) -> set[tuple[int, int]]:
    groups = find_employees(employees=employees)
    pairs = set()
    for emps in groups.values():
        emps = list(emps)
        for i in range(len(emps)):
            for j in range(i + 1, len(emps)):
                pair = (min(emps[i], emps[j]), max(emps[i], emps[j]))
                pairs.add(pair)
    return pairs

print(find_pairs(employees=employees))

#########################################################################################
# Reference solution
#
# Assumptions confirmed with the interviewer:
# - Interests are case- and whitespace-insensitive; blank interests are dropped.
# - The same id may appear in several records -> their interests merge.
# - Output sets are unordered; key order doesn't matter.
# - ~1e5 employees, 0..~20 interests each -> fits in memory.
#########################################################################################

from typing import Iterable


def normalize_interest(raw: str) -> str:
    """'Music', ' music ' -> 'music'.

    The only place normalization lives, so a new rule (e.g. 'bball' ->
    'basketball') is a one-line change.
    """
    return raw.strip().lower()


def group_by_interest(employees: Iterable[dict]) -> dict[str, set[int]]:
    """Inverted index: interest -> ids of employees who list it.

    No dedup code is needed: the set absorbs a repeated (interest, id) whether
    it comes from one record listing 'music' twice or from the same id
    appearing in two records.

    Time:  O(N * k * L)  N records, k interests each, L = max interest length
                         (strip, lower and hashing are each O(L)).
    Space: O(N * k) for the result -- each record adds at most k ids, and
           unique keys U <= N * k are covered by the same bound.
           O(L) auxiliary; `employees` can be a stream from disk.
    """
    index = defaultdict(set)
    for emp in employees:
        emp_id = emp["id"]
        for raw in emp["interests"]:
            interest = normalize_interest(raw)
            if interest:
                index[interest].add(emp_id)
    # Plain dict: a defaultdict would silently insert an empty set when the
    # caller looks up a missing interest, mutating their result.
    return dict(index)


def find_shared_interest_pairs(employees: Iterable[dict]) -> set[tuple[int, int]]:
    """Every unordered pair (a, b), a < b, sharing at least one interest.

    Two employees share an interest iff they sit in the same group of the
    inverted index, so pairs only ever come from within a group.

    Canonical form: sorting a group and only pairing i with j > i emits
    (a, b) with a < b, so (2, 3) and (3, 2) can't both appear. The outer set
    collapses pairs that share more than one interest.

    Time:  O(sum(s_i^2)) over group sizes s_i, plus building the index.
           Sorting is O(s_i log s_i) and is dominated. Worst case O(N^2)
           when one interest is shared by everyone.
    Space: O(N^2) worst case -- N(N-1)/2 pairs is the size of the answer
           itself, so no algorithm can beat it (output-sensitive bound).
    """
    pairs = set()
    for ids in group_by_interest(employees).values():
        ids = sorted(ids)
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                pairs.add((ids[i], ids[j]))
    return pairs


def interests_by_employee(employees: Iterable[dict]) -> dict[int, set[str]]:
    """Forward index: id -> normalized interests. Backs share_interest()."""
    index = defaultdict(set)
    for emp in employees:
        for raw in emp["interests"]:
            interest = normalize_interest(raw)
            if interest:
                index[emp["id"]].add(interest)
    return dict(index)


def share_interest(by_employee: dict[int, set[str]], a: int, b: int) -> bool:
    """Do a and b share an interest? O(min(k_a, k_b)), no pair table needed.

    This is the answer to "what does the caller actually need?" when the
    full pair set is too big to materialize.
    """
    return not by_employee.get(a, set()).isdisjoint(by_employee.get(b, set()))


# Scale: a billion employees
#
# What breaks first is the O(N * k) accumulator, not reading the input
# (that can be streamed). So distribute the accumulator with MapReduce:
#   map:     record -> (normalize_interest(i), id) for each interest i
#   shuffle: by hash(interest) % R, so one interest lands on one reducer
#   reduce:  (interest, [ids]) -> set(ids)
#
# Hot keys: 'music' with 1e8 ids overloads a single reducer while the rest
# idle. Salt the key ('music#0' .. 'music#99') to spread the load, then
# merge the partial sets in a second, much smaller pass.
#
# Pairs at that scale: C(1e8, 2) ~ 5e15 pairs (~80 PB) for one interest.
# More machines isn't the fix -- question the requirement instead:
#   - point query "do a and b share?"   -> share_interest(), O(k)
#   - "who is most like a?"             -> top-k by overlap count
#   - very common interests carry little signal -> drop or down-weight
#     them, IDF-style, before generating pairs


if __name__ == "__main__":
    sample = [
        {'id': 1, 'name': 'Alice',   'interests': ['basketball', 'coding']},
        {'id': 2, 'name': 'Bob',     'interests': ['basketball', 'music']},
        {'id': 3, 'name': 'Charlie', 'interests': ['coding', 'music']},
        {'id': 4, 'name': 'David',   'interests': ['music']},
    ]

    # Core problem
    assert group_by_interest(sample) == {
        'basketball': {1, 2},
        'coding':     {1, 3},
        'music':      {2, 3, 4},
    }
    assert group_by_interest([]) == {}
    # Mixed case/whitespace collapse, repeated id merges, blanks dropped
    messy = [
        {'id': 1, 'name': 'A', 'interests': ['Music', ' music ', 'MUSIC']},
        {'id': 1, 'name': 'A', 'interests': ['coding']},
        {'id': 2, 'name': 'B', 'interests': ['   ', '']},
    ]
    assert group_by_interest(messy) == {'music': {1}, 'coding': {1}}

    # Follow-up: pairs
    assert find_shared_interest_pairs(sample) == {
        (1, 2), (1, 3), (2, 3), (2, 4), (3, 4),
    }
    # Two shared interests, ids given in descending order -> one canonical pair
    assert find_shared_interest_pairs([
        {'id': 3, 'name': 'C', 'interests': ['a', 'b']},
        {'id': 2, 'name': 'B', 'interests': ['a', 'b']},
    ]) == {(2, 3)}

    # Follow-up: on-demand query instead of materializing pairs
    by_emp = interests_by_employee(sample)
    assert share_interest(by_emp, 1, 2)
    assert not share_interest(by_emp, 1, 4)
    assert not share_interest(by_emp, 1, 99)  # unknown id

    print("all tests passed")
