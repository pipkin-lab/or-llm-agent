import sys

# Distance matrix (1-indexed as per the model: cities 1, 2, 3, 4)
# d[i][j] where i, j are 1-based indices
d = {
    (1, 1): 0, (1, 2): 6, (1, 3): 7, (1, 4): 9,
    (2, 1): 8, (2, 2): 0, (2, 3): 9, (2, 4): 7,
    (3, 1): 5, (3, 2): 8, (3, 3): 0, (3, 4): 8,
    (4, 1): 6, (4, 2): 5, (4, 3): 5, (4, 4): 0,
}

cities = [1, 2, 3, 4]
start = 1
n = len(cities)

# C[i][S_mask] = min cost to start at city 1, visit exactly the set of cities
# represented by S_mask (a bitmask over cities 1..4), and end at city i.
# S_mask is a bitmask where bit k (0-indexed) corresponds to city k+1.
# We only consider states where city 1 is in S_mask and city i is in S_mask.

# Initialize DP table with infinity
INF = float('inf')
C = dict()

# Base case: C[1][{1}] = 0
# Bitmask for {1} is 1 (binary 0001)
C[(1, 1)] = 0

# Precompute all subsets containing city 1 (bit 0 set)
# We iterate by subset size (number of cities visited)
# For each subset S containing 1, for each i in S (i != 1 if |S| > 1),
# compute C[i][S] = min over j in S\{i} (j != 1 if |S| > 2, or j=1 if |S|=2)
# Actually, j can be 1 only if the state (1, S\{i}) is valid.
# In standard TSP DP, C[1][S] for |S| > 1 is typically not used as an intermediate
# because we don't return to start until the end. So we only define C[i][S]
# for i in S, and the recursion only pulls from C[j][S\{i}] where that state is valid.

# Build list of subsets by size
subsets_by_size = dict()
for mask in range(16):  # 0 to 15 (4 bits)
    if mask & 1 == 0:
        continue  # Must contain city 1 (bit 0)
    size = bin(mask).count('1')
    if size not in subsets_by_size:
        subsets_by_size[size] = []
    subsets_by_size[size].append(mask)

# Process stages from size 2 to 4
for k in range(2, n + 1):
    if k not in subsets_by_size:
        continue
    for S_mask in subsets_by_size[k]:
        # For each possible ending city i in S_mask (i != 1)
        for i in cities:
            if i == start:
                continue
            if (S_mask & (1 << (i - 1))) == 0:
                continue  # i not in S
            prev_mask = S_mask & ~(1 << (i - 1))  # S \ {i}
            best = INF
            for j in cities:
                if j == i:
                    continue
                if (prev_mask & (1 << (j - 1))) == 0:
                    continue  # j not in S\{i}
                # The state (j, prev_mask) must have been computed
                # It's valid if j != 1 or (j == 1 and prev_mask == 1)
                # Actually, C[1][prev_mask] is only valid if prev_mask == 1 (base case)
                # For |prev_mask| > 1, C[1][prev_mask] is not a valid intermediate state
                # in the standard forward TSP DP (we don't return to start mid-tour).
                # So we only consider j != 1, OR j == 1 only when prev_mask == 1.
                if j == start:
                    if prev_mask != 1:
                        continue
                key = (j, prev_mask)
                if key not in C:
                    continue
                cost = C[key] + d[(j, i)]
                if cost < best:
                    best = cost
            if best < INF:
                C[(i, S_mask)] = best

# Final step: return to start
full_mask = (1 << n) - 1  # 15 (binary 1111)
Z_star = INF
for i in cities:
    if i == start:
        continue
    key = (i, full_mask)
    if key in C:
        total = C[key] + d[(i, start)]
        if total < Z_star:
            Z_star = total

print("OPTIMAL_VALUE:", Z_star)