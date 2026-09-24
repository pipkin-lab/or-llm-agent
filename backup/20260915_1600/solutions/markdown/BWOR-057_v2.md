**MODEL TYPE:** MILP (Mixed Integer Linear Programming)

### 1. MANDATORY COST INVENTORY
Before modeling, we extract all cost-related parameters:
*   **Variable Costs ($c_i$):**
    *   Container 1: 5 Yuan/unit
    *   Container 2: 8 Yuan/unit
    *   Container 3: 10 Yuan/unit
    *   Container 4: 12 Yuan/unit
    *   Container 5: 16 Yuan/unit
    *   Container 6: 18 Yuan/unit
*   **Fixed Costs ($F$):**
    *   Machine for Container 1: 1,200 Yuan
    *   Machine for Container 2: 1,200 Yuan
    *   Machine for Container 3: 1,200 Yuan
    *   Machine for Container 4: 1,200 Yuan
    *   Machine for Container 5: 1,200 Yuan
    *   Machine for Container 6: 1,200 Yuan

All objective parameters are explicitly provided in the table and text.

### 2. Index Sets & Parameters

**Index Sets:**
*   $I = \{1, 2, 3, 4, 5, 6\}$: Set of container types.
*   $D_{ij}$: Substitution set for demand type $j$. Specifically, $D_{ij} = \{ i \in I \mid Cap_i \ge Cap_j \}$. This set includes container type $i$ if its capacity is sufficient to substitute for or satisfy the demand of type $j$.
    *   Note: Since capacities are strictly increasing ($1500 < 2500 < ... < 12000$), $D_{ij}$ is simply $\{j, j+1, ..., 6\}$ for each $j$. For example, demand for Type 1 can be met by Types 1, 2, 3, 4, 5, or 6. Demand for Type 6 can *only* be met by Type 6.

**Parameters (Values from Table 5-11):**
*   $Cap_i$: Capacity in $cm^3$
    *   $Cap = [1500, 2500, 4000, 6000, 9000, 12000]$
*   $Dem_j$: Demand in units
    *   $Dem = [500, 550, 700, 900, 400, 300]$
*   $c_i$: Variable cost in Yuan/unit
    *   $c = [5, 8, 10, 12, 16, 18]$
*   $F_i$: Fixed cost in Yuan (constant for all $i$)
    *   $F_i = 1200$ for all $i \in I$

### 3. Decision Variables

**Continuous Variables:**
*   $x_{ij} \ge 0$: Quantity of container type $i$ produced to satisfy demand for container type $j$.
    *   Domain: $x_{ij} \in \mathbb{R}^+$ if $i \in D_{ij}$, otherwise $x_{ij} = 0$.

**Binary Variables:**
*   $y_i \in \{0, 1\}$: Indicator variable that equals 1 if machine $i$ is turned on (i.e., production of type $i$ is initiated), and 0 otherwise.

### 4. Objective Function

Minimize total cost (Fixed Costs + Variable Costs):

$$ \text{Minimize } Z = \sum_{i \in I} F_i y_i + \sum_{j \in I} \sum_{i \in D_{ij}} c_i x_{ij} $$

Substituting values:
$$ \text{Minimize } Z = 1200(y_1 + y_2 + y_3 + y_4 + y_5 + y_6) + 5x_{11} + 8(x_{21} + x_{22}) + 10(x_{31} + x_{32} + x_{33}) + 12(x_{41} + x_{42} + x_{43} + x_{44}) + 16(x_{51} + x_{52} + x_{53} + x_{54} + x_{55}) + 18(x_{61} + x_{62} + x_{63} + x_{64} + x_{65} + x_{66}) $$

*(Note: Terms where $Cap_i < Cap_j$ are excluded from the sum as they are infeasible substitutions.)*

### 5. Operational Constraints

**1. Demand Satisfaction Constraints:**
For each demand type $j$, the total quantity of containers capable of fulfilling that demand (itself or larger substitutes) must meet the exact demand.

$$ \sum_{i \in D_{ij}} x_{ij} = Dem_j, \quad \forall j \in I $$

Explicitly:
*   $j=1$ (Type 1 Demand): $x_{11} + x_{21} + x_{31} + x_{41} + x_{51} + x_{61} = 500$
*   $j=2$ (Type 2 Demand): $x_{22} + x_{32} + x_{42} + x_{52} + x_{62} = 550$
*   $j=3$ (Type 3 Demand): $x_{33} + x_{43} + x_{53} + x_{63} = 700$
*   $j=4$ (Type 4 Demand): $x_{44} + x_{54} + x_{64} = 900$
*   $j=5$ (Type 5 Demand): $x_{55} + x_{65} = 400$
*   $j=6$ (Type 6 Demand): $x_{66} = 300$

**2. Machine Activation Linking Constraints (Big-M):**
If any quantity of container type $i$ is produced (for any demand $j$), machine $i$ must be turned on. The total production of type $i$ is $\sum_{j: i \in D_{ij}} x_{ij}$.

We define $M_i$ as an upper bound on the total production of type $i$. A safe upper bound is the sum of all demands for types $j$ where $Cap_i \ge Cap_j$.
$M_i = \sum_{j \in \{k \in I \mid Cap_k \le Cap_i\}} Dem_j$

*   $M_1 = Dem_1 = 500$
*   $M_2 = Dem_1 + Dem_2 = 500 + 550 = 1050$
*   $M_3 = Dem_1 + Dem_2 + Dem_3 = 500 + 550 + 700 = 1750$
*   $M_4 = Dem_1 + Dem_2 + Dem_3 + Dem_4 = 500 + 550 + 700 + 900 = 2650$
*   $M_5 = Dem_1 + Dem_2 + Dem_3 + Dem_4 + Dem_5 = 500 + 550 + 700 + 900 + 400 = 3050$
*   $M_6 = Dem_1 + ... + Dem_6 = 500 + 550 + 700 + 900 + 400 + 300 = 3350$

Constraint:
$$ \sum_{j \in I} x_{ij} \le M_i y_i, \quad \forall i \in I $$

Explicitly:
*   $x_{11} \le 500 y_1$
*   $x_{21} + x_{22} \le 1050 y_2$
*   $x_{31} + x_{32} + x_{33} \le 1750 y_3$
*   $x_{41} + x_{42} + x_{43} + x_{44} \le 2650 y_4$
*   $x_{51} + x_{52} + x_{53} + x_{54} + x_{55} \le 3050 y_5$
*   $x_{61} + x_{62} + x_{63} + x_{64} + x_{65} + x_{66} \le 3350 y_6$

**3. Non-negativity and Integrality:**
*   $x_{ij} \ge 0, \quad \forall i, j$
*   $y_i \in \{0, 1\}, \quad \forall i \in I$