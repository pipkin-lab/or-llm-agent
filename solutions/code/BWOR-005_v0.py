from ortools.linear_solver import pywraplp

# Define the solver for LP
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Index sets
I = ['A', 'B', 'C']  # Cargo types
J = ['F', 'M', 'R']  # Compartments: Front, Middle, Rear

# Parameters
CapW = dict()
CapW['F'] = 2000
CapW['M'] = 3000
CapW['R'] = 1500

CapV = dict()
CapV['F'] = 4000
CapV['M'] = 5000
CapV['R'] = 1500

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

# Decision variables: x[i, j] for i in I, j in J
x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, INF, 'x_' + i + '_' + j)

# Objective function: Maximize total revenue
obj_terms = []
for i in I:
    for j in J:
        obj_terms.append(p[i] * x[i, j])
solver.Maximize(sum(obj_terms))

# Volume constraints
for j in J:
    solver.Add(sum(v[i] * x[i, j] for i in I) <= CapV[j])

# Weight constraints
for j in J:
    solver.Add(sum(w[i] * x[i, j] for i in I) <= CapW[j])

# Supply constraints
for i in I:
    solver.Add(sum(x[i, j] for j in J) <= Q[i])

# Balance constraints (linearized)
# W_F = sum(w[i] * x[i, 'F'] for i in I)
# W_M = sum(w[i] * x[i, 'M'] for i in I)
# W_R = sum(w[i] * x[i, 'R'] for i in I)

# 1. Front >= 17/60 * Middle  =>  60*W_F - 17*W_M >= 0
solver.Add(
    60 * sum(w[i] * x[i, 'F'] for i in I) - 17 * sum(w[i] * x[i, 'M'] for i in I) >= 0
)

# 2. Front <= 23/60 * Middle  =>  60*W_F - 23*W_M <= 0
solver.Add(
    60 * sum(w[i] * x[i, 'F'] for i in I) - 23 * sum(w[i] * x[i, 'M'] for i in I) <= 0
)

# 3. Rear >= 17/40 * Middle  =>  40*W_R - 17*W_M >= 0
solver.Add(
    40 * sum(w[i] * x[i, 'R'] for i in I) - 17 * sum(w[i] * x[i, 'M'] for i in I) >= 0
)

# 4. Rear <= 23/40 * Middle  =>  40*W_R - 23*W_M <= 0
solver.Add(
    40 * sum(w[i] * x[i, 'R'] for i in I) - 23 * sum(w[i] * x[i, 'M'] for i in I) <= 0
)

# 5. Front >= 6/5 * Rear  =>  5*W_F - 6*W_R >= 0
solver.Add(
    5 * sum(w[i] * x[i, 'F'] for i in I) - 6 * sum(w[i] * x[i, 'R'] for i in I) >= 0
)

# 6. Front <= 22/15 * Rear  =>  15*W_F - 22*W_R <= 0
solver.Add(
    15 * sum(w[i] * x[i, 'F'] for i in I) - 22 * sum(w[i] * x[i, 'R'] for i in I) <= 0
)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")