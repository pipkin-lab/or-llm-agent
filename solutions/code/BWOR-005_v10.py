from ortools.linear_solver import pywraplp

# Define the solver for LP
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Index sets
I = ['A', 'B', 'C']
J = ['F', 'M', 'R']

# Parameters
W_max = dict()
W_max['F'] = 2000
W_max['M'] = 3000
W_max['R'] = 1500

V_max = dict()
V_max['F'] = 4000
V_max['M'] = 5000
V_max['R'] = 1500

Q = dict()
Q['A'] = 600
Q['B'] = 1000
Q['C'] = 800

v = dict()
v['A'] = 10
v['B'] = 5
v['C'] = 7

w = dict()
w['A'] = 8
w['B'] = 6
w['C'] = 4

p = dict()
p['A'] = 1000
p['B'] = 700
p['C'] = 600

# Decision variables: x[i, j]
x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, INF, 'x_' + i + '_' + j)

# Objective: Maximize total revenue
obj_terms = []
for i in I:
    for j in J:
        obj_terms.append(p[i] * x[i, j])
solver.Maximize(sum(obj_terms))

# Constraints 1: Cargo Availability
for i in I:
    solver.Add(sum(x[i, j] for j in J) <= Q[i])

# Constraints 2: Compartment Volume
for j in J:
    solver.Add(sum(v[i] * x[i, j] for i in I) <= V_max[j])

# Constraints 3: Compartment Weight
for j in J:
    solver.Add(sum(w[i] * x[i, j] for i in I) <= W_max[j])

# Helper to get weight expression for a compartment
def weight_expr(j):
    return sum(w[i] * x[i, j] for i in I)

# Constraints 4: Load Balance
# 4a: Front/Middle ratio deviation <= 15%
# W_F / W_M in [17/45, 23/45]
# 45 * W_F - 17 * W_M >= 0
# 45 * W_F - 23 * W_M <= 0
WF = weight_expr('F')
WM = weight_expr('M')
WR = weight_expr('R')

solver.Add(45 * WF - 17 * WM >= 0)
solver.Add(45 * WF - 23 * WM <= 0)

# 4b: Rear/Middle ratio deviation <= 15%
# W_R / W_M in [17/40, 23/40]
# 40 * W_R - 17 * W_M >= 0
# 40 * W_R - 23 * W_M <= 0
solver.Add(40 * WR - 17 * WM >= 0)
solver.Add(40 * WR - 23 * WM <= 0)

# 4c: Front/Rear ratio deviation <= 10%
# W_F / W_R in [6/5, 22/15]
# 5 * W_F - 6 * W_R >= 0
# 15 * W_F - 22 * W_R <= 0
solver.Add(5 * WF - 6 * WR >= 0)
solver.Add(15 * WF - 22 * WR <= 0)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")