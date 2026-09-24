from ortools.linear_solver import pywraplp

# Create the LP solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Define decision variables
x_A = solver.NumVar(0, solver.infinity(), 'x_A')
x_B = solver.NumVar(0, solver.infinity(), 'x_B')
x_C = solver.NumVar(0, solver.infinity(), 'x_C')
x_E = solver.NumVar(0, solver.infinity(), 'x_E')

# Objective function: Maximize Z = 0.05*x_A + 0.07*x_B + 0.10*x_C
obj = 0.05 * x_A + 0.07 * x_B + 0.10 * x_C
solver.Maximize(obj)

# Constraint 1: Minimum Investment in Product A
solver.Add(x_A >= 300)

# Constraint 2: Maximum Allocation per Product
solver.Add(x_A <= 350)
solver.Add(x_B <= 350)
solver.Add(x_C <= 350)

# Constraint 3: Emergency Reserve
solver.Add(x_E >= 100)

# Constraint 4: Total Fund Limitation (Equality)
solver.Add(x_A + x_B + x_C + x_E == 1000)

# Solve the model
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")