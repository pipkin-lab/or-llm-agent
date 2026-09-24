# Nurse Scheduling with Full-Time and Contract Nurses

## Model Type: MILP (Mixed Integer Linear Program)

## Pre-Modeling: Cost Inventory & Parameter Extraction

**Costs identified in text:**
- Full-time nurse wage: ¥10/hour → 8-hour shift cost = ¥80 per nurse per shift
- Contract nurse wage: ¥15/hour → 8-hour shift cost = ¥120 per nurse per shift

**Demand parameters (nurses required per 4-hour block):**
| Block | Time | Demand |
|-------|------|--------|
| b1 | 2:00–6:00 | 10 |
| b2 | 6:00–10:00 | 15 |
| b3 | 10:00–14:00 | 25 |
| b4 | 14:00–18:00 | 20 |
| b5 | 18:00–22:00 | 18 |
| b6 | 22:00–2:00 | 12 |

**Shift definitions (each nurse works 8 consecutive hours = 2 blocks):**
- Shift S1: starts 2:00 → covers b1, b2
- Shift S2: starts 6:00 → covers b2, b3
- Shift S3: starts 10:00 → covers b3, b4
- Shift S4: starts 14:00 → covers b4, b5
- Shift S5: starts 18:00 → covers b5, b6
- Shift S6: starts 22:00 → covers b6, b1

## Index Sets & Parameters

**Index Sets:**
- $S = \{1, 2, 3, 4, 5, 6\}$: set of 6 shifts
- $B = \{1, 2, 3, 4, 5, 6\}$: set of 6 four-hour time blocks

**Parameters:**
- $d_b$: minimum nurses required in block $b$
  - $d_1 = 10,\ d_2 = 15,\ d_3 = 25,\ d_4 = 20,\ d_5 = 18,\ d_6 = 12$
- $c_{FT} = 80$: cost of one full-time nurse for one 8-hour shift (¥10/hr × 8 hr)
- $c_{CT} = 120$: cost of one contract nurse for one 8-hour shift (¥15/hr × 8 hr)
- $a_{s,b} \in \{0, 1\}$: shift-block incidence matrix:
  - $a_{1,1}=1, a_{1,2}=1$ (S1 covers b1, b2)
  - $a_{2,2}=1, a_{2,3}=1$ (S2 covers b2, b3)
  - $a_{3,3}=1, a_{3,4}=1$ (S3 covers b3, b4)
  - $a_{4,4}=1, a_{4,5}=1$ (S4 covers b4, b5)
  - $a_{5,5}=1, a_{5,6}=1$ (S5 covers b5, b6)
  - $a_{6,6}=1, a_{6,1}=1$ (S6 covers b6, b1)

## Decision Variables

- $x_s$: number of **full-time** nurses assigned to shift $s$, for all $s \in S$. Domain: $x_s \in \mathbb{Z}_{\geq 0}$
- $y_s$: number of **contract** nurses assigned to shift $s$, for all $s \in S$. Domain: $y_s \in \mathbb{Z}_{\geq 0}$

## Objective Function

**MINIMIZE** total labor cost:

$$\min \sum_{s \in S} \left( 80 \cdot x_s + 120 \cdot y_s \right)$$

## Operational Constraints

**Coverage constraints** (for each time block $b \in B$, the total nurses on duty must meet or exceed the requirement):

$$\sum_{s \in S} a_{s,b} \left( x_s + y_s \right) \geq d_b, \quad \forall b \in B$$

Expanded explicitly:

- **Block b1 (2:00–6:00):** $x_1 + y_1 + x_6 + y_6 \geq 10$
- **Block b2 (6:00–10:00):** $x_1 + y_1 + x_2 + y_2 \geq 15$
- **Block b3 (10:00–14:00):** $x_2 + y_2 + x_3 + y_3 \geq 25$
- **Block b4 (14:00–18:00):** $x_3 + y_3 + x_4 + y_4 \geq 20$
- **Block b5 (18:00–22:00):** $x_4 + y_4 + x_5 + y_5 \geq 18$
- **Block b6 (22:00–2:00):** $x_5 + y_5 + x_6 + y_6 \geq 12$

**Non-negativity and integrality:**

$$x_s \in \mathbb{Z}_{\geq 0}, \quad y_s \in \mathbb{Z}_{\geq 0}, \quad \forall s \in S$$

## Feasibility Sanity Check

Total demand across all 6 blocks = 10+15+25+20+18+12 = 100 nurse-blocks. Since each nurse works exactly 2 blocks, the minimum total nurse-shifts needed (ignoring the discrete shift structure) is 100/2 = 50. The most demanding block is b3 with 25 nurses, requiring at least 25 nurses on shifts S2 and S3 combined. The problem is feasible (e.g., all full-time nurses can satisfy all constraints). Since contract nurses are more expensive (¥120 vs ¥80 per shift), the optimal solution will use contract nurses **only if** the shift structure forces it — but since any nurse (FT or contract) can work any shift and the only difference is cost, the optimal solution will use **zero contract nurses** (set all $y_s = 0$) and solve the standard single-type nurse scheduling problem with full-time nurses only. Contract nurses are never beneficial because they are strictly more expensive and have identical coverage properties.

## Objective Parameter Cross-Reference

| Parameter | Symbol | Value | Source in text |
|-----------|--------|-------|----------------|
| FT shift cost | $c_{FT}$ | 80 | "Full-time nurse = ¥10/hour" × 8 hours |
| CT shift cost | $c_{CT}$ | 120 | "Contract nurse = ¥15/hour" × 8 hours |
| Demand b1 | $d_1$ | 10 | "2:00~6:00 → 10 nurses" |
| Demand b2 | $d_2$ | 15 | "6:00~10:00 → 15 nurses" |
| Demand b3 | $d_3$ | 25 | "10:00~14:00 → 25 nurses" |
| Demand b4 | $d_4$ | 20 | "14:00~18:00 → 20 nurses" |
| Demand b5 | $d_5$ | 18 | "18:00~22:00 → 18 nurses" |
| Demand b6 | $d_6$ | 12 | "22:00~2:00 → 12 nurses" |

All parameters are fully specified. No [NOT_PROVIDED] values.