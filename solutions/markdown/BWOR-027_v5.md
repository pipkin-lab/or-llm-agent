To find the shortest route that visits each city exactly once, we formulate this as the **Traveling Salesman Problem (TSP)**.

### 1. Index Sets & Parameters

**Index Sets:**
*   $N = \{1, 2, ..., 10\}$: Set of cities.
*   $A = \{(i, j) \mid i, j \in N, i \neq j\}$: Set of directed arcs connecting all pairs of distinct cities.

**Parameters:**
*   $x_i, y_i$: The coordinates of city $i$.
*   $c_{ij}$: The Euclidean distance between city $i$ and city $j$, defined as:
    $$ c_{ij} = \sqrt{(x_i - x_j)^2 + (y_i - y_j)^2} \quad \forall (i, j) \in A $$

**Numeric Data (from Table 14-8):**
| City $i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $x_i$ | 0 | 5 | 8 | 7 | 10 | 12 | 18 | 18 | 18 | 20 |
| $y_i$ | 0 | 20 | 12 | 4 | 15 | 18 | 18 | 15 | 18 | 17 |

*(Note: The specific values of $c_{ij}$ are computed from these coordinates in the model implementation. For example, $c_{12} = \sqrt{(5-0)^2 + (20-0)^2} = \sqrt{425} \approx 20.62$.)*

### 2. Decision Variables

*   $x_{ij} \in \{0, 1\}$: Binary variable for each arc $(i, j) \in A$.
    *   $x_{ij} = 1$ if the route travels directly from city $i$ to city $j$.
    *   $x_{ij} = 0$ otherwise.
*   $u_k \in [0, N-1]$: Continuous auxiliary variable for each city $k \in N$ (used in the MTZ formulation to prevent subtours).

### 3. Objective Function

Minimize the total length of the tour:
$$ \text{Minimize } Z = \sum_{i \in N} \sum_{j \in N, j \neq i} c_{ij} x_{ij} $$

### 4. Operational Constraints

**A. Flow Conservation (Degree Constraints):**
Each city must be visited exactly once, meaning every city has exactly one incoming arc and one outgoing arc.

1.  **Outflow Constraint:** For each city $i \in N$:
    $$ \sum_{j \in N, j \neq i} x_{ij} = 1 $$

2.  **Inflow Constraint:** For each city $j \in N$:
    $$ \sum_{i \in N, i \neq j} x_{ij} = 1 $$

**B. Subtour Elimination (MTZ Formulation):**
To ensure the solution is a single Hamiltonian cycle (visiting all cities) and not a collection of smaller disjoint cycles (subtours), we use the Miller-Tucker-Zemlin (MTZ) constraints.

3.  **Subtour Prevention Constraints:** For each pair of distinct cities $i, j \in N$ ($i \neq j$):
    $$ u_i - u_j + N x_{ij} \leq N - 1 $$

    *(Explanation: The variable $u_i$ represents the "position" of city $i$ in the tour. If the solver tries to create a subtour, the $u$ values cannot be consistently assigned to satisfy these inequalities for all edges in the subtour.)*

**C. Variable Domains:**
4.  **Binary Bounds:**
    $$ x_{ij} \in \{0, 1\} \quad \forall (i, j) \in A $$
5.  **Auxiliary Bounds:**
    $$ 0 \leq u_k \leq N - 1 \quad \forall k \in N $$
    *(Note: In practice, $u_1$ is often fixed to 0 to break symmetry, i.e., $u_1 = 0$, and $0 \leq u_k \leq N-1$ for $k > 1$.)*

### Model Type Declaration
**MILP** (Mixed Integer Linear Programming).
Although the distances involve square roots, the coefficients $c_{ij}$ are pre-calculated constants. The variables are linear.