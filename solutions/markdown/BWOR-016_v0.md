## Model Type
**MILP** (Mixed-Integer Linear Program)

## Index Sets & Parameters

**Index Sets:**
- $I = \{1, 2, 3, 4\}$: Set of potential factories ($A_1, A_2, A_3, A_4$)
- $J = \{1, 2, 3, 4\}$: Set of demand locations ($B_1, B_2, B_3, B_4$)

**Parameters:**
- $c_{ij}$: Unit transportation cost from factory $i$ to location $j$ (thousand yuan/kt).
  - $c_{11}=2, c_{12}=9, c_{13}=3, c_{14}=4$
  - $c_{21}=8, c_{22}=3, c_{23}=5, c_{24}=7$
  - $c_{31}=7, c_{32}=6, c_{33}=1, c_{34}=2$
  - $c_{41}=4, c_{42}=5, c_{43}=2, c_{44}=5$
- $S_i$: Annual production capacity of factory $i$ (kt/year).
  - $S_1 = 400, S_2 = 600, S_3 = 200, S_4 = 200$
- $D_j$: Annual demand at location $j$ (kt/year).
  - $D_1 = 350, D_2 = 400, D_3 = 300, D_4 = 150$
- $F_i$: Annual fixed production cost of new factory $i$ (thousand yuan).
  - $F_3 = 1200, F_4 = 1500$
  - $F_1 = 0, F_2 = 0$ (Existing factories have no new fixed cost in this context)

**Total Supply:** $400 + 600 + 200 + 200 = 1400$ kt/year
**Total Demand:** $350 + 400 + 300 + 150 = 1200$ kt/year
*Note: Total Supply (1400) > Total Demand (1200).*

## Decision Variables

1.  **Binary Variables (Factory Selection):**
    -   $y_i \in \{0, 1\}$ for $i \in \{3, 4\}$:
        -   $y_i = 1$ if factory $A_i$ is built/selected.
        -   $y_i = 0$ otherwise.
    -   *Constraint:* Exactly one of $A_3$ or $A_4$ must be built.

2.  **Continuous Variables (Transportation Flows):**
    -   $x_{ij} \ge 0$ for $i \in \{1, 2, 3, 4\}, j \in \{1, 2, 3, 4\}$:
        -   Amount of material transported from factory $i$ to location $j$ (kt/year).

## Objective Function

Minimize the total annual cost (in thousand yuan), which includes transportation costs and the fixed production cost of the selected new factory.

$$
\text{Minimize } Z = \sum_{i=1}^{4} \sum_{j=1}^{4} c_{ij} x_{ij} + F_3 y_3 + F_4 y_4
$$

Substituting the numerical values:
$$
Z = 2x_{11} + 9x_{12} + 3x_{13} + 4x_{14} + 8x_{21} + 3x_{22} + 5x_{23} + 7x_{24} + 7x_{31} + 6x_{32} + 1x_{33} + 2x_{34} + 4x_{41} + 5x_{42} + 2x_{43} + 5x_{44} + 1200 y_3 + 1500 y_4
$$

## Operational Constraints

**1. Demand Satisfaction Constraints:**
The total amount of material received at each location $j$ must exactly meet the demand $D_j$.
$$
\sum_{i=1}^{4} x_{ij} = D_j, \quad \forall j \in J
$$
Explicitly:
-   $x_{11} + x_{21} + x_{31} + x_{41} = 350$
-   $x_{12} + x_{22} + x_{32} + x_{42} = 400$
-   $x_{13} + x_{23} + x_{33} + x_{43} = 300$
-   $x_{14} + x_{24} + x_{34} + x_{44} = 150$

**2. Capacity Constraints:**
The total amount of material shipped from each factory $i$ cannot exceed its production capacity $S_i$.
*Note: For the new factories $A_3$ and $A_4$, the capacity is only available if the factory is built. This is handled by linking $x_{ij}$ to $y_i$.*

For existing factories ($i=1, 2$):
$$
\sum_{j=1}^{4} x_{ij} \le S_i, \quad i \in \{1, 2\}
$$
-   $x_{11} + x_{12} + x_{13} + x_{14} \le 400$
-   $x_{21} + x_{22} + x_{23} + x_{24} \le 600$

For new factories ($i=3, 4$):
$$
\sum_{j=1}^{4} x_{ij} \le S_i y_i, \quad i \in \{3, 4\}
$$
-   $x_{31} + x_{32} + x_{33} + x_{34} \le 200 y_3$
-   $x_{41} + x_{42} + x_{43} + x_{44} \le 200 y_4$

**3. Factory Selection Constraint:**
Exactly one new factory must be built.
$$
y_3 + y_4 = 1
$$

**4. Non-negativity and Integrality Constraints:**
$$
x_{ij} \ge 0, \quad \forall i \in I, j \in J
$$
$$
y_3, y_4 \in \{0, 1\}
$$