from ortools.linear_solver import pywraplp

# Define the solver (MILP since ships are integer units)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
# Routes: 1 (E->D), 2 (B->C), 3 (A->F), 4 (D->B)
frequencies = {
    1: 3,
    2: 2,
    3: 1,
    4: 1
}

# Sailing times T[i, j]
# Based on the problem description:
# Route 1 (E->D): T_ED = 17, T_DE = 17
# Route 2 (B->C): T_BC = 3, T_CB = 3
# Route 3 (A->F): T_AF = 7, T_FA = 7
# Route 4 (D->B): T_DB = 13, T_BD = 13

# Cycle times C_r = 2 + T[O_r, D_r] + T[D_r, O_r]
cycle_times = {
    1: 2 + 17 + 17,  # 36
    2: 2 + 3 + 3,    # 8
    3: 2 + 7 + 7,    # 16
    4: 2 + 13 + 13   # 28
}

routes = [1, 2, 3, 4]

# Decision Variables
# x[r] = number of ships assigned to route r
x = dict()
for r in routes:
    x[r] = solver.IntVar(0, solver.infinity(), 'x_' + str(r))

# Objective Function: Minimize total ships
obj = sum(x[r] for r in routes)
solver.Minimize(obj)

# Constraints
# x[r] >= f[r] * C[r]
for r in routes:
    required_ships = frequencies[r] * cycle_times[r]
    solver.Add(x[r] >= required_ships)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")