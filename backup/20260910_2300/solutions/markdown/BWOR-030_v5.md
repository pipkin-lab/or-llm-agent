# Grain Trading Optimization Model

## Model Type: **MILP** (Mixed Integer Linear Programming)

*Note: While the quantities can technically be continuous (grain is divisible), in many practical contexts, grain is measured in discrete units (dan). However, since "dan" is a unit of weight (50 kg), and the problem deals with large aggregate quantities (thousands of dan), we will treat the decision variables as **CONTINUOUS** non-negative variables. If strict integrality is required for "dan" as a discrete countable unit in a specific context, they could be relaxed to integers, but standard LP relaxation is typically sufficient and preferred for such commodities unless specified otherwise. Given the scale (1000s), continuous is the standard interpretation for commodity trading flows. Let's stick to **LP** as the primary model, noting that if integer constraints are strictly enforced on the number of "batches" or if the problem implies discrete units, it would be MILP. However, usually, grain is treated as continuous mass. I will formulate as **LP** for continuous quantities, as is standard for commodity flow problems unless "number of shipments" is the variable. Here, the variable is quantity in dan.*

**Correction on Variable Domain**: The problem asks for purchase and sale *quantities*. Grain is a divisible commodity. We will use **CONTINUOUS** non-negative variables. Thus, the model is a **LP**.

## Index Sets & Parameters

**Index Sets:**
*   $T = \{1, 2, 3\}$: Set of months (January, February, March).
*   $t \in T$: Index for a specific month.

**Parameters:**
*   $K = 5,000$: Warehouse capacity (dan).
*   $I_0 = 1,000$: Initial inventory at start of Month 1 (dan).
*   $C_0 = 20,000$: Initial available capital (yuan).
*   $I_{final} = 2,000$: Target inventory at end of Month 3 (dan).
*   $P^{buy}_t$: Purchase price in month $t$ (yuan/dan).
    *   $P^{buy}_1 = 2.85$
    *   $P^{buy}_2 = 3.05$
    *   $P^{buy}_3 = 2.90$
*   $P^{sell}_t$: Selling price in month $t$ (yuan/dan).
    *   $P^{sell}_1 = 3.10$
    *   $P^{sell}_2 = 3.25$
    *   $P^{sell}_3 = 2.95$

**Derived/Logic Parameters:**
*   Inventory $I_t$ represents the stock **at the end** of month $t$.
*   Purchases $x_t$ are made in month $t$ and added to inventory at the end of month $t$ (or available immediately for next month's sale, but effectively part of end-of-month $t$ stock).
*   Sales $y_t$ are made in month $t$. The problem states: "Grain arrives in the month it is purchased, but can only be sold starting in the next month." This implies that grain purchased in month $t$ ($x_t$) cannot be sold in month $t$ ($y_t$). It can only be sold in months $> t$.
*   Therefore, the sale $y_t$ in month $t$ must come from inventory available **before** month $t$ (i.e., $I_{t-1}$).

## Decision Variables

*   $x_t \ge 0$: Quantity of grain purchased in month $t$ (dan).
*   $y_t \ge 0$: Quantity of grain sold in month $t$ (dan).

**Domains:**
*   $x_t \in \mathbb{R}^+$ for $t \in \{1, 2, 3\}$
*   $y_t \in \mathbb{R}^+$ for $t \in \{1, 2, 3\}$

## Objective Function

The goal is to **Maximize** the total profit (or equivalently, the final net worth: Final Capital - Initial Capital).

Let $Z$ be the total profit.
$$
\text{Maximize } Z = \sum_{t=1}^{3} (P^{sell}_t \cdot y_t) - \sum_{t=1}^{3} (P^{buy}_t \cdot x_t)
$$

Substituting values:
$$
\text{Maximize } Z = (3.10 y_1 + 3.25 y_2 + 2.95 y_3) - (2.85 x_1 + 3.05 x_2 + 2.90 x_3)
$$

*Note: We maximize profit generated from trading activities. The final capital constraint will ensure the cash flow is feasible.*

## Operational Constraints

### 1. Inventory Balance Constraints
Inventory at the end of month $t$ ($I_t$) is determined by the previous month's inventory, plus purchases in month $t$, minus sales in month $t$.
$$
I_t = I_{t-1} + x_t - y_t \quad \forall t \in \{1, 2, 3\}
$$
With $I_0 = 1,000$.

Explicitly:
*   **End of Month 1:** $I_1 = 1,000 + x_1 - y_1$
*   **End of Month 2:** $I_2 = I_1 + x_2 - y_2$
*   **End of Month 3:** $I_3 = I_2 + x_3 - y_3$

**Target Inventory Constraint:**
The problem states: "The target inventory at the end of March is 2,000 dan."
$$
I_3 = 2,000
$$
Substituting the balance equations:
$$
1,000 + x_1 - y_1 + x_2 - y_2 + x_3 - y_3 = 2,000
$$
$$
\sum_{t=1}^{3} x_t - \sum_{t=1}^{3} y_t = 1,000
$$

### 2. Warehouse Capacity Constraints
The inventory at the end of each month cannot exceed the warehouse capacity $K=5,000$.
$$
I_t \le 5,000 \quad \forall t \in \{1, 2, 3\}
$$
Explicitly:
*   $1,000 + x_1 - y_1 \le 5,000$
*   $I_1 + x_2 - y_2 \le 5,000$
*   $I_2 + x_3 - y_3 \le 5,000$

Also, inventory must be non-negative:
*   $I_t \ge 0 \quad \forall t \in \{1, 2, 3\}$

### 3. Cash Flow Constraints (Capital Availability)
The company starts with $C_0 = 20,000$ yuan.
Cash is spent on purchases and received from sales.
"Grain arrives in the month it is purchased... Cash payment upon delivery." -> Purchase in month $t$ costs money in month $t$.
"Can only be sold starting in the next month." -> Sales in month $t$ generate cash in month $t$ (from inventory available prior to $t$).

Let $C_t$ be the cash available at the **end** of month $t$.
$$
C_t = C_{t-1} - P^{buy}_t x_t + P^{sell}_t y_t
$$
With $C_0 = 20,000$.

The constraint is that cash cannot go negative (assuming no borrowing or credit facilities are mentioned, which is standard unless specified).
$$
C_t \ge 0 \quad \forall t \in \{1, 2, 3\}
$$

Explicitly:
*   **End of Month 1:**
    $$20,000 - 2.85 x_1 + 3.10 y_1 \ge 0$$
*   **End of Month 2:**
    $$(20,000 - 2.85 x_1 + 3.10 y_1) - 3.05 x_2 + 3.25 y_2 \ge 0$$
*   **End of Month 3:**
    $$(20,000 - 2.85 x_1 + 3.10 y_1 - 3.05 x_2 + 3.25 y_2) - 2.90 x_3 + 2.95 y_3 \ge 0$$

### 4. Sale Timing Constraint (Logical Consistency)
The problem states: "Grain arrives in the month it is purchased, but can only be sold starting in the next month."
This implies that sales in month $t$ ($y_t$) can only utilize inventory that existed at the start of month $t$ (i.e., $I_{t-1}$).
This is naturally handled by the inventory balance equation if we interpret $I_{t-1}$ as the stock available for sale in month $t$.
Specifically, $y_t$ is subtracted from $I_{t-1}$ to get $I_t$ after adding $x_t$?
Let's refine the inventory flow to ensure the "next month" rule is strictly modeled.

Standard interpretation:
Start of Month $t$: Inventory $I_{t-1}$.
During Month $t$:
1. Sell $y_t$ (must be $\le I_{t-1}$? Or just $\le I_{t-1} + x_t$? No, "sold starting in the next month" means $x_t$ cannot be sold in month $t$).
So, $y_t$ must be covered by $I_{t-1}$.
Constraint: $y_t \le I_{t-1}$ for $t=1,2,3$.
For $t=1$, $y_1 \le I_0 = 1,000$.
For $t=2$, $y_2 \le I_1$.
For $t=3$, $y_3 \le I_2$.

Then, after selling $y_t$, we add $x_t$ to get end-of-month inventory $I_t$.
$$
I_t = I_{t-1} - y_t + x_t
$$
This formulation explicitly enforces that only pre-existing inventory can be sold in month $t$. The newly purchased grain $x_t$ is added at the end (or available for future months). This matches the problem statement perfectly.

So, we add the explicit constraints:
$$
y_t \le I_{t-1} \quad \forall t \in \{1, 2, 3\}
$$
Substituting $I_{t-1}$ from the balance equations (or keeping $I_t$ as auxiliary variables for clarity):

Let's define auxiliary variables $I_1, I_2, I_3$ for end-of-month inventory to make the model cleaner for a solver.

**Revised Variable Definition:**
*   $x_t$: Purchase in month $t$
*   $y_t$: Sale in month $t$
*   $I_t$: Inventory at end of month $t$

**Constraints:**
1.  **Inventory Balance:**
    *   $I_1 = 1,000 - y_1 + x_1$
    *   $I_2 = I_1 - y_2 + x_2$
    *   $I_3 = I_2 - y_3 + x_3$
2.  **Sale Limitation (Next Month Rule):**
    *   $y_1 \le 1,000$  (Since $I_0=1,000$)
    *   $y_2 \le I_1$
    *   $y_3 \le I_2$
3.  **Capacity:**
    *   $I_1 \le 5,000$
    *   $I_2 \le 5,000$
    *   $I_3 \le 5,000$
    *   $I_t \ge 0$
4.  **Target Inventory:**
    *   $I_3 = 2,000$
5.  **Cash Flow:**
    *   $C_1 = 20,000 - 2.85 x_1 + 3.10 y_1 \ge 0$
    *   $C_2 = C_1 - 3.05 x_2 + 3.25 y_2 \ge 0$
    *   $C_3 = C_2 - 2.90 x_3 + 2.95 y_3 \ge 0$
    *(Where $C_t$ are auxiliary cash variables, or substitute recursively)*

## Final Formulation (Structured)

**Model Type:** LP

**Sets:**
$T = \{1, 2, 3\}$

**Parameters:**
*   $I_0 = 1,000$
*   $K = 5,000$
*   $C_0 = 20,000$
*   $I_{target} = 2,000$
*   $P^{buy} = [2.85, 3.05, 2.90]$
*   $P^{sell} = [3.10, 3.25, 2.95]$

**Variables:**
*   $x_t \ge 0$ : Purchase quantity in month $t$
*   $y_t \ge 0$ : Sale quantity in month $t$
*   $I_t \ge 0$ : Inventory at end of month $t$
*   $C_t \ge 0$ : Cash balance at end of month $t$

**Objective:**
$$
\text{Maximize } Z = \sum_{t=1}^{3} (P^{sell}_t y_t - P^{buy}_t x_t)
$$

**Constraints:**

1.  **Inventory Balance:**
    $$
    \begin{aligned}
    I_1 &= 1,000 - y_1 + x_1 \\
    I_2 &= I_1 - y_2 + x_2 \\
    I_3 &= I_2 - y_3 + x_3
    \end{aligned}
    $$

2.  **Sale Timing (No same-month sale of new stock):**
    $$
    \begin{aligned}
    y_1 &\le 1,000 \\
    y_2 &\le I_1 \\
    y_3 &\le I_2
    \end{aligned}
    $$

3.  **Warehouse Capacity:**
    $$
    \begin{aligned}
    I_1 &\le 5,000 \\
    I_2 &\le 5,000 \\
    I_3 &\le 5,000
    \end{aligned}
    $$

4.  **Target End Inventory:**
    $$
    I_3 = 2,000
    $$

5.  **Cash Flow (Capital Non-Negativity):**
    $$
    \begin{aligned}
    C_1 &= 20,000 - 2.85 x_1 + 3.10 y_1 \\
    C_2 &= C_1 - 3.05 x_2 + 3.25 y_2 \\
    C_3 &= C_2 - 2.90 x_3 + 2.95 y_3
    \end{aligned}
    $$
    $$
    C_1 \ge 0, \quad C_2 \ge 0, \quad C_3 \ge 0
    $$

6.  **Non-negativity:**
    $$
    x_t \ge 0, \quad y_t \ge 0, \quad I_t \ge 0 \quad \forall t \in \{1, 2, 3\}
    $$

### Feasibility Sanity Check

*   **Inventory Flow:**
    *   Start: 1,000.
    *   End Target: 2,000.
    *   Net Change Required: +1,000.
    *   So $\sum x_t - \sum y_t = 1,000$.
*   **Capacity:**
    *   Max inventory 5,000.
    *   If we buy a lot in Month 1, $I_1$ could be up to 5,000.
    *   $I_1 = 1,000 - y_1 + x_1$. Since $y_1 \le 1,000$, min $I_1$ is $x_1$. Max $I_1$ is $1,000 + x_1$ (if $y_1=0$).
    *   Constraint $I_1 \le 5,000$ is active if we buy heavily.
*   **Cash Flow:**
    *   Start 20,000.
    *   Buy price ~3, Sell price ~3.
    *   If we buy 5,000 dan in Month 1 at 2.85, cost = 14,250. Remaining cash = 5,750.
    *   We can sell from initial stock. $y_1 \le 1,000$. Max revenue $y_1=1,000 \times 3.10 = 3,100$.
    *   $C_1 = 20,000 - 14,250 + 3,100 = 8,850 \ge 0$. Feasible.
    *   The model will determine the optimal mix.

This formulation is complete, consistent, and captures all operational rules.