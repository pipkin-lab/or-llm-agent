**Model Type:** MILP (Mixed Integer Linear Programming)

*Note: Although the production quantities can theoretically be fractional in an LP, physical units of products are discrete. Therefore, we define variables as integers to ensure integer production and inventory levels.*

### Index Sets & Parameters

**Index Sets:**
*   $P = \{1, 2, 3\}$: Set of products (Product I, II, III).
*   $T = \{1, 2, 3, 4\}$: Set of quarters (Q1, Q2, Q3, Q4).
*   $P_t$: The set of products that can be produced in quarter $t$.
    *   $P_1 = \{1, 2, 3\}$
    *   $P_2 = \{2, 3\}$ (Product I cannot be produced in Q2)
    *   $P_3 = \{1, 2, 3\}$
    *   $P_4 = \{1, 2, 3\}$

**Parameters:**

*   $D_{p,t}$: Demand for product $p$ in quarter $t$ (units).
    *   Product I: $D_{1,1}=1500, D_{1,2}=1000, D_{1,3}=2000, D_{1,4}=1200$
    *   Product II: $D_{2,1}=1500, D_{2,2}=1500, D_{2,3}=1200, D_{2,4}=1500$
    *   Product III: $D_{3,1}=1000, D_{3,2}=2000, D_{3,3}=1500, D_{3,4}=2500$
*   $H$: Working hours available per quarter = 15,000 hours.
*   $h_p$: Production time per unit for product $p$ (hours/unit).
    *   $h_1 = 2$
    *   $h_2 = 4$
    *   $h_3 = 3$
*   $I_{p,0}$: Initial inventory for product $p$ at start of Q1 = 0 for all $p \in P$.
*   $I_{p,4}^{end}$: Required ending inventory for product $p$ at end of Q4 = 150 for all $p \in P$.
*   $c_{p}^{inv}$: Inventory holding cost per unit per quarter (yuan/unit/quarter).
    *   $c_{1}^{inv} = 5$
    *   $c_{2}^{inv} = 5$
    *   $c_{3}^{inv} = 5$
*   $c_{p}^{late}$: Late delivery penalty per unit per quarter (yuan/unit/quarter).
    *   $c_{1}^{late} = 20$
    *   $c_{2}^{late} = 20$
    *   $c_{3}^{late} = 10$

### Decision Variables

Let $x_{p,t}$ be the quantity of product $p$ produced in quarter $t$.
*   $x_{p,t} \in \mathbb{Z}_{\ge 0}$ for all $p \in P, t \in T$.
*   Constraint: $x_{1,2} = 0$ (Product I cannot be produced in Q2).

Let $I_{p,t}$ be the inventory of product $p$ at the **end** of quarter $t$.
*   $I_{p,t} \in \mathbb{Z}_{\ge 0}$ for all $p \in P, t \in T$.

Let $L_{p,t}$ be the quantity of product $p$ delivered **late** in quarter $t$ (i.e., demand for quarter $t$ that is satisfied by inventory carried over from previous quarters or produced later but attributed to the penalty of being late relative to the original quarter).
*   *Clarification on Late Penalty Logic*: The problem states "late delivery penalties are... per unit per quarter". This typically implies that if demand $D_{p,t}$ is not met in quarter $t$, the unmet portion is satisfied in a later quarter, and the penalty is incurred for each quarter of delay. Alternatively, and more commonly in simple inventory models with backlogging, $L_{p,t}$ represents the backlog at the end of period $t$. However, the cost is "per unit per quarter". Let's define $B_{p,t}$ as the backlog (unmet demand) of product $p$ at the end of quarter $t$.
    *   If demand is not met in quarter $t$, the unmet amount is added to the backlog.
    *   The penalty is incurred for the units in the backlog for each quarter they remain unmet.
    *   Let $B_{p,t}$ be the backlog of product $p$ at the end of quarter $t$. $B_{p,t} \in \mathbb{Z}_{\ge 0}$.
    *   The cost associated with backlogs is $\sum_{p \in P} \sum_{t=1}^{4} c_p^{late} B_{p,t}$.
    *   Note: The problem asks to minimize "total cost of late delivery penalties and inventory holding costs".
    *   Inventory holding cost is incurred on $I_{p,t}$ (on-hand inventory).
    *   Late penalty is incurred on $B_{p,t}$ (backlogged inventory).

Revised Variables:
*   $x_{p,t} \in \mathbb{Z}_{\ge 0}$: Production of product $p$ in quarter $t$.
*   $I_{p,t} \in \mathbb{Z}_{\ge 0}$: On-hand inventory of product $p$ at end of quarter $t$.
*   $B_{p,t} \in \mathbb{Z}_{\ge 0}$: Backlog (unmet demand) of product $p$ at end of quarter $t$.

### Objective Function

Minimize the total cost $Z$:

$$
\text{Minimize } Z = \sum_{p \in P} \sum_{t=1}^{4} \left( c_p^{inv} I_{p,t} + c_p^{late} B_{p,t} \right)
$$

### Operational Constraints

**1. Inventory Balance Constraints**
For each product $p$ and quarter $t$, the flow of units must balance.
Units available = Beginning Inventory + Production.
Units required = Demand + Ending Inventory - Ending Backlog.
*Note: Beginning Inventory for quarter $t$ is $I_{p,t-1}$. Beginning Backlog for quarter $t$ is $B_{p,t-1}$. Demand $D_{p,t}$ is satisfied first from current production and inventory, and any shortfall adds to the backlog. Any excess reduces the backlog.*

A standard way to model this with separate inventory and backlog variables is:
$$ I_{p,t} - B_{p,t} = I_{p,t-1} - B_{p,t-1} + x_{p,t} - D_{p,t} $$
for all $p \in P, t \in T$.

With initial conditions:
$$ I_{p,0} = 0, \quad B_{p,0} = 0 $$

Ending conditions (End of Q4):
The problem states "By the end of Q4, there must be an inventory of 150 units for each product."
This implies the on-hand inventory $I_{p,4}$ must be 150.
Does it imply the backlog $B_{p,4}$ must be 0?
Usually, "inventory of 150 units" refers to physical stock on hand. If there is a backlog, the net position would be $I_{p,4} - B_{p,4}$. However, late delivery penalties are paid per quarter. If we end Q4 with a backlog, we have incurred the penalty for Q4. Does the backlog persist beyond Q4? The problem only covers the coming year (4 quarters). It is standard in such finite-horizon problems to assume all demand must be met by the end of the horizon unless stated otherwise, or that the "inventory" requirement is the final state.
Given the phrasing "late delivery penalties... per unit per quarter", it implies the cost is time-dependent. If we leave a backlog at the end of Q4, we have paid the penalty for Q4. If the problem implies the contract is fulfilled by end of Q4, we should enforce $B_{p,4} = 0$. If not, the backlog could remain. However, "inventory of 150 units" usually means net inventory or gross inventory?
Let's look at the wording: "By the end of Q4, there must be an inventory of 150 units for each product."
In OR problems, "inventory" usually refers to $I$ (on-hand). If there is a backlog $B$, the net inventory is $I-B$.
If the requirement is strictly on-hand inventory $I_{p,4} = 150$, we must decide if backlogs are allowed to remain. Given the penalty structure, it is highly likely that all demand must be satisfied by the end of the period, i.e., $B_{p,4} = 0$. If backlogs were allowed to remain, the "late delivery" would be ongoing, which is not typical for a finite annual planning problem unless specified. I will assume **all demand must be met by the end of Q4**, so $B_{p,4} = 0$.

So, boundary conditions:
$$ I_{p,0} = 0, \quad B_{p,0} = 0 \quad \forall p \in P $$
$$ I_{p,4} = 150, \quad B_{p,4} = 0 \quad \forall p \in P $$

**2. Production Capacity Constraints**
Total production time in each quarter cannot exceed available hours.
$$ \sum_{p \in P_t} h_p x_{p,t} \le H, \quad \forall t \in T $$
Where $H = 15,000$.

Specifically:
*   Q1: $2x_{1,1} + 4x_{2,1} + 3x_{3,1} \le 15,000$
*   Q2: $4x_{2,2} + 3x_{3,2} \le 15,000$ (Note: $x_{1,2}=0$)
*   Q3: $2x_{1,3} + 4x_{2,3} + 3x_{3,3} \le 15,000$
*   Q4: $2x_{1,4} + 4x_{2,4} + 3x_{3,4} \le 15,000$

**3. Production Restriction**
$$ x_{1,2} = 0 $$

**4. Non-negativity and Integrality**
$$ x_{p,t} \in \mathbb{Z}_{\ge 0} $$
$$ I_{p,t} \in \mathbb{Z}_{\ge 0} $$
$$ B_{p,t} \in \mathbb{Z}_{\ge 0} $$

### Summary of the Model

**Sets:**
$P = \{1, 2, 3\}$
$T = \{1, 2, 3, 4\}$

**Parameters:**
$D = \begin{pmatrix} 1500 & 1000 & 2000 & 1200 \\ 1500 & 1500 & 1200 & 1500 \\ 1000 & 2000 & 1500 & 2500 \end{pmatrix}$
$h = (2, 4, 3)$
$H = 15000$
$c^{inv} = (5, 5, 5)$
$c^{late} = (20, 20, 10)$
$I_{p,0} = 0, B_{p,0} = 0$
$I_{p,4} = 150, B_{p,4} = 0$

**Variables:**
$x_{p,t} \in \mathbb{Z}_{\ge 0}$
$I_{p,t} \in \mathbb{Z}_{\ge 0}$
$B_{p,t} \in \mathbb{Z}_{\ge 0}$

**Objective:**
$\min \sum_{p=1}^3 \sum_{t=1}^4 (5 I_{p,t} + c_p^{late} B_{p,t})$
where $c_1^{late}=20, c_2^{late}=20, c_3^{late}=10$.

**Constraints:**
1.  $I_{p,t} - B_{p,t} = I_{p,t-1} - B_{p,t-1} + x_{p,t} - D_{p,t}, \quad \forall p \in P, t \in T$
2.  $\sum_{p \in P} h_p x_{p,t} \le 15000, \quad \forall t \in T$
    *   (Implicitly handles $x_{1,2}=0$ if we set $x_{1,2}=0$ explicitly or define domain)
3.  $x_{1,2} = 0$
4.  $I_{p,4} = 150, \quad \forall p \in P$
5.  $B_{p,4} = 0, \quad \forall p \in P$
6.  $x_{p,t}, I_{p,t}, B_{p,t} \ge 0$ and integer.