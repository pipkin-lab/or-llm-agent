from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
inf = solver.infinity()

# Index sets
C = ['A', 'B', 'C']
K = ['F', 'M', 'R']

# Parameters
W_max = {'F': 2000, 'M': 3000, 'R': 1500}
V_max = {'F': 4000, 'M': 5000, 'R': 1500}
Q = {'A': 600, 'B': 1000, 'C': 800}
v = {'A': 10, 'B': 5, 'C': 7}
w = {'A': 8, 'B': 6, 'C': 4}
p = {'A': 1000, 'B': 700, 'C': 600}

# Decision variables
x = dict()
for i in C:
    for k in K:
        x[i, k] = solver.NumVar(0, inf, 'x_' + i + '_' + k)

# Objective: Maximize total revenue
obj_terms = []
for i in C:
    for k in K:
        obj_terms.append(p[i] * x[i, k])
solver.Maximize(sum(obj_terms))

# A. Volume Constraints
for k in K:
    vol_expr = sum(v[i] * x[i, k] for i in C)
    solver.Add(vol_expr <= V_max[k])

# B. Weight Constraints
for k in K:
    wt_expr = sum(w[i] * x[i, k] for i in C)
    solver.Add(wt_expr <= W_max[k])

# C. Cargo Supply Constraints
for i in C:
    supply_expr = sum(x[i, k] for k in K)
    solver.Add(supply_expr <= Q[i])

# D. Balance (Stability) Constraints
# Define weight expressions for each compartment
WF = sum(w[i] * x[i, 'F'] for i in C)
WM = sum(w[i] * x[i, 'M'] for i in C)
WR = sum(w[i] * x[i, 'R'] for i in C)

# 1. Front/Middle Balance: (2/3)(1-0.15) WM <= WF <= (2/3)(1+0.15) WM
# Lower: WF - (17/30)WM <= 0
solver.Add(WF - (17.0 / 30.0) * WM <= 0)
# Upper: WF - (23/30)WM >= 0  =>  (23/30)WM - WF <= 0
solver.Add((23.0 / 30.0) * WM - WF <= 0)

# 2. Rear/Middle Balance: (1/2)(1-0.15) WM <= WR <= (1/2)(1+0.15) WM
# Lower: WR - (17/40)WM <= 0
solver.Add(WR - (17.0 / 40.0) * WM <= 0)
# Upper: WR - (23/40)WM >= 0  =>  (23/40)WM - WR <= 0
solver.Add((23.0 / 40.0) * WM - WR <= 0)

# 3. Front/Rear Balance: (4/3)(1-0.10) WR <= WF <= (4/3)(1+0.10) WR
# Lower: WF - (16/15)WR <= 0
solver.Add(WF - (16.0 / 15.0) * WR <= 0)
# Upper: WF - (22/15)WR >= 0  =>  (22/15)WR - WF <= 0
solver.Add((22.0 / 15.0) * WR - WF <= 0)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")