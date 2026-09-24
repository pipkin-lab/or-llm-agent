from ortools.linear_solver import pywraplp

# Parameter data
# Jobs are 1-indexed: 1..12
# p[j][0] = processing time on Machine A, p[j][1] = processing time on Machine B
p = dict()
p[1] = (5, 5)
p[2] = (8, 9)
p[3] = (11, 4)
p[4] = (2, 3)
p[5] = (7, 7)
p[6] = (6, 9)
p[7] = (3, 5)
p[8] = (9, 4)
p[9] = (8, 9)
p[10] = (3, 5)
p[11] = (6, 3)
p[12] = (10, 4)

jobs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
n = len(jobs)

# Big-M values
M_A = sum(p[j][0] for j in jobs)
M_B = sum(p[j][1] for j in jobs)

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
# x[j, l]: binary, 1 if job j is before job l in the sequence (j < l in index)
# We only define x[j, l] for j < l to avoid redundancy, and enforce x[j,l] + x[l,j] = 1
# But OR-Tools needs variables. Let's define x for all pairs j != l or just j < l?
# The model says: x[j,l] + x[l,j] = 1 for j < l.
# So we define x[j,l] for j < l.
x = dict()
for j in jobs:
    for l in jobs:
        if j < l:
            x[j, l] = solver.BoolVar('x_' + str(j) + '_' + str(l))

# S[j, 0]: start time of job j on Machine A
# S[j, 1]: start time of job j on Machine B
S = dict()
for j in jobs:
    S[j, 0] = solver.NumVar(0, INF, 'S_' + str(j) + '_A')
    S[j, 1] = solver.NumVar(0, INF, 'S_' + str(j) + '_B')

# Z: makespan
Z = solver.NumVar(0, INF, 'Z')

# Objective: Minimize Z
solver.Minimize(Z)

# Constraints:
# 1. Flow Constraint: S[j, B] >= S[j, A] + p[j, A]
for j in jobs:
    solver.Add(S[j, 1] >= S[j, 0] + p[j][0])

# 2. Objective link: Z >= S[j, B] + p[j, B]
for j in jobs:
    solver.Add(Z >= S[j, 1] + p[j][1])

# 3 & 4. Precedence on Machine A
# For j < l:
# If x[j,l] = 1 (j before l): S[j,A] + p[j,A] <= S[l,A]  => S[j,A] - S[l,A] <= -p[j,A] (Wait, standard form is S[j] - S[l] <= M(1-x) - p_j? No.)
# Let's re-read the model provided in the prompt carefully.
# Prompt Model:
# S[j,A] - S[l,A] <= M_A (1 - x[j,l])
# S[l,A] - S[j,A] <= M_A (1 - x[l,j])
# Note: Since x[l,j] is not defined in my x dict (only j<l), I need to be careful.
# If I define x[j,l] for j<l, then for the pair (j,l) where j<l:
# Constraint 1: S[j,A] - S[l,A] <= M_A (1 - x[j,l])
# Constraint 2: S[l,A] - S[j,A] <= M_A (1 - (1 - x[j,l])) = M_A * x[j,l]
# This works because if x[j,l]=1 (j before l), C1: S[j]-S[l] <= 0 (S[j]<=S[l]), C2: S[l]-S[j] <= M (loose).
# If x[j,l]=0 (l before j), C1: S[j]-S[l] <= M (loose), C2: S[l]-S[j] <= 0 (S[l]<=S[j]).
# This correctly enforces non-overlap?
# Wait, non-overlap means S[j] + p[j] <= S[l] OR S[l] + p[l] <= S[j].
# The constraints in the prompt are:
# S[j,A] - S[l,A] <= M_A (1 - x[j,l])  --> S[j] <= S[l] + M(1-x)
# S[l,A] - S[j,A] <= M_A (1 - x[l,j])  --> S[l] <= S[j] + M(1-x[l,j])
# This formulation in the prompt text seems to be missing the processing time p in the Big-M constraint logic for *ordering*?
# Standard Big-M for ordering:
# If x[j,l]=1 (j before l): S[l] >= S[j] + p[j]  => S[j] - S[l] <= -p[j]
# If x[j,l]=0 (l before j): S[j] >= S[l] + p[l]  => S[l] - S[j] <= -p[l]
# The prompt's constraints are:
# S[j] - S[l] <= M(1-x)
# S[l] - S[j] <= M(1-x[l,j])
# If x=1: S[j] - S[l] <= 0 => S[j] <= S[l]. This allows S[j] and S[l] to be equal or S[l] slightly larger. It does NOT enforce S[l] >= S[j] + p[j].
# Therefore, the constraints as written in the prompt text might be insufficient to prevent overlap unless interpreted differently or if I add the processing time.
# HOWEVER, the prompt explicitly says: "Convert this mathematical model...".
# Let's look at the "Summary of the Model to be Solved" section.
# 3. S[j,A] - S[l,A] <= 78 (1 - x[j,l])
# 4. S[l,A] - S[j,A] <= 78 (1 - x[l,j])
# These constraints ONLY enforce that the start times are ordered (non-negative difference bounded by M). They do NOT enforce the gap of p[j].
# If S[j]=0, S[l]=0, x[j,l]=1. C3: 0 <= 78. C4: 0 <= 0 (since 1-x[l,j] = 1-x[j,l] = 0? No, x[l,j] is the variable for the pair. If j<l, x[l,j] is not defined. The constraint says x[l,j]. In the loop j<l, x[l,j] is the complement.
# If the model provided is flawed/incomplete regarding the processing time gap, I should probably implement the *correct* flow shop MILP which is standard, OR strictly follow the prompt's equations.
# But wait, if I strictly follow S[j] - S[l] <= M(1-x), it allows overlap.
# Let's re-read the "Operational Constraints" section A.
# "If x_{j,l}=1 (job j before job l), then: 1. Job j must complete on Machine A before Job l starts on Machine A."
# This implies S[l] >= S[j] + p[j].
# The Big-M formulation for S[l] >= S[j] + p[j] is:
# S[l] - S[j] >= p[j] - M(1-x[j,l])  =>  S[j] - S[l] <= -p[j] + M(1-x[j,l])
# The prompt's summary says: S[j,A] - S[l,A] <= 78 (1 - x[j,l]). It is missing the -p[j] term.
# Is it possible the prompt implies S is completion time? No, it says Start Time.
# If I implement the prompt's exact equations, the solver might find a solution with overlapping jobs, which is infeasible for a flow shop.
# However, usually in these tasks, if the model description is slightly off but the intent is clear ("Two-Machine Flow Shop Scheduling"), I should implement the *correct* model that solves the problem described.
# BUT, the instruction says "Convert this mathematical model".
# Let's look at the Johnson's Rule verification. The optimal makespan is 81.
# If I use the correct Big-M constraints:
# For j < l:
# S[l] - S[j] >= p[j] - M_A (1 - x[j,l])  => S[j] - S[l] <= -p[j] + M_A (1 - x[j,l])
# S[j] - S[l] >= p[l] - M_A (1 - x[l,j])  => S[l] - S[j] <= -p[l] + M_A (1 - x[l,j])
# Since x[l,j] = 1 - x[j,l]:
# S[l] - S[j] <= -p[l] + M_A x[j,l]
#
# Let's check if the prompt's simplified constraints *accidentally* work or if I should fix them.
# Given the explicit "Summary of the Model to be Solved" lists the equations without p, but the text above explains the logic "Job j must complete... before Job l starts", I will implement the **correct** constraints that enforce the completion time gap, as that is the standard and correct MILP for Flow Shop. The prompt's equations in the summary are likely a simplification error in the prompt generation. The goal is to solve the "Two-Machine Flow Shop Scheduling" problem.
#
# Actually, let's look closer. If I use the prompt's exact constraints:
# S[j] - S[l] <= M(1-x)
# S[l] - S[j] <= M*x  (assuming x[l,j] = 1-x[j,l])
# This just says |S[j] - S[l]| <= M. It doesn't enforce order with duration.
# I will implement the standard correct constraints:
# 1. S[l] >= S[j] + p[j] - M(1-x[j,l])
# 2. S[j] >= S[l] + p[l] - M(1-x[l,j])  => S[j] >= S[l] + p[l] - M*x[j,l]
#
# Let's refine the constraints for Machine A (index 0):
# For j < l:
# solver.Add(S[l, 0] >= S[j, 0] + p[j][0] - M_A * (1 - x[j, l]))
# solver.Add(S[j, 0] >= S[l, 0] + p[l][0] - M_A * (1 - (1 - x[j, l]))) # 1 - x[l,j] is x[j,l] since x[l,j] = 1 - x[j,l]
# So: S[j, 0] >= S[l, 0] + p[l][0] - M_A * x[j, l]

# Let's refine the constraints for Machine B (index 1):
# For j < l:
# solver.Add(S[l, 1] >= S[j, 1] + p[j][1] - M_B * (1 - x[j, l]))
# solver.Add(S[j, 1] >= S[l, 1] + p[l][1] - M_B * x[j, l])

# Let's double check the variable definition.
# x[j, l] is defined for j < l.
# x[j, l] = 1 means j before l.
# x[l, j] is not a variable. The condition "l before j" corresponds to x[j, l] = 0.

# Implementation of Correct Big-M Constraints:

# Machine A
for j in jobs:
    for l in jobs:
        if j < l:
            # If x[j,l] = 1, then S[l] >= S[j] + p[j]
            # S[l] - S[j] >= p[j] - M_A(1 - x[j,l])
            solver.Add(S[l, 0] - S[j, 0] >= p[j][0] - M_A * (1 - x[j, l]))
            
            # If x[j,l] = 0, then S[j] >= S[l] + p[l]
            # S[j] - S[l] >= p[l] - M_A(1 - x[l,j])
            # Since x[l,j] is not a var, we use the fact that if x[j,l]=0, then effectively "l before j" is true.
            # The constraint for "l before j" is S[j] >= S[l] + p[l].
            # We can write this as: S[j] - S[l] >= p[l] - M_A * (1 - (1 - x[j,l])) = p[l] - M_A * x[j,l]
            solver.Add(S[j, 0] - S[l, 0] >= p[l][0] - M_A * x[j, l])

# Machine B
for j in jobs:
    for l in jobs:
        if j < l:
            # If x[j,l] = 1, then S[l] >= S[j] + p[j]
            solver.Add(S[l, 1] - S[j, 1] >= p[j][1] - M_B * (1 - x[j, l]))
            
            # If x[j,l] = 0, then S[j] >= S[l] + p[l]
            solver.Add(S[j, 1] - S[l, 1] >= p[l][1] - M_B * x[j, l])

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")