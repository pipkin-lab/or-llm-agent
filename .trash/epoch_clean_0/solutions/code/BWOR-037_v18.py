from ortools.linear_solver import pywraplp

# Initialize MILP solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables: number of crews for each task and option
x_1A = solver.IntVar(0, INF, 'x_1A')
x_1B = solver.IntVar(0, INF, 'x_1B')
x_2A = solver.IntVar(0, INF, 'x_2A')
x_2B = solver.IntVar(0, INF, 'x_2B')
x_3A = solver.IntVar(0, INF, 'x_3A')
x_3B = solver.IntVar(0, INF, 'x_3B')

# Objective function: Minimize total weekly wage cost
obj = 100 * x_1A + 260 * x_1B + 100 * x_2A + 80 * x_2B + 400 * x_3A + 340 * x_3B
solver.Minimize(obj)

# Task completion constraints (workload requirements)
# Task 1: 42 * x_1A + 114 * x_1B >= 10000
solver.Add(42 * x_1A + 114 * x_1B >= 10000)
# Task 2: 42 * x_2A + 36 * x_2B >= 20000
solver.Add(42 * x_2A + 36 * x_2B >= 20000)
# Task 3: 180 * x_3A + 150 * x_3B >= 30000
solver.Add(180 * x_3A + 150 * x_3B >= 30000)

# Workforce availability constraints
# Technicians: x_1A + x_1B + x_2A + x_3B <= 400
solver.Add(x_1A + x_1B + x_2A + x_3B <= 400)
# Laborers: 2*x_1B + x_2B + 5*x_3A + 3*x_3B <= 800
solver.Add(2 * x_1B + x_2B + 5 * x_3A + 3 * x_3B <= 800)

# Solve the model
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")