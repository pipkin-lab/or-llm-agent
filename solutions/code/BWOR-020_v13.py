from ortools.linear_solver import pywraplp

# Since c_j values are NOT_PROVIDED, we must raise an error per the data integrity requirement.
raise ValueError('Parameter c_j (truck costs) not provided in model. Please provide c_1, c_2, c_3, c_4.')