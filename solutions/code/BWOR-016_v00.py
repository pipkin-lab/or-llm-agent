from ortools.linear_solver import pywraplp

# Define the solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets
factories = [1, 2, 3, 4]
locations = [1, 2, 3, 4]
new_factories = [3, 4]

# Parameters
F = {3: 1200, 4: 1500}

# Transportation costs c_ij (from the problem, these are not explicitly given in the prompt)
# Since they are not provided, we raise an error as per data integrity requirements.
# However, looking at the prompt again, it says "c_ij is the unit transportation cost"
# but does not provide the actual values. Let me re-read...
# The prompt says "Use ONLY parameter values explicitly present in the Math Model."
# The transportation costs c_ij are NOT provided in the math model.
# I need to raise a ValueError.

raise ValueError('Transportation cost coefficients c_ij not provided in model')