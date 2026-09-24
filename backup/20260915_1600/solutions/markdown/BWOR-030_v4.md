# Multi-Period Grain Trading Optimization Model

## Model Type Declaration
**LP** (Linear Programming). All variables and constraints are linear. No integrality constraints are needed as grain quantities and cash flows are treated as continuous resources (or can be solved exactly with continuous variables given the linear structure).

## 1. Index Sets & Parameters

### Index Sets
*   $T = \{1, 2, 3\}$: Set of months (January, February, March).

### Parameters
*   $C_{cap}$: Warehouse capacity = $5,000$ dan.
*   $S_0$: Initial stock at start of Month 1 = $1,000$ dan.
*   $K_0$: Initial capital at start of Month 1 = $20,000$ yuan.
*   $S_{end}$: Target inventory at end of Month 3 = $2,000$ dan.
*   $P_t$: Purchase price in month $t$ (yuan/dan):
    *   $P_1 = 2.85$
    *   $P_2 = 3.05$
    *   $P_3 = 2.90$
*   $R_t$: Selling price in month $t$ (yuan/dan):
    *   $R_1 = 3.10$
    *   $R_2 = 3.25$
    *   $R_3 = 2.95$

**Note on Timing:**
*   Grain purchased in month $t$ arrives in month $t$ and can be sold starting in month $t+1$.
*   "Cash payment upon delivery" implies purchase costs are incurred in the month of purchase. Sales revenue is received in the month of sale.

## 2. Decision Variables

*   $x_t$: Quantity of grain purchased in month $t$ (dan). Domain: $x_t \ge 0, \forall t \in T$.
*   $y_t$: Quantity of grain sold in month $t$ (dan). Domain: $y_t \ge 0, \forall t \in T$.
    *   *Note:* $y_1$ represents sales of initial stock $S_0$. $y_t$ for $t>1$ can include stock from previous months.
*   $I_t$: Inventory of grain at the **end** of month $t$ (dan). Domain: $I_t \ge 0, \forall t \in T$.
*   $K_t$: Cash balance at the **end** of month $t$ (yuan). Domain: $K_t \ge 0, \forall t \in T$ (assuming no borrowing; if borrowing is allowed, this would be unbounded below, but typically "available capital" implies a working capital constraint where balance cannot be negative).

## 3. Objective Function

The problem asks to optimize the trading strategy. Typically, in such wholesale problems, the goal is to **maximize the final cash balance** (or profit) at the end of the planning horizon (end of March), subject to meeting the target inventory.

**Objective:** Maximize $K_3$ (Final Cash Balance)

$$ \text{Maximize } Z = K_3 $$

*(Alternatively, if the goal is to minimize purchase cost while meeting sales targets, the objective would differ, but given "trading company" and price fluctuations, maximizing final wealth/cash is the standard interpretation. Since the target end-inventory is fixed, maximizing final cash is equivalent to maximizing profit.)*

## 4. Operational Constraints

### A. Inventory Balance Constraints
The inventory at the end of month $t$ equals the inventory at the start of month $t$ plus purchases in month $t$ minus sales in month $t$.
*   Start of Month 1: $S_0 = 1,000$
*   Start of Month $t$ ($t > 1$): $I_{t-1}$

$$ I_t = I_{t-1} + x_t - y_t \quad \forall t \in T $$
Where $I_0 = S_0 = 1,000$.

Explicitly:
1.  $I_1 = 1,000 + x_1 - y_1$
2.  $I_2 = I_1 + x_2 - y_2$
3.  $I_3 = I_2 + x_3 - y_3$

### B. Sales Timing Constraint
Grain purchased in month $t$ can only be sold starting in month $t+1$. This means the quantity sold in month $t$ cannot exceed the inventory available at the **beginning** of month $t$.
*   Inventory available at beginning of month $t$ is $I_{t-1}$.
*   Therefore, $y_t \le I_{t-1}$.

Explicitly:
1.  $y_1 \le I_0 = 1,000$
2.  $y_2 \le I_1$
3.  $y_3 \le I_2$

*(Note: This constraint is naturally satisfied if we define $I_t \ge 0$ and $I_t = I_{t-1} + x_t - y_t$, because $y_t = I_{t-1} + x_t - I_t$. Since $x_t \ge 0$ and $I_t \ge 0$, $y_t$ can technically be larger than $I_{t-1}$ if we interpret $I_t$ as net position. However, physically, you cannot sell what you don't have *before* buying in the same month if sales happen before purchases, or you must specify the order. The problem states "Grain arrives in the month it is purchased, but can only be sold starting in the next month." This implies that purchases in month $t$ are NOT available for sale in month $t$. Thus, sales $y_t$ must be covered by stock from previous months only.
So, the constraint is: $y_t \le \text{Stock available at start of month } t$.
Stock available at start of month $t$ is $I_{t-1}$.
Therefore: $y_t \le I_{t-1}$ for all $t$.
Consequently, $I_t = I_{t-1} - y_t + x_t$. Since $y_t \le I_{t-1}$, $I_{t-1} - y_t \ge 0$. So $I_t \ge x_t \ge 0$. The non-negativity of $I_t$ is guaranteed by $y_t \le I_{t-1}$ and $x_t \ge 0$.)*

### C. Warehouse Capacity Constraints
The inventory at the end of each month cannot exceed warehouse capacity.
$$ I_t \le 5,000 \quad \forall t \in T $$

### D. Cash Flow Balance Constraints
Cash balance at end of month $t$ = Cash balance at start of month $t$ + Revenue from sales in month $t$ - Cost of purchases in month $t$.
*   Revenue in month $t$: $R_t \cdot y_t$
*   Cost in month $t$: $P_t \cdot x_t$
*   Start of Month 1 Cash: $K_0 = 20,000$
*   Start of Month $t$ ($t>1$) Cash: $K_{t-1}$

$$ K_t = K_{t-1} + R_t y_t - P_t x_t \quad \forall t \in T $$
Where $K_0 = 20,000$.

Explicitly:
1.  $K_1 = 20,000 + 3.10 y_1 - 2.85 x_1$
2.  $K_2 = K_1 + 3.25 y_2 - 3.05 x_2$
3.  $K_3 = K_2 + 2.95 y_3 - 2.90 x_3$

### E. Target Inventory Constraint
The inventory at the end of March (Month 3) must be exactly 2,000 dan.
$$ I_3 = 2,000 $$

### F. Non-negativity Constraints
$$ x_t \ge 0, \quad y_t \ge 0, \quad I_t \ge 0, \quad K_t \ge 0 \quad \forall t \in T $$

## Summary of the Model

**Maximize**
$$ Z = K_3 $$

**Subject to:**

1.  **Inventory Dynamics:**
    $$ I_1 = 1,000 + x_1 - y_1 $$
    $$ I_2 = I_1 + x_2 - y_2 $$
    $$ I_3 = I_2 + x_3 - y_3 $$

2.  **Sales Availability (Lagged Sales):**
    $$ y_1 \le 1,000 $$
    $$ y_2 \le I_1 $$
    $$ y_3 \le I_2 $$

3.  **Warehouse Capacity:**
    $$ I_1 \le 5,000 $$
    $$ I_2 \le 5,000 $$
    $$ I_3 \le 5,000 $$

4.  **Cash Flow:**
    $$ K_1 = 20,000 + 3.10 y_1 - 2.85 x_1 $$
    $$ K_2 = K_1 + 3.25 y_2 - 3.05 x_2 $$
    $$ K_3 = K_2 + 2.95 y_3 - 2.90 x_3 $$

5.  **Target End Inventory:**
    $$ I_3 = 2,000 $$

6.  **Non-negativity:**
    $$ x_t, y_t, I_t, K_t \ge 0 \quad \text{for } t=1,2,3 $$