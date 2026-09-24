Model Type: MILP (Mixed Integer Linear Programming)
*Note: While the physical quantities (units) are large, in production planning contexts involving thousands of units, variables are typically treated as continuous to allow for fractional solutions (representing average production rates or large batch sizes). However, strictly speaking, units are discrete. Given the scale (100,000+), continuous relaxation is standard and yields integer solutions in practice for such smooth LPs, but we declare it as MILP to be safe regarding the discrete nature of "units", or simply LP if we assume divisibility. Given the prompt asks for a mathematical formulation and standard OR practice for aggregate production planning at this scale, **LP** is the most appropriate structural classification, but I will define variables as non-negative continuous, which is standard for this textbook problem type. If strict integrality is required, the solver will handle it, but the structure is linear.*

Let's refine the model type: The problem involves production quantities and inventory levels. These are aggregate flows. Standard formulation is **LP**.

### Index Sets & Parameters

**Index Sets:**
- $t \in \{1, 2, ..., 12\}$: Months, where $t=1$ is January, ..., $t=12$ is December.
- $p \in \{I, II\}$: Product types.

**Parameters:**

1.  **Demand ($d_{p,t}$)**: Units required per month.
    -   *Product I:*
        -   $d_{I,t} = 10,000$ for $t \in \{1, 2, 3, 4\}$ (Jan-Apr)
        -   $d_{I,t} = 30,000$ for $t \in \{5, 6, 7, 8, 9\}$ (May-Sep)
        -   $d_{I,t} = 100,000$ for $t \in \{10, 11, 12\}$ (Oct-Dec)
    -   *Product II:*
        -   $d_{II,t} = 15,000$ for $t \in \{3, 4, 5, 6, 7, 8, 9\}$ (Mar-Sep)
        -   $d_{II,t} = 50,000$ for $t \in \{1, 2, 10, 11, 12\}$ (Other months: Jan, Feb, Oct, Nov, Dec)

2.  **Production Costs ($c_{p,t}$)**: Yuan per unit.
    -   *Product I:*
        -   $c_{I,t} = 5.00$ for $t \in \{1, ..., 5\}$ (Jan-May)
        -   $c_{I,t} = 4.50$ for $t \in \{6, ..., 12\}$ (Jun-Dec)
    -   *Product II:*
        -   $c_{II,t} = 8.00$ for $t \in \{1, ..., 5\}$ (Jan-May)
        -   $c_{II,t} = 7.00$ for $t \in \{6, ..., 12\}$ (Jun-Dec)

3.  **Capacity Constraints:**
    -   $C_{cap} = 120,000$: Total monthly production capacity (units) for both products combined.
    -   $V_I = 0.2$: Volume per unit of Product I ($m^3$/unit).
    -   $V_{II} = 0.4$: Volume per unit of Product II ($m^3$/unit).
    -   $W_{max} = 15,000$: In-house warehouse volume capacity ($m^3$).

4.  **Storage Costs:**
    -   $h_{in} = 1.00$: Cost per $m^3$ per month for in-house storage.
    -   $h_{out} = 1.50$: Cost per $m^3$ per month for external rented storage.
    -   *Note:* The problem states "if using the in-house warehouse... if renting... cost increases to 1.5". This implies a two-tier cost structure: the first 15,000 $m^3$ costs 1.00, and any excess costs 1.50. Alternatively, it can be modeled as minimizing the sum of internal storage usage (cost 1.0) and external storage usage (cost 1.5) subject to volume limits.

### Decision Variables

For each month $t \in \{1, ..., 12\}$ and product $p \in \{I, II\}$:

1.  $x_{p,t} \ge 0$: Number of units of product $p$ produced in month $t$.
2.  $I_{p,t} \ge 0$: Inventory volume (in $m^3$) of product $p$ stored in the **in-house** warehouse at the end of month $t$.
3.  $E_{p,t} \ge 0$: Inventory volume (in $m^3$) of product $p$ stored in the **external** warehouse at the end of month $t$.

*Alternative Variable Formulation for Clarity on Volume:*
It is often cleaner to define inventory in units and convert to volume in constraints, or define inventory in volume directly. Let's define inventory in **units** to keep demand/production units consistent, and convert to volume for capacity/cost constraints.

**Revised Decision Variables:**
1.  $x_{p,t} \ge 0$: Units of product $p$ produced in month $t$.
2.  $u_{p,t} \ge 0$: Units of product $p$ in **in-house** inventory at end of month $t$.
3.  $e_{p,t} \ge 0$: Units of product $p$ in **external** inventory at end of month $t$.

*Note on Timing:* Inventory balances are typically defined as:
$Inventory_{start,t} + Production_t - Demand_t = Inventory_{end,t}$
Assuming initial inventory is 0.
Let $Inv_{p,t}$ be the total units of product $p$ available at the end of month $t$.
We split $Inv_{p,t}$ into in-house ($u_{p,t}$) and external ($e_{p,t}$) components.
Total units in stock at end of $t$: $u_{p,t} + e_{p,t}$.

### Objective Function

Minimize Total Cost = Production Cost + Storage Cost.

$$
\text{Minimize } Z = \sum_{t=1}^{12} \sum_{p \in \{I, II\}} c_{p,t} x_{p,t} + \sum_{t=1}^{12} \left( \sum_{p \in \{I, II\}} h_{in} (V_p u_{p,t}) + \sum_{p \in \{I, II\}} h_{out} (V_p e_{p,t}) \right)
$$

Simplifying the storage cost term (converting unit inventory to volume cost):
Storage Cost for product $p$ in month $t$ = $1.00 \times (0.2 u_{I,t} + 0.4 u_{II,t}) + 1.50 \times (0.2 e_{I,t} + 0.4 e_{II,t})$

$$
Z = \sum_{t=1}^{12} \left[ 5.00 x_{I,t} + 8.00 x_{II,t} \quad (\text{if } t \le 5) \text{ or } 4.50 x_{I,t} + 7.00 x_{II,t} \quad (\text{if } t > 5) + 0.2 u_{I,t} + 0.4 u_{II,t} + 0.3 e_{I,t} + 0.6 e_{II,t} \right]
$$
*(Note: The coefficients for $x$ change based on $t$ as defined in parameters. The storage coefficients are constant: $1.0 \times 0.2 = 0.2$ for I-in, $1.0 \times 0.4 = 0.4$ for II-in, $1.5 \times 0.2 = 0.3$ for I-out, $1.5 \times 0.4 = 0.6$ for II-out.)*

### Operational Constraints

**1. Inventory Balance Constraints**
For each product $p$ and month $t$:
The units available at the end of month $t$ equal the units available at the end of month $t-1$ plus production in month $t$ minus demand in month $t$.
Initial inventory at end of month 0 is 0.

$$
u_{p,t} + e_{p,t} = u_{p,t-1} + e_{p,t-1} + x_{p,t} - d_{p,t} \quad \forall p \in \{I, II\}, \forall t \in \{1, ..., 12\}
$$
With $u_{p,0} = 0, e_{p,0} = 0$.

**2. Warehouse Capacity Constraints (In-House)**
The total volume of in-house inventory for both products must not exceed 15,000 $m^3$.

$$
0.2 u_{I,t} + 0.4 u_{II,t} \le 15,000 \quad \forall t \in \{1, ..., 12\}
$$

**3. Production Capacity Constraints**
The total units produced for both products in any month must not exceed 120,000 units.

$$
x_{I,t} + x_{II,t} \le 120,000 \quad \forall t \in \{1, ..., 12\}
$$

**4. Non-negativity Constraints**

$$
x_{p,t} \ge 0, \quad u_{p,t} \ge 0, \quad e_{p,t} \ge 0 \quad \forall p \in \{I, II\}, \forall t \in \{1, ..., 12\}
$$

---

### Part (a): Show that the above problem has no feasible solution.

To prove infeasibility for the original problem (without external storage), we must look at the volume constraints.
In the original problem, there is no external storage. Thus, all inventory must fit in the 15,000 $m^3$ in-house warehouse.
So, $e_{p,t} = 0$ for all $t, p$. The balance constraint becomes:
$u_{p,t} = u_{p,t-1} + x_{p,t} - d_{p,t}$
And the volume constraint is:
$0.2 u_{I,t} + 0.4 u_{II,t} \le 15,000$

Let's analyze the cumulative demand vs. capacity.
Total Demand for Product I:
Jan-Apr: $4 \times 10,000 = 40,000$
May-Sep: $5 \times 30,000 = 150,000$
Oct-Dec: $3 \times 100,000 = 300,000$
Total $D_I = 490,000$ units.
Volume of Total $D_I = 490,000 \times 0.2 = 98,000 m^3$.

Total Demand for Product II:
Mar-Sep: $7 \times 15,000 = 105,000$
Other (Jan, Feb, Oct, Nov, Dec): $5 \times 50,000 = 250,000$
Total $D_{II} = 355,000$ units.
Volume of Total $D_{II} = 355,000 \times 0.4 = 142,000 m^3$.

Total Volume of Demand = $98,000 + 142,000 = 240,000 m^3$.

However, we must look at **monthly** constraints and the ability to produce ahead.
The bottleneck is usually the months with highest demand or where production capacity is tight relative to demand spikes.

Let's check the **peak demand months** for volume requirements if we had to satisfy demand from inventory built up previously, or if we must produce exactly in that month.
Actually, the most direct proof of infeasibility in the *original* problem (no external storage) comes from the **monthly production capacity** combined with **demand** in specific months, or the **inventory volume capacity** preventing sufficient pre-production.

Let's look at **October, November, December**.
Demand for I: 100,000 units/month.
Demand for II: 50,000 units/month.
Total Demand in Oct, Nov, Dec = $150,000$ units/month.
Production Capacity = $120,000$ units/month.
Since Demand ($150,000$) > Capacity ($120,000$) in Oct, Nov, Dec, we **must** have inventory available at the start of October to cover the shortfall.
Shortfall per month in Oct-Dec = $150,000 - 120,000 = 30,000$ units.
Total shortfall for Oct, Nov, Dec = $90,000$ units.
This means we need to have accumulated at least 90,000 units of inventory by the end of September.

Let's check if we can accumulate this inventory given the volume constraint.
To have 90,000 units of inventory at the end of September, what is the minimum volume required?
The inventory can be a mix of Product I and II. To minimize volume, we should store the product with the smaller volume per unit (Product I, 0.2 $m^3$/unit) as much as possible.
However, we are constrained by the fact that we also need to produce and sell Product II.
Let's look at the **maximum possible inventory volume** allowed: 15,000 $m^3$.
If we store only Product I (smallest volume), the max units we can store is $15,000 / 0.2 = 75,000$ units.
If we store only Product II, the max units is $15,000 / 0.4 = 37,500$ units.
The maximum total units we can store in the warehouse is 75,000 units (if all Product I).

But we need to cover a shortfall of **90,000 units** in the next 3 months.
Even if we fill the entire warehouse with Product I (which has the smallest volume), we can only hold 75,000 units.
Since $75,000 < 90,000$, it is physically impossible to store enough inventory to cover the demand shortfall in Oct-Dec, given the warehouse volume limit of 15,000 $m^3$ and the production capacity limit of 120,000 units/month.

**Formal Proof of Infeasibility:**
1.  In months $t \in \{10, 11, 12\}$, total demand $d_{I,t} + d_{II,t} = 100,000 + 50,000 = 150,000$ units.
2.  Production capacity $C = 120,000$ units.
3.  Therefore, for each of these 3 months, the factory must draw down at least $150,000 - 120,000 = 30,000$ units from inventory.
4.  Total inventory required at the start of October (end of September) is at least $3 \times 30,000 = 90,000$ units.
5.  Let $V_{inv}$ be the volume of inventory at the end of September.
    $V_{inv} = 0.2 u_{I,9} + 0.4 u_{II,9}$.
    The constraint is $V_{inv} \le 15,000$.
6.  The total units in inventory $U_{inv} = u_{I,9} + u_{II,9}$.
    To maximize the number of units $U_{inv}$ for a given volume, we must minimize the average volume per unit. The minimum volume per unit is for Product I ($0.2 m^3$).
    Thus, $V_{inv} \ge 0.2 (u_{I,9} + u_{II,9}) = 0.2 U_{inv}$.
    This implies $U_{inv} \le V_{inv} / 0.2$.
    Substituting the max volume: $U_{inv} \le 15,000 / 0.2 = 75,000$ units.
7.  We require $U_{inv} \ge 90,000$ units.
8.  Since $75,000 < 90,000$, no feasible solution exists for the original problem.

### Final Model for Part (b)

**Model Type:** LP (Linear Programming)

**Sets:**
- $T = \{1, \dots, 12\}$ (Months)
- $P = \{I, II\}$ (Products)

**Parameters:**
- $d_{I,t}$: 
  - $10,000$ for $t=1..4$
  - $30,000$ for $t=5..9$
  - $100,000$ for $t=10..12$
- $d_{II,t}$:
  - $50,000$ for $t=1,2,10,11,12$
  - $15,000$ for $t=3..9$
- $c_{I,t}$:
  - $5.00$ for $t=1..5$
  - $4.50$ for $t=6..12$
- $c_{II,t}$:
  - $8.00$ for $t=1..5$
  - $7.00$ for $t=6..12$
- $C_{prod} = 120,000$ (Monthly production capacity in units)
- $V_I = 0.2$, $V_{II} = 0.4$ (Volume per unit in $m^3$)
- $W_{cap} = 15,000$ (In-house warehouse capacity in $m^3$)
- $h_{in} = 1.00$ ($m^3$/month)
- $h_{out} = 1.50$ ($m^3$/month)

**Decision Variables:**
- $x_{p,t} \ge 0$: Units of product $p$ produced in month $t$.
- $u_{p,t} \ge 0$: Units of product $p$ in in-house inventory at end of month $t$.
- $e_{p,t} \ge 0$: Units of product $p$ in external inventory at end of month $t$.

**Objective Function:**
$$
\text{Minimize } Z = \sum_{t=1}^{12} \sum_{p \in P} c_{p,t} x_{p,t} + \sum_{t=1}^{12} \left[ h_{in} \left( V_I u_{I,t} + V_{II} u_{II,t} \right) + h_{out} \left( V_I e_{I,t} + V_{II} e_{II,t} \right) \right]
$$

**Constraints:**

1.  **Inventory Balance:**
    $$
    u_{p,t} + e_{p,t} = u_{p,t-1} + e_{p,t-1} + x_{p,t} - d_{p,t} \quad \forall p \in P, t \in T
    $$
    Subject to $u_{p,0} = 0, e_{p,0} = 0$.

2.  **In-House Warehouse Capacity:**
    $$
    V_I u_{I,t} + V_{II} u_{II,t} \le W_{cap} \quad \forall t \in T
    $$
    $$
    0.2 u_{I,t} + 0.4 u_{II,t} \le 15,000 \quad \forall t \in T
    $$

3.  **Production Capacity:**
    $$
    x_{I,t} + x_{II,t} \le C_{prod} \quad \forall t \in T
    $$
    $$
    x_{I,t} + x_{II,t} \le 120,000 \quad \forall t \in T
    $$

4.  **Non-negativity:**
    $$
    x_{p,t} \ge 0, u_{p,t} \ge 0, e_{p,t} \ge 0 \quad \forall p \in P, t \in T
    $$