### Index Sets & Parameters

**Sets:**
- $I = \{1, 2, 3, 4, 5, 6\}$: Set of container types (and corresponding dedicated machines).

**Parameters:**
- $C_i$: Capacity of container type $i$ (in $cm^3$).
  - $C_1=1500, C_2=2500, C_3=4000, C_4=6000, C_5=9000, C_6=12000$
- $D_i$: Demand for container type $i$ (in units).
  - $D_1=500, D_2=550, D_3=700, D_4=900, D_5=400, D_6=300$
- $v_i$: Variable cost per unit for container type $i$ (in Yuan).
  - $v_1=5, v_2=8, v_3=10, v_4=12, v_5=16, v_6=18$
- $F$: Fixed cost for operating any machine (in Yuan).
  - $F = 1200$

**Derived Logic:**
- Substitution Rule: Container type $j$ can satisfy the demand for container type $i$ if and only if $C_j \ge C_i$. Let $S_i = \{j \in I \mid C_j \ge C_i\}$ be the set of container types that can substitute for type $i$.

### Decision Variables

1.  $x_{ij}$: **Continuous** (or Integer, depending on interpretation of "units"; typically integer for physical count, but often relaxed to continuous in LP approximations. Given "units" are discrete physical objects, **Integer** is technically correct, but standard OR formulations for production planning often treat them as continuous if volumes are large. However, since $D_i$ are integers and costs are linear, we will define them as **Non-negative Integers** to be rigorous, or **Non-negative Continuous** if an LP approximation is accepted. Let's stick to **Non-negative Integers** for physical units).
    -   $x_{ij} \in \mathbb{Z}^+ \cup \{0\}$
    -   Definition: The number of units of container type $j$ produced to satisfy the demand for container type $i$.
    -   Constraint: $x_{ij} = 0$ if $j \notin S_i$ (i.e., if $C_j < C_i$).

2.  $y_j$: **Binary** variable.
    -   $y_j \in \{0, 1\}$
    -   Definition: $y_j = 1$ if the machine for container type $j$ is operated (i.e., if any quantity of container $j$ is produced), and $0$ otherwise.

### Objective Function

Minimize the total cost, which consists of the sum of variable costs for all produced units and the fixed costs for all activated machines.

$$
\text{Minimize } Z = \sum_{i \in I} \sum_{j \in I} v_j x_{ij} + \sum_{j \in I} F y_j
$$

*Note: The variable cost is incurred based on the physical container $j$ produced, regardless of which demand $i$ it satisfies.*

### Operational Constraints

1.  **Demand Satisfaction Constraints:**
    For each container type $i$, the total number of units produced from eligible substitute types $j \in S_i$ must be at least the demand $D_i$.
    $$
    \sum_{j \in S_i} x_{ij} \ge D_i, \quad \forall i \in I
    $$

2.  **Machine Activation Linking Constraints:**
    If any quantity of container $j$ is produced (i.e., $\sum_{i \in I} x_{ij} > 0$), then the machine $j$ must be turned on ($y_j = 1$).
    We use a big-M constraint. Let $M_j$ be an upper bound on the total production of container $j$. A safe upper bound is the sum of all demands: $M_j = \sum_{k \in I} D_k$.
    $$
    \sum_{i \in I} x_{ij} \le M_j y_j, \quad \forall j \in I
    $$
    *(Here $M_j = 500+550+700+900+400+300 = 3350$)*

3.  **Substitution Feasibility Constraints:**
    Enforce that $x_{ij}$ is zero if container $j$ cannot substitute for $i$ (i.e., if $C_j < C_i$).
    $$
    x_{ij} = 0, \quad \forall i, j \in I \text{ such that } C_j < C_i
    $$

4.  **Non-negativity and Integrality:**
    $$
    x_{ij} \in \mathbb{Z}_{\ge 0}, \quad \forall i, j \in I
    $$
    $$
    y_j \in \{0, 1\}, \quad \forall j \in I
    $$

---

### Specific Model Instantiation

To make the model fully explicit, we define the sets $S_i$ based on capacities:
-   $S_1$ (needs $\ge 1500$): $\{1, 2, 3, 4, 5, 6\}$
-   $S_2$ (needs $\ge 2500$): $\{2, 3, 4, 5, 6\}$
-   $S_3$ (needs $\ge 4000$): $\{3, 4, 5, 6\}$
-   $S_4$ (needs $\ge 6000$): $\{4, 5, 6\}$
-   $S_5$ (needs $\ge 9000$): $\{5, 6\}$
-   $S_6$ (needs $\ge 12000$): $\{6\}$

**Final Formulation:**

**Minimize**
$$ Z = \sum_{i=1}^6 \sum_{j \in S_i} v_j x_{ij} + 1200 \sum_{j=1}^6 y_j $$

**Subject to:**

**Demand Constraints:**
1.  $x_{11} + x_{12} + x_{13} + x_{14} + x_{15} + x_{16} \ge 500$
2.  $x_{22} + x_{23} + x_{24} + x_{25} + x_{26} \ge 550$
3.  $x_{33} + x_{34} + x_{35} + x_{36} \ge 700$
4.  $x_{44} + x_{45} + x_{46} \ge 900$
5.  $x_{55} + x_{56} \ge 400$
6.  $x_{66} \ge 300$

**Linking Constraints (Big-M = 3350):**
1.  $x_{11} + x_{21} + x_{31} + x_{41} + x_{51} + x_{61} \le 3350 y_1$
2.  $x_{12} + x_{22} + x_{32} + x_{42} + x_{52} + x_{62} \le 3350 y_2$
3.  $x_{13} + x_{23} + x_{33} + x_{43} + x_{53} + x_{63} \le 3350 y_3$
4.  $x_{14} + x_{24} + x_{34} + x_{44} + x_{54} + x_{64} \le 3350 y_4$
5.  $x_{15} + x_{25} + x_{35} + x_{45} + x_{55} + x_{65} \le 3350 y_5$
6.  $x_{16} + x_{26} + x_{36} + x_{46} + x_{56} + x_{66} \le 3350 y_6$

**Variable Domains:**
-   $x_{ij}$ are non-negative integers where $j \in S_i$.
-   $y_j \in \{0, 1\}$ for $j=1,\dots,6$.