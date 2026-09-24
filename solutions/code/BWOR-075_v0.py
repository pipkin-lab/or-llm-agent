from ortools.linear_solver import pywraplp

# Define index sets
V = list(range(0, 9))  # Nodes 0 (Coast) through 8 (Wells)
N = list(range(1, 9))  # Well nodes 1 through 8
n_wells = len(N)       # 8

# Define the edge set E = {(i, j) | i, j in V, i < j}
E = list()
for i in range(0, 9):
    for j in range(i + 1, 9):
        E.append((i, j))

# Define cost parameters c_ij
c = dict()
c[0, 1] = 5.0
c[1, 2] = 1.3
c[1, 3] = 2.1
c[1, 4] = 0.9
c[1, 5] = 0.7
c[1, 6] = 1.8
c[1, 7] = 2.0
c[1, 8] = 1.5
c[2, 3] = 0.9
c[2, 4] = 1.8
c[2, 5] = 1.2
c[2, 6] = 2.6
c[2, 7] = 2.3
c[2, 8] = 1.1
c[3, 4] = 2.6
c[3, 5] = 1.7
c[3, 6] = 2.5
c[3, 7] = 1.9
c[3, 8] = 1.0
c[4, 5] = 0.7
c[4, 6] = 1.6
c[4, 7] = 1.5
c[4, 8] = 0.9
c[5, 6] = 0.9
c[5, 7] = 1.1
c[5, 8] = 0.8
c[6, 7] = 0.6
c[6, 8] = 1.0
c[7, 8] = 0.5

# For edges from Coast (node 0) to wells other than 1, cost is infinity (forbidden)
# We handle this by not adding those edges to the decision variables, or by setting a very large cost.
# Since the model says c_0j = infinity for j != 1, we simply do not create variables for (0, j) where j != 1.
# Valid edges involving node 0: only (0, 1).

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')
if solver is None:
    raise RuntimeError('SCIP solver not available')

# Create decision variables x_ij for each edge in E where c_ij is finite
x = dict()
for i, j in E:
    if i == 0 and j != 1:
        # Edge from coast to non-well-1 is forbidden (infinite cost)
        # We can either skip creating the variable or create it and force it to 0.
        # Skipping is cleaner.
        continue
    x[i, j] = solver.IntVar(0, 1, 'x_%d_%d' % (i, j))

# Objective: Minimize total pipeline length
obj = 0
for i, j in E:
    if i == 0 and j != 1:
        continue
    obj += c[i, j] * x[i, j]
solver.Minimize(obj)

# Constraint 1: Exactly |V| - 1 = 8 edges must be selected to form a spanning tree
# Sum of all x_ij = 8
total_edges = 0
for i, j in E:
    if i == 0 and j != 1:
        continue
    total_edges += x[i, j]
solver.Add(total_edges == 8)

# Constraint 2: Subtour Elimination Constraints (SEC)
# For every non-empty proper subset S of N (well nodes), 
# sum of x_ij for i in S, j not in S (where the edge exists) >= 1
# This ensures connectivity of all wells to the root.
# Since N has 8 elements, there are 2^8 - 2 = 254 proper non-empty subsets.
# We generate all of them.

import itertools

# Generate all non-empty proper subsets of N
for r in range(1, n_wells):  # r from 1 to 7 (proper subsets)
    for subset in itertools.combinations(N, r):
        S = set(subset)
        # The cut set: edges with exactly one endpoint in S
        # The other endpoint can be in V \ S.
        # Note: The root (node 0) is in V \ S.
        # So we sum x_ij for all i in S, j in V \ S where (min(i,j), max(i,j)) is a valid edge.
        
        cut_sum = 0
        has_edge = False
        for i in S:
            for j in V:
                if j in S:
                    continue
                # Check if edge (i, j) exists in our variable dictionary
                a, b = (i, j) if i < j else (j, i)
                if (a, b) in x:
                    cut_sum += x[a, b]
                    has_edge = True
        
        # Only add constraint if there is at least one possible edge crossing the cut
        if has_edge:
            solver.Add(cut_sum >= 1)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")