from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables
x_s = solver.NumVar(0, INF, 'x_s')
x_c = solver.NumVar(0, INF, 'x_c')
x_w = solver.NumVar(0, INF, 'x_w')
x_cow = solver.NumVar(0, INF, 'x_cow')
x_chick = solver.NumVar(0, INF, 'x_chick')
s_SS = solver.NumVar(0, INF, 's_SS')
s_AW = solver.NumVar(0, INF, 's_AW')

# Objective function
solver.Maximize(175 * x_s + 300 * x_c + 120 * x_w + 400 * x_cow + 2 * x_chick + 2.1 * s_SS + 1.8 * s_AW)

# Constraint 1: Land
solver.Add(x_s + x_c + x_w + 1.5 * x_cow <= 100)

# Constraint 2: Autumn/Winter Labor
solver.Add(20 * x_s + 35 * x_c + 10 * x_w + 100 * x_cow + 0.6 * x_chick + s_AW <= 3500)

# Constraint 3: Spring/Summer Labor
solver.Add(50 * x_s + 75 * x_c + 40 * x_w + 50 * x_cow + 0.3 * x_chick + s_SS <= 4000)

# Constraint 4: Capital
solver.Add(400 * x_cow + 3 * x_chick <= 15000)

# Constraint 5: Cow capacity
solver.Add(x_cow <= 32)

# Constraint 6: Chicken capacity
solver.Add(x_chick <= 3000)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")