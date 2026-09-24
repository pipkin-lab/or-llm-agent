### 1. Index Sets & Parameters

**Index Sets:**
*   $t$: Set of months, $\{1, 2, 3, 4, 5, 6\}$.

**Parameters:**
*   $D_t$: Demand (delivery requirement) in month $t$ (hundreds of units).
    *   $D_1 = 1, D_2 = 2, D_3 = 5, D_4 = 3, D_5 = 2, D_6 = 1$.
*   $C_{cap}$: Production capacity per month (hundreds of units) = 4.
*   $I_{cap}$: Warehouse storage capacity (hundreds of units) = 3.
*   $c_v$: Variable production cost (yuan per hundred units) = 100.
    *   *Note: 10,000 yuan / 100 units = 100 yuan per hundred units.*
*   $c_f$: Fixed production cost (yuan) = 4,000.
*   $c_h$: Holding cost (yuan per hundred units per month) = 10.
    *   *Note: 1,000 yuan / 100 units = 10 yuan per hundred units.*

### 2. Decision Variables

*   $x_t$: Production quantity in month $t$ (hundreds of units). Domain: $x_t \ge 0$.
    *   *Note: Although physical units are discrete, in aggregate production planning with capacities in the hundreds, standard practice and the "BWOR-080" rule suggest using continuous variables unless integer constraints are explicitly forced by small scale or explicit "integer" text. Given the costs are linear and scale is moderate, we define $x_t$ as continuous. However, looking at the fixed cost, if $x_t=0$, no fixed cost is paid. This requires a binary variable to linearize the fixed cost.*
*   $y_t$: Binary variable indicating if production occurs in month $t$.
    *   $y_t \in \{0, 1\}$.
    *   $y_t = 1$ if $x_t > 0$, else $0$.
*   $I_t$: Inventory level at the **end** of month $t$ (hundreds of units). Domain: $I_t \ge 0$.

### 3. Objective Function

Minimize Total Cost ($Z$):

$$
\min Z = \sum_{t=1}^{6} (c_v x_t + c_f y_t + c_h I_t)
$$

Substituting values:
$$
\min Z = \sum_{t=1}^{6} (100 x_t + 4000 y_t + 10 I_t)
$$

### 4. Operational Constraints

**1. Inventory Balance Constraints:**
The inventory at the end of month $t$ is the inventory from the previous month plus production in month $t$ minus demand in month $t$.
For $t=1, \dots, 6$:
$$
I_t = I_{t-1} + x_t - D_t
$$
With $I_0 = 0$ (no initial inventory).

Explicitly:
*   $t=1: I_1 = 0 + x_1 - 1$
*   $t=2: I_2 = I_1 + x_2 - 2$
*   $t=3: I_3 = I_2 + x_3 - 5$
*   $t=4: I_4 = I_3 + x_4 - 3$
*   $t=5: I_5 = I_4 + x_5 - 2$
*   $t=6: I_6 = I_5 + x_6 - 1$

**2. End-of-Horizon Inventory Constraint:**
"None remaining after the final delivery at the end of June":
$$
I_6 = 0
$$

**3. Production Capacity Constraints:**
Production cannot exceed monthly capacity ($C_{cap} = 4$):
$$
x_t \le 4 y_t, \quad \forall t \in \{1, \dots, 6\}
$$
*(Note: This also enforces $x_t=0$ if $y_t=0$, linking the binary variable to production. Since max capacity is 4, $M=4$ is a tight bound.)*

**4. Warehouse Storage Capacity Constraints:**
Inventory at the end of each month cannot exceed storage capacity ($I_{cap} = 3$):
$$
I_t \le 3, \quad \forall t \in \{1, \dots, 6\}
$$

**5. Non-negativity and Domain Constraints:**
$$
x_t \ge 0, \quad \forall t
$$
$$
I_t \ge 0, \quad \forall t
$$
$$
y_t \in \{0, 1\}, \quad \forall t
$$

### Summary of Model Formulation

**Model Type:** Mixed Integer Linear Programming (MILP)

**Variables:**
*   $x_t \in \mathbb{R}^+$ for $t=1..6$
*   $I_t \in \mathbb{R}^+$ for $t=1..6$
*   $y_t \in \{0,1\}$ for $t=1..6$

**Objective:**
$$ \min \sum_{t=1}^{6} (100 x_t + 4000 y_t + 10 I_t) $$

**Subject to:**
1.  $I_t - I_{t-1} - x_t = -D_t$ (for $t=1..6$, with $I_0=0$)
2.  $I_6 = 0$
3.  $x_t - 4 y_t \le 0$ (for $t=1..6$)
4.  $I_t \le 3$ (for $t=1..6$)
5.  $x_t, I_t \ge 0$ (for $t=1..6$)
6.  $y_t \in \{0,1\}$ (for $t=1..6$)