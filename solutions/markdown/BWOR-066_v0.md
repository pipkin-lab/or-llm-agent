# Mathematical Formulation: 4-Month Warehouse Purchasing & Sales Planning

## Model Type: MILP

## Index Sets & Parameters

**Index Sets:**
- $K = \{1, 2, 3, 4\}$: Set of months (January, February, March, April)
- $k$: Month index, where month $k$ runs from the beginning of month $k$ to the end of month $k$

**Parameters (extracted from Table 7-6):**

| Parameter | Description | Values |
|-----------|-------------|--------|
| $B_k$ | Buying price in month $k$ (per unit) | $B_1=10, B_2=9, B_3=11, B_4=15$ |
| $S_k$ | Selling price in month $k$ (per unit) | $S_1=12, S_2=9, S_3=13, S_4=17$ |
| $W$ | Warehouse capacity (units) | $W = 1000$ |
| $I_0$ | Initial inventory at start of Month 1 (units) | $I_0 = 500$ |

**Key Timing Rule:** Goods purchased in month $k$ are NOT available for sale until month $k+1$. Therefore, purchases in Month 4 cannot be sold within the 4-month horizon (no Month 5 exists in the planning period).

## Decision Variables

For each month $k \in K$:

| Variable | Description | Domain |
|----------|-------------|--------|
| $x_k$ | Quantity purchased in month $k$ | $x_k \in \mathbb{Z}_{\geq 0}$ |
| $y_k$ | Quantity sold in month $k$ | $y_k \in \mathbb{Z}_{\geq 0}$ |
| $I_k$ | Inventory at the **end** of month $k$ | $I_k \in \mathbb{Z}_{\geq 0}$ |

All variables are non-negative integers (product quantities are discrete units).

## Objective Function

Maximize total profit (revenue from sales minus cost of purchases):

$$\max \sum_{k=1}^{4} \left( S_k \cdot y_k - B_k \cdot x_k \right)$$

Substituting parameter values:

$$\max \; 12y_1 + 9y_2 + 13y_3 + 17y_4 - 10x_1 - 9x_2 - 11x_3 - 15x_4$$

**Objective Parameter Cross-Reference:**
- $S_1=12$ ✓ (Table, Month 1 Selling Price)
- $S_2=9$ ✓ (Table, Month 2 Selling Price)
- $S_3=13$ ✓ (Table, Month 3 Selling Price)
- $S_4=17$ ✓ (Table, Month 4 Selling Price)
- $B_1=10$ ✓ (Table, Month 1 Buying Price)
- $B_2=9$ ✓ (Table, Month 2 Buying Price)
- $B_3=11$ ✓ (Table, Month 3 Buying Price)
- $B_4=15$ ✓ (Table, Month 4 Buying Price)

All objective coefficients are confirmed from the table.

## Operational Constraints

### 1. Inventory Balance Constraints (for each month $k \in K$)

The inventory at the end of month $k$ equals the inventory at the start of month $k$ plus purchases made in month $k$ minus sales made in month $k$.

**Critical timing note:** Purchases in month $k$ arrive during month $k$ and are added to inventory at the end of month $k$. Sales in month $k$ draw from inventory available at the **start** of month $k$ (i.e., end-of-month $k-1$ inventory). Since purchases in month $k$ are not available for sale until month $k+1$, the sales in month $k$ are limited by the inventory carried in from the previous month.

The correct balance equation is:

$$I_k = I_{k-1} + x_k - y_k, \quad \forall k \in K$$

where $I_0 = 500$ (given initial inventory).

**Verification of timing logic:**
- **Month 1:** Start with $I_0 = 500$. Can sell up to 500 units ($y_1 \leq 500$). Buy $x_1$ units, which arrive and are stored. End inventory: $I_1 = 500 + x_1 - y_1$.
- **Month 2:** Start with $I_1$. Can sell up to $I_1$ units ($y_2 \leq I_1$). Buy $x_2$, stored. End: $I_2 = I_1 + x_2 - y_2$.
- **Month 3:** Start with $I_2$. Can sell up to $I_2$ units ($y_3 \leq I_2$). Buy $x_3$, stored. End: $I_3 = I_2 + x_3 - y_3$.
- **Month 4:** Start with $I_3$. Can sell up to $I_3$ units ($y_4 \leq I_3$). Buy $x_4$, stored. End: $I_4 = I_3 + x_4 - y_4$.

Writing each explicitly:

$$I_1 = 500 + x_1 - y_1$$
$$I_2 = I_1 + x_2 - y_2$$
$$I_3 = I_2 + x_3 - y_3$$
$$I_4 = I_3 + x_4 - y_4$$

### 2. Sales Limited by Available Inventory (for each month $k \in K$)

Since purchases in month $k$ are not available for sale until month $k+1$, the quantity sold in month $k$ cannot exceed the inventory at the **start** of month $k$ (which equals $I_{k-1}$, or $I_0$ for $k=1$):

$$y_k \leq I_{k-1}, \quad \forall k \in K$$

where $I_0 = 500$.

Explicitly:
- $y_1 \leq 500$
- $y_2 \leq I_1$
- $y_3 \leq I_2$
- $y_4 \leq I_3$

> **Note:** These constraints are implicitly enforced by the combination of the inventory balance equations and non-negativity of $I_k$, but they are stated explicitly for clarity and to prevent the solver from allowing $y_k > I_{k-1}$ (which would imply selling goods not yet in stock).

### 3. Warehouse Capacity Constraints (for each month $k \in K$)

The inventory at the end of each month must not exceed the warehouse capacity:

$$I_k \leq W = 1000, \quad \forall k \in K$$

Explicitly:
- $I_1 \leq 1000$
- $I_2 \leq 1000$
- $I_3 \leq 1000$
- $I_4 \leq 1000$

> **Note on $I_4$:** Since there is no Month 5 in the planning horizon, inventory remaining at the end of Month 4 has no further sale opportunity. The model allows $I_4 > 0$ (the store may hold unsold inventory), but since $x_4$ incurs a cost of 15 per unit and $y_4$ generates revenue of 17 per unit, the solver will naturally avoid unnecessary purchases in Month 4 unless beneficial. However, $x_4$ purchases that remain in $I_4$ will reduce profit, so the optimizer will set $x_4 = 0$ in the optimal solution (since $B_4 = 15$ and there is no future selling month to realize the $S_4=17$ benefit on those units — they were already sold from prior inventory).

### 4. Non-Negativity and Integrality

$$x_k \in \mathbb{Z}_{\geq 0}, \quad y_k \in \mathbb{Z}_{\geq 0}, \quad I_k \in \mathbb{Z}_{\geq 0}, \quad \forall k \in K$$

## Feasibility Sanity Check

- **Initial inventory:** 500 units available at start of Month 1.
- **Maximum possible sales in Month 1:** 500 (limited by initial stock).
- **Maximum possible purchases per month:** Limited by warehouse capacity. After selling in month $k$, the remaining inventory is $I_{k-1} - y_k$, and we can buy up to $1000 - (I_{k-1} - y_k)$ units.
- **No upper bound on purchases** other than warehouse capacity, so the model is bounded.
- **Trivial feasible solution:** Set $x_k = 0, y_k = 0, I_k = I_{k-1}$ for all $k$. This satisfies all constraints (inventory stays at 500, within capacity).
- **Total potential sales across 4 months:** Bounded by initial inventory + total purchases, which is bounded by capacity dynamics. The model is feasible and bounded.

## Final Magnitude Sanity Check

Consider a simple feasible plan:
- Month 1: Sell all 500 initial units at $S_1=12$, buy 500 at $B_1=10$ → $I_1 = 500$
- Month 2: Sell 500 at $S_2=9$, buy 500 at $B_2=9$ → $I_2 = 500$
- Month 3: Sell 500 at $S_3=13$, buy 500 at $B_3=11$ → $I_3 = 500$
- Month 4: Sell 500 at $S_4=17$, buy 0 → $I_4 = 0$

Profit = $(12-10)\cdot500 + (9-9)\cdot500 + (13-11)\cdot500 + (17-0)\cdot500 - 0 = 1000 + 0 + 1000 + 8500 = 10{,}500$

This is a reasonable magnitude for a profit over 4 months with ~500 units/month traded at margins of 0–2 per unit. The objective is in **yuan** (base currency units), matching the table's price units. No normalization is needed — the question asks to "maximize profit," which is the total dollar profit, a natural aggregate quantity.

## Summary of Model Structure

| Aspect | Detail |
|--------|--------|
| **Model Type** | MILP (Integer Linear Program) |
| **Variables** | 12 integer variables: $x_1..x_4$, $y_1..y_4$, $I_1..I_4$ |
| **Objective** | Maximize total profit = Σ(revenue) − Σ(cost) |
| **Key Constraints** | 4 inventory balances, 4 sales ≤ start-of-month inventory, 4 capacity ≤ 1000, 12 non-negativity/integrality |
| **Critical Timing** | Purchases in month $k$ available for sale only from month $k+1$ onward |