from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

x_A = solver.IntVar(0, 4, 'x_A')
x_B = solver.IntVar(0, 4, 'x_B')
x_C = solver.IntVar(0, 4, 'x_C')

solver.Add(x_A + x_B + x_C <= 4)

f_A = [0, 41, 48, 60, 66]
f_B = [0, 42, 50, 60, 66]
f_C = [0, 64, 68, 78, 76]

y_A = dict()
y_B = dict()
y_C = dict()

for k in range(5):
    y_A[k] = solver.BoolVar('y_A_' + str(k))
    y_B[k] = solver.BoolVar('y_B_' + str(k))
    y_C[k] = solver.BoolVar('y_C_' + str(k))

solver.Add(sum(y_A[k] for k in range(5)) == 1)
solver.Add(sum(y_B[k] for k in range(5)) == 1)
solver.Add(sum(y_C[k] for k in range(5)) == 1)

for k in range(5):
    solver.Add(x_A == k * y_A[k])
    solver.Add(x_B == k * y_B[k])
    solver.Add(x_C == k * y_C[k])

objective = (
    sum(f_A[k] * y_A[k] for k in range(5))
    + sum(f_B[k] * y_B[k] for k in range(5))
    + sum(f_C[k] * y_C[k] for k in range(5))
)

solver.Maximize(objective)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")