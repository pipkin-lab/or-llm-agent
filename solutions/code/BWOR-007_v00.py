from ortools.linear_solver import pywraplp

# Define the solver for Linear Programming
solver = pywraplp.Solver.CreateSolver('GLOP')
if solver is None:
    raise ValueError("GLOP solver not available")

# Parameters
# Monthly net cash flows (in thousand yuan)
# The problem statement mentions a table but does not provide the specific values for c_t.
# Based on standard problems of this type, I will look for the specific values.
# Since the prompt says "Use ONLY parameter values explicitly present in the Math Model" and
# the model text says "given in the table" but the table is missing in the prompt text,
# I must check if there's any implicit data.
# Wait, looking closely at the prompt: "Let c_t be the net cash flow for month t (given in the table)."
# The table is NOT provided in the prompt text.
# However, often in these conversion tasks, if the data is missing, I should raise an error
# OR, if this is a known problem instance, I might need to infer.
# BUT, the instructions say: "If a value is marked [NOT_PROVIDED] or is absent, do NOT substitute a guess.
# Instead, raise a runtime error with a clear message".

# Let's re-read carefully. Is there any hidden data? No.
# Therefore, I must raise a ValueError.

raise ValueError("Parameter c_t (monthly net cash flows) not provided in model")