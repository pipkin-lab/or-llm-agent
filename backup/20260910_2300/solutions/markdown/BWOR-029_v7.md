**Model Type:** MILP (Mixed Integer Linear Program)

### 1. Index Sets & Parameters

**Index Sets:**
*   $S = \{1, 2, 3, 4, 5, 6\}$: The set of shift start times.
    *   Shift 1: 2:00–10:00
    *   Shift 2: 6:00–14:00
    *   Shift 3: 10:00–18:00
    *   Shift 4: 14:00–22:00
    *   Shift 5: 18:00–26:00 (i.e., 18:00–2:00 next day)
    *   Shift 6: 22:00–30:00 (i.e., 22:00–6:00 next day)
*   $T = \{1, 2, 3, 4, 5, 6\}$: The set of 4-hour time blocks for coverage requirements.
    *   Block 1: 2:00–6:00
    *   Block 2: 6:00–10:00
    *   Block 3: 10:00–14:00
    *   Block 4: 14:00–18:00
    *   Block 5: 18:00–22:00
    *   Block 6: 22:00–2:00

**Parameters:**
*   $R_t$: Required number of nurses for time block $t \in T$.
    *   $R_1 = 10$
    *   $R_2 = 15$
    *   $R_3 = 25$
    *   $R_4 = 20$
    *   $R_5 = 18$
    *   $R_6 = 12$
*   $w_F$: Hourly wage for a full-time nurse = 10 ¥/hour.
*   $w_C$: Hourly wage for a contract nurse = 15 ¥/hour.
*   $H$: Duration of a shift in hours = 8 hours.
*   $C_F$: Total cost per full-time nurse per shift = $w_F \times H = 10 \times 8 = 80$ ¥.
*   $C_C$: Total cost per contract nurse per shift = $w_C \times H = 15 \times 8 = 120$ ¥.

**Shift Coverage Matrix ($A$):**
Let $a_{t,s}$ be 1 if a nurse starting shift $s$ is working during time block $t$, and 0 otherwise.
*   Shift 1 (2:00-10:00) covers Blocks 1 and 2.
*   Shift 2 (6:00-14:00) covers Blocks 2 and 3.
*   Shift 3 (10:00-18:00) covers Blocks 3 and 4.
*   Shift 4 (14:00-22:00) covers Blocks 4 and 5.
*   Shift 5 (18:00-2:00) covers Blocks 5 and 6.
*   Shift 6 (22:00-6:00) covers Blocks 6 and 1 (wrapping around).

Specifically:
*   $a_{1,1}=1, a_{2,1}=1$; $a_{t,1}=0$ for $t \notin \{1,2\}$
*   $a_{2,2}=1, a_{3,2}=1$; $a_{t,2}=0$ for $t \notin \{2,3\}$
*   $a_{3,3}=1, a_{4,3}=1$; $a_{t,3}=0$ for $t \notin \{3,4\}$
*   $a_{4,4}=1, a_{5,4}=1$; $a_{t,4}=0$ for $t \notin \{4,5\}$
*   $a_{5,5}=1, a_{6,5}=1$; $a_{t,5}=0$ for $t \notin \{5,6\}$
*   $a_{6,6}=1, a_{1,6}=1$; $a_{t,6}=0$ for $t \notin \{6,1\}$

### 2. Decision Variables

We define variables for the number of nurses assigned to each shift. Since we are comparing hiring strategies, we split the nurses into Full-time ($F$) and Contract ($C$) categories. Both types work the same shifts, so we need variables for each type in each shift.

*   $x_{F,s}$: Number of **full-time** nurses assigned to shift $s$ ($s \in S$).
    *   Domain: $x_{F,s} \in \mathbb{Z}_{\ge 0}$ (Non-negative Integers)
*   $x_{C,s}$: Number of **contract** nurses assigned to shift $s$ ($s \in S$).
    *   Domain: $x_{C,s} \in \mathbb{Z}_{\ge 0}$ (Non-negative Integers)

*Note: In a standard formulation without pre-existing staff, we are determining the total staffing plan. The problem asks "Should the hospital hire contract nurses?", which implies we are optimizing the mix. If the optimal solution has $x_{C,s} = 0$ for all $s$, then no contract nurses are hired. If any $x_{C,s} > 0$, they are hired.*

### 3. Objective Function

Minimize the total labor cost.

$$
\text{Minimize } Z = \sum_{s \in S} (C_F \cdot x_{F,s} + C_C \cdot x_{C,s})
$$

Substituting values:
$$
Z = 80 \sum_{s \in S} x_{F,s} + 120 \sum_{s \in S} x_{C,s}
$$

### 4. Operational Constraints

**Coverage Constraints:**
For each time block $t \in T$, the total number of nurses (full-time + contract) working during that block must meet or exceed the requirement $R_t$.

$$
\sum_{s \in S} (x_{F,s} + x_{C,s}) a_{t,s} \ge R_t, \quad \forall t \in T
$$

Explicitly written out for each block:

1.  **Block 1 (2:00-6:00):** Covered by Shift 1 and Shift 6.
    $$x_{F,1} + x_{C,1} + x_{F,6} + x_{C,6} \ge 10$$
2.  **Block 2 (6:00-10:00):** Covered by Shift 1 and Shift 2.
    $$x_{F,1} + x_{C,1} + x_{F,2} + x_{C,2} \ge 15$$
3.  **Block 3 (10:00-14:00):** Covered by Shift 2 and Shift 3.
    $$x_{F,2} + x_{C,2} + x_{F,3} + x_{C,3} \ge 25$$
4.  **Block 4 (14:00-18:00):** Covered by Shift 3 and Shift 4.
    $$x_{F,3} + x_{C,3} + x_{F,4} + x_{C,4} \ge 20$$
5.  **Block 5 (18:00-22:00):** Covered by Shift 4 and Shift 5.
    $$x_{F,4} + x_{C,4} + x_{F,5} + x_{C,5} \ge 18$$
6.  **Block 6 (22:00-2:00):** Covered by Shift 5 and Shift 6.
    $$x_{F,5} + x_{C,5} + x_{F,6} + x_{C,6} \ge 12$$

**Non-negativity and Integrality:**
$$
x_{F,s} \in \mathbb{Z}_{\ge 0}, \quad x_{C,s} \in \mathbb{Z}_{\ge 0}, \quad \forall s \in S
$$

### Feasibility Sanity Check

Let's verify if a solution exists.
Sum of requirements: $10+15+25+20+18+12 = 100$ nurse-blocks.
Each nurse works 2 blocks (8 hours).
Total nurse-shifts required $\approx 100/2 = 50$.
Since we can hire any number of nurses, the problem is clearly feasible. We can always hire enough full-time nurses to satisfy all constraints. The optimization will determine if mixing in contract nurses (which are more expensive) is ever beneficial. *Note: Since contract nurses are more expensive ($120 vs $80) and have identical coverage properties, the optimal solution will intuitively use **zero** contract nurses unless there are constraints on the maximum number of full-time nurses or specific shift preferences, which are not present in this text. The model will mathematically confirm this by setting all $x_{C,s} = 0$.*