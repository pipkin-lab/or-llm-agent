from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables: x_j for j in 1..6 (non-negative integers)
x = dict()
for j in range(1, 7):
    x[j] = solver.IntVar(0, INF, 'x_' + str(j))

# Demand parameters
D = dict()
D[1] = 10
D[2] = 15
D[3] = 25
D[4] = 20
D[5] = 18
D[6] = 12

# a[i][j] = 1 if shift j covers period i
# Shift 1: periods 1,2
# Shift 2: periods 2,3
# Shift 3: periods 3,4
# Shift 4: periods 4,5
# Shift 5: periods 5,6
# Shift 6: periods 6,1
a = dict()
for i in range(1, 7):
    for j in range(1, 7):
        a[i, j] = 0

# Shift 1 covers periods 1 and 2
a[1, 1] = 1
a[2, 1] = 1
# Shift 2 covers periods 2 and 3
a[2, 2] = 1
a[3, 2] = 1
# Shift 3 covers periods 3 and 4
a[3, 3] = 1
a[4, 3] = 1
# Shift 4 covers periods 4 and 5
a[4, 4] = 1
a[5, 4] = 1
# Shift 5 covers periods 5 and 6
a[5, 5] = 1
a[6, 5] = 1
# Shift 6 covers periods 6 and 1
a[6, 6] = 1
a[1, 6] = 1

# Staffing constraints: sum_j a[i,j] * x[j] >= D[i] for each period i
for i in range(1, 7):
    expr = 0
    for j in range(1, 7):
        if a[i, j] == 1:
            expr += x[j]
    solver.Add(expr >= D[i])

# Objective: minimize total nurses
obj = 0
for j in range(1, 7):
    obj += x[j]

solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")