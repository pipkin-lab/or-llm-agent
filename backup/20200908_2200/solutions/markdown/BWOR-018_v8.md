# Mathematical Optimization Model: Construction Task Assignment

## 1. Index Sets & Parameters

**Index Sets:**
- $I = \{1, 2, 3, 4, 5\}$: Set of construction companies ($A_i$).
- $J = \{1, 2, 3, 4, 5\}$: Set of new stores ($B_j$).

**Parameters:**
- $c_{ij}$: Construction cost (in thousand yuan) for company $A_i$ to build store $B_j$.
  - Given data matrix:
    $$
    C = \begin{bmatrix}
    4 & 8 & 7 & 15 & 12 \\
    7 & 9 & 17 & 14 & 10 \\
    6 & 9 & 12 & 8 & 7 \\
    6 & 7 & 14 & 6 & 10 \\
    6 & 9 & 12 & 10 & 6
    \end{bmatrix}
    $$

## 2. Decision Variables

- $x_{ij} \in \{0, 1\}$ for all $i \in I, j \in J$:
  - $x_{ij} = 1$ if construction company $A_i$ is assigned to build store $B_j$.
  - $x_{ij} = 0$ otherwise.

*Note: Since each store is a discrete physical entity and each company can only be assigned to one task (implied by the 1-to-1 assignment nature of "5 companies to 5 stores"), binary variables are required. The scale is small ($5 \times 5$), so Integer Linear Programming (ILP) is appropriate and computationally trivial.*

## 3. Objective Function

Minimize the total construction cost:

$$
\min Z = \sum_{i=1}^{5} \sum_{j=1}^{5} c_{ij} x_{ij}
$$

## 4. Operational Constraints

**1. Each store must be built by exactly one company:**
$$
\sum_{i=1}^{5} x_{ij} = 1, \quad \forall j \in J
$$

**2. Each company must be assigned to exactly one store:**
$$
\sum_{j=1}^{5} x_{ij} = 1, \quad \forall i \in I
$$

**3. Binary restrictions:**
$$
x_{ij} \in \{0, 1\}, \quad \forall i \in I, j \in J
$$

---

### Model Notes
- This is a standard **Linear Assignment Problem**, which is a special case of the Transportation Problem.
- The constraint structure (row sums = 1, column sums = 1) ensures a one-to-one matching between companies and stores.
- The problem is small enough ($n=5$) that the Hungarian Algorithm or any standard ILP solver will find the global optimum instantly.