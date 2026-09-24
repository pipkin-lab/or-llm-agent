from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if solver is None:
        print("NO_FEASIBLE_SOLUTION")
        return

    workers = ['A', 'B', 'C', 'D', 'E']
    stations = ['I', 'II', 'III', 'IV', 'V']

    efficiency = dict()
    efficiency[('A', 'I')] = 2
    efficiency[('A', 'II')] = 3
    efficiency[('A', 'III')] = 4
    efficiency[('A', 'IV')] = 1
    efficiency[('A', 'V')] = 7
    efficiency[('B', 'I')] = 3
    efficiency[('B', 'II')] = 4
    efficiency[('B', 'III')] = 2
    efficiency[('B', 'IV')] = 5
    efficiency[('B', 'V')] = 6
    efficiency[('C', 'I')] = 2
    efficiency[('C', 'II')] = 5
    efficiency[('C', 'III')] = 3
    efficiency[('C', 'IV')] = 4
    efficiency[('C', 'V')] = 1
    efficiency[('D', 'I')] = 5
    efficiency[('D', 'II')] = 2
    efficiency[('D', 'III')] = 3
    efficiency[('D', 'IV')] = 2
    efficiency[('D', 'V')] = 5
    efficiency[('E', 'I')] = 3
    efficiency[('E', 'II')] = 7
    efficiency[('E', 'III')] = 6
    efficiency[('E', 'IV')] = 2
    efficiency[('E', 'V')] = 4

    x = dict()
    for w in workers:
        for s in stations:
            x[w, s] = solver.NumVar(0, 1, 'x_' + w + '_' + s)

    for s in stations:
        solver.Add(sum(x[w, s] for w in workers) == 1)

    for w in workers:
        solver.Add(sum(x[w, s] for s in stations) == 1)

    obj_terms = []
    for w in workers:
        for s in stations:
            obj_terms.append(efficiency[w, s] * x[w, s])
    objective = sum(obj_terms)

    solver.Maximize(objective)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    main()