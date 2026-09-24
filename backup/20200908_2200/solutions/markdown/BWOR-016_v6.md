# Optimization Model for New Factory Construction and Transportation

## 1. Index Sets & Parameters

**Index Sets:**
*   $I = \{1, 2, 3, 4\}$: Set of factories ($A_1, A_2, A_3, A_4$).
*   $J = \{1, 2, 3, 4\}$: Set of demand locations ($B_1, B_2, B_3, B_4$).
*   $K = \{3, 4\}$: Set of potential new factories to be built.

**Parameters:**
*   $u_i$: Annual production capacity of factory $i$ (kt/year).
    *   $u_1 = 400$
    *   $u_2 = 600$
    *   $u_3 = 200$
    *   $u_4 = 200$
*   $d_j$: Annual demand at location $j$ (kt/year).
    *   $d_1 = 350$
    *   $d_2 = 400$
    *   $d_3 = 300$
    *   $d_4 = 150$
*   $c_{ij}$: Unit transportation cost from factory $i$ to location $j$ (thousand yuan/kt).
    *   Row 1 ($A_1$): $[2, 9, 3, 4]$
    *   Row 2 ($A_2$): $[8, 3, 5, 7]$
    *   Row 3 ($A_3$): $[7, 6, 1, 2]$
    *   Row 4 ($A_4$): $[4, 5, 2, 5]$
*   $F_k$: Fixed annual production cost for building new factory $k$ (thousand yuan).
    *   $F_3 = 1200$
    *   $F_4 = 1500$

**Data Completeness Check:**
*   Total Demand: $350 + 400 + 300 + 150 = 1200$ kt.
*   Total Existing Capacity ($A_1, A_2$): $400 + 600 = 1000$ kt.
*   Shortfall: $1200 - 1000 = 200$ kt.
*   Capacity of $A_3$ (200 kt) and $A_4$ (200 kt) exactly match the shortfall. This implies that if a new factory is built, it must operate at full capacity, and the existing factories will also likely operate near capacity depending on the transport cost optimization. The model constraints will handle this naturally.

## 2. Decision Variables

**Binary Variables (Construction Decision):**
*   $y_k \in \{0, 1\}$ for $k \in \{3, 4\}$:
    *   $y_k = 1$ if factory $A_k$ is built.
    *   $y_k = 0$ if factory $A_k$ is not built.

**Continuous Variables (Transportation Flow):**
*   $x_{ij} \geq 0$: Amount of material (kt) transported from factory $A_i$ to location $B_j$.

## 3. Objective Function

Minimize the total annual cost, which consists of the fixed cost of building the new factory and the variable transportation costs.

$$
\text{Minimize } Z = \sum_{k \in \{3,4\}} F_k y_k + \sum_{i \in I} \sum_{j \in J} c_{ij} x_{ij}
$$

Substituting the specific values:
$$
Z = 1200 y_3 + 1500 y_4 + \sum_{i=1}^{4} \sum_{j=1}^{4} c_{ij} x_{ij}
$$

## 4. Operational Constraints

### A. Capacity Constraints (Supply Side)
The total amount shipped from any factory $i$ cannot exceed its production capacity. For the new factories ($A_3, A_4$), the capacity is only available if the factory is built ($y_k=1$).

1.  For existing factory $A_1$:
    $$ \sum_{j=1}^{4} x_{1j} \leq 400 $$
2.  For existing factory $A_2$:
    $$ \sum_{j=1}^{4} x_{2j} \leq 600 $$
3.  For potential factory $A_3$:
    $$ \sum_{j=1}^{4} x_{3j} \leq 200 y_3 $$
4.  For potential factory $A_4$:
    $$ \sum_{j=1}^{4} x_{4j} \leq 200 y_4 $$

### B. Demand Satisfaction Constraints (Demand Side)
The total amount received by each location $j$ from all factories must exactly meet the demand $d_j$. (Note: Since total capacity of $A_1+A_2+\max(A_3,A_4)$ is $1000+200=1200$, which equals total demand, and we must build one, the system is balanced. Using equality constraints is appropriate).

1.  $$ \sum_{i=1}^{4} x_{i1} = 350 $$
2.  $$ \sum_{i=1}^{4} x_{i2} = 400 $$
3.  $$ \sum_{i=1}^{4} x_{i3} = 300 $$
4.  $$ \sum_{i=1}^{4} x_{i4} = 150 $$

### C. Construction Logic Constraints
We must build **exactly one** new factory (either $A_3$ or $A_4$).

$$ y_3 + y_4 = 1 $$

### D. Non-negativity and Integrality
*   $x_{ij} \geq 0$ for all $i \in I, j \in J$.
*   $y_k \in \{0, 1\}$ for $k \in \{3, 4\}$.

---

### Final Formulated Model Summary

**Variables:**
*   $x_{ij} \ge 0$ for $i=1..4, j=1..4$
*   $y_3, y_4 \in \{0, 1\}$

**Objective:**
$$ \min Z = 1200y_3 + 1500y_4 + \sum_{i=1}^4 \sum_{j=1}^4 c_{ij}x_{ij} $$

**Subject to:**
1.  **Supply Capacities:**
    *   $\sum_{j=1}^4 x_{1j} \le 400$
    *   $\sum_{j=1}^4 x_{2j} \le 600$
    *   $\sum_{j=1}^4 x_{3j} \le 200y_3$
    *   $\sum_{j=1}^4 x_{4j} \le 200y_4$
2.  **Demand Satisfaction:**
    *   $\sum_{i=1}^4 x_{i1} = 350$
    *   $\sum_{i=1}^4 x_{i2} = 400$
    *   $\sum_{i=1}^4 x_{i3} = 300$
    *   $\sum_{i=1}^4 x_{i4} = 150$
3.  **Build Exactly One:**
    *   $y_3 + y_4 = 1$
4.  **Cost Matrix Values ($c_{ij}$):**
    *   $c_{1j} = [2, 9, 3, 4]$
    *   $c_{2j} = [8, 3, 5, 7]$
    *   $c_{3j} = [7, 6, 1, 2]$
    *   $c_{4j} = [4, 5, 2, 5]$