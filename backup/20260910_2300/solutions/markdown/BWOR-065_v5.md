# Production Planning Optimization Model

## Model Type Declaration
**Mixed Integer Linear Programming (MILP)**

The model requires binary variables to capture the fixed cost incurred when production occurs in a given month. All other terms are linear.

## Index Sets & Parameters

**Sets:**
- $T = \{1, 2, 3, 4, 5, 6\}$: Set of months.

**Parameters (converted to consistent units of "hundreds of units" and "yuan"):**
- $d_t$: Delivery demand at the end of month $t$ (in hundreds of units).
  - $d_1 = 1, d_2 = 2, d_3 = 5, d_4 = 3, d_5 = 2, d_6 = 1$.
- $M$: Maximum production capacity per month = 400 units = **4** (hundreds of units).
- $K$: Maximum warehouse storage capacity = 300 units = **3** (hundreds of units).
- $c_v$: Variable production cost = 10,000 yuan per 100 units = **10,000** (yuan per hundred units).
- $c_f$: Fixed production cost per active month = **4,000** (yuan).
- $c_s$: Storage cost = 1,000 yuan per 100 units per month = **1,000** (yuan per hundred units per month).
- $I_0$: Initial inventory = 0.
- $I_6$: Final inventory = 0.

## Decision Variables

1.  $x_t \in \mathbb{R}_{\ge 0}$: Quantity produced in month $t$ (in hundreds of units).
2.  $I_t \in \mathbb{R}_{\ge 0}$: Inventory level at the end of month $t$ (after delivery) (in hundreds of units).
3.  $y_t \in \{0, 1\}$: Binary variable where $y_t = 1$ if production takes place in month $t$ (i.e., $x_t > 0$), and $y_t = 0$ otherwise.

## Objective Function

Minimize Total Cost ($Z$):
$$
\text{Minimize } Z = \sum_{t=1}^{6} \left( c_v x_t + c_f y_t + c_s I_t \right)
$$

Substituting parameter values:
$$
\text{Minimize } Z = 10000 \sum_{t=1}^{6} x_t + 4000 \sum_{t=1}^{6} y_t + 1000 \sum_{t=1}^{6} I_t
$$

## Operational Constraints

**1. Inventory Balance Constraints**
The inventory at the end of month $t$ is the previous inventory plus current production minus current delivery.
$$
I_t = I_{t-1} + x_t - d_t, \quad \forall t \in \{1, \dots, 6\}
$$
*Boundary Conditions:*
- $I_0 = 0$
- $I_6 = 0$

**2. Production Capacity Constraints**
Production in any month cannot exceed the maximum capacity.
$$
x_t \le M \cdot y_t, \quad \forall t \in \{1, \dots, 6\}
$$
Substituting $M=4$:
$$
x_t \le 4 y_t, \quad \forall t \in \{1, \dots, 6\}
$$
*Note: This constraint ensures that if $x_t > 0$, then $y_t$ must be 1, triggering the fixed cost. If $y_t=0$, then $x_t=0$.*

**3. Warehouse Storage Capacity Constraints**
The inventory at the end of each month cannot exceed the warehouse capacity.
$$
I_t \le K, \quad \forall t \in \{1, \dots, 6\}
$$
Substituting $K=3$:
$$
I_t \le 3, \quad \forall t \in \{1, \dots, 6\}
$$

**4. Non-negativity and Domain Constraints**
$$
x_t \ge 0, \quad \forall t \in \{1, \dots, 6\}
$$
$$
I_t \ge 0, \quad \forall t \in \{1, \dots, 6\}
$$
$$
y_t \in \{0, 1\}, \quad \forall t \in \{1, \dots, 6\}
$$

## Feasibility Sanity Check

- **Total Demand**: $\sum d_t = 1 + 2 + 5 + 3 + 2 + 1 = 14$ (hundreds).
- **Total Capacity**: $6 \times 4 = 24$ (hundreds). Total supply capacity exceeds total demand, so the problem is feasible regarding aggregate volume.
- **Peak Demand Check**:
  - Month 1: $I_1 = 0 + x_1 - 1$. Max $I_1=3 \implies x_1 \le 4$. OK.
  - Month 2: $I_2 = I_1 + x_2 - 2$.
  - Month 3: $I_3 = I_2 + x_3 - 5$. Max $I_3=3$.
    - To satisfy $d_3=5$, we need sufficient prior stock.
    - If we produce max in M1 (4) and M2 (4), $I_2$ could be up to $3+4-2=5$ (but capped at 3). So $I_2=3$.
    - Then $I_3 = 3 + x_3 - 5 = x_3 - 2$. For $I_3 \ge 0$, we need $x_3 \ge 2$. This is within capacity ($x_3 \le 4$).
    - So, it is feasible to meet the high demand in Month 3 by stocking up in Months 1 and 2.
- **End Condition**: $I_6=0$ is achievable by reducing production in later months.

The model is feasible.