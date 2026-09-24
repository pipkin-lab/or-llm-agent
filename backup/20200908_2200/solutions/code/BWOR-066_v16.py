from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
P_buy = [10, 9, 11, 15]
P_sell = [12, 9, 13, 17]
I_0 = 500
Cap = 1000
n_months = 4

# Decision Variables
x = dict()  # x[k]: purchases in month k
s = dict()  # s[k]: sales in month k
I = dict()  # I[k]: inventory at end of month k

for k in range(1, n_months + 1):
    x[k] = solver.IntVar(0, solver.infinity(), 'x_' + str(k))
    s[k] = solver.IntVar(0, solver.infinity(), 's_' + str(k))
    I[k] = solver.IntVar(0, solver.infinity(), 'I_' + str(k))

# Objective: Maximize total profit
objective_terms = []
for k in range(1, n_months + 1):
    objective_terms.append(P_sell[k - 1] * s[k])
    objective_terms.append(-P_buy[k - 1] * x[k])

solver.Maximize(sum(objective_terms))

# Inventory Balance Constraints
# I_1 = I_0 - s_1
solver.Add(I[1] == I_0 - s[1])

for k in range(2, n_months + 1):
    # I_k = I_{k-1} + x_{k-1} - s_k
    solver.Add(I[k] == I[k - 1] + x[k - 1] - s[k])

# Capacity Constraints
# Start of M1: I_0 <= Cap (Always true since 500 <= 1000, but add for completeness if needed, though I_0 is fixed)
# Start of M2: I_1 + x_1 <= Cap
solver.Add(I[1] + x[1] <= Cap)
# Start of M3: I_2 + x_2 <= Cap
solver.Add(I[2] + x[2] <= Cap)
# Start of M4: I_3 + x_3 <= Cap
solver.Add(I[3] + x[3] <= Cap)
# End of M4 / Start of M5: I_4 + x_4 <= Cap
# Note: The model states x_4 is bought in M4 and available in M5.
# The capacity constraint for the state including x_4 is I_4 + x_4 <= Cap.
solver.Add(I[4] + x[4] <= Cap)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")