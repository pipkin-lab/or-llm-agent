# Mathematical Formulation: Transportation Problem

## MANDATORY COST INVENTORY (PRE-MODELING STEP)

The problem provides a **unit transportation cost table** (cost per unit shipped from origin $i$ to destination $j$). These are the objective coefficients. There are 4 origins and 6 destinations, yielding 24 distinct unit costs, all explicitly given in Table 3-8. No other costs (fixed charges, penalties, etc.) are mentioned. The objective is to **minimize** total transportation cost.

**Supply-Demand Balance Check:**
- Total Supply = 50 + 40 + 60 + 31 = **181**
- Total Demand = 30 + 50 + 20 + 40 + 30 + 11 = **181**
- Supply = Demand → **Balanced** transportation problem.

---

## Model Type Declaration

**LP** (Linear Program). All variables are continuous (shipment quantities), the objective and all constraints are linear. A standard LP solver suffices.

---

## Index Sets & Parameters

| Symbol | Description |
|--------|-------------|
| $I = \{1, 2, 3, 4\}$ | Set of origins (suppliers) |
| $J = \{1, 2, 3, 4, 5, 6\}$ | Set of destinations (consumers) |
| $a_i$ | Supply at origin $i$ |
| $b_j$ | Demand at destination $j$ |
| $c_{ij}$ | Unit transportation cost from origin $i$ to destination $j$ |

### Parameter Values (from Table 3-8)

**Supply vector** $a_i$:

| $i$ | 1 (A1) | 2 (A2) | 3 (A3) | 4 (A4) |
|-----|--------|--------|--------|--------|
| $a_i$ | 50 | 40 | 60 | 31 |

**Demand vector** $b_j$:

| $j$ | 1 (B1) | 2 (B2) | 3 (B3) | 4 (B4) | 5 (B5) | 6 (B6) |
|-----|--------|--------|--------|--------|--------|--------|
| $b_j$ | 30 | 50 | 20 | 40 | 30 | 11 |

**Unit cost matrix** $c_{ij}$:

| $c_{ij}$ | B1 | B2 | B3 | B4 | B5 | B6 |
|----------|----|----|----|----|----|----|
| **A1** ($i=1$) | 2 | 1 | 3 | 3 | 3 | 5 |
| **A2** ($i=2$) | 4 | 2 | 2 | 4 | 4 | 4 |
| **A3** ($i=3$) | 3 | 5 | 4 | 2 | 4 | 1 |
| **A4** ($i=4$) | 4 | 2 | 2 | 1 | 2 | 2 |

---

## Decision Variables

$$x_{ij} = \text{quantity shipped from origin } i \in I \text{ to destination } j \in J$$

**Domain:** $x_{ij} \geq 0 \quad \forall\, i \in I,\; j \in J$

(Continuous variables — shipment quantities are not required to be integer in this problem.)

---

## Objective Function

$$\min \; Z = \sum_{i=1}^{4} \sum_{j=1}^{6} c_{ij} \, x_{ij}$$

Expanded:

$$\min \; Z = 2x_{11} + 1x_{12} + 3x_{13} + 3x_{14} + 3x_{15} + 5x_{16}$$
$$+ 4x_{21} + 2x_{22} + 2x_{23} + 4x_{24} + 4x_{25} + 4x_{26}$$
$$+ 3x_{31} + 5x_{32} + 4x_{33} + 2x_{34} + 4x_{35} + 1x_{36}$$
$$+ 4x_{41} + 2x_{42} + 2x_{43} + 1x_{44} + 2x_{45} + 2x_{46}$$

**Objective Parameter Cross-Reference:** Every $c_{ij}$ appearing in the objective has an explicit numeric value from Table 3-8. No parameter is `[NOT_PROVIDED]`.

---

## Operational Constraints

### 1. Supply (Source) Constraints — Equality (Rule 9: Supply = Demand, balanced)

Each unit of supply must be fully allocated (shipped). Since total supply equals total demand, these are **equalities**:

$$\sum_{j=1}^{6} x_{ij} = a_i \quad \forall\, i \in I$$

Explicitly:

$$\begin{aligned}
x_{11} + x_{12} + x_{13} + x_{14} + x_{15} + x_{16} &= 50 \\
x_{21} + x_{22} + x_{23} + x_{24} + x_{25} + x_{26} &= 40 \\
x_{31} + x_{32} + x_{33} + x_{34} + x_{35} + x_{36} &= 60 \\
x_{41} + x_{42} + x_{43} + x_{44} + x_{45} + x_{46} &= 31
\end{aligned}$$

### 2. Demand (Destination) Constraints — Equality (balanced)

All demand must be met exactly:

$$\sum_{i=1}^{4} x_{ij} = b_j \quad \forall\, j \in J$$

Explicitly:

$$\begin{aligned}
x_{11} + x_{21} + x_{31} + x_{41} &= 30 \\
x_{12} + x_{22} + x_{32} + x_{42} &= 50 \\
x_{13} + x_{23} + x_{33} + x_{43} &= 20 \\
x_{14} + x_{24} + x_{34} + x_{44} &= 40 \\
x_{15} + x_{25} + x_{35} + x_{45} &= 30 \\
x_{16} + x_{26} + x_{36} + x_{46} &= 11
\end{aligned}$$

### 3. Non-negativity

$$x_{ij} \geq 0 \quad \forall\, i \in I,\; j \in J$$

---

## Feasibility Sanity Check (Rule 7)

- Total supply (181) = Total demand (181) → balanced, feasible.
- No additional capacity, fixed-charge, or lower-bound constraints are imposed.
- The constraint matrix is a standard transportation tableau (totally unimodular), so if an integer solution is desired, integrality holds automatically at any LP basic feasible solution.

## Final Magnitude Sanity Check (Rule 11)

The problem asks for the **optimal transportation plan** (the allocation $x_{ij}$) and implicitly the **minimum total cost** $Z$. The objective is in the same units as the given cost table (cost units per shipment unit). No normalization or division is needed — the answer is the raw total cost in the problem's native units. A greedy/inspection estimate: the cheapest routes are $c_{36}=1$, $c_{12}=1$, $c_{44}=1$, etc. The optimal total cost will be on the order of a few hundred (e.g., roughly 181 × average cost ≈ 181 × 2.5 ≈ 450), which is a sensible magnitude. No missing normalization factor is suspected.