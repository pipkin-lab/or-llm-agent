Based on the problem description, here is the formal mathematical optimization model.

### Index Sets & Parameters

**Index Sets:**
*   $t \in \{1, 2, 3\}$: Set of months.

**Parameters:**
*   $d_t$: Demand in month $t$.
    *   $d_1 = 100$
    *   $d_2 = 110$
    *   $d_3 = 120$
*   $h$: Inventory holding cost per unit per month.
    *   $h = 1$
*   $s_0$: Initial inventory at the beginning of month 1.
    *   $s_0 = 0$
*   $s_3$: Required ending inventory at the end of month 3.
    *   $s_3 = 0$

### Decision Variables

*   $x_t$: Quantity of Product A produced in month $t$ (Continuous, $x_t \ge 0$).
*   $s_t$: Inventory level at the **end** of month $t$ (Continuous, $s_t \ge 0$).
    *   Note: $s_0$ is a parameter (start of month 1), and $s_3$ is constrained to be 0 (end of month 3). We define $s_t$ for $t \in \{1, 2, 3\}$ as the closing inventory for that month.

### Objective Function

Minimize the total cost, which consists of production costs and inventory holding costs.

$$
\text{Minimize } Z = \sum_{t=1}^{3} \left( x_t^2 + h \cdot s_t \right)
$$

Substituting the value of $h=1$:

$$
Z = (x_1^2 + s_1) + (x_2^2 + s_2) + (x_3^2 + s_3)
$$

### Operational Constraints

**1. Inventory Balance Constraints**
For each month $t$, the inventory at the end of the month is equal to the previous period's ending inventory plus current production minus current demand.
*   Timing Convention:
    *   Start of Month $t$ inventory = $s_{t-1}$ (where $s_0=0$).
    *   Production $x_t$ occurs during Month $t$.
    *   Demand $d_t$ is met during Month $t$.
    *   End of Month $t$ inventory = $s_t$.
    *   Holding cost is applied to the ending inventory $s_t$ (standard convention unless specified otherwise; even if applied to average or beginning, the structure is linear. Given "per unit per month" and discrete periods, applying to end-of-period stock is the standard interpretation for this type of linear holding cost term in LP/Convex optimization contexts).

The constraints are:
$$
\begin{aligned}
s_1 &= s_0 + x_1 - d_1 \\
s_2 &= s_1 + x_2 - d_2 \\
s_3 &= s_2 + x_3 - d_3
\end{aligned}
$$

Substituting known parameters ($s_0=0, d_1=100, d_2=110, d_3=120$):
$$
\begin{aligned}
s_1 &= x_1 - 100 \\
s_2 &= s_1 + x_2 - 110 \\
s_3 &= s_2 + x_3 - 120
\end{aligned}
$$

**2. Boundary Conditions**
The problem states the ending inventory at the end of the third month is 0.
$$
s_3 = 0
$$

**3. Non-negativity Constraints**
Production quantities and inventory levels must be non-negative.
$$
x_t \ge 0, \quad \forall t \in \{1, 2, 3\}
$$
$$
s_t \ge 0, \quad \forall t \in \{1, 2, 3\}
$$
*(Note: $s_t \ge 0$ ensures backlogging is not allowed, which is standard for "inventory" unless "backorder" is explicitly mentioned.)*

---

### Summary of the Model

**Minimize:**
$$ Z = x_1^2 + x_2^2 + x_3^2 + s_1 + s_2 + s_3 $$

**Subject to:**
1.  $s_1 - x_1 = -100$
2.  $s_2 - s_1 - x_2 = -110$
3.  $s_3 - s_2 - x_3 = -120$
4.  $s_3 = 0$
5.  $x_1, x_2, x_3, s_1, s_2, s_3 \ge 0$