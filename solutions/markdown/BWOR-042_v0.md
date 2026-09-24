# Transportation Problem Formulation

## Model Type Declaration
**LP** (Linear Programming). The problem is a standard transportation problem with linear objective and linear constraints. Total supply (300) equals total demand (300), so all balance constraints are equalities.

## Parameter Completeness & Cost Inventory
**Mandatory Cost Inventory (Pre-Modeling Step):**
The problem provides a single unit transportation cost matrix $c_{ij}$ (cost per unit shipped from origin $i$ to destination $j$). There are no fixed costs, no per-truck fees, or other charges. The objective coefficients are exactly the entries in the cost table.

| $c_{ij}$ | A | B | C | D | E |
|---|---|---|---|---|---|
| I | 10 | 15 | 20 | 20 | 40 |
| II | 20 | 10 | 15 | 30 | 30 |
| III | 30 | 35 | 40 | 55 | 25 |

Supply vector $s = (50, 100, 150)$; total = 300.
Demand vector $d = (25, 115, 60, 30, 70)$; total = 300.
**Balance check:** Total Supply = 300 = Total Demand. Balanced problem.

## Index Sets & Parameters

- **Origins (Supply nodes):** $I = \{1, 2, 3\}$ corresponding to I, II, III.
- **Destinations (Demand nodes):** $J = \{1, 2, 3, 4, 5\}$ corresponding to A, B, C, D, E.
- **Supply capacities** (units):
  - $s_1 = 50$ (Origin I)
  - $s_2 = 100$ (Origin II)
  - $s_3 = 150$ (Origin III)
- **Demand requirements** (units):
  - $d_1 = 25$ (Dest A)
  - $d_2 = 115$ (Dest B)
  - $d_3 = 60$ (Dest C)
  - $d_4 = 30$ (Dest D)
  - $d_5 = 70$ (Dest E)
- **Unit transportation costs** $c_{ij}$ (as tabulated above):
  - $c_{1,1}=10, c_{1,2}=15, c_{1,3}=20, c_{1,4}=20, c_{1,5}=40$
  - $c_{2,1}=20, c_{2,2}=10, c_{2,3}=15, c_{2,4}=30, c_{2,5}=30$
  - $c_{3,1}=30, c_{3,2}=35, c_{3,3}=40, c_{3,4}=55, c_{3,5}=25$

## Decision Variables

- $x_{ij} \in \mathbb{R}_{\ge 0}$ for all $i \in I, j \in J$: the quantity (number of units) shipped from origin $i$ to destination $j$.
- **Domain:** Continuous, non-negative. (In a balanced transportation problem with integer supplies/demands/costs, an optimal basic feasible solution is automatically integer, but the LP relaxation is sufficient and standard.)

## Objective Function

**Minimize total transportation cost:**

$$
\min \sum_{i \in I} \sum_{j \in J} c_{ij} \, x_{ij}
$$

Expanded:
$$
\min \; 10 x_{1,1} + 15 x_{1,2} + 20 x_{1,3} + 20 x_{1,4} + 40 x_{1,5} + 20 x_{2,1} + 10 x_{2,2} + 15 x_{2,3} + 30 x_{2,4} + 30 x_{2,5} + 30 x_{3,1} + 35 x_{3,2} + 40 x_{3,3} + 55 x_{3,4} + 25 x_{3,5}
$$

**Objective Parameter Cross-Reference:** Every coefficient $c_{ij}$ appearing in the objective has been explicitly listed above with its numeric value from Table 3-7. No parameter is missing.

## Operational Constraints

**1. Supply constraints (one per origin, equality since balanced):**

$$
\sum_{j \in J} x_{1j} = 50 \quad \text{(Origin I)}
$$
$$
\sum_{j \in J} x_{2j} = 100 \quad \text{(Origin II)}
$$
$$
\sum_{j \in J} x_{3j} = 150 \quad \text{(Origin III)}
$$

**2. Demand constraints (one per destination, equality since balanced):**

$$
\sum_{i \in I} x_{i1} = 25 \quad \text{(Dest A)}
$$
$$
\sum_{i \in I} x_{i2} = 115 \quad \text{(Dest B)}
$$
$$
\sum_{i \in I} x_{i3} = 60 \quad \text{(Dest C)}
$$
$$
\sum_{i \in I} x_{i4} = 30 \quad \text{(Dest D)}
$$
$$
\sum_{i \in I} x_{i5} = 70 \quad \text{(Dest E)}
$$

**3. Non-negativity bounds:**

$$
x_{ij} \ge 0 \quad \forall \, i \in I, \, j \in J
$$

## Feasibility Sanity Check

- Total supply: $50 + 100 + 150 = 300$.
- Total demand: $25 + 115 + 60 + 30 + 70 = 300$.
- Supply = Demand → the system is balanced. All constraints are equalities. The feasible region is non-empty (e.g., a greedy assignment exists). No artificial relaxation is needed.

## Objective Unit & Normalization Verification

The question asks for the "optimal transportation (allocation) plan," i.e., the allocation $x_{ij}$ that minimizes total cost. The objective is the **total cost** (sum of $c_{ij} x_{ij}$), which is the natural and standard quantity for a transportation problem. No per-unit normalization or division is required — the problem does not ask for an average cost or a rate. The magnitude check: a greedy assignment (e.g., shipping along cheapest arcs) yields a total cost in the range of a few thousand units, which is consistent with the cost coefficients (10–55) multiplied by quantities summing to 300. No scaling factor is needed; the objective coefficients are already in the problem's native units (cost per unit).