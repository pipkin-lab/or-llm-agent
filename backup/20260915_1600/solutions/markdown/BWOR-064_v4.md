# Mathematical Optimization Model

## Model Type: **MILP** (Mixed-Integer Linear Program)

---

## Index Sets & Parameters

**Sets:**
- $I = \{1, 2, 3\}$: set of factories
- $J_i$: set of available plans for factory $i$ (excluding the "do nothing" plan, which is implicit)
  - $J_1 = \{2, 3\}$ (plans requiring 1 or 2 million yuan)
  - $J_2 = \{2, 3, 4\}$ (plans requiring 2, 3, or 4 million yuan)
  - $J_3 = \{2\}$ (plan requiring 1 million yuan)

**Parameters (all in million yuan):**

| $i$ (Factory) | Plan $j$ | Investment $c_{ij}$ | Return $r_{ij}$ |
|:---:|:---:|:---:|:---:|
| 1 | 2 | 1 | 5 |
| 1 | 3 | 2 | 6 |
| 2 | 2 | 2 | 8 |
| 2 | 3 | 3 | 9 |
| 2 | 4 | 4 | 12 |
| 3 | 2 | 1 | 3 |

**Global Parameter:**
- $B = 5$: total available budget (million yuan)

---

## Decision Variables

For each factory $i \in I$ and each available plan $j \in J_i$:

$$x_{ij} \in \{0, 1\}$$

where $x_{ij} = 1$ if factory $i$ selects plan $j$, and $0$ otherwise.

**Domain:** All $x_{ij}$ are binary (INTEGER, 0/1).

---

## Objective Function

**MAXIMIZE** total expected return:

$$\max \; Z = \sum_{i=1}^{3} \sum_{j \in J_i} r_{ij} \, x_{ij}$$

Expanding explicitly:

$$Z = 5x_{1,2} + 6x_{1,3} + 8x_{2,2} + 9x_{2,3} + 12x_{2,4} + 3x_{3,2}$$

---

## Operational Constraints

### 1. Budget Constraint (Total investment ≤ available budget)

$$\sum_{i=1}^{3} \sum_{j \in J_i} c_{ij} \, x_{ij} \leq B$$

Expanded:

$$1 \cdot x_{1,2} + 2 \cdot x_{1,3} + 2 \cdot x_{2,2} + 3 \cdot x_{2,3} + 4 \cdot x_{2,4} + 1 \cdot x_{3,2} \leq 5$$

### 2. Mutual Exclusivity (At most one plan per factory)

Since each factory can adopt **at most one** expansion plan (or none):

$$\sum_{j \in J_i} x_{ij} \leq 1, \quad \forall i \in I$$

Explicitly:
- Factory 1: $\quad x_{1,2} + x_{1,3} \leq 1$
- Factory 2: $\quad x_{2,2} + x_{2,3} + x_{2,4} \leq 1$
- Factory 3: $\quad x_{3,2} \leq 1$

### 3. Non-negativity / Domain Bounds

$$x_{ij} \in \{0, 1\}, \quad \forall i \in I, \; j \in J_i$$

---

## Feasibility Sanity Check

- **Total budget:** 5 million yuan.
- **Maximum possible investment if all best plans were selected:** e.g., $x_{1,3}=1$ (2), $x_{2,4}=1$ (4), $x_{3,2}=1$ (1) → total = 7 > 5. So the budget constraint is binding and will restrict combinations.
- **Minimum investment for any single plan:** 1 million yuan. Since $B=5$, at least one plan can always be funded. The model is feasible (e.g., select only $x_{3,2}=1$ with cost 1 ≤ 5).
- No contradictory constraints are present.

## Objective Magnitude Sanity Check

A greedy hand-calculation:
- Best single plan: $x_{2,4}=1$ → return 12, cost 4. Remaining budget: 1. Can add $x_{3,2}=1$ (cost 1, return 3) or $x_{1,2}=1$ (cost 1, return 5). Best: add $x_{1,2}$.
- Total return: $12 + 5 = 17$, total cost: $4+1=5 \leq 5$. ✓
- Alternative: $x_{2,3}=1$ (cost 3, return 9) + $x_{1,2}=1$ (cost 1, return 5) + $x_{3,2}=1$ (cost 1, return 3) → return 17, cost 5. Same.
- Alternative: $x_{1,3}=1$ (cost 2, return 6) + $x_{2,2}=1$ (cost 2, return 8) + $x_{3,2}=1$ (cost 1, return 3) → return 17, cost 5. Same.

Expected optimal objective: **Z* = 17** (million yuan). This is a reasonable magnitude for the problem scale.