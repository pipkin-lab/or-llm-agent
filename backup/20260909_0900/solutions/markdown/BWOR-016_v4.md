### 1. Index Sets & Parameters

**Index Sets:**
- $I = \{1, 2, 3, 4\}$: Set of factories (Supply nodes).
  - $A_1, A_2$: Existing factories.
  - $A_3, A_4$: Candidate new factories.
- $J = \{1, 2, 3, 4\}$: Set of demand locations (Demand nodes) $B_1, B_2, B_3, B_4$.

**Parameters:**
- $C_{ij}$: Unit transportation cost from factory $i$ to location $j$ (thousand yuan/kt).
  - Row 1 ($A_1$): $[2, 9, 3, 4]$
  - Row 2 ($A_2$): $[8, 3, 5, 7]$
  - Row 3 ($A_3$): $[7, 6, 1, 2]$
  - Row 4 ($A_4$): $[4, 5, 2, 5]$
- $S_i$: Production capacity of factory $i$ (kt/year).
  - $S_1 = 400$
  - $S_2 = 600$
  - $S_3 = 200$
  - $S_4 = 200$
- $D_j$: Annual demand at location $j$ (kt/year).
  - $D_1 = 350$
  - $D_2 = 400$
  - $D_3 = 300$
  - $D_4 = 150$
- $F_k$: Annual fixed production cost if new factory $k$ is built (thousand yuan/year).
  - $F_3 = 1200$
  - $F_4 = 1500$
- $M$: A sufficiently large number (Big-M) for capacity constraints. We can use the total demand $\sum D_j = 1200$ as a safe upper bound for $M$ in the context of flow limits, or simply use the specific capacity $S_i$ directly in the constraint logic if structured properly. Given the structure, we will use $S_i$ directly in the linear constraints.

**Total Demand Check:**
$\sum_{j \in J} D_j = 350 + 400 + 300 + 150 = 1200$ kt/year.
$\sum_{i \in \{1,2,3,4\}} S_i = 400 + 600 + 200 + 200 = 1400$ kt/year.
Supply exceeds demand, so the model is feasible.

### 2. Decision Variables

**Binary Variables (Facility Location):**
- $y_3$: Binary variable where $y_3 = 1$ if factory $A_3$ is built, $0$ otherwise.
- $y_4$: Binary variable where $y_4 = 1$ if factory $A_4$ is built, $0$ otherwise.

**Continuous Variables (Flow):**
- $x_{ij}$: Amount of material transported from factory $i$ to location $j$ (kt/year), for all $i \in I, j \in J$.
  - Domain: $x_{ij} \ge 0$.

### 3. Objective Function

Minimize the total annual cost, which consists of the fixed costs of the new factories plus the variable transportation costs.

$$
\text{Minimize } Z = 1200 y_3 + 1500 y_4 + \sum_{i=1}^{4} \sum_{j=1}^{4} C_{ij} x_{ij}
$$

Expanded transportation cost term:
$$
\begin{aligned}
\sum_{i,j} C_{ij} x_{ij} = & 2x_{11} + 9x_{12} + 3x_{13} + 4x_{14} \\
& + 8x_{21} + 3x_{22} + 5x_{23} + 7x_{24} \\
& + 7x_{31} + 6x_{32} + 1x_{33} + 2x_{34} \\
& + 4x_{41} + 5x_{42} + 2x_{43} + 5x_{44}
\end{aligned}
$$

### 4. Operational Constraints

**1. Demand Satisfaction Constraints:**
The total amount received by each location $j$ must exactly meet its demand $D_j$.
$$
\sum_{i=1}^{4} x_{ij} = D_j, \quad \forall j \in \{1, 2, 3, 4\}
$$
Specifically:
- $x_{11} + x_{21} + x_{31} + x_{41} = 350$
- $x_{12} + x_{22} + x_{32} + x_{42} = 400$
- $x_{13} + x_{23} + x_{33} + x_{43} = 300$
- $x_{14} + x_{24} + x_{34} + x_{44} = 150$

**2. Supply Capacity Constraints:**
The total amount shipped from each factory $i$ cannot exceed its production capacity $S_i$.
- For existing factories ($A_1, A_2$), the capacity is fixed and always available (assuming they are already operational).
- For new factories ($A_3, A_4$), the capacity is only available if the factory is built. This is modeled using the binary variables.

$$
\sum_{j=1}^{4} x_{ij} \le S_i \cdot y_i, \quad \text{for } i \in \{3, 4\}
$$
Where $y_3$ and $y_4$ are the binary variables. If $y_3=0$, then $\sum x_{3j} \le 0 \implies x_{3j}=0$. If $y_3=1$, then $\sum x_{3j} \le 200$.

For existing factories:
$$
\sum_{j=1}^{4} x_{1j} \le 400
$$
$$
\sum_{j=1}^{4} x_{2j} \le 600
$$

**3. Exclusive Construction Constraint:**
The problem states "decide whether to build factory $A_3$ **or** $A_4$". This implies exactly one of the two new factories must be selected.
$$
y_3 + y_4 = 1
$$

**4. Non-negativity and Integrality:**
$$
x_{ij} \ge 0, \quad \forall i \in \{1,2,3,4\}, j \in \{1,2,3,4\}
$$
$$
y_3, y_4 \in \{0, 1\}
$$

### Summary of Model Structure
- **Type:** Mixed Integer Linear Programming (MILP).
- **Variables:** 16 continuous variables ($x_{ij}$) and 2 binary variables ($y_3, y_4$).
- **Constraints:**
  - 4 demand equality constraints.
  - 4 supply capacity inequality constraints.
  - 1 binary logic equality constraint ($y_3 + y_4 = 1$).
  - Non-negativity and integrality bounds.