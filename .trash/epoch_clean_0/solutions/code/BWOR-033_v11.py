from ortools.linear_solver import pywraplp

# Define solver (Continuous variables -> GLOP)
solver = pywraplp.Solver.CreateSolver('GLOP')

# Index Sets
products = ['I', 'II', 'III']
quarters = [1, 2, 3, 4]
P_All = products
P_Q2 = ['II', 'III']

# Parameters
D = {
    ('I', 1): 1500, ('I', 2): 1000, ('I', 3): 2000, ('I', 4): 1200,
    ('II', 1): 1500, ('II', 2): 1500, ('II', 3): 1200, ('II', 4): 1500,
    ('III', 1): 1000, ('III', 2): 2000, ('III', 3): 1500, ('III', 4): 2500
}

H = {'I': 5, 'II': 5, 'III': 5}
L = {'I': 20, 'II': 20, 'III': 10}
R = {'I': 2, 'II': 4, 'III': 3}
C = {1: 15000, 2: 15000, 3: 15000, 4: 15000}

Inv_init = {'I': 0, 'II': 0, 'III': 0}
Back_init = {'I': 0, 'II': 0, 'III': 0}
Inv_end_req = 150

# Decision Variables
x = dict()
Inv = dict()
Back = dict()

for p in products:
    for t in quarters:
        x[p, t] = solver.NumVar(0, solver.infinity(), 'x_' + p + '_' + str(t))
        Inv[p, t] = solver.NumVar(0, solver.infinity(), 'Inv_' + p + '_' + str(t))
        Back[p, t] = solver.NumVar(0, solver.infinity(), 'Back_' + p + '_' + str(t))

# Constraint: x_{I,2} = 0
solver.Add(x['I', 2] == 0)

# Objective Function
obj_expr = 0
for p in products:
    for t in quarters:
        obj_expr += H[p] * Inv[p, t] + L[p] * Back[p, t]

solver.Minimize(obj_expr)

# A. Inventory Balance Constraints
for p in products:
    # t = 1
    solver.Add(
        Inv[p, 1] - Back[p, 1] == 
        Inv_init[p] - Back_init[p] + x[p, 1] - D[p, 1]
    )
    for t in [2, 3, 4]:
        solver.Add(
            Inv[p, t] - Back[p, t] == 
            Inv[p, t-1] - Back[p, t-1] + x[p, t] - D[p, t]
        )

# B. Labor Capacity Constraints
# Q1
solver.Add(2 * x['I', 1] + 4 * x['II', 1] + 3 * x['III', 1] <= C[1])
# Q2 (Product I excluded)
solver.Add(4 * x['II', 2] + 3 * x['III', 2] <= C[2])
# Q3
solver.Add(2 * x['I', 3] + 4 * x['II', 3] + 3 * x['III', 3] <= C[3])
# Q4
solver.Add(2 * x['I', 4] + 4 * x['II', 4] + 3 * x['III', 4] <= C[4])

# C. Ending Inventory Requirements
for p in products:
    solver.Add(Inv[p, 4] == 150)
    solver.Add(Back[p, 4] == 0)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")