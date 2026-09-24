from ortools.linear_solver import pywraplp

# Profit lookup tables
# r1[x][y] for Department 1
r1 = dict()
r1[(0,0)] = 0
r1[(0,1)] = 0
r1[(0,2)] = 0
r1[(0,3)] = 0
r1[(1,0)] = 0
r1[(1,1)] = 0
r1[(1,2)] = 0
r1[(1,3)] = 0
r1[(2,0)] = 0
r1[(2,1)] = 0
r1[(2,2)] = 0
r1[(2,3)] = 0
r1[(3,0)] = 0
r1[(3,1)] = 0
r1[(3,2)] = 0
r1[(3,3)] = 0

# r2[x][y] for Department 2
r2 = dict()
r2[(0,0)] = 0
r2[(0,1)] = 0
r2[(0,2)] = 0
r2[(0,3)] = 0
r2[(1,0)] = 0
r2[(1,1)] = 0
r2[(1,2)] = 0
r2[(1,3)] = 0
r2[(2,0)] = 0
r2[(2,1)] = 0
r2[(2,2)] = 0
r2[(2,3)] = 0
r2[(3,0)] = 0
r2[(3,1)] = 0
r2[(3,2)] = 0
r2[(3,3)] = 0

# r3[x][y] for Department 3
r3 = dict()
r3[(0,0)] = 0
r3[(0,1)] = 0
r3[(0,2)] = 0
r3[(0,3)] = 0
r3[(1,0)] = 0
r3[(1,1)] = 0
r3[(1,2)] = 0
r3[(1,3)] = 0
r3[(2,0)] = 0
r3[(2,1)] = 0
r3[(2,2)] = 0
r3[(2,3)] = 0
r3[(3,0)] = 0
r3[(3,1)] = 0
r3[(3,2)] = 0
r3[(3,3)] = 0

# Since the actual profit values from Table 7-3 are not provided in the model,
# we raise an error as per the data integrity requirement.
raise ValueError("Profit lookup table values (r1, r2, r3) not provided in model")