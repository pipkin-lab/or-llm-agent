To solve this problem, we need to formulate a Mixed Integer Linear Programming (MILP) model.

### 1. MANDATORY COST INVENTORY
Before modeling, we extract all costs and parameters:
*   **Variable Costs ($c_j$)**:
    *   Type 1: 5 Yuan/unit
    *   Type 2: 8 Yuan/unit
    *   Type 3: 10 Yuan/unit
    *   Type 4: 12 Yuan/unit
    *   Type 5: 16 Yuan/unit
    *   Type 6: 18 Yuan/unit
*   **Fixed Costs ($F_j$)**:
    *   Machine for Type 1: 1,200 Yuan
    *   Machine for Type 2: 1,200 Yuan
    *   Machine for Type 3: 1,200 Yuan
    *   Machine for Type 4: 1,200 Yuan
    *   Machine for Type 5: 1,200 Yuan
    *   Machine for Type 6: 1,200 Yuan
*   **Capacities ($Cap_j$)**:
    *   Type 1: 1500 cm³
    *   Type 2: 2500 cm³
    *   Type 3: 4000 cm³
    *   Type 4: 6000 cm³
    *   Type 5: 9000 cm³
    *   Type 6: 12000 cm³
*   **Demands ($D_i$)**:
    *   Type 1: 500 units
    *   Type 2: 550 units
    *   Type 3: 700 units
    *   Type 4: 900 units
    *   Type 5: 400 units
    *   Type 6: 300 units

*Note: The problem states "containers with larger capacities may be used as substitutes." This implies that if the specific machine for Type $i$ is not used or if its production is insufficient, the demand for Type $i$ can be met by producing Type $j$ where $Cap_j \ge Cap_i$. However, standard interpretation of "substitutes" in production planning with dedicated machines usually means:
1.  You must satisfy the *demand* for each container type.
2.  A container of type $j$ can satisfy the demand of type $i$ if $Cap_j \ge Cap_i$ (downward substitution is allowed: a big box can hold what a small box holds, but a small box cannot hold what a big box holds).
3.  If we produce $x_j$ units of type $j$, these units can be allocated to satisfy demands of types $i$ such that $Cap_j \ge Cap_i$.

Let $x_{ij}$ be the number of containers of type $j$ produced to satisfy the demand of type $i$.
Constraint: $x_{ij} > 0$ is only allowed if $Cap_j \ge Cap_i$.

The total production of type $j$ is $X_j = \sum_{i: Cap_i \le Cap_j} x_{ij}$.
The fixed cost is incurred if $X_j > 0$.

### 2. Model Type Declaration
**Model Type**: MILP (Mixed Integer Linear Programming)
*   Continuous variables for production quantities ($x_{ij}$).
*   Binary variables for machine activation ($y_j$).

### 3. Index Sets & Parameters

**Sets:**
*   $I = \{1, 2, 3, 4, 5, 6\}$: Set of container demand types.
*   $J = \{1, 2, 3, 4, 5, 6\}$: Set of container production types (machines).
*   $S_{ij} = \{(i,j) \in I \times J \mid Cap_j \ge Cap_i\}$: The set of valid substitution pairs. Pair $(i,j)$ is valid if machine $j$ can produce a container large enough to satisfy demand $i$.

**Parameters (Yuan, cm³, units):**
*   $D_i$: Demand for type $i$.
    *   $D_1=500, D_2=550, D_3=700, D_4=900, D_5=400, D_6=300$.
*   $c_j$: Variable cost per unit for type $j$.
    *   $c_1=5, c_2=8, c_3=10, c_4=12, c_5=16, c_6=18$.
*   $F_j$: Fixed cost for machine $j$.
    *   $F_1=1200, F_2=1200, F_3=1200, F_4=1200, F_5=1200, F_6=1200$.
*   $Cap_j$: Capacity of container type $j$.
    *   $Cap_1=1500, Cap_2=2500, Cap_3=4000, Cap_4=6000, Cap_5=9000, Cap_6=12000$.

### 4. Decision Variables

*   $x_{ij}$: Continuous, non-negative variable representing the number of containers of type $j$ produced to satisfy the demand of type $i$. Defined for all $(i,j) \in S_{ij}$.
*   $y_j$: Binary variable for $j \in J$.
    *   $y_j = 1$ if machine $j$ is turned on (produces at least one unit).
    *   $y_j = 0$ if machine $j$ is turned off.

### 5. Objective Function

Minimize Total Cost = Total Variable Cost + Total Fixed Cost

$$ \min Z = \sum_{j \in J} \left( F_j y_j + \sum_{i \in I, (i,j) \in S_{ij}} c_j x_{ij} \right) $$

Expanding the summation for clarity (where $x_{ij}$ is only defined if $Cap_j \ge Cap_i$):

$$
\begin{aligned}
\min Z = \ & 1200y_1 + 1200y_2 + 1200y_3 + 1200y_4 + 1200y_5 + 1200y_6 \\
& + 5x_{11} + 8x_{21} + 10x_{31} + 12x_{41} + 16x_{51} + 18x_{61} \\
& + 5x_{12} + 8x_{22} + 10x_{32} + 12x_{42} + 16x_{52} + 18x_{62} \\
& + 5x_{13} + 8x_{23} + 10x_{33} + 12x_{43} + 16x_{53} + 18x_{63} \\
& + 5x_{14} + 8x_{24} + 10x_{34} + 12x_{44} + 16x_{54} + 18x_{64} \\
& + 5x_{15} + 8x_{25} + 10x_{35} + 12x_{45} + 16x_{55} + 18x_{65} \\
& + 5x_{16} + 8x_{26} + 10x_{36} + 12x_{46} + 16x_{56} + 18x_{66}
\end{aligned}
$$
*Note: The coefficients $c_j$ apply to $x_{ij}$ based on the production type $j$, not the demand type $i$.*

### 6. Operational Constraints

**1. Demand Satisfaction Constraints**
For each demand type $i \in I$, the sum of all containers substituted for it must equal its demand.
$$ \sum_{j \in J, (i,j) \in S_{ij}} x_{ij} = D_i, \quad \forall i \in I $$

Explicitly:
*   $i=1$ ($Cap=1500$): Can be met by types 1,2,3,4,5,6.
    $$ x_{11} + x_{12} + x_{13} + x_{14} + x_{15} + x_{16} = 500 $$
*   $i=2$ ($Cap=2500$): Can be met by types 2,3,4,5,6.
    $$ x_{12} \text{ (invalid, } Cap_1 < Cap_2) \rightarrow \text{Only } j \ge 2. $$
    $$ x_{22} + x_{23} + x_{24} + x_{25} + x_{26} = 550 $$
*   $i=3$ ($Cap=4000$): Can be met by types 3,4,5,6.
    $$ x_{33} + x_{34} + x_{35} + x_{36} = 700 $$
*   $i=4$ ($Cap=6000$): Can be met by types 4,5,6.
    $$ x_{44} + x_{45} + x_{46} = 900 $$
*   $i=5$ ($Cap=9000$): Can be met by types 5,6.
    $$ x_{55} + x_{56} = 400 $$
*   $i=6$ ($Cap=12000$): Can be met by type 6 only.
    $$ x_{66} = 300 $$

**2. Machine Activation Constraints (Fixed-Charge Logic)**
The total production of type $j$ is the sum of all $x_{ij}$ assigned to it. If this sum is greater than 0, $y_j$ must be 1. We use a big-M constraint where $M_j$ is an upper bound on the total possible production of type $j$.
The maximum possible production of type $j$ is the sum of all demands that can be satisfied by type $j$.
$M_j = \sum_{i: Cap_i \le Cap_j} D_i$.

$$ \sum_{i \in I, (i,j) \in S_{ij}} x_{ij} \le M_j y_j, \quad \forall j \in J $$

Calculating $M_j$:
*   $M_1 = D_1 = 500$
*   $M_2 = D_1 + D_2 = 500 + 550 = 1050$
*   $M_3 = D_1 + D_2 + D_3 = 500 + 550 + 700 = 1750$
*   $M_4 = D_1 + D_2 + D_3 + D_4 = 500 + 550 + 700 + 900 = 2650$
*   $M_5 = D_1 + D_2 + D_3 + D_4 + D_5 = 500 + 550 + 700 + 900 + 400 = 3050$
*   $M_6 = D_1 + D_2 + D_3 + D_4 + D_5 + D_6 = 500 + 550 + 700 + 900 + 400 + 300 = 3350$

Constraints:
*   $x_{11} \le 500 y_1$
*   $x_{12} + x_{22} \le 1050 y_2$
*   $x_{13} + x_{23} + x_{33} \le 1750 y_3$
*   $x_{14} + x_{24} + x_{34} + x_{44} \le 2650 y_4$
*   $x_{15} + x_{25} + x_{35} + x_{45} + x_{55} \le 3050 y_5$
*   $x_{16} + x_{26} + x_{36} + x_{46} + x_{56} + x_{66} \le 3350 y_6$

**3. Variable Domains**
$$ x_{ij} \ge 0, \quad \forall (i,j) \in S_{ij} $$
$$ y_j \in \{0, 1\}, \quad \forall j \in J $$

### Summary of Model Structure for Solver

**Sets:**
*   $I = \{1..6\}$
*   $J = \{1..6\}$
*   Valid Pairs $S_{ij}$:
    *   $i=1: j \in \{1,2,3,4,5,6\}$
    *   $i=2: j \in \{2,3,4,5,6\}$
    *   $i=3: j \in \{3,4,5,6\}$
    *   $i=4: j \in \{4,5,6\}$
    *   $i=5: j \in \{5,6\}$
    *   $i=6: j \in \{6\}$

**Parameters:**
*   $D = [500, 550, 700, 900, 400, 300]$
*   $C = [5, 8, 10, 12, 16, 18]$
*   $F = [1200, 1200, 1200, 1200, 1200, 1200]$
*   $M = [500, 1050, 1750, 2650, 3050, 3350]$ (Big-M values)

**Objective:**
Min $\sum_{j} F_j y_j + \sum_{(i,j) \in S_{ij}} C_j x_{ij}$

**Constraints:**
1.  $\sum_{j: (i,j) \in S_{ij}} x_{ij} = D_i, \forall i$
2.  $\sum_{i: (i,j) \in S_{ij}} x_{ij} \le M_j y_j, \forall j$
3.  $x_{ij} \ge 0, y_j \in \{0,1\}$