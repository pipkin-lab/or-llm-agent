from ortools.linear_solver import pywraplp

# Parameters
customers = ['A', 'B', 'C', 'D', 'E']
trucks = [1, 2, 3, 4]

demand = dict()
demand['A'] = 1
demand['B'] = 2
demand['C'] = 3
demand['D'] = 4
demand['E'] = 8

capacity = dict()
capacity[1] = 2
capacity[2] = 6
capacity[3] = 8
capacity[4] = 11

# Cost c_j is not provided in the model, so we raise an error as per requirements
# However, looking at the problem, it says "c_j for using Truck j" but doesn't give values.
# Wait, the prompt says "Use ONLY parameter values explicitly present in the Math Model."
# The cost values are NOT explicitly provided as numbers.
# "Costs: c_j for using Truck j (where j in {1, 2, 3, 4})."
# There are no specific numbers for c_1, c_2, c_3, c_4.
# Therefore, I must raise a ValueError.

raise ValueError('Parameter c_j (trucks costs) not provided in model')