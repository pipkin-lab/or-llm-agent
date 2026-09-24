To formulate the mathematical model for this production planning problem, we must carefully account for the monthly variability in machine capacity due to maintenance, the inventory dynamics (production, sales, storage costs), and the specific boundary conditions (initial and final inventory).

### 1. Model Type Declaration
**Model Type:** Linear Programming (LP)
*   **Reasoning:** All decision variables (production quantities) are continuous (or can be treated as integer if strict integrality is required, but typically LP is standard for large-scale production planning unless specified; given the large numbers, LP is appropriate. However, since units are discrete, an **MILP** is technically more rigorous. I will formulate it as an **MILP** to ensure physical realizability, though the LP relaxation is often near-integer here).
*   **Note:** The problem asks to "plan production," implying discrete units. I will define variables as integers.

### 2. Index Sets & Parameters

**Sets:**
*   $M = \{1, 2, 3, 4, 5, 6\}$: Set of months (Jan, Feb, Mar, Apr, May, Jun).
*   $P = \{1, 2, 3, 4, 5, 6, 7\}$: Set of products (I, II, III, IV, V, VI, VII).
*   $E = \{1, 2, 3, 4, 5\}$: Set of machine types.
    *   $E_1$: Grinding Machines
    *   $E_2$: Upright Drills
    *   $E_3$: Horizontal Drills
    *   $E_4$: Boring Machine
    *   $E_5$: Planer

**Parameters:**

*   **Total Monthly Machine Hours ($H_{t,e}$):**
    The factory operates 24 days/month $\times$ 2 shifts/day $\times$ 8 hours/shift = **384 hours** per machine per month.
    Let $N_e$ be the total number of machines of type $e$.
    *   $N_1 = 4$ (Grinding)
    *   $N_2 = 2$ (Upright Drill)
    *   $N_3 = 3$ (Horizontal Drill)
    *   $N_4 = 1$ (Boring)
    *   $N_5 = 1$ (Planer)
    
    Let $M_{t,e}$ be the number of machines of type $e$ undergoing maintenance in month $t$.
    The available number of machines is $N_e - M_{t,e}$.
    The total available hours for machine type $e$ in month $t$ is:
    $$ H_{t,e} = (N_e - M_{t,e}) \times 384 $$

    **Maintenance Schedule ($M_{t,e}$):**
    *   **Jan ($t=1$):** $M_{1,1}=1$ (1 Grinding), others 0.
    *   **Feb ($t=2$):** $M_{2,3}=2$ (2 Horiz. Drills), others 0.
    *   **Mar ($t=3$):** $M_{3,4}=1$ (1 Boring), others 0.
    *   **Apr ($t=4$):** $M_{4,2}=1$ (1 Upright), others 0.
    *   **May ($t=5$):** $M_{5,1}=1$ (1 Grinding), $M_{5,2}=1$ (1 Upright), others 0.
    *   **Jun ($t=6$):** $M_{6,5}=1$ (1 Planer), $M_{6,3}=1$ (1 Horiz. Drill), others 0.

    **Calculated Available Hours ($H_{t,e}$):**
    *   **Grinding ($E_1$, Total Cap 4 $\times$ 384 = 1536 hrs):**
        *   Jan: $(4-1)\times 384 = 1152$
        *   Feb: $4\times 384 = 1536$
        *   Mar: $4\times 384 = 1536$
        *   Apr: $4\times 384 = 1536$
        *   May: $(4-1)\times 384 = 1152$
        *   Jun: $4\times 384 = 1536$
    *   **Upright Drill ($E_2$, Total Cap 2 $\times$ 384 = 768 hrs):**
        *   Jan: $2\times 384 = 768$
        *   Feb: $2\times 384 = 768$
        *   Mar: $2\times 384 = 768$
        *   Apr: $(2-1)\times 384 = 384$
        *   May: $(2-1)\times 384 = 384$
        *   Jun: $2\times 384 = 768$
    *   **Horizontal Drill ($E_3$, Total Cap 3 $\times$ 384 = 1152 hrs):**
        *   Jan: $3\times 384 = 1152$
        *   Feb: $(3-2)\times 384 = 384$
        *   Mar: $3\times 384 = 1152$
        *   Apr: $3\times 384 = 1152$
        *   May: $3\times 384 = 1152$
        *   Jun: $(3-1)\times 384 = 768$
    *   **Boring Machine ($E_4$, Total Cap 1 $\times$ 384 = 384 hrs):**
        *   Jan: $1\times 384 = 384$
        *   Feb: $1\times 384 = 384$
        *   Mar: $(1-1)\times 384 = 0$
        *   Apr: $1\times 384 = 384$
        *   May: $1\times 384 = 384$
        *   Jun: $1\times 384 = 384$
    *   **Planer ($E_5$, Total Cap 1 $\times$ 384 = 384 hrs):**
        *   Jan: $1\times 384 = 384$
        *   Feb: $1\times 384 = 384$
        *   Mar: $1\times 384 = 384$
        *   Apr: $1\times 384 = 384$
        *   May: $1\times 384 = 384$
        *   Jun: $(1-1)\times 384 = 0$

*   **Machine Hours per Unit ($a_{e,p}$):**
    From Table C-3. "--" denotes 0.
    *   $a_{1,p}$ (Grinding): $[0.5, 0.7, 0, 0, 0.3, 0.2, 0.5]$
    *   $a_{2,p}$ (Upright): $[0.1, 0.2, 0, 0.3, 0, 0.6, 0]$
    *   $a_{3,p}$ (Horiz): $[0.2, 0, 0.8, 0, 0, 0, 0.6]$
    *   $a_{4,p}$ (Boring): $[0.05, 0.03, 0, 0.07, 0.1, 0, 0.08]$
    *   $a_{5,p}$ (Planer): $[0, 0, 0.01, 0, 0.05, 0, 0.05]$

*   **Unit Profit ($c_p$):**
    From Table C-3.
    $c = [100, 60, 80, 40, 110, 90, 30]$

*   **Market Demand ($D_{t,p}$):**
    From Table C-4.
    *   Jan ($t=1$): $[500, 1000, 300, 300, 800, 200, 100]$
    *   Feb ($t=2$): $[600, 500, 200, 0, 400, 300, 150]$
    *   Mar ($t=3$): $[300, 600, 0, 0, 500, 400, 100]$
    *   Apr ($t=4$): $[200, 300, 400, 500, 200, 0, 100]$
    *   May ($t=5$): $[0, 100, 500, 100, 1000, 300, 0]$
    *   Jun ($t=6$): $[500, 500, 100, 300, 1100, 500, 60]$

*   **Storage Cost ($s_p$):**
    $s_p = 5$ yuan/unit/month for all $p \in P$.

*   **Storage Capacity ($K_p$):**
    $K_p = 100$ units for all $p \in P$.

*   **Initial Inventory ($I_{0,p}$):**
    $I_{0,p} = 0$ for all $p \in P$.

*   **Final Inventory Requirement ($I_{6,p}$):**
    $I_{6,p} = 50$ for all $p \in P$.

### 3. Decision Variables

Let $x_{t,p}$ be the number of units of product $p$ produced in month $t$.
**Domain:** $x_{t,p} \in \mathbb{Z}_{\ge 0}$ (Non-negative integers)

Let $I_{t,p}$ be the inventory of product $p$ at the **end** of month $t$.
**Domain:** $I_{t,p} \in \mathbb{Z}_{\ge 0}$ (Non-negative integers)

*(Note: While we could eliminate $I_{t,p}$ by substituting the balance equation, keeping them as variables makes the storage cost and capacity constraints explicit and easier to manage.)*

### 4. Objective Function

Maximize Total Profit.
Total Profit = (Total Revenue from Sales) - (Total Storage Costs).
*Wait*: The profit $c_p$ is given as "profit per unit" in the table. Usually, "profit" implies net of production cost. The problem asks to maximize "total profit".
Standard formulation:
$$ \text{Maximize } Z = \sum_{t=1}^{6} \sum_{p=1}^{7} c_p \cdot S_{t,p} - \sum_{t=1}^{6} \sum_{p=1}^{7} s_p \cdot I_{t,p} $$
Where $S_{t,p}$ is the amount sold in month $t$.
However, it is often cleaner to express this in terms of production and inventory.
Revenue is generated when goods are sold.
$S_{t,p} = I_{t-1,p} + x_{t,p} - I_{t,p}$.
Substituting this into the objective:
$$ Z = \sum_{t=1}^{6} \sum_{p=1}^{7} c_p (I_{t-1,p} + x_{t,p} - I_{t,p}) - \sum_{t=1}^{6} \sum_{p=1}^{7} 5 I_{t,p} $$
This can be rearranged, but it's safer to stick to the definition: Profit is earned on sold units.
Alternatively, if "profit per unit" is the contribution margin, we maximize:
$$ \text{Maximize } \sum_{t=1}^{6} \sum_{p=1}^{7} c_p \cdot S_{t,p} - \sum_{t=1}^{6} \sum_{p=1}^{7} 5 \cdot I_{t,p} $$

Let's verify the "Profit" definition. "Profit per unit" usually means $(Price - Variable Cost)$. So maximizing sum of (Profit $\times$ Sold Units) - Storage Costs is correct.

### 5. Operational Constraints

**1. Machine Capacity Constraints:**
For each month $t \in M$ and each machine type $e \in E$:
$$ \sum_{p=1}^{7} a_{e,p} \cdot x_{t,p} \le H_{t,e} $$

**2. Inventory Balance Constraints:**
For each month $t \in M$ and each product $p \in P$:
$$ I_{t,p} = I_{t-1,p} + x_{t,p} - S_{t,p} $$
Since $S_{t,p}$ is not a direct decision variable but derived from sales, and sales are limited by demand, we can substitute $S_{t,p}$.
However, it is more direct to constrain sales. Let's introduce $S_{t,p}$ as an auxiliary variable or simply enforce the relationship:
$$ S_{t,p} = I_{t-1,p} + x_{t,p} - I_{t,p} $$
And we know $0 \le S_{t,p} \le D_{t,p}$.
So:
$$ 0 \le I_{t-1,p} + x_{t,p} - I_{t,p} \le D_{t,p} $$
This splits into two inequalities:
(a) **Non-negative Sales:** $I_{t,p} \le I_{t-1,p} + x_{t,p}$ (Inventory cannot exceed available stock)
(b) **Demand Limit:** $I_{t-1,p} + x_{t,p} - I_{t,p} \le D_{t,p} \implies I_{t,p} \ge I_{t-1,p} + x_{t,p} - D_{t,p}$

**3. Storage Capacity Constraints:**
For each month $t \in M$ and each product $p \in P$:
$$ I_{t,p} \le 100 $$

**4. Initial and Final Inventory Conditions:**
*   **Initial:** $I_{0,p} = 0$ for all $p$.
*   **Final:** $I_{6,p} = 50$ for all $p$.

**5. Non-negativity and Integrality:**
$$ x_{t,p} \ge 0, \quad I_{t,p} \ge 0 $$
$$ x_{t,p}, I_{t,p} \in \mathbb{Z} $$

---

### Final Formal Model

**Model Type:** MILP (Mixed Integer Linear Programming)

**Sets:**
*   $T = \{1, \dots, 6\}$ (Months)
*   $P = \{1, \dots, 7\}$ (Products)
*   $E = \{1, \dots, 5\}$ (Machine Types)

**Parameters:**
*   $H_{t,e}$: Available machine hours for type $e$ in month $t$ (calculated above).
*   $a_{e,p}$: Machine hours required on type $e$ for product $p$ (Table C-3).
*   $c_p$: Unit profit for product $p$ (Table C-3).
*   $D_{t,p}$: Max demand for product $p$ in month $t$ (Table C-4).
*   $s_p = 5$: Storage cost per unit per month.
*   $K_p = 100$: Max inventory level.
*   $I_{0,p} = 0$: Initial inventory.
*   $I_{6,p} = 50$: Required final inventory.

**Variables:**
*   $x_{t,p} \in \mathbb{Z}_{\ge 0}$: Production quantity of product $p$ in month $t$.
*   $I_{t,p} \in \mathbb{Z}_{\ge 0}$: Ending inventory of product $p$ in month $t$.
*   $S_{t,p} \in \mathbb{Z}_{\ge 0}$: Sales quantity of product $p$ in month $t$. (Auxiliary variable for clarity).

**Objective Function:**
$$ \text{Maximize } Z = \sum_{t=1}^{6} \sum_{p=1}^{7} c_p S_{t,p} - \sum_{t=1}^{6} \sum_{p=1}^{7} 5 I_{t,p} $$

**Constraints:**

1.  **Machine Capacity:**
    $$ \sum_{p=1}^{7} a_{e,p} x_{t,p} \le H_{t,e} \quad \forall t \in T, e \in E $$

2.  **Inventory Balance:**
    $$ I_{t,p} = I_{t-1,p} + x_{t,p} - S_{t,p} \quad \forall t \in T, p \in P $$
    *(Note: $I_{0,p} = 0$)*

3.  **Demand Satisfaction:**
    $$ S_{t,p} \le D_{t,p} \quad \forall t \in T, p \in P $$

4.  **Storage Capacity:**
    $$ I_{t,p} \le 100 \quad \forall t \in T, p \in P $$

5.  **Final Inventory Requirement:**
    $$ I_{6,p} = 50 \quad \forall p \in P $$

6.  **Non-negativity:**
    $$ x_{t,p} \ge 0, \quad I_{t,p} \ge 0, \quad S_{t,p} \ge 0 \quad \forall t \in T, p \in P $$

7.  **Integrality:**
    $$ x_{t,p}, I_{t,p}, S_{t,p} \in \mathbb{Z} \quad \forall t \in T, p \in P $$

**Parameter Values for Implementation:**

*   **$H_{t,e}$ Matrix (Rows: t=1..6, Cols: e=1..5):**
    *   t=1: [1152, 768, 1152, 384, 384]
    *   t=2: [1536, 768, 384, 384, 384]
    *   t=3: [1536, 768, 1152, 0, 384]
    *   t=4: [1536, 384, 1152, 384, 384]
    *   t=5: [1152, 384, 1152, 384, 384]
    *   t=6: [1536, 768, 768, 384, 0]

*   **$a_{e,p}$ Matrix (Rows: e=1..5, Cols: p=1..7):**
    *   e=1: [0.5, 0.7, 0, 0, 0.3, 0.2, 0.5]
    *   e=2: [0.1, 0.2, 0, 0.3, 0, 0.6, 0]
    *   e=3: [0.2, 0, 0.8, 0, 0, 0, 0.6]
    *   e=4: [0.05, 0.03, 0, 0.07, 0.1, 0, 0.08]
    *   e=5: [0, 0, 0.01, 0, 0.05, 0, 0.05]

*   **$c_p$ Vector (p=1..7):**
    *   [100, 60, 80, 40, 110, 90, 30]

*   **$D_{t,p}$ Matrix (Rows: t=1..6, Cols: p=1..7):**
    *   t=1: [500, 1000, 300, 300, 800, 200, 100]
    *   t=2: [600, 500, 200, 0, 400, 300, 150]
    *   t=3: [300, 600, 0, 0, 500, 400, 100]
    *   t=4: [200, 300, 400, 500, 200, 0, 100]
    *   t=5: [0, 100, 500, 100, 1000, 300, 0]
    *   t=6: [500, 500, 100, 300, 1100, 500, 60]