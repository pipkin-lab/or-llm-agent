from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
x_soy = solver.NumVar(0, INF, 'x_soy')
x_corn = solver.NumVar(0, INF, 'x_corn')
x_wheat = solver.NumVar(0, INF, 'x_wheat')

y_cow = solver.IntVar(0, 32, 'y_cow')
y_chicken = solver.IntVar(0, 3000, 'y_chicken')

u_aw = solver.NumVar(0, INF, 'u_aw')
u_ss = solver.NumVar(0, INF, 'u_ss')

# Objective: maximize total annual net income
obj = (175 * x_soy + 300 * x_corn + 120 * x_wheat
       + 400 * y_cow + 2 * y_chicken
       + 1.8 * u_aw + 2.1 * u_ss)
solver.Maximize(obj)

# Constraint 1: Land
solver.Add(x_soy + x_corn + x_wheat + 1.5 * y_cow <= 100)

# Constraint 2: Capital
solver.Add(400 * y_cow + 3 * y_chicken <= 15000)

# Constraint 3: Autumn/Winter labor
solver.Add(20 * x_soy + 35 * x_corn + 10 * x_wheat
           + 100 * y_cow + 0.6 * y_chicken + u_aw <= 3500)

# Constraint 4: Spring/Summer labor
solver.Add(50 * x_soy + 75 * x_corn + 40 * x_wheat
           + 50 * y_cow + 0.3 * y_chicken + u_ss <= 4000)

# Constraint 5: Animal capacity (already enforced by variable bounds, but explicit)
solver.Add(y_cow <= 32)
solver.Add(y_chicken <= 3000)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")