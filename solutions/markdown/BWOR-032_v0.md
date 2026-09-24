**Model Type Declaration:** MILP (Mixed-Integer Linear Program)
*Note: While the core structure is linear, production quantities are typically discrete units. However, given the large scale (tens of thousands of units), continuous variables are often acceptable for LP solvers unless integer precision is strictly required. Based on standard OR problem conventions for such large numbers, we will define variables as **Continuous** for computational tractability, but note that if strict integrality is required, they would be Integer. Given the prompt's rule "Use INTEGER variables for discrete physical units (e.g., ships, workers, machines)" and "CONTINUOUS variables for continuous resources (e.g., ... aggregate quantities)", production units are discrete physical items. However, in large-scale production planning, LP relaxation is standard. Let's look at the rules again. Rule 2: "Use INTEGER variables for discrete physical units". Product units are discrete. But solving a 12-month, 2-product MILP with these magnitudes is standard. Let's stick to **LP** (Continuous) as is standard for production planning problems of this magnitude unless "integer" is explicitly emphasized in the problem context (it is not, it asks for a schedule). Actually, looking at Rule 2 again: "Use INTEGER variables for discrete physical units (e.g., ships, workers, machines). Use CONTINUOUS variables for continuous resources (e.g., time, area, land, aggregate quantities)." Production quantity is an aggregate quantity. I will use **Continuous** variables to ensure the model is an LP, which is the standard approach for this classic problem type. If the solver requires integers, the logic holds, but LP is the primary model type here. Let's classify it as **LP**.

### Index Sets & Parameters

**Index Sets:**
*   $t \in \{1, 2, ..., 12\}$: Months (Jan to Dec).
*   $p \in \{1, 2\}$: Products (I and II).

**Parameters:**

**1. Demand ($D_{p,t}$):**
*   **Product I ($p=1$):**
    *   $t \in \{1, 2, 3, 4\}$ (Jan-Apr): $D_{1,t} = 10,000$
    *   $t \in \{5, 6, 7, 8, 9\}$ (May-Sep): $D_{1,t} = 30,000$
    *   $t \in \{10, 11, 12\}$ (Oct-Dec): $D_{1,t} = 100,000$
*   **Product II ($p=2$):**
    *   $t \in \{3, 4, 5, 6, 7, 8, 9\}$ (Mar-Sep): $D_{2,t} = 15,000$
    *   $t \in \{1, 2, 10, 11, 12\}$ (Jan, Feb, Oct, Nov, Dec): $D_{2,t} = 50,000$

**2. Production Costs ($c_{p,t}$):**
*   **Product I ($p=1$):**
    *   $t \in \{1, ..., 5\}$ (Jan-May): $c_{1,t} = 5.0$ yuan/unit
    *   $t \in \{6, ..., 12\}$ (Jun-Dec): $c_{1,t} = 4.5$ yuan/unit
*   **Product II ($p=2$):**
    *   $t \in \{1, ..., 5\}$ (Jan-May): $c_{2,t} = 5.0$? No, text says: "For product II: 8 yuan per unit if produced from January to May".
    *   Correction:
        *   $t \in \{1, ..., 5\}$ (Jan-May): $c_{2,t} = 8.0$ yuan/unit
        *   $t \in \{6, ..., 12\}$ (Jun-Dec): $c_{2,t} = 7.0$ yuan/unit

**3. Capacity & Volume:**
*   **Monthly Production Capacity ($C_t$):** $120,000$ units for all $t$.
*   **Unit Volume ($v_p$):**
    *   Product I: $v_1 = 0.2$ m³/unit
    *   Product II: $v_2 = 0.4$ m³/unit
*   **Warehouse Capacity ($W_{cap}$):** $15,000$ m³ (Internal).
*   **Storage Costs ($h_{t}$):**
    *   Internal: $1.0$ yuan/m³/month.
    *   External: $1.5$ yuan/m³/month.
    *   *Note:* The problem states "If using the in-house warehouse, the cost per m³ per month is 1 yuan; if renting from an external warehouse, the cost increases to 1.5 yuan per m³ per month." This implies a two-tier storage cost structure based on volume used.

**4. Other:**
*   Initial Inventory: $0$ for both products.
*   Final Inventory: $0$ (Demand must be met, no explicit salvage value, assume end inventory must be 0 or simply that all demand is met by production + initial inventory). Standard assumption: Meet demand exactly, end inventory can be 0 unless specified otherwise. Usually, "meet market demand" implies $I_{p,12} \ge 0$ and we minimize cost, so excess inventory at the end would incur storage cost but no penalty. However, typically we assume no need for inventory beyond meeting the last period's demand. Let's assume $I_{p,12} = 0$ is not strictly required, but since there is no salvage value and positive holding cost, optimal solution will likely have $I_{p,12}=0$. To be safe, we allow $I_{p,12} \ge 0$.

### Decision Variables

Let:
*   $x_{p,t} \ge 0$: Continuous variable representing the quantity of product $p$ produced in month $t$.
*   $I_{p,t} \ge 0$: Continuous variable representing the inventory of product $p$ at the **end** of month $t$.
*   $S_{t} \ge 0$: Continuous variable representing the volume (m³) of **external** warehouse space rented in month $t$.
*   $V_{t}^{in} \ge 0$: Auxiliary variable representing the volume (m³) of inventory stored in the **internal** warehouse at the end of month $t$.
    *   *Alternative formulation for storage costs:* Since the cost depends on whether internal or external space is used, and internal is cheaper, the optimal strategy will always fill internal space first.
    *   Total Volume at end of month $t$: $Vol_t = \sum_{p} v_p I_{p,t}$.
    *   Internal Volume Used: $V_t^{in} = \min(Vol_t, W_{cap})$.
    *   External Volume Used: $S_t = \max(0, Vol_t - W_{cap})$.
    *   This non-linearity ($\min/\max$) can be linearized.
    *   Let $V_t$ be the total volume.
    *   Constraint 1: $V_t = \sum_{p} v_p I_{p,t}$
    *   Constraint 2: $V_t^{in} + S_t = V_t$ (All volume is either internal or external)
    *   Constraint 3: $V_t^{in} \le W_{cap}$
    *   Constraint 4: $S_t \ge 0$
    *   Objective term for storage: $1.0 \cdot V_t^{in} + 1.5 \cdot S_t$.
    *   Since $1.0 < 1.5$, the solver will naturally minimize $S_t$ (external) by maximizing $V_t^{in}$ up to $W_{cap}$. This linear formulation is correct.

### Objective Function

Minimize Total Cost $Z$:

$$ Z = \sum_{p \in \{1,2\}} \sum_{t=1}^{12} c_{p,t} x_{p,t} + \sum_{t=1}^{12} (1.0 \cdot V_t^{in} + 1.5 \cdot S_t) $$

Where:
*   Production Cost: $\sum c_{p,t} x_{p,t}$
*   Storage Cost: $\sum (1.0 V_t^{in} + 1.5 S_t)$

### Operational Constraints

**1. Inventory Balance Constraints (for each product $p$ and month $t$):**
$$ I_{p,t-1} + x_{p,t} = D_{p,t} + I_{p,t} $$
*   For $t=1$, $I_{p,0} = 0$.
*   $I_{p,t} \ge 0$.

**2. Production Capacity Constraint (for each month $t$):**
$$ x_{1,t} + x_{2,t} \le 120,000 $$

**3. Warehouse Volume Constraints (for each month $t$):**
*   Total Volume:
    $$ V_t = 0.2 I_{1,t} + 0.4 I_{2,t} $$
*   Internal/External Split:
    $$ V_t^{in} + S_t = V_t $$
    $$ V_t^{in} \le 15,000 $$
    $$ V_t^{in} \ge 0, \quad S_t \ge 0 $$

**4. Non-negativity:**
$$ x_{p,t} \ge 0, \quad I_{p,t} \ge 0, \quad V_t^{in} \ge 0, \quad S_t \ge 0 \quad \forall p, t $$

---

### Analysis of Part (a): Infeasibility Check

To show part (a) is infeasible, we check if demand can be met without external storage (i.e., $S_t = 0 \implies V_t \le 15,000$ for all $t$) or if the production capacity is insufficient to meet demand even with infinite storage.

Let's check the peak demand month, October ($t=10$).
*   $D_{1,10} = 100,000$
*   $D_{2,10} = 50,000$
*   Total Demand in Oct = $150,000$ units.
*   Production Capacity in Oct = $120,000$ units.

If we rely solely on production in October, we can only produce 120,000 units. The remaining 30,000 units must come from inventory accumulated in previous months.
Let's check if we can accumulate enough inventory.
Total Volume Constraint: $0.2 I_{1,t} + 0.4 I_{2,t} \le 15,000$.

Let's look at the total units required over the whole year vs total production capacity.
Total Production Capacity = $12 \times 120,000 = 1,440,000$ units.

Total Demand:
Product I:
*   Jan-Apr (4 mo): $4 \times 10,000 = 40,000$
*   May-Sep (5 mo): $5 \times 30,000 = 150,000$
*   Oct-Dec (3 mo): $3 \times 100,000 = 300,000$
*   Total I = $490,000$ units.

Product II:
*   Jan, Feb (2 mo): $2 \times 50,000 = 100,000$
*   Mar-Sep (7 mo): $7 \times 15,000 = 105,000$
*   Oct-Dec (3 mo): $3 \times 50,000 = 150,000$
*   Total II = $355,000$ units.

Total Demand = $490,000 + 355,000 = 845,000$ units.
Total Capacity = $1,440,000$ units.
Aggregate supply > aggregate demand. So, aggregate capacity is not the issue. The issue is timing and storage.

The problem asks to "Show that the above problem has no feasible solution." This usually refers to the original problem description *before* allowing external storage. The original text says "the factory's warehouse volume capacity is 15,000 m³". It doesn't mention external storage in the first paragraph. Part (b) introduces external storage. Thus, Part (a) asks to prove infeasibility of the model **without** external storage (i.e., $S_t = 0$ for all $t$).

Let's verify infeasibility of the model with $S_t=0$ (Internal Only).
Constraint: $0.2 I_{1,t} + 0.4 I_{2,t} \le 15,000$ for all $t$.
This implies max inventory volume is 15,000 m³.
Max units of Product I stored: $15,000 / 0.2 = 75,000$ units.
Max units of Product II stored: $15,000 / 0.4 = 37,500$ units.

Look at October ($t=10$).
Demand $D_{1,10} = 100,000$, $D_{2,10} = 50,000$.
Total Demand = 150,000.
Production Capacity = 120,000.
Deficit in Oct = 30,000 units.
This deficit must be covered by $I_{1,9} + I_{2,9}$.
So we need $I_{1,9} + I_{2,9} \ge 30,000$.
Also, volume constraint at $t=9$: $0.2 I_{1,9} + 0.4 I_{2,9} \le 15,000$.

Let $I_{1,9} = x, I_{2,9} = y$.
1) $x + y \ge 30,000$
2) $0.2x + 0.4y \le 15,000 \implies x + 2y \le 75,000$

From (1), $x \ge 30,000 - y$.
Substitute into (2):
$(30,000 - y) + 2y \le 75,000$
$30,000 + y \le 75,000$
$y \le 45,000$.
This is feasible so far. For example, if $y=0, x=30,000$, volume is $0.2(30,000) = 6,000 \le 15,000$.

However, we must also satisfy the inventory balance for previous months.
To have $x=30,000$ units of Product I in inventory at end of Sep ($t=9$), we must have produced excess in previous months.
Let's check the cumulative balance.

Actually, a simpler check might be the peak demand vs capacity + max storage.
In any month $t$, Max Deliverable = Production ($120,000$) + Inventory from previous month.
Inventory from previous month is limited by volume.
Max Inventory Volume = 15,000 m³.
Max Units in Inventory depends on mix.
If we store only Product I (0.2 m³/unit), max units = 75,000.
If we store only Product II (0.4 m³/unit), max units = 37,500.
So max units available from inventory is 75,000 (if all Product I).

In October:
Demand = 150,000.
Production = 120,000.
Need 30,000 from inventory.
Can we have 30,000 units of inventory? Yes, 30,000 units of Product I is 6,000 m³, which is < 15,000 m³.
So, is it infeasible?

Let's look at November ($t=11$) and December ($t=12$).
Oct Demand: 150,000.
Nov Demand: 150,000.
Dec Demand: 150,000.
Total Q4 Demand = 450,000.
Total Q4 Capacity = $3 \times 120,000 = 360,000$.
Total Deficit in Q4 = $450,000 - 360,000 = 90,000$ units.
These 90,000 units must come from inventory built up in Jan-Sep.
So, $I_{1,9} + I_{2,9}$ (total units in inventory at end of Sep) must be at least 90,000 units.
Let's check if we can store 90,000 units in 15,000 m³.
Min volume for 90,000 units:
To minimize volume, we should store the product with smaller volume per unit? No, we are constrained by volume.
Max units we can store in 15,000 m³:
If all Product I: $15,000 / 0.2 = 75,000$ units.
If all Product II: $15,000 / 0.4 = 37,500$ units.
Maximum possible units in inventory at any time is 75,000 (if all Product I).
But we need 90,000 units of *total* inventory (mix of I and II) to cover the Q4 deficit?
Wait, the deficit is calculated as Total Demand - Total Production.
Let $I_{total, 9} = I_{1,9} + I_{2,9}$.
We need $I_{total, 9} \ge 90,000$.
Constraint: $0.2 I_{1,9} + 0.4 I_{2,9} \le 15,000$.
Let's maximize $I_{1,9} + I_{2,9}$ subject to $0.2 I_{1,9} + 0.4 I_{2,9} \le 15,000$ and $I \ge 0$.
Since Product I has lower volume per unit (0.2 vs 0.4), we should fill the warehouse with Product I to maximize unit count.
Max Units = $15,000 / 0.2 = 75,000$ units (all Product I).
So, max inventory units at end of Sep is 75,000.
But we need 90,000 units to cover the Q4 deficit.
$75,000 < 90,000$.
Therefore, it is impossible to meet the demand in Q4 with the given production capacity and internal warehouse limit.
Thus, the problem is **INFEASIBLE** without external storage.

### Final Formulation for Part (b)

Part (b) allows renting external storage. This removes the hard cap on total volume, replacing it with a cost penalty. The model defined above (with $S_t$) is the correct formulation for Part (b).

**Summary of Model for Part (b):**

**Sets:**
$t = 1, \dots, 12$
$p = 1, 2$

**Parameters:**
$D_{1,t}$: 10k (Jan-Apr), 30k (May-Sep), 100k (Oct-Dec)
$D_{2,t}$: 50k (Jan, Feb, Oct, Nov, Dec), 15k (Mar-Sep)
$c_{1,t}$: 5.0 (Jan-May), 4.5 (Jun-Dec)
$c_{2,t}$: 8.0 (Jan-May), 7.0 (Jun-Dec)
$Cap_t = 120,000$
$v_1 = 0.2, v_2 = 0.4$
$W_{cap} = 15,000$
$h_{in} = 1.0, h_{ext} = 1.5$

**Variables:**
$x_{p,t} \ge 0$: Production of product $p$ in month $t$.
$I_{p,t} \ge 0$: End-of-month inventory of product $p$.
$V_t^{in} \ge 0$: Volume of internal storage used in month $t$.
$S_t \ge 0$: Volume of external storage rented in month $t$.

**Objective:**
Min $Z = \sum_{t=1}^{12} \left( 5.0 x_{1,t}^{Jan-May} + 4.5 x_{1,t}^{Jun-Dec} + 8.0 x_{2,t}^{Jan-May} + 7.0 x_{2,t}^{Jun-Dec} + 1.0 V_t^{in} + 1.5 S_t \right)$
*(Note: The coefficients for $x$ change based on $t$. In code, use $c_{p,t}$.)*

**Constraints:**
1.  **Inventory Balance:**
    $I_{p,t-1} + x_{p,t} = D_{p,t} + I_{p,t}$ for all $p, t$ (with $I_{p,0}=0$)
2.  **Production Capacity:**
    $x_{1,t} + x_{2,t} \le 120,000$ for all $t$
3.  **Volume Balance:**
    $V_t^{in} + S_t = 0.2 I_{1,t} + 0.4 I_{2,t}$ for all $t$
4.  **Internal Warehouse Limit:**
    $V_t^{in} \le 15,000$ for all $t$
5.  **Non-negativity:**
    $x_{p,t}, I_{p,t}, V_t^{in}, S_t \ge 0$