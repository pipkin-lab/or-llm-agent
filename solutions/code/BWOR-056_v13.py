from ortools.linear_solver import pywraplp

# Course set C = {1, 2, 3, 4, 5, 6, 7}
C = [1, 2, 3, 4, 5, 6, 7]

# Category sets
categories = ['Math', 'OR', 'CS']
Req = dict()
Req['Math'] = 2
Req['OR'] = 2
Req['CS'] = 2

# Category Membership Matrix M[c][k]
# Course 1: Calculus -> Math=1, OR=0, CS=0
# Course 2: Operations Research -> Math=1, OR=1, CS=0
# Course 3: Data Structures -> Math=1, OR=0, CS=1
# Course 4: Managerial Statistics -> Math=1, OR=1, CS=0
# Course 5: Computer Simulation -> Math=0, OR=1, CS=1
# Course 6: Computer Programming -> Math=0, OR=0, CS=1
# Course 7: Forecasting -> Math=1, OR=1, CS=0

M = dict()
for c in C:
    M[c] = dict()

M[1] = dict()
M[1]['Math'] = 1
M[1]['OR'] = 0
M[1]['CS'] = 0

M[2] = dict()
M[2]['Math'] = 1
M[2]['OR'] = 1
M[2]['CS'] = 0

M[3] = dict()
M[3]['Math'] = 1
M[3]['OR'] = 0
M[3]['CS'] = 1

M[4] = dict()
M[4]['Math'] = 1
M[4]['OR'] = 1
M[4]['CS'] = 0

M[5] = dict()
M[5]['Math'] = 0
M[5]['OR'] = 1
M[5]['CS'] = 1

M[6] = dict()
M[6]['Math'] = 0
M[6]['OR'] = 0
M[6]['CS'] = 1

M[7] = dict()
M[7]['Math'] = 1
M[7]['OR'] = 1
M[7]['CS'] = 0

# Prerequisite pairs: (predecessor, successor) meaning if successor is taken, predecessor must be taken
prereqs = dict()
# x_5 <= x_6 (5 requires 6)
prereqs[5] = 6
# x_3 <= x_6 (3 requires 6)
prereqs[3] = 6
# x_4 <= x_1 (4 requires 1)
prereqs[4] = 1
# x_7 <= x_4 (7 requires 4)
prereqs[7] = 4

# Create Solver (MILP -> SCIP)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision Variables
x = dict()
for c in C:
    x[c] = solver.BoolVar('x_' + str(c))

# Objective: Minimize sum of x_c
objective = sum(x[c] for c in C)
solver.Minimize(objective)

# Category Coverage Constraints
for k in categories:
    solver.Add(sum(M[c][k] * x[c] for c in C) >= Req[k])

# Prerequisite Constraints
for succ, pred in prereqs.items():
    solver.Add(x[succ] <= x[pred])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")