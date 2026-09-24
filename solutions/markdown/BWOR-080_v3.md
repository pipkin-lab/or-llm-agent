To formulate the mathematical model, we must first define the sets, parameters, and variables that capture the production, storage, and capacity constraints over the 6-month horizon.

### MANDATORY COST INVENTORY
*   **Unit Profits ($c_j$)**: Product I: 100, II: 60, III: 80, IV: 40, V: 110, VI: 90, VII: 30 (yuan/unit).
*   **Storage Cost ($h$)**: 5 yuan/unit/month.
*   **Machine Capacities**: Calculated from 24 days/month $\times$ 2 shifts/day $\times$ 8 hours/shift = 384 hours/month per machine.

### Index Sets
*   $T = \{1, 2, 3, 4, 5, 6\}$: Set of months (Jan to Jun).
*   $J = \{1, 2, 3, 4, 5, 6, 7\}$: Set of products (I to VII).
*   $M = \{1, 2, 3, 4, 5\}$: Set of machine types (1: Grinding, 2: Upright Drill, 3: Horizontal Drill, 4: Boring, 5: Planer).

### Parameters
*   $c_j$: Profit per unit of product $j$ (yuan).
    *   $c = [100, 60, 80, 40, 110, 90, 30]$
*   $h = 5$: Monthly storage cost per unit (yuan).
*   $H_{max} = 100$: Maximum inventory level per product (units).
*   $D_{t,j}$: Market demand for product $j$ in month $t$ (units).
    *   See Table C-4 in the problem description.
*   $a_{m,j}$: Machine-hours required on machine type $m$ for one unit of product $j$.
    *   Note: `--` in Table C-3 implies 0 hours.
    *   Matrix $A$ (rows $m$, cols $j$):
        $$
        A = \begin{bmatrix}
        0.5 & 0.7 & 0 & 0 & 0.3 & 0.2 & 0.5 \\
        0.1 & 0.2 & 0 & 0.3 & 0 & 0.6 & 0 \\
        0.2 & 0 & 0.8 & 0 & 0 & 0 & 0.6 \\
        0.05 & 0.03 & 0 & 0.07 & 0.1 & 0 & 0.08 \\
        0 & 0 & 0.01 & 0 & 0.05 & 0 & 0.05
        \end{bmatrix}
        $$
*   $Cap_{m,t}$: Total available hours for machine type $m$ in month $t$.
    *   Base capacity: $384$ hours per machine.
    *   Number of machines per type:
        *   $N_1 = 4$ (Grinding)
        *   $N_2 = 2$ (Upright Drill)
        *   $N_3 = 3$ (Horizontal Drill)
        *   $N_4 = 1$ (Boring)
        *   $N_5 = 1$ (Planer)
    *   Maintenance deductions (hours lost = $384 \times$ machines down):
        *   $t=1$ (Jan): 1 Grinding down $\rightarrow Cap_{1,1} = (4-1)\times 384 = 1152$. Others full.
        *   $t=2$ (Feb): 2 Horizontal Drills down $\rightarrow Cap_{3,2} = (3-2)\times 384 = 384$. Others full.
        *   $t=3$ (Mar): 1 Boring down $\rightarrow Cap_{4,3} = (1-1)\times 384 = 0$. Others full.
        *   $t=4$ (Apr): 1 Upright Drill down $\rightarrow Cap_{2,4} = (2-1)\times 384 = 384$. Others full.
        *   $t=5$ (May): 1 Grinding, 1 Upright Drill down $\rightarrow Cap_{1,5} = 3 \times 384 = 1152$, $Cap_{2,5} = 1 \times 384 = 384$. Others full.
        *   $t=6$ (Jun): 1 Planer, 1 Horizontal Drill down $\rightarrow Cap_{5,6} = 0$, $Cap_{3,6} = 2 \times 384 = 768$. Others full.

    *   *Explicit Capacity Vectors ($Cap_{m,t}$ for $m=1..5, t=1..6$)*:
        *   $t=1$: $[1152, 768, 1152, 384, 384]$
        *   $t=2$: $[1536, 768, 384, 384, 384]$
        *   $t=3$: $[1536, 768, 1152, 0, 384]$
        *   $t=4$: $[1536, 384, 1152, 384, 384]$
        *   $t=5$: $[1152, 384, 1152, 384, 384]$
        *   $t=6$: $[1536, 768, 768, 384, 0]$

### Decision Variables
*   $x_{t,j}$: Number of units of product $j$ produced in month $t$.
    *   Domain: $x_{t,j} \in \mathbb{R}_{\ge 0}$ (Continuous, as production quantities are aggregate and large).
*   $I_{t,j}$: Inventory of product $j$ at the **end** of month $t$.
    *   Domain: $I_{t,j} \in \mathbb{R}_{\ge 0}$.

### Objective Function
Maximize total profit (revenue from sales minus storage costs). Note that production cost is implicit in the "profit per unit" given, so we maximize sum of (Sales Profit) - (Storage Costs).

$$
\text{Maximize } Z = \sum_{t=1}^{6} \sum_{j=1}^{7} \left( c_j \cdot S_{t,j} - h \cdot I_{t,j} \right)
$$

Where $S_{t,j}$ is the amount sold in month $t$. Since we assume production meets demand up to the limit, and we track inventory, it is cleaner to express the objective in terms of production and inventory changes, or simply recognize that Profit = (Sales $\times$ Price) - (Storage). However, the standard formulation for "profit per unit" usually implies the margin after production costs. The problem states "profit per unit", so $c_j$ is the contribution margin.
We must be careful: Do we earn profit on units *produced* or units *sold*? Typically, profit is realized upon sale. However, in production planning LPs with "unit profit" given, it is standard to maximize $\sum c_j x_{t,j} - \sum h I_{t,j}$ **IF** the constraint is that we cannot sell more than demand and we must satisfy initial/final inventory conditions.
Let's verify the flow:
Inventory Balance: $I_{t,j} = I_{t-1,j} + x_{t,j} - S_{t,j}$.
Sales $S_{t,j} \le D_{t,j}$.
If we produce more than we sell, it goes to inventory. The profit $c_j$ is earned when the unit is sold.
So, Objective: $\sum_{t,j} c_j S_{t,j} - \sum_{t,j} h I_{t,j}$.
Substituting $S_{t,j} = I_{t-1,j} + x_{t,j} - I_{t,j}$:
$$
Z = \sum_{t=1}^{6} \sum_{j=1}^{7} c_j (I_{t-1,j} + x_{t,j} - I_{t,j}) - \sum_{t=1}^{6} \sum_{j=1}^{7} h I_{t,j}
$$
Rearranging terms to simplify implementation (optional but good for clarity):
$$
Z = \sum_{j} c_j I_{0,j} + \sum_{t,j} c_j x_{t,j} - \sum_{t,j} c_j I_{t,j} - \sum_{t,j} h I_{t,j}
$$
Since $I_{0,j} = 0$ for all $j$, this becomes:
$$
\text{Maximize } Z = \sum_{t=1}^{6} \sum_{j=1}^{7} c_j x_{t,j} - \sum_{t=1}^{6} \sum_{j=1}^{7} (c_j + h) I_{t,j}
$$
Wait, this transformation assumes we can sell any amount. But we are limited by demand $D_{t,j}$.
Actually, the most robust formulation keeps $S_{t,j}$ as a variable or simply enforces that production plus beginning inventory equals sales plus ending inventory, with sales capped by demand.
Let's stick to the direct definition:
$$
\text{Maximize } Z = \sum_{t=1}^{6} \sum_{j=1}^{7} c_j S_{t,j} - \sum_{t=1}^{6} \sum_{j=1}^{7} h I_{t,j}
$$
Subject to Sales Constraints: $S_{t,j} \le D_{t,j}$.
And Inventory Balance: $I_{t,j} = I_{t-1,j} + x_{t,j} - S_{t,j}$.

However, since $S_{t,j}$ only appears in the objective with a positive coefficient $c_j$ and in the balance constraint, and $I_{t,j}$ has a negative cost, the solver will maximize $S_{t,j}$ up to $\min(D_{t,j}, I_{t-1,j} + x_{t,j})$.
To reduce variables, we can eliminate $S_{t,j}$:
From balance: $S_{t,j} = I_{t-1,j} + x_{t,j} - I_{t,j}$.
Constraint: $0 \le S_{t,j} \le D_{t,j} \implies 0 \le I_{t-1,j} + x_{t,j} - I_{t,j} \le D_{t,j}$.
Substitute $S_{t,j}$ into Objective:
$$
Z = \sum_{t=1}^{6} \sum_{j=1}^{7} c_j (I_{t-1,j} + x_{t,j} - I_{t,j}) - \sum_{t=1}^{6} \sum_{j=1}^{7} h I_{t,j}
$$
$$
Z = \sum_{t=1}^{6} \sum_{j=1}^{7} c_j x_{t,j} - \sum_{t=1}^{6} \sum_{j=1}^{7} (c_j + h) I_{t,j} + \sum_{j=1}^{7} c_j I_{0,j}
$$
Since $I_{0,j}=0$, the constant term vanishes.
**Final Objective Function:**
$$
\text{Maximize } Z = \sum_{t=1}^{6} \sum_{j=1}^{7} c_j x_{t,j} - \sum_{t=1}^{6} \sum_{j=1}^{7} (c_j + 5) I_{t,j}
$$

### Operational Constraints

**1. Inventory Balance and Demand Satisfaction**
For each month $t \in T$ and product $j \in J$:
The amount available for sale is Beginning Inventory + Production. This must equal Sales + Ending Inventory.
Sales cannot exceed Demand.
$$
I_{t-1,j} + x_{t,j} - I_{t,j} \le D_{t,j} \quad \forall t \in T, j \in J
$$
$$
I_{t-1,j} + x_{t,j} - I_{t,j} \ge 0 \quad \forall t \in T, j \in J \quad (\text{Non-negative sales})
$$
Or simply:
$$
0 \le I_{t-1,j} + x_{t,j} - I_{t,j} \le D_{t,j}
$$

**2. Inventory Capacity Limits**
Storage limit: No more than 100 units per product at any time.
$$
0 \le I_{t,j} \le 100 \quad \forall t \in T, j \in J
$$

**3. Initial and Final Inventory Conditions**
Initial inventory (Jan 1): 0.
$$
I_{0,j} = 0 \quad \forall j \in J
$$
Final inventory (End of June): 50 units of each product.
$$
I_{6,j} = 50 \quad \forall j \in J
$$
*(Note: Since $I_{6,j}$ is fixed to 50, the upper bound $I_{t,j} \le 100$ is automatically satisfied for $t=6$. The variable $I_{6,j}$ can be removed from the optimization and treated as a parameter in the balance equation for $t=6$, or kept as a variable with equality constraint. Keeping it as a variable with equality is cleaner for the general structure.)*

**4. Machine Capacity Constraints**
For each month $t \in T$ and machine type $m \in M$:
Total hours required for production cannot exceed available capacity.
$$
\sum_{j=1}^{7} a_{m,j} x_{t,j} \le Cap_{m,t} \quad \forall t \in T, m \in M
$$

**5. Non-negativity**
$$
x_{t,j} \ge 0 \quad \forall t \in T, j \in J
$$
$$
I_{t,j} \ge 0 \quad \forall t \in T, j \in J
$$

### Model Type Declaration
**LP** (Linear Programming). All variables are continuous.

### Parameter Completeness Check
*   $c_j$: Provided in Table C-3.
*   $a_{m,j}$: Provided in Table C-3.
*   $D_{t,j}$: Provided in Table C-4.
*   $Cap_{m,t}$: Derived from text (24 days, 2 shifts, 8 hrs, machine counts, maintenance schedule).
*   $h$: 5 yuan/unit/month.
*   $I_{0,j}$: 0.
*   $I_{6,j}$: 50.
*   $H_{max}$: 100.

All parameters are explicitly defined or derived from the text.

### Final Formulation Summary

**Index Sets:**
*   $T = \{1, \dots, 6\}$ (Months)
*   $J = \{1, \dots, 7\}$ (Products)
*   $M = \{1, \dots, 5\}$ (Machine Types)

**Variables:**
*   $x_{t,j} \in \mathbb{R}_+$: Units of product $j$ produced in month $t$.
*   $I_{t,j} \in \mathbb{R}_+$: Units of product $j$ in inventory at end of month $t$.

**Objective:**
$$
\text{Maximize } Z = \sum_{t=1}^{6} \sum_{j=1}^{7} c_j x_{t,j} - \sum_{t=1}^{6} \sum_{j=1}^{7} (c_j + 5) I_{t,j}
$$

**Constraints:**
1.  **Flow/Demand:**
    $$
    0 \le I_{t-1,j} + x_{t,j} - I_{t,j} \le D_{t,j} \quad \forall t \in T, j \in J
    $$
    *(Note: $I_{0,j} = 0$ for all $j$.)*

2.  **Inventory Bounds:**
    $$
    0 \le I_{t,j} \le 100 \quad \forall t \in T, j \in J
    $$

3.  **Final Inventory Fix:**
    $$
    I_{6,j} = 50 \quad \forall j \in J
    $$

4.  **Machine Capacities:**
    $$
    \sum_{j=1}^{7} a_{m,j} x_{t,j} \le Cap_{m,t} \quad \forall t \in T, m \in M
    $$
    *(Where $a_{m,j}$ and $Cap_{m,t}$ are as defined in the Parameters section.)*