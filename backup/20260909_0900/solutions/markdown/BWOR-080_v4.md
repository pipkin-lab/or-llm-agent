### 1. Index Sets & Parameters

**Sets:**
*   $P$: Set of products, $P = \{I, II, III, IV, V, VI, VII\}$ (indexed by $j=1,\dots,7$).
*   $M$: Set of machine types, $M = \{G, UD, HD, B, Pl\}$ (Grinding, Upright Drill, Horizontal Drill, Boring, Planer).
*   $T$: Set of months, $T = \{Jan, Feb, Mar, Apr, May, Jun\}$ (indexed by $t=1,\dots,6$).

**Parameters:**
*   $a_{m,j}$: Machine hours required per unit of product $j$ on machine type $m$.
    *   If $a_{m,j} = 0$ or "--", the product does not require that machine.
    *   **Data from Table C-3:**
        *   Grinding ($G$): $[0.5, 0.7, 0, 0, 0.3, 0.2, 0.5]$
        *   Upright Drill ($UD$): $[0.1, 0.2, 0, 0.3, 0, 0.6, 0]$
        *   Horizontal Drill ($HD$): $[0.2, 0, 0.8, 0, 0, 0, 0.6]$
        *   Boring ($B$): $[0.05, 0.03, 0, 0.07, 0.1, 0, 0.08]$
        *   Planer ($Pl$): $[0, 0, 0.01, 0, 0.05, 0, 0.05]$
*   $c_j$: Profit per unit of product $j$ (yuan).
    *   $c = [100, 60, 80, 40, 110, 90, 30]$
*   $D_{t,j}$: Maximum market demand for product $j$ in month $t$ (units).
    *   **Data from Table C-4:**
        *   Jan: $[500, 1000, 300, 300, 800, 200, 100]$
        *   Feb: $[600, 500, 200, 0, 400, 300, 150]$
        *   Mar: $[300, 600, 0, 0, 500, 400, 100]$
        *   Apr: $[200, 300, 400, 500, 200, 0, 100]$
        *   May: $[0, 100, 500, 100, 1000, 300, 0]$
        *   Jun: $[500, 500, 100, 300, 1100, 500, 60]$
*   $h_j$: Holding cost per unit per month. $h_j = 5$ for all $j$.
*   $I_{max}$: Maximum inventory level per product. $I_{max} = 100$.
*   $I_{0,j}$: Initial inventory. $I_{0,j} = 0$ for all $j$.
*   $I_{T,j}$: Required final inventory (end of June). $I_{T,j} = 50$ for all $j$.
*   $H_{total}$: Total available hours per machine type per month before maintenance.
    *   Working days = 24, Shifts/day = 2, Hours/shift = 8.
    *   Hours/month per machine = $24 \times 2 \times 8 = 384$ hours.
*   $N_m$: Total number of machines of type $m$.
    *   $N_G = 4, N_{UD} = 2, N_{HD} = 3, N_B = 1, N_{Pl} = 1$.
*   $K_{t,m}$: Number of machines of type $m$ undergoing maintenance in month $t$.
    *   Jan: $K_{G}=1$, others 0.
    *   Feb: $K_{HD}=2$, others 0.
    *   Mar: $K_{B}=1$, others 0.
    *   Apr: $K_{UD}=1$, others 0.
    *   May: $K_{G}=1, K_{UD}=1$, others 0.
    *   Jun: $K_{Pl}=1, K_{HD}=1$, others 0.

**Derived Parameter:**
*   $Cap_{t,m}$: Available capacity (hours) for machine type $m$ in month $t$.
    *   $Cap_{t,m} = (N_m - K_{t,m}) \times 384$.

### 2. Decision Variables

Let:
*   $x_{t,j}$: Number of units of product $j$ produced in month $t$. **Continuous**, $x_{t,j} \ge 0$.
*   $S_{t,j}$: Number of units of product $j$ sold in month $t$. **Continuous**, $S_{t,j} \ge 0$.
*   $Inv_{t,j}$: Inventory of product $j$ at the **end** of month $t$. **Continuous**, $Inv_{t,j} \ge 0$.

### 3. Objective Function

Maximize total profit over 6 months. Profit is generated upon sale. Holding costs are incurred on ending inventory for each month.

$$
\text{Maximize } Z = \sum_{t=1}^{6} \sum_{j \in P} c_j S_{t,j} - \sum_{t=1}^{6} \sum_{j \in P} h_j Inv_{t,j}
$$

### 4. Operational Constraints

**1. Inventory Balance Constraint**
For each month $t$ and product $j$:
$$
Inv_{t-1,j} + x_{t,j} - S_{t,j} = Inv_{t,j}
$$
With $Inv_{0,j} = 0$.

**2. Sales Demand Constraint**
Sales cannot exceed market demand in any month.
$$
S_{t,j} \le D_{t,j} \quad \forall t \in T, j \in P
$$

**3. Inventory Capacity Constraint**
Inventory at the end of each month cannot exceed the storage limit.
$$
Inv_{t,j} \le 100 \quad \forall t \in T, j \in P
$$

**4. Final Inventory Requirement**
The inventory at the end of June must be exactly 50 units for each product.
$$
Inv_{6,j} = 50 \quad \forall j \in P
$$
*(Note: This constraint effectively forces the model to produce enough in the final periods or early periods to satisfy this exact closing balance, combined with the storage limit).*

**5. Machine Capacity Constraints**
For each machine type $m$ and month $t$, the total processing time required by production must not exceed available capacity.
$$
\sum_{j \in P} a_{m,j} x_{t,j} \le Cap_{t,m} \quad \forall m \in M, t \in T
$$

**6. Non-negativity**
$$
x_{t,j} \ge 0, \quad S_{t,j} \ge 0, \quad Inv_{t,j} \ge 0 \quad \forall t, j
$$