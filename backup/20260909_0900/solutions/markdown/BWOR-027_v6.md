# Traveling Salesman Problem (TSP) Formulation

## 1. Index Sets & Parameters

**Index Sets:**
- $V = \{1, 2, \dots, 10\}$: Set of cities (nodes).
- $A = \{(i, j) \in V \times V \mid i \neq j\}$: Set of directed arcs between cities.

**Parameters:**
- $x_i, y_i$: Coordinates of city $i$ (given in Table 14-8).
- $d_{ij}$: Euclidean distance between city $i$ and city $j$, calculated as:
  $$ d_{ij} = \sqrt{(x_i - x_j)^2 + (y_i - y_j)^2} $$
  for all $i, j \in V, i \neq j$.

## 2. Decision Variables

- $x_{ij} \in \{0, 1\}$ for all $(i, j) \in A$: Binary variable where $x_{ij} = 1$ if the route travels directly from city $i$ to city $j$, and $0$ otherwise.
- $u_i \in [0, 9]$ for all $i \in V \setminus \{1\}$: Continuous auxiliary variables used for the Miller-Tucker-Zemlin (MTZ) subtour elimination constraints. We fix the start node as city 1, so $u_1$ is not a variable (implicitly 0).

## 3. Objective Function

**Minimize** the total travel distance:
$$ \text{Minimize } Z = \sum_{i \in V} \sum_{j \in V, j \neq i} d_{ij} x_{ij} $$

## 4. Operational Constraints

**1. Flow Conservation (Out-degree Constraint):**
Each city must have exactly one outgoing arc.
$$ \sum_{j \in V, j \neq i} x_{ij} = 1, \quad \forall i \in V $$

**2. Flow Conservation (In-degree Constraint):**
Each city must have exactly one incoming arc.
$$ \sum_{i \in V, i \neq j} x_{ij} = 1, \quad \forall j \in V $$

**3. Subtour Elimination (MTZ Constraints):**
To ensure a single Hamiltonian cycle and eliminate subtours of length less than $|V|$:
$$ u_i - u_j + |V| x_{ij} \leq |V| - 1, \quad \forall i, j \in V \setminus \{1\}, i \neq j $$
$$ u_i \geq 0, \quad \forall i \in V \setminus \{1\} $$
$$ u_i \leq |V| - 2, \quad \forall i \in V \setminus \{1\} $$
*(Note: Since $|V|=10$, the bounds are $0 \leq u_i \leq 8$. The start node city 1 is excluded from the $u$ variable set as it acts as the root with potential 0.)*

**4. Variable Domains:**
$$ x_{ij} \in \{0, 1\}, \quad \forall (i, j) \in A $$
$$ u_i \in \mathbb{R}, \quad \forall i \in V \setminus \{1\} $$