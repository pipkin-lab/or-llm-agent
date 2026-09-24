from ortools.linear_solver import pywraplp
import math

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Index sets
parts = [1, 2, 3, 4]

# Parameters
distances = dict()
distances[1] = 450
distances[2] = 480
distances[3] = 540
distances[4] = 600

p_h = dict()
p_h[1] = 0.10
p_h[2] = 0.20
p_h[3] = 0.15
p_h[4] = 0.25

p_l = dict()
p_l[1] = 0.08
p_l[2] = 0.16
p_l[3] = 0.12
p_l[4] = 0.20

# Fuel per sortie (liters)
# Heavy: outbound d/2, return d/4, +100 takeoff/landing
# Light: outbound d/3, return d/4, +100 takeoff/landing
F_h = dict()
F_l = dict()
for i in parts:
    d = distances[i]
    F_h[i] = d * (1.0 / 2.0 + 1.0 / 4.0) + 100.0
    F_l[i] = d * (1.0 / 3.0 + 1.0 / 4.0) + 100.0

# Objective coefficients: ln(1 - p)
C_h = dict()
C_l = dict()
for i in parts:
    C_h[i] = math.log(1.0 - p_h[i])
    C_l[i] = math.log(1.0 - p_l[i])

# Resource limits
H_max = 48
L_max = 32
Fuel_max = 48000.0

# Decision variables
x_h = dict()
x_l = dict()
for i in parts:
    x_h[i] = solver.IntVar(0, INF, 'x_h_' + str(i))
    x_l[i] = solver.IntVar(0, INF, 'x_l_' + str(i))

# Objective: minimize sum of C_ik * x_ik (negative coefficients)
obj_terms = []
for i in parts:
    obj_terms.append(C_h[i] * x_h[i])
    obj_terms.append(C_l[i] * x_l[i])
solver.Minimize(sum(obj_terms))

# Constraint 1: Total heavy bombs
solver.Add(sum(x_h[i] for i in parts) <= H_max)

# Constraint 2: Total light bombs
solver.Add(sum(x_l[i] for i in parts) <= L_max)

# Constraint 3: Fuel
fuel_terms = []
for i in parts:
    fuel_terms.append(F_h[i] * x_h[i])
    fuel_terms.append(F_l[i] * x_l[i])
solver.Add(sum(fuel_terms) <= Fuel_max)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    log_survival = solver.Objective().Value()
    survival_prob = math.exp(log_survival)
    destruction_prob = 1.0 - survival_prob
    print("OPTIMAL_VALUE:", destruction_prob)
else:
    print("NO_FEASIBLE_SOLUTION")