from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

W = ['A', 'B', 'C', 'D', 'E']
L = ['Urban', 'alpha', 'beta']

S = dict()
S[('A', 'alpha')] = 100
S[('A', 'beta')] = 100
S[('B', 'alpha')] = 150
S[('B', 'beta')] = 200
S[('C', 'alpha')] = 100
S[('C', 'beta')] = 150
S[('D', 'alpha')] = 200
S[('D', 'beta')] = 150
S[('E', 'alpha')] = 50
S[('E', 'beta')] = 150

C = dict()
C[('A', 'C')] = 1000
C[('A', 'D')] = 1500
C[('B', 'C')] = 1400
C[('B', 'D')] = 1200
C[('C', 'E')] = 2000
C[('D', 'E')] = 700

D_cost = dict()
D_cost[('alpha', 'alpha')] = 500
D_cost[('alpha', 'beta')] = 1400
D_cost[('alpha', 'Urban')] = 1300
D_cost[('beta', 'beta')] = 500
D_cost[('beta', 'Urban')] = 900
D_cost[('Urban', 'Urban')] = 1000

def get_D(j, l):
    if j == l:
        return D_cost[(j, l)]
    if (j, l) in D_cost:
        return D_cost[(j, l)]
    if (l, j) in D_cost:
        return D_cost[(l, j)]
    raise ValueError('D cost not provided for ' + j + ' and ' + l)

x = dict()
for i in W:
    for l in L:
        x[i, l] = solver.BoolVar('x_' + i + '_' + l)

y = dict()
for i in W:
    for k in W:
        for j in L:
            for l in L:
                y[i, k, j, l] = solver.BoolVar('y_' + i + '_' + k + '_' + j + '_' + l)

for i in W:
    solver.Add(sum(x[i, l] for l in L) == 1)

for l in L:
    solver.Add(sum(x[i, l] for i in W) <= 3)

for i in W:
    for k in W:
        for j in L:
            for l in L:
                solver.Add(y[i, k, j, l] <= x[i, j])
                solver.Add(y[i, k, j, l] <= x[k, l])
                solver.Add(y[i, k, j, l] >= x[i, j] + x[k, l] - 1)

obj_terms = []
for i in W:
    for k in W:
        for j in L:
            for l in L:
                if i == k and j == l:
                    continue
                if i == k:
                    continue
                c_val = 0
                if (i, k) in C:
                    c_val = C[(i, k)]
                elif (k, i) in C:
                    c_val = C[(k, i)]
                if c_val == 0:
                    continue
                d_val = get_D(j, l)
                coeff = c_val * d_val
                obj_terms.append(coeff * y[i, k, j, l])

savings_terms = []
for i in W:
    for l in ['alpha', 'beta']:
        s_val = S[(i, l)]
        savings_terms.append(10000 * s_val * x[i, l])

objective = sum(obj_terms) - sum(savings_terms)
solver.Minimize(objective)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")