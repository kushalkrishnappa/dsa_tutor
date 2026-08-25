"""Utility Functions for DSA."""


def print_line(line_len: int = 80):
    """Prints separator line of len 80."""
    print("-" * line_len)


def print_topic(topic: str, end: str = None):
    """Prints topic name in '#' block."""
    print()
    magic_hash = "#" * (39 - len(topic) // 2)
    print(
        f"{magic_hash}" + f" {topic} " + f"{magic_hash}",
        end=end,
    )
    print()
