## Model Type Declaration
**Model Type:** LP (Linear Programming)

## Index Sets & Parameters

**Sets:**
- $t \in \{1, 2, 3\}$: Set of months (January, February, March).

**Parameters:**
- $C_{max} = 5000$: Warehouse capacity (dan).
- $S_0 = 1000$: Initial inventory in stock at the beginning of Month 1 (dan).
- $K_0 = 20000$: Initial available capital (yuan).
- $I_{target} = 2000$: Target ending inventory at the end of Month 3 (dan).
- $P^b_t$: Purchase price in month $t$ (yuan/dan).
  - $P^b_1 = 2.85$
  - $P^b_2 = 3.05$
  - $P^b_3 = 2.90$
- $P^s_t$: Selling price in month $t$ (yuan/dan).
  - $P^s_1 = 3.10$
  - $P^s_2 = 3.25$
  - $P^s_3 = 2.95$

## Decision Variables

Let:
- $x_t$: Quantity of grain purchased in month $t$ (continuous, $\ge 0$).
- $y_t$: Quantity of grain sold in month $t$ (continuous, $\ge 0$).
- $I_t$: Inventory level at the **end** of month $t$ (continuous, $\ge 0$).
- $B_t$: Cash balance at the **end** of month $t$ (continuous, $\ge 0$).

## Objective Function

The problem asks to maximize profit (or equivalently, the final wealth/cash balance plus the value of remaining assets). Since the problem specifies a target ending inventory, we maximize the total financial position at the end of Month 3. This includes the cash balance $B_3$ and the market value of the ending inventory $I_3$ (valued at the Month 3 selling price, or simply maximizing $B_3$ if inventory value is considered separately; however, standard inventory problems maximize the final cash balance assuming inventory is an asset. To be precise, the objective is to maximize the total value at the end of March: Cash + Inventory Value. Let's maximize $B_3 + P^s_3 I_3$. Alternatively, and more commonly in such textbook problems, if no salvage value is given for inventory beyond its market price, we maximize the cash balance $B_3$ subject to the inventory constraint, but usually, the "profit" is defined as ending cash + ending inventory value - initial cash - initial inventory value. Let's stick to maximizing the final net worth: $Z = B_3 + P^s_3 I_3$.

*Refinement:* Often in these problems, the objective is simply to maximize the cash balance $B_3$, assuming the inventory is a liability or just tracked separately. However, since inventory is an asset, the most robust objective is maximizing the total final value. Let's look at the cash flow.
Actually, a simpler and very common formulation for "maximize profit" in trading is to maximize the final cash balance $B_3$, provided that the ending inventory constraint is met. But wait, if we buy grain in month 3, it adds to $I_3$ but reduces $B_3$. If we don't sell it, it's still an asset.
Let's define the objective as maximizing the **final cash balance** $B_3$. Why? Because the inventory $I_3$ is constrained to be exactly 2000 dan. The "value" of that 2000 dan is fixed in terms of quantity. Whether we value it at cost or market price is a convention. Standard practice: Maximize $B_3$. The inventory is a required state.

Let's verify this interpretation. If I maximize $B_3$, I am maximizing the liquid cash. The grain is held. This is a valid objective.
Objective: $\text{Maximize } Z = B_3$

## Operational Constraints

**1. Inventory Balance Constraints**
The inventory at the end of month $t$ equals the inventory at the end of month $t-1$ plus purchases in month $t$ minus sales in month $t$.
Note: The problem states "Grain arrives in the month it is purchased, but can only be sold starting in the next month."
This implies that grain purchased in month $t$ ($x_t$) is available in inventory $I_t$.
Grain sold in month $t$ ($y_t$) must come from inventory available *before* the end of month $t$, i.e., $I_{t-1}$. It cannot come from $x_t$ (purchased in month $t$).

So, the balance equation is:
$$ I_t = I_{t-1} + x_t - y_t \quad \forall t \in \{1, 2, 3\} $$
With $I_0 = 1000$.

**2. Sales Availability Constraint**
Sales in month $t$ ($y_t$) cannot exceed the inventory available at the start of month $t$ (which is $I_{t-1}$). The problem explicitly says "can only be sold starting in the next month". This means $y_t$ is constrained by $I_{t-1}$, not $I_t$.
$$ y_t \le I_{t-1} \quad \forall t \in \{1, 2, 3\} $$
*Note:* Since $I_{t-1} \ge 0$, this ensures we don't sell grain we don't have yet. Also, from the balance equation $I_t = I_{t-1} + x_t - y_t$, if $y_t \le I_{t-1}$, then $I_t \ge x_t \ge 0$. So $I_t$ is naturally non-negative if $I_{t-1} \ge 0$ and $x_t, y_t \ge 0$ and $y_t \le I_{t-1}$.

**3. Warehouse Capacity Constraints**
Inventory at the end of each month cannot exceed warehouse capacity.
$$ I_t \le 5000 \quad \forall t \in \{1, 2, 3\} $$

**4. Cash Flow Balance Constraints**
Cash at the end of month $t$ equals cash at the end of month $t-1$ plus revenue from sales in month $t$ minus cost of purchases in month $t$.
- Revenue in month $t$: $P^s_t \cdot y_t$
- Cost in month $t$: $P^b_t \cdot x_t$

$$ B_t = B_{t-1} + P^s_t y_t - P^b_t x_t \quad \forall t \in \{1, 2, 3\} $$
With $B_0 = 20000$.

**5. Non-negativity and Capital Constraints**
- $x_t \ge 0, y_t \ge 0, I_t \ge 0, B_t \ge 0 \quad \forall t \in \{1, 2, 3\}$
- Note: $B_t \ge 0$ ensures we don't go into debt (standard assumption unless credit is allowed; problem says "available capital", implying a budget constraint).

**6. Ending Inventory Constraint**
The target inventory at the end of March is 2,000 dan.
$$ I_3 = 2000 $$

## Final Model Formulation

**Maximize**
$$ Z = B_3 $$

**Subject to:**

**Inventory Balances:**
1. $I_1 = 1000 + x_1 - y_1$
2. $I_2 = I_1 + x_2 - y_2$
3. $I_3 = I_2 + x_3 - y_3$

**Sales Constraints (Cannot sell current month's purchase):**
4. $y_1 \le 1000$
5. $y_2 \le I_1$
6. $y_3 \le I_2$

**Capacity Constraints:**
7. $I_1 \le 5000$
8. $I_2 \le 5000$
9. $I_3 \le 5000$

**Cash Flow Balances:**
10. $B_1 = 20000 + 3.10 y_1 - 2.85 x_1$
11. $B_2 = B_1 + 3.25 y_2 - 3.05 x_2$
12. $B_3 = B_2 + 2.95 y_3 - 2.90 x_3$

**Ending Inventory Requirement:**
13. $I_3 = 2000$

**Non-negativity:**
14. $x_1, x_2, x_3, y_1, y_2, y_3, I_1, I_2, I_3, B_1, B_2, B_3 \ge 0$

---
### Parameter Completeness Check
- $C_{max} = 5000$ (Provided)
- $S_0 = 1000$ (Provided)
- $K_0 = 20000$ (Provided)
- $I_{target} = 2000$ (Provided)
- Prices $P^b_t, P^s_t$ for $t=1,2,3$ (Provided in Table)

All parameters are explicitly defined from the text.

### Feasibility Sanity Check
- Total Supply/Demand: The company can buy and sell freely within cash and capacity limits.
- Cash: Starts with 20,000 yuan.
- Inventory: Starts with 1,000 dan.
- Constraint: $I_3 = 2,000$.
- Is it feasible? Yes. For example, do nothing ($x=0, y=0$).
  - $I_1 = 1000, I_2 = 1000, I_3 = 1000$. This violates $I_3 = 2000$.
  - We need to increase inventory by 1,000 dan over the quarter.
  - We can buy 1,000 dan in Month 1. Cost = $1000 \times 2.85 = 2850$.
  - $B_1 = 20000 - 2850 = 17150$.
  - $I_1 = 1000 + 1000 - 0 = 2000$.
  - Month 2: Buy 0, Sell 0. $I_2 = 2000$. $B_2 = 17150$.
  - Month 3: Buy 0, Sell 0. $I_3 = 2000$. $B_3 = 17150$.
  - This is a feasible solution.

The model is strictly defined.