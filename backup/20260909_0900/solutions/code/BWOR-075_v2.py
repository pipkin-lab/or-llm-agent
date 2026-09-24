from ortools.linear_solver import pywraplp
import itertools

# Define nodes
V = list(range(9))  # 0: Coast, 1-8: Wells
N = len(V)

# Define edges and costs
# Costs are provided for well-to-well and coast-to-well1
# All other coast-to-well connections are infeasible (infinite cost)
# We only include feasible edges in the model

# Cost matrix (symmetric), initialize with large M for infeasible
M = 1000000
c = dict()
for i in range(N):
    for j in range(i + 1, N):
        c[(i, j)] = M  # default infeasible

# Set feasible costs
c[(0, 1)] = 5.0
well_costs = {
    (1, 2): 1.3, (1, 3): 2.1, (1, 4): 0.9, (1, 5): 0.7, (1, 6): 1.8, (1, 7): 2.0, (1, 8): 1.5,
    (2, 3): 0.9, (2, 4): 1.8, (2, 5): 1.2, (2, 6): 2.6, (2, 7): 2.3, (2, 8): 1.1,
    (3, 4): 2.6, (3, 5): 1.7, (3, 6): 2.5, (3, 7): 1.9, (3, 8): 1.0,
    (4, 5): 0.7, (4, 6): 1.6, (4, 7): 1.5, (4, 8): 0.9,
    (5, 6): 0.9, (5, 7): 1.1, (5, 8): 0.8,
    (6, 7): 0.6, (6, 8): 1.0,
    (7, 8): 0.5
}
for (i, j), val in well_costs.items():
    c[(i, j)] = val
    c[(j, i)] = val  # for reference, though we only use i<j

# List of feasible edges (only those with finite cost)
E = []
for i in range(N):
    for j in range(i + 1, N):
        if c[(i, j)] < M:
            E.append((i, j))

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')
if solver is None:
    raise Exception("SCIP solver not available")

# Decision variables: x[(i,j)] for each feasible edge
x = dict()
for (i, j) in E:
    x[(i, j)] = solver.BoolVar('x_' + str(i) + '_' + str(j))

# Objective: Minimize total pipeline length
obj_terms = []
for (i, j) in E:
    obj_terms.append(c[(i, j)] * x[(i, j)])
solver.Minimize(solver.Sum(obj_terms))

# Constraint 1: Exactly N-1 edges selected
edge_count = solver.Sum(x[(i, j)] for (i, j) in E)
solver.Add(edge_count == N - 1)

# Constraint 2: Cutset inequalities for connectivity
# For every non-empty proper subset S of V, sum of x over edges crossing the cut >= 1
# To avoid generating 2^9 - 2 = 510 subsets (which is manageable), we generate all proper non-empty subsets
# However, we can optimize by only considering subsets that contain node 0 (Coast) or not,
# but the standard cutset requires all subsets. For N=9, 510 constraints is fine.

# Generate all non-empty proper subsets
for r in range(1, N):
    for S in itertools.combinations(V, r):
        S_set = set(S)
        if len(S_set) == N:
            continue
        # Build the cut: edges with one endpoint in S and one outside
        cut_edges = []
        for (i, j) in E:
            if (i in S_set) != (j in S_set):
                cut_edges.append(x[(i, j)])
        if cut_edges:
            solver.Add(solver.Sum(cut_edges) >= 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")