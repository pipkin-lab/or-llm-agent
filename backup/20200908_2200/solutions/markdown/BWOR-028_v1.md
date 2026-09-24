Here is the formal mathematical optimization model for the nurse scheduling problem.

### 1. Index Sets & Parameters

**Index Sets:**
*   $P = \{1, 2, 3, 4, 5, 6\}$: The set of time periods.
    *   $P_1$: 2:00 – 6:00
    *   $P_2$: 6:00 – 10:00
    *   $P_3$: 10:00 – 14:00
    *   $P_4$: 14:00 – 18:00
    *   $P_5$: 18:00 – 22:00
    *   $P_6$: 22:00 – 2:00
*   $S = \{1, 2, 3, 4, 5, 6\}$: The set of shift start times, corresponding to the start of each period in $P$.
    *   Shift 1 starts at 2:00
    *   Shift 2 starts at 6:00
    *   Shift 3 starts at 10:00
    *   Shift 4 starts at 14:00
    *   Shift 5 starts at 18:00
    *   Shift 6 starts at 22:00

**Parameters:**
*   $d_p$: Minimum number of nurses required during period $p \in P$.
    *   $d_1 = 10$
    *   $d_2 = 15$
    *   $d_3 = 25$
    *   $d_4 = 20$
    *   $d_5 = 18$
    *   $d_6 = 12$
*   $a_{p,s}$: Binary parameter indicating whether a nurse starting shift $s \in S$ is working during period $p \in P$.
    *   $a_{p,s} = 1$ if shift $s$ covers period $p$.
    *   $a_{p,s} = 0$ otherwise.
    *   *Logic*: Since each shift is 8 hours long and periods are 4 hours long, each shift covers exactly two consecutive periods.
        *   Shift 1 (2:00 start) covers $P_1, P_2$.
        *   Shift 2 (6:00 start) covers $P_2, P_3$.
        *   Shift 3 (10:00 start) covers $P_3, P_4$.
        *   Shift 4 (14:00 start) covers $P_4, P_5$.
        *   Shift 5 (18:00 start) covers $P_5, P_6$.
        *   Shift 6 (22:00 start) covers $P_6, P_1$ (wrapping around to the next day's 2:00).

### 2. Decision Variables

*   $x_s$: The number of nurses assigned to start shift $s$.
    *   Domain: $x_s \in \mathbb{Z}^+$ (Non-negative integers) for all $s \in S$.

### 3. Objective Function

The goal is to minimize the total number of nurses scheduled. This is an absolute count of the workforce, not a profit or delta calculation.

$$ \text{Minimize } Z = \sum_{s \in S} x_s $$

### 4. Operational Constraints

**Staffing Requirements:**
For each period $p$, the total number of nurses on duty (from all shifts covering that period) must be greater than or equal to the minimum requirement $d_p$.

$$ \sum_{s \in S} a_{p,s} x_s \ge d_p \quad \forall p \in P $$

Expanding this for each period based on the coverage logic defined in Parameters:

1.  **Period 1 (2:00–6:00)**: Covered by Shift 6 (ending) and Shift 1 (starting).
    $$ x_6 + x_1 \ge 10 $$
2.  **Period 2 (6:00–10:00)**: Covered by Shift 1 (ending) and Shift 2 (starting).
    $$ x_1 + x_2 \ge 15 $$
3.  **Period 3 (10:00–14:00)**: Covered by Shift 2 (ending) and Shift 3 (starting).
    $$ x_2 + x_3 \ge 25 $$
4.  **Period 4 (14:00–18:00)**: Covered by Shift 3 (ending) and Shift 4 (starting).
    $$ x_3 + x_4 \ge 20 $$
5.  **Period 5 (18:00–22:00)**: Covered by Shift 4 (ending) and Shift 5 (starting).
    $$ x_4 + x_5 \ge 18 $$
6.  **Period 6 (22:00–2:00)**: Covered by Shift 5 (ending) and Shift 6 (starting).
    $$ x_5 + x_6 \ge 12 $$

**Variable Bounds:**
$$ x_s \ge 0, \quad x_s \in \mathbb{Z} \quad \forall s \in \{1, 2, 3, 4, 5, 6\} $$

***

### Modeling Verification
*   **Unit Consistency**: All variables represent counts of nurses (integers). All parameters represent counts of nurses (integers). Units are consistent.
*   **Objective Direction**: The problem asks for the "minimum number of nurses," so the objective is Minimization.
*   **Absolute vs. Delta**: The objective is to find the total workforce size $\sum x_s$. This is an absolute state variable, not a net gain. No initial/final wealth distinction applies here as this is a static resource allocation problem.
*   **Cyclic Nature**: The constraint for Period 1 correctly includes $x_6$ (the shift starting at 22:00 the previous day) because the hospital operates 24/7 and shifts wrap around. The model accounts for this via the specific coverage pairs derived from the 8-hour shift length and 4-hour periods.