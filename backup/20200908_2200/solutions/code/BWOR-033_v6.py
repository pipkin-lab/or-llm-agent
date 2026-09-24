from ortools.linear_solver import pywraplp

# Define solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets
products = ['I', 'II', 'III']
quarters = [1, 2, 3, 4]

# Parameters
demand = {
    ('I', 1): 1500, ('I', 2): 1000, ('I', 3): 2000, ('I', 4): 1200,
    ('II', 1): 1500, ('II', 2): 1500, ('II', 3): 1200, ('II', 4): 1500,
    ('III', 1): 1000, ('III', 2): 2000, ('III', 3): 1500, ('III', 4): 2500
}

H_t = 15000
h = {'I': 2, 'II': 4, 'III': 3}
C_hold = 5
C_late = {'I': 20, 'II': 20, 'III': 10}
Inv_end = 150

# Decision variables
# x[p][t] : Production of product p in quarter t
# Inv[p][t] : Ending inventory of product p in quarter t
# Back[p][t] : Ending backlog of product p in quarter t

x = {}
Inv = {}
Back = {}

for p in products:
    x[p] = {}
    Inv[p] = {}
    Back[p] = {}
    for t in quarters:
        x[p][t] = solver.IntVar(0, solver.infinity(), 'x_' + p + '_' + str(t))
        Inv[p][t] = solver.IntVar(0, solver.infinity(), 'Inv_' + p + '_' + str(t))
        Back[p][t] = solver.IntVar(0, solver.infinity(), 'Back_' + p + '_' + str(t))

# Production restriction: Product I cannot be produced in Q2
solver.Add(x['I'][2] == 0)

# Objective function
objective = 0
for p in products:
    for t in quarters:
        objective += C_hold * Inv[p][t]
        objective += C_late[p] * Back[p][t]

# Note: Inv and Back at t=4 are fixed, so their costs are included in the sum
# but the variables are constrained to specific values.
# The objective minimizes the sum of holding and backlog costs over all periods.

# Balance constraints
# Inv[p][t] - Back[p][t] = Inv[p][t-1] - Back[p][t-1] + x[p][t] - d[p][t]
# For t=1, Inv[p][0]=0 and Back[p][0]=0

for p in products:
    for t in quarters:
        if t == 1:
            # Inv[p][1] - Back[p][1] = 0 - 0 + x[p][1] - demand[p][1]
            solver.Add(Inv[p][1] - Back[p][1] == x[p][1] - demand[(p, 1)])
        else:
            # Inv[p][t] - Back[p][t] = Inv[p][t-1] - Back[p][t-1] + x[p][t] - demand[p][t]
            solver.Add(Inv[p][t] - Back[p][t] == Inv[p][t-1] - Back[p][t-1] + x[p][t] - demand[(p, t)])

# Capacity constraints
for t in quarters:
    capacity_expr = 0
    for p in products:
        capacity_expr += h[p] * x[p][t]
    solver.Add(capacity_expr <= H_t)

# Final state constraints
for p in products:
    solver.Add(Inv[p][4] == Inv_end)
    solver.Add(Back[p][4] == 0)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")