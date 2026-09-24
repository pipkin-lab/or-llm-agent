Here is the formal mathematical optimization model for the T Factory production planning problem.

### 1. Index Sets & Parameters

**Index Sets:**
*   $t \in T = \{1, 2, 3, 4, 5, 6\}$: Set of months (January to June).

**Parameters:**
*   $D_t$: Delivery demand in month $t$ (in hundreds of units).
    *   $D_1 = 1, D_2 = 2, D_3 = 5, D_4 = 3, D_5 = 2, D_6 = 1$.
*   $C_{max}$: Monthly production capacity = 400 units = **4** (hundreds of units).
*   $S_{max}$: Warehouse storage capacity = 300 units = **3** (hundreds of units).
*   $C_{prod}$: Variable production cost = 10,000 yuan per 100 units = **10,000** (yuan/hundred units).
*   $F$: Fixed operating cost if production occurs = **4,000** (yuan).
*   $C_{hold}$: Inventory holding cost = 1,000 yuan per 100 units per month = **1,000** (yuan/hundred units).
*   $I_0$: Initial inventory = 0.

**Derived Constants:**
*   Total Demand $\sum_{t=1}^6 D_t = 14$ (hundreds of units).

### 2. Decision Variables

*   $x_t$: Amount of production in month $t$ (continuous variable, in hundreds of units).
    *   Domain: $x_t \ge 0, \quad \forall t \in T$
*   $I_t$: Inventory level at the end of month $t$ (continuous variable, in hundreds of units).
    *   Domain: $I_t \ge 0, \quad \forall t \in T$
*   $y_t$: Binary indicator variable for production activity in month $t$.
    *   Domain: $y_t \in \{0, 1\}, \quad \forall t \in T$
    *   $y_t = 1$ if $x_t > 0$, else $y_t = 0$.

### 3. Objective Function

Minimize the total cost, which includes variable production costs, fixed operating costs, and inventory holding costs.

$$
\min Z = \sum_{t=1}^{6} \left( C_{prod} x_t + F y_t + C_{hold} I_{t-1} \right)
$$

Substituting the parameter values (note: $I_0 = 0$):

$$
\min Z = \sum_{t=1}^{6} \left( 10000 x_t + 4000 y_t + 1000 I_{t-1} \right)
$$

*Note: Inventory holding cost is typically charged on the inventory held during the period. Since $I_t$ is the ending inventory of month $t$, it is held during month $t+1$. Alternatively, one can model the cost as being paid on $I_{t-1}$ at the start of month $t$. Given the constraint that inventory must be zero after the final delivery, the cost of holding inventory $I_t$ at the end of month $t$ applies to the period until it is used. Standard formulation charges holding cost on the ending inventory of the previous period or the average. Let's refine based on standard production planning: Holding cost is incurred for units in inventory at the end of the month. Thus, cost is $1000 \cdot I_t$ for $t=1$ to $5$. $I_6=0$. So the term is $\sum_{t=1}^{5} 1000 I_t$.

**Revised Objective Function:**
$$
\min Z = \sum_{t=1}^{6} (10000 x_t + 4000 y_t) + \sum_{t=1}^{5} 1000 I_t
$$

### 4. Operational Constraints

**A. Inventory Balance Constraints**
The inventory at the end of month $t$ equals the previous inventory plus current production minus current demand.
$$
I_t = I_{t-1} + x_t - D_t, \quad \forall t \in T
$$
With $I_0 = 0$ and $I_6 = 0$ (no remaining inventory after final delivery).

Explicitly:
1.  $I_1 = 0 + x_1 - 1$
2.  $I_2 = I_1 + x_2 - 2$
3.  $I_3 = I_2 + x_3 - 5$
4.  $I_4 = I_3 + x_4 - 3$
5.  $I_5 = I_4 + x_5 - 2$
6.  $I_6 = I_5 + x_6 - 1 = 0 \implies I_5 + x_6 = 1$

**B. Production Capacity Constraints**
Production cannot exceed the monthly capacity of 400 units (4 hundreds).
$$
x_t \le 4, \quad \forall t \in T
$$

**C. Warehouse Storage Capacity Constraints**
Inventory at the end of each month cannot exceed the warehouse capacity of 300 units (3 hundreds).
$$
I_t \le 3, \quad \forall t \in T
$$
*(Note: Since $I_6=0$, this constraint is active for $t=1$ to $5$.)*

**D. Linking Constraints (Fixed Cost Activation)**
Production $x_t$ can only be positive if the factory is operational ($y_t = 1$). We use the capacity bound as the big-M constant.
$$
x_t \le 4 y_t, \quad \forall t \in T
$$

**E. Non-negativity and Domain Constraints**
$$
x_t \ge 0, \quad \forall t \in T
$$
$$
I_t \ge 0, \quad \forall t \in T
$$
$$
y_t \in \{0, 1\}, \quad \forall t \in T
$$