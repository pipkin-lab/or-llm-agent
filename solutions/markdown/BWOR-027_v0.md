To solve the problem of finding the shortest route that visits each city exactly once, we formulate this as a **Traveling Salesman Problem (TSP)**. This is a combinatorial optimization problem typically modeled as a Mixed Integer Linear Program (MILP).

### 1. Index Sets & Parameters

**Index Sets:**
*   $I = \{1, 2, \dots, 10\}$: The set of cities.
*   $A = \{(i, j) \mid i, j \in I, i \neq j\}$: The set of all directed arcs connecting city $i$ to city $j$.

**Parameters:**
*   $x_i, y_i$: The coordinates of city $i$ (extracted from Table 14-8).
    *   City 1: $(0, 0)$
    *   City 2: $(5, 20)$
    *   City 3: $(8, 12)$
    *   City 4: $(7, 4)$
    *   City 5: $(10, 15)$
    *   City 6: $(12, 18)$
    *   City 7: $(18, 18)$
    *   City 8: $(18, 15)$
    *   City 9: $(18, 18)$
    *   City 10: $(20, 17)$
*   $d_{ij}$: The Euclidean distance between city $i$ and city $j$, calculated as:
    $$ d_{ij} = \sqrt{(x_i - x_j)^2 + (y_i - y_j)^2} $$
    *Note: $d_{ij} = d_{ji}$ and $d_{ii} = 0$.*

### 2. Decision Variables

*   $x_{ij} \in \{0, 1\}$: Binary variable for all $(i, j) \in A$.
    *   $x_{ij} = 1$ if the route travels directly from city $i$ to city $j$.
    *   $x_{ij} = 0$ otherwise.
*   $u_i \in \mathbb{R}$: Continuous auxiliary variable for all $i \in \{2, \dots, 10\}$ (used for subtour elimination).

### 3. Objective Function

Minimize the total length of the tour:

$$ \text{Minimize } Z = \sum_{i \in I} \sum_{j \in I, j \neq i} d_{ij} x_{ij} $$

### 4. Operational Constraints

**1. Flow Conservation (Each city is entered exactly once):**
For every city $i \in I$:
$$ \sum_{j \in I, j \neq i} x_{ji} = 1 $$

**2. Flow Conservation (Each city is exited exactly once):**
For every city $i \in I$:
$$ \sum_{j \in I, j \neq i} x_{ij} = 1 $$

**3. Subtour Elimination (MTZ Formulation):**
To ensure a single Hamiltonian cycle rather than multiple disjoint loops, we use the Miller-Tucker-Zemlin (MTZ) constraints. For all $i, j \in \{2, \dots, 10\}$ with $i \neq j$:
$$ u_i - u_j + n x_{ij} \leq n - 1 $$
*(Note: $n=10$ is the total number of cities. The variables $u_i$ are bounded, e.g., $1 \leq u_i \leq n-1$, though often implicit in the constraint logic).*

**4. Variable Bounds:**
$$ x_{ij} \in \{0, 1\} \quad \forall (i, j) \in A $$
$$ 1 \leq u_i \leq 9 \quad \forall i \in \{2, \dots, 10\} $$

===============================================================================
MODEL TYPE: MILP (Mixed Integer Linear Program)
===============================================================================