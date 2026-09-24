from ortools.linear_solver import pywraplp

# 1. Data Initialization
P = [1, 2, 3]  # Products I, II, III
T = [1, 2, 3, 4]  # Quarters 1-4

# Demand D[p][t]
D = {
    1: {1: 1500, 2: 1000, 3: 2000, 4: 1200},
    2: {1: 1500, 2: 1500, 3: 1200, 4: 1500},
    3: {1: 1000, 2: 2000, 3: 1500, 4: 2500}
}

# Holding Cost H[p]
H = {1: 5, 2: 5, 3: 5}

# Late Delivery Penalty L[p]
L = {1: 20, 2: 20, 3: 10}

# Production Time a[p]
a = {1: 2, 2: 4, 3: 3}

# Capacity Cap[t]
Cap = {1: 15000, 2: 15000, 3: 15000, 4: 15000}

# Production Feasibility E[p][t] (0 if not allowed, 1 if allowed)
E = {
    1: {1: 1, 2: 0, 3: 1, 4: 1},
    2: {1: 1, 2: 1, 3: 1, 4: 1},
    3: {1: 1, 2: 1, 3: 1, 4: 1}
}

# Initial Inventory/Backlog (0 for all)
I_init = {1: 0, 2: 0, 3: 0}
B_init = {1: 0, 2: 0, 3: 0}

# Final Required Inventory/Backlog
I_final = 150
B_final = 0

# 2. Solver Setup
# Since variables are integers, use SCIP (MILP)
solver = pywraplp.Solver.CreateSolver('SCIP')

# 3. Decision Variables
# x[p][t]: Production quantity
# Inv[p][t]: Ending Inventory
# Back[p][t]: Ending Backlog

x = dict()
Inv = dict()
Back = dict()

for p in P:
    for t in T:
        # Production x
        if E[p][t] == 0:
            x[p, t] = solver.IntVar(0, 0, 'x_' + str(p) + '_' + str(t))
        else:
            x[p, t] = solver.IntVar(0, solver.infinity(), 'x_' + str(p) + '_' + str(t))
        
        # Inventory Inv
        # Note: For t=4, we will fix it to 150. We can define it with bounds and add constraint, or define it directly.
        # It's cleaner to define variables and add constraints.
        Inv[p, t] = solver.IntVar(0, solver.infinity(), 'Inv_' + str(p) + '_' + str(t))
        
        # Backlog Back
        Back[p, t] = solver.IntVar(0, solver.infinity(), 'Back_' + str(p) + '_' + str(t))

# 4. Constraints

# 4.1 Capacity Constraints
for t in T:
    # Sum of production time <= Capacity
    # sum(a[p] * x[p][t] for p in P) <= Cap[t]
    solver.Add(sum(a[p] * x[p, t] for p in P) <= Cap[t])

# 4.2 Production Feasibility (x[p][t] = 0 if E[p][t] == 0)
# This is already handled by defining x[p,t] with upper bound 0 in the variable creation step.
# Explicitly adding for clarity if not done in creation, but creation is sufficient.

# 4.3 Inventory/Backlog Balance Constraints
# Inv[p][t] - Back[p][t] = Inv[p][t-1] - Back[p][t-1] + x[p][t] - D[p][t]
# For t=1, Inv[p][0] - Back[p][0] = 0 (initial state)

for p in P:
    for t in T:
        if t == 1:
            # Initial state is 0
            solver.Add(
                Inv[p, t] - Back[p, t] == 
                0 - 0 + x[p, t] - D[p][t]
            )
        else:
            solver.Add(
                Inv[p, t] - Back[p, t] == 
                Inv[p, t-1] - Back[p, t-1] + x[p, t] - D[p][t]
            )

# 4.4 Terminal Conditions
# End of Q4: Inv[p][4] = 150, Back[p][4] = 0
for p in P:
    solver.Add(Inv[p, 4] == I_final)
    solver.Add(Back[p, 4] == B_final)

# 5. Objective Function
# Minimize total cost: Sum(H[p] * Inv[p][t] + L[p] * Back[p][t])

obj = 0
for p in P:
    for t in T:
        obj += H[p] * Inv[p, t]
        obj += L[p] * Back[p, t]

solver.Minimize(obj)

# 6. Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")