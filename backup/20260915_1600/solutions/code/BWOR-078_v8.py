from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    tasks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'L', 'm', 'n']
    durations = dict()
    durations['a'] = 10
    durations['b'] = 8
    durations['c'] = 6
    durations['d'] = 16
    durations['e'] = 24
    durations['f'] = 4
    durations['g'] = 4
    durations['h'] = 10
    durations['i'] = 4
    durations['j'] = 12
    durations['k'] = 16
    durations['L'] = 8
    durations['m'] = 24
    durations['n'] = 4

    predecessors = dict()
    predecessors['a'] = []
    predecessors['b'] = []
    predecessors['c'] = ['a', 'b']
    predecessors['d'] = ['b']
    predecessors['e'] = ['c']
    predecessors['f'] = ['d', 'e']
    predecessors['g'] = ['f']
    predecessors['h'] = ['f']
    predecessors['i'] = ['f']
    predecessors['j'] = ['g']
    predecessors['k'] = ['h', 'i', 'j']
    predecessors['L'] = ['c']
    predecessors['m'] = ['L']
    predecessors['n'] = ['k', 'm']

    S = dict()
    for t in tasks:
        S[t] = solver.NumVar(0, INF, 'S_' + t)

    Z = solver.NumVar(0, INF, 'Z')

    for t in tasks:
        for p in predecessors[t]:
            solver.Add(S[t] >= S[p] + durations[p])

    for t in tasks:
        solver.Add(Z >= S[t] + durations[t])

    solver.Minimize(Z)
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    main()