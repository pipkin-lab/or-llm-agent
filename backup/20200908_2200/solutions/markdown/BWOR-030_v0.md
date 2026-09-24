# Optimization Model: Grain Trading and Inventory Management

## 1. Index Sets & Parameters

**Index Sets:**
*   $t \in \{1, 2, 3\}$: Set of months (January, February, March).
*   $T_{end} = 3$: The final month of the planning horizon.

**Parameters:**
*   $C_{cap} = 5,000$: Warehouse capacity (dan).
*   $I_0 = 1,000$: Initial inventory at the start of Month 1 (dan).
*   $K_0 = 20,000$: Initial available capital (yuan).
*   $I_{target} = 2,000$: Target inventory level at the end of Month 3 (dan).
*   $P^b_t$: Purchase price in month $t$ (yuan/dan).
    *   $P^b_1 = 2.85$
    *   $P^b_2 = 3.05$
    *   $P^b_3 = 2.90$
*   $P^s_t$: Selling price in month $t$ (yuan/dan).
    *   $P^s_1 = 3.10$
    *   $P^s_2 = 3.25$
    *   $P^s_3 = 2.95$

**Derived Parameters:**
*   $t \in \{1, 2, 3\}$: Months where selling is possible based on previous month's stock. Note that grain purchased in month $t$ can only be sold in month $t+1$.
    *   Sales in Month 1 ($t=1$) come from Initial Inventory ($I_0$).
    *   Sales in Month 2 ($t=2$) come from Inventory at end of Month 1 ($I_1$).
    *   Sales in Month 3 ($t=3$) come from Inventory at end of Month 2 ($I_2$).
    *   *Constraint Check*: Grain bought in Month 3 cannot be sold within the horizon (as sales happen next month, i.e., Month 4, which is outside the scope).

## 2. Decision Variables

Let:
*   $x_t$: Amount of grain purchased in month $t$ (dan).
*   $y_t$: Amount of grain sold in month $t$ (dan).
*   $I_t$: Inventory level at the **end** of month $t$ (dan).
*   $K_t$: Cash balance at the **end** of month $t$ (yuan).

**Domains:**
*   $x_t \ge 0, \quad \forall t \in \{1, 2, 3\}$
*   $y_t \ge 0, \quad \forall t \in \{1, 2, 3\}$
*   $I_t \ge 0, \quad \forall t \in \{1, 2, 3\}$
*   $K_t \ge 0, \quad \forall t \in \{1, 2, 3\}$ (Cash cannot be negative)

## 3. Objective Function

The company aims to **maximize** its total profit (or equivalently, maximize the final cash balance, assuming no other costs). Since initial capital is fixed and all transactions are cash-based, maximizing the final cash balance $K_3$ is equivalent to maximizing profit.

$$ \text{Maximize } Z = K_3 $$

*Alternatively, formulated as Net Revenue - Net Cost:*
$$ \text{Maximize } Z = \sum_{t=1}^{3} P^s_t y_t - \sum_{t=1}^{3} P^b_t x_t $$

Both formulations are mathematically equivalent given the balance constraints below. We will use the cash flow formulation for clarity in constraints.

## 4. Operational Constraints

### A. Inventory Balance Constraints
Inventory at the end of month $t$ equals inventory at the beginning of month $t$ plus purchases in month $t$ minus sales in month $t$.

*   **Month 1:**
    $$ I_1 = I_0 + x_1 - y_1 $$
    $$ I_1 = 1,000 + x_1 - y_1 $$

*   **Month 2:**
    $$ I_2 = I_1 + x_2 - y_2 $$

*   **Month 3:**
    $$ I_3 = I_2 + x_3 - y_3 $$

### B. Cash Flow Constraints
Cash at the end of month $t$ equals cash at the beginning of month $t$ plus revenue from sales in month $t$ minus cost of purchases in month $t$.

*   **Month 1:**
    $$ K_1 = K_0 + P^s_1 y_1 - P^b_1 x_1 $$
    $$ K_1 = 20,000 + 3.10 y_1 - 2.85 x_1 $$

*   **Month 2:**
    $$ K_2 = K_1 + P^s_2 y_2 - P^b_2 x_2 $$
    $$ K_2 = K_1 + 3.25 y_2 - 3.05 x_2 $$

*   **Month 3:**
    $$ K_3 = K_2 + P^s_3 y_3 - P^b_3 x_3 $$
    $$ K_3 = K_2 + 2.95 y_3 - 2.90 x_3 $$

### C. Storage Capacity Constraints
The inventory at the end of each month must not exceed the warehouse capacity.

$$ I_t \le 5,000, \quad \forall t \in \{1, 2, 3\} $$

### D. Sales Feasibility Constraints (Lagged Sales)
Grain purchased in month $t$ can only be sold in month $t+1$. This implies that the amount sold in month $t$ cannot exceed the inventory available at the start of month $t$ (which is $I_{t-1}$).

*   **Month 1 Sales:** Can only sell from Initial Stock $I_0$.
    $$ y_1 \le I_0 \implies y_1 \le 1,000 $$
    *(Note: $x_1$ is added to inventory after sales occur in this month's balance equation, but logically, you cannot sell what you just bought if the rule is strict "next month only". The inventory balance equation $I_1 = I_0 + x_1 - y_1$ combined with $y_1 \le I_0$ ensures $x_1$ is not sold in month 1.)*

*   **Month 2 Sales:** Can only sell from Inventory at end of Month 1 ($I_1$).
    $$ y_2 \le I_1 $$

*   **Month 3 Sales:** Can only sell from Inventory at end of Month 2 ($I_2$).
    $$ y_3 \le I_2 $$

*   **Month 4 Sales:** Not in horizon. Grain purchased in Month 3 ($x_3$) remains in $I_3$ and cannot be sold.

### E. Target Inventory Constraint
The inventory at the end of March (Month 3) must equal the target level.

$$ I_3 = 2,000 $$

### F. Non-negativity
$$ x_t \ge 0, \quad y_t \ge 0, \quad I_t \ge 0, \quad K_t \ge 0 \quad \forall t \in \{1, 2, 3\} $$

---

### Summary of Full Model

**Maximize:**
$$ K_3 $$

**Subject to:**

**Inventory Balances:**
1.  $I_1 = 1,000 + x_1 - y_1$
2.  $I_2 = I_1 + x_2 - y_2$
3.  $I_3 = I_2 + x_3 - y_3$

**Cash Flows:**
4.  $K_1 = 20,000 + 3.10 y_1 - 2.85 x_1$
5.  $K_2 = K_1 + 3.25 y_2 - 3.05 x_2$
6.  $K_3 = K_2 + 2.95 y_3 - 2.90 x_3$

**Capacity & Target:**
7.  $I_1 \le 5,000$
8.  $I_2 \le 5,000$
9.  $I_3 = 2,000$  *(This also implies $I_3 \le 5,000$ is satisfied)*

**Sales Restrictions (Next Month Rule):**
10. $y_1 \le 1,000$
11. $y_2 \le I_1$
12. $y_3 \le I_2$

**Non-negativity:**
13. $x_t, y_t, I_t, K_t \ge 0$ for $t=1,2,3$