
# Core Recursion

1. 
- IDENTITY - what value does an empty subtree represent
- COMBINE - computer the result from childrens and the node values
- count_nodes = IDENTITY = 0; COMBINE = left + right + 1

2.
- It needed a check if the left or right is empty without it the min will report to parent that it has hit leaf nodes
even if the other subtree has elements.
- it will fail for a skewed tree

3.
- each node returns to it's parent the curr dia (old dia + 1)
- 

4.
- the time complexity of fully skewed tree is O(n^2). Because for every node the tree has to calculate the height of all of it's subtree again and again.
