from ortools.linear_solver import pywraplp

# Initialize solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Parameters
Cap = [400, 450]  # Cap[0] for station 1, Cap[1] for station 2
D_min = [290, 250, 270]
D_max = [320, 250, 350]
C = [[15, 18, 22],
     [21, 25, 16]]

# Decision Variables
# x[s][c] where s=0,1 and c=0,1,2
x = dict()
for s in range(2):
    for c in range(3):
        x[s, c] = solver.NumVar(0, solver.infinity(), 'x_' + str(s) + '_' + str(c))

# Objective Function
obj = 0
for s in range(2):
    for c in range(3):
        obj += C[s][c] * x[s, c]

solver.Minimize(obj)

# Supply Capacity Constraints
for s in range(2):
    solver.Add(sum(x[s, c] for c in range(3)) == Cap[s])

# City Demand Constraints
for c in range(3):
    solver.Add(sum(x[s, c] for s in range(2)) >= D_min[c])
    solver.Add(sum(x[s, c] for s in range(2)) <= D_max[c])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")