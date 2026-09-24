# Nurse Scheduling Optimization Model

## Model Type: MILP (Mixed Integer Linear Program)
*Note: Since the decision variables represent the number of nurses (discrete physical units), they must be integer. However, because the constraint matrix is totally unimodular (network/shift structure), the LP relaxation will yield integer solutions. We declare it as MILP to be safe for discrete counting.*

## 1. Index Sets & Parameters

**Index Sets:**
*   $S = \{1, 2, 3, 4, 5, 6\}$: The set of shift start times.
    *   Shift 1 starts at 02:00
    *   Shift 2 starts at 06:00
    *   Shift 3 starts at 10:00
    *   Shift 4 starts at 14:00
    *   Shift 5 starts at 18:00
    *   Shift 6 starts at 22:00
*   $T = \{1, 2, 3, 4, 5, 6\}$: The set of 4-hour time periods covering the 24-hour day.
    *   Period 1: 02:00 – 06:00
    *   Period 2: 06:00 – 10:00
    *   Period 3: 10:00 – 14:00
    *   Period 4: 14:00 – 18:00
    *   Period 5: 18:00 – 22:00
    *   Period 6: 22:00 – 02:00 (next day)

**Parameters:**
*   $D_t$: Minimum number of nurses required during period $t \in T$.
    *   $D_1 = 10$
    *   $D_2 = 15$
    *   $D_3 = 25$
    *   $D_4 = 20$
    *   $D_5 = 18$
    *   $D_6 = 12$
*   $a_{t,s}$: Binary parameter indicating whether a nurse starting shift $s$ is working during period $t$.
    *   Each nurse works 8 consecutive hours, which covers exactly 2 consecutive 4-hour periods.
    *   Shift 1 (02:00 start): Works Period 1 (02-06) and Period 2 (06-10).
    *   Shift 2 (06:00 start): Works Period 2 (06-10) and Period 3 (10-14).
    *   Shift 3 (10:00 start): Works Period 3 (10-14) and Period 4 (14-18).
    *   Shift 4 (14:00 start): Works Period 4 (14-18) and Period 5 (18-22).
    *   Shift 5 (18:00 start): Works Period 5 (18-22) and Period 6 (22-02).
    *   Shift 6 (22:00 start): Works Period 6 (22-02) and Period 1 (02-06, next day).

    The matrix $A = [a_{t,s}]$ is:
    $$
    A = \begin{bmatrix}
    1 & 0 & 0 & 0 & 0 & 1 \\
    1 & 1 & 0 & 0 & 0 & 0 \\
    0 & 1 & 1 & 0 & 0 & 0 \\
    0 & 0 & 1 & 1 & 0 & 0 \\
    0 & 0 & 0 & 1 & 1 & 0 \\
    0 & 0 & 0 & 0 & 1 & 1
    \end{bmatrix}
    $$
    *(Row $t$, Column $s$)*

## 2. Decision Variables

Let $x_s$ be the number of nurses scheduled to start shift $s$.

*   $x_s \in \mathbb{Z}^+ \cup \{0\}$ for all $s \in S$ (Non-negative integers).

## 3. Objective Function

Minimize the total number of nurses scheduled.

$$
\text{Minimize } Z = \sum_{s=1}^{6} x_s
$$

## 4. Operational Constraints

**Staffing Coverage Constraints:**
For each period $t \in T$, the total number of nurses on duty must meet or exceed the demand $D_t$. A nurse is on duty in period $t$ if they started a shift $s$ such that $a_{t,s} = 1$.

1.  **Period 1 (02:00 – 06:00):** Nurses from Shift 1 and Shift 6 are working.
    $$x_1 + x_6 \ge 10$$

2.  **Period 2 (06:00 – 10:00):** Nurses from Shift 1 and Shift 2 are working.
    $$x_1 + x_2 \ge 15$$

3.  **Period 3 (10:00 – 14:00):** Nurses from Shift 2 and Shift 3 are working.
    $$x_2 + x_3 \ge 25$$

4.  **Period 4 (14:00 – 18:00):** Nurses from Shift 3 and Shift 4 are working.
    $$x_3 + x_4 \ge 20$$

5.  **Period 5 (18:00 – 22:00):** Nurses from Shift 4 and Shift 5 are working.
    $$x_4 + x_5 \ge 18$$

6.  **Period 6 (22:00 – 02:00):** Nurses from Shift 5 and Shift 6 are working.
    $$x_5 + x_6 \ge 12$$

**Non-negativity and Integrality:**
$$x_s \ge 0, \quad x_s \in \mathbb{Z} \quad \forall s \in \{1, 2, 3, 4, 5, 6\}$$

---
### Feasibility Sanity Check
Let's verify if a feasible solution exists by checking aggregate demand.
Total nurse-shifts required per day (sum of demands) = $10 + 15 + 25 + 20 + 18 + 12 = 100$ nurse-periods.
Each nurse provides 8 hours of coverage, which equals 2 nurse-periods (since periods are 4 hours).
Total nurse-periods provided by $N$ nurses = $2N$.
So, $2N \ge 100 \implies N \ge 50$.
The model will find the minimum integer $N \ge 50$ that satisfies the specific cyclic constraints. The constraints are mutually consistent and feasible.