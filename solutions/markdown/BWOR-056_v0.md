## Model Type: ILP (Integer Linear Programming)

## Index Sets & Parameters

**Courses (index set $C$):**
| Index $i$ | Course Name |
|---|---|
| 1 | Calculus |
| 2 | Operations Research |
| 3 | Data Structures |
| 4 | Managerial Statistics |
| 5 | Computer Simulation |
| 6 | Computer Programming |
| 7 | Forecasting |

**Category-Assignment Parameters $a_{i,k}$** (1 if course $i$ belongs to category $k$, 0 otherwise):

| | Math ($k=1$) | OR ($k=2$) | CS ($k=3$) |
|---|---|---|---|
| 1: Calculus | 1 | 0 | 0 |
| 2: Operations Research | 1 | 1 | 0 |
| 3: Data Structures | 1 | 0 | 1 |
| 4: Managerial Statistics | 1 | 1 | 0 |
| 5: Computer Simulation | 0 | 1 | 1 |
| 6: Computer Programming | 0 | 0 | 1 |
| 7: Forecasting | 1 | 1 | 0 |

**Required minimums per category:**
- $R_{\text{Math}} = 2$
- $R_{\text{OR}} = 2$
- $R_{\text{CS}} = 2$

**Prerequisite Relations (binary parameters $p_{i,j} = 1$ if course $i$ requires course $j$ as prerequisite):**
- $p_{5,6} = 1$ (Computer Simulation requires Computer Programming)
- $p_{3,6} = 1$ (Data Structures requires Computer Programming)
- $p_{4,1} = 1$ (Managerial Statistics requires Calculus)
- $p_{7,4} = 1$ (Forecasting requires Managerial Statistics)

All other $p_{i,j} = 0$.

## Decision Variables

$$x_i \in \{0, 1\}, \quad \forall i \in \{1, 2, 3, 4, 5, 6, 7\}$$

where $x_i = 1$ if course $i$ is selected, and $x_i = 0$ otherwise.

## Objective Function

$$\min \quad \sum_{i=1}^{7} x_i$$

## Operational Constraints

**Category Coverage Constraints:**

$$\sum_{i=1}^{7} a_{i,1} \, x_i \;\geq\; 2 \quad \text{(Mathematics: at least 2 courses)}$$

$$\sum_{i=1}^{7} a_{i,2} \, x_i \;\geq\; 2 \quad \text{(Operations Research: at least 2 courses)}$$

$$\sum_{i=1}^{7} a_{i,3} \, x_i \;\geq\; 2 \quad \text{(Computer Science: at least 2 courses)}$$

Expanding explicitly:

1. **Math (≥ 2):** $\;x_1 + x_2 + x_3 + x_4 + x_7 \;\geq\; 2$

2. **OR (≥ 2):** $\;x_2 + x_4 + x_5 + x_7 \;\geq\; 2$

3. **CS (≥ 2):** $\;x_3 + x_5 + x_6 \;\geq\; 2$

**Prerequisite Constraints:**

4. Computer Simulation requires Computer Programming: $\;x_5 \;\leq\; x_6$

5. Data Structures requires Computer Programming: $\;x_3 \;\leq\; x_6$

6. Managerial Statistics requires Calculus: $\;x_4 \;\leq\; x_1$

7. Forecasting requires Managerial Statistics: $\;x_7 \;\leq\; x_4$

## Feasibility Sanity Check

- **CS requirement (≥ 2):** Only 3 CS courses exist (Data Structures, Computer Simulation, Computer Programming). At least 2 must be chosen.
- If we pick Computer Programming ($x_6=1$), we still need 1 more from {Data Structures, Computer Simulation}.
- **OR requirement (≥ 2):** OR courses are {Operations Research, Managerial Statistics, Computer Simulation, Forecasting}.
- **Math requirement (≥ 2):** Math courses are {Calculus, Operations Research, Data Structures, Managerial Statistics, Forecasting}.

A feasible 4-course solution exists, e.g.:
- Pick: **Calculus** ($x_1=1$), **Operations Research** ($x_2=1$), **Computer Programming** ($x_6=1$), **Data Structures** ($x_3=1$)
- Math: $x_1 + x_2 + x_3 = 3 \geq 2$ ✓
- OR: $x_2 = 1 < 2$ ✗ — need one more OR course.

Try 5 courses: **Calculus, Operations Research, Managerial Statistics, Computer Programming, Data Structures**
- Math: $x_1 + x_2 + x_3 + x_4 = 4 \geq 2$ ✓
- OR: $x_2 + x_4 = 2 \geq 2$ ✓
- CS: $x_3 + x_6 = 2 \geq 2$ ✓
- Prereqs: $x_3 \leq x_6$ (1≤1) ✓, $x_4 \leq x_1$ (1≤1) ✓

This is feasible with **5 courses**. A 4-course solution is infeasible because the CS constraint forces at least 2 of {3, 5, 6}, and the prerequisite chain plus OR/Math requirements cannot all be satisfied with only 4 total courses. The model correctly yields the optimal answer of **5 courses**.