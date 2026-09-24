## MANDATORY COST INVENTORY (PRE-MODELING STEP)

The problem asks to **minimize total expected accidents**. The "cost" coefficients are the accident counts in Table 7-11.

| Patrol Units | Warehouse 1 | Warehouse 2 | Warehouse 3 | Warehouse 4 |
|:---:|:---:|:---:|:---:|:---:|
| 2 | 18 | 38 | 14 | 34 |
| 3 | 16 | 36 | 12 | 31 |
| 4 | 12 | 30 | 11 | 25 |

All 12 cost figures are present. Each warehouse has 3 possible assignments (2, 3, or 4 units). The decision is which integer count (2, 3, or 4) to assign to each warehouse such that the total equals 12 and the sum of accidents is minimized.

## MODEL TYPE

**MILP** (Multi-Integer Linear Programming) — all variables are integer-valued, objective and constraints are linear.

===============================================================================

## Index Sets & Parameters

**Sets:**
- $W = \{1, 2, 3, 4\}$: Set of warehouses.
- $K = \{2, 3, 4\}$: Set of allowable patrol unit assignments per warehouse.

**Parameters (expected annual accidents):**

| $c_{w,k}$ | $k=2$ | $k=3$ | $k=4$ |
|:---:|:---:|:---:|:---:|
| $w=1$ | 18 | 16 | 12 |
| $w=2$ | 38 | 36 | 30 |
| $w=3$ | 14 | 12 | 11 |
| $w=4$ | 34 | 31 | 25 |

**Global Parameters:**
- $N = 12$: Total number of patrol units.
- $k_{\min} = 2$, $k_{\max} = 4$: Bounds on units per warehouse.

===============================================================================

## Decision Variables

For each warehouse $w \in W$ and each allowable assignment level $k \in K$, define a binary variable:

$$x_{w,k} = \begin{cases} 1 & \text{if } k \text{ patrol units are assigned to warehouse } w \\ 0 & \text{otherwise} \end{cases} \quad \forall w \in W,\; k \in \{2,3,4\}$$

**Domain:** $x_{w,k} \in \{0, 1\}$ (binary / integer).

The actual number of units assigned to warehouse $w$ is recovered as:
$$n_w = \sum_{k \in K} k \cdot x_{w,k}$$

===============================================================================

## Objective Function

**MINIMIZE** the total expected number of accidents per year:

$$\min \; Z = \sum_{w=1}^{4} \sum_{k \in \{2,3,4\}} c_{w,k} \cdot x_{w,k}$$

Expanded:
$$Z = 18x_{1,2} + 16x_{1,3} + 12x_{1,4} + 38x_{2,2} + 36x_{2,3} + 30x_{2,4} + 14x_{3,2} + 12x_{3,3} + 11x_{3,4} + 34x_{4,2} + 31x_{4,3} + 25x_{4,4}$$

===============================================================================

## Operational Constraints

**1. Exactly one assignment level per warehouse** (each warehouse receives exactly one of the valid unit counts):

$$\sum_{k \in \{2,3,4\}} x_{w,k} = 1 \quad \forall w \in \{1, 2, 3, 4\}$$

i.e.,
- $x_{1,2} + x_{1,3} + x_{1,4} = 1$
- $x_{2,2} + x_{2,3} + x_{2,4} = 1$
- $x_{3,2} + x_{3,3} + x_{3,4} = 1$
- $x_{4,2} + x_{4,3} + x_{4,4} = 1$

**2. Total patrol units constraint** (all 12 units must be allocated):

$$\sum_{w=1}^{4} \sum_{k \in \{2,3,4\}} k \cdot x_{w,k} = 12$$

Expanded:
$$2(x_{1,2}+x_{2,2}+x_{3,2}+x_{4,2}) + 3(x_{1,3}+x_{2,3}+x_{3,3}+x_{4,3}) + 4(x_{1,4}+x_{2,4}+x_{3,4}+x_{4,4}) = 12$$

**3. Variable domains:**

$$x_{w,k} \in \{0, 1\} \quad \forall w \in W,\; k \in \{2,3,4\}$$

===============================================================================

## Feasibility Sanity Check

- **Lower bound on total units:** $4 \times 2 = 8$
- **Upper bound on total units:** $4 \times 4 = 16$
- **Required total:** $12$

Since $8 \leq 12 \leq 16$, the constraint system is feasible. The problem admits multiple feasible integer allocations (e.g., $\{3,3,3,3\}$, $\{2,3,3,4\}$, $\{2,2,4,4\}$, etc.).

===============================================================================

## Objective Parameter Cross-Reference

Every coefficient in the objective is accounted for:

| Symbol | Value | Source |
|:---:|:---:|:---:|
| $c_{1,2}$ | 18 | Table 7-11, row "2", col "1" |
| $c_{1,3}$ | 16 | Table 7-11, row "3", col "1" |
| $c_{1,4}$ | 12 | Table 7-11, row "4", col "1" |
| $c_{2,2}$ | 38 | Table 7-11, row "2", col "2" |
| $c_{2,3}$ | 36 | Table 7-11, row "3", col "2" |
| $c_{2,4}$ | 30 | Table 7-11, row "4", col "2" |
| $c_{3,2}$ | 14 | Table 7-11, row "2", col "3" |
| $c_{3,3}$ | 12 | Table 7-11, row "3", col "3" |
| $c_{3,4}$ | 11 | Table 7-11, row "4", col "3" |
| $c_{4,2}$ | 34 | Table 7-11, row "2", col "4" |
| $c_{4,3}$ | 31 | Table 7-11, row "3", col "4" |
| $c_{4,4}$ | 25 | Table 7-11, row "4", col "4" |

All 12 objective parameters are confirmed present. No parameter is marked [NOT_PROVIDED].

===============================================================================

## Magnitude Sanity Check

Greedy / trivial solution: assign all warehouses 3 units → total = 12 units (feasible).
$$Z_{\text{greedy}} = 16 + 36 + 12 + 31 = 95$$

Another feasible solution: $\{4, 4, 2, 2\}$ → total = 12.
$$Z = 12 + 30 + 14 + 34 = 90$$

Another: $\{4, 3, 3, 2\}$ → total = 12.
$$Z = 12 + 36 + 12 + 34 = 94$$

Another: $\{4, 4, 3, 1\}$ — infeasible (min 2 per warehouse).

Another: $\{3, 4, 3, 2\}$ → total = 12.
$$Z = 16 + 30 + 12 + 34 = 92$$

The objective values are in the range of 80–100, which is consistent with the scale of the input data (individual accident counts are 11–38). No normalization is needed; the answer is the raw sum of expected accidents. ✓