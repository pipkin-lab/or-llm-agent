**Model Type:** LP (Linear Programming)

### 1. Index Sets & Parameters

**Index Sets:**
- $I$: Set of flour mills, $I = \{1, 2, 3\}$ (corresponding to I, II, III)
- $J$: Set of food processing factories, $J = \{1, 2, 3\}$

**Parameters:**
- $S_i$: Supply capacity (output) of flour mill $i$ (in units).
  - $S_1 = 20$
  - $S_2 = 30$
  - $S_3 = 20$
- $D_j$: Demand capacity (processing capacity) of factory $j$ (in units).
  - $D_1 = 15$
  - $D_2 = 25$
  - $D_3 = 20$
- $c_{ij}$: Unit transportation cost from mill $i$ to factory $j$ (yuan/unit).
  - $c_{11} = 3, c_{12} = 10, c_{13} = 2$
  - $c_{21} = 4, c_{22} = 11, c_{23} = 8$
  - $c_{31} = 8, c_{32} = 11, c_{33} = 4$
- $p_j$: Unit profit from processing flour at factory $j$ (yuan/unit).
  - $p_1 = 12$
  - $p_2 = 16$
  - $p_3 = 11$

**Derived Parameter:**
- $z_{ij}$: Net unit benefit of shipping from mill $i$ to factory $j$.
  - $z_{ij} = p_j - c_{ij}$
  - Calculation:
    - $z_{11} = 12 - 3 = 9$
    - $z_{12} = 16 - 10 = 6$
    - $z_{13} = 11 - 2 = 9$
    - $z_{21} = 12 - 4 = 8$
    - $z_{22} = 16 - 11 = 5$
    - $z_{23} = 11 - 8 = 3$
    - $z_{31} = 12 - 8 = 4$
    - $z_{32} = 16 - 11 = 5$
    - $z_{33} = 11 - 4 = 7$

### 2. Decision Variables

- $x_{ij}$: Amount of flour shipped from flour mill $i$ to food factory $j$.
  - Domain: $x_{ij} \ge 0$ for all $i \in I, j \in J$ (Continuous variable, as flour is a bulk commodity).

### 3. Objective Function

Maximize the total net benefit (Total Profit - Total Transportation Cost).

$$
\text{Maximize } Z = \sum_{i \in I} \sum_{j \in J} (p_j - c_{ij}) x_{ij}
$$

Substituting the calculated net benefits $z_{ij}$:

$$
\text{Maximize } Z = 9x_{11} + 6x_{12} + 9x_{13} + 8x_{21} + 5x_{22} + 3x_{23} + 4x_{31} + 5x_{32} + 7x_{33}
$$

### 4. Operational Constraints

**Supply Constraints (Mill Outputs):**
The total amount shipped from each mill cannot exceed its output capacity. Since total supply ($20+30+20=70$) equals total demand ($15+25+20=60$) is false ($70 \neq 60$), and specifically Supply > Demand, we use inequalities for supply. However, in standard transportation problems where Supply > Demand, the constraint is typically $\le S_i$. But wait, let's check totals.
Total Supply = 70.
Total Demand = 60.
Since Supply > Demand, not all supply will be used. The factories have limited capacity ("processing capacity" is given as Demand in the table header "Factory Demand" or "processing capacity"). The problem states "processing capacity of each food factory". This implies factories cannot process more than their capacity. Therefore, the inflow to each factory must be $\le D_j$.
The mills have "output" which acts as the available supply. We can choose to not produce/ship all output if it is not profitable or if demand is limited. Given all net benefits $z_{ij}$ are positive, we want to ship as much as possible. The bottleneck is the factories' capacity.

Constraint 1: Supply from each mill $i$ must not exceed $S_i$.
$$
\sum_{j \in J} x_{ij} \le S_i \quad \forall i \in I
$$
- $\sum_{j=1}^{3} x_{1j} \le 20$
- $\sum_{j=1}^{3} x_{2j} \le 30$
- $\sum_{j=1}^{3} x_{3j} \le 20$

Constraint 2: Inflow to each factory $j$ must not exceed its processing capacity $D_j$.
$$
\sum_{i \in I} x_{ij} \le D_j \quad \forall j \in J
$$
- $\sum_{i=1}^{3} x_{i1} \le 15$
- $\sum_{i=1}^{3} x_{i2} \le 25$
- $\sum_{i=1}^{3} x_{i3} \le 20$

Constraint 3: Non-negativity.
$$
x_{ij} \ge 0 \quad \forall i \in I, j \in J
$$

**Feasibility & Logic Check:**
Total Max Demand = 60. Total Supply = 70.
Since all net unit benefits ($z_{ij}$) are positive, the optimal solution will utilize the full capacity of the factories (i.e., $\sum x_{ij} = D_j$ for all $j$) because shipping more flour increases total benefit until factory capacities are hit. The mills will have unused capacity (70 - 60 = 10 units unused). The model correctly allows this via the $\le S_i$ constraints.