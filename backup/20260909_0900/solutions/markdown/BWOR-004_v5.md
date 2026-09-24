# Optimization Model for Hongdou Garment Factory Production Planning

## 1. Index Sets & Parameters

**Index Sets:**
*   $T = \{1, 2, 3, 4, 5, 6\}$: Set of months (January to June).
*   $t \in T$: Index for a specific month.

**Parameters:**

**Demand & Inventory:**
*   $D_t$: Predicted demand in month $t$ (units).
    *   $D_1 = 3000, D_2 = 3600, D_3 = 4000, D_4 = 4600, D_5 = 4800, D_6 = 5000$.
*   $I_0$: Initial inventory at start of January = 400 units.
*   $I_{max, 6}$: Maximum allowed ending inventory in June = 100 units.
*   $h$: Holding cost per unit per month = $10.

**Labor & Production:**
*   $W_0$: Initial number of skilled workers in January = 80.
*   $H_{cap}$: Maximum working hours per skilled worker per month = 160 hours.
*   $h_{train}$: Hours of skilled labor required to train one trainee per month = 50 hours.
*   $r$: Monthly attrition rate for skilled workers = 2% (0.02).
*   $a_{train}$: Allowance paid to a trainee during the month of training = $800.
*   $w_{skilled}$: Monthly salary for a skilled worker = $2,000.
*   $time\_per\_unit$: Skilled labor hours required to produce one unit = 4 hours.
*   $cost\_material$: Raw material cost per unit = $150.
*   $price$: Selling price per unit = $240.

**Derived Parameters:**
*   $M$: A sufficiently large constant for Big-M constraints (e.g., $M = 1000$).

## 2. Decision Variables

**Continuous Variables:**
*   $N_t$: Number of new trainees hired at the beginning of month $t$.
*   $W_t$: Number of skilled workers available at the beginning of month $t$ (before attrition/training allocation). *Note: We will define $W_t$ as the skilled workforce available for work/training in month $t$.*
*   $P_t$: Total production quantity in month $t$ (units).
*   $I_t$: Ending inventory in month $t$ (units).

**Binary Variables:**
*   *Note: While workforce problems are often formulated with continuous variables in LP contexts, the problem specifies "2% of skilled workers... leave". In standard LP formulations for large-scale aggregate planning, we treat workforce levels as continuous to allow for fractional expected values, or we assume the numbers are large enough that integrality is relaxed. Given the scale (80 workers), integrality might be expected, but standard textbook LPs for this type often relax to continuous. However, "2% leave" implies a linear transition. Let's stick to **Continuous** variables for $W_t$ and $N_t$ as is standard for this class of "Workforce Planning LP" problems unless integer constraints are explicitly demanded by the solver type. If MILP is required, $W_t, N_t$ would be Integer. Given the prompt's general guidance on large scale/aggregate planning, we will use **Continuous** variables to ensure the LP relaxation is the primary model, which is typical for "Design a plan" questions in OR courses unless "integer" is specified. Wait, 80 workers is small. Let's look at the "Integrity & Scale Check". "For farm/resource allocation... prefer CONTINUOUS". "For large-scale multi-period production... use CONTINUOUS". This is a small workforce (80). Usually, workforce is integer. However, the attrition is 2%. If we use integers, the model is MILP. If we use continuous, it's LP. Most standard solutions to this specific problem type (Workforce Planning with Attrition) are solved as LPs. I will define them as Continuous but note that in practice they should be integers. To be safe and rigorous for a general OR model, I will specify them as **Continuous** to match the LP relaxation expectation for aggregate planning, but add a note. Actually, looking at similar problems, if the result is expected to be an integer, it's MILP. If not specified, LP is the default "standard" model. Let's assume **Continuous** for $W_t$ and $N_t$.*

*Correction*: The prompt says "2% of skilled workers... leave". This is a linear relationship. If we use continuous variables, $W_{t+1} = (1-r)W_t + N_t$. This is linear.
Let's define:
*   $W_t$: Skilled workers working in month $t$.
*   $N_t$: New hires (trainees) starting in month $t$.

## 3. Objective Function

**Maximize Total Profit (Revenue - Costs)**

Profit = Total Sales Revenue - Total Labor Costs - Total Material Costs - Total Holding Costs

$$
\text{Maximize } Z = \sum_{t=1}^{6} \left[ \text{Revenue}_t - \text{Labor}_t - \text{Material}_t - \text{Holding}_t \right]
$$

Breaking it down:
1.  **Revenue**: $240 \times P_t$ (assuming all production is sold or held, but usually revenue is recognized on sale. However, in production planning LPs, we often maximize "Contribution Margin" or "Profit". The problem asks to maximize "total revenue". This is slightly ambiguous. Usually, it means Net Profit. "Maximizing revenue" while incurring costs is ill-posed without a profit constraint. Given the context of "Design a labor and production plan... maximizing total revenue", it is highly likely a misstatement for **Maximizing Total Profit** (or Net Income). If we strictly maximize Revenue ($240 P_t$), we would produce as much as possible, which is constrained by labor. Let's assume **Maximize Net Profit**.)
    *   *Self-Correction*: The prompt says "maximizing the total revenue". In many OR contexts, if costs are variable and fixed, maximizing revenue is the same as maximizing profit if fixed costs are constant. Here, labor costs are variable (salary per worker). So maximizing Revenue $\sum 240 P_t$ is equivalent to maximizing Profit $\sum (240 P_t - \text{Costs}_t)$ ONLY IF the costs are not in the objective. But costs ARE incurred. Standard interpretation: Maximize Net Profit.
    *   Let's check the wording again: "maximizing the total revenue". If I produce 1 unit, I gain $240 but spend $150 (material) + Labor. If the problem strictly says Revenue, it might ignore costs? No, that's bad modeling. It almost certainly means **Profit**. I will model **Maximize Net Profit**.

    *   **Material Cost**: $150 \times P_t$.
    *   **Labor Cost**:
        *   Skilled Workers: $2000 \times W_t$.
        *   Trainees: $800 \times N_t$.
    *   **Holding Cost**: $10 \times I_t$. (Applied to ending inventory of each month).

$$
\text{Maximize } Z = \sum_{t=1}^{6} \left( 240 P_t - 150 P_t - 2000 W_t - 800 N_t - 10 I_t \right)
$$
$$
Z = \sum_{t=1}^{6} \left( 90 P_t - 2000 W_t - 800 N_t - 10 I_t \right)
$$

## 4. Operational Constraints

### A. Workforce Dynamics

1.  **Workforce Balance (Transition):**
    The number of skilled workers at the beginning of month $t+1$ is determined by the workers remaining from month $t$ (after 2% attrition) plus the new workers who completed training in month $t$ (i.e., those hired in month $t$).
    
    *Note on Attrition Timing*: "Each month, 2% of skilled workers... leave". Usually, this applies to the workforce present during that month.
    $W_{t+1} = (1 - 0.02) W_t + N_t$
    For $t=1, \dots, 5$.
    Initial: $W_1 = 80$.

    So, for $t=1$:
    $$ W_1 = 80 $$
    For $t=2, \dots, 6$:
    $$ W_t = 0.98 W_{t-1} + N_{t-1} $$

### B. Production Capacity Constraints

The total skilled labor hours available in month $t$ are consumed by:
1.  Training new hires: $50 \times N_t$ hours.
2.  Production: $4 \times P_t$ hours.

The total available hours are $160 \times W_t$.

$$ 50 N_t + 4 P_t \leq 160 W_t \quad \forall t \in T $$

### C. Inventory Balance Constraints

Inventory at the end of month $t$ is the inventory from the previous month plus production minus demand.

For $t=1$:
$$ I_1 = I_0 + P_1 - D_1 = 400 + P_1 - 3000 $$

For $t=2, \dots, 6$:
$$ I_t = I_{t-1} + P_t - D_t $$

### D. Inventory Bounds

1.  **Non-negativity of Inventory**:
    $$ I_t \geq 0 \quad \forall t \in T $$
    *(Note: The problem does not explicitly state that backlogging is allowed. "If garments are not delivered... incur storage cost". This implies we must meet demand from inventory or production. If $I_t < 0$, it would be a backlog. Standard interpretation of "inventory requirements" without explicit backlog allowance is $I_t \geq 0$. If backlogs were allowed, the holding cost structure would usually differ or be symmetric. I will assume $I_t \geq 0$).*

2.  **Ending Inventory Constraint**:
    $$ I_6 \leq 100 $$

### E. Non-negativity

$$ W_t \geq 0, \quad N_t \geq 0, \quad P_t \geq 0 \quad \forall t \in T $$

---

### Summary of the Model

**Sets:**
$T = \{1, \dots, 6\}$

**Parameters:**
$D = [3000, 3600, 4000, 4600, 4800, 5000]$
$I_0 = 400$
$I_{6}^{max} = 100$
$W_1^{init} = 80$
$H_{cap} = 160$
$h_{train} = 50$
$r = 0.02$
$cost_{skilled} = 2000$
$cost_{trainee} = 800$
$cost_{mat} = 150$
$price = 240$
$hold\_cost = 10$
$hrs\_prod = 4$

**Variables:**
$W_t \geq 0, N_t \geq 0, P_t \geq 0, I_t \geq 0 \quad \forall t \in T$

**Objective:**
$$ \text{Maximize } \sum_{t=1}^{6} (240 P_t - 150 P_t - 2000 W_t - 800 N_t - 10 I_t) $$
Simplifies to:
$$ \text{Maximize } \sum_{t=1}^{6} (90 P_t - 2000 W_t - 800 N_t - 10 I_t) $$

**Constraints:**

1.  **Workforce Init:**
    $$ W_1 = 80 $$

2.  **Workforce Transition:**
    $$ W_t - 0.98 W_{t-1} - N_{t-1} = 0 \quad \forall t=2, \dots, 6 $$

3.  **Labor Capacity:**
    $$ 4 P_t + 50 N_t \leq 160 W_t \quad \forall t \in T $$

4.  **Inventory Balance:**
    $$ I_1 - P_1 = 400 - 3000 \implies I_1 - P_1 = -2600 $$
    $$ I_t - I_{t-1} - P_t = -D_t \quad \forall t=2, \dots, 6 $$

5.  **Inventory Limits:**
    $$ I_6 \leq 100 $$
    $$ I_t \geq 0 \quad \forall t \in T $$

6.  **Non-negativity:**
    $$ W_t, N_t, P_t, I_t \geq 0 \quad \forall t \in T $$