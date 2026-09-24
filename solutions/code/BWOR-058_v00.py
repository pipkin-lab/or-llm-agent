from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
x = dict()
x[1] = solver.IntVar(1, 3, 'x_1')  # Jewelry
x[2] = solver.IntVar(1, 2, 'x_2')  # Shoes & Hats
x[3] = solver.IntVar(1, 3, 'x_3')  # Department Store
x[4] = solver.IntIntVar = None  # placeholder, will overwrite
x[4] = solver.IntVar(0, 2, 'x_4')  # Bookstore
x[5] = solver.IntVar(1, 3, 'x_5')  # Catering

# Binary variables y[i, k]: 1 if x_i == k
y = dict()
# i=1: k in {1,2,3}
for k in [1, 2, 3]:
    y[1, k] = solver.BoolVar('y_1_' + str(k))
# i=2: k in {1,2}
for k in [1, 2]:
    y[2, k] = solver.BoolVar('y_2_' + str(k))
# i=3: k in {1,2,3}
for k in [1, 2, 3]:
    y[3, k] = solver.BoolVar('y_3_' + str(k))
# i=4: k in {0,1,2}
for k in [0, 1, 2]:
    y[4, k] = solver.BoolVar('y_4_' + str(k))
# i=5: k in {1,2,3}
for k in [1, 2, 3]:
    y[5, k] = solver.BoolVar('y_5_' + str(k))

# Link x_i to y[i,k]: x_i = sum_k k * y[i,k]
solver.Add(x[1] == 1 * y[1, 1] + 2 * y[1, 2] + 3 * y[1, 3])
solver.Add(x[2] == 1 * y[2, 1] + 2 * y[2, 2])
solver.Add(x[3] == 1 * y[3, 1] + 2 * y[3, 2] + 3 * y[3, 3])
solver.Add(x[4] == 0 * y[4, 0] + 1 * y[4, 1] + 2 * y[4, 2])
solver.Add(x[5] == 1 * y[5, 1] + 2 * y[5, 2] + 3 * y[5, 3])

# Each y[i,k] sum to 1 (exactly one k chosen per i)
solver.Add(y[1, 1] + y[1, 2] + y[1, 3] == 1)
solver.Add(y[2, 1] + y[2, 2] == 1)
solver.Add(y[3, 1] + y[3, 2] + y[3, 3] == 1)
solver.Add(y[4, 0] + y[4, 1] + y[4, 2] == 1)
solver.Add(y[5, 1] + y[5, 2] + y[5, 3] == 1)

# Area constraint
solver.Add(250 * x[1] + 350 * x[2] + 800 * x[3] + 400 * x[4] + 500 * x[5] <= 5000)

# Objective: Maximize total rent income
# Rent income = sum over i of (sum over k of R[i,k] * y[i,k])
# Because x_i * R[i, x_i] = sum_k k * R[i,k] * y[i,k] ... 
# Actually, rent income is x_i * R[i, x_i]. If x_i = k, then rent = k * R[i,k].
# So objective = sum_i sum_k k * R[i,k] * y[i,k]

# R values (rent per store at quantity k):
# i=1: R[1,1]=1.8, R[1,2]=1.6, R[1,3]=1.4
# i=2: R[2,1]=2.0, R[2,2]=1.8
# i=3: R[3,1]=5.4, R[3,2]=4.2, R[3,3]=4.0
# i=4: R[4,0]=0 (no store, no rent), R[4,1]=3.2, R[4,2]=2.0
# i=5: R[5,1]=3.4, R[5,2]=3.0, R[5,3]=2.4

obj_terms = []
obj_terms.append(1 * 1.8 * y[1, 1] + 2 * 1.6 * y[1, 2] + 3 * 1.4 * y[1, 3])
obj_terms.append(1 * 2.0 * y[2, 1] + 2 * 1.8 * y[2, 2])
obj_terms.append(1 * 5.4 * y[3, 1] + 2 * 4.2 * y[3, 2] + 3 * 4.0 * y[3, 3])
obj_terms.append(0 * 0.0 * y[4, 0] + 1 * 3.2 * y[4, 1] + 2 * 2.0 * y[4, 2])
obj_terms.append(1 * 3.4 * y[5, 1] + 2 * 3.0 * y[5, 2] + 3 * 2.4 * y[5, 3])

objective = sum(obj_terms)
solver.Maximize(objective)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")