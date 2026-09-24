from ortools.linear_solver import pywraplp
import itertools

# Initialize MILP solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Node indices 1-8 (wells); coast node 0 is fixed
nodes = [1, 2, 3, 4, 5, 6, 7, 8]
n = len(nodes)  # 8

# Cost matrix c[i][j] for i < j (1-indexed)
c = dict()
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

# Decision variables: x[i, j] for 1 <= i < j <= 8
x = dict()
for i in nodes:
    for j in nodes:
        if i < j:
            x[i, j] = solver.BoolVar('x_' + str(i) + '_' + str(j))

# Objective: 5.0 (coast to well 1, fixed) + sum of c[i,j] * x[i,j]
obj_terms = [5.0]
for i in nodes:
    for j in nodes:
        if i < j:
            obj_terms.append(c[i, j] * x[i, j])
obj = sum(obj_terms)
solver.Minimize(obj)

# Constraint (b): Exactly 7 edges among the 8 wells (tree on 8 nodes)
edge_count = sum(x[i, j] for i in nodes for j in nodes if i < j)
solver.Add(edge_count == 7)

# Constraint (a): Subtour elimination for all proper non-empty subsets S of {1,...,8}
# For each subset S with 2 <= |S| <= 7:
#   sum of x[i,j] where i in S, j not in S (and i < j) >= 1
# Note: since x is only defined for i < j, we count edges crossing the cut.
for subset_size in range(2, n):  # 2 to 7
    for S in itertools.combinations(nodes, subset_size):
        S_set = set(S)
        # Count edges with one endpoint in S and the other not in S
        crossing = []
        for i in nodes:
            for j in nodes:
                if i < j:
                    if (i in S_set) and (j not in S_set):
                        crossing.append(x[i, j])
                    elif (j in S_set) and (i not in S_set):
                        crossing.append(x[i, j])
        if crossing:
            solver.Add(sum(crossing) >= 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")