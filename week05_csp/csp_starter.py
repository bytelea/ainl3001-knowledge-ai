"""
AINL3001 — Knowledge-Driven AI
Week 5 — Constraint Satisfaction Problems
BSP 2026

Australian map colouring: six regions and three colours.

Tasks
-----
0. Examine an invalid assignment.
1. Understand variables, domains and constraints.
2. Implement constraint checking.
3. Implement backtracking with simple variable selection.
4. Compare backtracking with brute force.
5. Improve variable selection using MRV.
"""

# --------------------------------------------------
# TASK 0 — MANUAL EXPLORATION
# --------------------------------------------------

example_assignment = {
    "WA": "Red",
    "NT": "Red",
    "SA": "Green",
    "Q": "Blue",
    "NSW": "Red",
    "V": "Green",
}

print("Manual CSP Exploration")
print(example_assignment)

# --------------------------------------------------
# TASK 1 — CSP REPRESENTATION
# --------------------------------------------------

variables = ["WA", "NT", "SA", "Q", "NSW", "V"]

domains = {
    variable: ["Red", "Green", "Blue"]
    for variable in variables
}

constraints = [
    ("WA", "NT"),
    ("WA", "SA"),
    ("NT", "SA"),
    ("NT", "Q"),
    ("SA", "Q"),
    ("SA", "NSW"),
    ("SA", "V"),
    ("Q", "NSW"),
    ("NSW", "V"),
]

# --------------------------------------------------
# TASK 2 — CONSTRAINT CHECKING
# --------------------------------------------------

def is_valid_assignment(assignment):
    """Return True if a complete or partial assignment is valid."""

    for region1, region2 in constraints:
        if region1 in assignment and region2 in assignment:
            if assignment[region1] == assignment[region2]:
                return False

    return True


# --------------------------------------------------
# TASK 3 AND TASK 5 — VARIABLE SELECTION
# --------------------------------------------------

def select_unassigned_variable(assignment):
    """Choose the unassigned region with the fewest legal colours."""

    best_variable = None
    fewest_legal_colours = float("inf")

    for variable in variables:

        if variable in assignment:
            continue

        legal_colours = 0

        for colour in domains[variable]:

            assignment[variable] = colour

            if is_valid_assignment(assignment):
                legal_colours += 1

            del assignment[variable]

        if legal_colours < fewest_legal_colours:
            fewest_legal_colours = legal_colours
            best_variable = variable

    return best_variable


# --------------------------------------------------
# TASK 3 — BACKTRACKING SEARCH
# --------------------------------------------------

def backtracking_search(assignment):
    """Return a complete valid assignment, or None if none exists."""

    if len(assignment) == len(variables):
        if is_valid_assignment(assignment):
            return assignment.copy()
        return None

    variable = select_unassigned_variable(assignment)

    for colour in domains[variable]:

        assignment[variable] = colour

        if is_valid_assignment(assignment):

            result = backtracking_search(assignment)

            if result is not None:
                return result

        del assignment[variable]

    return None


# --------------------------------------------------
# TASK 4 — BRUTE FORCE COMPARISON
# --------------------------------------------------

# Six regions with three colours each give 3 ** 6 = 729
# possible complete assignments. Backtracking can reject invalid
# partial assignments before building every complete assignment.


# --------------------------------------------------
# TESTING AREA
# --------------------------------------------------

if __name__ == "__main__":

    print("\n" + "=" * 50)
    print("WEEK 5 — CONSTRAINT SATISFACTION PROBLEMS")
    print("=" * 50)

    print("\nVariables:", variables)
    print("Domains:", domains)
    print("Constraints:", constraints)

    print("\nExample assignment valid?")
    print(is_valid_assignment(example_assignment))

    partial_assignment = {
        "WA": "Red",
        "NT": "Green"
    }

    print("\nPartial assignment valid?")
    print(is_valid_assignment(partial_assignment))

    print("\nSearching for a solution...")

    solution = backtracking_search({})

    print("Solution:", solution)

    if solution is not None:

        print(
            "\nSolution valid?",
            is_valid_assignment(solution)
        )

        print("\nColour assignment:")

        for region in variables:
            print(
                f"{region:4} -> {solution[region]}"
            )

    print(
        "\nPossible complete assignments:",
        3 ** len(variables)
    )

    print("\nReflection:")
    print("1. Backtracking happens when a choice leads to a violation or dead end.")
    print("2. It is faster than brute force because invalid partial assignments are rejected early.")
    print("3. MRV chooses the variable with the fewest legal choices, so difficult choices are handled earlier.")
    print("4. Timetabling can use lectures as variables, rooms/times as domains, and clash rules as constraints.")
