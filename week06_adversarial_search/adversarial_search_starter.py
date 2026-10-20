"""
AINL3001 — Knowledge-Driven AI
Week 6 — Adversarial Search (Tic-Tac-Toe)
BSP 2026

X is MAX (+1 for a win); O is MIN (-1 for a win).
A draw has utility 0. Search assumes both players play optimally.

Tasks:
0. Evaluate a small game tree manually.
1. Represent and display a board; implement legal moves.
2. Check winners, terminal states and utility.
3. Implement Minimax.
4. Choose the best move for X.
5. Count visited game-tree nodes.
6. Implement Alpha-Beta Pruning and compare results.

Extensions: depth-limited search, heuristic evaluation, Connect Four.
"""

# TASK 0 — MANUAL MINIMAX
print("=" * 50)
print("TASK 0 — MANUAL MINIMAX")
print("=" * 50)
print(r"""
            MAX
           /   \
         MIN   MIN
        /  \   /  \
       3    5  2    9
""")
print("Left MIN returns:", min(3, 5))
print("Right MIN returns:", min(2, 9))
print("MAX chooses:", max(min(3, 5), min(2, 9)))
print("MAX follows the left branch because 3 is greater than 2.")

# BOARD — X plays next (three X marks and two O marks).
# Board positions are numbered 0 to 8, left to right, top to bottom.
board = [
    "X", "O", "X",
    " ", "O", " ",
    " ", " ", "X",
]

WINNING_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]


# --------------------------------------------------
# TASK 1 — BOARD REPRESENTATION
# --------------------------------------------------

def print_board(state):
    """Display the nine cells as a 3-by-3 board."""
    for row in range(0, 9, 3):
        print(f"{state[row]} | {state[row + 1]} | {state[row + 2]}")
        if row < 6:
            print("--+---+--")


# --------------------------------------------------
# TASK 1 — AVAILABLE MOVES
# --------------------------------------------------

def available_moves(state):
    """Return indices of empty cells (0 through 8)."""
    return [index for index, cell in enumerate(state) if cell == " "]


# --------------------------------------------------
# TASK 1 — MAKE A MOVE
# --------------------------------------------------

def make_move(state, move, player):
    """Return a NEW board with player ('X' or 'O') at move.

    Assume move is legal. Do not modify the input board.
    """
    new_state = state.copy()
    new_state[move] = player
    return new_state


# --------------------------------------------------
# TASK 2 — WINNER
# --------------------------------------------------

def check_winner(state):
    """Return 'X', 'O' or None by checking all winning lines."""
    for a, b, c in WINNING_LINES:
        if state[a] != " " and state[a] == state[b] == state[c]:
            return state[a]
    return None


# --------------------------------------------------
# TASK 2 — TERMINAL STATE
# --------------------------------------------------

def is_terminal(state):
    """Return True for a win or a full board (draw)."""
    return check_winner(state) is not None or not available_moves(state)


# --------------------------------------------------
# TASK 2 — UTILITY
# --------------------------------------------------

def utility(state):
    """Return +1 for X win, -1 for O win, 0 for draw/no winner.

    Minimax calls this only at terminal states.
    """
    winner = check_winner(state)

    if winner == "X":
        return 1
    if winner == "O":
        return -1
    return 0


# --------------------------------------------------
# TASK 3 — MINIMAX
# --------------------------------------------------

def minimax(state, maximizing, counter):
    """Return game-theoretic score; count every visited node.

    maximizing=True means X moves next; False means O moves next.
    counter is a one-item dictionary: {'nodes': 0}.
    """
    counter["nodes"] += 1

    if is_terminal(state):
        return utility(state)

    if maximizing:
        best_score = float("-inf")

        for move in available_moves(state):
            child = make_move(state, move, "X")
            score = minimax(child, False, counter)
            best_score = max(best_score, score)

        return best_score

    best_score = float("inf")

    for move in available_moves(state):
        child = make_move(state, move, "O")
        score = minimax(child, True, counter)
        best_score = min(best_score, score)

    return best_score


# --------------------------------------------------
# TASK 4 AND 5 — BEST MOVE
# --------------------------------------------------

def best_move(state, counter):
    """Return the best move index for X, or None if game is over.

    Count nodes in recursive Minimax searches. Ties use first move.
    """
    if is_terminal(state):
        return None

    best_score = float("-inf")
    best_choice = None

    for move in available_moves(state):
        child = make_move(state, move, "X")
        score = minimax(child, False, counter)

        if score > best_score:
            best_score = score
            best_choice = move

    return best_choice


# --------------------------------------------------
# TASK 6 — ALPHA-BETA PRUNING
# --------------------------------------------------

def alpha_beta(state, maximizing, alpha, beta, counter):
    """Return the same score as Minimax, pruning irrelevant branches.

    alpha = best score MAX can guarantee so far.
    beta  = best score MIN can guarantee so far.
    """
    counter["nodes"] += 1

    if is_terminal(state):
        return utility(state)

    if maximizing:
        value = float("-inf")

        for move in available_moves(state):
            child = make_move(state, move, "X")
            score = alpha_beta(child, False, alpha, beta, counter)
            value = max(value, score)
            alpha = max(alpha, value)

            if alpha >= beta:
                break

        return value

    value = float("inf")

    for move in available_moves(state):
        child = make_move(state, move, "O")
        score = alpha_beta(child, True, alpha, beta, counter)
        value = min(value, score)
        beta = min(beta, value)

        if alpha >= beta:
            break

    return value


# --------------------------------------------------
# TASK 6 — BEST MOVE WITH ALPHA-BETA
# --------------------------------------------------

def best_move_alpha_beta(state, counter):
    """Return the best move index for X using Alpha-Beta search."""
    if is_terminal(state):
        return None

    best_score = float("-inf")
    best_choice = None
    alpha = float("-inf")
    beta = float("inf")

    for move in available_moves(state):
        child = make_move(state, move, "X")
        score = alpha_beta(child, False, alpha, beta, counter)

        if score > best_score:
            best_score = score
            best_choice = move

        alpha = max(alpha, best_score)

    return best_choice


# --------------------------------------------------
# TESTING — RUN PYTHON FILE IN VS CODE
# --------------------------------------------------

if __name__ == "__main__":
    print("\nCurrent board (X to move):")
    print_board(board)
    print("\nAvailable moves:", available_moves(board))
    print("Winner:", check_winner(board))
    print("Terminal:", is_terminal(board))
    print("Utility:", utility(board))

    # Task 2 checks: X win, O win and draw.
    x_win_board = [
        "X", "X", "X",
        "O", "O", " ",
        " ", " ", " ",
    ]
    o_win_board = [
        "X", "X", " ",
        "O", "O", "O",
        "X", " ", " ",
    ]
    draw_board = [
        "X", "O", "X",
        "X", "O", "O",
        "O", "X", "X",
    ]

    print("\nTask 2 outcome checks:")
    print("X-win board winner:", check_winner(x_win_board))
    print("O-win board winner:", check_winner(o_win_board))
    print(
        "Draw board terminal:",
        is_terminal(draw_board),
        "| utility:",
        utility(draw_board),
    )

    # For a meaningful comparison, both algorithms use the same board
    # and count the same thing: recursive game-tree nodes visited.
    minimax_counter = {"nodes": 0}
    move_minimax = best_move(board, minimax_counter)
    print("\nMinimax best move for X:", move_minimax)
    print("Minimax nodes visited:", minimax_counter["nodes"])

    alpha_beta_counter = {"nodes": 0}
    move_ab = best_move_alpha_beta(board, alpha_beta_counter)
    print("\nAlpha-Beta best move for X:", move_ab)
    print("Alpha-Beta nodes visited:", alpha_beta_counter["nodes"])

    if move_minimax is not None:
        print("\nBoard after Minimax move:")
        print_board(make_move(board, move_minimax, "X"))

    print("\nComparison:")
    print("Same chosen move:", move_minimax == move_ab)
    print(
        "Nodes saved by Alpha-Beta:",
        minimax_counter["nodes"] - alpha_beta_counter["nodes"],
    )

    print("\nReflection:")
    print(
        "1. Tic-Tac-Toe is a search problem because each legal move creates "
        "a new state and possible future moves form a game tree."
    )
    print(
        "2. Minimax assumes an optimal opponent so MAX chooses the best "
        "outcome it can guarantee even against the strongest reply."
    )
    print(
        "3. A utility function gives terminal outcomes numerical values so "
        "Minimax can compare wins, losses and draws."
    )
    print(
        "4. As games become larger, the game tree grows rapidly, so full "
        "Minimax becomes expensive and techniques such as Alpha-Beta "
        "pruning become more useful."
    )
