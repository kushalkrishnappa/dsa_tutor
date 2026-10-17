"""
Questions:
- will there be a missing values in the dict for certail columns?
- Can I assume the key are same across all the rows?
- What all characters can be present in both keys and values? Can I assume 
capital and lower english letters and numbers for keys and str(again same as mentioned) | int | float?
- what if the first record is empty and all other records are valid? Do you want me to skip the recond if it
is empty?
- what can be the max len of the key string or the val string.
"""

def parse_columns(records: list[dict]) -> dict[str, dict]:
    metadata = {}
    first = records[0]
    for key, value in first.items():
        record_metadata = {"column_len": max(len(key), len(str(value))), "type": type(value)}
        metadata[key] = record_metadata
    for i in range(1, len(records)):
        record = records[i]
        for key, value in record.items():
            record_metadata = {"column_len": max(metadata[key]["column_len"], len(str(value))), "type": type(value)}
            metadata[key] = record_metadata
    return metadata

def construct_header(column_metadata:dict[str, dict]) -> str:
    header = ""
    for column, metadata in column_metadata.items():
        column_len, column_type = metadata["column_len"], metadata["type"]
        if column_type == str:
            header.join(column + " " * (column_len - len(column)))
    

def format_table(records: list[dict]) -> str:
    """
    Renders a list of record dicts as a plaintext columnar table.

    Args:
        records: list of dicts with identical keys.

    Returns:
        Formatted table as a string.
    """
    """
    Approach:
    - parse the columns -> store in list
    - write a function to print the separator.
    """
    if not records:
        return ""
    result = ""

    column_metadata = parse_columns(records)
    print(column_metadata)


    return result

records = [
    {"name": "Alice", "department": "Engineering", "salary": 95000.5, "years": 3},
    {"name": "Bob", "department": "Sales", "salary": 72000.0, "years": 7},
    {"name": "Cassandra", "department": "Engineering", "salary": 110000.75, "years": 10},
]

format_table(records)



"""
Approach: two passes
- pass 1 (measure): render every value to a string, find each column's width,
  and decide each column's alignment (numbers right, text left).
- pass 2 (build):   pad every cell to its column width and join the lines.
Time: O(R * C)   R = rows, C = columns
Space: O(R * C)  the rendered cells
"""

# ---------- cell helpers ----------

def is_numeric(value) -> bool:
    # bool is a subclass of int, so exclude it explicitly
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def render_cell(value) -> str:
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def pad(text: str, width: int, right_align: bool) -> str:
    return text.rjust(width) if right_align else text.ljust(width)


# ---------- pass 1: measure ----------

def column_widths(columns: list[str], cells: list[list[str]]) -> list[int]:
    # a column is as wide as its longest text, header included
    widths = [len(col) for col in columns]
    for row in cells:
        for i, text in enumerate(row):
            widths[i] = max(widths[i], len(text))
    return widths


def column_alignments(columns: list[str], records: list[dict]) -> list[bool]:
    # right-align a column only if every value in it is a number
    return [all(is_numeric(record[col]) for record in records) for col in columns]


# ---------- pass 2: build ----------

def format_line(texts: list[str], widths: list[int], right_align: list[bool]) -> str:
    padded = [pad(text, widths[i], right_align[i]) for i, text in enumerate(texts)]
    return " | ".join(padded)


def format_separator(widths: list[int]) -> str:
    return "-|-".join("-" * w for w in widths)


def format_table(records: list[dict]) -> str:
    if not records:
        return ""

    columns = list(records[0].keys())
    cells = [[render_cell(record[col]) for col in columns] for record in records]

    # pass 1: measure
    widths = column_widths(columns, cells)
    right_align = column_alignments(columns, records)

    # pass 2: build
    header = format_line(columns, widths, right_align)
    separator = format_separator(widths)
    rows = [format_line(row, widths, right_align) for row in cells]

    return "\n".join([header, separator, *rows])
