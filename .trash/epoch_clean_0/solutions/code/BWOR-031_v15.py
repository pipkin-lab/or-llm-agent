from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
L = 100
F = 15000
B_AW = 3500
B_SS = 4000
w_SS = 2.1
w_AW = 1.8

I_cow = 400
I_ch = 3
l_cow = 1.5

a_cow = 100
s_cow = 50
r_cow = 400

a_ch = 0.6
s_ch = 0.3
r_ch = 2

N_ch_max = 3000
N_cow_max = 32

a_soy = 20
s_soy = 50
r_soy = 175

a_corn = 35
s_corn = 75
r_corn = 300

a_wheat = 10
s_wheat = 40
r_wheat = 120

# Decision Variables
x_soy = solver.NumVar(0, solver.infinity(), 'x_soy')
x_corn = solver.NumVar(0, solver.infinity(), 'x_corn')
x_wheat = solver.NumVar(0, solver.infinity(), 'x_wheat')

N_cow = solver.IntVar(0, N_cow_max, 'N_cow')
N_ch = solver.IntVar(0, N_ch_max, 'N_ch')

u_AW = solver.NumVar(0, solver.infinity(), 'u_AW')
u_SS = solver.NumVar(0, solver.infinity(), 'u_SS')

# Objective Function
objective = (r_soy * x_soy + r_corn * x_corn + r_wheat * x_wheat +
             r_cow * N_cow + r_ch * N_ch +
             w_AW * u_AW + w_SS * u_SS)

solver.Maximize(objective)

# Constraints

# 1. Land Constraint
solver.Add(x_soy + x_corn + x_wheat + l_cow * N_cow <= L)

# 2. Fund Constraint
solver.Add(I_cow * N_cow + I_ch * N_ch <= F)

# 3. Autumn/Winter Labor Constraint
solver.Add(a_soy * x_soy + a_corn * x_corn + a_wheat * x_wheat +
           a_cow * N_cow + a_ch * N_ch + u_AW == B_AW)

# 4. Spring/Summer Labor Constraint
solver.Add(s_soy * x_soy + s_corn * x_corn + s_wheat * x_wheat +
           s_cow * N_cow + s_ch * N_ch + u_SS == B_SS)

# 5. Chicken House Capacity (already bounded in variable definition, but explicit for clarity)
solver.Add(N_ch <= N_ch_max)

# 6. Cow Shed Capacity (already bounded in variable definition, but explicit for clarity)
solver.Add(N_cow <= N_cow_max)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")