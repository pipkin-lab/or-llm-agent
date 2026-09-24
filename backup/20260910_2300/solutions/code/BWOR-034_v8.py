from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
inf = solver.infinity()

# Parameters
R = dict()
R[1] = 1500
R[2] = 1000
R[3] = 2000
R[4] = 1200

C = dict()
C[1] = 28
C[2] = 45
C[3] = 60
C[4] = 73

# Valid (t, d) pairs where t + d - 1 <= 4
valid_pairs = dict()
for t in range(1, 5):
    for d in range(1, 5):
        if t + d - 1 <= 4:
            valid_pairs[(t, d)] = solver.NumVar(0, inf, 'x_' + str(t) + '_' + str(d))

# Objective: minimize total cost
obj_terms = []
for (t, d), var in valid_pairs.items():
    obj_terms.append(C[d] * var)
objective = sum(obj_terms)
solver.Minimize(objective)

# Capacity coverage constraints
for t in range(1, 5):
    active_terms = []
    for (t_prime, d), var in valid_pairs.items():
        if t_prime <= t <= t_prime + d - 1:
            active_terms.append(var)
    solver.Add(sum(active_terms) >= R[t])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")