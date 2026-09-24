**Model Type:** MILP (Mixed Integer Linear Programming)

### 1. Index Sets & Parameters

**Index Sets:**
*   $t \in \{1, 2, 3, 4, 5, 6\}$: Set of months.
    *   $t=1$: October
    *   $t=2$: November
    *   $t=3$: December
    *   $t=4$: January
    *   $t=5$: February
    *   $t=6$: March
*   $k \in \{1, 2, 3, 4, 5\}$: Set of possible order quantity levels.
    *   $k=1$: 10 pairs
    *   $k=2$: 20 pairs
    *   $k=3$: 30 pairs
    *   $k=4$: 40 pairs
    *   $k=5$: 50 pairs

**Parameters:**

*   $D_t$: Demand in month $t$ (pairs).
    *   $D_1 = 40$
    *   $D_2 = 20$
    *   $D_3 = 30$
    *   $D_4 = 40$
    *   $D_5 = 30$
    *   $D_6 = 20$
*   $Q_k$: Order quantity corresponding to level $k$ (pairs).
    *   $Q_1 = 10$
    *   $Q_2 = 20$
    *   $Q_3 = 30$
    *   $Q_4 = 40$
    *   $Q_5 = 50$
*   $C_k$: Variable cost (material/production cost) for order level $k$ (yuan).
    *   $C_1 = 48$
    *   $C_2 = 86$
    *   $C_3 = 118$
    *   $C_4 = 138$
    *   $C_5 = 160$
*   $F$: Fixed ordering cost per order placed (yuan).
    *   $F = 10$
*   $h$: Holding cost per pair per month (yuan).
    *   $h = 0.2$
*   $H_{max}$: Maximum end-of-month inventory capacity (pairs).
    *   $H_{max} = 40$

### 2. Decision Variables

*   $x_{t,k} \in \{0, 1\}$: Binary variable. Equals 1 if an order of quantity $Q_k$ is placed in month $t$, 0 otherwise.
*   $I_t \ge 0$: Continuous variable representing the inventory at the **end** of month $t$ (pairs).

### 3. Objective Function

Minimize the total cost, which consists of variable order costs, fixed ordering costs, and holding costs.

$$ \text{Minimize } Z = \sum_{t=1}^{6} \left( \sum_{k=1}^{5} (C_k \cdot x_{t,k}) + F \cdot \left( \sum_{k=1}^{5} x_{t,k} \right) \right) + \sum_{t=1}^{6} (h \cdot I_t) $$

Expanding the fixed cost term, note that $\sum_{k=1}^{5} x_{t,k}$ is 1 if an order is placed in month $t$, and 0 otherwise. Let $y_t = \sum_{k=1}^{5} x_{t,k}$.

$$ Z = \sum_{t=1}^{6} \left( 48 x_{t,1} + 86 x_{t,2} + 118 x_{t,3} + 138 x_{t,4} + 160 x_{t,5} + 10 y_t \right) + 0.2 \sum_{t=1}^{6} I_t $$

### 4. Operational Constraints

**A. One Order Per Month (Mutual Exclusivity)**
At most one order quantity can be selected per month. (Note: It is possible to place no order if inventory suffices, so this is an inequality $\le 1$, but typically in these discrete lot-sizing problems, if you order, you pick one size. If no order is needed, all $x_{t,k}=0$).

$$ \sum_{k=1}^{5} x_{t,k} \le 1, \quad \forall t \in \{1, \dots, 6\} $$

**B. Inventory Balance**
The inventory at the end of month $t$ is the inventory from the previous month plus the quantity ordered in month $t$, minus the demand in month $t$.
Initial inventory $I_0 = 0$.

$$ I_t = I_{t-1} + \sum_{k=1}^{5} (Q_k \cdot x_{t,k}) - D_t, \quad \forall t \in \{1, \dots, 6\} $$

Specifically:
*   $t=1$: $I_1 = 0 + 10x_{1,1} + 20x_{1,2} + 30x_{1,3} + 40x_{1,4} + 50x_{1,5} - 40$
*   $t=2$: $I_2 = I_1 + 10x_{2,1} + 20x_{2,2} + 30x_{2,3} + 40x_{2,4} + 50x_{2,5} - 20$
*   $t=3$: $I_3 = I_2 + 10x_{3,1} + 20x_{3,2} + 30x_{3,3} + 40x_{3,4} + 50x_{3,5} - 30$
*   $t=4$: $I_4 = I_3 + 10x_{4,1} + 20x_{4,2} + 30x_{4,3} + 40x_{4,4} + 50x_{4,5} - 40$
*   $t=5$: $I_5 = I_4 + 10x_{5,1} + 20x_{5,2} + 30x_{5,3} + 40x_{5,4} + 50x_{5,5} - 30$
*   $t=6$: $I_6 = I_5 + 10x_{6,1} + 20x_{6,2} + 30x_{6,3} + 40x_{6,4} + 50x_{6,5} - 20$

**C. Inventory Capacity Constraint**
End-of-month inventory must not exceed 40 pairs.

$$ I_t \le 40, \quad \forall t \in \{1, \dots, 6\} $$

**D. Non-Backlogging Constraint**
Inventory cannot be negative (demand must be met from available inventory/orders).

$$ I_t \ge 0, \quad \forall t \in \{1, \dots, 6\} $$

**E. End-of-Season Constraint**
The inventory at the end of the peak season (March, $t=6$) must be zero.

$$ I_6 = 0 $$

**F. Variable Domains**

$$ x_{t,k} \in \{0, 1\}, \quad \forall t \in \{1, \dots, 6\}, \forall k \in \{1, \dots, 5\} $$
$$ I_t \ge 0, \quad \forall t \in \{1, \dots, 6\} $$