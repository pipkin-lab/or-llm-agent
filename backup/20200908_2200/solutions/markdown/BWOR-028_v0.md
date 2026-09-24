# Nurse Scheduling Optimization Model

## 1. Index Sets & Parameters

**Index Sets:**
*   $S = \{1, 2, 3, 4, 5, 6\}$: Set of shift start times.
    *   Shift 1 starts at 2:00
    *   Shift 2 starts at 6:00
    *   Shift 3 starts at 10:00
    *   Shift 4 starts at 14:00
    *   Shift 5 starts at 18:00
    *   Shift 6 starts at 22:00
*   $T = \{1, 2, 3, 4, 5, 6\}$: Set of time periods.
    *   Period 1: 2:00 – 6:00
    *   Period 2: 6:00 – 10:00
    *   Period 3: 10:00 – 14:00
    *   Period 4: 14:00 – 18:00
    *   Period 5: 18:00 – 22:00
    *   Period 6: 22:00 – 2:00 (next day)

**Parameters:**
*   $R_t$: Minimum number of nurses required in time period $t \in T$.
    *   $R_1 = 10$
    *   $R_2 = 15$
    *   $R_3 = 25$
    *   $R_4 = 20$
    *   $R_5 = 18$
    *   $R_6 = 12$

*   $a_{s,t}$: Binary parameter indicating whether a nurse starting shift $s$ works during time period $t$.
    *   Since each shift is 8 hours long and each period is 4 hours long, each nurse works exactly 2 consecutive periods.
    *   Shift 1 (2:00-10:00) covers Periods 1 and 2.
    *   Shift 2 (6:00-14:00) covers Periods 2 and 3.
    *   Shift 3 (10:00-18:00) covers Periods 3 and 4.
    *   Shift 4 (14:00-22:00) covers Periods 4 and 5.
    *   Shift 5 (18:00-2:00) covers Periods 5 and 6.
    *   Shift 6 (22:00-6:00) covers Periods 6 and 1 (wrapping around).

    The matrix $A = [a_{s,t}]$ is:
    $$
    A = \begin{bmatrix}
    1 & 1 & 0 & 0 & 0 & 0 \\
    0 & 1 & 1 & 0 & 0 & 0 \\
    0 & 0 & 1 & 1 & 0 & 0 \\
    0 & 0 & 0 & 1 & 1 & 0 \\
    0 & 0 & 0 & 0 & 1 & 1 \\
    1 & 0 & 0 & 0 & 0 & 1
    \end{bmatrix}
    $$
    *(Rows are shifts $s=1..6$, Columns are periods $t=1..6$)*

## 2. Decision Variables

Let $x_s$ be the number of nurses assigned to shift starting at time $s$.

*   $x_s \in \mathbb{Z}^+$ for all $s \in S$
    *   $x_1$: Number of nurses starting at 2:00
    *   $x_2$: Number of nurses starting at 6:00
    *   $x_3$: Number of nurses starting at 10:00
    *   $x_4$: Number of nurses starting at 14:00
    *   $x_5$: Number of nurses starting at 18:00
    *   $x_6$: Number of nurses starting at 22:00

## 3. Objective Function

Minimize the total number of nurses scheduled.

$$
\text{Minimize } Z = \sum_{s=1}^{6} x_s
$$

$$
Z = x_1 + x_2 + x_3 + x_4 + x_5 + x_6
$$

## 4. Operational Constraints

The total number of nurses working in each time period $t$ must meet or exceed the required number $R_t$.

For each period $t \in \{1, \dots, 6\}$:

1.  **Period 1 (2:00-6:00):** Covered by Shift 1 and Shift 6 (from previous day/late night).
    $$ x_1 + x_6 \ge 10 $$

2.  **Period 2 (6:00-10:00):** Covered by Shift 1 and Shift 2.
    $$ x_1 + x_2 \ge 15 $$

3.  **Period 3 (10:00-14:00):** Covered by Shift 2 and Shift 3.
    $$ x_2 + x_3 \ge 25 $$

4.  **Period 4 (14:00-18:00):** Covered by Shift 3 and Shift 4.
    $$ x_3 + x_4 \ge 20 $$

5.  **Period 5 (18:00-22:00):** Covered by Shift 4 and Shift 5.
    $$ x_4 + x_5 \ge 18 $$

6.  **Period 6 (22:00-2:00):** Covered by Shift 5 and Shift 6.
    $$ x_5 + x_6 \ge 12 $$

**Non-negativity and Integrality:**
$$
x_s \ge 0, \quad x_s \in \mathbb{Z} \quad \forall s \in \{1, \dots, 6\}
$$