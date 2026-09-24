from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
P = {1: 2.5, 2: 2.6, 3: 2.8, 4: 3.1}
SV = {1: 2.0, 2: 1.6, 3: 1.3, 4: 1.1}
C = {1: 0.3, 2: 0.8, 3: 1.5, 4: 2.0}

# Calculate K[t, d] = P[t] + sum(C[1..d]) - SV[d]
def calc_K(t, d):
    op_cost = sum(C[k] for k in range(1, d + 1))
    return P[t] + op_cost - SV[d]

# Define valid (t, d) pairs
valid_pairs = []
for t in range(1, 5):
    for d in range(1, 5):
        if t + d - 1 <= 4:
            valid_pairs.append((t, d))

# Create variables
x = dict()
for t, d in valid_pairs:
    x[(t, d)] = solver.IntVar(0, 1, 'x_' + str(t) + '_' + str(d))

# Objective: Minimize total cost
obj = sum(calc_K(t, d) * x[(t, d)] for t, d in valid_pairs)
solver.Minimize(obj)

# Constraint 1: A machine must be purchased at the beginning of Year 1
solver.Add(sum(x[(1, d)] for d in range(1, 5)) == 1)

# Constraint 2: Year 2 purchase = Year 1 machine lasted 1 year
solver.Add(sum(x[(2, d)] for d in range(1, 4)) == x[(1, 1)])

# Constraint 3: Year 3 purchase = Year 1 machine lasted 2 years OR Year 2 machine lasted 1 year
solver.Add(sum(x[(3, d)] for d in range(1, 3)) == x[(1, 2)] + x[(2, 1)])

# Constraint 4: Year 4 purchase = Year 1 machine lasted 3 years OR Year 2 machine lasted 2 years OR Year 3 machine lasted 1 year
solver.Add(x[(4, 1)] == x[(1, 3)] + x[(2, 2)] + x[(3, 1)])

# Constraint 5: End of horizon check
solver.Add(x[(1, 4)] + x[(2, 3)] + x[(3, 2)] + x[(4, 1)] == 1)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")