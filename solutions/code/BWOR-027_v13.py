import math
from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()
    N = 10
    nodes = list(range(1, N + 1))
    
    coords = dict()
    coords[1] = (0, 0)
    coords[2] = (5, 20)
    coords[3] = (8, 12)
    coords[4] = (7, 4)
    coords[5] = (10, 15)
    coords[6] = (12, 18)
    coords[7] = (18, 18)
    coords[8] = (18, 15)
    coords[9] = (18, 18)
    coords[10] = (20, 17)

    c = dict()
    for i in nodes:
        for j in nodes:
            if i != j:
                c[i, j] = math.sqrt((coords[i][0] - coords[j][0])**2 + (coords[i][1] - coords[j][1])**2)
            else:
                c[i, j] = 0

    x = dict()
    for i in nodes:
        for j in nodes:
            if i != j:
                x[i, j] = solver.BoolVar('x_{}_{}'.format(i, j))

    s = dict()
    for i in nodes:
        s[i] = solver.BoolVar('s_{}'.format(i))

    e = dict()
    for i in nodes:
        e[i] = solver.BoolVar('e_{}'.format(i))

    u = dict()
    for i in nodes:
        u[i] = solver.NumVar(0, N - 1, 'u_{}'.format(i))

    # Objective
    objective_terms = [c[i, j] * x[i, j] for i in nodes for j in nodes if i != j]
    solver.Minimize(sum(objective_terms))

    # Start/End Uniqueness
    solver.Add(sum(s[i] for i in nodes) == 1)
    solver.Add(sum(e[i] for i in nodes) == 1)
    for i in nodes:
        solver.Add(s[i] + e[i] <= 1)

    # Flow Conservation
    for i in nodes:
        # Out-degree
        out_terms = [x[i, j] for j in nodes if j != i]
        solver.Add(sum(out_terms) == 1 - e[i])
        
        # In-degree
        in_terms = [x[j, i] for j in nodes if j != i]
        solver.Add(sum(in_terms) == 1 - s[i])

    # Subtour Elimination (MTZ)
    for i in nodes:
        for j in nodes:
            if i != j:
                solver.Add(u[i] - u[j] + N * x[i, j] <= N - 1)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    main()