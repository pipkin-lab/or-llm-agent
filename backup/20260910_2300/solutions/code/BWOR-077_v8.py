from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

W = [1, 2, 3, 4, 5]
S = [1, 2, 3, 4, 5]

# Efficiency matrix c[w][s]
# Workers: 1=A, 2=B, 3=C, 4=D, 5=E
# Stations: 1=I, 2=II, 3=III, 4=IV, 5=V
c = dict()
eff_matrix = {
    1: [2, 3, 4, 1, 7],  # A
    2: [3, 4, 2, 5, 6],  # B
    3: [2, 5, 3, 4, 1],  # C
    4: [5, 2, 3, 2, 5],  # D
    5: [3, 7, 6, 2, 4]   # E
}
for w in W:
    for s in S:
        c[w, s] = eff_matrix[w][s - 1]

# Decision variables
x = dict()
for w in W:
    for s in S:
        x[w, s] = solver.BoolVar('x_' + str(w) + '_' + str(s))

# Auxiliary variable Z (bottleneck)
Z = solver.NumVar(0, solver.infinity(), 'Z')

# Objective: Maximize Z
solver.Maximize(Z)

# Constraints: Each worker assigned to exactly one station
for w in W:
    solver.Add(sum(x[w, s] for s in S) == 1)

# Constraints: Each station assigned exactly one worker
for s in S:
    solver.Add(sum(x[w, s] for w in W) == 1)

# Bottleneck constraints: efficiency of station s >= Z
for s in S:
    solver.Add(sum(c[w, s] * x[w, s] for w in W) >= Z)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")