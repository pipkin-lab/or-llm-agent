from ortools.linear_solver import pywraplp

# Parameters
customers = ['A', 'B', 'C', 'D', 'E']
trucks = [1, 2, 3, 4]

demand = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 8}
capacity = {1: 2, 2: 6, 3: 8, 4: 11}
cost = {1: 1, 2: 1, 3: 1, 4: 1} # Placeholder costs, problem didn't specify exact values, but structure is what matters.
# Wait, the prompt says "Cost $c_j$". It doesn't give specific numbers.
# However, usually in such problems, if costs are not given, they might be 1 or proportional to capacity.
# Let's re-read carefully. "Using a truck incurs cost c_j".
# If no specific costs are provided in the prompt text, I should probably assume they are 1 or leave them as variables?
# No, the code must be executable.
# Looking at the prompt again: "Using a truck incurs cost c_j".
# It does not give values for c_j.
# In many textbook examples of this type (Set Covering/Assignment), if costs aren't specified, they are often 1 (minimize number of trucks) or equal to capacity.
# Let's assume cost is 1 for all trucks to minimize the number of trucks used, which is a common default interpretation for "minimize cost" when costs are abstract.
# Alternatively, if I look at similar problems online, sometimes the cost is the capacity or a fixed fee.
# Let's assume cost = 1 for all trucks for the sake of a runnable example, as no data is provided.
# Wait, if I just use 1, the objective is to minimize the number of trucks.
# Let's check if the problem implies specific costs. No.
# I will use cost = 1 for all trucks.

# Create the solver
solver = pywraplp.Solver.CreateSolver('SCIP')
if not solver:
    print("Could not create solver")
    exit(1)

# Decision Variables
# z[i, j] = 1 if customer i is assigned to truck j
z = dict()
for i in customers:
    for j in trucks:
        z[i, j] = solver.BoolVar('z_' + i + '_' + str(j))

# y[j] = 1 if truck j is used
y = dict()
for j in trucks:
    y[j] = solver.BoolVar('y_' + str(j))

# Objective Function
obj_terms = []
for j in trucks:
    obj_terms.append(cost[j] * y[j])
solver.Minimize(sum(obj_terms))

# Constraints

# 1. Assignment: Each customer assigned to exactly one truck
for i in customers:
    solver.Add(sum(z[i, j] for j in trucks) == 1)

# 2. Capacity: Total demand on truck <= Capacity * Used
for j in trucks:
    cap_expr = sum(demand[i] * z[i, j] for i in customers)
    solver.Add(cap_expr <= capacity[j] * y[j])

# 3. Usage Consistency: If customer i is on truck j, truck j is used
for i in customers:
    for j in trucks:
        solver.Add(z[i, j] <= y[j])

# 4. Conflict A-C: Truck cannot serve both A and C
for j in trucks:
    solver.Add(z['A', j] + z['C', j] <= 1)

# 5. Conflict B-D: Truck cannot serve both B and D
for j in trucks:
    solver.Add(z['B', j] + z['D', j] <= 1)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")