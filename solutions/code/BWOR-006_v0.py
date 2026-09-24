from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables: x[a, b, p]
# a in {1, 2} for A1, A2
# b in {1, 2, 3} for B1, B2, B3
# p in {0, 1, 2} for I, II, III

# Valid combinations:
# Product I (p=0): all (a,b)
# Product II (p=1): (1,1), (2,1)
# Product III (p=2): (2,2)

x = dict()

# Product I
for a in range(1, 3):
    for b in range(1, 4):
        x[a, b, 0] = solver.NumVar(0, INF, 'x_{}_{}_I'.format(a, b))

# Product II
x[1, 1, 1] = solver.NumVar(0, INF, 'x_1_1_II')
x[2, 1, 1] = solver.NumVar(0, INF, 'x_2_1_II')

# Product III
x[2, 2, 2] = solver.NumVar(0, INF, 'x_2_2_III')

# Objective coefficients (profit per unit)
# Product I
pi_I = dict()
pi_I[(1, 1)] = 0.39
pi_I[(1, 2)] = 0.31
pi_I[(1, 3)] = 0.40
pi_I[(2, 1)] = 0.43
pi_I[(2, 2)] = 0.35
pi_I[(2, 3)] = 0.44

# Product II
pi_II = dict()
pi_II[(1, 1)] = 0.67
pi_II[(2, 1)] = 0.90

# Product III
pi_III = dict()
pi_III[(2, 2)] = 0.73

# Build objective
obj = 0
for a in range(1, 3):
    for b in range(1, 4):
        obj += pi_I[(a, b)] * x[a, b, 0]

obj += pi_II[(1, 1)] * x[1, 1, 1]
obj += pi_II[(2, 1)] * x[2, 1, 1]
obj += pi_III[(2, 2)] * x[2, 2, 2]

solver.Maximize(obj)

# Machine capacity constraints
# Processing times: t[a, b, p]
# Stage A machines: a=1 (A1), a=2 (A2)
# Stage B machines: b=1 (B1), b=2 (B2), b=3 (B3)

# Stage A - A1 (a=1): 5*x_11^I + 10*x_11^II <= 6000
solver.Add(5 * x[1, 1, 0] + 10 * x[1, 1, 1] <= 6000)

# Stage A - A2 (a=2): 7*x_21^I + 9*x_21^II + 12*x_22^III <= 10000
solver.Add(7 * x[2, 1, 0] + 9 * x[2, 1, 1] + 12 * x[2, 2, 2] <= 10000)

# Stage B - B1 (b=1): 6*x_11^I + 8*x_11^II <= 4000
solver.Add(6 * x[1, 1, 0] + 8 * x[1, 1, 1] <= 4000)

# Stage B - B2 (b=2): 4*x_12^I + 11*x_22^III <= 7000
solver.Add(4 * x[1, 2, 0] + 11 * x[2, 2, 2] <= 7000)

# Stage B - B3 (b=3): 7*x_13^I <= 4000
solver.Add(7 * x[1, 3, 0] <= 4000)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")