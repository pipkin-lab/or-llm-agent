### 1. Index Sets & Parameters

**Sets:**
*   $C = \{1, 2, 3\}$: Set of components ($A_1, A_2, A_3$).
*   $K = \{1, 2, 3\}$: Set of possible number of spare parts for each component.

**Parameters:**
*   $B = 8$: Total budget constraint (thousand yuan).
*   $r_{c, k}$: Reliability of component $c$ when allocated $k$ spare parts.
*   $cost_{c, k}$: Cost (thousand yuan) of allocating $k$ spare parts to component $c$.

**Data Table:**

| $k$ | $r_{1,k}$ ($A_1$) | $r_{2,k}$ ($A_2$) | $r_{3,k}$ ($A_3$) | $cost_{1,k}$ | $cost_{2,k}$ | $cost_{3,k}$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 0.3 | 0.2 | 0.1 | 1 | 3 | 2 |
| 2 | 0.4 | 0.5 | 0.2 | 2 | 5 | 3 |
| 3 | 0.5 | 0.9 | 0.7 | 3 | 6 | 4 |

*Note: The problem states the components work in series, so the system reliability is the product $\prod r_{c,k_c}$. Maximizing the product is equivalent to maximizing the sum of logarithms $\sum \ln(r_{c,k_c})$.*

### 2. Decision Variables

Let $x_{c, k}$ be a binary decision variable:
$$
x_{c, k} = 
\begin{cases} 
1 & \text{if } k \text{ spare parts are allocated to component } c \\
0 & \text{otherwise}
\end{cases}
$$
where $c \in \{1, 2, 3\}$ and $k \in \{1, 2, 3\}$.

### 3. Objective Function

Maximize the sum of the logarithms of the component reliabilities (equivalent to maximizing the total system reliability):

$$
\text{Maximize } Z = \sum_{c=1}^{3} \sum_{k=1}^{3} x_{c, k} \ln(r_{c, k})
$$

### 4. Operational Constraints

**1. Allocation Constraint:**
Exactly one number of spare parts must be chosen for each component.
$$
\sum_{k=1}^{3} x_{c, k} = 1, \quad \forall c \in \{1, 2, 3\}
$$

**2. Budget Constraint:**
The total cost of spare parts must not exceed the budget limit of 8 thousand yuan.
$$
\sum_{c=1}^{3} \sum_{k=1}^{3} cost_{c, k} x_{c, k} \le 8
$$

**3. Variable Bounds:**
$$
x_{c, k} \in \{0, 1\}, \quad \forall c \in \{1, 2, 3\}, \forall k \in \{1, 2, 3\}
$$