Based on the problem description and the provided table, here is the formal mathematical optimization model.

### **Model Type**
**MILP** (Mixed Integer Linear Programming)
*Reasoning: The decision involves selecting discrete plans (integer choices) for each factory, and the objective function and constraints are linear.*

### **Index Sets & Parameters**

*   **Sets:**
    *   $I = \{1, 2, 3\}$: Set of factories.
    *   $J_i$: Set of available plans for factory $i$.
        *   $J_1 = \{0, 1, 2\}$ (Plans 1, 2, 3 from the table; Plan 1 is "No Investment")
        *   $J_2 = \{0, 1, 2, 3\}$ (Plans 1, 2, 3, 4 from the table)
        *   $J_3 = \{0, 1\}$ (Plans 1, 2 from the table)
    *   *Note: We re-index the plans locally for each factory to 0, 1, ... $n_i-1$ for clarity, where index 0 corresponds to "Plan 1" (0 investment, 0 return).*

*   **Parameters:**
    *   $C_{i,j}$: Investment cost (million yuan) for plan $j$ at factory $i$.
    *   $R_{i,j}$: Return (million yuan) for plan $j$ at factory $i$.
    *   $B$: Total available budget (million yuan). $B = 5$.

**Data Extraction from Table 7-4:**

| Factory ($i$) | Plan Index ($j$) | Description | Investment $C_{i,j}$ | Return $R_{i,j}$ |
| :--- | :---: | :--- | :---: | :---: |
| **1** | 0 | Plan 1 (None) | 0 | 0 |
| | 1 | Plan 2 | 1 | 5 |
| | 2 | Plan 3 | 2 | 6 |
| **2** | 0 | Plan 1 (None) | 0 | 0 |
| | 1 | Plan 2 | 2 | 8 |
| | 2 | Plan 3 | 3 | 9 |
| | 3 | Plan 4 | 4 | 12 |
| **3** | 0 | Plan 1 (None) | 0 | 0 |
| | 1 | Plan 2 | 1 | 3 |

### **Decision Variables**

Let $x_{i,j}$ be a binary variable for each factory $i \in I$ and each available plan $j \in J_i$:

$$
x_{i,j} = 
\begin{cases} 
1 & \text{if plan } j \text{ is selected for factory } i \\
0 & \text{otherwise}
\end{cases}
$$

**Domain:** $x_{i,j} \in \{0, 1\}$ for all $i \in I, j \in J_i$.

### **Objective Function**

Maximize the total return across all factories.

$$
\text{Maximize } Z = \sum_{i \in I} \sum_{j \in J_i} R_{i,j} x_{i,j}
$$

Expanding with specific values:
$$
Z = 5x_{1,1} + 6x_{1,2} + 8x_{2,1} + 9x_{2,2} + 12x_{2,3} + 3x_{3,1}
$$

### **Operational Constraints**

1.  **Budget Constraint:**
    The total investment across all selected plans must not exceed the available budget of 5 million yuan.
    $$
    \sum_{i \in I} \sum_{j \in J_i} C_{i,j} x_{i,j} \le 5
    $$
    Expanded:
    $$
    1x_{1,1} + 2x_{1,2} + 2x_{2,1} + 3x_{2,2} + 4x_{2,3} + 1x_{3,1} \le 5
    $$

2.  **Single Plan Selection Constraint:**
    Exactly one plan must be selected for each factory.
    $$
    \sum_{j \in J_i} x_{i,j} = 1, \quad \forall i \in I
    $$
    Expanded:
    *   Factory 1: $x_{1,0} + x_{1,1} + x_{1,2} = 1$
    *   Factory 2: $x_{2,0} + x_{2,1} + x_{2,2} + x_{2,3} = 1$
    *   Factory 3: $x_{3,0} + x_{3,1} = 1$

3.  **Integrality Constraints:**
    $$
    x_{i,j} \in \{0, 1\}, \quad \forall i \in I, j \in J_i
    $$