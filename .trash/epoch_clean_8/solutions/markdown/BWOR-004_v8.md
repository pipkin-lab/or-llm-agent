To formulate this problem, we must carefully track the workforce dynamics (hiring, training, attrition) and the inventory flow (production, demand, storage costs) over the 6-month horizon.

### 1. Model Type Declaration
**Model Type:** Mixed Integer Linear Programming (MILP)
*   **Reasoning:** The number of skilled workers and trainees must be integer values (discrete physical units). Production quantities can be continuous or integer; given the scale (thousands of units) and labor constraints, integer production is safer, but often treated as continuous in large-scale LPs. However, since workers are discrete and "each unit requires 4 hours," and workers work 160 hours, the capacity is discrete. We will define worker variables as integers. Production variables can be continuous, but to ensure exact fulfillment of "4 hours per unit" with discrete workers, we will treat production as continuous constrained by total available labor hours.

### 2. Index Sets & Parameters

**Index Sets:**
*   $t \in \{1, 2, 3, 4, 5, 6\}$: Months (January to June).

**Parameters:**
*   $D_t$: Predicted demand in month $t$.
    *   $D_1 = 3000, D_2 = 3600, D_3 = 4000, D_4 = 4600, D_5 = 4800, D_6 = 5000$.
*   $H_{sk}$: Hours per skilled worker per month = 160.
*   $h_{unit}$: Hours per unit of production = 4.
*   $c_{mat}$: Raw material cost per unit = $\$150$.
*   $p_{sell}$: Selling price per unit = $\$240$.
*   $W_0$: Initial skilled workers at start of Jan = 80.
*   $I_0$: Initial inventory at start of Jan = 400.
*   $c_{store}$: Storage cost per unit per month = $\$10$.
*   $c_{train\_hour}$: Cost of skilled worker time for training = $\$2,000 / 160 \text{ hours} = \$12.5/\text{hour}$? No, the problem states "Training a new worker takes 50 hours of a skilled worker’s time". The cost is the *opportunity cost* of that time (lost production) or simply the labor cost is already accounted for in the salary?
    *   *Clarification on Training Cost:* The problem states "Skilled workers are paid 2,000 dollars per month." This is a fixed cost. The "50 hours of skilled worker's time" reduces the available production capacity. It does not incur an *additional* cash cost beyond the salary, but it consumes capacity.
    *   $T_{hours}$: Hours of skilled labor required to train one new worker = 50.
*   $c_{sk}$: Salary per skilled worker per month = $\$2,000$.
*   $c_{tr}$: Allowance per trainee per month = $\$800$.
*   $\alpha$: Attrition rate = 0.02 (2%).
*   $I_{max, 6}$: Max ending inventory in June = 100.

### 3. Decision Variables

*   $S_t$: Number of **skilled workers** available for production/training at the **beginning** of month $t$. (Integer, $\ge 0$)
*   $H_t$: Number of **trainees** hired at the beginning of month $t$. (Integer, $\ge 0$)
    *   *Note:* Trainees work for 1 month. They become skilled workers at the *beginning* of the next month (start of $t+1$).
*   $x_t$: Number of units **produced** in month $t$. (Continuous, $\ge 0$)
*   $I_t$: Ending **inventory** in month $t$. (Continuous, $\ge 0$)

### 4. Objective Function

**Goal:** Maximize Total Revenue (Profit is implied by "revenue... while satisfying... costs"? The prompt says "maximizing the total revenue". In OR contexts, "revenue" sometimes loosely means "net profit" or "net benefit". However, strictly "revenue" is just $p_{sell} \times x$. But if we just maximize revenue, we would produce as much as possible. The constraints limit production to demand + inventory limits. Usually, "maximize revenue" in cost-included problems implies **Maximize Net Profit** (Revenue - Costs). Let's look at the wording: "maximizing the total revenue". If it meant profit, it would say profit. However, standard business problems asking to "maximize revenue" with explicit costs usually imply maximizing **Profit** (Net Income). If we maximize Gross Revenue, we ignore the costs of labor/materials. Given the detailed cost structure, it is highly likely the objective is **Maximize Net Profit**.
*Correction*: Re-reading carefully: "maximizing the total revenue". In many textbook problems, "revenue" is used interchangeably with "profit" if costs are subtracted, or it's a typo for "profit". If we strictly maximize Revenue ($\sum 240 x_t$), we would produce to the maximum capacity allowed by labor, regardless of material/labor cost, potentially losing money. But we are constrained by Demand. We can only sell what we demand (or store). If we produce more than demand, we store it. Storage costs apply.
Let's assume the standard interpretation: **Maximize Net Profit**.
Profit = Total Sales - Total Material Costs - Total Labor Costs (Skilled + Trainees) - Total Storage Costs.

$$ \text{Maximize } Z = \sum_{t=1}^{6} (p_{sell} \cdot x_t - c_{mat} \cdot x_t - c_{sk} \cdot S_t - c_{tr} \cdot H_t - c_{store} \cdot I_t) $$

*Wait*, does the factory pay for labor even if not used? "Skilled workers are paid 2,000 dollars per month." Yes, fixed cost.
Does the training time cost extra? No, it's part of the skilled worker's time. The cost is the salary, which is paid regardless. The *constraint* is that training time reduces production time.

So, Objective:
$$ \text{Maximize } Z = \sum_{t=1}^{6} \left[ 240 x_t - 150 x_t - 2000 S_t - 800 H_t - 10 I_t \right] $$
$$ \text{Maximize } Z = \sum_{t=1}^{6} \left[ 90 x_t - 2000 S_t - 800 H_t - 10 I_t \right] $$

*(Note: If "Revenue" strictly means Gross Revenue, the costs would not be in the objective, but that makes the cost data irrelevant, which is unlikely in an OR problem with such specific cost details. We proceed with Net Profit.)*

### 5. Operational Constraints

#### A. Workforce Balance (Recurrence)
The number of skilled workers at the beginning of month $t+1$ depends on:
1.  Skilled workers at beginning of month $t$ ($S_t$).
2.  Minus attrition: $2\%$ of $S_t$ leave. The problem states "2% of skilled workers (including those newly trained and on the job for at least one month) leave". This phrasing is slightly ambiguous. Usually, attrition applies to the existing pool. "Including those newly trained..." suggests that workers who *just* finished training in month $t$ (and thus joined the skilled pool at start of $t+1$) might also be subject to attrition? Or does it mean the 2% applies to the total skilled workforce present?
    *   Standard interpretation: At the end of month $t$ (or beginning of $t+1$), 2% of the current skilled workers leave.
    *   Let's refine the timing.
    *   Start of Month $t$: We have $S_t$ skilled workers.
    *   During Month $t$:
        *   We hire $H_t$ trainees.
        *   Skilled workers work. 2% of $S_t$ leave. Do they leave at the end of the month? "Each month, 2% ... leave". Let's assume attrition happens at the end of the month, reducing the count for the next month.
        *   Trainees $H_t$ finish training at the end of Month $t$ and become skilled workers at the Start of Month $t+1$.
    *   So, $S_{t+1} = S_t \cdot (1 - 0.02) + H_t$.
    *   *Check on "including those newly trained"*: If the 2% applies to the workers *present* during the month, then the $H_t$ trainees are not skilled workers *during* month $t$, so they don't leave. They join the skilled pool for month $t+1$. In month $t+1$, they are part of $S_{t+1}$ and subject to the next month's attrition. This fits the recurrence $S_{t+1} = 0.98 S_t + H_t$.
    *   Are $S_t$ integers? Yes. Does $0.98 S_t$ result in an integer? Not necessarily. We must handle this carefully. In linear programming, we cannot have $0.98 S_t$ if $S_t$ is integer without making the constraint non-linear or using big-M/integer logic.
    *   *Alternative:* Define $L_t$ as the number of workers leaving in month $t$.
        *   $L_t = \text{round}(0.02 S_t)$? No, must be linear.
        *   Usually, in such problems, if the percentage is small, we might assume the attrition is deterministic and fractional workers are not allowed, so we must enforce $L_t$ to be the exact 2%. But 2% of an integer is not always an integer.
        *   *Standard OR Approach:* Often, the problem implies that the 2% is an expected value, or we assume the workforce is large enough that we can treat it as continuous for the recurrence, but the variable $S_t$ must be integer. If we write $S_{t+1} = 0.98 S_t + H_t$, and $S_t, S_{t+1}, H_t$ are integers, then $0.02 S_t$ must be an integer, i.e., $S_t$ must be a multiple of 50. This is a strong constraint.
        *   *Better Approach:* Introduce an integer variable $A_t$ for attrition in month $t$.
            *   $A_t \approx 0.02 S_t$.
            *   Constraint: $0.02 S_t - 0.5 \le A_t \le 0.02 S_t + 0.5$? No, that's non-linear if we multiply? No, $A_t$ and $S_t$ are variables. $A_t \ge 0.02 S_t$ and $A_t \le 0.02 S_t + 1$?
            *   Actually, let's look at the phrasing "2% ... leave". If we must maintain integer workers, we can define the relationship as:
                $S_{t+1} = S_t - A_t + H_t$
                Subject to: $A_t = \lfloor 0.02 S_t \rfloor$ or similar? This is non-linear.
            *   *Pragmatic LP/MILP Solution:* In many textbook problems of this type, if the base number is large (80), 2% is 1.6. It's messy. Let's re-read: "2% of skilled workers ... leave".
            *   Let's assume the standard linear approximation where we allow fractional workers in the *logic* of the model but constrain the final count to integer? No, that violates physical reality.
            *   Let's assume the problem expects us to use the linear recurrence $S_{t+1} = 0.98 S_t + H_t$ and declare $S_t$ as **Continuous** or **Integer**?
            *   If $S_t$ is Integer, $0.98 S_t$ is not integer.
            *   Let's check if the problem implies that the 2% is applied to the *total* including trainees? "including those newly trained... on the job for at least one month". This suggests that workers who have been there for 1 month leave. Trainees are on the job for 0 months in month $t$ (they are being trained). So they don't leave in month $t$.
            *   Given the difficulty of integer attrition, and that this is a modeling exercise, we will define $S_t$ as **Continuous** for the recurrence, but note that in practice, one would round. OR, we define $S_t$ as Integer and add the constraint:
                $S_{t+1} \ge S_t + H_t - 0.02 S_t$
                $S_{t+1} \le S_t + H_t - 0.02 S_t + 1$
                This allows for the "rounding" of the 2%.
            *   However, a simpler interpretation often found in such problems is that the "2%" is a rate, and we just use the linear equation $S_{t+1} = 0.98 S_t + H_t$ and treat $S_t$ as **Continuous** variables, acknowledging that in the real world they are integers, but for the sake of the LP formulation, we relax to continuous if the numbers are large, OR we keep them Integer and accept that the model might be infeasible if 0.02*S_t is not integer, which is bad.
            *   Let's look at the initial value: 80. 2% of 80 = 1.6.
            *   Let's assume **Integer** variables for workers and use the standard linear constraint with a tolerance or simply define the attrition variable $A_t$ as integer and link it:
                $A_t \ge 0.02 S_t$
                $A_t \le 0.02 S_t + 1$
                (This ensures $A_t$ is the ceiling of 2%, or close to it).
                Actually, the most robust linear formulation for "approximately 2%" with integers is:
                $S_{t+1} = S_t + H_t - A_t$
                $A_t \ge 0.02 S_t$
                $A_t \le 0.02 S_t + 1$
                $A_t \in \mathbb{Z}^+$
                This is a valid MILP formulation.

#### B. Labor Capacity Constraint (Production + Training)
In month $t$, skilled workers $S_t$ provide $160 S_t$ total hours.
These hours are used for:
1.  Production: $4 x_t$ hours.
2.  Training: $50 H_t$ hours.
(The trainees themselves do not produce or train others in this model, they just receive training).
Constraint:
$$ 4 x_t + 50 H_t \le 160 S_t \quad \forall t \in \{1, \dots, 6\} $$

#### C. Inventory Balance
For each month $t$:
$$ I_t = I_{t-1} + x_t - D_t $$
With $I_0 = 400$.
So:
$$ I_t - I_{t-1} - x_t = -D_t $$
Or:
$$ I_t = I_{t-1} + x_t - D_t $$

#### D. Inventory Bounds
*   Non-negativity: $I_t \ge 0$ for all $t$. (Cannot have negative inventory/backorders unless specified; problem says "ending inventory... not exceed", implies stock on hand).
*   End of June: $I_6 \le 100$.

#### E. Variable Domains
*   $S_t \in \mathbb{Z}^+$ (Integer, positive)
*   $H_t \in \mathbb{Z}^+$ (Integer, positive)
*   $A_t \in \mathbb{Z}^+$ (Integer, positive)
*   $x_t \in \mathbb{R}^+$ (Continuous, positive) - *Note: Production can be continuous. If we want integer production, we can make $x_t$ integer, but with 4 hours/unit and 160 hours/worker, $x_t$ is naturally integer if hours are allocated discretely. However, usually production quantity is continuous in LPs unless "units" are explicitly indivisible. Garments are discrete. So $x_t \in \mathbb{Z}^+$. Let's make $x_t$ Integer to be safe with "units".*
*   $I_t \in \mathbb{R}^+$ (Continuous is fine for inventory, but if $x$ and $D$ are integers, $I$ is integer. So $I_t \in \mathbb{Z}^+$).

### Final Formulation Summary

**Model Type:** MILP

**Parameters:**
*   $D = [3000, 3600, 4000, 4600, 4800, 5000]$
*   $I_0 = 400$
*   $S_0 = 80$ (Initial skilled workers)
*   $c_{sk} = 2000, c_{tr} = 800$
*   $c_{mat} = 150, p_{sell} = 240, c_{store} = 10$
*   $h_{prod} = 4, h_{train} = 50, H_{cap} = 160$
*   $\alpha = 0.02$

**Variables:**
*   $S_t$: Skilled workers at start of month $t$ ($\mathbb{Z}^+$)
*   $H_t$: Trainees hired at start of month $t$ ($\mathbb{Z}^+$)
*   $A_t$: Skilled workers leaving in month $t$ ($\mathbb{Z}^+$)
*   $x_t$: Units produced in month $t$ ($\mathbb{Z}^+$)
*   $I_t$: Ending inventory in month $t$ ($\mathbb{Z}^+$)

**Objective:**
$$ \text{Maximize } Z = \sum_{t=1}^{6} (240 x_t - 150 x_t - 2000 S_t - 800 H_t - 10 I_t) $$
$$ \text{Maximize } Z = \sum_{t=1}^{6} (90 x_t - 2000 S_t - 800 H_t - 10 I_t) $$

**Constraints:**

1.  **Workforce Balance (Attrition & Hiring):**
    For $t=1$:
    $$ S_1 = 80 $$
    For $t=2, \dots, 6$:
    $$ S_t = S_{t-1} - A_{t-1} + H_{t-1} $$
    *(Note: Workers hired as trainees in month $t-1$ finish training and join the skilled pool at the start of month $t$. Workers leaving in month $t-1$ are subtracted from the end-of-month $t-1$ pool, which becomes the start-of-month $t$ pool before adding new skilled graduates? Wait.)*
    
    *Timing Refinement:*
    *   Start Month $t$: Have $S_t$ skilled workers.
    *   During Month $t$:
        *   $A_t$ workers leave.
        *   $H_t$ trainees are hired.
    *   End Month $t$:
        *   Remaining Skilled: $S_t - A_t$.
        *   New Skilled (from trainees): $H_t$.
    *   Start Month $t+1$:
        *   $S_{t+1} = (S_t - A_t) + H_t$.
    
    So the recurrence is:
    $$ S_{t+1} = S_t - A_t + H_t \quad \forall t \in \{1, \dots, 5\} $$
    With $S_1 = 80$.

2.  **Attrition Logic:**
    For each $t \in \{1, \dots, 6\}$:
    $$ A_t \ge 0.02 S_t $$
    $$ A_t \le 0.02 S_t + 1 $$
    *(This ensures $A_t$ is an integer close to 2% of $S_t$. Since $A_t$ is in the objective/cost? No, $A_t$ is not in the objective directly, but $S_t$ and $H_t$ are. The constraint links them.)*
    *Wait*, if $A_t$ is not in the objective, the solver will push $A_t$ to the minimum allowed to maximize $S_{t+1}$ (since higher $S$ allows more production). The constraint $A_t \ge 0.02 S_t$ forces attrition. The upper bound is just to keep it integer-like. Actually, if we want to be precise about "2% leave", and we can't have fractional workers, the constraint $A_t \ge 0.02 S_t$ and $A_t \in \mathbb{Z}$ is sufficient if we assume the factory *must* lose at least 2%. If they can lose *at most* 2%, it would be different. "2% ... leave" implies a deterministic loss. Given the integer constraint, $A_t = \lceil 0.02 S_t \rceil$ is a reasonable physical interpretation. The linear constraints above model this.

3.  **Labor Capacity:**
    For $t \in \{1, \dots, 6\}$:
    $$ 4 x_t + 50 H_t \le 160 S_t $$

4.  **Inventory Balance:**
    For $t \in \{1, \dots, 6\}$:
    $$ I_t = I_{t-1} + x_t - D_t $$
    Where $I_0 = 400$.

5.  **Inventory Limits:**
    $$ I_t \ge 0 \quad \forall t \in \{1, \dots, 6\} $$
    $$ I_6 \le 100 $$

6.  **Variable Bounds:**
    $$ S_t, H_t, A_t, x_t, I_t \ge 0, \quad \text{Integer for all variables except potentially } x_t, I_t \text{ (but we set them to Integer)} $$