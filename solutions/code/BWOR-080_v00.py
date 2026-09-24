from ortools.linear_solver import pywraplp

# Parameters
P = [100, 60, 80, 40, 110, 90, 30]

# Demand matrix D[i][t] where i is 0-indexed product, t is 0-indexed month
# Table C-4 (assuming standard values if not explicitly listed, but the prompt says "from Table C-4")
# Since the prompt says "Use ONLY parameter values explicitly present in the Math Model" and 
# "If a value is marked [NOT_PROVIDED] or is absent, do NOT substitute a guess", 
# BUT the prompt DOES provide the structure and says "D (Demand Matrix 7x6 from Table C-4)".
# Looking closely at the prompt, it says "Summary of Data Parameters for Implementation" 
# but does NOT explicitly list the numeric values for D or A in the text provided.
# However, in typical OR-Tools conversion tasks of this format, if the table is referenced but not 
# fully transcribed in the text, I must check if I can infer or if I should raise an error.
# The prompt says: "Use ONLY parameter values explicitly present in the Math Model."
# The Math Model text says: "D (Demand Matrix 7x6 from Table C-4)" and "A (Machine Hours Matrix 5x7 from Table C-3)".
# It does NOT provide the actual numbers for D and A in the text body, only the structure.
# Wait, let me re-read carefully.
# "Where: Profit_i is the unit profit... P1=100..." -> P is provided.
# "D (Demand Matrix 7x6 from Table C-4)" -> Values NOT provided in text.
# "A (Machine Hours Matrix 5x7 from Table C-3)" -> Values NOT provided in text.
#
# If I cannot find the values, I must raise a ValueError.
# However, often in these prompts, the "Table C-3" and "Table C-4" data might be implied or I might have missed it.
# Let's look at the example:
# "Example (Grinding, Jan): ... 0.5 x_{1,1} + 0.7 x_{2,1} + 0.3 x_{5,1} + 0.2 x_{6,1} + 0.5 x_{7,1}"
# This gives partial A values for Grinding (Row 1 of A, 0-indexed Row 0):
# Product 1 (idx 0): 0.5
# Product 2 (idx 1): 0.7
# Product 5 (idx 4): 0.3
# Product 6 (idx 5): 0.2
# Product 7 (idx 6): 0.5
# Products 3 (idx 2) and 4 (idx 3) are 0 for Grinding.
#
# But I don't have the rest of A or D.
# The instructions say: "If a value is marked [NOT_PROVIDED] or is absent, do NOT substitute a guess. Instead, raise a runtime error..."
#
# However, looking at the very beginning of the prompt, it says "Convert this mathematical model...".
# Usually, if the data is missing, the script should fail gracefully.
# BUT, sometimes the user provides the data in the "Summary" section implicitly or I should check if there is a standard dataset this refers to.
# Given the strict instruction "Use ONLY parameter values explicitly present", and D and A are referenced but not numerically defined in the text block provided, I must raise an error.
#
# WAIT. Let me double check the prompt text again.
# "Summary of Data Parameters for Implementation"
# "P = [100, 60, 80, 40, 110, 90, 30]" -> Provided.
# "D (Demand Matrix 7x6 from Table C-4)" -> Not provided numerically.
# "A (Machine Hours Matrix 5x7 from Table C-3)" -> Not provided numerically (only one example row partially).
#
# Therefore, I will raise a ValueError indicating that D and A are missing.
#
# HOWEVER, in many similar tasks, the "Table C-3" and "Table C-4" are standard or the user expects me to know them or they were in a previous part of the context.
# Since I am an agent and must produce executable code, and the prompt says "If a value is... absent... raise a runtime error", I will do so.
#
# BUT, let's look at the "Example" again. It gives specific coefficients.
# If I raise an error, the code is technically correct per instructions.
# Let's assume the user *intended* to provide the tables but the prompt text only contains the model description.
#
# Actually, looking at the pattern of such prompts, often the "Table C-3" and "Table C-4" data is standard for a specific textbook problem (e.g., Hillier & Lieberman).
# If I search my internal knowledge for "Production and Inventory Planning Model 7 products 6 months 5 machines", this looks like a classic LP problem.
#
# Let's try to find the data.
# Problem: 7 products, 6 months.
# If I cannot be 100% sure of the numbers, I must raise an error.
#
# Let's re-read the prompt's "DATA INTEGRITY" rule: "Use ONLY parameter values explicitly present in the Math Model. FORBIDDEN: Inventing... If a value is... absent... raise a runtime error".
#
# The values for D and A are NOT explicitly present in the text.
# Therefore, the correct action is to raise a ValueError.
#
# However, if I just raise an error, is that the best help?
# The prompt asks to "Convert this mathematical model into... Python code".
# If the data is missing, I cannot solve it.
#
# Let's check if I missed any numbers.
# "P = [100, 60, 80, 40, 110, 90, 30]"
# "M = [4, 2, 3, 1, 1]"
# "O = [[1,0,0,0,1,0], ...]"
# "Storage cost = 5"
# "Final inventory = 50"
# "Max inventory = 100"
#
# Missing: D (7x6), A (5x7).
#
# I will write the code structure but raise an error at the point where D and A would be defined, with a clear message.
#
# Wait, is it possible the "Table C-3" and "Table C-4" are provided in the "Math Model" section implicitly?
# No, they are referenced as "from Table C-4" and "from Table C-3".
#
# I will produce the code that raises the error.
#
# One more check: Did the user provide the tables in the "Example" section fully?
# "Example (Grinding, Jan): 0.5 x_{1,1} + 0.7 x_{2,1} + 0.3 x_{5,1} + 0.2 x_{6,1} + 0.5 x_{7,1}"
# This is just one constraint.
#
# Okay, I will raise a ValueError.
#
# Code Structure:
# 1. Define known parameters.
# 2. Check for D and A. Since they are missing, raise ValueError.
# 3. If they were present, build the model.
#
# To be most helpful, I will define the variables D and A as None and check them.
#
# Actually, let's look at the instruction again.
# "If a value is marked [NOT_PROVIDED] or is absent, do NOT substitute a guess. Instead, raise a runtime error with a clear message"
#
# I will implement the solver logic but insert the check immediately after defining the known parameters.
#
# However, if I can't provide the data, the script is useless.
# Is there any chance the prompt *is* the entire context and I'm expected to know the tables?
# No, "Use ONLY parameter values explicitly present".
#
# I will write the script to raise the error.

# Known Parameters
P = [100, 60, 80, 40, 110, 90, 30]
M = [4, 2, 3, 1, 1]
O = [
    [1, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 1, 0],
    [0, 2, 0, 0, 0, 1],
    [0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1]
]
STORAGE_COST = 5
FINAL_INV = 50
MAX_INV = 100
NUM_PRODUCTS = 7
NUM_MONTHS = 6
NUM_EQUIPMENT = 5
BASE_HOURS = 384

# Missing Parameters
# D: 7x6 Demand Matrix
# A: 5x7 Machine Hours Matrix

raise ValueError("Parameters D (Demand Matrix) and A (Machine Hours Matrix) are not provided in the model description. Please provide the numeric values for Table C-3 and Table C-4.")

# The rest of the code would follow if data were present.
# Since I must output executable code, and it will crash, I should ensure the crash is the intended behavior.
# But wait, if I just raise the error, the code is very short.
# Is it better to provide the full code structure with the error at the top?
# Yes.

# Alternative: Maybe the user *did* provide the data and I missed it?
# "Table C-3" usually contains: Product, Profit, and Machine Hours.
# "Table C-4" contains: Product, Month 1-6 Demand.
# The prompt text does not contain these numbers.
#
# I will proceed with the ValueError.

# To make the code "clean" and "self-contained" as requested, I will structure it properly.
# However, since it fails immediately, I'll just put the raise statement.
# But the prompt asks for "Convert... into... Python code".
# If I just raise an error, is that a conversion?
# It is a valid Python script that correctly identifies the missing data.
#
# Let's double check if I should try to reconstruct the tables from common problems.
# No, "FORBIDDEN: Inventing...".
#
# Final decision: Raise ValueError.

# To satisfy the "executable code" requirement, the script will run and then raise the error.
# This is the most honest and compliant response.

# I will wrap it in a main function or just script it.
# The prompt says "The first line inside the code block MUST be a valid Python statement".
# `raise` is a valid statement.
# But it's better to define the constants first, then raise.

# Let's write the full code structure that *would* work, but with the raise.

from ortools.linear_solver import pywraplp

# Parameters
P = [100, 60, 80, 40, 110, 90, 30]
M = [4, 2, 3, 1, 1]
O = [
    [1, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 1, 0],
    [0, 2, 0, 0, 0, 1],
    [0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1]
]
STORAGE_COST = 5
FINAL_INV = 50
MAX_INV = 100
NUM_PRODUCTS = 7
NUM_MONTHS = 6
NUM_EQUIPMENT = 5
BASE_HOURS = 384

# Check for missing data
# D and A are required but not provided in the text.
if True:
    raise ValueError("Parameters D (Demand Matrix) and A (Machine Hours Matrix) are not provided in the model description. Please provide the numeric values for Table C-3 and Table C-4.")

# If data were provided, the code would continue here:
# solver = pywraplp.Solver.CreateSolver('GLOP')
# INF = solver.infinity()
#
# x = dict()
# I = dict()
# S = dict()
#
# for i in range(NUM_PRODUCTS):
#     for t in range(NUM_MONTHS):
#         x[i, t] = solver.NumVar(0, INF, f'x_{i}_{t}')
#         I[i, t] = solver.NumVar(0, MAX_INV, f'I_{i}_{t}')
#         S[i, t] = solver.NumVar(0, D[i][t], f'S_{i}_{t}')
#
# # Objective
# objective = 0
# for i in range(NUM_PRODUCTS):
#     for t in range(NUM_MONTHS):
#         objective += P[i] * S[i, t] - STORAGE_COST * I[i, t]
# solver.Maximize(objective)
#
# # Constraints
# for i in range(NUM_PRODUCTS):
#     for t in range(NUM_MONTHS):
#         # Inventory Balance
#         if t == 0:
#             solver.Add(I[i, t] == x[i, t] - S[i, t])
#         else:
#             solver.Add(I[i, t] == I[i, t-1] + x[i, t] - S[i, t])
#         
#         # Final Inventory
#         if t == NUM_MONTHS - 1:
#             solver.Add(I[i, t] == FINAL_INV)
#
#     # Demand Limit is handled by S upper bound
#
# for t in range(NUM_MONTHS):
#     for k in range(NUM_EQUIPMENT):
#         capacity = (M[k] - O[k][t]) * BASE_HOURS
#         constraint = 0
#         for i in range(NUM_PRODUCTS):
#             constraint += A[k][i] * x[i, t]
#         solver.Add(constraint <= capacity)
#
# status = solver.Solve()
# if status == pywraplp.Solver.OPTIMAL:
#     print("OPTIMAL_VALUE:", solver.Objective().Value())
# else:
#     print("NO_FEASIBLE_SOLUTION")