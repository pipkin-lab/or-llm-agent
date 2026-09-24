from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision Variables
x = dict()
# Stage A
x['A1_1'] = solver.NumVar(0, INF, 'x_A1_1')
x['A1_2'] = solver.NumVar(0, INF, 'x_A1_2')
x['A2_1'] = solver.NumVar(0, INF, 'x_A2_1')
x['A2_2'] = solver.NumVar(0, INF, 'x_A2_2')
x['A2_3'] = solver.NumVar(0, INF, 'x_A2_3')
# Stage B
x['B1_1'] = solver.NumVar(0, INF, 'x_B1_1')
x['B1_2'] = solver.NumVar(0, INF, 'x_B1_2')
x['B2_1'] = solver.NumVar(0, INF, 'x_B2_1')
x['B2_3'] = solver.NumVar(0, INF, 'x_B2_3')
x['B3_1'] = solver.NumVar(0, INF, 'x_B3_1')

# Parameters
p_price = {1: 1.25, 2: 2.00, 3: 2.80}
r_cost = {1: 0.25, 2: 0.35, 3: 0.50}

# Processing times (minutes)
t_A1 = {1: 5, 2: 10}
t_A2 = {1: 7, 2: 9, 3: 12}
t_B1 = {1: 6, 2: 8}
t_B2 = {1: 4, 3: 11}
t_B3 = {1: 7}

# Machine costs (yuan/hour)
c_A1 = 0.05
c_A2 = 0.03
c_B1 = 0.06
c_B2 = 0.11
c_B3 = 0.05

# Machine capacities (minutes)
H_A1 = 6000 * 60
H_A2 = 10000 * 60
H_B1 = 4000 * 60
H_B2 = 7000 * 60
H_B3 = 4000 * 60

# Objective Function
# Maximize Z = sum_p (p_p - r_p) * Q_p - sum_m (c_m/60) * sum_p t_m_p * x_m_p
# Q_p = sum of Stage A variables for product p
# Q1 = x_A1_1 + x_A2_1
# Q2 = x_A1_2 + x_A2_2
# Q3 = x_A2_3

# Revenue - Raw Material Cost terms
obj = 0
obj += (p_price[1] - r_cost[1]) * (x['A1_1'] + x['A2_1'])
obj += (p_price[2] - r_cost[2]) * (x['A1_2'] + x['A2_2'])
obj += (p_price[3] - r_cost[3]) * (x['A2_3'])

# Processing Cost terms (subtract cost)
# Stage A
obj -= (c_A1 / 60) * (t_A1[1] * x['A1_1'] + t_A1[2] * x['A1_2'])
obj -= (c_A2 / 60) * (t_A2[1] * x['A2_1'] + t_A2[2] * x['A2_2'] + t_A2[3] * x['A2_3'])
# Stage B
obj -= (c_B1 / 60) * (t_B1[1] * x['B1_1'] + t_B1[2] * x['B1_2'])
obj -= (c_B2 / 60) * (t_B2[1] * x['B2_1'] + t_B2[3] * x['B2_3'])
obj -= (c_B3 / 60) * (t_B3[1] * x['B3_1'])

solver.Maximize(obj)

# Flow Balance Constraints
# Product 1: A1_1 + A2_1 = B1_1 + B2_1 + B3_1
solver.Add(x['A1_1'] + x['A2_1'] == x['B1_1'] + x['B2_1'] + x['B3_1'])
# Product 2: A1_2 + A2_2 = B1_2
solver.Add(x['A1_2'] + x['A2_2'] == x['B1_2'])
# Product 3: A2_3 = B2_3
solver.Add(x['A2_3'] == x['B2_3'])

# Capacity Constraints
# A1: 5*x_A1_1 + 10*x_A1_2 <= 360000
solver.Add(5 * x['A1_1'] + 10 * x['A1_2'] <= H_A1)
# A2: 7*x_A2_1 + 9*x_A2_2 + 12*x_A2_3 <= 600000
solver.Add(7 * x['A2_1'] + 9 * x['A2_2'] + 12 * x['A2_3'] <= H_A2)
# B1: 6*x_B1_1 + 8*x_B1_2 <= 240000
solver.Add(6 * x['B1_1'] + 8 * x['B1_2'] <= H_B1)
# B2: 4*x_B2_1 + 11*x_B2_3 <= 420000
solver.Add(4 * x['B2_1'] + 11 * x['B2_3'] <= H_B2)
# B3: 7*x_B3_1 <= 240000
solver.Add(7 * x['B3_1'] <= H_B3)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")