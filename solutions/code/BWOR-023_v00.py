from itertools import combinations

# Distance matrix d[i][j] for i, j in {1, 2, 3, 4}
d = {
    (1, 2): 6, (1, 3): 7, (1, 4): 9,
    (2, 1): 8, (2, 3): 9, (2, 4): 7,
    (3, 1): 5, (3, 2): 8, (3, 4): 8,
    (4, 1): 6, (4, 2): 5, (4, 3): 5
}

cities = [2, 3, 4]
n = len(cities)

# C[S][k] = minimum cost to start at city 1, visit all cities in subset S (as a frozenset),
# and end at city k, where k is in S.

# Base case: subsets of size 1
C = dict()
for k in cities:
    S = frozenset([k])
    C[(S, k)] = d[(1, k)]

# Recurrence: for each subset S of cities (size >= 2), and each k in S:
# C(S, k) = min over j in S\{k} of [C(S\{k}, j) + d[j][k]]
for size in range(2, n + 1):
    for subset_tuple in combinations(cities, size):
        S = frozenset(subset_tuple)
        for k in subset_tuple:
            S_without_k = frozenset(set(S) - {k})
            min_cost = float('inf')
            for j in subset_tuple:
                if j == k:
                    continue
                prev = C[(S_without_k, j)]
                cost = prev + d[(j, k)]
                if cost < min_cost:
                    min_cost = cost
            C[(S, k)] = min_cost

# Objective: min over k in {2,3,4} of C({2,3,4}, k) + d[k][1]
full_set = frozenset(cities)
Z = float('inf')
for k in cities:
    total = C[(full_set, k)] + d[(k, 1)]
    if total < Z:
        Z = total

print("OPTIMAL_VALUE:", Z)