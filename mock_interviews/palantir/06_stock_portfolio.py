"""
Questions:
- what is the format of the date?
- I will assume the data is clean and does not contain
tailing spaces.
- Are updates sorted? I will assume it otherwise as it
makes sense the change happens linear timeline.
- Do you want the result sorted by date?
- What can be the maximum size of updates?
- if the updates are nil, I wil return empty list. Is that okay?
"""

"""
Approach:

updates = [
    ("2024-05-01", "PLTR", 100),
    ("2024-05-01", "AMZN", 200),
    ("2024-05-05", "PLTR", 200),
    ("2024-05-05", "MSFT", 50),
    ("2024-05-08", "MSFT", 100),
    ("2024-05-08", "AMZN", 100),
]
== [("2024-05-01", 300), ("2024-05-05", 450), ("2024-05-08", 400)]

- if there is reps, for the same ticker with different prices on same date
how would you want me to handle it? == pick the last one and sorting by date 
will still make sure the order is maintained. The lastest value will replace
the earlier ones in hashmap.


- Sort the updated list by date.
- group by dates -> followed by ticker => nested hashmap {"date": {"ticker": value}}
- traverse the grouped hashmap and compute the total by comparing to the prev stock
prices.
"""
from collections import defaultdict

def calculate_total(dates: list[str], transactions: dict[dict[str, int]]) -> list[tuple[str, int]]:
    result = []
    holdings = {}
    total = 0
    for date in dates:
        for ticker, balance in transactions[date].items():
            total += balance - holdings.get(ticker, 0)
            holdings[ticker] = balance
        result.append((date, total))
    return result


def portfolio_totals(updates: list[tuple[str, str, int]]) -> list[tuple[str, int]]:
    """
    updates: list of (date, ticker, balance) records.
    Returns: list of (date, total_balance) — one entry per date that had a change.
    """
    if not updates:
        return []
    
    hm = defaultdict(dict)
    for date, ticker, price in updates:
        hm[date][ticker] = price
    return calculate_total(sorted(hm), hm)

updates = [
    ("2024-05-01", "PLTR", 100),
    ("2024-05-01", "AMZN", 200),
    ("2024-05-05", "PLTR", 200),
    ("2024-05-05", "MSFT", 50),
    ("2024-05-08", "MSFT", 100),
    ("2024-05-08", "AMZN", 100),
]

print(portfolio_totals(updates))
