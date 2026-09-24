### 1. Index Sets & Parameters

**Index Sets:**
*   $P = \{1, 2, 3\}$: Set of products (I, II, III).
*   $T = \{1, 2, 3, 4\}$: Set of quarters.

**Parameters:**
*   $D_{p,t}$: Contracted demand (order quantity) for product $p$ in quarter $t$ (units).
    *   From Table 1-10:
        *   $D_{1,1}=1500, D_{1,2}=1000, D_{1,3}=2000, D_{1,4}=1200$
        *   $D_{2,1}=1500, D_{2,2}=1500, D_{2,3}=1200, D_{2,4}=1500$
        *   $D_{3,1}=1000, D_{3,2}=2000, D_{3,3}=1500, D_{3,4}=2500$
*   $H_p$: Inventory holding cost per unit per quarter for product $p$.
    *   $H_1 = 5, H_2 = 5, H_3 = 5$ (yuan/unit/quarter).
*   $L_p$: Late delivery penalty cost per unit per quarter for product $p$.
    *   $L_1 = 20, L_2 = 20, L_3 = 10$ (yuan/unit/quarter).
*   $a_p$: Production time required per unit of product $p$ (hours/unit).
    *   $a_1 = 2, a_2 = 4, a_3 = 3$.
*   $Cap_t$: Available working hours in quarter $t$.
    *   $Cap_t = 15000$ for all $t \in T$.
*   $E_{p,t}$: Binary parameter indicating if product $p$ can be produced in quarter $t$.
    *   $E_{1,2} = 0$ (Product I cannot be produced in Q2).
    *   $E_{p,t} = 1$ for all other $p, t$.
*   $I_{p,0}$: Initial inventory for product $p$ at start of Q1.
    *   $I_{p,0} = 0$ for all $p \in P$.
*   $I_{p,T}$: Required ending inventory for product $p$ at end of Q4.
    *   $I_{p,4} = 150$ for all $p \in P$.

### 2. Decision Variables

To accurately model late deliveries and inventory separately, we use the standard "backlog" formulation where inventory and backlog variables are non-negative and mutually exclusive (or handled via net inventory if allowed, but separate variables are safer for cost calculation).

*   $x_{p,t}$: Number of units of product $p$ produced in quarter $t$.
    *   Domain: $x_{p,t} \in \mathbb{Z}^+$ (Non-negative Integer) for all $p \in P, t \in T$.
    *   Constraint: If $E_{p,t} = 0$, then $x_{p,t} = 0$.

*   $Inv_{p,t}$: Ending inventory level of product $p$ at the end of quarter $t$.
    *   Domain: $Inv_{p,t} \in \mathbb{Z}^+$ (Non-negative Integer) for all $p \in P, t \in T$.

*   $Back_{p,t}$: Backlog (unmet demand carried over) level of product $p$ at the end of quarter $t$.
    *   Domain: $Back_{p,t} \in \mathbb{Z}^+$ (Non-negative Integer) for all $p \in P, t \in T$.

*   *Note on Mutually Exclusive State:* In standard linear inventory models, $Inv_{p,t}$ and $Back_{p,t}$ cannot both be positive. This is naturally enforced if we use the balance equation $Inv_{p,t} - Back_{p,t} = Inv_{p,t-1} - Back_{p,t-1} + x_{p,t} - D_{p,t}$ along with non-negativity, provided we interpret the state correctly. However, a more robust integer formulation often uses a single net inventory variable $S_{p,t}$ which can be positive (stock) or negative (backlog).
    *   Let's use **Net Inventory** $S_{p,t}$ to simplify the balance equation, then split costs based on the sign. However, linear programming/MILP cannot directly use $max(0, S)$ or $min(0, S)$ in the objective without auxiliary variables.
    *   Therefore, we stick to the split variables $Inv_{p,t}$ and $Back_{p,t}$ and enforce the balance. To ensure $Inv_{p,t} \cdot Back_{p,t} = 0$, we rely on the cost minimization (since both costs are positive, the solver will drive one to zero).
    *   Balance Equation: $Inv_{p,t} - Back_{p,t} = Inv_{p,t-1} - Back_{p,t-1} + x_{p,t} - D_{p,t}$.

### 3. Objective Function

Minimize the total cost of inventory holding and late delivery penalties over all quarters and products.

$$
\text{Minimize } Z = \sum_{p \in P} \sum_{t=1}^{4} \left( H_p \cdot Inv_{p,t} + L_p \cdot Back_{p,t} \right)
$$

**Clarification on Cost Timing:**
*   Inventory cost is incurred on the *ending* inventory of each quarter ($Inv_{p,t}$).
*   Late delivery penalty is incurred on the *ending* backlog of each quarter ($Back_{p,t}$). This represents the units that are still undelivered at the end of quarter $t$.
*   The problem states "late delivery penalties are... per unit per quarter". This implies that for every quarter a unit is delayed, the penalty accumulates. The variable $Back_{p,t}$ represents the cumulative number of units still not delivered by the end of quarter $t$. If a unit is delivered in Q3 for a Q1 order, it contributes to $Back_{p,1}$ and $Back_{p,2}$, incurring the penalty twice. This matches the "per unit per quarter" description.

### 4. Operational Constraints

**1. Capacity Constraints (Production Hours)**
For each quarter $t$, the total production time must not exceed available hours.
$$
\sum_{p \in P} a_p \cdot x_{p,t} \leq Cap_t \quad \forall t \in T
$$
Specifically:
*   $2 x_{1,t} + 4 x_{2,t} + 3 x_{3,t} \leq 15000$ for $t=1, 3, 4$
*   $0 x_{1,t} + 4 x_{2,t} + 3 x_{3,t} \leq 15000$ for $t=2$ (since $x_{1,2}=0$)

**2. Production Feasibility Constraints**
Product I cannot be produced in Q2.
$$
x_{1,2} = 0
$$
For all other $p, t$:
$$
x_{p,t} \geq 0
$$

**3. Inventory/Backlog Balance Constraints**
The net inventory state evolves based on previous state, production, and demand.
For each product $p$ and quarter $t$:
$$
Inv_{p,t} - Back_{p,t} = Inv_{p,t-1} - Back_{p,t-1} + x_{p,t} - D_{p,t}
$$
With initial conditions:
$$
Inv_{p,0} = 0, \quad Back_{p,0} = 0 \quad \forall p \in P
$$
And terminal conditions (End of Q4 must have 150 units inventory, implying no backlog):
$$
Inv_{p,4} = 150 \quad \forall p \in P
$$
$$
Back_{p,4} = 0 \quad \forall p \in P
$$
*(Note: The problem states "By the end of Q4, there must be an inventory of 150 units". This implies the final state is purely positive inventory.)*

**4. Non-negativity and Integrality**
$$
x_{p,t} \in \mathbb{Z}^+ \quad \forall p \in P, t \in T
$$
$$
Inv_{p,t} \in \mathbb{Z}^+ \quad \forall p \in P, t \in T
$$
$$
Back_{p,t} \in \mathbb{Z}^+ \quad \forall p \in P, t \in T
$$

### Verification & Notes

1.  **Units:** All quantities are in units (integer). Costs are in Yuan. Hours are in hours.
2.  **Objective Direction:** Minimization of total penalty + holding costs.
3.  **Data Completeness:**
    *   Demands: Provided in Table 1-10.
    *   Costs: Holding (5), Penalties (20, 20, 10).
    *   Times: 2, 4, 3 hours.
    *   Capacity: 15,000 hours/quarter.
    *   Initial/Final Inventory: 0 start, 150 end.
    *   Constraint: No Prod I in Q2.
    *   All parameters are explicitly defined.
4.  **Integrality:** Since production units are discrete (ships, machines, etc., or simply "units" of product where 1.5 units is not standard for this type of OR problem unless specified as continuous flow), and the scale is moderate (thousands), integer variables are appropriate. However, given the large numbers (15,000 capacity, ~1000-2000 demand), LP relaxation might yield integer solutions naturally, but MILP is the rigorous formulation.
5.  **Backlog Logic:** The balance equation $Inv_t - Back_t = Inv_{t-1} - Back_{t-1} + x_t - D_t$ correctly tracks the net position. Since $H_p > 0$ and $L_p > 0$, the optimal solution will satisfy $Inv_{p,t} \cdot Back_{p,t} = 0$. If the net position is positive, $Back=0, Inv>0$. If negative, $Inv=0, Back>0$.

**Final Model Structure Summary:**

*   **Variables:** $x_{p,t}, Inv_{p,t}, Back_{p,t}$ (Integers $\ge 0$)
*   **Objective:** $\min \sum_{p} \sum_{t} (5 \cdot Inv_{p,t} + L_p \cdot Back_{p,t})$ where $L=[20, 20, 10]$
*   **Constraints:**
    1.  $\sum_{p} a_p x_{p,t} \le 15000$ (for $t=1,3,4$; $x_{1,2}=0$)
    2.  $Inv_{p,t} - Back_{p,t} - Inv_{p,t-1} + Back_{p,t-1} + D_{p,t} = x_{p,t}$ (Rearranged balance)
    3.  $Inv_{p,0}=0, Back_{p,0}=0$
    4.  $Inv_{p,4}=150, Back_{p,4}=0$
    5.  $x_{1,2}=0$