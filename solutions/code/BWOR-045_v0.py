from ortools.linear_solver import pywraplp

# Define index sets
P = ['A', 'B', 'C', 'D']
R = ['I', 'II', 'III', 'IV', 'V', 'VI']

# Parameters
S = dict()
S['A'] = 200
S['B'] = 300
S['C'] = 400
S['D'] = 100

D = dict()
D['I'] = 200
D['II'] = 150
D['III'] = 400
D['IV'] = 100
D['V'] = 150
D['VI'] = 150

# Net profit coefficients in Yuan/ton: Pi[i][j] = 1000 * (p_j - c_i - t_ij)
Pi = dict()
# Plant A
Pi[('A', 'I')] = 300
Pi[('A', 'II')] = 800
Pi[('A', 'III')] = 300
Pi[('A', 'IV')] = 600
Pi[('A', 'V')] = 100
Pi[('A', 'VI')] = 700
# Plant B
Pi[('B', 'I')] = 300
Pi[('B', 'II')] = 200
Pi[('B', 'III')] = -500
Pi[('B', 'IV')] = 300
Pi[('B', 'V')] = -400
Pi[('B', 'VI')] = 400
# Plant C
Pi[('C', 'I')] = 200
Pi[('C', 'II')] = 600
Pi[('C', 'III')] = 400
Pi[('C', 'IV')] = 400
Pi[('C', 'V')] = 100
Pi[('C', 'VI')] = 500
# Plant D
Pi[('D', 'I')] = -100
Pi[('D', 'II')] = 500
Pi[('D', 'III')] = 100
Pi[('D', 'IV')] = 100
Pi[('D', 'V')] = -400
Pi[('D', 'VI')] = -300

# Create solver
solver = pywraplp.Solver.CreateSolver('GLOP')
if solver is None:
    raise RuntimeError("Failed to create GLOP solver")

INF = solver.infinity()

# Decision variables: x[i, j] >= 0
x = dict()
for i in P:
    for j in R:
        x[i, j] = solver.NumVar(0, INF, 'x_' + i + '_' + j)

# Objective: Maximize total profit
obj_terms = []
for i in P:
    for j in R:
        obj_terms.append(Pi[(i, j)] * x[i, j])
objective = sum(obj_terms)
solver.Maximize(objective)

# Supply constraints: sum_j x[i,j] = S[i]
for i in P:
    solver.Add(sum(x[i, j] for j in R) == S[i])

# Demand constraints
# Region I: <= 200
solver.Add(sum(x[i, 'I'] for i in P) <= D['I'])
# Region II: <= 150
solver.Add(sum(x[i, 'II'] for i in P) <= D['II'])
# Region III: <= 400 and >= 100
solver.Add(sum(x[i, 'III'] for i in P) <= D['III'])
solver.Add(sum(x[i, 'III'] for i in P) >= 100)
# Region IV: = 100 (fully satisfied)
solver.Add(sum(x[i, 'IV'] for i in P) == D['IV'])
# Region V: <= 150
solver.Add(sum(x[i, 'V'] for i in P) <= D['V'])
# Region VI: <= 150
solver.Add(sum(x[i, 'VI'] for i in P) <= D['VI'])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")