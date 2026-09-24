# Assignment Problem: Construction Task Allocation

## Model Type
**MILP** (Linear objective and linear constraints with binary decision variables).

## Index Sets & Parameters

**Index Sets:**
- $I = \{1, 2, 3, 4, 5\}$: Set of construction companies ($A_i$).
- $J = \{1, 2, 3, 4, 5\}$: Set of new stores ($B_j$).

**Parameters:**
- $c_{ij}$: Construction cost (in thousand yuan) for company $A_i$ to build store $B_j$.

| $i \setminus j$ | $B_1$ | $B_2$ | $B_3$ | $B_4$ | $B_5$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| $A_1$ | 4 | 8 | 7 | 15 | 12 |
| $A_2$ | 7 | 9 | 17 | 14 | 10 |
| $A_3$ | 6 | 9 | 12 | 8 | 7 |
| $A_4$ | 6 | 7 | 14 | 6 | 10 |
| $A_5$ | 6 | 9 | 12 | 10 | 6 |

*Note: All cost values are extracted directly from Table 5-10.*

## Decision Variables

- $x_{ij} \in \{0, 1\}$ for all $i \in I, j \in J$:
  - $x_{ij} = 1$ if construction company $A_i$ is assigned to build store $B_j$.
  - $x_{ij} = 0$ otherwise.

## Objective Function

Minimize the total construction cost:

$$
\min Z = \sum_{i=1}^{5} \sum_{j=1}^{5} c_{ij} x_{ij}
$$

## Operational Constraints

1. **Store Assignment Constraint:** Each store must be assigned to exactly one construction company.
   $$
   \sum_{i=1}^{5} x_{ij} = 1, \quad \forall j \in J
   $$

2. **Company Assignment Constraint:** Each construction company can be assigned to exactly one store.
   $$
   \sum_{j=1}^{5} x_{ij} = 1, \quad \forall i \in I
   $$

3. **Binary Constraints:**
   $$
   x_{ij} \in \{0, 1\}, \quad \forall i \in I, j \in J
   $$