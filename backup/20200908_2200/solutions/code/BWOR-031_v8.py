from ortools.linear_solver import pywraplp

# Create the solver (MILP due to integer animal variables)
solver = pywraplp.Solver.CreateSolver('SCIP')
inf = solver.infinity()

# Decision Variables
# x1: Area of Soybeans (hm2)
x1 = solver.NumVar(0, inf, 'x1')
# x2: Area of Corn (hm2)
x2 = solver.NumVar(0, inf, 'x2')
# x3: Area of Wheat (hm2)
x3 = solver.NumVar(0, inf, 'x3')
# y1: Number of Dairy Cows
y1 = solver.IntVar(0, 32, 'y1')
# y2: Number of Chickens
y2 = solver.IntVar(0, 3000, 'y2')
# u1: Unused labor in Autumn/Winter (person-days)
u1 = solver.NumVar(0, inf, 'u1')
# u2: Unused labor in Spring/Summer (person-days)
u2 = solver.NumVar(0, inf, 'u2')

# Objective Function
# Maximize Z = 175x1 + 300x2 + 120x3 + 400y1 + 2y2 + 1.8u1 + 2.1u2
objective = 175 * x1 + 300 * x2 + 120 * x3 + 400 * y1 + 2 * y2 + 1.8 * u1 + 2.1 * u2
solver.Maximize(objective)

# Constraints

# 1. Land Constraint: x1 + x2 + x3 + 1.5y1 <= 100
land_constraint = x1 + x2 + x3 + 1.5 * y1 <= 100
solver.Add(land_constraint)

# 2. Fund Constraint: 400y1 + 3y2 <= 15000
fund_constraint = 400 * y1 + 3 * y2 <= 15000
solver.Add(fund_constraint)

# 3. Labor Constraint (Autumn/Winter): 20x1 + 35x2 + 10x3 + 100y1 + 0.6y2 + u1 = 3500
labor_aw_constraint = 20 * x1 + 35 * x2 + 10 * x3 + 100 * y1 + 0.6 * y2 + u1 == 3500
solver.Add(labor_aw_constraint)

# 4. Labor Constraint (Spring/Summer): 50x1 + 75x2 + 40x3 + 50y1 + 0.3y2 + u2 = 4000
labor_ss_constraint = 50 * x1 + 75 * x2 + 40 * x3 + 50 * y1 + 0.3 * y2 + u2 == 4000
solver.Add(labor_ss_constraint)

# Solve the model
status = solver.Solve()

# Check the status of the solution
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")