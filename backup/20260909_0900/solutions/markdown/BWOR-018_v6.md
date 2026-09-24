# Operations Research Model: Construction Task Assignment

## 1. Index Sets & Parameters

**Index Sets:**
- $I = \{1, 2, 3, 4, 5\}$: Set of construction companies ($A_i$).
- $J = \{1, 2, 3, 4, 5\}$: Set of new stores to be built ($B_j$).

**Parameters:**
- $c_{ij}$: Cost (in thousand yuan) for construction company $A_i$ to build store $B_j$.
  - Given table:
    - $c_{1} = [4, 8, 7, 15, 12]$
    - $c_{2} = [7, 9, 17, 14, 10]$
    - $c_{3} = [6, 9, 12, 8, 7]$
    - $c_{4} = [6, 7, 14, 6, 10]$
    - $c_{5} = [6, 9, 12, 10, 6]$

## 2. Decision Variables

Let $x_{ij}$ be a binary variable defined as:
$$
x_{ij} = 
\begin{cases} 
1 & \text{if construction company } A_i \text{ is assigned to build store } B_j \\
0 & \text{otherwise}
\end{cases}
$$
Domain: $x_{ij} \in \{0, 1\}$ for all $i \in I, j \in J$.

## 3. Objective Function

Minimize the total construction cost:
$$
\min Z = \sum_{i=1}^{5} \sum_{j=1}^{5} c_{ij} x_{ij}
$$

## 4. Operational Constraints

**1. Each store is built by exactly one construction company:**
For every store $j \in J$:
$$
\sum_{i=1}^{5} x_{ij} = 1 \quad \forall j \in \{1, 2, 3, 4, 5\}
$$

**2. Each construction company is assigned to exactly one store:**
For every construction company $i \in I$:
$$
\sum_{j=1}^{5} x_{ij} = 1 \quad \forall i \in \{1, 2, 3, 4, 5\}
$$

**3. Binary Constraints:**
$$
x_{ij} \in \{0, 1\} \quad \forall i \in I, j \in J
$$

*(Note: This is a standard Assignment Problem, which is a special case of the Transportation Problem. Since the number of companies equals the number of stores, it is a balanced assignment problem.)*