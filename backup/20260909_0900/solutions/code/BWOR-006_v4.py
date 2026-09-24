from ortools.linear_solver import pywraplp

# Create the solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Define parameters
# Processing times
t_A = {
    (1, 1): 5, (2, 1): 7,
    (1, 2): 10, (2, 2): 9,
    (2, 3): 12
}
t_B = {
    (1, 1): 6, (2, 1): 4, (3, 1): 7,
    (1, 2): 8,
    (2, 3): 11
}

# Available hours
H_A = {1: 6000, 2: 10000}
H_B = {1: 4000, 2: 7000, 3: 4000}

# Processing costs per hour
c_A = {1: 0.05, 2: 0.03}
c_B = {1: 0.06, 2: 0.11, 3: 0.05}

# Raw material cost per unit
r = {1: 0.25, 2: 0.35, 3: 0.50}

# Selling price per unit
s = {1: 1.25, 2: 2.00, 3: 2.80}

# Define decision variables
# x_A[m, p] for m in {1, 2}, p in {1, 2, 3}
# x_B[m, p] for m in {1, 2, 3}, p in {1, 2, 3}

x_A = dict()
x_B = dict()

# Feasible routes for Stage A
# Product 1: A1, A2
# Product 2: A1, A2
# Product 3: A2 only
for m in [1, 2]:
    for p in [1, 2, 3]:
        if (m, p) in t_A:
            x_A[m, p] = solver.NumVar(0, solver.infinity(), 'x_A_' + str(m) + '_' + str(p))
        else:
            x_A[m, p] = 0

# Feasible routes for Stage B
# Product 1: B1, B2, B3
# Product 2: B1 only
# Product 3: B2 only
for m in [1, 2, 3]:
    for p in [1, 2, 3]:
        if (m, p) in t_B:
            x_B[m, p] = solver.NumVar(0, solver.infinity(), 'x_B_' + str(m) + '_' + str(p))
        else:
            x_B[m, p] = 0

# Objective function
# Maximize Z = sum_{p, mA} (s_p - r_p - t_A[mA, p]*c_A[mA]) * x_A[mA, p] - sum_{p, mB} (t_B[mB, p]*c_B[mB]) * x_B[mB, p]

obj = 0
for p in [1, 2, 3]:
    for mA in [1, 2]:
        if (mA, p) in t_A:
            coeff_A = s[p] - r[p] - t_A[mA, p] * c_A[mA]
            obj += coeff_A * x_A[mA, p]

for p in [1, 2, 3]:
    for mB in [1, 2, 3]:
        if (mB, p) in t_B:
            coeff_B = -t_B[mB, p] * c_B[mB]
            obj += coeff_B * x_B[mB, p]

solver.Maximize(obj)

# Constraints

# 1. Flow Conservation: sum_mA x_A[mA, p] = sum_mB x_B[mB, p] for all p
for p in [1, 2, 3]:
    flow_A = sum(x_A[mA, p] for mA in [1, 2] if (mA, p) in t_A)
    flow_B = sum(x_B[mB, p] for mB in [1, 2, 3] if (mB, p) in t_B)
    solver.Add(flow_A == flow_B)

# 2. Machine Capacity Constraints (Stage A)
for mA in [1, 2]:
    capacity_expr = 0
    for p in [1, 2, 3]:
        if (mA, p) in t_A:
            capacity_expr += t_A[mA, p] * x_A[mA, p]
    solver.Add(capacity_expr <= H_A[mA])

# 3. Machine Capacity Constraints (Stage B)
for mB in [1, 2, 3]:
    capacity_expr = 0
    for p in [1, 2, 3]:
        if (mB, p) in t_B:
            capacity_expr += t_B[mB, p] * x_B[mB, p]
    solver.Add(capacity_expr <= H_B[mB])

# Solve the problem
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")