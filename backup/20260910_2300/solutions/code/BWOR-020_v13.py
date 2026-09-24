from ortools.linear_solver import pywraplp

# Parameters
K = ['A', 'B', 'C', 'D', 'E']
J = [1, 2, 3, 4]

d = dict()
d['A'] = 1
d['B'] = 2
d['C'] = 3
d['D'] = 4
d['E'] = 8

C = dict()
C[1] = 2
C[2] = 6
C[3] = 8
C[4] = 11

# Cost c_j is NOT_PROVIDED, so we must raise an error
raise ValueError('Parameter c_j not provided in model')