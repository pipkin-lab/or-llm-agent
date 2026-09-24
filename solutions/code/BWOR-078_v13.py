from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Parameters
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

# Predecessors
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

tasks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'L', 'm', 'n']

# Variables
S = dict()
for t in tasks:
    S[t] = solver.NumVar(0, INF, 'S_' + t)

Z = solver.NumVar(0, INF, 'Z')

# Objective
solver.Minimize(Z)

# Precedence constraints
for t in tasks:
    for p in P[t]:
        solver.Add(S[t] >= S[p] + D[p])

# Project completion: n is the unique terminal node
solver.Add(Z >= S['n'] + D['n'])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")