from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    infinity = solver.infinity()
    
    # Parameters
    num_shifts = 6
    num_slots = 6
    
    # Requirements per slot (R_1 to R_6)
    R = [10, 15, 25, 20, 18, 12]
    
    # Costs per shift
    cost_ft = 80
    cost_ct = 120
    
    # Decision Variables
    # x[k]: Number of full-time nurses for shift k (0-indexed in code, 1-indexed in math)
    # y[k]: Number of contract nurses for shift k
    x = dict()
    y = dict()
    
    for k in range(num_shifts):
        x[k] = solver.NumVar(0, infinity, 'x_' + str(k))
        y[k] = solver.NumVar(0, infinity, 'y_' + str(k))
    
    # Objective Function: Minimize total cost
    obj = sum(cost_ft * x[k] + cost_ct * y[k] for k in range(num_shifts))
    solver.Minimize(obj)
    
    # Constraints
    # Shift k (0-indexed) covers slots:
    # Shift 0 (2:00 start) -> Slots 0, 1
    # Shift 1 (6:00 start) -> Slots 1, 2
    # Shift 2 (10:00 start)-> Slots 2, 3
    # Shift 3 (14:00 start)-> Slots 3, 4
    # Shift 4 (18:00 start)-> Slots 4, 5
    # Shift 5 (22:00 start)-> Slots 5, 0
    
    # Slot 0 (2:00-6:00) is covered by Shift 5 and Shift 0
    solver.Add(x[5] + y[5] + x[0] + y[0] >= R[0])
    
    # Slot 1 (6:00-10:00) is covered by Shift 0 and Shift 1
    solver.Add(x[0] + y[0] + x[1] + y[1] >= R[1])
    
    # Slot 2 (10:00-14:00) is covered by Shift 1 and Shift 2
    solver.Add(x[1] + y[1] + x[2] + y[2] >= R[2])
    
    # Slot 3 (14:00-18:00) is covered by Shift 2 and Shift 3
    solver.Add(x[2] + y[2] + x[3] + y[3] >= R[3])
    
    # Slot 4 (18:00-22:00) is covered by Shift 3 and Shift 4
    solver.Add(x[3] + y[3] + x[4] + y[4] >= R[4])
    
    # Slot 5 (22:00-2:00) is covered by Shift 4 and Shift 5
    solver.Add(x[4] + y[4] + x[5] + y[5] >= R[5])
    
    # Solve
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()