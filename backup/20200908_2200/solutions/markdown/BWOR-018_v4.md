### 1. Index Sets & Parameters

**Index Sets:**
- $I = \{1, 2, 3, 4, 5\}$: Set of construction companies, indexed by $i$.
- $J = \{1, 2, 3, 4, 5\}$: Set of new stores, indexed by $j$.

**Parameters:**
- $c_{ij}$: The construction cost (in thousand yuan) for company $A_i$ to build store $B_j$. The values are given in Table 5-10:

| $c_{ij}$ | $B_1$ | $B_2$ | $B_3$ | $B_4$ | $B_5$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **$A_1$** | 4 | 8 | 7 | 15 | 12 |
| **$A_2$** | 7 | 9 | 17 | 14 | 10 |
| **$A_3$** | 6 | 9 | 12 | 8 | 7 |
| **$A_4$** | 6 | 7 | 14 | 6 | 10 |
| **$A_5$** | 6 | 9 | 12 | 10 | 6 |

### 2. Decision Variables

Let $x_{ij}$ be a binary decision variable defined for all $i \in I$ and $j \in J$:

$$
x_{ij} = 
\begin{cases} 
1 & \text{if construction company } A_i \text{ is assigned to build store } B_j \\
0 & \text{otherwise}
\end{cases}
$$

**Domain:**
$$ x_{ij} \in \{0, 1\} \quad \forall i \in I, j \in J $$

### 3. Objective Function

The goal is to **minimize** the total construction cost.

$$
\text{Minimize } Z = \sum_{i=1}^{5} \sum_{j=1}^{5} c_{ij} x_{ij}
$$

### 4. Operational Constraints

**1. Each store must be built by exactly one company:**
For every store $j$, the sum of assignments across all companies must equal 1.
$$
\sum_{i=1}^{5} x_{ij} = 1 \quad \forall j \in J
$$

**2. Each company is assigned to exactly one store:**
For every company $i$, the sum of assignments across all stores must equal 1.
$$
\sum_{j=1}^{5} x_{ij} = 1 \quad \forall i \in I
$$

**3. Binary Constraints:**
$$
x_{ij} \in \{0, 1\} \quad \forall i \in I, j \in J
$$

---

### Model Verification & Notes

1.  **Problem Type**: This is a standard **Assignment Problem**, which is a special case of the Transportation Problem where supply and demand are equal (1 unit per source/destination). It can be solved as a Linear Programming (LP) problem because the constraint matrix for the assignment problem is totally unimodular, ensuring that the optimal solution to the LP relaxation will be integer (binary). However, explicitly defining $x_{ij}$ as binary (MILP) is the most robust formalization.
2.  **Data Completeness**: All 25 cost parameters $c_{ij}$ are explicitly provided in the table. No missing data.
3.  **Objective Direction**: The problem explicitly asks to **minimize** total cost.
4.  **Unit Consistency**: All costs are in "thousand yuan". No conversion is needed as the objective is a sum of these values.