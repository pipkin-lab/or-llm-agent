from ortools.linear_solver import pywraplp

# Initialize LP solver
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables: daily consumption (units of 500g)
x1 = solver.NumVar(0, INF, 'x1')
x2 = solver.NumVar(0, INF, 'x2')
x3 = solver.NumVar(0, INF, 'x3')

# Deviation variables
d1_minus = solver.NumVar(0, INF, 'd1_minus')
d1_plus = solver.NumVar(0, INF, 'd1_plus')
d2_minus = solver.NumVar(0, INF, 'd2_minus')
d2_plus = solver.NumVar(0, INF, 'd2_plus')
d3_minus = solver.NumVar(0, INF, 'd3_minus')
d3_plus = solver.NumVar(0, INF, 'd3_plus')
d4_minus = solver.NumVar(0, INF, 'd4_minus')
d4_plus = solver.NumVar(0, INF, 'd4_plus')
d5_minus = solver.NumVar(0, INF, 'd5_minus')
d5_plus = solver.NumVar(0, INF, 'd5_plus')

# Goal Equations (System Constraints)
# 1. Vitamin A: Target = 1
solver.Add(1 * x1 + 1 * x2 + 10 * x3 + d1_minus - d1_plus == 1)

# 2. Vitamin C: Target = 30
solver.Add(100 * x1 + 10 * x2 + 10 * x3 + d2_minus - d2_plus == 30)

# 3. Vitamin D: Target = 10
solver.Add(10 * x1 + 100 * x2 + 10 * x3 + d3_minus - d3_plus == 10)

# 4. Cholesterol: Target = 0 (Minimize intake)
solver.Add(70 * x1 + 50 * x2 + 120 * x3 + d4_minus - d4_plus == 0)

# 5. Cost: Target = 0 (Minimize cost)
solver.Add(1.5 * x1 + 8 * x2 + 4 * x3 + d5_minus - d5_plus == 0)

# Lexicographic Goal Programming

# Priority 1: Minimize unmet vitamin requirements (d1_minus + d2_minus + d3_minus)
obj_p1 = d1_minus + d2_minus + d3_minus
solver.Minimize(obj_p1)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    # Fix P1 objective
    p1_value = solver.Objective().Value()
    solver.Add(obj_p1 == p1_value)
else:
    print("NO_FEASIBLE_SOLUTION")
    exit(0)

# Priority 2: Minimize excess cholesterol (d4_plus)
obj_p2 = d4_plus
solver.Minimize(obj_p2)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    # Fix P2 objective
    p2_value = solver.Objective().Value()
    solver.Add(obj_p2 == p2_value)
else:
    print("NO_FEASIBLE_SOLUTION")
    exit(0)

# Priority 3: Minimize excess cost (d5_plus)
obj_p3 = d5_plus
solver.Minimize(obj_p3)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    # The final objective value is the cost (d5_plus)
    final_value = solver.Objective().Value()
    print("OPTIMAL_VALUE:", final_value)
else:
    print("NO_FEASIBLE_SOLUTION")