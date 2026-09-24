**Model Type:** MILP (Mixed Integer Linear Programming)

### 1. Index Sets & Parameters

**Index Sets:**
*   $t$: Set of months, $t \in \{1, 2, 3, 4, 5, 6\}$

**Parameters (in base units: units and yuan):**
*   $D_t$: Delivery requirement (demand) for month $t$.
    *   $D_1 = 100$
    *   $D_2 = 200$
    *   $D_3 = 500$
    *   $D_4 = 300$
    *   $D_5 = 200$
    *   $D_6 = 100$
    *   *(Note: Table values are in "hundreds of units", so 1 unit in table = 100 units.)*
*   $P_{max}$: Maximum production capacity per month = $400$ units.
*   $I_{max}$: Maximum warehouse storage capacity = $300$ units.
*   $c_{prod}$: Variable production cost rate = $10,000$ yuan / 100 units = $100$ yuan/unit.
*   $F$: Fixed operating expense per production month = $4,000$ yuan.
*   $c_{hold}$: Holding cost rate = $1,000$ yuan / 100 units / month = $10$ yuan/unit/month.
*   $I_0$: Initial inventory = $0$.
*   $I_6$: Final inventory = $0$.

### 2. Decision Variables

*   $x_t$: Number of units produced in month $t$.
    *   Domain: $x_t \in \mathbb{Z}_{\ge 0}$ for $t=1,...,6$
    *   Bound: $0 \le x_t \le 400$
*   $y_t$: Binary variable indicating if production occurs in month $t$.
    *   Domain: $y_t \in \{0, 1\}$ for $t=1,...,6$
*   $I_t$: Inventory level at the end of month $t$ (before final delivery, effectively inventory carried to month $t+1$).
    *   Domain: $I_t \in \mathbb{Z}_{\ge 0}$ for $t=1,...,5$
    *   Bound: $0 \le I_t \le 300$
    *   Note: $I_0 = 0$ and $I_6 = 0$ are fixed parameters.

### 3. Objective Function

Minimize Total Cost $Z$:

$$
\text{Minimize } Z = \sum_{t=1}^{6} \left( 100 x_t + 4000 y_t + 10 I_t \right)
$$

*Explanation:*
*   $100 x_t$: Variable production cost ($100$ yuan/unit).
*   $4000 y_t$: Fixed cost incurred only if $x_t > 0$.
*   $10 I_t$: Holding cost for inventory carried from end of month $t$ to month $t+1$. Note that $I_6=0$, so no holding cost is charged for month 6 inventory (which is zero anyway). The holding cost is typically charged on the inventory held *during* the month or at the *end* of the month. Standard convention: cost is incurred on the ending inventory $I_t$ for the period leading to the next month. Since $I_6=0$, the sum runs effectively on $I_1, ..., I_5$.

### 4. Operational Constraints

**1. Linking Production and Fixed Cost:**
For each month $t \in \{1, ..., 6\}$:
$$
x_t \le 400 y_t
$$
*(If $y_t=0$, then $x_t=0$. If $x_t > 0$, then $y_t$ must be 1.)*

**2. Inventory Balance Constraints:**
For each month $t \in \{1, ..., 6\}$:
$$
I_{t-1} + x_t - D_t = I_t
$$
Where:
*   $I_0 = 0$
*   $I_6 = 0$
*   $D_t$ is as defined in Parameters.

Explicitly:
*   $t=1: 0 + x_1 - 100 = I_1$
*   $t=2: I_1 + x_2 - 200 = I_2$
*   $t=3: I_2 + x_3 - 500 = I_3$
*   $t=4: I_3 + x_4 - 300 = I_4$
*   $t=5: I_4 + x_5 - 200 = I_5$
*   $t=6: I_5 + x_6 - 100 = 0$

**3. Warehouse Capacity Constraints:**
For each month $t \in \{1, ..., 5\}$:
$$
I_t \le 300
$$
*(Also $I_t \ge 0$ is enforced by variable domain. $I_6=0$ satisfies this trivially.)*

**4. Production Capacity Constraints:**
For each month $t \in \{1, ..., 6\}$:
$$
x_t \le 400
$$
*(This is redundant with the linking constraint $x_t \le 400 y_t$ since $y_t \le 1$, but explicitly stated for clarity.)*

**5. Non-negativity and Integrality:**
$$
x_t \in \mathbb{Z}_{\ge 0}
$$
$$
y_t \in \{0, 1\}
$$
$$
I_t \in \mathbb{Z}_{\ge 0}
$$