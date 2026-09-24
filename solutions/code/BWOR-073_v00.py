import numpy as np

# Cost table: C[i][x] where i is warehouse (1-4), x is units (2-4)
# Using 1-indexed for warehouses, and 2-4 for units
C = {
    1: {2: 18, 3: 16, 4: 12},
    2: {2: 38, 3: 36, 4: 30},
    3: {2: 14, 3: 12, 4: 11},
    4: {2: 34, 3: 31, 4: 25}
}

# f[s][k] = minimum expected accidents for warehouses s through 4 given k units
# s ranges from 1 to 5 (5 is boundary), k ranges from 0 to 12
INF = float('inf')

# Initialize f as a 2D list: f[s][k]
# s: 1..5, k: 0..12
f = [[0] * 13 for _ in range(6)]  # index 0 unused for s, index 0..12 for k
# argmin_x[s][k] = optimal x_s to use at stage s with k units
argmin_x = [[0] * 13 for _ in range(6)]

# Boundary condition: f_5(k) = 0 for all valid k
# Already initialized to 0

# Backward pass: s = 4, 3, 2, 1
for s in range(4, 0, -1):
    for k in range(13):
        # Determine valid range for x_s
        # x_s in {2, 3, 4}
        # k - x_s >= 2 * (5 - s)  =>  enough for remaining warehouses (s+1 to 4)
        # k - x_s <= 4 * (5 - s)  =>  not exceeding max capacity of remaining
        # Also k - x_s >= 0
        best_val = INF
        best_x = -1
        for x in [2, 3, 4]:
            remaining = k - x
            # Check remaining units are valid for warehouses s+1 to 4
            num_remaining_warehouses = 5 - s  # warehouses s+1, s+2, ..., 4
            if remaining < 2 * num_remaining_warehouses:
                continue
            if remaining > 4 * num_remaining_warehouses:
                continue
            if remaining < 0:
                continue
            # Check that remaining is within the valid range for f_{s+1}
            # f_{s+1} is only defined for k values that are achievable
            # But we need to ensure f[s+1][remaining] has been computed
            # Since we're going backward, f[s+1] is already computed
            cost = C[s][x] + f[s + 1][remaining]
            if cost < best_val:
                best_val = cost
                best_x = x
        if best_x != -1:
            f[s][k] = best_val
            argmin_x[s][k] = best_x
        else:
            f[s][k] = INF
            argmin_x[s][k] = -1

# The answer is f_1(12)
optimal_value = f[1][12]

# Recover the optimal assignment
assignment = [0] * 5  # 1-indexed
k = 12
for s in range(1, 5):
    assignment[s] = argmin_x[s][k]
    k -= assignment[s]

print("OPTIMAL_VALUE:", optimal_value)