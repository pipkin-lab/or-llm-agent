## Model Type
**MILP** (Mixed-Integer Linear Programming)

*Note: While the constraint matrix is totally unimodular (assignment problem structure) ensuring integer solutions even if relaxed to LP, the decision variables represent discrete assignment choices. Therefore, it is formally an Integer Linear Program (ILP), which falls under the MILP category.*

## Index Sets & Parameters

**Index Sets:**
- $I = \{1, 2, 3, 4, 5\}$: Set of construction companies ($A_i$).
- $J = \{1, 2, 3, 4, 5\}$: Set of new stores to be built ($B_j$).

**Parameters:**
- $c_{ij}$: Construction cost (in thousand yuan) for company $A_i$ to build store $B_j$.
  The cost matrix $C = [c_{ij}]$ is:
  $$
  C = \begin{bmatrix}
  4 & 8 & 7 & 15 & 12 \\
  7 & 9 & 17 & 14 & 10 \\
  6 & 9 & 12 & 8 & 7 \\
  6 & 7 & 14 & 6 & 10 \\
  6 & 9 & 12 & 10 & 6
  \end{bmatrix}
  $$
  Specifically:
  - $c_{11}=4, c_{12}=8, c_{13}=7, c_{14}=15, c_{15}=12$
  - $c_{21}=7, c_{22}=9, c_{23}=17, c_{24}=14, c_{25}=10$
  - $c_{31}=6, c_{32}=9, c_{33}=12, c_{34}=8, c_{35}=7$
  - $c_{41}=6, c_{42}=7, c_{43}=14, c_{44}=6, c_{45}=10$
  - $c_{51}=6, c_{52}=9, c_{53}=12, c_{54}=10, c_{55}=6$

## Decision Variables

Let $x_{ij}$ be a binary decision variable for each $i \in I$ and $j \in J$:
$$
x_{ij} = \begin{cases} 
1 & \text{if construction company } A_i \text{ is assigned to build store } B_j \\
0 & \text{otherwise}
\end{cases}
$$

**Domain:**
$$
x_{ij} \in \{0, 1\}, \quad \forall i \in I, j \in J
$$

## Objective Function

Minimize the total construction cost:
$$
\min Z = \sum_{i=1}^{5} \sum_{j=1}^{5} c_{ij} x_{ij}
$$

Expanding the objective function with specific coefficients:
$$
\min Z = 4x_{11} + 8x_{12} + 7x_{13} + 15x_{14} + 12x_{15} + 7x_{21} + 9x_{22} + 17x_{23} + 14x_{24} + 10x_{25} + 6x_{31} + 9x_{32} + 12x_{33} + 8x_{34} + 7x_{35} + 6x_{41} + 7x_{42} + 14x_{43} + 6x_{44} + 10x_{45} + 6x_{51} + 9x_{52} + 12x_{53} + 10x_{54} + 6x_{55}
$$

## Operational Constraints

**1. Each store must be built by exactly one construction company:**
$$
\sum_{i=1}^{5} x_{ij} = 1, \quad \forall j \in \{1, 2, 3, 4, 5\}
$$

Explicitly:
- Store $B_1$: $x_{11} + x_{21} + x_{31} + x_{41} + x_{51} = 1$
- Store $B_2$: $x_{12} + x_{22} + x_{32} + x_{42} + x_{52} = 1$
- Store $B_3$: $x_{13} + x_{23} + x_{33} + x_{43} + x_{53} = 1$
- Store $B_4$: $x_{14} + x_{24} + x_{34} + x_{44} + x_{54} = 1$
- Store $B_5$: $x_{15} + x_{25} + x_{35} + x_{45} + x_{55} = 1$

**2. Each construction company can be assigned to build at most one store:**
$$
\sum_{j=1}^{5} x_{ij} \leq 1, \quad \forall i \in \{1, 2, 3, 4, 5\}
$$

*Note: In a standard square assignment problem where $|I| = |J|$, the "at most one" constraint combined with the "exactly one" constraint for all stores implies that each company will be used exactly once (since there are 5 stores and 5 companies, and the total sum of assignments must be 5). Thus, equality $\sum_{j=1}^{5} x_{ij} = 1$ is also valid and often preferred for symmetry. We will use equality for strict 1-to-1 assignment.*

Corrected Constraint 2 (Each company builds exactly one store):
$$
\sum_{j=1}^{5} x_{ij} = 1, \quad \forall i \in \{1, 2, 3, 4, 5\}
$$

Explicitly:
- Company $A_1$: $x_{11} + x_{12} + x_{13} + x_{14} + x_{15} = 1$
- Company $A_2$: $x_{21} + x_{22} + x_{23} + x_{24} + x_{25} = 1$
- Company $A_3$: $x_{31} + x_{32} + x_{33} + x_{34} + x_{35} = 1$
- Company $A_4$: $x_{41} + x_{42} + x_{43} + x_{44} + x_{45} = 1$
- Company $A_5$: $x_{51} + x_{52} + x_{53} + x_{54} + x_{55} = 1$

**3. Binary Constraints:**
$$
x_{ij} \in \{0, 1\}, \quad \forall i \in \{1, \dots, 5\}, j \in \{1, \dots, 5\}
$$

## Feasibility Sanity Check
- **Supply**: 5 construction companies, each can take 1 job. Total capacity = 5 jobs.
- **Demand**: 5 stores, each needs 1 job. Total demand = 5 jobs.
- **Balance**: Supply = Demand. A feasible perfect matching exists. The constraint sets are consistent.