from ortools.linear_solver import pywraplp

# Create the solver
solver = pywraplp.Solver.CreateSolver('SCIP')
if solver is None:
    print("Could not create solver")
    exit(1)

# Define parameters
T = [1, 2, 3]
P = ['N', 'O']

# Demand
D = {1: 3, 2: 3, 3: 3}
I0 = 2
I_end = 1

# Capacities
Cap_N = {1: 2, 2: 4, 3: 1}
Cap_O = {1: 3, 2: 2, 3: 3}

# Costs
C_N = {1: 500, 2: 600, 3: 550}
C_O = {1: 570, 2: 670, 3: 620}
h = 40

# Decision variables
x = {}
for t in T:
    for p in P:
        x[t, p] = solver.IntVar(0, solver.infinity(), f'x_{t}_{p}')

I = {}
for t in T:
    I[t] = solver.IntVar(0, solver.infinity(), f'I_{t}')

# Objective function
obj_terms = []
for t in T:
    for p in P:
        if p == 'N':
            obj_terms.append(C_N[t] * x[t, p])
        else:
            obj_terms.append(C_O[t] * x[t, p])
    obj_terms.append(h * I[t])

solver.Minimize(sum(obj_terms))

# Constraints

# A. Inventory Balance Constraints
# I_t = I_{t-1} + sum(x_{t,p}) - D_t
solver.Add(I[1] == I0 + x[1, 'N'] + x[1, 'O'] - D[1])
solver.Add(I[2] == I[1] + x[2, 'N'] + x[2, 'O'] - D[2])
solver.Add(I[3] == I[2] + x[3, 'N'] + x[3, 'O'] - D[3])

# B. Ending Inventory Requirement
solver.Add(I[3] == I_end)

# C. Production Capacity Constraints
for t in T:
    solver.Add(x[t, 'N'] <= Cap_N[t])
    solver.Add(x[t, 'O'] <= Cap_O[t])

# Solve the model
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")