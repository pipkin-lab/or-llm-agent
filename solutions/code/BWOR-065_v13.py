from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

T = list(range(1, 7))

demand = dict()
demand[1] = 1
demand[2] = 2
demand[3] = 5
demand[4] = 3
demand[5] = 2
demand[6] = 1

cap_prod = 4
cap_storage = 3
cost_var_prod = 10000
cost_fixed_prod = 4000
cost_storage = 1000

x = dict()
for t in T:
    x[t] = solver.NumVar(0, cap_prod, 'x_' + str(t))

I = dict()
for t in range(1, 6):
    I[t] = solver.NumVar(0, cap_storage, 'I_' + str(t))

y = dict()
for t in T:
    y[t] = solver.BoolVar('y_' + str(t))

obj = 0
for t in T:
    obj += cost_var_prod * x[t] + cost_fixed_prod * y[t]
for t in range(1, 6):
    obj += cost_storage * I[t]
solver.Minimize(obj)

solver.Add(x[1] - I[1] == demand[1])
solver.Add(I[1] + x[2] - I[2] == demand[2])
solver.Add(I[2] + x[3] - I[3] == demand[3])
solver.Add(I[3] + x[4] - I[4] == demand[4])
solver.Add(I[4] + x[5] - I[5] == demand[5])
solver.Add(I[5] + x[6] == demand[6])

for t in T:
    solver.Add(x[t] <= cap_prod * y[t])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")