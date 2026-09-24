### 1. Index Sets & Parameters

**Index Sets:**
- $I = \{1, 2, 3\}$: Set of flour mills (indexed by $i$).
- $J = \{1, 2, 3\}$: Set of food processing factories (indexed by $j$).

**Parameters:**
- $a_i$: Supply capacity (output) of flour mill $i$ (units).
  - $a_1 = 20$
  - $a_2 = 30$
  - $a_3 = 20$
- $b_j$: Demand (processing capacity) of food factory $j$ (units).
  - $b_1 = 15$
  - $b_2 = 25$
  - $b_3 = 20$
- $c_{ij}$: Unit transportation cost from mill $i$ to factory $j$ (yuan/unit).
  - $c_{11}=3, c_{12}=10, c_{13}=2$
  - $c_{21}=4, c_{22}=11, c_{23}=8$
  - $c_{31}=8, c_{32}=11, c_{33}=4$
- $p_j$: Unit profit from processing flour at factory $j$ (yuan/unit).
  - $p_1 = 12$
  - $p_2 = 16$
  - $p_3 = 11$

**Derived Parameters:**
- $r_{ij}$: Net unit benefit of transporting flour from mill $i$ to factory $j$.
  - Formula: $r_{ij} = p_j - c_{ij}$
  - Calculations:
    - $r_{11} = 12 - 3 = 9$
    - $r_{12} = 16 - 10 = 6$
    - $r_{13} = 11 - 2 = 9$
    - $r_{21} = 12 - 4 = 8$
    - $r_{22} = 16 - 11 = 5$
    - $r_{23} = 11 - 8 = 3$
    - $r_{31} = 12 - 8 = 4$
    - $r_{32} = 16 - 11 = 5$
    - $r_{33} = 11 - 4 = 7$

**Balance Check:**
- Total Supply: $20 + 30 + 20 = 70$
- Total Demand: $15 + 25 + 20 = 60$
- Since Total Supply ($70$) > Total Demand ($60$), this is an unbalanced transportation problem. The surplus supply ($10$ units) will remain unused at the mills.

### 2. Decision Variables

Let $x_{ij}$ be the amount of flour transported from flour mill $i$ to food factory $j$.

- **Domain**: $x_{ij} \ge 0$ for all $i \in I, j \in J$.
- **Type**: Continuous (LP). *Note: While physical units are discrete, standard transportation problems of this scale are typically solved as Linear Programs. Given the coefficients are integers, the optimal solution to the LP relaxation will be integer-valued due to the total unimodularity of the transportation constraint matrix. Therefore, explicit integer constraints are not strictly necessary for correctness but can be added if strict integrality is required.*

### 3. Objective Function

**Goal**: Maximize total net benefit (Total Profit - Total Transportation Cost).

$$ \text{Maximize } Z = \sum_{i \in I} \sum_{j \in J} (p_j - c_{ij}) x_{ij} $$

Substituting the calculated net benefits $r_{ij}$:

$$ Z = 9x_{11} + 6x_{12} + 9x_{13} + 8x_{21} + 5x_{22} + 3x_{23} + 4x_{31} + 5x_{32} + 7x_{33} $$

### 4. Operational Constraints

**1. Supply Constraints (Outflow from Mills)**
The amount shipped from any mill cannot exceed its total output.
$$ \sum_{j \in J} x_{ij} \le a_i, \quad \forall i \in I $$

- Mill 1: $x_{11} + x_{12} + x_{13} \le 20$
- Mill 2: $x_{21} + x_{22} + x_{23} \le 30$
- Mill 3: $x_{31} + x_{32} + x_{33} \le 20$

**2. Demand Constraints (Inflow to Factories)**
The amount received by any factory must exactly meet its demand/capacity (since demand is the maximum processing capacity and we want to maximize benefit, we will fill these capacities if profitable, but strictly speaking, the constraint is that inflow cannot exceed capacity. However, since all net benefits $r_{ij}$ are positive, the optimal solution will fully utilize the demand).
$$ \sum_{i \in I} x_{ij} = b_j, \quad \forall j \in J $$
*(Note: Using equality is standard here because all net profits are positive, meaning it is always better to ship more to meet demand than to leave capacity unused, subject to supply limits. Since Supply > Demand, all demand will be met.)*

- Factory 1: $x_{11} + x_{21} + x_{31} = 15$
- Factory 2: $x_{12} + x_{22} + x_{32} = 25$
- Factory 3: $x_{13} + x_{23} + x_{33} = 20$

**3. Non-negativity Constraints**
$$ x_{ij} \ge 0, \quad \forall i \in I, j \in J $$