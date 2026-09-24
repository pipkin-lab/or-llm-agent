from ortools.linear_solver import pywraplp

# Create the solver
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Define index sets
grades = [1, 2, 3]
brands = ['R', 'Y', 'Bl']

# Parameters
supply = dict()
supply[1] = 1500
supply[2] = 2000
supply[3] = 1000

cost = dict()
cost[1] = 6.0
cost[2] = 4.5
cost[3] = 3.0

price = dict()
price['R'] = 5.5
price['Y'] = 5.0
price['Bl'] = 4.8

min_production_R = 2000

# Decision variables
x = dict()
for g in grades:
    for b in brands:
        x[g, b] = solver.NumVar(0, INF, 'x_{}_{}'.format(g, b))

X = dict()
for b in brands:
    X[b] = solver.NumVar(0, INF, 'X_{}'.format(b))

# Objective: Maximize profit = sum over b,g of (P_b - C_g) * x[g,b]
obj_terms = []
for b in brands:
    for g in grades:
        obj_terms.append((price[b] - cost[g]) * x[g, b])
solver.Maximize(sum(obj_terms))

# A. Production Balance constraints
for b in brands:
    solver.Add(X[b] == sum(x[g, b] for g in grades))

# B. Supply constraints
for g in grades:
    solver.Add(sum(x[g, b] for b in brands) <= supply[g])

# C. Blending constraints

# Red Brand:
# x_{1,R} >= x_{2,R} + x_{3,R}  =>  x_{1,R} - x_{2,R} - x_{3,R} >= 0
solver.Add(x[1, 'R'] - x[2, 'R'] - x[3, 'R'] >= 0)
# 9*x_{3,R} <= x_{1,R} + x_{2,R}  =>  -x_{1,R} - x_{2,R} + 9*x_{3,R} <= 0
solver.Add(-x[1, 'R'] - x[2, 'R'] + 9 * x[3, 'R'] <= 0)

# Yellow Brand:
# 4*x_{1,Y} >= x_{2,Y} + x_{3,Y}  =>  4*x_{1,Y} - x_{2,Y} - x_{3,Y} >= 0
solver.Add(4 * x[1, 'Y'] - x[2, 'Y'] - x[3, 'Y'] >= 0)
# 3*x_{3,Y} <= 7*(x_{1,Y} + x_{2,Y})  =>  -7*x_{1,Y} - 7*x_{2,Y} + 3*x_{3,Y} <= 0
solver.Add(-7 * x[1, 'Y'] - 7 * x[2, 'Y'] + 3 * x[3, 'Y'] <= 0)

# Blue Brand:
# 9*x_{1,Bl} >= x_{2,Bl} + x_{3,Bl}  =>  9*x_{1,Bl} - x_{2,Bl} - x_{3,Bl} >= 0
solver.Add(9 * x[1, 'Bl'] - x[2, 'Bl'] - x[3, 'Bl'] >= 0)
# x_{3,Bl} <= x_{1,Bl} + x_{2,Bl}  =>  -x_{1,Bl} - x_{2,Bl} + x_{3,Bl} <= 0
solver.Add(-x[1, 'Bl'] - x[2, 'Bl'] + x[3, 'Bl'] <= 0)

# D. Minimum production requirement for Red
solver.Add(X['R'] >= min_production_R)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")