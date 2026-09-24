from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
K = [1, 2, 3, 4]
I0 = 500
C_buy = {1: 10, 2: 9, 3: 11, 4: 15}
C_sell = {1: 12, 2: 9, 3: 13, 4: 17}
Cap = 1000

# Variables
B = dict()
S = dict()
I = dict()

for k in K:
    B[k] = solver.IntVar(0, solver.infinity(), 'B_' + str(k))
    S[k] = solver.IntVar(0, solver.infinity(), 'S_' + str(k))
    I[k] = solver.IntVar(0, solver.infinity(), 'I_' + str(k))

# Constraints
# Inventory balance
# Month 1: I_1 = I0 - S_1 (B0 = 0)
solver.Add(I[1] == I0 - S[1])

# Month 2: I_2 = I_1 + B_1 - S_2
solver.Add(I[2] == I[1] + B[1] - S[2])

# Month 3: I_3 = I_2 + B_2 - S_3
solver.Add(I[3] == I[2] + B[2] - S[3])

# Month 4: I_4 = I_3 + B_3 - S_4
solver.Add(I[4] == I[3] + B[3] - S[4])

# Warehouse capacity
for k in K:
    solver.Add(I[k] <= Cap)

# Objective: Maximize total profit
obj = 0
for k in K:
    obj += C_sell[k] * S[k] - C_buy[k] * B[k]

solver.Maximize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")