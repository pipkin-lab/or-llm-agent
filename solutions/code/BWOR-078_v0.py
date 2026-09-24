from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Define tasks and their durations
tasks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'L', 'm', 'n']
D = dict()
D['a'] = 10
D['b'] = 8
D['c'] = 6
D['d'] = 16
D['e'] = 24
D['f'] = 4
D['g'] = 4
D['h'] = 10
D['i'] = 4
D['j'] = 12
D['k'] = 16
D['L'] = 8
D['m'] = 24
D['n'] = 4

# Precedence: P(i) = set of immediate predecessors
P = dict()
P['a'] = []
P['b'] = []
P['c'] = ['a', 'b']
P['d'] = ['b']
P['e'] = ['c']
P['f'] = ['d', 'e']
P['g'] = ['f']
P['h'] = ['f']
P['i'] = ['f']
P['j'] = ['g']
P['k'] = ['h', 'i', 'j']
P['L'] = ['c']
P['m'] = ['L']
P['n'] = ['k', 'm']

# Decision variables: ES_i for each task, and T_proj
ES = dict()
for t in tasks:
    ES[t] = solver.NumVar(0, INF, 'ES_' + t)

T_proj = solver.NumVar(0, INF, 'T_proj')

# Precedence constraints: ES_i >= ES_p + D_p
for t in tasks:
    for p in P[t]:
        solver.Add(ES[t] >= ES[p] + D[p])

# Project completion: T_proj >= ES_n + D_n (n is the unique terminal task)
solver.Add(T_proj >= ES['n'] + D['n'])

# Objective: minimize T_proj
solver.Minimize(T_proj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")