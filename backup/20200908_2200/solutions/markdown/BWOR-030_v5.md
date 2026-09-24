# Optimization Model: Grain Trading and Inventory Management

## 1. Index Sets & Parameters

**Index Sets:**
*   $t$: Set of months in the planning horizon, $t \in \{1, 2, 3\}$ (January, February, March).
*   $t+1$: The month of sale corresponding to purchase month $t$ (Sale can only occur in month $t+1$ if purchased in $t$). Note: Since sales start in the next month, grain purchased in March cannot be sold within the Q1 horizon.

**Parameters:**
*   $C_{wh}$: Warehouse capacity = $5,000$ dan.
*   $I_0$: Initial inventory at start of Month 1 = $1,000$ dan.
*   $K_0$: Initial available capital = $20,000$ yuan.
*   $I_{target}$: Target ending inventory at end of Month 3 = $2,000$ dan.
*   $P^{buy}_t$: Purchase price in month $t$ (yuan/dan).
    *   $P^{buy}_1 = 2.85$
    *   $P^{buy}_2 = 3.05$
    *   $P^{buy}_3 = 2.90$
*   $P^{sell}_t$: Selling price in month $t$ (yuan/dan).
    *   $P^{sell}_1 = 3.10$
    *   $P^{sell}_2 = 3.25$
    *   $P^{sell}_3 = 2.95$

## 2. Decision Variables

Let the planning horizon be months $t=1, 2, 3$.

*   $x_t$: Quantity of grain purchased in month $t$ (dan).
    *   Domain: $x_t \ge 0$, continuous (grain is divisible in large quantities, standard LP assumption).
*   $s_t$: Quantity of grain sold in month $t$ (dan).
    *   Domain: $s_t \ge 0$, continuous.
    *   *Note on Timing*: Grain sold in month $t$ must have been in inventory at the start of month $t$ (i.e., purchased in month $t-1$ or earlier). Specifically, $s_1$ comes from initial stock. $s_2$ comes from initial stock + $x_1$. $s_3$ comes from initial stock + $x_1 + x_2$.
*   $I_t$: Inventory level at the **end** of month $t$ (dan).
    *   Domain: $I_t \ge 0$.

## 3. Objective Function

The goal is to **maximize the final wealth** (Final Capital + Final Inventory Value) or equivalently, **maximize Profit**.
Standard practice for trading problems with a fixed ending inventory target is to maximize the final cash balance, assuming the ending inventory is valued at its market price or simply that the objective is to maximize the net financial position.
However, often in these textbook problems, the objective is to **Maximize Profit**, defined as:
$$ \text{Profit} = \text{Total Revenue} - \text{Total Cost} $$
Where:
*   Total Revenue = $\sum_{t=1}^3 P^{sell}_t \cdot s_t$
*   Total Cost = $\sum_{t=1}^3 P^{buy}_t \cdot x_t$
*   *Correction*: We must account for the initial capital constraint and the final state. A more robust objective for "trading company" problems with a fixed end inventory is usually **Maximize Final Cash Balance**. Let's verify if "Profit" is the standard metric.
    *   Initial Cash: 20,000
    *   Cash Flow in Month $t$: $P^{sell}_t s_t - P^{buy}_t x_t$
    *   Final Cash $C_3 = K_0 + \sum_{t=1}^3 (P^{sell}_t s_t - P^{buy}_t x_t)$
    *   Since the ending inventory $I_3$ is fixed at 2,000, the value of that inventory is not "realized" cash. If the question implies maximizing the company's worth, we might add the value of the ending inventory. However, typically "Profit" in short-term trading contexts refers to the cash generated. Let's assume the objective is to **Maximize Final Cash Balance** (or equivalently, Net Profit from trading activities, as initial inventory value is sunk cost and final inventory is a constraint, not a sale).
    
    *Alternative Interpretation Check*: If the goal is to maximize the value of the firm at the end of March, it would be $C_3 + P^{sell}_3 \cdot I_3$ (or purchase price, depending on accounting). However, given the specific "Target Inventory" constraint, the primary decision driver is cash flow. Let's formulate for **Maximizing Net Profit** (Revenue - Purchase Cost), which is linearly equivalent to maximizing Final Cash given fixed initial cash.
    
    Objective: Maximize $Z$
    $$ Z = \sum_{t=1}^3 P^{sell}_t s_t - \sum_{t=1}^3 P^{buy}_t x_t $$
    
    *Self-Correction*: Does the initial inventory have a cost? No, it's already owned. Does the final inventory have a value? It's a constraint. So maximizing (Sales Revenue - Purchase Cost) is the correct proxy for profit generated during the period.

## 4. Operational Constraints

### 4.1 Inventory Balance Constraints
Inventory at the end of month $t$ is the inventory at the start of month $t$ plus purchases in month $t$ minus sales in month $t$.
*Note on Sales Timing*: The problem states "Grain arrives in the month it is purchased, but can only be sold starting in the next month."
This implies:
*   Sales in Month 1 ($s_1$) can only use Initial Inventory ($I_0$). $x_1$ is not available for sale in Month 1.
*   Sales in Month 2 ($s_2$) can use $I_0$ and $x_1$.
*   Sales in Month 3 ($s_3$) can use $I_0$, $x_1$, and $x_2$.

Let $I_t$ be the inventory at the **end** of month $t$.
*   **Month 1 Balance:**
    $$ I_1 = I_0 + x_1 - s_1 $$
    Constraint: $s_1 \le I_0$ (Cannot sell what isn't there). This is covered by $I_1 \ge 0$ and $x_1 \ge 0$, but strictly, $s_1$ is limited by available stock *before* purchase. Since purchase adds to stock, but sale is restricted to *prior* stock, we must be careful.
    Actually, the constraint "sold starting in the next month" means $s_t$ is limited by $\sum_{j=0}^{t-1} (\text{stock added in } j) - \sum_{k=1}^{t-1} s_k$.
    
    Let's write the standard balance equation which naturally enforces non-negativity:
    $$ I_t = I_{t-1} + x_t - s_t \quad \text{for } t=1,2,3 $$
    *Wait*, does $x_t$ contribute to $s_t$? No. The problem says "can only be sold starting in the next month".
    This means $s_t$ cannot include $x_t$.
    The standard balance equation $I_t = I_{t-1} + x_t - s_t$ implies that $x_t$ *could* be sold in month $t$ if $I_{t-1}$ was 0 and $s_t > I_{t-1}$.
    To enforce the "next month sale" rule, we must constrain sales to be less than or equal to the inventory available *before* the purchase in that month is added? Or simply that $s_t$ is limited by the inventory carried over from the previous month?
    
    Let's look at Month 1:
    Available for sale: $I_0 = 1000$.
    $s_1 \le 1000$.
    $I_1 = 1000 + x_1 - s_1$.
    
    Month 2:
    Available for sale: $I_1$ (which includes $x_1$).
    $s_2 \le I_1$.
    $I_2 = I_1 + x_2 - s_2$.
    
    Month 3:
    Available for sale: $I_2$ (which includes $x_2$).
    $s_3 \le I_2$.
    $I_3 = I_2 + x_3 - s_3$.
    
    This set of balance equations combined with $I_t \ge 0$ and $s_t, x_t \ge 0$ correctly models the flow. The restriction "sold starting in next month" is inherently handled if we assume that $x_t$ is added to inventory *after* the sales of month $t$ occur, or more simply, that the inventory available for sale in month $t$ is $I_{t-1}$.
    
    So, the constraints are:
    1.  $I_1 = 1000 + x_1 - s_1$
    2.  $I_2 = I_1 + x_2 - s_2$
    3.  $I_3 = I_2 + x_3 - s_3$
    
    *Crucial Check*: Does $I_1 = 1000 + x_1 - s_1$ allow $s_1 > 1000$?
    If $s_1 = 1100$, then $I_1 = 1000 + x_1 - 1100 = x_1 - 100$.
    If we set $x_1 = 200$, $I_1 = 100$.
    Physically, did we sell 1100 units in Jan? We only had 1000. We bought 200.
    The rule says "can only be sold starting in the next month". So we **cannot** sell the 200 bought in Jan in Jan.
    Therefore, we must explicitly constrain sales to the inventory held *at the beginning* of the month.
    
    **Revised Inventory/Sales Constraints:**
    *   $s_1 \le 1000$  (Sales in Jan limited to Initial Stock)
    *   $s_2 \le 1000 + x_1 - s_1$  (Sales in Feb limited to End-of-Jan Inventory)
    *   $s_3 \le 1000 + x_1 - s_1 + x_2 - s_2$  (Sales in Mar limited to End-of-Feb Inventory)
    
    And the final inventory equation:
    *   $I_3 = 1000 + x_1 + x_2 + x_3 - s_1 - s_2 - s_3$
    
    We can use the recursive balance equations $I_t = I_{t-1} + x_t - s_t$ **IF** we interpret the variable $s_t$ as "sales made from stock available prior to month t". But mathematically, the explicit constraints $s_t \le I_{t-1}$ are safer to enforce the "next month" rule strictly, although in LP solvers, if the objective function incentivizes buying low and selling high, and prices are such that $P^{sell}_{t} > P^{buy}_{t-1}$, the solver might try to "short sell" or use current purchases for current sales if not constrained.
    
    Let's check prices:
    Buy 1: 2.85, Sell 1: 3.10. (Can't sell Buy 1 in Month 1).
    Buy 1: 2.85, Sell 2: 3.25. (Can sell Buy 1 in Month 2).
    Buy 2: 3.05, Sell 2: 3.25. (Can't sell Buy 2 in Month 2).
    Buy 2: 3.05, Sell 3: 2.95. (Loss if sold in Month 3).
    Buy 3: 2.90. (No sale in Q1).
    
    Since $P^{sell}_2 (3.25) > P^{buy}_1 (2.85)$, there is an incentive to buy in Jan and sell in Feb.
    Since $P^{sell}_3 (2.95) < P^{buy}_2 (3.05)$, there is NO incentive to buy in Feb and sell in Mar (unless forced by inventory target, but target is 2000, and we can hold Jan stock).
    
    To be rigorous, we include the explicit availability constraints:
    $$ s_1 \le 1000 $$
    $$ s_2 \le I_1 $$
    $$ s_3 \le I_2 $$
    
    Where $I_1, I_2$ are defined by the balance equations.

### 4.2 Warehouse Capacity Constraints
Inventory at the end of each month cannot exceed capacity.
$$ I_1 \le 5000 $$
$$ I_2 \le 5000 $$
$$ I_3 \le 5000 $$

### 4.3 Capital Constraints (Cash Flow)
The company has 20,000 yuan initially. Purchases require immediate cash payment. Sales generate cash. The company cannot have negative cash balance (assumed, as "available capital" implies a hard budget constraint unless credit is allowed. Standard assumption: no borrowing).

Let $C_t$ be the cash balance at the end of month $t$.
*   $C_0 = 20,000$
*   Cash flow in Month $t$: $P^{sell}_t s_t - P^{buy}_t x_t$
*   Constraint: $C_t \ge 0$ for $t=1,2,3$.

Recursively:
1.  $C_1 = 20000 + 3.10 s_1 - 2.85 x_1 \ge 0$
2.  $C_2 = C_1 + 3.25 s_2 - 3.05 x_2 \ge 0$
3.  $C_3 = C_2 + 2.95 s_3 - 2.90 x_3 \ge 0$

Substituting to avoid auxiliary variables $C_t$ (or keeping them for clarity):
*   $2.85 x_1 - 3.10 s_1 \le 20000$
*   $2.85 x_1 + 3.05 x_2 - 3.10 s_1 - 3.25 s_2 \le 20000$
*   $2.85 x_1 + 3.05 x_2 + 2.90 x_3 - 3.10 s_1 - 3.25 s_2 - 2.95 s_3 \le 20000$

### 4.4 Target Inventory Constraint
The problem states: "The target inventory at the end of March is 2,000 dan."
In optimization, "target" can mean an equality constraint or a goal. Given the context of a standard LP formulation task, it is usually an equality constraint unless "minimize deviation" is specified. We will treat it as a hard constraint.
$$ I_3 = 2000 $$
Using the balance equation:
$$ 1000 + x_1 + x_2 + x_3 - s_1 - s_2 - s_3 = 2000 $$
$$ x_1 + x_2 + x_3 - s_1 - s_2 - s_3 = 1000 $$

### 4.5 Non-negativity
$$ x_t \ge 0, \quad s_t \ge 0, \quad I_t \ge 0 \quad \forall t \in \{1,2,3\} $$

---

## Final Mathematical Formulation

**Decision Variables:**
*   $x_1, x_2, x_3$: Purchases in months 1, 2, 3 (dan)
*   $s_1, s_2, s_3$: Sales in months 1, 2, 3 (dan)
*   $I_1, I_2, I_3$: End-of-month inventory in months 1, 2, 3 (dan)

**Objective Function:**
Maximize Profit $Z$:
$$ Z = 3.10 s_1 + 3.25 s_2 + 2.95 s_3 - 2.85 x_1 - 3.05 x_2 - 2.90 x_3 $$

**Subject to:**

**Inventory Balance:**
1.  $I_1 = 1000 + x_1 - s_1$
2.  $I_2 = I_1 + x_2 - s_2$
3.  $I_3 = I_2 + x_3 - s_3$

**Sales Availability (Enforcing "Next Month" Rule):**
4.  $s_1 \le 1000$
5.  $s_2 \le I_1$
6.  $s_3 \le I_2$

**Warehouse Capacity:**
7.  $I_1 \le 5000$
8.  $I_2 \le 5000$
9.  $I_3 \le 5000$

**Capital Constraints (No Negative Cash):**
10. $-2.85 x_1 + 3.10 s_1 \le 20000$
11. $-2.85 x_1 - 3.05 x_2 + 3.10 s_1 + 3.25 s_2 \le 20000$
12. $-2.85 x_1 - 3.05 x_2 - 2.90 x_3 + 3.10 s_1 + 3.25 s_2 + 2.95 s_3 \le 20000$

**Target Ending Inventory:**
13. $I_3 = 2000$

**Non-negativity:**
14. $x_1, x_2, x_3, s_1, s_2, s_3, I_1, I_2, I_3 \ge 0$

*(Note: Constraint 13 can be substituted into the system to reduce variables, e.g., expressing $x_3$ in terms of others, but leaving it as is is standard for clarity.)*