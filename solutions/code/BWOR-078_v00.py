from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

tasks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'L', 'm', 'n']

t = dict()
for task in tasks:
    t[task] = solver.NumVar(0, INF, 't_' + task)

t_end = solver.NumVar(0, INF, 't_end')

solver.Add(t['c'] >= t['a'] + 10)
solver.Add(t['c'] >= t['b'] + 8)
solver.Add(t['d'] >= t['b'] + 8)
solver.Add(t['e'] >= t['c'] + 6)
solver.Add(t['f'] >= t['d'] + 16)
solver.Add(t['f'] >= t['e'] + 24)
solver.Add(t['g'] >= t['f'] + 4)
solver.Add(t['h'] >= t['f'] + 4)
solver.Add(t['i'] >= t['f'] + 4)
solver.Add(t['j'] >= t['g'] + 4)
solver.Add(t['k'] >= t['h'] + 10)
solver.Add(t['k'] >= t['i'] + 4)
solver.Add(t['k'] >= t['j'] + 12)
solver.Add(t['L'] >= t['c'] + 6)
solver.Add(t['m'] >= t['L'] + 8)
solver.Add(t['n'] >= t['k'] + 16)
solver.Add(t['n'] >= t['m'] + 24)

solver.Add(t_end >= t['n'] + 4)

solver.Minimize(t_end)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")