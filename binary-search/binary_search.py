"""Binary Search Technique.

[0, n] - find the number

[0, n + 1) == [0, n]
    code: lo, hi = 0, n;
    while lo < hi;
    else lo = mid + 1;

bounds:
1. arr[mid] >= target => lower_bound (c++) or bisect_left (python) => hi = mid

2. arr[mid] > target => upper_bound (c++) or bisect_right (python) => hi = mid
"""

def binary_search(arr: list, target: int) -> int:
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo)//2
        if arr[mid] == target:
            return mid
        elif arr[mid] > target:
            hi = mid - 1
        elif arr[mid] < target:
            lo = mid + 1
    return -1

assert(binary_search(arr=[1, 3, 4, 7, 9], target=4) == 2)
assert(binary_search(arr=[3, 4, 7, 9], target=1) == -1)
assert(binary_search(arr=[1, 3, 4, 7, 9], target=26) == -1)
assert(binary_search(arr=[1, 3, 4, 7, 9], target=9) == 4)
assert(binary_search(arr=[1, 3], target=3) == 1)
assert(binary_search(arr=[1, 3], target=4) == -1)
assert(binary_search(arr=[1], target=1) == 0)
assert(binary_search(arr=[1], target=4) == -1)
assert(binary_search(arr=[], target=4) == -1)

def binary_search_half_open(arr: list, target: int) -> int:
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = lo + (hi - lo)//2
        if arr[mid] >= target:
            hi = mid
        else:
            lo = mid + 1
    if lo < len(arr) and arr[lo] == target:
        return lo
    return -1

assert(binary_search_half_open(arr=[3, 4, 7, 9], target=1) == -1)
assert(binary_search_half_open(arr=[1, 3, 4, 7, 9], target=26) == -1)
assert(binary_search_half_open(arr=[1, 3, 4, 7, 9], target=9) == 4)
assert(binary_search_half_open(arr=[1, 3], target=3) == 1)
assert(binary_search_half_open(arr=[1, 3, 4, 7, 9], target=4) == 2)
assert(binary_search_half_open(arr=[1, 3], target=4) == -1)
assert(binary_search_half_open(arr=[1], target=1) == 0)
assert(binary_search_half_open(arr=[1], target=4) == -1)
assert(binary_search_half_open(arr=[], target=4) == -1)

def lower_bound(arr: list, target: int) -> int:
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = lo + (hi - lo)//2
        if arr[mid] >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo

assert(lower_bound(arr=[1, 3, 3, 3, 4], target=3) == 1)
assert(lower_bound(arr=[1, 3, 4, 7, 9], target=1) == 0)
assert(lower_bound(arr=[1, 3], target=3) == 1)
assert(lower_bound(arr=[1, 3, 4, 7, 9], target=4) == 2)
assert(lower_bound(arr=[1, 3], target=4) == 2)
assert(lower_bound(arr=[1], target=1) == 0)
assert(lower_bound(arr=[1], target=4) == 1)
assert(lower_bound(arr=[], target=4) == 0)
assert(lower_bound(arr=[1, 3, 5, 7], target=4) == 2)

def upper_bound(arr: list, target: int) -> int:
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = lo + (hi - lo)//2
        if arr[mid] > target:
            hi = mid
        else:
            lo = mid + 1
    return lo

assert(upper_bound(arr=[1, 3, 3, 3, 4], target=3) == 4)
assert(upper_bound(arr=[1, 3, 4, 7, 9], target=1) == 1)
assert(upper_bound(arr=[1, 3, 4, 4], target=4) == 4)
assert(upper_bound(arr=[1, 3, 4, 7, 9], target=4) == 3)
assert(upper_bound(arr=[1, 3], target=4) == 2)
assert(upper_bound(arr=[1], target=1) == 1)
assert(upper_bound(arr=[1], target=4) == 1)
assert(upper_bound(arr=[], target=4) == 0)
