"""
Questions:
- can there be repeatition of the same record in before and after? Do you
want me to return the repition or return it only once in the output dict?
- Do I need to strip the input of spaces or can I assume input is clean?
- Can I assume all the permission, resources and user_id are lower cased?
- I will assume (user_id: str, resource_id: str, permission: str) order is
always true for every record.
- What can be the min and max log size for both before and after?
- I will add to modidfy if permission change is only there for the same user_id
and resource. For example: ("carol", "reports", "read") -> ("carol", "reports", "write")
as per the expectation. If there is a new resource for same user it will go into the 
added.

Time: O(N) for before to store the before, O(K) for after to traverse, compare against the before = O(N) + O(N + K)
Space: O(N) to store the before data + O(added + removed + modified)
"""

"""
- build a hm of before: key(user_id, resource), value(permission)
- iterate after and check if the permission is changed and append
to modified.
"""

class Permissions:
    """Valid Permissions for recourse."""

    ADDED = "added"
    REMOVED = "removed"
    MODIFIED = "modified"

def before_mapping(before: list[tuple[str, str, str]]) -> dict[tuple, str]:
    hm = {}
    for user_id, resource, permission in before:
        hm[(user_id, resource)] = [permission, 1]
    return hm

def build_modified_record(user_id: str, resource_id: str, before_perm: str, after_perm: str) -> dict:
    return {
            "user_id": user_id, 
            "resource_id": resource_id, 
            "before_permission": before_perm[0], 
            "after_permission": after_perm
        }

def compute_diff(
    before: list[tuple[str, str, str]],
    after: list[tuple[str, str, str]]
) -> dict[str, list[tuple|dict]]:
    before_map = before_mapping(before=before)

    # before = (a, b, c),  after = (a, b)
    # before - after = c
    # key = (user_id, resource) not in after then removed.

    added, removed, modified = [], [], []

    for user_id, resource, permission in after:
        if (user_id, resource) not in before_map: # Added
            added.append((user_id, resource, permission))
        elif before_map[(user_id, resource)][0] != permission: # Modified
            modified.append(build_modified_record(user_id, 
                                                  resource, 
                                                  before_map[(user_id, resource)], 
                                                  permission))
            occurance = before_map[(user_id, resource)][1]
            before_map[(user_id, resource)][1] = occurance - 1
        else:
            occurance = before_map[(user_id, resource)][1]
            before_map[(user_id, resource)][1] = occurance - 1
            
    for key, val in before_map.items():
        if val[1] == 1:
            removed.append((key[0], key[1], val[0]))

    added.sort()
    removed.sort()
    modified.sort(key=lambda x: (x["user_id"], x["resource_id"]))

    return {"added": added, "removed": removed, "modified": modified}
        

before = [
    ("alice", "reports",   "read"),
    ("alice", "dashboard", "admin"),
    ("bob",   "reports",   "write"),
]

after = [
    ("alice", "reports",   "write"),   # permission changed
    ("alice", "dashboard", "admin"),   # unchanged
    ("carol", "reports",   "read"),    # new user
    # bob removed entirely
]

result = compute_diff(before, after)
print(result)
