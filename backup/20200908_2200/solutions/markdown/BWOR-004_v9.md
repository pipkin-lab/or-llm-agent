### 1. Index Sets & Parameters

**Index Sets:**
*   $t \in \{1, 2, 3, 4, 5, 6\}$: Set of months (January to June).
*   $t \in \{0\}$: Beginning of January (initial state).

**Parameters:**
*   $D_t$: Predicted demand in month $t$ (units).
    *   $D_1=3000, D_2=3600, D_3=4000, D_4=4600, D_5=4800, D_6=5000$.
*   $h_{lab}$: Hours required per unit of production = 4 hours/unit.
*   $C_{mat}$: Raw material cost per unit = $150.
*   $P_{sell}$: Selling price per unit = $240.
*   $H_0$: Initial inventory at beginning of January = 400 units.
*   $H_{max, end}$: Maximum allowed ending inventory in June = 100 units.
*   $H_{hold}$: Holding cost per unit per month = $10.
*   $W_0$: Initial number of skilled workers at beginning of January = 80.
*   $H_{work}$: Working hours per skilled worker per month = 160 hours.
*   $T_{train}$: Training hours required per new worker = 50 hours.
*   $C_{skilled}$: Monthly salary per skilled worker = $2,000.
*   $C_{trainee}$: Monthly allowance per trainee = $800.
*   $r_{attr}$: Attrition rate of skilled workers per month = 2% (0.02).
    *   *Note:* Attrition applies to the workforce available at the *beginning* of the month, or more commonly in such models, the workers present during the month. The problem states "Each month, 2% of skilled workers... leave". Standard interpretation: The number of workers leaving in month $t$ is $0.02 \times (\text{Workers available in month } t)$. Let's assume attrition happens based on the workforce present in month $t$.

### 2. Decision Variables

*   $x_t$: Number of units produced in month $t$. (Continuous, $x_t \ge 0$)
*   $H_t$: Inventory level at the *end* of month $t$. (Continuous, $H_t \ge 0$)
    *   $H_0 = 400$.
*   $N_t$: Number of new workers hired (as trainees) at the *beginning* of month $t$. (Continuous, $N_t \ge 0$)
    *   *Note:* While "workers" are discrete, in large-scale aggregate planning (hundreds of workers, thousands of units), it is standard practice to use continuous variables unless integer constraints are explicitly demanded or the scale is very small. Given the scale (80+ workers, 3000+ units), LP relaxation is appropriate and expected for this type of operational planning problem.
*   $W_t$: Number of skilled workers available for production/training in month $t$. (Continuous, $W_t \ge 0$)
    *   *Clarification:* $W_t$ represents the total skilled labor force working in month $t$.

### 3. Objective Function

We want to **Maximize** Total Profit (Revenue - Costs).

**Revenue:**
$R = \sum_{t=1}^{6} P_{sell} \cdot x_t$

**Costs:**
1.  **Raw Material Cost:** $\sum_{t=1}^{6} C_{mat} \cdot x_t$
2.  **Skilled Labor Cost:** $\sum_{t=1}^{6} C_{skilled} \cdot W_t$
3.  **Trainee Allowance Cost:** $\sum_{t=1}^{6} C_{trainee} \cdot N_t$
4.  **Inventory Holding Cost:** $\sum_{t=1}^{6} H_{hold} \cdot H_t$
    *   *Note:* Holding cost is incurred on the ending inventory of each month.

**Objective Function:**
$$ \text{Maximize } Z = \sum_{t=1}^{6} \left[ (P_{sell} - C_{mat}) x_t - C_{skilled} W_t - C_{trainee} N_t - H_{hold} H_t \right] $$

Substituting values:
$$ \text{Maximize } Z = \sum_{t=1}^{6} \left[ (240 - 150) x_t - 2000 W_t - 800 N_t - 10 H_t \right] $$
$$ \text{Maximize } Z = \sum_{t=1}^{6} \left[ 90 x_t - 2000 W_t - 800 N_t - 10 H_t \right] $$

### 4. Operational Constraints

**A. Inventory Balance Constraints**
For each month $t \in \{1, \dots, 6\}$:
$$ H_t = H_{t-1} + x_t - D_t $$
*   $H_0 = 400$
*   $H_t \ge 0$ (No backlogging allowed, implied by "inventory" and standard production planning unless backlogs are explicitly permitted. The problem asks to satisfy demand, and holding costs are for "garments... not delivered", implying we can produce early, but typically "demand" is met from inventory. If backlogging were allowed, we would need a backlog variable. Given "ending inventory... not exceed", it implies $H_t$ is the physical stock. We assume all demand is met in the period or from prior inventory. If $H_t < 0$, it would be a backlog. However, standard formulation with $H_t \ge 0$ assumes no backlogging. Let's assume no backlogging is allowed as is standard for fashion goods with specific monthly demands.)

**B. Ending Inventory Constraint**
$$ H_6 \le 100 $$

**C. Workforce Dynamics (Recruitment and Attrition)**
Let $W_t$ be the number of skilled workers working in month $t$.
Let $N_t$ be the number of new hires (trainees) starting in month $t$.

1.  **Transition of Workforce:**
    Workers hired in month $t$ ($N_t$) are trainees during month $t$ and become skilled workers starting month $t+1$.
    Skilled workers in month $t$ ($W_t$) are subject to attrition. The problem states "2% of skilled workers... leave". This usually means the workforce at the start of the month or during the month reduces.
    
    Let's define the flow:
    *   Skilled workers available in month $t$ is $W_t$.
    *   Of these, some leave. Let's assume the attrition is applied to the workforce present in month $t$.
    *   The skilled workers available for month $t+1$ come from:
        1.  Survivors from $W_t$: $(1 - r_{attr}) W_t$
        2.  Graduates from training in month $t$: $N_t$ (since training takes 1 month, those trained in $t$ are ready in $t+1$).
    
    Therefore, the workforce balance equation is:
    $$ W_{t+1} = (1 - 0.02) W_t + N_t = 0.98 W_t + N_t $$
    for $t = 1, \dots, 5$.
    
    Initial condition:
    $$ W_1 = 80 $$
    *Note:* $N_1$ are hired at the beginning of Jan, train in Jan, and become skilled in Feb. So they do not contribute to $W_1$ production capacity, but they do incur training costs and consume skilled labor hours in month 1.

**D. Production Capacity Constraints**
Production in month $t$ is limited by the total available skilled labor hours.
Total available hours in month $t$ = $W_t \times H_{work} = 160 W_t$.

These hours are consumed by:
1.  Production of units $x_t$: Requires $h_{lab} x_t = 4 x_t$ hours.
2.  Training of new hires $N_t$: Requires $T_{train} N_t = 50 N_t$ hours.
    *   *Assumption:* Skilled workers perform the training. The problem says "Training a new worker takes 50 hours of a skilled worker’s time". This implies the skilled workers in $W_t$ spend part of their 160 hours training $N_t$.

Thus, the capacity constraint for month $t$ is:
$$ 4 x_t + 50 N_t \le 160 W_t $$
for $t = 1, \dots, 6$.

**E. Non-negativity and Domain Bounds**
$$ x_t \ge 0, \quad H_t \ge 0, \quad N_t \ge 0, \quad W_t \ge 0 \quad \forall t \in \{1, \dots, 6\} $$

### Summary of the Model

**Variables:**
*   $x_t \in \mathbb{R}^+$ : Production in month $t$
*   $H_t \in \mathbb{R}^+$ : Ending inventory in month $t$
*   $N_t \in \mathbb{R}^+$ : New hires (trainees) in month $t$
*   $W_t \in \mathbb{R}^+$ : Skilled workers in month $t$

**Objective:**
$$ \text{Max } Z = \sum_{t=1}^{6} (90 x_t - 2000 W_t - 800 N_t - 10 H_t) $$

**Subject to:**

1.  **Inventory Balance:**
    $$ H_t = H_{t-1} + x_t - D_t, \quad \forall t=1,\dots,6 $$
    $$ H_0 = 400 $$

2.  **End-of-Year Inventory Limit:**
    $$ H_6 \le 100 $$

3.  **Workforce Balance:**
    $$ W_1 = 80 $$
    $$ W_{t+1} = 0.98 W_t + N_t, \quad \forall t=1,\dots,5 $$

4.  **Labor Capacity:**
    $$ 4 x_t + 50 N_t \le 160 W_t, \quad \forall t=1,\dots,6 $$

5.  **Non-negativity:**
    $$ x_t, H_t, N_t, W_t \ge 0, \quad \forall t=1,\dots,6 $$