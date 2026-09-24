from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables
x_S = solver.NumVar(0, INF, 'x_S')
x_C = solver.NumVar(0, INF, 'x_C')
x_W = solver.NumVar(0, INF, 'x_W')
x_cow = solver.NumVar(0, INF, 'x_cow')
x_chick = solver.NumVar(0, INF, 'x_chick')
u_A = solver.NumVar(0, INF, 'u_A')
u_S = solver.NumVar(0, INF, 'u_S')

# Objective: Maximize total annual net income
obj = 175 * x_S + 300 * x_C + 120 * x_W + 400 * x_cow + 2 * x_chick + 1.8 * u_A + 2.1 * u_S
solver.Maximize(obj)

# Constraint 1: Land
solver.Add(x_S + x_C + x_W + 1.5 * x_cow <= 100)

# Constraint 2: Funds
solver.Add(400 * x_cow + 3 * x_chick <= 15000)

# Constraint 3: Autumn/Winter Labor (equality)
solver.Add(20 * x_S + 35 * x_C + 10 * x_W + 100 * x_cow + 0.6 * x_chick + u_A == 3500)

# Constraint 4: Spring/Summer Labor (equality)
solver.Add(50 * x_S + 75 * x_C + 40 * x_W + 50 * x_cow + 0.3 * x_chick + u_S == 4000)

# Constraint 5: Capacity
solver.Add(x_chick <= 3000)
solver.Add(x_cow <= 32)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")