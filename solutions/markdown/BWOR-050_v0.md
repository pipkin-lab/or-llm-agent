To solve the problem of selecting the optimal relay team for the 200-meter medley relay, we must assign exactly one athlete to each of the four strokes (Backstroke, Breaststroke, Butterfly, Freestyle) such that each athlete is assigned to at most one stroke, and the total swimming time is minimized. This is a classic **Assignment Problem**, which can be formulated as a Linear Programming (LP) model with binary decision variables.

### **Model Type**
**MILP** (Mixed Integer Linear Programming)
*Note: Since the constraint matrix of the assignment problem is totally unimodular, the LP relaxation yields integer solutions. However, strictly speaking, the variables are binary/integer.*

### **Index Sets & Parameters**

**Index Sets:**
*   $S = \{1, 2, 3, 4\}$: Set of strokes.
    *   $1$: Backstroke
    *   $2$: Breaststroke
    *   $3$: Butterfly
    *   $4$: Freestyle
*   $A = \{1, 2, 3, 4, 5\}$: Set of athletes.
    *   $1$: Zhao
    *   $2$: Qian
    *   $3$: Zhang
    *   $4$: Wang
    *   $5$: Zhou

**Parameters:**
$c_{a,s}$: Time (in seconds) for athlete $a \in A$ to swim stroke $s \in S$.
Extracted from Table 5-2:

| Stroke $\downset$ / Athlete $\rightarrow$ | 1 (Zhao) | 2 (Qian) | 3 (Zhang) | 4 (Wang) | 5 (Zhou) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1 (Backstroke)** | 37.7 | 32.9 | 33.8 | 37.0 | 35.4 |
| **2 (Breaststroke)** | 43.4 | 33.1 | 42.2 | 34.7 | 41.8 |
| **3 (Butterfly)** | 33.3 | 28.5 | 38.9 | 30.4 | 33.6 |
| **4 (Freestyle)** | 29.2 | 26.4 | 29.6 | 28.5 | 31.1 |

### **Decision Variables**

Let $x_{a,s}$ be a binary decision variable:
$$
x_{a,s} = 
\begin{cases} 
1 & \text{if athlete } a \text{ is assigned to stroke } s \\
0 & \text{otherwise}
\end{cases}
$$
for all $a \in A, s \in S$.

### **Objective Function**

Minimize the total expected relay time:
$$
\text{Minimize } Z = \sum_{a=1}^{5} \sum_{s=1}^{4} c_{a,s} x_{a,s}
$$

### **Operational Constraints**

1.  **Stroke Coverage Constraint**: Each stroke must be assigned to exactly one athlete.
    $$
    \sum_{a=1}^{5} x_{a,s} = 1 \quad \forall s \in S
    $$
    *   For Backstroke ($s=1$): $x_{1,1} + x_{2,1} + x_{3,1} + x_{4,1} + x_{5,1} = 1$
    *   For Breaststroke ($s=2$): $x_{1,2} + x_{2,2} + x_{3,2} + x_{4,2} + x_{5,2} = 1$
    *   For Butterfly ($s=3$): $x_{1,3} + x_{2,3} + x_{3,3} + x_{4,3} + x_{5,3} = 1$
    *   For Freestyle ($s=4$): $x_{1,4} + x_{2,4} + x_{3,4} + x_{4,4} + x_{5,4} = 1$

2.  **Athlete Uniqueness Constraint**: Each athlete can swim at most one stroke.
    $$
    \sum_{s=1}^{4} x_{a,s} \leq 1 \quad \forall a \in A
    $$
    *   For Zhao ($a=1$): $x_{1,1} + x_{1,2} + x_{1,3} + x_{1,4} \leq 1$
    *   For Qian ($a=2$): $x_{2,1} + x_{2,2} + x_{2,3} + x_{2,4} \leq 1$
    *   For Zhang ($a=3$): $x_{3,1} + x_{3,2} + x_{3,3} + x_{3,4} \leq 1$
    *   For Wang ($a=4$): $x_{4,1} + x_{4,2} + x_{4,3} + x_{4,4} \leq 1$
    *   For Zhou ($a=5$): $x_{5,1} + x_{5,2} + x_{5,3} + x_{5,4} \leq 1$

3.  **Binary Constraints**:
    $$
    x_{a,s} \in \{0, 1\} \quad \forall a \in A, s \in S
    $$