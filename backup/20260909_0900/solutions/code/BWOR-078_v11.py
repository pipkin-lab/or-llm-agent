from ortools.linear_solver import pywraplp

# Define the solver (LP since all variables are continuous and constraints are difference inequalities)
solver = pywraplp.Solver.CreateSolver('GLOP')

# Task set
tasks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'L', 'm', 'n']

# Durations
D = {
    'a': 10, 'b': 8, 'c': 6, 'd': 16, 'e': 24, 'f': 4,
    'g': 4, 'h': 10, 'i': 4, 'j': 12, 'k': 16, 'L': 8,
    'm': 24, 'n': 4
}

# Precedence: list of (predecessor, successor) pairs
precedence = [
    ('a', 'c'),
    ('b', 'c'),
    ('b', 'd'),
    ('c', 'e'),
    ('c', 'L'),
    ('d', 'f'),
    ('e', 'f'),
    ('f', 'g'),
    ('f', 'h'),
    ('f', 'i'),
    ('g', 'j'),
    ('h', 'k'),
    ('i', 'k'),
    ('j', 'k'),
    ('L', 'm'),
    ('k', 'n'),
    ('m', 'n')
]

# Create start time variables S_t >= 0
S = dict()
for t in tasks:
    S[t] = solver.NumVar(0, solver.infinity(), 'S_' + t)

# Add precedence constraints: S_s >= S_t + D_t
for (p, s) in precedence:
    solver.Add(S[s] >= S[p] + D[p])

# Objective: Minimize S_n + D_n  (completion time of final task n)
obj = S['n'] + D['n']
solver.Minimize(obj)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")