**Model Type:** MILP (Mixed-Integer Linear Programming)
*Note: The number of workers must be integer. Production quantities can be continuous or integer depending on interpretation, but typically units are discrete. However, given the scale (thousands of units), we will treat production as continuous variables for standard LP formulation unless strict integrality is required, but worker counts MUST be integer. Given the "1 unit" granularity in demand, we will define production as continuous but bounded by capacity, and workers as integers. Actually, standard practice for such large-scale production planning is often to relax workers to continuous for estimation, but the problem asks for a "labor plan," implying specific headcounts. We will define $W_t$ as INTEGER. Production $P_t$ can be continuous (or integer, but continuous is safer for solver efficiency and often accepted in OR contexts for large $N$; however, to be strictly correct with "units," we will make $P_t$ continuous as labor hours are the bottleneck, but $W_t$ must be integer to represent people. Let's assume $P_t$ is continuous for simplicity, as fractional units of clothing are physically impossible, but with 160 hours and 4 hours/unit, max production is 40 units per worker. With ~80 workers, production is in hundreds. Let's enforce integrality on workers only, and production can be continuous in the LP relaxation, but strictly speaking, production should be integer. I will declare $P_t$ as CONTINUOUS for the model structure but note that in practice it would be integer. For the purpose of this formulation, I will treat $P_t$ as a continuous variable bounded by labor hours, which is standard in production planning LPs. The key discrete variable is the workforce size.*)

### Index Sets & Parameters

**Index Sets:**
*   $t \in \{1, 2, 3, 4, 5, 6\}$: Months (Jan to June).
*   Let $t=1$ be January, $t=6$ be June.

**Parameters:**
*   $D_t$: Demand in month $t$ (units).
    *   $D_1 = 3000$
    *   $D_2 = 3600$
    *   $D_3 = 4000$
    *   $D_4 = 4600$
    *   $D_5 = 4800$
    *   $D_6 = 5000$
*   $h_{labor}$: Skilled labor hours required per unit = 4 hours.
*   $c_{mat}$: Raw material cost per unit = $150.
*   $P_{sell}$: Selling price per unit = $240.
*   $H_{cap}$: Working hours per skilled worker per month = 160 hours.
*   $W_{start}$: Initial skilled workers at start of Jan = 80.
*   $c_{train\_time}$: Skilled worker hours required to train one new worker = 50 hours.
*   $c_{skill}$: Salary per skilled worker per month = $2,000.
*   $c_{trainee}$: Allowance per trainee per month = $800.
*   $r_{attrition}$: Monthly attrition rate for skilled workers = 2% (0.02).
*   $I_{start}$: Initial inventory at start of Jan = 400 units.
*   $I_{max\_end}$: Maximum ending inventory in June = 100 units.
*   $c_{hold}$: Storage cost per unit per month = $10.

**Derived Parameters / Constants:**
*   Max production per skilled worker in month $t$, denoted as $U_t$, depends on whether training occurs.
    *   If a worker is skilled at the *start* of month $t$, they can produce.
    *   Training consumes time *during* the month.
    *   Let $Y_t$ be the number of new workers hired (trainees) at the beginning of month $t$.
    *   These $Y_t$ workers are in training during month $t$. They do NOT produce.
    *   The training requires 50 hours of *skilled* worker time per trainee.
    *   Therefore, the total skilled labor hours available for production in month $t$ is:
        $(\text{Skilled Workers Present in Month } t) \times 160 - 50 \times Y_t$.
    *   *Clarification on "Skilled Workers Present"*:
        *   Workers who leave: 2% of skilled workers *at the beginning of the month* leave? Or end? "Each month, 2% of skilled workers... leave". Usually, attrition happens over the month. Let's assume the 2% leave at the *end* of the month or effectively reduce the effective capacity. Standard interpretation: The workforce available for work in month $t$ is $W_t$. The attrition affects the next month's workforce.
        *   Let $W_t$ be the number of skilled workers working in month $t$.
        *   Let $Y_t$ be the number of trainees starting training in month $t$.
        *   Constraint on Workforce Dynamics:
            *   Workers at start of $t$: $W_t$.
            *   Workers leaving during $t$: $0.02 W_t$? Or is it $0.02$ of the *beginning* of the month?
            *   Usually, $W_{t+1} = W_t (1 - 0.02) + Y_t$.
            *   Let's verify the timing. "Each month, 2% of skilled workers... leave". "Trainees... become skilled workers [after 1 month]".
            *   So, $W_{t+1} = W_t - 0.02 W_t + Y_t = 0.98 W_t + Y_t$.
            *   Note: $Y_t$ must be an integer. $W_t$ must be an integer.
            *   Does the 2% apply to $W_t$ (those working in $t$) or those at the start? Yes, $W_t$ is the workforce for month $t$. The ones who leave are from this group. The survivors ($0.98 W_t$) plus the new graduates ($Y_t$) form $W_{t+1}$.
            *   *Crucial Check*: Can $0.98 W_t$ be non-integer? Yes. But $W_{t+1}$ must be an integer. This implies the attrition might be modeled as a loss of integer workers. However, in LP/MILP formulations of this type, it is common to treat the workforce balance as a linear constraint. If we strictly require integer workers, the term $0.98 W_t$ is problematic for integer programming unless we model the attrition as a separate variable or assume large numbers where rounding is negligible.
            *   *Alternative Interpretation*: The 2% is a rate. We can define $L_t$ (leavers) as a variable. $L_t = 0.02 W_t$. This makes it non-linear or requires linearization if $W_t$ is integer.
            *   *Standard OR Approach for this specific problem type*: Often, the attrition is applied to the *beginning* of the month workforce. Let's assume the constraint is:
                $W_{t+1} = W_t - 0.02 W_t + Y_t$.
                To keep it linear and handle integers, we might relax $W$ to continuous in the LP, or accept that $0.98 W_t$ is a coefficient. If $W_t$ is integer, $0.98 W_t$ is not necessarily integer.
                Let's look at the phrasing: "2% of skilled workers ... leave".
                Let's define the balance as:
                $W_{t+1} = 0.98 W_t + Y_t$.
                If we require $W_t \in \mathbb{Z}$, this constraint is valid in a MILP solver if we allow the RHS to be real, but LHS must be integer. This is fine. The solver will find integer $W_{t+1}$ and $Y_t$ such that the equation holds? No, $0.98 W_t$ is fixed if $W_t$ is fixed. If $W_t=100$, $0.98 W_t = 98$. $W_{11} = 98 + Y_t$. This works perfectly for integer $W_t$ if $W_t$ is a multiple of 50? No. If $W_t=81$, $0.98 \times 81 = 79.38$. Then $W_{t+1} = 79.38 + Y_t$. Since $W_{t+1}$ must be an integer, $Y_t$ would have to be fractional to compensate, or the model is infeasible for $W_t=81$ unless we interpret "2% leave" as "at least 2%" or use an integer number of leavers $A_t \ge 0.02 W_t$.
                *Refined Model*: Let $A_t$ be the number of workers leaving in month $t$.
                Constraint: $A_t \ge 0.02 W_t$.
                Balance: $W_{t+1} = W_t - A_t + Y_t$.
                Objective: Minimize cost of leaving? No, leaving is a loss of revenue/capability, but the cost is just the salary not paid? No, they are paid for the month? "Skilled workers are paid... per month". Usually, if they leave mid-month, they might be paid less, but "per month" suggests a fixed monthly cost for active workers.
                Actually, the problem says "maximizing total revenue".
                Revenue = Sales - Costs.
                Costs = Material + Labor (Skilled) + Trainee Allowance + Holding.
                Sales = $240 \times (\text{Units Sold})$.
                Units Sold = $D_t$ (assuming we meet demand from inventory+production). The problem says "satisfies the monthly... requirements". This implies we must meet demand. If we have excess inventory, we hold it. If we have shortage, we cannot sell? "Satisfies... requirements" usually means $I_{t-1} + P_t \ge D_t$.
                Objective: Maximize Profit = $\sum (240 D_t - 150 D_t) - \text{Labor Costs} - \text{Holding Costs}$.
                Wait, "Revenue" usually means Sales. "Maximizing total revenue" is ambiguous. Does it mean Gross Revenue ($240 \times \text{Units Sold}$) or Profit (Revenue - Costs)?
                Given the detailed cost structure (labor, materials, holding), it is standard to maximize **Profit** (Net Revenue). If it meant Gross Revenue, the cost details would be irrelevant unless they constrain the ability to sell (which they do, via capacity). But if we can always meet demand (by producing enough), Gross Revenue is fixed at $\sum 240 D_t$. Since we *can* recruit, Gross Revenue is likely constant if we meet all demand. The optimization would then be trivial or about minimizing costs.
                Re-reading: "Design a labor and production plan... while maximizing the total revenue".
                In many textbook contexts, "Revenue" is used loosely for "Profit" or "Net Benefit". Or, perhaps we are *not* required to meet all demand? "Satisfies the monthly... requirements". This phrasing strongly suggests Demand is a hard lower bound on sales. If we sell exactly $D_t$, Gross Revenue is constant.
                Is it possible we can sell *more*? "Predicted demand... is as follows". Usually, you can't sell more than demand.
                If Gross Revenue is constant, maximizing it is trivial.
                Therefore, "Maximizing total revenue" MUST be interpreted as **Maximizing Total Profit** (or Net Revenue), i.e., Revenue from sales minus all associated costs.
                
                Let's assume **Maximize Profit**.
                Profit = $\sum_{t=1}^6 [ 240 S_t - 150 P_t - 2000 W_t - 800 Y_t - 10 I_t ]$
                Where $S_t$ is units sold.
                Inventory Balance: $I_t = I_{t-1} + P_t - S_t$.
                Constraint: $S_t \le D_t$ (Cannot sell more than demand).
                Constraint: "Satisfies monthly requirements". This usually means $S_t = D_t$ is required? Or $I_t \ge 0$?
                "Satisfies the monthly ... inventory requirements".
                Usually, this means we must meet the demand in that month. So $S_t = D_t$.
                If $S_t = D_t$ is fixed, then the term $240 D_t$ is constant.
                Then Maximizing Profit is equivalent to **Minimizing Total Costs**.
                Total Cost = $\sum (150 P_t + 2000 W_t + 800 Y_t + 10 I_t)$.
                
                Let's proceed with **Maximizing Profit**, which reduces to **Minimizing Total Variable Costs** given fixed Sales = Demand.
                
                Objective Function:
                Maximize $Z = \sum_{t=1}^6 (240 D_t - 150 P_t - 2000 W_t - 800 Y_t - 10 I_t)$
                Since $\sum 240 D_t$ is constant, this is equivalent to:
                Minimize $C = \sum_{t=1}^6 (150 P_t + 2000 W_t + 800 Y_t + 10 I_t)$
                
                Wait, is there a cost for *leaving*? No, just loss of capacity.
                Is there a cost for *hiring*? "Recruit and train... Training takes 50 hours... Trainees receive... 800". No direct hiring fee mentioned, only the training time cost (opportunity cost of skilled labor) and the trainee allowance.
                
                Let's refine the Production Capacity Constraint.
                In month $t$:
                Skilled workers available: $W_t$.
                Hours available per skilled worker: 160.
                Total skilled hours: $160 W_t$.
                Hours consumed by training: $50 Y_t$.
                Hours available for production: $160 W_t - 50 Y_t$.
                Production $P_t$ requires 4 hours per unit.
                So, $4 P_t \le 160 W_t - 50 Y_t$.
                $\implies P_t \le 40 W_t - 12.5 Y_t$.
                
                Workforce Balance:
                Start of Jan ($t=1$): $W_1 = 80$.
                For $t=1 \dots 5$:
                $W_{t+1} = W_t - A_t + Y_t$.
                Where $A_t$ is attrition.
                Constraint: $A_t \ge 0.02 W_t$.
                To maximize profit (minimize cost), we want to minimize $W_t$ (salary cost) but we need capacity. Attrition is a *loss* of workers. We don't "pay" for the ones who leave, but we lose the capacity. The salary cost is $2000 W_t$ for the workers *present* in month $t$.
                Do we pay the leavers? Usually, if they leave, they are not in $W_t$ for the next month. In month $t$, are they part of $W_t$?
                "At the beginning of January... 80 workers".
                "Each month, 2% ... leave".
                If 2% leave during the month, do they work the full month?
                Standard assumption: The workforce $W_t$ is the number of workers *employed during month t*.
                If they leave, they are not in $W_{t+1}$.
                Does the 2% leave *at the end* of the month or *during*?
                If they leave during, their contribution to production is reduced.
                However, the training constraint uses $W_t$ (skilled workers).
                Let's assume the standard flow:
                $W_t$ = Skilled workers working in month $t$.
                Attrition $A_t$ occurs such that $W_{t+1} = W_t - A_t + Y_t$.
                And $A_t \ge 0.02 W_t$.
                Since we want to minimize cost ($2000 W_t$), and $W_t$ is a decision variable (constrained by previous month), we should minimize $W_t$ as much as possible while satisfying production.
                However, $W_t$ is constrained by $W_{t-1}$ and $Y_{t-1}$.
                
                Let's check the timing of $Y_t$.
                $Y_t$ are trainees *starting* in month $t$.
                They do NOT produce in month $t$.
                They DO produce in month $t+1$ (after completing training).
                So $Y_t$ adds to $W_{t+1}$.
                
                So the system is:
                $W_1 = 80$.
                For $t=1 \dots 5$:
                $W_{t+1} = 0.98 W_t + Y_t$ (Assuming we minimize attrition to exactly 2%? Or is it a constraint $W_{t+1} \le 0.98 W_t + Y_t$? No, attrition is a *fact*. "2% ... leave". It's a fixed rate. So $A_t = 0.02 W_t$ is a deterministic loss.
                If $W_t$ is integer, $0.02 W_t$ might not be integer.
                In real life, you lose integer people.
                Let's use the variable $A_t$ with $A_t \ge 0.02 W_t$ and $A_t \in \mathbb{Z}$.
                Actually, to keep the model simple and standard for this level of problem, we often assume the workforce is large enough that $0.02 W_t$ is effectively integer or we relax to continuous. But $W$ must be integer.
                Let's stick to:
                $W_{t+1} = W_t - A_t + Y_t$
                $A_t \ge 0.02 W_t$
                $A_t \in \mathbb{Z}_{\ge 0}$
                $W_t \in \mathbb{Z}_{\ge 0}$
                $Y_t \in \mathbb{Z}_{\ge 0}$
                
                Production Constraint:
                $4 P_t \le 160 W_t - 50 Y_t$
                $P_t \le 40 W_t - 12.5 Y_t$
                
                Inventory Constraint:
                $I_t = I_{t-1} + P_t - D_t$
                $I_t \ge 0$ (Assuming we must meet demand, so we can't have negative inventory/backorders unless specified. "Satisfies requirements" implies no backorders).
                $I_0 = 400$.
                $I_6 \le 100$.
                
                Objective:
                Maximize Profit.
                Profit = $\sum_{t=1}^6 (240 D_t) - \sum_{t=1}^6 (150 P_t + 2000 W_t + 800 Y_t + 10 I_t)$.
                Note: The holding cost is on $I_t$ (ending inventory). "If garments are not delivered in the month of production, they incur a storage cost... per month". This usually applies to the inventory held at the end of the month.
                
                Let's double check the "Revenue" wording. If it strictly means Gross Revenue, and we must meet demand, the answer is just $\sum 240 D_t$. That's too simple. The cost parameters are clearly meant to be used. So it's Profit.

### Decision Variables

*   $W_t$: Number of skilled workers working in month $t$ (Integer, $\ge 0$).
*   $Y_t$: Number of new trainees hired at the beginning of month $t$ (Integer, $\ge 0$).
*   $A_t$: Number of skilled workers leaving in month $t$ (Integer, $\ge 0$).
*   $P_t$: Number of units produced in month $t$ (Continuous, $\ge 0$). *Note: While units are discrete, for large numbers, continuous is standard in LP. If integer is required, specify $P_t \in \mathbb{Z}$. Given $D_t$ are integers and costs are linear, LP relaxation usually yields integer solutions for such network-like structures, or we can enforce integrality. I will specify Continuous for $P_t$ to allow standard LP/MILP solvers to handle it efficiently, but note that $P_t$ represents physical units.*
*   $I_t$: Inventory at the end of month $t$ (Continuous, $\ge 0$).

### Objective Function

Maximize Total Profit $Z$:
$$ Z = \sum_{t=1}^6 (240 D_t) - \sum_{t=1}^6 (150 P_t + 2000 W_t + 800 Y_t + 10 I_t) $$

Since $\sum_{t=1}^6 240 D_t$ is a constant, this is equivalent to minimizing total costs:
$$ \text{Minimize } C = \sum_{t=1}^6 (150 P_t + 2000 W_t + 800 Y_t + 10 I_t) $$

### Operational Constraints

1.  **Workforce Dynamics:**
    *   Initial Workforce:
        $$ W_1 = 80 $$
    *   Balance for $t = 1, \dots, 5$:
        $$ W_{t+1} = W_t - A_t + Y_t $$
    *   Attrition Constraint (2% leave):
        $$ A_t \ge 0.02 W_t \quad \forall t = 1, \dots, 5 $$
        *(Note: We assume the factory cannot control the rate to be lower than 2%, so this is a lower bound on leavers. To minimize cost, we would prefer fewer workers, but we are forced to lose them. The equation links them exactly.)*

2.  **Production Capacity:**
    *   For each month $t = 1, \dots, 6$:
        The available skilled labor hours are $160 W_t$ minus the hours spent training $Y_t$ new workers ($50 Y_t$).
        Production requires 4 hours per unit.
        $$ 4 P_t \le 160 W_t - 50 Y_t $$
        Or simplified:
        $$ P_t \le 40 W_t - 12.5 Y_t $$
        Also, production cannot be negative:
        $$ P_t \ge 0 $$

3.  **Inventory Balance:**
    *   For each month $t = 1, \dots, 6$:
        $$ I_t = I_{t-1} + P_t - D_t $$
    *   Initial Inventory:
        $$ I_0 = 400 $$
    *   Non-negativity of Inventory (No backorders allowed as we must "satisfy requirements"):
        $$ I_t \ge 0 \quad \forall t = 1, \dots, 6 $$

4.  **Ending Inventory Constraint:**
    *   Ending inventory in June (month 6) must not exceed 100 units:
        $$ I_6 \le 100 $$

5.  **Variable Domains:**
    *   $W_t \in \mathbb{Z}_{\ge 0}$ for $t=1,\dots,6$
    *   $Y_t \in \mathbb{Z}_{\ge 0}$ for $t=1,\dots,6$
    *   $A_t \in \mathbb{Z}_{\ge 0}$ for $t=1,\dots,5$
    *   $P_t \in \mathbb{R}_{\ge 0}$ for $t=1,\dots,6$
    *   $I_t \in \mathbb{R}_{\ge 0}$ for $t=1,\dots,6$

### Final Model Summary

**Model Type:** MILP

**Sets:**
$T = \{1, 2, 3, 4, 5, 6\}$

**Parameters:**
$D = [3000, 3600, 4000, 4600, 4800, 5000]$
$h_L = 4$ (hours/unit)
$c_M = 150$ ($/unit)
$P_{sell} = 240$ ($/unit)
$H_{mon} = 160$ (hours/worker/month)
$W_{start} = 80$
$h_{train} = 50$ (skilled hours/trainee)
$c_S = 2000$ ($/skilled worker/month)
$c_T = 800$ ($/trainee/month)
$r = 0.02$ (attrition rate)
$I_{start} = 400$
$I_{max} = 100$
$c_H = 10$ ($/unit/month)

**Variables:**
$W_t \in \mathbb{Z}^+$ (Skilled workers in month $t$)
$Y_t \in \mathbb{Z}^+$ (Trainees starting in month $t$)
$A_t \in \mathbb{Z}^+$ (Leavers in month $t$)
$P_t \in \mathbb{R}^+$ (Production in month $t$)
$I_t \in \mathbb{R}^+$ (Inventory end of month $t$)

**Objective:**
Maximize $Z = \sum_{t=1}^6 240 D_t - \sum_{t=1}^6 (150 P_t + 2000 W_t + 800 Y_t + 10 I_t)$

**Constraints:**
1.  $W_1 = 80$
2.  $W_{t+1} = W_t - A_t + Y_t, \quad \forall t \in \{1,\dots,5\}$
3.  $A_t \ge 0.02 W_t, \quad \forall t \in \{1,\dots,5\}$
4.  $P_t \le 40 W_t - 12.5 Y_t, \quad \forall t \in \{1,\dots,6\}$
5.  $I_t = I_{t-1} + P_t - D_t, \quad \forall t \in \{1,\dots,6\}$
6.  $I_0 = 400$
7.  $I_t \ge 0, \quad \forall t \in \{1,\dots,6\}$
8.  $I_6 \le 100$
9.  $P_t \ge 0, \forall t$
10. $W_t, Y_t, A_t$ are non-negative integers.