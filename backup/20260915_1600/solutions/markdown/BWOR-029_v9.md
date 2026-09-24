To formulate this problem, we first perform the mandatory pre-modeling steps.

### 1. MANDATORY COST INVENTORY & PARAMETER EXTRACTION

**Costs:**
1.  **Full-time nurse wage**: ¥10/hour.
    *   Shift length: 8 hours.
    *   Cost per full-time nurse per shift: $10 \times 8 = 80$ ¥.
2.  **Contract nurse wage**: ¥15/hour.
    *   Shift length: 8 hours.
    *   Cost per contract nurse per shift: $15 \times 8 = 120$ ¥.

**Demand Parameters (Nurses Required):**
The hospital operates on a 24-hour cycle. There are 6 distinct 4-hour time blocks.
*   Block 1 ($2:00 - 6:00$): 10 nurses
*   Block 2 ($6:00 - 10:00$): 15 nurses
*   Block 3 ($10:00 - 14:00$): 25 nurses
*   Block 4 ($14:00 - 18:00$): 20 nurses
*   Block 5 ($18:00 - 22:00$): 18 nurses
*   Block 6 ($22:00 - 2:00$): 12 nurses

**Shift Definitions:**
Nurses work 8 consecutive hours. There are 6 possible shift start times. Let's index the shifts by their start time $s \in \{1, 2, 3, 4, 5, 6\}$ corresponding to start times $\{2:00, 6:00, 10:00, 14:00, 18:00, 22:00\}$.

*   **Shift 1 (Start 2:00)**: Covers 2:00-6:00 (Block 1) and 6:00-10:00 (Block 2).
*   **Shift 2 (Start 6:00)**: Covers 6:00-10:00 (Block 2) and 10:00-14:00 (Block 3).
*   **Shift 3 (Start 10:00)**: Covers 10:00-14:00 (Block 3) and 14:00-18:00 (Block 4).
*   **Shift 4 (Start 14:00)**: Covers 14:00-18:00 (Block 4) and 18:00-22:00 (Block 5).
*   **Shift 5 (Start 18:00)**: Covers 18:00-22:00 (Block 5) and 22:00-2:00 (Block 6).
*   **Shift 6 (Start 22:00)**: Covers 22:00-2:00 (Block 6) and 2:00-6:00 (Block 1).

### 2. MODEL FORMULATION

**Model Type:** MILP (Mixed Integer Linear Programming)
*   *Note*: While the costs are linear, the number of nurses must be integer values. However, since this is a standard linear programming problem with integer coefficients and a totally unimodular constraint matrix (coverage constraints), the LP relaxation will yield integer solutions. We declare variables as INTEGER to be strictly correct for "number of nurses."

**Index Sets:**
*   $S = \{1, 2, 3, 4, 5, 6\}$: Set of shifts, indexed by start time.
*   $B = \{1, 2, 3, 4, 5, 6\}$: Set of 4-hour time blocks.
    *   $B_1$: 2:00-6:00
    *   $B_2$: 6:00-10:00
    *   $B_3$: 10:00-14:00
    *   $B_4$: 14:00-18:00
    *   $B_5$: 18:00-22:00
    *   $B_6$: 22:00-2:00

**Parameters:**
*   $D_b$: Minimum nurses required for block $b$.
    *   $D_1 = 10$
    *   $D_2 = 15$
    *   $D_3 = 25$
    *   $D_4 = 20$
    *   $D_5 = 18$
    *   $D_6 = 12$
*   $C_{ft}$: Cost per full-time nurse per shift = $10 \text{ ¥/hr} \times 8 \text{ hrs} = 80$ ¥.
*   $C_{ct}$: Cost per contract nurse per shift = $15 \text{ ¥/hr} \times 8 \text{ hrs} = 120$ ¥.
*   $A_{s,b}$: Binary parameter equal to 1 if shift $s$ covers block $b$, 0 otherwise.
    *   Shift 1 covers $B_1, B_2 \rightarrow A_{1,1}=1, A_{1,2}=1$
    *   Shift 2 covers $B_2, B_3 \rightarrow A_{2,2}=1, A_{2,3}=1$
    *   Shift 3 covers $B_3, B_4 \rightarrow A_{3,3}=1, A_{3,4}=1$
    *   Shift 4 covers $B_4, B_5 \rightarrow A_{4,4}=1, A_{4,5}=1$
    *   Shift 5 covers $B_5, B_6 \rightarrow A_{5,5}=1, A_{5,6}=1$
    *   Shift 6 covers $B_6, B_1 \rightarrow A_{6,6}=1, A_{6,1}=1$

**Decision Variables:**
*   $x_s$: Number of **full-time** nurses assigned to shift $s$ (Integer, $\ge 0$).
*   $y_s$: Number of **contract** nurses assigned to shift $s$ (Integer, $\ge 0$).

**Objective Function:**
Minimize Total Labor Cost:
$$ \text{Minimize } Z = \sum_{s \in S} (C_{ft} x_s + C_{ct} y_s) $$
$$ Z = 80(x_1 + x_2 + x_3 + x_4 + x_5 + x_6) + 120(y_1 + y_2 + y_3 + y_4 + y_5 + y_6) $$

**Operational Constraints:**
For each time block $b \in B$, the sum of full-time and contract nurses working during that block must meet or exceed the demand $D_b$.

1.  **Block 1 (2:00-6:00)**: Covered by Shift 1 and Shift 6.
    $$ x_1 + y_1 + x_6 + y_6 \ge 10 $$
2.  **Block 2 (6:00-10:00)**: Covered by Shift 1 and Shift 2.
    $$ x_1 + y_1 + x_2 + y_2 \ge 15 $$
3.  **Block 3 (10:00-14:00)**: Covered by Shift 2 and Shift 3.
    $$ x_2 + y_2 + x_3 + y_3 \ge 25 $$
4.  **Block 4 (14:00-18:00)**: Covered by Shift 3 and Shift 4.
    $$ x_3 + y_3 + x_4 + y_4 \ge 20 $$
5.  **Block 5 (18:00-22:00)**: Covered by Shift 4 and Shift 5.
    $$ x_4 + y_4 + x_5 + y_5 \ge 18 $$
6.  **Block 6 (22:00-2:00)**: Covered by Shift 5 and Shift 6.
    $$ x_5 + y_5 + x_6 + y_6 \ge 12 $$

**Variable Bounds:**
$$ x_s \in \mathbb{Z}^+, \quad y_s \in \mathbb{Z}^+, \quad \forall s \in \{1, 2, 3, 4, 5, 6\} $$

---

### FINAL MATHEMATICAL MODEL

**Model Type:** MILP

**Index Sets & Parameters:**
*   $S = \{1, 2, 3, 4, 5, 6\}$ (Shifts starting at 2, 6, 10, 14, 18, 22 hours)
*   $B = \{1, 2, 3, 4, 5, 6\}$ (4-hour blocks)
*   $D_1=10, D_2=15, D_3=25, D_4=20, D_5=18, D_6=12$
*   $C_{ft} = 80$
*   $C_{ct} = 120$

**Decision Variables:**
*   $x_s$: Integer, $\ge 0$, number of full-time nurses in shift $s$.
*   $y_s$: Integer, $\ge 0$, number of contract nurses in shift $s$.

**Objective Function:**
$$ \text{Minimize } Z = 80 \sum_{s=1}^{6} x_s + 120 \sum_{s=1}^{6} y_s $$

**Operational Constraints:**
1.  $x_1 + y_1 + x_6 + y_6 \ge 10$
2.  $x_1 + y_1 + x_2 + y_2 \ge 15$
3.  $x_2 + y_2 + x_3 + y_3 \ge 25$
4.  $x_3 + y_3 + x_4 + y_4 \ge 20$
5.  $x_4 + y_4 + x_5 + y_5 \ge 18$
6.  $x_5 + y_5 + x_6 + y_6 \ge 12$
7.  $x_s, y_s \in \mathbb{Z}$ for all $s=1,\dots,6$.