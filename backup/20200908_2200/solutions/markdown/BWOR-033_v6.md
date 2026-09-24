To formulate this problem, we must carefully distinguish between what is being produced, what is being delivered, and the resulting inventory states. The problem involves production planning with capacity constraints, specific production restrictions, and costs associated with both holding inventory and failing to meet demand on time (late delivery penalties).

### 1. Index Sets & Parameters

**Index Sets:**
*   $P = \{I, II, III\}$: Set of products.
*   $T = \{1, 2, 3, 4\}$: Set of quarters.

**Parameters:**
*   $d_{p,t}$: Contracted demand (order quantity) for product $p$ in quarter $t$ (from Table 1-10).
    *   $d_{I,1}=1500, d_{I,2}=1000, d_{I,3}=2000, d_{I,4}=1200$
    *   $d_{II,1}=1500, d_{II,2}=1500, d_{II,3}=1200, d_{II,4}=1500$
    *   $d_{III,1}=1000, d_{III,2}=2000, d_{III,3}=1500, d_{III,4}=2500$
*   $H_t = 15,000$: Total available working hours in quarter $t$.
*   $h_p$: Production hours required per unit of product $p$.
    *   $h_I = 2, h_{II} = 4, h_{III} = 3$
*   $C_{hold} = 5$: Inventory holding cost per unit per quarter.
*   $C_{late,p}$: Late delivery penalty per unit per quarter.
    *   $C_{late,I} = 20, C_{late,II} = 20, C_{late,III} = 10$
*   $Inv_{p,0} = 0$: Initial inventory at the beginning of Q1.
*   $Inv_{p,4} = 150$: Required ending inventory at the end of Q4.
*   $M$: A large number (upper bound on production/delivery) to handle binary indicators if needed, though standard flow balance usually suffices if we define variables carefully. Note: Since late delivery is penalized rather than forbidden, demand is *soft*. We can satisfy demand in a later quarter, incurring a penalty for the delay.

**Production Restriction:**
*   Product I cannot be produced in Q2. This implies $x_{I,2} = 0$.

### 2. Decision Variables

We need to track production, delivery, and inventory/shortage states.
A robust way to model "late delivery" with per-quarter penalties is to track the inventory level. If inventory is negative, it represents unmet demand (backlog). However, standard LP formulations often restrict inventory to be non-negative and use separate variables for production and delivery, or allow negative inventory (backlog).

Given the penalty is "per unit per quarter" of lateness, this suggests a **backlog** model is most natural. If a unit is not delivered in the quarter it was due, it accumulates penalty for each subsequent quarter until delivered.
*Let's refine the variable definitions to handle this:*

Let:
*   $x_{p,t} \ge 0$: Units of product $p$ produced in quarter $t$.
*   $y_{p,t} \ge 0$: Units of product $p$ delivered in quarter $t$.
*   $Inv_{p,t} \ge 0$: Inventory of product $p$ at the **end** of quarter $t$.
*   $Back_{p,t} \ge 0$: Backlog (unmet demand) of product $p$ at the **end** of quarter $t$.

*Note on Inventory vs Backlog:*
In many inventory models, $Inv_{p,t} - Back_{p,t} = \text{Net Inventory}$. Only one can be non-zero at a time (or both zero).
The cost structure is:
1.  **Inventory Cost**: Charged on positive inventory ($Inv_{p,t}$). Rate: 5 yuan/unit.
2.  **Late Delivery Penalty**: Charged on backlog ($Back_{p,t}$). Rate: $C_{late,p}$ yuan/unit.
    *   *Interpretation Check*: "If a product is not delivered on time, late delivery penalties are: 20 yuan per unit per quarter". This typically means if a unit due in Q1 is delivered in Q2, it incurs a penalty for the delay. If the penalty is cumulative per quarter of delay, the cost is proportional to the backlog level at the end of the period.

**Alternative Interpretation (Simpler Flow Balance):**
Often in these textbook problems, "late delivery penalty" is treated as a cost for satisfying demand in a later period.
Let's use the standard Inventory Balance Equation:
$Inv_{p,t} - Back_{p,t} = Inv_{p,t-1} - Back_{p,t-1} + x_{p,t} - y_{p,t}$
With the condition that $Inv_{p,t} \cdot Back_{p,t} = 0$.

However, a simpler formulation that avoids the complementarity constraint is to assume we can only hold positive inventory or positive backlog.
Let's define:
*   $x_{p,t}$: Production of $p$ in $t$.
*   $I_{p,t}$: Inventory of $p$ at end of $t$ (must be $\ge 0$).
*   $B_{p,t}$: Backlog of $p$ at end of $t$ (must be $\ge 0$).

**Constraint on Delivery:**
The problem asks to minimize cost. It doesn't explicitly forbid delivering *more* than demand, but "contract order quantities" imply a fixed demand. Usually, you can over-deliver (incurring inventory cost) or under-deliver (incurring backlog penalty).
Actually, the standard interpretation for "minimize cost of late delivery and inventory" with fixed demand $d_{p,t}$ is:
You can produce $x_{p,t}$. You can deliver $y_{p,t}$.
The net change in position is $x_{p,t} - y_{p,t}$.
If net position is positive, it's inventory. If negative, it's backlog.

Let's stick to the variables:
*   $x_{p,t} \in \mathbb{R}_{\ge 0}$: Production quantity.
*   $Inv_{p,t} \in \mathbb{R}_{\ge 0}$: Ending inventory.
*   $Back_{p,t} \in \mathbb{R}_{\ge 0}$: Ending backlog (unmet demand from current or previous periods).

**Balance Equation:**
$Inv_{p,t} - Back_{p,t} = Inv_{p,p-1} - Back_{p,t-1} + x_{p,t} - d_{p,t}$
*Wait*, does $d_{p,t}$ represent the demand that *must* be delivered in period $t$? Yes.
So, if $x_{p,t}$ (production) is less than $d_{p,t}$ (demand) plus previous backlog, we add to the backlog.
The equation:
$Inv_{p,t} - Back_{p,t} = (Inv_{p,t-1} - Back_{p,t-1}) + x_{p,t} - d_{p,t}$

**Boundary Conditions:**
*   Start: $Inv_{p,0} = 0, Back_{p,0} = 0$.
*   End: The problem states "By the end of Q4, there must be an inventory of 150 units for each product."
    *   This implies $Inv_{p,4} = 150$ and $Back_{p,4} = 0$. (You cannot have a backlog at the end if you have a specific inventory requirement, and typically contracts are fully satisfied by the end or the penalty structure handles the timing). Given the phrasing "inventory of 150", it implies a net positive stock.

**Production Constraint:**
$\sum_{p \in P} h_p x_{p,t} \le H_t$ for all $t$.
And $x_{I,2} = 0$.

**Objective Function:**
Minimize Total Cost = (Inventory Holding Costs) + (Late Delivery Penalties)
Cost per quarter $t$:
$\sum_{p \in P} [ C_{hold} \cdot Inv_{p,t} + C_{late,p} \cdot Back_{p,t} ]$

### 3. Objective Function

$$
\text{Minimize } Z = \sum_{t=1}^{4} \sum_{p \in \{I, II, III\}} \left( 5 \cdot Inv_{p,t} + C_{late,p} \cdot Back_{p,t} \right)
$$
Where:
*   $C_{late,I} = 20$
*   $C_{late,II} = 20$
*   $C_{late,III} = 10$

### 4. Operational Constraints

**1. Inventory/Backlog Balance Constraints:**
For each product $p \in \{I, II, III\}$ and quarter $t \in \{1, 2, 3, 4\}$:
$$
Inv_{p,t} - Back_{p,t} = Inv_{p,t-1} - Back_{p,t-1} + x_{p,t} - d_{p,t}
$$
Subject to:
$$
Inv_{p,t} \ge 0, \quad Back_{p,t} \ge 0
$$
*(Note: In a linear programming formulation, the solver will naturally drive one of $Inv$ or $Back$ to zero in the optimal solution because having both positive would allow reducing both by the same amount to reduce cost or satisfy constraints more efficiently, provided the costs are positive. Specifically, if $Inv>0$ and $Back>0$, you could decrease $Inv$ and $Back$ simultaneously, which might violate the balance equation unless you adjust production/delivery, but physically they represent opposite states. Standard LP solvers handle this via the linear structure of the balance equation and non-negativity.)*

**2. Production Capacity Constraints:**
For each quarter $t \in \{1, 2, 3, 4\}$:
$$
2 x_{I,t} + 4 x_{II,t} + 3 x_{III,t} \le 15,000
$$

**3. Production Restriction:**
Product I cannot be produced in Q2:
$$
x_{I,2} = 0
$$

**4. Initial Conditions:**
For all $p \in \{I, II, III\}$:
$$
Inv_{p,0} = 0
$$
$$
Back_{p,0} = 0
$$

**5. Final Conditions:**
For all $p \in \{I, II, III\}$:
$$
Inv_{p,4} = 150
$$
$$
Back_{p,4} = 0
$$
*(Assumption: The requirement "inventory of 150 units" implies no outstanding backlog at the end of the horizon. If backlog were allowed, the inventory level would be net of backlog, but "inventory of 150" is a hard state constraint.)*

**6. Non-negativity:**
$$
x_{p,t} \ge 0 \quad \forall p, t
$$
$$
Inv_{p,t} \ge 0 \quad \forall p, t
$$
$$
Back_{p,t} \ge 0 \quad \forall p, t
$$

### Summary of Model Structure

*   **Variables**: 12 production variables ($x$), 12 inventory variables ($Inv$), 12 backlog variables ($Back$). Total 36 continuous variables.
*   **Objective**: Linear combination of ending inventory and ending backlog levels over 4 quarters.
*   **Constraints**:
    *   4 linear capacity constraints.
    *   1 equality constraint $x_{I,2}=0$.
    *   12 balance equations (one for each product-quarter).
    *   6 boundary equalities ($Inv_{p,4}=150, Back_{p,4}=0$).
    *   Non-negativity constraints.

This is a Linear Programming (LP) problem. Since production quantities and inventories can be fractional in the mathematical relaxation, but "units" are discrete, strictly speaking, this is a Mixed Integer Linear Programming (MILP) problem if $x, Inv, Back$ are required to be integers. However, given the large scale (thousands of units) and the fact that OR problems of this type often accept LP solutions as approximations or assume continuous flow for hours/units unless "integer" is specified, we define them as continuous non-negative variables. *Self-correction based on "Integrality" rule*: The problem involves "units" of product. In strict OR practice for small counts, integers are required. Here counts are in the thousands. Usually, LP relaxation is acceptable, but to be mathematically rigorous for "units", they should be integers. However, without an explicit instruction to use integers, and given the magnitude, standard practice for such cost-minimization flow problems is LP. I will specify them as non-negative real numbers, but note that integer constraints can be added if discrete units are strictly enforced. Given the prompt's instruction "If the problem involves 'units'... where fractional units are physically impossible... use integer variables", I will specify **Integer** variables for $x, Inv, Back$ to be safe and compliant with the strict modeling rules.

**Revised Variable Domains:**
$x_{p,t}, Inv_{p,t}, Back_{p,t} \in \mathbb{Z}_{\ge 0}$

### Final Formulation

**1. Index Sets & Parameters**
*   $P = \{I, II, III\}$
*   $T = \{1, 2, 3, 4\}$
*   $d_{p,t}$: Demand matrix from Table 1-10.
*   $H = 15000$
*   $h = [2, 4, 3]$ for $I, II, III$.
*   $C_{hold} = 5$
*   $C_{late} = [20, 20, 10]$ for $I, II, III$.

**2. Decision Variables**
*   $x_{p,t} \in \mathbb{Z}_{\ge 0}$: Production of product $p$ in quarter $t$.
*   $Inv_{p,t} \in \mathbb{Z}_{\ge 0}$: Ending inventory of product $p$ in quarter $t$.
*   $Back_{p,t} \in \mathbb{Z}_{\ge 0}$: Ending backlog of product $p$ in quarter $t$.

**3. Objective Function**
$$
\text{Minimize } Z = \sum_{t=1}^{4} \left( 5(Inv_{I,t} + Inv_{II,t} + Inv_{III,t}) + 20(Back_{I,t} + Back_{II,t}) + 10 Back_{III,t} \right)
$$

**4. Operational Constraints**
1.  **Balance**:
    $$Inv_{p,t} - Back_{p,t} = Inv_{p,t-1} - Back_{p,t-1} + x_{p,t} - d_{p,t} \quad \forall p \in P, t \in T$$
2.  **Capacity**:
    $$2x_{I,t} + 4x_{II,t} + 3x_{III,t} \le 15000 \quad \forall t \in T$$
3.  **Restriction**:
    $$x_{I,2} = 0$$
4.  **Initial State**:
    $$Inv_{p,0} = 0, \quad Back_{p,0} = 0 \quad \forall p \in P$$
5.  **Final State**:
    $$Inv_{p,4} = 150, \quad Back_{p,4} = 0 \quad \forall p \in P$$
6.  **Non-negativity/Integrality**:
    $$x_{p,t}, Inv_{p,t}, Back_{p,t} \ge 0 \quad \text{and integer}$$