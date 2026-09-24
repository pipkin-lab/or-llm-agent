from ortools.linear_solver import pywraplp

# Parameters
products = [1, 2, 3]
stages = [1, 2, 3]

# Demand D[i, t]
D = dict()
D[1, 1] = 500
D[1, 2] = 680
D[1, 3] = 800
D[2, 1] = 750
D[2, 2] = 800
D[2, 3] = 950
D[3, 1] = 900
D[3, 2] = 800
D[3, 3] = 1000

# Equipment hours per unit a[i]
a = dict()
a[1] = 2.0
a[2] = 1.0
a[3] = 3.1

# Capital per unit b[i]
b = dict()
b[1] = 40
b[2] = 20
b[3] = 55

# Equipment capacity limit
K_eq = 5000

# Capital limit
K_cap = 93000

# Stockout weights w[i]
w = dict()
w[1] = 1
w[2] = 1
w[3] = 2


def build_solver():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    # Variables
    x = dict()
    I = dict()
    S = dict()
    O = dict()

    for i in products:
        for t in stages:
            x[i, t] = solver.IntVar(0, INF, 'x_' + str(i) + '_' + str(t))
            S[i, t] = solver.IntVar(0, INF, 'S_' + str(i) + '_' + str(t))
            if t < 3:
                I[i, t] = solver.IntVar(0, INF, 'I_' + str(i) + '_' + str(t))
    # I[i, 3] is forced to 0, so no variable needed.
    # But for constraint convenience, we can create it and fix to 0, or handle in constraint.
    # Let's create I for t=1,2 only, and treat I[i,3]=0 in constraints.
    # Actually, let's create I[i,t] for t in 1..3 but fix I[i,3]=0?
    # The model says I[i,3]=0.
    # Let's just not create I[i,3] as a variable and use 0 in constraints.
    # Or create it and add constraint I[i,3] == 0.
    # Let's create it for uniformity.
    for i in products:
        I[i, 3] = solver.IntVar(0, 0, 'I_' + str(i) + '_3')

    for t in stages:
        O[t] = solver.NumVar(0, INF, 'O_' + str(t))

    # Constraints
    # 1. Inventory Balance: x[i,t] + I[i,t-1] + S[i,t] = D[i,t] + I[i,t]
    for i in products:
        for t in stages:
            prev_inv = 0 if t == 1 else I[i, t - 1]
            solver.Add(x[i, t] + prev_inv + S[i, t] == D[i, t] + I[i, t])

    # 2. Equipment Capacity (Soft): sum a[i]*x[i,t] - K_eq <= O[t]
    for t in stages:
        hours = sum(a[i] * x[i, t] for i in products)
        solver.Add(hours - K_eq <= O[t])

    # 3. Working Capital (Hard): sum b[i]*x[i,t] <= K_cap
    for t in stages:
        solver.Add(sum(b[i] * x[i, t] for i in products) <= K_cap)

    return solver, x, I, S, O


# Phase 1: Minimize Weighted Stockouts
solver, x, I, S, O = build_solver()

obj1 = sum(w[i] * S[i, t] for i in products for t in stages)
solver.Minimize(obj1)

status = solver.Solve()
if status != pywraplp.Solver.OPTIMAL and status != pywraplp.Solver.FEASIBLE:
    print("NO_FEASIBLE_SOLUTION")
    exit(1)

z1_star = solver.Objective().Value()

# Phase 2: Minimize Overloading, subject to obj1 == z1_star
solver.Add(obj1 == z1_star)
obj2 = sum(O[t] for t in stages)
solver.Minimize(obj2)

status = solver.Solve()
if status != pywraplp.Solver.OPTIMAL and status != pywraplp.Solver.FEASIBLE:
    print("NO_FEASIBLE_SOLUTION")
    exit(1)

# The problem asks for the final solution.
# Usually, the "OPTIMAL_VALUE" in such multi-objective contexts might refer to the last objective or a combined view.
# However, the prompt says "print exactly one line: 'OPTIMAL_VALUE:' followed by the single numeric result the problem asks for."
# The problem statement doesn't explicitly ask for a single number, but the structure implies finding the optimal plan.
# In many OR-Tools conversion tasks, if it's multi-objective lexicographic, the final objective value of the last priority is often reported, or the primary one.
# Given the "Goal Programming" style, often the final "achievement" is what matters.
# Let's look at the instruction: "After the final phase, the script must print exactly one line: 'OPTIMAL_VALUE:' followed by the single numeric result the problem asks for."
# Since no specific final objective is defined as "THE" answer, and the problem is about finding the plan, typically the final objective value (Priority 2, since Priority 3 is a constraint) is a good candidate. Or perhaps the sum of penalties?
# Let's re-read: "Ensure that working capital usage does not exceed the limit." This is a hard constraint.
# So we have 2 objectives minimized lexicographically.
# I will print the value of the last minimized objective (Z2) as the final result, as it represents the final optimization step's outcome.
# Alternatively, if the user expects the total cost or something, it's ambiguous.
# However, standard practice for these conversions: if the problem is "solve the model", and the model has a final objective, print that.
# Let's print Z2 (min overload).

print("OPTIMAL_VALUE:", solver.Objective().Value())