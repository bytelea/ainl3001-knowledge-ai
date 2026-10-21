"""
AINL3001 - Knowledge-Driven AI
BSP 2026
Topic 2: Uninformed Search

In Week 1 we represented a problem as states and actions.

This week we will explore a state space using:

1. Breadth-First Search (BFS),
2. Depth-First Search (DFS).

----------------------------------------------------
YOUR TASKS

Task 1:
    Complete the BFS algorithm

Task 2:
    Complete the DFS algorithm

Task 3:
    Compare the paths returned

Task 4:
    Explain the differences between BFS and DFS

----------------------------------------------------
"""

# the collections functionality is not used yet in the 
# starter.py. It is your job to make use of it for the
# solution.
from collections import deque


# --------------------------------------------------
# GRID CONFIGURATION
# --------------------------------------------------

GRID_SIZE = 5

START_STATE = (0, 0)

GOAL_STATE = (4, 4)

OBSTACLES = [
    (1, 1),
    (2, 2),
    (3, 2)
]


# --------------------------------------------------
# HELPER FUNCTION
# --------------------------------------------------

def get_neighbours(state):
    """
    Returns all valid neighbouring states.

    A valid move:
        - stays inside the grid
        - does not move into an obstacle
    """

    x, y = state

    possible_moves = [
        (x + 1, y),  # right
        (x - 1, y),  # left
        (x, y + 1),  # down
        (x, y - 1)   # up
    ]

    neighbours = []

    for move in possible_moves:

        mx, my = move

        inside_grid = (
            0 <= mx < GRID_SIZE and
            0 <= my < GRID_SIZE
        )

        if inside_grid and move not in OBSTACLES:
            neighbours.append(move)

    return neighbours


# --------------------------------------------------
# TASK 1 - BFS
# --------------------------------------------------

def bfs(start, goal):
    """
    Breadth-First Search

    1. Create a queue,
    2. Create a visited set,
    3. Explore states,
    4. Return path when goal is found.

    Uses:
        Queue (FIFO)
    """

    queue = deque([
        (start, [start])
    ])

    visited = {
        start
    }

    while queue:

        current, path = queue.popleft()

        if current == goal:
            return path

        for neighbour in get_neighbours(current):

            if neighbour not in visited:

                visited.add(neighbour)

                new_path = path + [neighbour]

                queue.append(
                    (neighbour, new_path)
                )

    return []


# --------------------------------------------------
# TASK 2 - DFS
# --------------------------------------------------

def dfs(start, goal):
    """
    Depth-First Search

    1. Create a stack,
    2. Create a visited set,
    3. Explore states,
    4. Return path when goal is found.

    Uses:
        Stack (Python list)
    """

    stack = [
        (start, [start])
    ]

    visited = {
        start
    }

    while stack:

        current, path = stack.pop()

        if current == goal:
            return path

        for neighbour in get_neighbours(current):

            if neighbour not in visited:

                visited.add(neighbour)

                new_path = path + [neighbour]

                stack.append(
                    (neighbour, new_path)
                )

    return []


# --------------------------------------------------
# DEMONSTRATION SECTION
# --------------------------------------------------

print("===================================")
print(" WEEK 2 - UNINFORMED SEARCH")
print("===================================")

print("\nStart State:")
print(START_STATE)

print("\nGoal State:")
print(GOAL_STATE)

print("\nObstacles:")
print(OBSTACLES)

print("\nNeighbours of Start State:")
print(get_neighbours(START_STATE))

print("\nRunning BFS...")
bfs_path = bfs(START_STATE, GOAL_STATE)

print("BFS Path:")
print(bfs_path)

print("\nRunning DFS...")
dfs_path = dfs(START_STATE, GOAL_STATE)

print("DFS Path:")
print(dfs_path)


# --------------------------------------------------
# TASK 3 - COMPARE PATHS
# --------------------------------------------------

print("\nBFS Path Length:")
print(len(bfs_path) - 1)

print("\nDFS Path Length:")
print(len(dfs_path) - 1)

if len(bfs_path) < len(dfs_path):
    print("\nBFS found a shorter path.")

elif len(dfs_path) < len(bfs_path):
    print("\nDFS found a shorter path.")

else:
    print("\nBoth algorithms found paths of equal length.")


# --------------------------------------------------
# REFLECTION QUESTIONS
# --------------------------------------------------

"""
Be prepared to discuss:

1. What data structure does BFS use?

2. What data structure does DFS use?

3. Why does BFS usually return a shorter path?

4. Which algorithm explores more states?

5. What effect do obstacles have?

"""
