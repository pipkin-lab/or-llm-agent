# Mathematical Optimization Model: Construction Assignment Problem

## 1. Index Sets & Parameters

**Index Sets:**
*   $I = \{1, 2, 3, 4, 5\}$: Set of construction companies ($A_i$).
*   $J = \{1, 2, 3, 4, 5\}$: Set of stores to be constructed ($B_j$).

**Parameters:**
*   $c_{ij}$: The cost (in thousand yuan) for construction company $A_i$ to build store $B_j$. The values are given in the table:

| $c_{ij}$ | $B_1$ | $B_2$ | $B_3$ | $B_4$ | $B_5$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **$A_1$** | 4 | 8 | 7 | 15 | 12 |
| **$A_2$** | 7 | 9 | 17 | 14 | 10 |
| **$A_3$** | 6 | 9 | 12 | 8 | 7 |
| **$A_4$** | 6 | 7 | 14 | 6 | 10 |
| **$A_5$** | 6 | 9 | 12 | 10 | 6 |

## 2. Decision Variables

Let $x_{ij}$ be a binary decision variable defined as:
$$
x_{ij} = 
\begin{cases} 
1 & \text{if construction company } A_i \text{ is assigned to build store } B_j \\
0 & \text{otherwise}
\end{cases}
$$
For all $i \in I, j \in J$.

*Domain:* $x_{ij} \in \{0, 1\}$

## 3. Objective Function

The goal is to **minimize** the total construction cost.

$$
\text{Minimize } Z = \sum_{i \in I} \sum_{j \in J} c_{ij} x_{ij}
$$

## 4. Operational Constraints

**Constraint 1: Each store is built by exactly one construction company.**
For every store $j \in J$:
$$
\sum_{i \in I} x_{ij} = 1
$$

**Constraint 2: Each construction company is assigned to build exactly one store.**
For every construction company $i \in I$:
$$
\sum_{j \in J} x_{ij} = 1
$$

**Constraint 3: Binary restrictions.**
$$
x_{ij} \in \{0, 1\} \quad \forall i \in I, j \in J
$$

### Model Notes
*   This is a standard **Assignment Problem**, which is a special case of the Transportation Problem where supply and demand are both 1 for all origins and destinations.
*   Since the number of companies equals the number of stores ($n=5$), the constraints ensure a one-to-one bijection between companies and stores.
*   The constraint matrix of an assignment problem is totally unimodular. Therefore, the Linear Programming (LP) relaxation of this model (where $0 \le x_{ij} \le 1$) will yield integer solutions. However, specifying $x_{ij}$ as binary is the standard and safest formulation for clarity and direct solver compatibility.