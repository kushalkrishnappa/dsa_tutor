"""Sliding Window Technique for Arrays and Strings."""

def len_of_longest_substring(s: str) -> int:
    left = right = 0
    max_len = 0
    curr_window_set = set([])
    while right < len(s):
        while left < right and s[right] in curr_window_set:
            curr_window_set.remove(s[left])
            left += 1
        curr_window_set.add(s[right])
        max_len = max(max_len, len(curr_window_set))
        right += 1
    return max_len

print(f"abcabcbb: {len_of_longest_substring("abcabcbb")}")

def max_avg_subarray(arr: list, k: int):
    """Maximum Average Subarray"""
    left = right = 0
    max_avg = float("-inf")
    curr_sum = 0
    while right < len(arr):
        # expand the window
        while right - left < k and right < len(arr):
            curr_sum += arr[right]
            right += 1
        # logic
        max_avg = max(max_avg, curr_sum / k)
        # shrink
        curr_sum -= arr[left]
        left += 1
    return max_avg

print(f"Max Avg Subarray: {max_avg_subarray([1, 2, 3, 4, 5], 2)}")
