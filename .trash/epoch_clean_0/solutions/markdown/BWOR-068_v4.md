# Mathematical Model: Snow Boot Ordering & Inventory Planning

## 1. Index Sets & Parameters

**Index Sets:**
*   $T = \{1, 2, 3, 4, 5, 6\}$: Set of months in the peak season.
    *   $t=1$: October
    *   $t=2$: November
    *   $t=3$: December
    *   $t=4$: January
    *   $t=5$: February
    *   $t=6$: March

**Parameters:**
*   $D_t$: Forecasted demand for month $t$ (pairs).
    *   $D = [40, 20, 30, 40, 30, 20]$
*   $K = \{1, 2, 3, 4, 5\}$: Set of possible order quantity levels.
*   $Q_k$: Order quantity for level $k$ (pairs).
    *   $Q = [10, 20, 30, 40, 50]$
*   $C_{var, k}$: Variable cost associated with order quantity level $k$ (yuan).
    *   $C_{var} = [48, 86, 118, 138, 160]$
*   $C_{fixed}$: Fixed ordering cost per order (yuan).
    *   $C_{fixed} = 10$
*   $h$: Holding cost per pair per month (yuan).
    *   $h = 0.2$
*   $I_{max}$: Maximum end-of-month inventory capacity (pairs).
    *   $I_{max} = 40$

## 2. Decision Variables

Since the order quantities are restricted to a discrete set $\{10, 20, 30, 40, 50\}$, we use binary variables to select the specific order level for each month.

*   $x_{t, k} \in \{0, 1\}$: Binary variable.
    *   $x_{t, k} = 1$ if the store orders exactly $Q_k$ pairs in month $t$.
    *   $x_{t, k} = 0$ otherwise.
*   $I_t \ge 0$: Continuous variable representing the inventory level at the **end** of month $t$ (pairs).

**Domain Notes:**
*   While $I_t$ is continuous, due to the discrete nature of demands and order quantities, the optimal solution will naturally result in integer values for $I_t$. However, defining it as continuous is standard and sufficient for LP/MILP solvers unless strict integrality of inventory is required (which is implied by the integer inputs). We will keep it continuous for flexibility, but note that $I_t$ will be integer-valued in the optimal solution.

## 3. Objective Function

Minimize the total cost over the 6 months. The total cost consists of:
1.  **Variable Ordering Costs**: Sum of $C_{var, k}$ for the selected order level.
2.  **Fixed Ordering Costs**: Sum of $C_{fixed}$ for each month where an order is placed.
3.  **Holding Costs**: Sum of $h \times I_t$ for each month.

$$
\text{Minimize } Z = \sum_{t=1}^{6} \sum_{k=1}^{5} C_{var, k} \cdot x_{t, k} + \sum_{t=1}^{6} C_{fixed} \cdot \left( \sum_{k=1}^{5} x_{t, k} \right) + \sum_{t=1}^{6} h \cdot I_t
$$

*Note: The term $\sum_{k=1}^{5} x_{t, k}$ equals 1 if an order is placed in month $t$, and 0 if no order is placed (if we allow "no order" as an option). However, the problem states "possible order quantities... are limited to 10, 20, 30, 40, or 50". It does not explicitly state that ordering 0 is an option with a cost of 0. Usually, in such problems, you can choose *not* to order. If we must choose one of the 5 levels, we cannot choose 0. Let's re-read carefully: "possible order quantities... are limited to 10, 20, 30, 40, or 50". This implies if you order, it's one of these. Can you order 0?
Standard interpretation: You can choose to order 0. If you order 0, you pay no variable cost and no fixed cost.
To handle this, we introduce a binary variable $y_t$ indicating if an order is placed, OR we can add a dummy option $k=0$ with $Q_0=0, C_{var,0}=0$.
However, the fixed cost is incurred *per order*. If we don't order, we pay 0.
Let's refine the variable definition to be precise.

**Revised Decision Variables:**
*   $x_{t, k} \in \{0, 1\}$ for $t \in T, k \in \{1, 2, 3, 4, 5\}$: 1 if order level $k$ is chosen in month $t$.
*   $z_t \in \{0, 1\}$: 1 if an order is placed in month $t$, 0 otherwise.
*   $I_t \ge 0$: End-of-month inventory.

Actually, a simpler approach: Since the set of allowed orders is discrete, we can define $x_{t,k}$ for $k \in \{1,..,5\}$.
Constraint: $\sum_{k=1}^5 x_{t,k} \le 1$. (You can place at most one order level per month. If sum is 0, no order).
Fixed Cost Term: $C_{fixed} \cdot \sum_{k=1}^5 x_{t,k}$. This works perfectly. If sum is 0, cost is 0. If sum is 1, cost is 10.

So the objective remains:
$$
\text{Minimize } Z = \sum_{t=1}^{6} \sum_{k=1}^{5} (C_{var, k} + C_{fixed}) \cdot x_{t, k} + \sum_{t=1}^{6} h \cdot I_t
$$
*(Note: I combined the fixed cost into the sum over k. Since $\sum x_{t,k}$ is either 0 or 1, adding $C_{fixed}$ to each $C_{var,k}$ is equivalent to adding $C_{fixed} \cdot \mathbb{1}_{\{order\}}$.)*

Wait, strictly speaking:
If I choose $k=1$, cost is $C_{var,1} + C_{fixed}$.
If I choose $k=2$, cost is $C_{var,2} + C_{fixed}$.
If I choose none, cost is 0.
This formulation is correct.

## 4. Operational Constraints

### 1. Order Selection Constraint
For each month $t$, you can select at most one order level.
$$
\sum_{k=1}^{5} x_{t, k} \le 1, \quad \forall t \in T
$$

### 2. Inventory Balance Constraint
The inventory at the end of month $t$ ($I_t$) is determined by the previous inventory ($I_{t-1}$), the order placed in month $t$ ($Order_t$), and the demand in month $t$ ($D_t$).

First, define the order quantity in month $t$:
$$
Order_t = \sum_{k=1}^{5} Q_k \cdot x_{t, k}
$$

The balance equation is:
$$
I_t = I_{t-1} + \sum_{k=1}^{5} Q_k \cdot x_{t, k} - D_t, \quad \forall t \in T
$$

**Boundary Conditions:**
*   Beginning of season inventory ($I_0$): 0.
    $$ I_0 = 0 $$
*   End of season inventory ($I_6$): 0.
    $$ I_6 = 0 $$

### 3. Inventory Capacity Constraint
The end-of-month inventory must not exceed 40 pairs.
$$
I_t \le 40, \quad \forall t \in T
$$

### 4. Non-negativity of Inventory
Inventory cannot be negative (no backlogging allowed, as is standard for this type of problem unless specified; "demand is met" implies $I_{t-1} + Order_t \ge D_t$).
$$
I_t \ge 0, \quad \forall t \in T
$$
*(Note: The balance equation $I_t = I_{t-1} + Order_t - D_t$ combined with $I_t \ge 0$ enforces that total available stock meets demand.)*

### 5. Variable Domains
$$
x_{t, k} \in \{0, 1\}, \quad \forall t \in T, k \in \{1, 2, 3, 4, 5\}
$$
$$
I_t \ge 0, \quad \forall t \in T
$$

## Summary of Model Structure

*   **Type**: Mixed Integer Linear Programming (MILP)
*   **Variables**:
    *   30 Binary variables ($x_{t,k}$ for 6 months $\times$ 5 levels)
    *   6 Continuous variables ($I_t$)
*   **Objective**: Minimize Total Cost (Variable Order Cost + Fixed Order Cost + Holding Cost)
*   **Key Logic**:
    *   The fixed cost is linearized by adding it to the variable cost coefficients in the objective function, coupled with the binary selection variables.
    *   Inventory flows are balanced monthly.
    *   Initial and final inventory are fixed to 0.
    *   Inventory capacity is capped at 40.