To formulate the optimal ordering plan for the snow boot store, we must capture the non-linear pricing structure of the order quantities and the inventory dynamics over the 6-month peak season.

### 1. Problem Analysis

*   **Time Horizon**: 6 months ($t=1$ to $6$), corresponding to October, November, December, January, February, and March.
*   **Decision**: How many pairs to order each month.
*   **Constraints**:
    *   Inventory balance: Demand must be met.
    *   Inventory capacity: End-of-month inventory $\le 40$.
    *   Boundary conditions: Initial inventory $I_0 = 0$, Final inventory $I_6 = 0$.
    *   Ordering options: Discrete set of quantities $\{10, 20, 30, 40, 50\}$ or 0.
*   **Costs**:
    *   Variable ordering cost: Non-linear relationship between quantity and cost.
    *   Fixed ordering cost: 10 yuan if $Q_t > 0$.
    *   Holding cost: 0.2 yuan per pair per month (based on $I_t$).
*   **Model Type**: Since the decision variables (order quantities) are discrete integers chosen from a specific set, and the cost structure is non-linear (step function), this is a **Mixed Integer Linear Programming (MILP)** problem if we linearize the cost, or more accurately, a **Mixed Integer Non-Linear Programming (MINLP)** problem if we use direct non-linear cost functions. However, given the small discrete set of order quantities, it is best modeled as a **MILP** by introducing binary variables for each possible order option, which allows us to use standard linear solvers.

Let's define the model using binary variables for the order options to handle the non-linear costs and fixed costs linearly.

### 2. Index Sets & Parameters

**Index Sets:**
*   $t \in \{1, 2, 3, 4, 5, 6\}$: Set of months (1=Oct, 2=Nov, 3=Dec, 4=Jan, 5=Feb, 6=Mar).
*   $k \in \{0, 1, 2, 3, 4, 5\}$: Set of possible order quantity options.
    *   $k=0 \implies Q=0$
    *   $k=1 \implies Q=10$
    *   $k=2 \implies Q=20$
    *   $k=3 \implies Q=30$
    *   $k=4 \implies Q=40$
    *   $k=5 \implies Q=50$

**Parameters:**
*   $D_t$: Demand in month $t$ (pairs).
    *   $D_1=40, D_2=20, D_3=30, D_4=40, D_5=30, D_6=20$.
*   $Q_k$: Order quantity for option $k$ (pairs).
    *   $Q_0=0, Q_1=10, Q_2=20, Q_3=30, Q_4=40, Q_5=50$.
*   $C_k$: Variable ordering cost for option $k$ (yuan).
    *   $C_0=0$
    *   $C_1=48$
    *   $C_2=86$
    *   $C_3=118$
    *   $C_4=138$
    *   $C_5=160$
*   $F$: Fixed ordering cost per order (yuan). $F = 10$.
*   $h$: Holding cost per pair per month (yuan). $h = 0.2$.
*   $I_{max}$: Maximum inventory capacity (pairs). $I_{max} = 40$.
*   $I_0$: Initial inventory. $I_0 = 0$.
*   $I_6$: Final inventory requirement. $I_6 = 0$.

### 3. Decision Variables

*   $x_{t,k}$: Binary variable.
    *   $x_{t,k} = 1$ if option $k$ is chosen in month $t$.
    *   $x_{t,k} = 0$ otherwise.
*   $I_t$: Continuous variable (though it will take integer values given integer inputs).
    *   Inventory level at the **end** of month $t$ (pairs).

### 4. Objective Function

Minimize the total cost, which consists of variable ordering costs, fixed ordering costs, and holding costs.

$$
\text{Minimize } Z = \sum_{t=1}^{6} \left( \sum_{k=0}^{5} C_k x_{t,k} + F \cdot y_t + h \cdot I_t \right)
$$

Where $y_t$ is a binary indicator if an order is placed in month $t$. To avoid introducing extra variables $y_t$, we can incorporate the fixed cost directly into the option costs.
Let $K_k$ be the total cost for option $k$:
*   $K_0 = 0$ (No order, no fixed cost)
*   $K_1 = 48 + 10 = 58$
*   $K_2 = 86 + 10 = 96$
*   $K_3 = 118 + 10 = 128$
*   $K_4 = 138 + 10 = 148$
*   $K_5 = 160 + 10 = 170$

Revised Objective Function:
$$
\text{Minimize } Z = \sum_{t=1}^{6} \left( \sum_{k=0}^{5} K_k x_{t,k} + 0.2 I_t \right)
$$

### 5. Operational Constraints

**1. Exactly one order option selected per month:**
$$
\sum_{k=0}^{5} x_{t,k} = 1, \quad \forall t \in \{1, \dots, 6\}
$$

**2. Inventory Balance Equation:**
Inventory at end of month $t$ = Inventory at end of month $t-1$ + Orders in month $t$ - Demand in month $t$.
$$
I_t = I_{t-1} + \sum_{k=0}^{5} Q_k x_{t,k} - D_t, \quad \forall t \in \{1, \dots, 6\}
$$
With $I_0 = 0$.

**3. Inventory Capacity Constraint:**
End-of-month inventory must not exceed 40 pairs.
$$
0 \le I_t \le 40, \quad \forall t \in \{1, \dots, 5\}
$$
*(Note: $I_0$ and $I_6$ are fixed at 0, so bounds are redundant there but consistent.)*

**4. Final Inventory Constraint:**
Inventory at the end of the season must be zero.
$$
I_6 = 0
$$

**5. Variable Domains:**
$$
x_{t,k} \in \{0, 1\}, \quad \forall t \in \{1, \dots, 6\}, k \in \{0, \dots, 5\}
$$
$$
I_t \ge 0, \quad \forall t \in \{1, \dots, 6\}
$$

### 6. Feasibility Sanity Check

*   **Total Demand**: $40+20+30+40+30+20 = 180$ pairs.
*   **Total Supply**: Must equal 180 pairs since $I_0=I_6=0$.
*   **Order Options**: We need a combination of orders from $\{0, 10, 20, 30, 40, 50\}$ summing to 180.
    *   Example: $30+30+30+30+30+30 = 180$ (6 orders of 30).
    *   Example: $50+50+50+30 = 180$ (4 months order, 2 months zero).
*   **Capacity Check**: Max inventory is 40.
    *   If we order 50 in Oct ($I_1 = 0+50-40=10$).
    *   If we order 50 in Nov ($I_2 = 10+50-20=40$).
    *   If we order 0 in Dec ($I_3 = 40+0-30=10$).
    *   This path seems feasible. The constraint $I_t \le 40$ is tight but satisfiable.
*   **Costs**: All parameters are provided. No missing values.

### Final Model Summary

**Model Type**: MILP (Mixed Integer Linear Programming)

**Objective**:
$$ \min \sum_{t=1}^{6} \left( 58 x_{t,1} + 96 x_{t,2} + 128 x_{t,3} + 148 x_{t,4} + 170 x_{t,5} + 0.2 I_t \right) $$
*(Note: $x_{t,0}$ has cost 0, so it is omitted from the sum, but included in constraints.)*

**Constraints**:
1.  $\sum_{k=0}^{5} x_{t,k} = 1, \quad \forall t=1,\dots,6$
2.  $I_t - I_{t-1} = \sum_{k=1}^{5} Q_k x_{t,k} - D_t, \quad \forall t=1,\dots,6$ (with $I_0=0$)
3.  $I_6 = 0$
4.  $0 \le I_t \le 40, \quad \forall t=1,\dots,5$
5.  $x_{t,k} \in \{0,1\}, \quad \forall t, k$
6.  $I_t \ge 0, \quad \forall t$

**Parameter Values**:
*   $Q = [0, 10, 20, 30, 40, 50]$
*   $K = [0, 58, 96, 128, 148, 170]$
*   $D = [40, 20, 30, 40, 30, 20]$
*   $h = 0.2$
*   $I_{max} = 40$