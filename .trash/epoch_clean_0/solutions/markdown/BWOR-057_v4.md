# Mathematical Optimization Model

## Model Type Declaration
**MILP** (Mixed-Integer Linear Programming)

**Reasoning**:
- The production quantities for each container type are continuous (or large enough integers to be treated as continuous for linear approximation, but given "units" and "machines", we must consider if quantities are integer. Usually, in such industrial problems with large volumes, continuous is acceptable, BUT the "fixed cost per machine" implies a binary decision on whether to *run* the machine. If a machine runs, it produces some amount $x_{ij}$. If it doesn't run, $x_{ij}=0$.
- However, there is a nuance: "Fixed cost for each machine is 1,200 Yuan." This is a fixed charge. We need binary variables $y_j$ indicating if machine $j$ is operating.
- The substitution constraint allows larger containers to satisfy demand of smaller ones. This creates a flow of capacity.
- Demand is in "units" (discrete physical items), but typically in OR models of this scale (hundreds/thousands), we treat production quantities as continuous variables for simplicity unless strict integrality is required. Given the fixed charge structure, the key discrete decision is the machine on/off status. The production quantities $x_{ij}$ can be continuous. If the problem implies integer containers, we would make $x$ integer, but standard practice for "production planning" with fixed charges treats $x$ as continuous and $y$ as binary. Let's assume **Continuous** production quantities and **Binary** machine status. This makes it a **MILP** (if we consider the binary variables) or **LP** if we relax binaries? No, fixed charges require binaries or big-M. So it is **MILP**.

*Correction*: Actually, if we use the standard fixed-charge formulation with binaries, it is a MILP.

---

## 1. Index Sets & Parameters

**Sets:**
- $J = \{1, 2, 3, 4, 5, 6\}$: Set of container types (and corresponding dedicated machines).
- $i \in J$: Index for the specific container type whose demand is being satisfied.
- $j \in J$: Index for the machine/container type being produced.

**Parameters (from Table 5-11):**

| Parameter | Symbol | Description | Values |
| :--- | :--- | :--- | :--- |
| $C_j$ | Capacity of container $j$ (cm³) | Physical volume | $C = [1500, 2500, 4000, 6000, 9000, 12000]$ |
| $D_i$ | Demand for container type $i$ (units) | Required units | $D = [500, 550, 700, 900, 400, 300]$ |
| $v_j$ | Variable cost of container $j$ (Yuan/unit) | Production cost | $v = [5, 8, 10, 12, 16, 18]$ |
| $F$ | Fixed cost per machine (Yuan) | Setup cost | $F = 1200$ |

**Derived/Substitution Logic Parameter:**
- Substitution Rule: A container of type $j$ can substitute for demand of type $i$ **if and only if** $C_j \ge C_i$.
- Let $S_i = \{j \in J \mid C_j \ge C_i\}$ be the set of machines that can satisfy the demand of type $i$.

*Note on Substitution Logic*: The problem states "containers with larger capacities may be used as substitutes." This implies:
- Demand for Type 1 (1500 cm³) can be met by Types 1, 2, 3, 4, 5, 6.
- Demand for Type 2 (2500 cm³) can be met by Types 2, 3, 4, 5, 6.
- ...
- Demand for Type 6 (12000 cm³) can be met by Type 6 only.

This is a "nested" or "ladder" substitution structure.

---

## 2. Decision Variables

1.  **$x_{ij}$**: Continuous variable.
    -   Represents the number of units of container type $j$ produced **to satisfy the demand of container type $i$**.
    -   Domain: $x_{ij} \ge 0$ for all $i, j \in J$ where $j \in S_i$. $x_{ij} = 0$ if $j \notin S_i$.
    -   *Note*: It is more efficient to define $x_{ij}$ only for valid pairs.

2.  **$y_j$**: Binary variable.
    -   Represents whether machine $j$ is turned on (operating).
    -   Domain: $y_j \in \{0, 1\}$ for all $j \in J$.
    -   $y_j = 1$ if any unit of container $j$ is produced ($\sum_{i} x_{ij} > 0$).
    -   $y_j = 0$ if no unit of container $j$ is produced.

---

## 3. Objective Function

Minimize the total cost, which includes variable production costs and fixed machine operating costs.

$$
\text{Minimize } Z = \sum_{i \in J} \sum_{j \in S_i} v_j x_{ij} + \sum_{j \in J} F \cdot y_j
$$

**Expanded Objective:**
$$
Z = 5(\sum_{i} x_{i1}) + 8(\sum_{i} x_{i2}) + 10(\sum_{i} x_{i3}) + 12(\sum_{i} x_{i4}) + 16(\sum_{i} x_{i5}) + 18(\sum_{i} x_{i6}) + 1200(y_1 + y_2 + y_3 + y_4 + y_5 + y_6)
$$
*(Where the summation for $x_{ij}$ is restricted to valid substitution pairs $j \in S_i$)*

---

## 4. Operational Constraints

### A. Demand Satisfaction Constraints
For each container type $i$, the total units allocated to satisfy its demand must equal the total demand $D_i$. Only machines $j$ with sufficient capacity ($C_j \ge C_i$) can contribute.

$$
\sum_{j \in S_i} x_{ij} = D_i \quad \forall i \in J
$$

**Explicitly:**
1.  $\sum_{j=1}^{6} x_{1j} = 500$
2.  $\sum_{j=2}^{6} x_{2j} = 550$
3.  $\sum_{j=3}^{6} x_{3j} = 700$
4.  $\sum_{j=4}^{6} x_{4j} = 900$
5.  $\sum_{j=5}^{6} x_{5j} = 400$
6.  $\sum_{j=6}^{6} x_{6j} = 300 \implies x_{66} = 300$

### B. Machine Capacity/Production Linking Constraints (Big-M)
If a machine $j$ is off ($y_j=0$), it produces 0 units. If it is on ($y_j=1$), it can produce up to its maximum possible demand allocation.
The maximum possible production for machine $j$ is bounded by the sum of demands of all types $i$ for which $j$ is a valid substitute.
Let $U_j = \sum_{i: j \in S_i} D_i$.

$$
\sum_{i: j \in S_i} x_{ij} \le U_j \cdot y_j \quad \forall j \in J
$$

**Calculating Upper Bounds ($U_j$):**
-   $U_1$: Machine 1 can only serve Type 1. $U_1 = D_1 = 500$.
-   $U_2$: Machine 2 can serve Types 1, 2. $U_2 = D_1 + D_2 = 500 + 550 = 1050$.
-   $U_3$: Machine 3 can serve Types 1, 2, 3. $U_3 = 500 + 550 + 700 = 1750$.
-   $U_4$: Machine 4 can serve Types 1, 2, 3, 4. $U_4 = 500 + 550 + 700 + 900 = 2650$.
-   $U_5$: Machine 5 can serve Types 1, 2, 3, 4, 5. $U_5 = 2650 + 400 = 3050$.
-   $U_6$: Machine 6 can serve Types 1, 2, 3, 4, 5, 6. $U_6 = 3050 + 300 = 3350$.

**Constraints:**
1.  $\sum_{i=1}^{1} x_{i1} \le 500 y_1$
2.  $\sum_{i=1}^{2} x_{i2} \le 1050 y_2$
3.  $\sum_{i=1}^{3} x_{i3} \le 1750 y_3$
4.  $\sum_{i=1}^{4} x_{i4} \le 2650 y_4$
5.  $\sum_{i=1}^{5} x_{i5} \le 3050 y_5$
6.  $\sum_{i=1}^{6} x_{i6} \le 3350 y_6$

### C. Non-negativity and Domain Constraints

$$
x_{ij} \ge 0 \quad \forall i, j \in J \text{ such that } j \in S_i
$$
$$
y_j \in \{0, 1\} \quad \forall j \in J
$$

---

## 5. Feasibility Sanity Check

1.  **Total Demand vs Total Supply Potential**:
    -   Total Demand Units: $500+550+700+900+400+300 = 3350$ units.
    -   The model allows mixing. Since larger containers can substitute for smaller ones, we are effectively allocating "capacity units" or "demand slots".
    -   Constraint 6 forces $x_{66}=300$. This requires $y_6=1$ because $300 > 0$. Cost contribution: $300 \times 18 + 1200$ (fixed).
    -   The remaining demand for types 1-5 (2850 units) can be met by machines 5, 4, 3, 2, 1.
    -   Is it possible to satisfy all demand? Yes, because Machine 6 alone could theoretically produce 3350 units (its upper bound $U_6$), and it is already forced to produce at least 300. Even if we only used Machine 6 for everything, $x_{i6}$ could cover all $D_i$. So the problem is feasible.

2.  **Cost Logic Check**:
    -   Variable costs increase with capacity ($5 < 8 < ... < 18$).
    -   Fixed costs are identical ($1200$).
    -   Intuitively, it is cheaper to produce smaller containers (lower variable cost) if possible. However, we *must* produce Type 6 containers for Type 6 demand.
    -   For Type 5 demand, we can use Machine 5 (cost 16) or Machine 6 (cost 18). Since $16 < 18$, we prefer Machine 5 unless Machine 5 is already running for other reasons or Machine 6 is running and has "spare" capacity logic? No, the fixed cost is per machine run.
    -   *Subtle Point*: If Machine 6 is ON (which it must be for Type 6 demand), does it make sense to produce Type 5 demand on Machine 6?
        -   Option A: Run M5 and M6.
            -   M6 produces 300 (for T6). Cost: $300 \times 18 + 1200 = 6600$.
            -   M5 produces 400 (for T5). Cost: $400 \times 16 + 1200 = 7600$.
            -   Total for T5/T6 part: $14200$.
        -   Option B: Run M6 only for T5 and T6.
            -   M6 produces 300 (for T6) + 400 (for T5) = 700 units.
            -   Cost: $700 \times 18 + 1200 = 12600 + 1200 = 13800$.
            -   Total for T5/T6 part: $13800$.
        -   Option B is cheaper ($13800 < 14200$). The model will capture this because $v_6 (18) > v_5 (16)$, but the fixed cost saving of turning off M5 ($1200$) outweighs the extra variable cost ($400 \times (18-16) = 800$).
        -   The MILP formulation correctly handles this trade-off via the $y_j$ binaries and big-M constraints.

3.  **Unit Consistency**:
    -   Costs are in Yuan.
    -   Demands are in Units.
    -   Capacities are in cm³ (used only for substitution logic $C_j \ge C_i$).
    -   No unit conversion errors detected.

## Final Model Summary

**Model Type:** MILP

**Minimize:**
$$ Z = \sum_{j=1}^6 v_j \left( \sum_{i: C_i \le C_j} x_{ij} \right) + 1200 \sum_{j=1}^6 y_j $$

**Subject to:**
1.  **Demand Balance:**
    $$ \sum_{j: C_j \ge C_i} x_{ij} = D_i, \quad \forall i=1..6 $$
2.  **Fixed Charge Linkage:**
    $$ \sum_{i: C_i \le C_j} x_{ij} \le U_j y_j, \quad \forall j=1..6 $$
    Where $U_j = \sum_{i: C_i \le C_j} D_i$.
3.  **Domains:**
    $$ x_{ij} \ge 0 $$
    $$ y_j \in \{0,1\} $$