### 1. Index Sets & Parameters

**Index Sets:**
*   $T = \{1, 2, 3, 4, 5, 6\}$: Set of months in the peak season.
    *   $t=1$: October
    *   $t=2$: November
    *   $t=3$: December
    *   $t=4$: January
    *   $t=5$: February
    *   $t=6$: March
*   $K = \{1, 2, 3, 4, 5\}$: Set of discrete order quantity options.
    *   $k=1 \rightarrow 10$ pairs
    *   $k=2 \rightarrow 20$ pairs
    *   $k=3 \rightarrow 30$ pairs
    *   $k=4 \rightarrow 40$ pairs
    *   $k=5 \rightarrow 50$ pairs

**Parameters:**
*   $D_t$: Forecasted demand in month $t$ (pairs).
    *   $D_1=40, D_2=20, D_3=30, D_4=40, D_5=30, D_6=20$.
*   $Q_k$: Order quantity corresponding to option $k$ (pairs).
    *   $Q_1=10, Q_2=20, Q_3=30, Q_4=40, Q_5=50$.
*   $C_k$: Variable cost associated with order quantity option $k$ (yuan).
    *   $C_1=48, C_2=86, C_3=118, C_4=138, C_5=160$.
*   $F$: Fixed ordering cost per order (yuan).
    *   $F = 10$.
*   $h$: Holding cost per pair per month (yuan).
    *   $h = 0.2$.
*   $H_{max}$: Maximum end-of-month inventory (pairs).
    *   $H_{max} = 40$.
*   $I_0$: Initial inventory at the start of the season (month 1).
    *   $I_0 = 0$.

### 2. Decision Variables

*   $x_{t,k} \in \{0, 1\}$: Binary variable for all $t \in T, k \in K$.
    *   $x_{t,k} = 1$ if the store orders quantity $Q_k$ in month $t$.
    *   $x_{t,k} = 0$ otherwise.
*   $I_t \in \mathbb{Z}_{\ge 0}$: Integer variable for all $t \in T$.
    *   Inventory level at the end of month $t$ (pairs).

### 3. Objective Function

Minimize the total cost over the peak season, which consists of variable ordering costs, fixed ordering costs, and inventory holding costs.

$$ \text{Minimize } Z = \sum_{t=1}^{6} \left( \sum_{k=1}^{5} (C_k \cdot x_{t,k}) + F \cdot \left(\sum_{k=1}^{5} x_{t,k}\right) + h \cdot I_t \right) $$

*Note: The term $\sum_{k=1}^{5} x_{t,k}$ equals 1 if an order is placed in month $t$, and 0 otherwise. Since $F$ is constant per order, this correctly applies the fixed cost only when $x_{t,k}=1$ for some $k$.*

### 4. Operational Constraints

**1. Order Quantity Exclusivity (One Order Option Per Month)**
In any given month, the store can choose at most one order quantity option. (Assuming 0 is also a valid "no order" state implicitly handled by the logic that inventory balances demand, but typically in these discrete choice problems, we enforce that if you order, you pick exactly one quantity. If no order is placed, all $x_{t,k}=0$. We must ensure that if an order is placed, exactly one $k$ is selected, or 0 orders are selected. However, the problem implies we can choose *from* the list. Let's assume the set of possible actions includes "No Order". The constraint below ensures that if any order is made, it is exactly one type. To allow "No Order", we simply allow $\sum x_{t,k} = 0$ or $1$. We do *not* force $\sum x_{t,k} = 1$ because we might not need to order if inventory suffices. However, the inventory balance constraint will dictate whether we *need* to order. But wait, if we don't order, $I_{t-1}$ must cover $D_t$. If $I_{t-1} < D_t$, we *must* order. The model should allow $\sum x_{t,k} \le 1$.

$$ \sum_{k=1}^{5} x_{t,k} \le 1, \quad \forall t \in T $$

**2. Inventory Balance**
The inventory at the end of month $t$ is the previous month's inventory plus the incoming order minus the demand of month $t$.

$$ I_t = I_{t-1} + \sum_{k=1}^{5} (Q_k \cdot x_{t,k}) - D_t, \quad \forall t \in T $$
*   With $I_0 = 0$.

**3. Inventory Capacity**
The end-of-month inventory cannot exceed the storage limit.

$$ I_t \le 40, \quad \forall t \in T $$

**4. Non-negativity of Inventory**
Inventory cannot be negative (backordering is not explicitly allowed; usually in such seasonal problems, demand must be met from current stock/orders. If backordering were allowed, $I_t$ could be negative. Given "inventory... expected to be zero" at start/end and standard retail context, we assume no backorders, i.e., $I_t \ge 0$).

$$ I_t \ge 0, \quad \forall t \in T $$

**5. End-of-Season Inventory**
The problem states inventory at the end of the peak season is expected to be zero.

$$ I_6 = 0 $$

**6. Variable Domains**
$$ x_{t,k} \in \{0, 1\}, \quad \forall t \in T, k \in K $$
$$ I_t \in \mathbb{Z}, \quad \forall t \in T $$