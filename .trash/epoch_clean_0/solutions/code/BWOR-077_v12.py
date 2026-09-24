from ortools.linear_solver import pywraplp

W = ['A', 'B', 'C', 'D', 'E']
S = ['I', 'II', 'III', 'IV', 'V']

c = dict()
c[('A', 'I')] = 2; c[('A', 'II')] = 3; c[('A', 'III')] = 4; c[('A', 'IV')] = 1; c[('A', 'V')] = 7
c[('B', 'I')] = 3; c[('B', 'II')] = 4; c[('B', 'III')] = 2; c[('B', 'IV')] = 5; c[('B', 'V')] = 6
c[('C', 'I')] = 2; c[('C', 'II')] = 5; c[('C', 'III')] = 3; c[('C', 'IV')] = 4; c[('C', 'V')] = 1
c[('D', 'I')] = 5; c[('D', 'II')] = 2; c[('D', 'III')] = 3; c[('D', 'IV')] = 2; c[('D', 'V')] = 5
c[('E', 'I')] = 3; c[('E', 'II')] = 7; c[('E', 'III')] = 6; c[('E', 'IV')] = 2; c[('E', 'V')] = 4

solver = pywraplp.Solver.CreateSolver('SCIP')

x = dict()
for w in W:
    for s in S:
        x[w, s] = solver.BoolVar('x_' + w + '_' + s)

R = solver.NumVar(0, solver.infinity(), 'R')

for w in W:
    solver.Add(sum(x[w, s] for s in S) == 1)

for s in S:
    solver.Add(sum(x[w, s] for w in W) == 1)

for s in S:
    solver.Add(R <= sum(c[w, s] * x[w, s] for w in W))

solver.Maximize(R)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")