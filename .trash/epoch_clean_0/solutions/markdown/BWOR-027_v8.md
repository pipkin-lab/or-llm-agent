Here is the formal mathematical optimization model for the Traveling Salesman Problem (TSP) based on the provided city coordinates.

### 1. Index Sets & Parameters

**Index Sets:**
*   $V = \{1, 2, ..., 10\}$: The set of cities.
*   $i, j \in V$: Indices for cities.

**Parameters:**
*   $x_i, y_i$: The Cartesian coordinates of city $i$. Based on Table 14-8:
    *   $x = [0, 5, 8, 7, 10, 12, 18, 18, 18, 20]$
    *   $y = [0, 20, 12, 4, 15, 18, 15, 15, 18, 17]$
*   $d_{ij}$: The Euclidean distance between city $i$ and city $j$, calculated as:
    $$ d_{ij} = \sqrt{(x_i - x_j)^2 + (y_i - y_j)^2} $$
    *Note: $d_{ii} = 0$.*
*   $n$: The total number of cities, $n = 10$.

### 2. Decision Variables

*   $x_{ij}$: Binary variable.
    $$
    x_{ij} = \begin{cases} 
    1 & \text{if the route travels directly from city } i \text{ to city } j \\
    0 & \text{otherwise}
    \end{cases}
    $$
    where $i, j \in V, i \neq j$.

*   $u_i$: Continuous auxiliary variable (Miller-Tucker-Zemlin constraint variable) used to eliminate subtours.
    *   $u_i \in [0, n-1]$ for all $i \in V$.
    *   We fix the starting city as city 1, so $u_1 = 0$.

### 3. Objective Function

Minimize the total travel distance $Z$:

$$ \min Z = \sum_{i \in V} \sum_{j \in V, j \neq i} d_{ij} x_{ij} $$

### 4. Operational Constraints

**1. Flow Conservation (In/Out Degree Constraints):**
Each city must have exactly one incoming edge and one outgoing edge.

$$ \sum_{j \in V, j \neq i} x_{ij} = 1 \quad \forall i \in V $$
$$ \sum_{i \in V, i \neq j} x_{ij} = 1 \quad \forall j \in V $$

**2. Subtour Elimination (Miller-Tucker-Zemlin Formulation):**
To ensure the solution is a single tour visiting all cities and not a collection of disjoint cycles, we use the MTZ constraints. For all $i, j \in V$ where $i \neq j$, $i \neq 1$, and $j \neq 1$:

$$ u_i - u_j + n x_{ij} \leq n - 1 $$

*Explanation*: This constraint ensures that if the arc $(i, j)$ is selected ($x_{ij}=1$), then $u_j \geq u_i + 1$. Since $u_1=0$ and $u_i$ are bounded by $n-1$, this forces a Hamiltonian path starting at 1 that visits all nodes without closing loops prematurely.

**3. Variable Domains & Bounds:**

$$ x_{ij} \in \{0, 1\} \quad \forall i, j \in V, i \neq j $$
$$ 0 \leq u_i \leq n - 1 \quad \forall i \in V \setminus \{1\} $$
$$ u_1 = 0 $$