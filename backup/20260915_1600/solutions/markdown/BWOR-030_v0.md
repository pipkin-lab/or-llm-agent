### Mathematical Optimization Model

**Model Type:** LP (Linear Programming)

#### 1. Index Sets & Parameters

**Index Sets:**
- $T = \{1, 2, 3\}$: Set of months (January, February, March).
- $T_{sell} = \{2, 3\}$: Set of months in which grain can be sold (since grain purchased in month $t$ can only be sold starting in month $t+1$).

**Parameters:**
- $C_{max} = 5,000$: Warehouse capacity (dan).
- $I_0 = 1,000$: Initial inventory of grain as of Jan 1 (dan).
- $M_0 = 20,000$: Initial available capital (yuan).
- $I_{target} = 2,000$: Target inventory at the end of March (dan).
- $P^{buy}_t$: Purchase price in month $t$ (yuan/dan).
  - $P^{buy}_1 = 2.85$
  - $P^{buy}_2 = 3.05$
  - $P^{buy}_3 = 2.90$
- $P^{sell}_t$: Selling price in month $t$ (yuan/dan).
  - $P^{sell}_1 = 3.10$ (Note: Cannot sell in month 1 from month 1 purchases, but can sell initial stock? The problem states "Grain arrives in the month it is purchased, but can only be sold starting in the next month." This implies a 1-month lag for *purchased* grain. Does this lag apply to the *initial* stock? Usually, initial stock is available immediately unless specified otherwise. However, standard interpretation of "can only be sold starting in the next month" in such trading problems often refers to the specific grain lots. Let's look closely: "Grain arrives in the month it is purchased... sold starting in the next month." It does not explicitly restrict the initial stock. However, often in these textbook problems, the lag applies to the flow. If we assume initial stock is "already there", it might be sellable in month 1. But let's look at the prices. Buy 2.85, Sell 3.10. If we can sell initial stock in month 1, we make a profit. If we cannot, we must hold it.
    - *Interpretation Check:* "Grain arrives in the month it is purchased... sold starting in the next month." This sentence specifically links the lag to the *purchase* event. The initial stock was purchased in the past. Therefore, it is likely available for sale in Month 1.
    - *Alternative Interpretation:* The rule "can only be sold starting in the next month" is a general operational constraint for the warehouse. If so, even initial stock cannot be sold in Month 1.
    - Let's check feasibility/profitability.
      - If initial stock is sellable in M1: Buy 1000 (M1) -> Sell in M2. Sell 1000 (Initial) in M1.
      - If initial stock is NOT sellable in M1: It must be sold in M2 or M3.
    - Most standard interpretations of "purchased... sold next month" imply that *new* purchases have a 1-month lag. Existing inventory is typically available immediately. However, without explicit statement "initial stock is available for sale", there is ambiguity. Let's look at the cash flow.
    - Let's assume the standard constraint: **Sales in month $t$ consist only of inventory available at the start of month $t$ that is not restricted.**
    - Let's refine the "Lag" constraint. "Grain arrives in the month it is purchased, but can only be sold starting in the next month." This is a specific rule about the *flow* of purchased goods.
    - Let's define variables carefully to handle this.
    - $x_t$: Amount of grain purchased in month $t$.
    - $y_t$: Amount of grain sold in month $t$.
    - $I_t$: Inventory at the end of month $t$.
    
    The constraint "purchased in $t$, sold in $\ge t+1$" means that the quantity $x_t$ cannot contribute to $y_t$. It contributes to $y_{t+1}, y_{t+2}, \dots$.
    The initial inventory $I_0$ is available at the start of Month 1. Can it be sold in Month 1? The text doesn't say "Initial stock is restricted". It says "Grain [that is] purchased...". I will assume **Initial stock is sellable in Month 1**. If the problem intended a global 1-month lag, it would usually say "All grain must be held for at least one month before sale". The phrasing ties the restriction to the act of purchasing.
    
    *Self-Correction/Refinement:* In many such OR problems, if the lag is a property of the commodity handling, it applies to all grain. However, "purchased... sold next month" is a flow constraint. Let's assume the most logical business interpretation: You can sell what you have on hand at the beginning of the month, *unless* it was just purchased. Since $I_0$ was purchased in the past, it is sellable in Month 1.
    
    Let's verify the "Cash payment upon delivery" constraint.
    - Month 1: Pay for $x_1$. Receive cash from $y_1$.
    - Month 2: Pay for $x_2$. Receive cash from $y_2$.
    - Month 3: Pay for $x_3$. Receive cash from $y_3$.

    **Price Parameters:**
    - $P^{buy} = [2.85, 3.05, 2.90]$
    - $P^{sell} = [3.10, 3.25, 2.95]$

#### 2. Decision Variables

- $x_t$: Quantity of grain purchased in month $t$ (dan).
  - Domain: $x_t \ge 0, \quad \forall t \in \{1, 2, 3\}$
- $y_t$: Quantity of grain sold in month $t$ (dan).
  - Domain: $y_t \ge 0, \quad \forall t \in \{1, 2, 3\}$
- $I_t$: Inventory level at the end of month $t$ (dan).
  - Domain: $I_t \ge 0, \quad \forall t \in \{1, 2, 3\}$
- $M_t$: Cash balance at the end of month $t$ (yuan).
  - Domain: $M_t \ge 0, \quad \forall t \in \{1, 2, 3\}$ (Assuming no borrowing, only available capital can be used. The problem says "20,000 yuan in available capital", implying a budget constraint).

*Note on Sellability of Initial Stock:*
If we assume initial stock $I_0$ is sellable in Month 1, then $y_1$ can be up to $I_0 + x_0$ (where $x_0=0$ effectively, but $I_0$ is available).
However, the constraint "purchased in $t$, sold in $t+1$" specifically restricts $x_t$.
Let's model the inventory balance to ensure consistency.

#### 3. Objective Function

The problem asks to maximize profit (implied by "trading company", "wholesale", and providing buy/sell prices).
Profit = Total Revenue - Total Cost.
Total Revenue = $\sum_{t=1}^{3} P^{sell}_t y_t$
Total Cost = $\sum_{t=1}^{3} P^{buy}_t x_t$

**Maximize:**
$$ Z = \sum_{t=1}^{3} (P^{sell}_t y_t - P^{buy}_t x_t) $$
$$ Z = 3.10 y_1 + 3.25 y_2 + 2.95 y_3 - 2.85 x_1 - 3.05 x_2 - 2.90 x_3 $$

#### 4. Operational Constraints

**A. Inventory Balance Constraints**
The inventory at the end of month $t$ is the inventory from the previous month plus purchases in month $t$ minus sales in month $t$.
$$ I_t = I_{t-1} + x_t - y_t \quad \forall t \in \{1, 2, 3\} $$
Where $I_0 = 1,000$.

*Constraint Check regarding "Sold starting next month":*
Does the equation $I_t = I_{t-1} + x_t - y_t$ allow selling $x_t$ in month $t$?
Yes, algebraically, if we just use the balance equation, $y_t$ could be funded by $x_t$.
To enforce the rule "Grain purchased in month $t$ cannot be sold in month $t$", we need to ensure that the sales $y_t$ are covered by inventory available *before* the month's purchases are added, or specifically exclude $x_t$ from the sellable pool.
Since $I_{t-1}$ is the inventory at the end of the previous month, it contains grain purchased in $t-1$ (which is now old enough to sell) and older grain.
The grain purchased in month $t$ ($x_t$) arrives *during* month $t$. The rule says it can only be sold starting in the *next* month ($t+1$).
Therefore, the maximum amount that can be sold in month $t$ is the inventory available at the beginning of month $t$, which is $I_{t-1}$.
So, we add the constraint:
$$ y_t \le I_{t-1} \quad \forall t \in \{1, 2, 3\} $$
This constraint ensures that we only sell what we had on hand at the start of the month. The new purchases $x_t$ add to $I_t$ but are not available for $y_t$.
For $t=1$: $y_1 \le I_0 = 1,000$. (Initial stock is sellable).
For $t=2$: $y_2 \le I_1$. ($I_1$ includes $x_1$, which was purchased in month 1, so it is eligible for sale in month 2. Correct).
For $t=3$: $y_3 \le I_2$. ($I_2$ includes $x_2$, eligible for sale in month 3. Correct).

**B. Warehouse Capacity Constraints**
The warehouse capacity is 5,000 dan. This applies to the inventory level.
$$ I_t \le 5,000 \quad \forall t \in \{1, 2, 3\} $$
Note: Does the capacity constraint apply to $I_0$? $I_0=1000 \le 5000$, so it's fine.
Does it apply to transient states? The balance equation defines $I_t$ as the end-of-month level. Usually, capacity constraints apply to the stored inventory.

**C. Cash Flow Constraints**
"Cash payment upon delivery."
Available capital is 20,000 yuan. This is the initial cash $M_0$.
The company cannot spend more than it has.
Cash Balance Equation for month $t$:
$$ M_t = M_{t-1} + P^{sell}_t y_t - P^{buy}_t x_t \quad \forall t \in \{1, 2, 3\} $$
Where $M_0 = 20,000$.

Non-negativity of cash (No borrowing allowed unless specified, "available capital" implies a budget limit):
$$ M_t \ge 0 \quad \forall t \in \{1, 2, 3\} $$

**D. Target Inventory Constraint**
"The target inventory at the end of March is 2,000 dan."
This is a specific requirement.
$$ I_3 = 2,000 $$

**E. Non-negativity**
$$ x_t \ge 0, \quad y_t \ge 0, \quad I_t \ge 0, \quad M_t \ge 0 \quad \forall t \in \{1, 2, 3\} $$

### Summary of the Formulation

**Model Type:** LP

**Sets:**
$T = \{1, 2, 3\}$

**Parameters:**
- $I_0 = 1,000$
- $M_0 = 20,000$
- $C_{max} = 5,000$
- $I_{target} = 2,000$
- $P^{buy} = [2.85, 3.05, 2.90]$
- $P^{sell} = [3.10, 3.25, 2.95]$

**Variables:**
- $x_t \in \mathbb{R}^+$: Purchases in month $t$
- $y_t \in \mathbb{R}^+$: Sales in month $t$
- $I_t \in \mathbb{R}^+$: End-of-month inventory in month $t$
- $M_t \in \mathbb{R}^+$: End-of-month cash in month $t$

**Objective:**
Maximize $Z = 3.10 y_1 + 3.25 y_2 + 2.95 y_3 - 2.85 x_1 - 3.05 x_2 - 2.90 x_3$

**Constraints:**
1.  **Inventory Balance:**
    $I_1 = 1,000 + x_1 - y_1$
    $I_2 = I_1 + x_2 - y_2$
    $I_3 = I_2 + x_3 - y_3$

2.  **Sellability Lag (Sales limited by beginning-of-month inventory):**
    $y_1 \le 1,000$
    $y_2 \le I_1$
    $y_3 \le I_2$

3.  **Capacity:**
    $I_1 \le 5,000$
    $I_2 \le 5,000$
    $I_3 \le 5,000$

4.  **Cash Flow:**
    $M_1 = 20,000 + 3.10 y_1 - 2.85 x_1 \ge 0$
    $M_2 = M_1 + 3.25 y_2 - 3.05 x_2 \ge 0$
    $M_3 = M_2 + 2.95 y_3 - 2.90 x_3 \ge 0$

5.  **Target Inventory:**
    $I_3 = 2,000$

6.  **Non-negativity:**
    $x_t \ge 0, y_t \ge 0, I_t \ge 0, M_t \ge 0$ for all $t \in \{1, 2, 3\}$.