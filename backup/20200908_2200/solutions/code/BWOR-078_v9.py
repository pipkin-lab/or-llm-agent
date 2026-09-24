from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if solver is None:
        print("No suitable solver found.")
        return

    # Task durations
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

    tasks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'L', 'm', 'n']

    # Start time variables
    t = dict()
    for task in tasks:
        t[task] = solver.NumVar(0, solver.infinity(), 't_' + task)

    # Project completion time
    T = solver.NumVar(0, solver.infinity(), 'T')

    # Precedence constraints
    # t_i >= t_j + D_j  =>  t_i - t_j >= D_j
    precedence = dict()
    precedence['c'] = ['a', 'b']
    precedence['d'] = ['b']
    precedence['e'] = ['c']
    precedence['f'] = ['d', 'e']
    precedence['g'] = ['f']
    precedence['h'] = ['f']
    precedence['i'] = ['f']
    precedence['j'] = ['g']
    precedence['k'] = ['h', 'i', 'j']
    precedence['L'] = ['c']
    precedence['m'] = ['L']
    precedence['n'] = ['k', 'm']

    for task, preds in precedence.items():
        for pred in preds:
            solver.Add(t[task] - t[pred] >= D[pred])

    # Project completion constraint
    solver.Add(T >= t['n'] + D['n'])

    # Objective: minimize T
    solver.Minimize(T)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    main()