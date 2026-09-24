from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

# Index sets
G = ['I', 'II', 'III']
B = ['R', 'Y', 'Bl']

# Decision variables
x = dict()
for g in G:
    for b in B:
        x[g, b] = solver.NumVar(0, solver.infinity(), 'x_' + g + '_' + b)

# Total production per brand
Z = dict()
for b in B:
    Z[b] = sum(x[g, b] for g in G)

# Parameters
S = dict()
S['I'] = 1500
S['II'] = 2000
S['III'] = 1000

C = dict()
C['I'] = 6.0
C['II'] = 4.5
C['III'] = 3.0

P = dict()
P['R'] = 5.5
P['Y'] = 5.0
P['Bl'] = 4.8

# Supply constraints
for g in G:
    solver.Add(sum(x[g, b] for b in B) <= S[g])

# Minimum Red production
solver.Add(Z['R'] >= 2000)

# Blending constraints - Red
# Grade III < 10%: 9*x_III_R <= x_I_R + x_II_R
solver.Add(9 * x['III', 'R'] <= x['I', 'R'] + x['II', 'R'])
# Grade I > 50%: x_I_R >= x_II_R + x_III_R
solver.Add(x['I', 'R'] >= x['II', 'R'] + x['III', 'R'])

# Blending constraints - Yellow
# Grade III < 70%: 3*x_III_Y <= 7*(x_I_Y + x_II_Y)
solver.Add(3 * x['III', 'Y'] <= 7 * (x['I', 'Y'] + x['II', 'Y']))
# Grade I > 20%: 4*x_I_Y >= x_II_Y + x_III_Y
solver.Add(4 * x['I', 'Y'] >= x['II', 'Y'] + x['III', 'Y'])

# Blending constraints - Blue
# Grade III < 50%: x_III_Bl <= x_I_Bl + x_II_Bl
solver.Add(x['III', 'Bl'] <= x['I', 'Bl'] + x['II', 'Bl'])
# Grade I > 10%: 9*x_I_Bl >= x_II_Bl + x_III_Bl
solver.Add(9 * x['I', 'Bl'] >= x['II', 'Bl'] + x['III', 'Bl'])

# Objective: Maximize profit = sum(P_b * Z_b) - sum(C_g * sum_b x_g_b)
obj_terms = []
for b in B:
    obj_terms.append(P[b] * Z[b])
for g in G:
    obj_terms.append(-C[g] * sum(x[g, b] for b in B))

solver.Maximize(sum(obj_terms))

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")