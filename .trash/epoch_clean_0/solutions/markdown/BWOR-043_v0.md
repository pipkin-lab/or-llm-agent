### 1. Index Sets & Parameters

**Index Sets:**
- $I = \{1, 2, 3, 4\}$: Set of supply origins (A1, A2, A3, A4).
- $J = \{1, 2, 3, 4, 5, 6\}$: Set of demand destinations (B1, B2, B3, B4, B5, B6).

**Parameters:**
- $S_i$: Supply capacity at origin $i$.
  - $S_1 = 50$ (A1)
  - $S_2 = 40$ (A2)
  - $S_3 = 60$ (A3)
  - $S_4 = 31$ (A4)
  - Total Supply = 181

- $D_j$: Demand requirement at destination $j$.
  - $D_1 = 30$ (B1)
  - $D_2 = 50$ (B2)
  - $D_3 = 20$ (B3)
  - $D_4 = 40$ (B4)
  - $D_5 = 30$ (B5)
  - $D_6 = 11$ (B6)
  - Total Demand = 181

- $C_{ij}$: Unit transportation cost from origin $i$ to destination $j$.
  - Row 1 (A1): $[2, 1, 3, 3, 3, 5]$
  - Row 2 (A2): $[4, 2, 2, 4, 4, 4]$
  - Row 3 (A3): $[3, 5, 4, 2, 4, 1]$
  - Row 4 (A4): $[4, 2, 2, 1, 2, 2]$

*Note: Total Supply (181) equals Total Demand (181), so this is a balanced transportation problem. No dummy nodes are required.*

### 2. Decision Variables

- $x_{ij} \in \mathbb{R}^+$: The quantity of goods transported from origin $i \in I$ to destination $j \in J$.
  - Domain: $x_{ij} \ge 0$ for all $i \in I, j \in J$.
  - *Modeling Note: As this is a large-scale aggregate transportation problem (total volume 181), standard Linear Programming (LP) relaxation is used. The transportation problem has the integrality property, so if the supplies and demands are integers, the optimal basic feasible solution will naturally have integer values for $x_{ij}$ without explicitly forcing integer constraints, which is computationally more efficient.*

### 3. Objective Function

Minimize the total transportation cost:

$$ \text{Minimize } Z = \sum_{i \in I} \sum_{j \in J} C_{ij} x_{ij} $$

Expanded:
$$ Z = 2x_{11} + 1x_{12} + 3x_{13} + 3x_{14} + 3x_{15} + 5x_{16} + $$
$$ 4x_{21} + 2x_{22} + 2x_{23} + 4x_{24} + 4x_{25} + 4x_{26} + $$
$$ 3x_{31} + 5x_{32} + 4x_{33} + 2x_{34} + 4x_{35} + 1x_{36} + $$
$$ 4x_{41} + 2x_{42} + 2x_{43} + 1x_{44} + 2x_{45} + 2x_{46} $$

### 4. Operational Constraints

**Supply Constraints (Flow out of each origin cannot exceed supply):**
Since the problem is balanced, these can be modeled as equalities (or inequalities; in a balanced problem, if all demands are met, supplies will automatically be fully utilized in the optimal solution if costs are positive, but equalities are standard for balanced TP).

$$ \sum_{j \in J} x_{ij} = S_i, \quad \forall i \in I $$

1.  $x_{11} + x_{12} + x_{13} + x_{14} + x_{15} + x_{16} = 50$
2.  $x_{21} + x_{22} + x_{23} + x_{24} + x_{25} + x_{26} = 40$
3.  $x_{31} + x_{32} + x_{33} + x_{34} + x_{35} + x_{36} = 60$
4.  $x_{41} + x_{42} + x_{43} + x_{44} + x_{45} + x_{46} = 31$

**Demand Constraints (Flow into each destination must meet demand):**

$$ \sum_{i \in I} x_{ij} = D_j, \quad \forall j \in J $$

1.  $x_{11} + x_{21} + x_{31} + x_{41} = 30$
2.  $x_{12} + x_{22} + x_{32} + x_{42} = 50$
3.  $x_{13} + x_{23} + x_{33} + x_{43} = 20$
4.  $x_{14} + x_{24} + x_{34} + x_{44} = 40$
5.  $x_{15} + x_{25} + x_{35} + x_{45} = 30$
6.  $x_{16} + x_{26} + x_{36} + x_{46} = 11$

**Non-negativity Constraints:**

$$ x_{ij} \ge 0, \quad \forall i \in I, j \in J $$