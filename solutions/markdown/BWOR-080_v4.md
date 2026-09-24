To formulate this problem, we must define the sets, parameters, and decision variables that capture the production, inventory, and machine availability constraints over the 6-month horizon.

### 1. Model Type Declaration
**Model Type:** MILP (Mixed Integer Linear Programming)
*Note: While the objective is linear and constraints are linear, production quantities are typically discrete physical units. However, given the large scale of demands (hundreds/thousands) and the continuous nature of time/resource allocation in many factory planning contexts, this is often solved as an LP. If integer constraints are required for physical units, it is an MILP. Given the "machine-hours" are continuous resources, and demands are large, an LP formulation is standard and robust for this scale unless "integer units" is strictly enforced. I will define variables as Continuous (LP) as is standard for production planning with large batch sizes, but note that if $x_{jt}$ must be integer, it becomes MILP. Given the prompt asks for "how to plan", and units are products, I will treat them as **Continuous** for mathematical tractability unless specified otherwise, but typically product counts are integers. Let's look at the scale: 500, 1000 units. The difference between LP and IP is negligible relative to the scale. I will define them as **Continuous** $\ge 0$ for the primary formulation, as is common in linear programming textbooks for production planning, but I will explicitly state the domain. Actually, standard practice for "units of product" is Integer. However, machine hours are continuous. Let's stick to **MILP** to be safe on the "physical units" aspect, or **LP** if we assume divisible production. Most OR texts treat production volume $x$ as continuous if the numbers are large. I will use **Continuous** variables for production and inventory to ensure a clean LP, which is the standard interpretation for "maximize profit" in linear production planning unless "integer" is explicitly requested. Wait, Rule 2 says "Use INTEGER variables for discrete physical units (e.g., ships, workers, machines)." Products are discrete physical units. I will declare them as **Integer** to be rigorous, acknowledging it is an MILP.

### 2. Index Sets & Parameters

**Sets:**
*   $M$: Set of machine types, $M = \{1, \dots, 6\}$ (Grinding, Upright Drill, Horizontal Drill, Boring, Planer).
    *   $m=1$: Grinding (4 machines)
    *   $m=2$: Upright Drill (2 machines)
    *   $m=3$: Horizontal Drill (3 machines)
    *   $m=4$: Boring Machine (1 machine)
    *   $m=5$: Planer (1 machine)
    *   *(Note: There are 5 distinct machine types listed in the table rows, but the text says "4 grinding, 2 upright, 3 horizontal, 1 boring, 1 planer". The table has 5 rows of equipment. Let's map them:)*
        1.  Grinding
        2.  Upright Drill
        3.  Horizontal Drill
        4.  Boring Machine
        5.  Planer
*   $J$: Set of products, $J = \{1, \dots, 7\}$ (Products I to VII).
*   $T$: Set of months, $T = \{1, \dots, 6\}$ (January to June).

**Parameters:**

*   $a_{mj}$: Machine-hours required on machine type $m$ for one unit of product $j$.
    *   From Table C-3:
        *   $a_{1,1}=0.5, a_{1,2}=0.7, a_{1,5}=0.3, a_{1,6}=0.2, a_{1,7}=0.5$
        *   $a_{2,1}=0.1, a_{2,2}=0.2, a_{2,4}=0.3, a_{2,6}=0.6$
        *   $a_{3,1}=0.2, a_{3,3}=0.8, a_{3,7}=0.6$
        *   $a_{4,1}=0.05, a_{4,2}=0.03, a_{4,4}=0.07, a_{4,5}=0.1, a_{4,7}=0.08$
        *   $a_{5,3}=0.01, a_{5,5}=0.05, a_{5,7}=0.05$
        *   All other $a_{mj} = 0$.

*   $p_j$: Profit per unit of product $j$ (yuan).
    *   From Table C-3:
        *   $p_1=100, p_2=60, p_3=80, p_4=40, p_5=110, p_6=90, p_7=30$.

*   $D_{jt}$: Maximum market demand for product $j$ in month $t$.
    *   From Table C-4 (Rows Jan-Jun, Cols I-VII):
        *   $t=1$ (Jan): $D_{1,1}=500, D_{2,1}=1000, D_{3,1}=300, D_{4,1}=300, D_{5,1}=800, D_{6,1}=200, D_{7,1}=100$
        *   $t=2$ (Feb): $D_{1,2}=600, D_{2,2}=500, D_{3,2}=200, D_{4,2}=0, D_{5,2}=400, D_{6,2}=300, D_{7,2}=150$
        *   $t=3$ (Mar): $D_{1,3}=300, D_{2,3}=600, D_{3,3}=0, D_{4,3}=0, D_{5,3}=500, D_{6,3}=400, D_{7,3}=100$
        *   $t=4$ (Apr): $D_{1,4}=200, D_{2,4}=300, D_{3,4}=400, D_{4,4}=500, D_{5,4}=200, D_{6,4}=0, D_{7,4}=100$
        *   $t=5$ (May): $D_{1,5}=0, D_{2,5}=100, D_{3,5}=500, D_{4,5}=100, D_{5,5}=1000, D_{6,5}=300, D_{7,5}=0$
        *   $t=6$ (Jun): $D_{1,6}=500, D_{2,6}=500, D_{3,6}=100, D_{4,6}=300, D_{5,6}=1100, D_{6,6}=500, D_{7,6}=60$

*   $h_j$: Monthly storage cost per unit for product $j$.
    *   $h_j = 5$ for all $j \in J$.

*   $S_{max}$: Maximum inventory limit per product at any time.
    *   $S_{max} = 100$.

*   $I_{j}^{init}$: Initial inventory for product $j$ at $t=0$.
    *   $I_{j}^{init} = 0$ for all $j$.

*   $I_{j}^{final}$: Required final inventory for product $j$ at end of $t=6$.
    *   $I_{j}^{final} = 50$ for all $j$.

*   $N_m$: Total number of machines of type $m$.
    *   $N_1 = 4$ (Grinding)
    *   $N_2 = 2$ (Upright Drill)
    *   $N_3 = 3$ (Horizontal Drill)
    *   $N_4 = 1$ (Boring Machine)
    *   $N_5 = 1$ (Planer)

*   $H_{total}$: Total available operating hours per machine per month.
    *   24 days/month $\times$ 2 shifts/day $\times$ 8 hours/shift = 384 hours.

*   $U_{mt}$: Number of machines of type $m$ unavailable (under maintenance) in month $t$.
    *   Derived from text:
        *   $t=1$ (Jan): 1 Grinding ($m=1$). $U_{1,1}=1$, others 0.
        *   $t=2$ (Feb): 2 Horizontal Drills ($m=3$). $U_{3,2}=2$, others 0.
        *   $t=3$ (Mar): 1 Boring Machine ($m=4$). $U_{4,3}=1$, others 0.
        *   $t=4$ (Apr): 1 Upright Drill ($m=2$). $U_{2,4}=1$, others 0.
        *   $t=5$ (May): 1 Grinding ($m=1$) and 1 Upright Drill ($m=2$). $U_{1,5}=1, U_{2,5}=1$, others 0.
        *   $t=6$ (Jun): 1 Planer ($m=5$) and 1 Horizontal Drill ($m=3$). $U_{5,6}=1, U_{3,6}=1$, others 0.
    *   All other $U_{mt} = 0$.

*   $Cap_{mt}$: Total available machine-hours for machine type $m$ in month $t$.
    *   $Cap_{mt} = (N_m - U_{mt}) \times H_{total}$
    *   $Cap_{mt} = (N_m - U_{mt}) \times 384$

    *Calculation of $Cap_{mt}$:*
    *   $m=1$ (Grinding, $N=4$):
        *   $t=1: (4-1) \times 384 = 1152$
        *   $t=2: (4-0) \times 384 = 1536$
        *   $t=3: (4-0) \times 384 = 1536$
        *   $t=4: (4-0) \times 384 = 1536$
        *   $t=5: (4-1) \times 384 = 1152$
        *   $t=6: (4-0) \times 384 = 1536$
    *   $m=2$ (Upright, $N=2$):
        *   $t=1: (2-0) \times 384 = 768$
        *   $t=2: (2-0) \times 384 = 768$
        *   $t=3: (2-0) \times 384 = 768$
        *   $t=4: (2-1) \times 384 = 384$
        *   $t=5: (2-1) \times 384 = 384$
        *   $t=6: (2-0) \times 384 = 768$
    *   $m=3$ (Horizontal, $N=3$):
        *   $t=1: (3-0) \times 384 = 1152$
        *   $t=2: (3-2) \times 384 = 384$
        *   $t=3: (3-0) \times 384 = 1152$
        *   $t=4: (3-0) \times 384 = 1152$
        *   $t=5: (3-0) \times 384 = 1152$
        *   $t=6: (3-1) \times 384 = 768$
    *   $m=4$ (Boring, $N=1$):
        *   $t=1: (1-0) \times 384 = 384$
        *   $t=2: (1-0) \times 384 = 384$
        *   $t=3: (1-1) \times 384 = 0$
        *   $t=4: (1-0) \times 384 = 384$
        *   $t=5: (1-0) \times 384 = 384$
        *   $t=6: (1-0) \times 384 = 384$
    *   $m=5$ (Planer, $N=1$):
        *   $t=1: (1-0) \times 384 = 384$
        *   $t=2: (1-0) \times 384 = 384$
        *   $t=3: (1-0) \times 384 = 384$
        *   $t=4: (1-0) \times 384 = 384$
        *   $t=5: (1-0) \times 384 = 384$
        *   $t=6: (1-1) \times 384 = 0$

### 3. Decision Variables

*   $x_{jt}$: Number of units of product $j$ produced in month $t$.
    *   Domain: $x_{jt} \in \mathbb{Z}_{\ge 0}$ (Integer, non-negative) for all $j \in J, t \in T$.
*   $I_{jt}$: Inventory of product $j$ at the **end** of month $t$.
    *   Domain: $I_{jt} \in \mathbb{Z}_{\ge 0}$ (Integer, non-negative) for all $j \in J, t \in T$.
    *   Note: $I_{j0} = 0$ is fixed.

### 4. Objective Function

Maximize total profit over the 6 months, subtracting storage costs.

$$
\text{Maximize } Z = \sum_{t=1}^{6} \left( \sum_{j=1}^{7} p_j x_{jt} - h_j I_{jt} \right)
$$

Substituting values:
$$
Z = \sum_{t=1}^{6} \left( 100x_{1t} + 60x_{2t} + 80x_{3t} + 40x_{4t} + 110x_{5t} + 90x_{6t} + 30x_{7t} - 5I_{1t} - 5I_{2t} - 5I_{3t} - 5I_{4t} - 5I_{5t} - 5I_{6t} - 5I_{7t} \right)
$$

### 5. Operational Constraints

**1. Inventory Balance Constraints:**
For each product $j$ and month $t$, the inventory at the end of the month equals the inventory at the beginning of the month plus production minus sales. Sales are limited by demand. Let $S_{jt}$ be the sales. Since we want to maximize profit and profits are positive, we will always sell as much as possible up to demand. Thus, Sales $= \min(D_{jt}, \text{Available})$. In an LP/MILP formulation, we can model this by linking sales to demand.
Actually, it is simpler to define $x_{jt}$ as production and assume all produced units are either sold or stored. The sales variable $s_{jt}$ is implicitly determined by the inventory balance if we assume we don't want to hold unnecessary inventory that costs money, but we *must* meet the final inventory requirement.
Wait, standard formulation:
$I_{j,t-1} + x_{jt} - s_{jt} = I_{jt}$
$s_{jt} \le D_{jt}$
$s_{jt} \ge 0$
However, since holding inventory costs money ($5/unit/month) and selling makes money ($p_j$), the solver will naturally try to sell as much as possible ($s_{jt} = D_{jt}$) unless production is constrained such that it's cheaper to produce later? No, production cost is not explicit, only profit per unit is given. "Profit per unit" usually means Revenue - Variable Cost. So producing and selling yields $p_j$. Producing and storing yields $p_j$ (eventually) - $h_j$.
If we produce in month $t$ and sell in month $t$, profit is $p_j$.
If we produce in month $t$ and sell in month $t+k$, profit is $p_j - k \cdot h_j$ (roughly, depending on when storage cost is applied).
The objective function above subtracts $5 I_{jt}$. This correctly accounts for storage costs incurred at the end of each month.
To ensure we don't produce more than can ever be sold (which would just add storage cost and never yield profit if not sold, but we *must* have final inventory), we need to ensure sales are maximized.
A safer formulation introduces sales variables $s_{jt}$:
Max $\sum \sum p_j s_{jt} - \sum \sum h_j I_{jt}$
Subject to:
$I_{j,t-1} + x_{jt} - s_{jt} = I_{jt}$
$s_{jt} \le D_{jt}$
$x_{jt} \ge 0$
$I_{jt} \ge 0$

Let's stick to this. Note that if $s_{jt}$ is not explicitly in the objective as revenue, but $x_{jt}$ is, we must ensure $x$ doesn't exceed what can be sold.
Actually, the problem says "Profit per unit... is given". This usually implies the contribution margin of the unit *when sold*.
If I produce $x$ and sell $s$, profit is $p_j s$.
So Objective: $\sum_{t} \sum_{j} p_j s_{jt} - \sum_{t} \sum_{j} 5 I_{jt}$.

**2. Machine Capacity Constraints:**
For each machine type $m$ and month $t$, the total processing time required by production $x_{jt}$ must not exceed the available capacity $Cap_{mt}$.

$$
\sum_{j=1}^{7} a_{mj} x_{jt} \le Cap_{mt}, \quad \forall m \in \{1,\dots,5\}, t \in \{1,\dots,6\}
$$

Explicitly:
*   **Grinding ($m=1$):**
    *   $0.5 x_{1t} + 0.7 x_{2t} + 0.3 x_{5t} + 0.2 x_{6t} + 0.5 x_{7t} \le Cap_{1t}$
*   **Upright Drill ($m=2$):**
    *   $0.1 x_{1t} + 0.2 x_{2t} + 0.3 x_{4t} + 0.6 x_{6t} \le Cap_{2t}$
*   **Horizontal Drill ($m=3$):**
    *   $0.2 x_{1t} + 0.8 x_{3t} + 0.6 x_{7t} \le Cap_{3t}$
*   **Boring Machine ($m=4$):**
    *   $0.05 x_{1t} + 0.03 x_{2t} + 0.07 x_{4t} + 0.1 x_{5t} + 0.08 x_{7t} \le Cap_{4t}$
*   **Planer ($m=5$):**
    *   $0.01 x_{3t} + 0.05 x_{5t} + 0.05 x_{7t} \le Cap_{5t}$

**3. Demand Constraints:**
Sales cannot exceed market demand.
$$
s_{jt} \le D_{jt}, \quad \forall j \in J, t \in T
$$

**4. Inventory Limits:**
Storage limit is 100 units per product at any time.
$$
I_{jt} \le 100, \quad \forall j \in J, t \in \{1,\dots,6\}
$$
Note: "At any time" usually implies the end of the month for this discrete model, or the peak. In a monthly aggregate model, $I_{jt}$ (end of month) is the standard proxy. Given the small limit (100) compared to production volumes, this is a tight constraint.

**5. Final Inventory Requirement:**
End of June ($t=6$) inventory must be 50 for each product.
$$
I_{j6} = 50, \quad \forall j \in J
$$

**6. Initial Inventory:**
$$
I_{j0} = 0, \quad \forall j \in J
$$

**7. Non-negativity and Integrality:**
$$
x_{jt} \in \mathbb{Z}_{\ge 0}, \quad s_{jt} \in \mathbb{Z}_{\ge 0}, \quad I_{jt} \in \mathbb{Z}_{\ge 0}
$$

### Summary of Parameters for Implementation

**Capacities ($Cap_{mt}$):**
*   $Cap_{1,1}=1152, Cap_{1,2}=1536, Cap_{1,3}=1536, Cap_{1,4}=1536, Cap_{1,5}=1152, Cap_{1,6}=1536$
*   $Cap_{2,1}=768, Cap_{2,2}=768, Cap_{2,3}=768, Cap_{2,4}=384, Cap_{2,5}=384, Cap_{2,6}=768$
*   $Cap_{3,1}=1152, Cap_{3,2}=384, Cap_{3,3}=1152, Cap_{3,4}=1152, Cap_{3,5}=1152, Cap_{3,6}=768$
*   $Cap_{4,1}=384, Cap_{4,2}=384, Cap_{4,3}=0, Cap_{4,4}=384, Cap_{4,5}=384, Cap_{4,6}=384$
*   $Cap_{5,1}=384, Cap_{5,2}=384, Cap_{5,3}=384, Cap_{5,4}=384, Cap_{5,5}=384, Cap_{5,6}=0$

**Demands ($D_{jt}$):**
(As listed in Section 2)

**Processing Times ($a_{mj}$):**
(As listed in Section 2)

**Profits ($p_j$):**
(As listed in Section 2)

**Storage Cost ($h_j$):**
5 for all $j$.

**Inventory Bound:**
100 for all $j, t$.

**Final Inventory:**
50 for all $j$ at $t=6$.