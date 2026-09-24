from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables: x[m, i] = units of product i on machine m
# Only feasible (m, i) pairs
x = dict()
feasible_pairs = [
    ('A1', 1), ('A1', 2),
    ('A2', 1), ('A2', 2), ('A2', 3),
    ('B1', 1), ('B1', 2),
    ('B2', 1), ('B2', 3),
    ('B3', 1)
]
for m, i in feasible_pairs:
    x[m, i] = solver.NumVar(0, INF, 'x_' + m + '_' + str(i))

# Parameters
t = dict()
t['A1', 1] = 5
t['A1', 2] = 10
t['A2', 1] = 7
t['A2', 2] = 9
t['A2', 3] = 12
t['B1', 1] = 6
t['B1', 2] = 8
t['B2', 1] = 4
t['B2', 3] = 11
t['B3', 1] = 7

C = dict()
C['A1'] = 6000
C['A2'] = 10000
C['B1'] = 4000
C['B2'] = 7000
C['B3'] = 4000

r = dict()
r['A1'] = 0.05
r['A2'] = 0.03
r['B1'] = 0.06
r['B2'] = 0.11
r['B3'] = 0.05

c = dict()
c[1] = 0.25
c[2] = 0.35
c[3] = 0.50

p = dict()
p[1] = 1.25
p[2] = 2.00
p[3] = 2.80

# Objective: Maximize Z
# Z = sum_i (sum_m x[m,i]) * (p_i - c_i) - sum_m (sum_i x[m,i] * t[m,i]) * r[m]
obj = 0
for i in [1, 2, 3]:
    q_i = sum(x[m, i] for (m, ii) in feasible_pairs if ii == i)
    obj += (p[i] - c[i]) * q_i

for m, i in feasible_pairs:
    obj -= r[m] * t[m, i] * x[m, i]

solver.Maximize(obj)

# Flow balance constraints
# Product I: A1,1 + A2,1 = B1,1 + B2,1 + B3,1
solver.Add(x['A1', 1] + x['A2', 1] == x['B1', 1] + x['B2', 1] + x['B3', 1])
# Product II: A1,2 + A2,2 = B1,2
solver.Add(x['A1', 2] + x['A2', 2] == x['B1', 2])
# Product III: A2,3 = B2,3
solver.Add(x['A2', 3] == x['B2', 3])

# Machine capacity constraints
solver.Add(5 * x['A1', 1] + 10 * x['A1', 2] <= C['A1'])
solver.Add(7 * x['A2', 1] + 9 * x['A2', 2] + 12 * x['A2', 3] <= C['A2'])
solver.Add(6 * x['B1', 1] + 8 * x['B1', 2] <= C['B1'])
solver.Add(4 * x['B2', 1] + 11 * x['B2', 3] <= C['B2'])
solver.Add(7 * x['B3', 1] <= C['B3'])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")