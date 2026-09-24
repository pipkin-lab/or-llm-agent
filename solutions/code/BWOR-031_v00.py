from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables
x1 = solver.NumVar(0, INF, 'x1')  # Hectares of Soybeans
x2 = solver.NumVar(0, INF, 'x2')  # Hectares of Corn
x3 = solver.NumVar(0, INF, 'x3')  # Hectares of Wheat
y1 = solver.NumVar(0, INF, 'y1')  # Number of Dairy Cows
y2 = solver.NumVar(0, INF, 'y2')  # Number of Chickens
z1 = solver.NumVar(0, INF, 'z1')  # Person-days labor exported in Autumn/Winter
z2 = solver.NumVar(0, INF, 'z2')  # Person-days labor exported in Spring/Summer

# Objective function: Maximize total annual net income
solver.Maximize(175 * x1 + 300 * x2 + 120 * x3 + 400 * y1 + 2 * y2 + 1.8 * z1 + 2.1 * z2)

# Constraints

# 1. Land constraint (100 hm²)
solver.Add(x1 + x2 + x3 + 1.5 * y1 <= 100)

# 2. Capital/funds constraint (15,000 yuan)
solver.Add(400 * y1 + 3 * y2 <= 15000)

# 3. Labor constraints
# Autumn/Winter labor (3,500 person-days)
solver.Add(20 * x1 + 35 * x2 + 10 * x3 + 100 * y1 + 0.6 * y2 + z1 <= 3500)

# Spring/Summer labor (4,000 person-days)
solver.Add(50 * x1 + 75 * x2 + 40 * x3 + 50 * y1 + 0.3 * y2 + z2 <= 4000)

# 4. Capacity constraints
# Chicken house capacity (3,000 chickens)
solver.Add(y2 <= 3000)

# Cowshed capacity (32 dairy cows)
solver.Add(y1 <= 32)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")