## Model Type
**LP** (Linear Program)

## Index Sets & Parameters

**Time Periods** (indexed by $t = 1, \dots, 6$):
| $t$ | Time Window | Demand $d_t$ (nurses) |
|-----|------------|----------------------|
| 1 | 22:00 – 02:00 | 12 |
| 2 | 02:00 – 06:00 | 10 |
| 3 | 06:00 – 10:00 | 15 |
| 4 | 10:00 – 14:00 | 25 |
| 5 | 14:00 – 18:00 | 20 |
| 6 | 18:00 – 22:00 | 18 |

**Shift Start Times** (indexed by $s = 1, \dots, 6$):
| $s$ | Shift Start | Hours Worked |
|-----|------------|--------------|
| 1 | 22:00 | 22:00 – 06:00 (next day) |
| 2 | 02:00 | 02:00 – 10:00 |
| 3 | 06:00 | 06:00 – 14:00 |
| 4 | 10:00 | 10:00 – 18:00 |
| 5 | 14:00 | 14:00 – 22:00 |
| 6 | 18:00 | 18:00 – 02:00 (next day) |

**Coverage Matrix** $a_{t,s}$: equals 1 if a nurse starting shift $s$ is on duty during period $t$, else 0.

| $t \backslash s$ | 1 (22:00) | 2 (02:00) | 3 (06:00) | 4 (10:00) | 5 (14:00) | 6 (18:00) |
|---|---|---|---|---|---|---|
| **1** (22:00–02:00) | 1 | 0 | 0 | 0 | 0 | 1 |
| **2** (02:00–06:00) | 1 | 1 | 0 | 0 | 0 | 0 |
| **3** (06:00–10:00) | 0 | 1 | 1 | 0 | 0 | 0 |
| **4** (10:00–14:00) | 0 | 0 | 1 | 1 | 0 | 0 |
| **5** (14:00–18:00) | 0 | 0 | 0 | 1 | 1 | 0 |
| **6** (18:00–22:00) | 0 | 0 | 0 | 0 | 1 | 1 |

**Parameters:**
- $d_1 = 12, \; d_2 = 10, \; d_3 = 15, \; d_4 = 25, \; d_5 = 20, \; d_6 = 18$

## Decision Variables

$$x_s \in \mathbb{Z}^+ \quad \text{for } s = 1, \dots, 6$$

where $x_s$ = number of nurses assigned to the shift starting at time $s$.

*(Note: Since we are minimizing the total number of nurses and all demands are integers, the LP relaxation will yield an integer solution due to the total unimodularity of the constraint matrix, but we specify integer variables for correctness.)*

## Objective Function

$$\min \; Z = x_1 + x_2 + x_3 + x_4 + x_5 + x_6$$

## Operational Constraints

**Coverage Constraints** (for each period $t = 1, \dots, 6$):

$$\sum_{s=1}^{6} a_{t,s} \, x_s \geq d_t$$

Explicitly:

1. **Period 1 (22:00–02:00):** 
$$x_1 + x_6 \geq 12$$

2. **Period 2 (02:00–06:00):** 
$$x_1 + x_2 \geq 10$$

3. **Period 3 (06:00–10:00):** 
$$x_2 + x_3 \geq 15$$

4. **Period 4 (10:00–14:00):** 
$$x_3 + x_4 \geq 25$$

5. **Period 5 (14:00–18:00):** 
$$x_4 + x_5 \geq 20$$

6. **Period 6 (18:00–22:00):** 
$$x_5 + x_6 \geq 18$$

**Non-negativity & Integrality:**
$$x_s \geq 0, \quad x_s \in \mathbb{Z} \quad \forall s = 1, \dots, 6$$