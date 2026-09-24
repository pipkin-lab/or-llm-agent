**Model Type:** MILP (Mixed-Integer Linear Program)
*Note: Since production capacities and demands are integers, and the objective is linear, the constraint matrix is totally unimodular for this network flow structure. Thus, a standard LP solver will yield integer solutions. However, strictly speaking, production quantities are discrete units, so they are defined as Integer variables.*

### 1. Index Sets & Parameters

**Index Sets:**
*   $t \in \{1, 2, 3, 4\}$: Set of quarters.

**Parameters (extracted from Table 3-30):**
*   $C_t$: Production capacity in quarter $t$ (units)
    *   $C_1 = 25$
    *   $C_2 = 35$
    *   $C_3 = 30$
    *   $C_4 = 20$
*   $D_t$: Delivery quantity required in quarter $t$ (units)
    *   $D_1 = 15$
    *   $D_2 = 20$
    *   $D_3 = 25$
    *   $D_4 = 20$
*   $p_t$: Production cost per unit in quarter $t$ (thousand yuan)
    *   $p_1 = 12.0$
    *   $p_2 = 11.0$
    *   $p_3 = 11.5$
    *   $p_4 = 12.5$
*   $h$: Holding/storage cost per unit per quarter (thousand yuan)
    *   $h = 0.1$

**Derived Parameters:**
*   $N$: Total number of quarters, $N=4$.

### 2. Decision Variables

Let $x_t$ be the quantity of equipment produced in quarter $t$.
*   Domain: $x_t \in \mathbb{Z}^+$ (Non-negative integers) for $t \in \{1, 2, 3, 4\}$.

Let $I_t$ be the inventory level at the **end** of quarter $t$.
*   Domain: $I_t \in \mathbb{Z}^+$ (Non-negative integers) for $t \in \{1, 2, 3, 4\}$.
*   Note: $I_4 = 0$ is implied by the balance equation if total production equals total demand, but we will enforce the balance constraints explicitly.

### 3. Objective Function

Minimize the total annual cost, which consists of production costs plus holding costs.

$$ \text{Minimize } Z = \sum_{t=1}^{4} p_t x_t + \sum_{t=1}^{3} h I_t $$

*Note: Inventory at the end of Quarter 4 is zero (all demand met by end of year, no need to carry stock past the planning horizon). Even if we included $h I_4$, the balance constraint will force $I_4=0$. We sum holding costs for $t=1$ to $3$ because $I_4$ is the end-of-year inventory which is 0.*

Substituting values:
$$ Z = 12.0 x_1 + 11.0 x_2 + 11.5 x_3 + 12.5 x_4 + 0.1(I_1 + I_2 + I_3) $$

### 4. Operational Constraints

**1. Inventory Balance Constraints:**
For each quarter $t$, the inventory at the end of the quarter equals the previous inventory plus current production minus current demand.
*   Beginning inventory $I_0 = 0$.
*   Constraint for $t=1$:
    $$ I_1 = I_0 + x_1 - D_1 \implies I_1 = x_1 - 15 $$
*   Constraint for $t=2$:
    $$ I_2 = I_1 + x_2 - D_2 \implies I_2 = I_1 + x_2 - 20 $$
*   Constraint for $t=3$:
    $$ I_3 = I_2 + x_3 - D_3 \implies I_3 = I_2 + x_3 - 25 $$
*   Constraint for $t=4$:
    $$ I_4 = I_3 + x_4 - D_4 \implies I_4 = I_3 + x_4 - 20 $$
    *   Since there is no benefit to holding inventory after the final demand is met (and typically contracts require exact fulfillment by the end of the period without excess carry-over unless specified), and to ensure all production is allocated to specific demands within the year, we impose $I_4 = 0$. This ensures $\sum x_t = \sum D_t = 80$.

**2. Capacity Constraints:**
Production in any quarter cannot exceed the quarterly capacity.
*   $x_1 \le 25$
*   $x_2 \le 35$
*   $x_3 \le 30$
*   $x_4 \le 20$

**3. Non-negativity and Integrality:**
*   $x_t \ge 0, \quad x_t \in \mathbb{Z}$ for $t=1, \dots, 4$
*   $I_t \ge 0, \quad I_t \in \mathbb{Z}$ for $t=1, \dots, 4$

**4. Demand Satisfaction:**
The balance equations combined with $I_t \ge 0$ ensure that demand is met in the current or previous quarters. Specifically, the cumulative production up to any quarter $t$ must be at least the cumulative demand up to $t$:
*   $\sum_{\tau=1}^{t} x_\tau \ge \sum_{\tau=1}^{t} D_\tau$ for $t=1, \dots, 4$.
    *(This is implicitly enforced by $I_t \ge 0$ in the balance equations $I_t = \sum_{\tau=1}^{t} x_\tau - \sum_{\tau=1}^{t} D_\tau$)*.

**Summary of the Linear Model:**

$$
\begin{aligned}
\text{Minimize} \quad & 12.0 x_1 + 11.0 x_2 + 11.5 x_3 + 12.5 x_4 + 0.1 I_1 + 0.1 I_2 + 0.1 I_3 \\
\text{Subject to:} \quad & I_1 = x_1 - 15 \\
& I_2 = I_1 + x_2 - 20 \\
& I_3 = I_2 + x_3 - 25 \\
& I_3 + x_4 - 20 = 0 \quad (\text{i.e., } I_4=0) \\
& x_1 \le 25 \\
& x_2 \le 35 \\
& x_3 \le 30 \\
& x_4 \le 20 \\
& x_t \in \mathbb{Z}^+, I_t \in \mathbb{Z}^+ \quad \forall t
\end{aligned}
$$