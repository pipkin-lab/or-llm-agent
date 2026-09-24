from ortools.linear_solver import pywraplp

# Define the solver
solver = pywraplp.Solver.CreateSolver('GLOP')
inf = solver.infinity()

# Parameters
D = [0, 3000, 3600, 4000, 4600, 4800, 5000]  # Demand for months 1-6 (index 0 unused for D, D[1] to D[6])
h_lab = 4.0
C_mat = 150.0
P_sell = 240.0
H_0 = 400.0
H_max_end = 100.0
H_hold = 10.0
W_0 = 80.0
H_work = 160.0
T_train = 50.0
C_skilled = 2000.0
C_trainee = 800.0
r_attr = 0.02

# Decision Variables
# x[t]: Production in month t
# H[t]: Ending inventory in month t
# N[t]: New hires (trainees) in month t
# W[t]: Skilled workers in month t
x = dict()
H = dict()
N = dict()
W = dict()

for t in range(1, 7):
    x[t] = solver.NumVar(0, inf, 'x_' + str(t))
    H[t] = solver.NumVar(0, inf, 'H_' + str(t))
    N[t] = solver.NumVar(0, inf, 'N_' + str(t))
    W[t] = solver.NumVar(0, inf, 'W_' + str(t))

# Objective Function
# Max Z = sum(90*x[t] - 2000*W[t] - 800*N[t] - 10*H[t])
objective_terms = []
for t in range(1, 7):
    objective_terms.append(90 * x[t] - 2000 * W[t] - 800 * N[t] - 10 * H[t])

solver.Maximize(sum(objective_terms))

# Constraints

# 1. Inventory Balance: H[t] = H[t-1] + x[t] - D[t]
# H_0 = 400
solver.Add(H[1] == H_0 + x[1] - D[1])
for t in range(2, 7):
    solver.Add(H[t] == H[t-1] + x[t] - D[t])

# 2. End-of-Year Inventory Limit: H[6] <= 100
solver.Add(H[6] <= H_max_end)

# 3. Workforce Balance
# W[1] = 80
solver.Add(W[1] == W_0)
# W[t+1] = 0.98 * W[t] + N[t] for t = 1..5
for t in range(1, 6):
    solver.Add(W[t+1] == (1 - r_attr) * W[t] + N[t])

# 4. Labor Capacity: 4*x[t] + 50*N[t] <= 160*W[t]
for t in range(1, 7):
    solver.Add(h_lab * x[t] + T_train * N[t] <= H_work * W[t])

# Solve the problem
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")