from ortools.linear_solver import pywraplp
import math

# Parameters
D = {1: 450, 2: 480, 3: 540, 4: 600}
P = {
    (1, 'H'): 0.10, (1, 'L'): 0.08,
    (2, 'H'): 0.20, (2, 'L'): 0.16,
    (3, 'H'): 0.15, (3, 'L'): 0.12,
    (4, 'H'): 0.25, (4, 'L'): 0.20,
}
R_H = 2
R_L = 3
R_empty = 4
F_fixed = 100
Fuel_max = 48000
N_H_max = 48
N_L_max = 32

# Pre-compute fuel cost per bomb and log-damage coefficient
F_cost = {}
C_coeff = {}
for k in [1, 2, 3, 4]:
    for b in ['H', 'L']:
        R = R_H if b == 'H' else R_L
        F_cost[(k, b)] = D[k] * (1.0 / R + 1.0 / R_empty) + F_fixed
        C_coeff[(k, b)] = -math.log(1.0 - P[(k, b)])

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

x = dict()
for k in [1, 2, 3, 4]:
    for b in ['H', 'L']:
        x[(k, b)] = solver.IntVar(0, INF, 'x_' + str(k) + '_' + b)

# Objective: Maximize sum of x * C_coeff
obj = 0
for k in [1, 2, 3, 4]:
    for b in ['H', 'L']:
        obj += x[(k, b)] * C_coeff[(k, b)]
solver.Maximize(obj)

# Constraint 1: Heavy bomb availability
solver.Add(sum(x[(k, 'H')] for k in [1, 2, 3, 4]) <= N_H_max)

# Constraint 2: Light bomb availability
solver.Add(sum(x[(k, 'L')] for k in [1, 2, 3, 4]) <= N_L_max)

# Constraint 3: Fuel constraint
fuel_expr = 0
for k in [1, 2, 3, 4]:
    for b in ['H', 'L']:
        fuel_expr += x[(k, b)] * F_cost[(k, b)]
solver.Add(fuel_expr <= Fuel_max)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    Z_star = solver.Objective().Value()
    prob = 1.0 - math.exp(-Z_star)
    print("OPTIMAL_VALUE:", prob)
else:
    print("NO_FEASIBLE_SOLUTION")