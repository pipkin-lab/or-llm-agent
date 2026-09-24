# Assembly Line Worker Assignment — Bottleneck Optimization

**Model Type:** MILP (Mixed-Integer Linear Program)

> **Critical Modeling Note (Rule 15):** This is a **serial assembly line** where every unit must pass through all 5 stations in sequence. The overall production capacity is limited by the **bottleneck** (slowest) station, NOT the sum of station rates. Therefore, the objective is to **maximize the minimum station throughput**, not the sum of efficiencies.

---

## MANDATORY COST INVENTORY (PRE-MODELING STEP)

This problem does not involve costs to minimize; it involves **efficiency values** (pieces/min) to maximize the bottleneck. The efficiency matrix is:

| Worker | St. I | St. II | St. III | St. IV | St. V |
|--------|-------|--------|---------|--------|-------|
| A      | 2     | 3      | 4       | 1      | 7     |
| B      | 3     | 4      | 2       | 5      | 6     |
| C      | 2     | 5      | 3       | 4      | 1     |
| D      | 5     | 2      | 3       | 2      | 5     |
| E      | 3     | 7      | 6       | 2      | 4     |

All 25 efficiency values are extracted and will serve as constraint coefficients.

---

## Index Sets & Parameters

- **Workers:** $W = \{A, B, C, D, E\}$, indexed by $i = 1, 2, 3, 4, 5$
- **Stations:** $S = \{I, II, III, IV, V\}$, indexed by $j = 1, 2, 3, 4, 5$
- **Efficiency parameter:** $e_{i,j}$ = production rate (pieces/min) of worker $i$ at station $j$, as given in the table above.

---

## Decision Variables

- $x_{i,j} \in \{0, 1\}$ for all $i \in W, j \in S$:
  - $x_{i,j} = 1$ if worker $i$ is assigned to station $j$, else $0$.
- $Z \geq 0$ (continuous):
  - Represents the overall production capacity of the assembly line (bottleneck rate, pieces/min).

---

## Objective Function

$$\max \quad Z$$

> **Rule 15 Verification:** If one station has rate 2 and all others have rate 7, the objective correctly yields $Z = 2$ (the bottleneck limits the whole line). This confirms the min-max (bottleneck) formulation is appropriate.

---

## Operational Constraints

### 1. Each worker is assigned to exactly one station
$$\sum_{j=1}^{5} x_{i,j} = 1 \quad \forall \, i \in W$$

### 2. Each station is staffed by exactly one worker
$$\sum_{i=1}^{5} x_{i,j} = 1 \quad \forall \, j \in S$$

### 3. Bottleneck constraints (each station's rate must meet or exceed Z)
$$\sum_{i=1}^{5} e_{i,j} \, x_{i,j} \geq Z \quad \forall \, j \in S$$

Expanded explicitly for each station:

- **Station I:** $2x_{A,1} + 3x_{B,1} + 2x_{C,1} + 5x_{D,1} + 3x_{E,1} \geq Z$
- **Station II:** $3x_{A,2} + 4x_{B,2} + 5x_{C,2} + 2x_{D,2} + 7x_{E,2} \geq Z$
- **Station III:** $4x_{A,3} + 2x_{B,3} + 3x_{C,3} + 3x_{D,3} + 6x_{E,3} \geq Z$
- **Station IV:** $1x_{A,4} + 5x_{B,4} + 4x_{C,4} + 2x_{D,4} + 2x_{E,4} \geq Z$
- **Station V:** $7x_{A,5} + 6x_{B,5} + 1x_{C,5} + 5x_{D,5} + 4x_{E,5} \geq Z$

### 4. Non-negativity / domain bounds
$$x_{i,j} \in \{0, 1\} \quad \forall \, i \in W, \, j \in S$$
$$Z \geq 0$$

---

## FEASIBILITY SANITY CHECK

- This is a standard 5×5 assignment problem with 5! = 120 possible assignments, so feasible solutions exist.
- The bottleneck $Z$ will be bounded above by the minimum over stations of the best single-worker efficiency at that station:
  - St. I: max = 5 (D), St. II: max = 7 (E), St. III: max = 6 (E), St. IV: max = 5 (B), St. V: max = 7 (A)
  - So $Z \leq \min(5, 7, 6, 5, 7) = 5$.
- The optimal $Z^*$ will be the maximum bottleneck achievable across all valid permutations.

**Expected answer magnitude:** A single-digit number (between 1 and 5), consistent with the "pieces/min" unit and the bottleneck nature of a serial line. No normalization division is needed — the question asks for the overall production capacity in pieces/min, which is exactly $Z$.