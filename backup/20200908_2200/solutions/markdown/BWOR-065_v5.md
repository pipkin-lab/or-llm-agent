To model this production planning problem, we must carefully handle the units, fixed costs, and inventory constraints. This is a mixed-integer linear programming (MILP) problem because the fixed operating cost requires a binary variable to indicate whether production occurs.

### 1. Index Sets & Parameters

**Index Sets:**
*   $t = \{1, 2, 3, 4, 5, 6\}$: Set of months.

**Parameters (converted to consistent units):**
The problem provides data in "hundreds of units" for quantities and "yuan" for costs. To avoid large numbers and confusion, we will define the decision variables in **hundreds of units**.

*   $D_t$: Demand (delivery requirement) in month $t$ (hundreds of units).
    *   $D_1=1, D_2=2, D_3=5, D_4=3, D_5=2, D_6=1$.
*   $C_{prod}$: Variable production cost per 100 units = 10,000 yuan.
*   $C_{fix}$: Fixed operating cost if production occurs = 4,000 yuan.
*   $C_{store}$: Storage cost per 100 units per month = 1,000 yuan.
*   $P_{cap}$: Maximum production capacity per month = 400 units = **4** (hundreds of units).
*   $I_{cap}$: Maximum warehouse storage capacity = 300 units = **3** (hundreds of units).

### 2. Decision Variables

*   $x_t \ge 0$: The quantity produced in month $t$ (in hundreds of units).
    *   *Note on Integrality:* The problem asks "How many units". While production is often continuous in LP, "units" are discrete. However, the scale is small (hundreds). Standard production planning models often assume divisibility unless specified otherwise. Given the target is likely an integer solution in practice, we will define $x_t$ as **continuous** first, but note that if the optimal solution yields non-integers, rounding or integer constraints $x_t \in \mathbb{Z}$ might be needed. However, looking at the data (integers for demand and capacity), an LP relaxation often yields integer results for this specific structure (network flow-like). Let's stick to $x_t \ge 0$ (continuous) as is standard for textbook production planning unless "integer units" is explicitly stressed over the "hundreds" block. *Self-Correction*: The prompt says "How many units". 1 unit is the base. But the table is in hundreds. Let's define $x_t$ in **hundreds of units**. If the answer requires specific unit counts, we multiply by 100. Given the fixed cost is small relative to variable costs, integer constraints on the *hundreds* might be too restrictive or unnecessary. Let's assume continuous $x_t$ for the model formulation, which is standard for this type of linear programming problem.

*   $y_t \in \{0, 1\}$: Binary variable for month $t$.
    *   $y_t = 1$ if $x_t > 0$ (production takes place).
    *   $y_t = 0$ if $x_t = 0$.

*   $I_t \ge 0$: Inventory level at the **end** of month $t$ (in hundreds of units).

### 3. Objective Function

Minimize Total Cost ($Z$):

$$ Z = \sum_{t=1}^{6} \left( C_{prod} x_t + C_{fix} y_t + C_{store} I_t \right) $$

Substituting values:
$$ Z = \sum_{t=1}^{6} (10000 x_t + 4000 y_t + 1000 I_t) $$

### 4. Operational Constraints

**A. Inventory Balance (Flow Conservation)**
The inventory at the end of month $t$ is the previous inventory plus production minus demand.
$$ I_t = I_{t-1} + x_t - D_t, \quad \forall t \in \{1, \dots, 6\} $$
*   Given $I_0 = 0$ (no initial inventory).

**B. Final Inventory Constraint**
No inventory remaining after the final delivery.
$$ I_6 = 0 $$

**C. Production Capacity**
Production cannot exceed the monthly capacity.
$$ x_t \le P_{cap}, \quad \forall t \in \{1, \dots, 6\} $$
$$ x_t \le 4, \quad \forall t \in \{1, \dots, 6\} $$

**D. Warehouse Capacity**
Inventory at the end of each month cannot exceed storage capacity.
$$ I_t \le I_{cap}, \quad \forall t \in \{1, \dots, 6\} $$
$$ I_t \le 3, \quad \forall t \in \{1, \dots, 6\} $$

**E. Linking Fixed Cost to Production (Big-M Constraint)**
If production occurs ($x_t > 0$), then $y_t$ must be 1. If $y_t = 0$, then $x_t$ must be 0.
We use the production capacity $P_{cap}$ as the Big-M constant.
$$ x_t \le P_{cap} y_t, \quad \forall t \in \{1, \dots, 6\} $$
$$ x_t \le 4 y_t, \quad \forall t \in \{1, \dots, 6\} $$

**F. Non-negativity and Domains**
$$ x_t \ge 0, \quad \forall t \in \{1, \dots, 6\} $$
$$ I_t \ge 0, \quad \forall t \in \{1, \dots, 6\} $$
$$ y_t \in \{0, 1\}, \quad \forall t \in \{1, \dots, 6\} $$

### 5. Model Summary

**Minimize:**
$$ 10000 \sum_{t=1}^{6} x_t + 4000 \sum_{t=1}^{6} y_t + 1000 \sum_{t=1}^{6} I_t $$

**Subject to:**
1.  $I_t - I_{t-1} - x_t = -D_t, \quad t=1,\dots,6$ (with $I_0=0$)
2.  $I_6 = 0$
3.  $x_t \le 4, \quad t=1,\dots,6$
4.  $I_t \le 3, \quad t=1,\dots,6$
5.  $x_t - 4y_t \le 0, \quad t=1,\dots,6$
6.  $x_t \ge 0, I_t \ge 0, y_t \in \{0,1\}, \quad t=1,\dots,6$

**Demand Vector $D$:** $[1, 2, 5, 3, 2, 1]$