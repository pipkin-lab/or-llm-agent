from ortools.linear_solver import pywraplp
from itertools import combinations, combinations_with_replacement

# Define the set of wells N = {1, 2, ..., 8}
N = list(range(1, 9))
n_nodes = len(N)

# Distance matrix c[i][j] for wells 1..8
# We'll use a dictionary or a 2D list indexed by well numbers.
# Initialize with 0
c = [[0.0] * 9 for _ in range(9)]

# Populate distances from Table 8-4
# c[i][j] = c[j][i]
distances = {
    (1, 2): 1.3, (1, 3): 2.1, (1, 4): 0.9, (1, 5): 0.7, (1, 6): 1.8, (1, 7): 2.0, (1, 8): 1.5,
    (2, 3): 0.9, (2, 4): 1.8, (2, 5): 1.2, (2, 6): 2.6, (2, 7): 2.3, (2, 8): 1.1,
    (3, 4): 2.6, (3, 5): 1.7, (3, 6): 2.5, (3, 7): 1.9, (3, 8): 1.0,
    (4, 5): 0.7, (4, 6): 1.6, (4, 7): 1.5, (4, 8): 0.9,
    (5, 6): 0.9, (5, 7): 1.1, (5, 8): 0.8,
    (6, 7): 0.6, (6, 8): 1.0,
    (7, 8): 0.5
}

for (i, j), d in distances.items():
    c[i][j] = d
    c[j][i] = d

# Coast to Well 1 distance
c_coast_well1 = 5.0

# Create the solver (MILP because variables are binary)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Define binary variables y[i][j] for i < j in N
y = dict()
for i in range(1, 9):
    for j in range(i + 1, 9):
        y[i, j] = solver.IntVar(0, 1, 'y_' + str(i) + '_' + str(j))

# Objective function: Minimize total cost
# Z = 5.0 + sum(c[i][j] * y[i][j])
objective = solver.Objective()
objective.SetCoefficient(0) # Just to initialize, we will build the sum properly

# Actually, it's better to build the expression and pass it to Minimize
obj_expr = c_coast_well1
for i in range(1, 9):
    for j in range(i + 1, 9):
        obj_expr += c[i][j] * y[i, j]

solver.Minimize(obj_expr)

# Constraint 1: Tree Cardinality
# Sum of all y[i][j] = n_nodes - 1 = 7
total_edges = 0
for i in range(1, 9):
    for j in range(i + 1, 9):
        total_edges += y[i, j]

solver.Add(total_edges == n_nodes - 1)

# Constraint 2: Connectivity (Subtour Elimination)
# For all non-empty proper subsets S of N, sum of y[i][j] where i in S and j not in S >= 1
# Since N is small (8 nodes), we can enumerate all subsets.
# A subset S is represented by a bitmask or a set of nodes.
# We need to check all S such that S is not empty and S is not N.

import itertools

# Generate all subsets of N
all_nodes_set = set(N)
for r in range(1, n_nodes):
    for S in itertools.combinations(N, r):
        S_set = set(S)
        # S must be a proper subset, so S_set != all_nodes_set
        # Since r < n_nodes, S_set is automatically a proper subset.
        # Also S is not empty since r >= 1.
        
        # Sum of y[i][j] such that i in S and j not in S
        # Note: y is defined for i < j.
        # If i in S and j not in S, the edge (i, j) crosses the cut.
        # We need to be careful with the definition of y[i, j] where i < j.
        # The edge crosses the cut if (i in S and j not in S) OR (j in S and i not in S).
        # In our y dictionary, keys are (i, j) with i < j.
        # So for a given key (i, j):
        # If i in S and j not in S -> crosses.
        # If i not in S and j in S -> crosses.
        # If both in S or both not in S -> does not cross.
        
        cut_sum = 0
        for i in S:
            for j in N:
                if j in S:
                    continue
                # Edge between i and j. Let a = min(i, j), b = max(i, j).
                a = min(i, j)
                b = max(i, j)
                # This edge is represented by y[a, b]
                cut_sum += y[a, b]
        
        solver.Add(cut_sum >= 1)

# Solve the problem
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")