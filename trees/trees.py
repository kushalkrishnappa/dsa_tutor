"""Tree Data Structure and Algorithms"""

class TreeNode:
    def __init__(self, val, left=None, right=None):
        """definition for a binary tree node."""
        self.val = val
        self.left = left
        self.right = right

################################################################
# Recursion Contract
################################################################

def count_nodes(node):
    """Bottom up aggregation.
    
            2 (0 + 0 + 1 = num of nodes = 1)
           / \
        None  None (return 0)
    """
    # if not node: # do not use this - check __bool__ in TreeNode
    if node is None:
        return 0
    left = count_nodes(node.left)
    right = count_nodes(node.right)
    return left + right + 1

def sum_values(node):
    """Bottom up aggregation
    
            2 (0 + 0 + node.val(2) = sum of values = 2)
           / \
        None  None (return 0)
    """
    # if not node: # do not use this - check __bool__ in TreeNode
    if node is None:
        return 0
    left = sum_values(node.left)
    right = sum_values(node.right)
    return left + right + node.val


#       1
#      / \
#     0   3        <- note the 0
#    /
#   4
root = TreeNode(1, TreeNode(0, TreeNode(4)), TreeNode(3))
print(count_nodes(root), sum_values(root))

################################################################
# Tree Traversals
################################################################
from collections import deque

def level_order(node):
    if root is None:
        return []
    queue = deque([node])
    levels = []
    while queue:
        level_size = len(queue)
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left is not None: queue.append(node.left)
            if node.right is not None: queue.append(node.right)
        levels.append(level)
    return levels


#       1
#      / \
#     2   3
#    / \   \
#   4   5   6
root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3, None, TreeNode(6)))
print(level_order(root))   # expect: [[1], [2, 3], [4, 5, 6]]

def preorder_iter(root):
    if root is None:
        return []
    stack, result = [root], []
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right is not None: stack.append(node.right)
        if node.left is not None: stack.append(node.left)
    return result

def inorder_iter(root) -> list:
    if root is None:
        return []
    stack, result = [(root, False)], []
    while stack:
        node, visited = stack.pop()
        if not visited:
            if node.right is not None: stack.append((node.right, False)) 
            stack.append((node, True))
            if node.left is not None: stack.append((node.left, False))
        else:
            result.append(node.val)
    return result

def postorder_iter(root):
    if root is None:
        return []
    stack, result = [(root, False)], []
    while stack:
        node, visited = stack.pop()
        if not visited:
            stack.append((node, True))
            if node.right is not None: stack.append((node.right, False))
            if node.left is not None: stack.append((node.left, False))
        else:
            result.append(node.val)
    return result

################################################################
# Bottom-Up Aggregate
################################################################

def diameter_of_tree(root):
    def longest_path(root):
        if root is None:
            return -1
        left = longest_path(root.left)
        right = longest_path(root.right)
        nonlocal dia
        dia = max(dia, left + right + 2)
        return max(left, right) + 1
    dia = 0
    longest_path(root)
    return dia

def isBalanced(root: Optional[TreeNode]) -> bool:
    """Bottom Up Aggregate"""
    def height(root):
        if root is None:
            return 0
        left = height(root.left)
        right = height(root.right)
        if abs(left - right) > 1:
            nonlocal is_balanced
            if is_balanced:
                is_balanced = not is_balanced
        return max(left, right) + 1
    is_balanced = True
    height(root)
    return is_balanced

balanced = TreeNode(0, TreeNode(1, TreeNode(2), TreeNode(3)), TreeNode(4))
unbalanced = TreeNode(0, TreeNode(1, TreeNode(2, TreeNode(3, TreeNode(4)))))

print(f"balanced: {isBalanced(balanced)}")  # true
print(f"unbalanced: {isBalanced(unbalanced)}") # false

################################################################
# Top-Down Accumulate
################################################################

def has_path_sum(root: TreeNode, target: int):
    if root is None:
        return False
    # pass the information to the childern
    if target == root.val and all([root.left is None, root.right is None]): 
        return True
    return has_path_sum(root.left, target - root.val) \
        or has_path_sum(root.right, target - root.val)

root = TreeNode(5, TreeNode(4, TreeNode(11, TreeNode(7), TreeNode(2))), 
                TreeNode(8, TreeNode(13), TreeNode(4, None, TreeNode(1))))
print(f"Has PathSum: {has_path_sum(root, target=22)}")

################################################################
# Structural Compare
################################################################

def same_tree(root1: TreeNode, root2: TreeNode):
    if root1 is None and root2 is None:
        return True
    if root1 is None or root2 is None:
        return False
    return root1.val == root2.val \
        and same_tree(root1.left, root2.left) \
        and same_tree(root1.right, root2.right)

print(f"Same Tree: {same_tree(TreeNode(1, TreeNode(2)), TreeNode(1, TreeNode(3)))}")


################################################################
# Find Height and Depth
################################################################

def height_and_depth(root: TreeNode):
    if root is None:
        return -1
    global curr_depth
    curr_depth += 1
    left = height_and_depth(root.left)
    right = height_and_depth(root.right)
    height = max(left, right) + 1 # node
    curr_depth -= 1
    print(f"Node-{root.val} - height: {height} - depth: {curr_depth}") # ref: on node 0
    return height

curr_depth = 0
# height_and_depth(TreeNode(0, TreeNode(1, TreeNode(2), TreeNode(3)), TreeNode(4)))
"""
          0
    1.         4
2.     3.   
"""
