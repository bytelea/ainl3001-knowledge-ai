"""
AINL3001
BSP 2026

Topic 3 Lab

Informed Search and Heuristics

This week we introduce:

0. Manual exploration of heuristics,
1. Manhattan Distance,
2. Greedy Best-First Search,
3. A* Search.

The goal is to compare these algorithms
against BFS from Week 2.

TASKS

Task 0:
    Explore a manual heuristic.

Task 1:
    Implement the Manhattan Distance heuristic

Task 2:
    Implement Greedy Best-First Search

Task 3:
    Implement A* Search

Task 4:
    Compare A* against BFS
"""

from collections import deque
import heapq


# --------------------------------------------------
# GRID CONFIGURATION
# --------------------------------------------------

GRID_SIZE = 10

START_STATE = (0, 0)

GOAL_STATE = (9, 9)

OBSTACLES = [
    (2, 1),
    (2, 2),
    (2, 3),
    (2, 4),
    (5, 6),
    (6, 6),
    (7, 6)
]


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def get_neighbours(state):

    x, y = state

    possible_moves = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1)
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
# TASK 0 - MANUAL HEURISTIC EXPLORATION
# --------------------------------------------------


# --------------------------------------------------
# TASK 1 - MANHATTAN DISTANCE
# --------------------------------------------------

def manhattan_distance(state, goal):
    """
    Returns Manhattan Distance

    Formula:

    abs(goal_x - current_x)
    +
    abs(goal_y - current_y)
    """

    x1, y1 = state
    x2, y2 = goal

    return abs(x2 - x1) + abs(y2 - y1)


# --------------------------------------------------
# PROVIDED FROM WEEK 2
# --------------------------------------------------

def reconstruct_path(parents, goal):

    path = []

    current = goal

    while current is not None:

        path.append(current)

        current = parents[current]

    return list(reversed(path))


# --------------------------------------------------
# TASK 2 - GREEDY BEST-FIRST SEARCH
# --------------------------------------------------

def greedy_best_first_search(start, goal):
    """
    Greedy Best-First Search

    Uses only:

    h(n)

    where h(n) is the Manhattan Distance
    from the current state to the goal.

    Greedy ignores the path cost travelled so far.
    """

    frontier = []

    # Add start state to priority queue.
    # Priority = heuristic value.
    heapq.heappush(
        frontier,
        (manhattan_distance(start, goal), start)
    )

    visited = set()

    parents = {
        start: None
    }

    while frontier:

        heuristic, current = heapq.heappop(frontier)

        # Goal found
        if current == goal:
            return reconstruct_path(parents, goal)

        # Ignore nodes already explored
        if current in visited:
            continue

        visited.add(current)

        # Explore neighbours
        for neighbour in get_neighbours(current):

            if neighbour not in visited and neighbour not in parents:

                parents[neighbour] = current

                priority = manhattan_distance(
                    neighbour,
                    goal
                )

                heapq.heappush(
                    frontier,
                    (priority, neighbour)
                )

    # No path found
    return None


# --------------------------------------------------
# TASK 3 - A*
# --------------------------------------------------

def astar(start, goal):
    """
    A* Search

    Uses:

    f(n) = g(n) + h(n)

    where:

    g(n) = path cost so far

    h(n) = Manhattan Distance

    f(n) = estimated total cost
    """

    frontier = []

    # At the start:
    # g(start) = 0
    # f(start) = 0 + heuristic
    heapq.heappush(
        frontier,
        (manhattan_distance(start, goal), start)
    )

    parents = {
        start: None
    }

    g_cost = {
        start: 0
    }

    visited = set()

    while frontier:

        f_score, current = heapq.heappop(frontier)

        # Goal found
        if current == goal:
            return reconstruct_path(parents, goal)

        if current in visited:
            continue

        visited.add(current)

        # Explore neighbours
        for neighbour in get_neighbours(current):

            # Every move costs 1
            new_g_cost = g_cost[current] + 1

            # If this is a new node OR
            # we found a cheaper route to it
            if (
                neighbour not in g_cost
                or new_g_cost < g_cost[neighbour]
            ):

                g_cost[neighbour] = new_g_cost

                parents[neighbour] = current

                h = manhattan_distance(
                    neighbour,
                    goal
                )

                f = new_g_cost + h

                heapq.heappush(
                    frontier,
                    (f, neighbour)
                )

    # No path found
    return None


# --------------------------------------------------
# BFS FROM WEEK 2
# Used here so that we can compare it with A*
# --------------------------------------------------

def bfs(start, goal):

    queue = deque([start])

    visited = {start}

    parents = {
        start: None
    }

    while queue:

        current = queue.popleft()

        if current == goal:
            return reconstruct_path(parents, goal)

        for neighbour in get_neighbours(current):

            if neighbour not in visited:

                visited.add(neighbour)

                parents[neighbour] = current

                queue.append(neighbour)

    return None


# --------------------------------------------------
# TESTING AREA
# --------------------------------------------------

if __name__ == "__main__":

    print("=" * 50)
    print("WEEK 3")
    print("=" * 50)

    print("\nTASK 0 - MANUAL HEURISTIC EXPLORATION")

    manual_goal = (4, 4)

    state_a = (0, 0)
    state_b = (2, 2)
    state_c = (4, 3)

    print("\nGoal State =", manual_goal)

    print("\nState A =", state_a)
    print("State B =", state_b)
    print("State C =", state_c)

    print("\nManhattan Distances:")

    print(
        "State A:",
        manhattan_distance(state_a, manual_goal)
    )

    print(
        "State B:",
        manhattan_distance(state_b, manual_goal)
    )

    print(
        "State C:",
        manhattan_distance(state_c, manual_goal)
    )


    # --------------------------------------------------
    # GREEDY SEARCH
    # --------------------------------------------------

    print("\n" + "=" * 50)

    print("GREEDY BEST-FIRST SEARCH")

    greedy_path = greedy_best_first_search(
        START_STATE,
        GOAL_STATE
    )

    print("\nGreedy Path:")
    print(greedy_path)

    if greedy_path is not None:
        print(
            "Greedy Path Length:",
            len(greedy_path) - 1
        )


    # --------------------------------------------------
    # A*
    # --------------------------------------------------

    print("\n" + "=" * 50)

    print("A* SEARCH")

    astar_path = astar(
        START_STATE,
        GOAL_STATE
    )

    print("\nA* Path:")
    print(astar_path)

    if astar_path is not None:
        print(
            "A* Path Length:",
            len(astar_path) - 1
        )


    # --------------------------------------------------
    # BFS COMPARISON
    # --------------------------------------------------

    print("\n" + "=" * 50)

    print("BFS COMPARISON")

    bfs_path = bfs(
        START_STATE,
        GOAL_STATE
    )

    print("\nBFS Path:")
    print(bfs_path)

    if bfs_path is not None:
        print(
            "BFS Path Length:",
            len(bfs_path) - 1
        )


    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    print("\n" + "=" * 50)

    print("SUMMARY")

    print(
        "Greedy uses h(n) only."
    )

    print(
        "A* uses f(n) = g(n) + h(n)."
    )

    print(
        "BFS searches level by level without a heuristic."
    )

    print("=" * 50)
