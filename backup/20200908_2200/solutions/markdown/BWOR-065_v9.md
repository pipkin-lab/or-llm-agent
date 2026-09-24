Here is the formal mathematical optimization model for the T Factory production planning problem.

### 1. Index Sets & Parameters

**Index Sets:**
*   $t \in \{1, 2, 3, 4, 5, 6\}$: Set of months.

**Parameters:**
*   $D_t$: Delivery demand in month $t$ (in hundreds of units).
    *   $D_1 = 1, D_2 = 2, D_3 = 5, D_4 = 3, D_5 = 2, D_6 = 1$.
*   $C_{prod}$: Variable production cost per 100 units = 10,000 yuan.
*   $C_{fixed}$: Fixed operating cost per month if production occurs = 4,000 yuan.
*   $C_{hold}$: Holding cost per 100 units per month = 1,000 yuan.
*   $K_{prod}$: Monthly production capacity = 400 units = 4 (in hundreds of units).
*   $K_{store}$: Warehouse storage capacity = 300 units = 3 (in hundreds of units).
*   $M$: A sufficiently large constant for linearization (e.g., $M = 10$).

### 2. Decision Variables

**Continuous Variables:**
*   $x_t \ge 0$: Production quantity in month $t$ (in hundreds of units).
*   $I_t \ge 0$: Inventory level at the end of month $t$ (in hundreds of units).

**Binary Variables:**
*   $y_t \in \{0, 1\}$: Indicator variable where $y_t = 1$ if production occurs in month $t$ ($x_t > 0$), and $y_t = 0$ otherwise.

### 3. Objective Function

Minimize the total cost, which includes variable production costs, fixed operating costs, and inventory holding costs.

$$
\text{Minimize } Z = \sum_{t=1}^{6} (C_{prod} x_t + C_{fixed} y_t + C_{hold} I_t)
$$

Substituting the parameter values:
$$
Z = \sum_{t=1}^{6} (10000 x_t + 4000 y_t + 1000 I_t)
$$

*Note: Holding cost is incurred on the inventory remaining at the end of each month. The problem states no inventory after the final delivery, so $I_6 = 0$, meaning the holding cost term for $t=6$ is zero.*

### 4. Operational Constraints

**1. Inventory Balance Constraints:**
The inventory at the end of month $t$ is the previous inventory plus current production minus current delivery.

$$
I_t = I_{t-1} + x_t - D_t, \quad \forall t \in \{1, \dots, 6\}
$$
With $I_0 = 0$ (no initial inventory).

**2. Final Inventory Constraint:**
No inventory remains after the final delivery.

$$
I_6 = 0
$$

**3. Production Capacity Constraints:**
Production cannot exceed the monthly capacity.

$$
x_t \le K_{prod}, \quad \forall t \in \{1, \dots, 6\}
$$
$$
x_t \le 4, \quad \forall t \in \{1, \dots, 6\}
$$

**4. Storage Capacity Constraints:**
Inventory at the end of each month cannot exceed warehouse capacity.

$$
I_t \le K_{store}, \quad \forall t \in \{1, \dots, 5\}
$$
$$
I_t \le 3, \quad \forall t \in \{1, \dots, 5\}
$$
*(Note: $I_6=0$ is already constrained, so the bound applies to $t=1..5$ effectively, though $I_6 \le 3$ is also true.)*

**5. Linking Constraints (Big-M):**
These constraints ensure that the fixed cost is incurred only if production is positive.

$$
x_t \le M \cdot y_t, \quad \forall t \in \{1, \dots, 6\}
$$
Since max production is 4, we can set $M=4$ for tighter relaxation, or use a larger safe bound. Let's use $M=4$.
$$
x_t \le 4 y_t, \quad \forall t \in \{1, \dots, 6\}
$$

**6. Non-negativity and Integrality:**
$$
x_t \ge 0, \quad I_t \ge 0, \quad \forall t
$$
$$
y_t \in \{0, 1\}, \quad \forall t
$$