**Model Type:** LP (Linear Programming)

### Index Sets & Parameters

**Index Sets:**
- $I$: Set of flour mills, $I = \{1, 2, 3\}$ (corresponding to Mills I, II, III)
- $J$: Set of food processing factories, $J = \{1, 2, 3\}$

**Parameters:**

1.  **Supply Capacity ($S_i$)**: Maximum output of flour mill $i$ (in units).
    -   $S_1 = 20$ (Mill I)
    -   $S_2 = 30$ (Mill II)
    -   $S_3 = 20$ (Mill III)
    -   *Total Supply = 70 units*

2.  **Demand Requirement ($D_j$)**: Processing capacity/demand of factory $j$ (in units).
    -   $D_1 = 15$ (Factory 1)
    -   $D_2 = 25$ (Factory 2)
    -   $D_3 = 20$ (Factory 3)
    -   *Total Demand = 60 units*

3.  **Unit Transportation Cost ($c_{ij}$)**: Cost to transport one unit of flour from mill $i$ to factory $j$ (yuan/unit).
    -   $c_{11}=3, c_{12}=10, c_{13}=2$
    -   $c_{21}=4, c_{22}=11, c_{23}=8$
    -   $c_{31}=8, c_{32}=11, c_{33}=4$

4.  **Unit Profit ($p_j$)**: Profit per unit of flour processed at factory $j$ (yuan/unit).
    -   $p_1 = 12$
    -   $p_2 = 16$
    -   $p_3 = 11$

**Derived Parameter (Net Benefit Coefficient $b_{ij}$):**
The net benefit of shipping one unit from mill $i$ to factory $j$ is the profit earned minus the transportation cost.
$b_{ij} = p_j - c_{ij}$

-   **To Factory 1 ($p_1=12$):**
    -   $b_{11} = 12 - 3 = 9$
    -   $b_{21} = 12 - 4 = 8$
    -   $b_{31} = 12 - 8 = 4$
-   **To Factory 2 ($p_2=16$):**
    -   $b_{12} = 16 - 10 = 6$
    -   $b_{22} = 16 - 11 = 5$
    -   $b_{32} = 16 - 11 = 5$
-   **To Factory 3 ($p_3=11$):**
    -   $b_{13} = 11 - 2 = 9$
    -   $b_{23} = 11 - 8 = 3$
    -   $b_{33} = 11 - 4 = 7$

### Decision Variables

Let $x_{ij}$ be the amount of flour (in units) transported from flour mill $i$ to food factory $j$.
-   $x_{ij} \ge 0, \quad \forall i \in I, j \in J$
-   Domain: Continuous (Flour is typically treated as a divisible commodity in such LP contexts unless specified as discrete lots; standard transportation problems assume continuity).

### Objective Function

Maximize the total net benefit (Total Profit - Total Transportation Cost).
$$ \text{Maximize } Z = \sum_{i \in I} \sum_{j \in J} b_{ij} x_{ij} $$

Substituting the calculated net benefit coefficients:
$$ Z = 9x_{11} + 6x_{12} + 9x_{13} + 8x_{21} + 5x_{22} + 3x_{23} + 4x_{31} + 5x_{32} + 7x_{33} $$

### Operational Constraints

1.  **Supply Constraints (Mill Capacities):**
    The amount shipped from each mill cannot exceed its production capacity. Since Total Supply (70) > Total Demand (60), these are inequalities ($\le$).
    $$ \sum_{j \in J} x_{1j} \le 20 \quad (\text{Mill I}) $$
    $$ \sum_{j \in J} x_{2j} \le 30 \quad (\text{Mill II}) $$
    $$ \sum_{j \in J} x_{3j} \le 20 \quad (\text{Mill III}) $$

2.  **Demand Constraints (Factory Capacities):**
    The amount received by each factory must exactly meet its processing capacity/demand (assuming the goal is to utilize the processing capacity to generate profit, and demand represents the maximum useful processing amount). Since Total Supply > Total Demand, we can fully satisfy all demands.
    $$ \sum_{i \in I} x_{i1} = 15 \quad (\text{Factory 1}) $$
    $$ \sum_{i \in I} x_{i2} = 25 \quad (\text{Factory 2}) $$
    $$ \sum_{i \in I} x_{i3} = 20 \quad (\text{Factory 3}) $$

3.  **Non-negativity:**
    $$ x_{ij} \ge 0 \quad \forall i \in I, j \in J $$