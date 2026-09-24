## Model Type: MILP (Mixed-Integer Linear Programming)

## Index Sets & Parameters

**Index Sets:**
- $I = \{1, 2, 3, 4, 5, 6\}$: Set of time periods (each 4 hours long).
- $J = \{1, 2, 3, 4, 5, 6\}$: Set of shift start times (corresponding to 2:00, 6:00, 10:00, 14:00, 18:00, 22:00).

**Parameters:**
- $D_i$: Minimum number of nurses required in period $i$.
  - $D_1 = 10$ (2:00–6:00)
  - $D_2 = 15$ (6:00–10:00)
  - $D_3 = 25$ (10:00–14:00)
  - $D_4 = 20$ (14:00–18:00)
  - $D_5 = 18$ (18:00–22:00)
  - $D_6 = 12$ (22:00–2:00)

- $a_{i,j}$: Binary parameter equal to 1 if a nurse starting shift $j$ works during period $i$, and 0 otherwise.
  - Each shift is 8 hours long, which spans exactly 2 consecutive 4-hour periods.
  - Shift 1 (2:00 start): Works periods 1 and 2. $\rightarrow a_{1,1}=1, a_{2,1}=1$, others 0.
  - Shift 2 (6:00 start): Works periods 2 and 3. $\rightarrow a_{2,2}=1, a_{3,2}=1$, others 0.
  - Shift 3 (10:00 start): Works periods 3 and 4. $\rightarrow a_{3,3}=1, a_{4,3}=1$, others 0.
  - Shift 4 (14:00 start): Works periods 4 and 5. $\rightarrow a_{4,4}=1, a_{5,4}=1$, others 0.
  - Shift 5 (18:00 start): Works periods 5 and 6. $\rightarrow a_{5,5}=1, a_{6,5}=1$, others 0.
  - Shift 6 (22:00 start): Works periods 6 and 1 (wraps around). $\rightarrow a_{6,6}=1, a_{1,6}=1$, others 0.

## Decision Variables

- $x_j$: Number of nurses assigned to shift $j$ (starting at the specific time corresponding to index $j$).
  - Domain: $x_j \in \mathbb{Z}_{\ge 0}$ for all $j \in J$.
  - (Nurses are discrete units, so variables must be non-negative integers).

## Objective Function

Minimize the total number of nurses scheduled. Since each nurse works exactly one shift, the total number of nurses is the sum of nurses assigned to all shifts.

$$ \text{Minimize } Z = \sum_{j=1}^{6} x_j $$

## Operational Constraints

**Staffing Requirements:**
For each time period $i$, the total number of nurses working on shift $j$ must be at least the demand $D_i$. A nurse on shift $j$ covers period $i$ if and only if $a_{i,j} = 1$.

$$ \sum_{j=1}^{6} a_{i,j} x_j \ge D_i, \quad \forall i \in I $$

**Explicit Constraints:**

1.  **Period 1 (2:00–6:00):** Covered by Shift 1 (starts 2:00) and Shift 6 (starts 22:00, works until 6:00).
    $$ x_1 + x_6 \ge 10 $$

2.  **Period 2 (6:00–10:00):** Covered by Shift 1 (ends 10:00) and Shift 2 (starts 6:00).
    $$ x_1 + x_2 \ge 15 $$

3.  **Period 3 (10:00–14:00):** Covered by Shift 2 (ends 14:00) and Shift 3 (starts 10:00).
    $$ x_2 + x_3 \ge 25 $$

4.  **Period 4 (14:00–18:00):** Covered by Shift 3 (ends 18:00) and Shift 4 (starts 14:00).
    $$ x_3 + x_4 \ge 20 $$

5.  **Period 5 (18:00–22:00):** Covered by Shift 4 (ends 22:00) and Shift 5 (starts 18:00).
    $$ x_4 + x_5 \ge 18 $$

6.  **Period 6 (22:00–2:00):** Covered by Shift 5 (ends 2:00) and Shift 6 (starts 22:00).
    $$ x_5 + x_6 \ge 12 $$

**Non-negativity and Integrality:**
$$ x_j \in \mathbb{Z}_{\ge 0}, \quad \forall j \in \{1, 2, 3, 4, 5, 6\} $$