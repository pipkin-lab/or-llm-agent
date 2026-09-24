# Model Type: MILP (Mixed-Integer Linear Programming)
*Note: While the physical units are continuous, in many textbook contexts for this specific problem (Taha, etc.), production is treated as continuous. However, given the magnitude (10,000s), we will define variables as **Continuous** to allow for fractional units if necessary, or **Integer** if strict unit counts are required. Given the "units" language, **Integer** is safer for physical goods, but standard LP solvers often treat these as continuous. We will specify **Continuous** for mathematical tractability unless integer constraints are explicitly demanded, but note that with such large numbers, the LP relaxation is usually very close to the integer solution. Let's assume **Continuous** variables for standard LP formulation, as is common in production planning unless "whole units" is stressed. Actually, let's look at the costs. 10,000 units is large. Let's stick to **Continuous** to allow for a pure LP solution, which is standard for this type of aggregate planning problem. If the problem implies discrete units, the Code Agent can switch to MILP. I will specify **Continuous** but note the domain.*

**Re-evaluation of Variable Domain**: The problem asks for "units". In OR models of this scale, variables are typically continuous. I will define them as **Continuous** ($x \ge 0$).

---

## 1. Index Sets & Parameters

### Time Index
Let $t \in \{1, 2, ..., 12\}$ represent the months from January to December.
- $t=1$: Jan, $t=2$: Feb, ..., $t=12$: Dec.

### Product Index
Let $p \in \{1, 2\}$ represent Product I and Product II.

### Parameters

**1. Market Demand ($D_{p,t}$) [units/month]**
*Product I ($p=1$):*
- $D_{1,t} = 10,000$ for $t \in \{1, 2, 3, 4\}$ (Jan-Apr)
- $D_{1,t} = 30,000$ for $t \in \{5, 6, 7, 8, 9\}$ (May-Sep)
- $D_{1,t} = 100,000$ for $t \in \{10, 11, 12\}$ (Oct-Dec)

*Product II ($p=2$):*
- $D_{2,t} = 15,000$ for $t \in \{3, 4, 5, 6, 7, 8, 9\}$ (Mar-Sep)
- $D_{2,t} = 50,000$ for $t \in \{1, 2, 10, 11, 12\}$ (Jan, Feb, Oct, Nov, Dec)

**2. Production Costs ($C_{p,t}$) [yuan/unit]**
*Product I ($p=1$):*
- $C_{1,t} = 5.00$ for $t \in \{1, ..., 5\}$ (Jan-May)
- $C_{1,t} = 4.50$ for $t \in \{6, ..., 12\}$ (Jun-Dec)

*Product II ($p=2$):*
- $C_{2,t} = 8.00$ for $t \in \{1, ..., 5\}$ (Jan-May)
- $C_{2,t} = 7.00$ for $t \in \{6, ..., 12\}$ (Jun-Dec)

**3. Capacity & Volume Parameters**
- **Monthly Production Capacity**: $Cap_{prod} = 120,000$ units/month (Total for both products).
- **Volume per Unit**:
  - $v_1 = 0.2$ m³/unit (Product I)
  - $v_2 = 0.4$ m³/unit (Product II)
- **In-house Warehouse Capacity**: $W_{in} = 15,000$ m³.
- **In-house Storage Cost**: $h_{in} = 1.00$ yuan/m³/month.
- **External Storage Cost**: $h_{ext} = 1.50$ yuan/m³/month.
- **External Warehouse Capacity**: Assumed unbounded (or sufficiently large) as it is a rental option for overflow.

**4. Initial Inventory**
- $I_{p,0} = 0$ for all $p$ (Assume no starting inventory unless specified. Standard assumption for "determine schedule" problems starting from scratch).

---

## 2. Decision Variables

Let:
1.  $x_{p,t}$: Quantity of product $p$ produced in month $t$. ($x_{p,t} \ge 0$, Continuous)
2.  $I_{p,t}$: Total inventory of product $p$ at the **end** of month $t$. ($I_{p,t} \ge 0$, Continuous)
3.  $E_{p,t}$: Volume of product $p$ stored in **external** warehouse at the **end** of month $t$ (in m³). ($E_{p,t} \ge 0$, Continuous)
    *Note: We define external volume directly in m³ to simplify cost calculation. Alternatively, we can define external units. Let's use m³ for storage variables to match the cost rates.*
    *Let's refine: It is often cleaner to track inventory in **units** and split it into internal and external volumes.*
    
    Let:
    - $I_{p,t}$: Total units of product $p$ in inventory at end of month $t$.
    - $Vol_{p,t}^{in}$: Volume of product $p$ stored in **internal** warehouse at end of month $t$ (m³).
    - $Vol_{p,t}^{ext}$: Volume of product $p$ stored in **external** warehouse at end of month $t$ (m³).

    Constraints linking these:
    - $Vol_{p,t}^{in} + Vol_{p,t}^{ext} = I_{p,t} \times v_p$ (Total Volume = Units * Unit Volume)
    - $Vol_{p,t}^{in} \le W_{in, p}$? No, the warehouse is shared.
    - $\sum_{p} Vol_{p,t}^{in} \le W_{in}$ (Total internal volume constraint).

    So, final variable list:
    - $x_{p,t} \ge 0$ : Production of product $p$ in month $t$ (units).
    - $I_{p,t} \ge 0$ : Total units of product $p$ in stock at end of month $t$.
    - $V^{in}_{p,t} \ge 0$ : Volume of product $p$ in internal storage at end of month $t$ (m³).
    - $V^{ext}_{p,t} \ge 0$ : Volume of product $p$ in external storage at end of month $t$ (m³).

---

## 3. Objective Function

Minimize Total Cost = Total Production Cost + Total Storage Cost (Internal) + Total Storage Cost (External).

$$
\text{Minimize } Z = \sum_{t=1}^{12} \sum_{p=1}^{2} C_{p,t} x_{p,t} + \sum_{t=1}^{12} \sum_{p=1}^{2} \left( h_{in} V^{in}_{p,t} + h_{ext} V^{ext}_{p,t} \right)
$$

Substituting values:
$$
Z = \sum_{t=1}^{12} \sum_{p=1}^{2} C_{p,t} x_{p,t} + \sum_{t=1}^{12} \sum_{p=1}^{2} \left( 1.0 V^{in}_{p,t} + 1.5 V^{ext}_{p,t} \right)
$$

---

## 4. Operational Constraints

### A. Inventory Balance Constraints
For each product $p$ and month $t$:
$$
I_{p,t-1} + x_{p,t} - D_{p,t} = I_{p,t}
$$
With $I_{p,0} = 0$.
This ensures that beginning inventory plus production minus demand equals ending inventory.

### B. Volume Conservation Constraints
For each product $p$ and month $t$:
$$
V^{in}_{p,t} + V^{ext}_{p,t} = I_{p,t} \times v_p
$$
This links the unit-based inventory variable to the volume-based storage variables.

### C. Internal Warehouse Capacity Constraint
The total volume stored internally across all products must not exceed the in-house capacity.
$$
\sum_{p=1}^{2} V^{in}_{p,t} \le 15,000 \quad \forall t \in \{1, ..., 12\}
$$

### D. Monthly Production Capacity Constraint
The total units produced for all products in any given month must not exceed the factory capacity.
$$
\sum_{p=1}^{2} x_{p,t} \le 120,000 \quad \forall t \in \{1, ..., 12\}
$$

### E. Non-negativity Constraints
$$
x_{p,t} \ge 0, \quad I_{p,t} \ge 0, \quad V^{in}_{p,t} \ge 0, \quad V^{ext}_{p,t} \ge 0 \quad \forall p, t
$$

---

## 5. Feasibility Analysis for Part (a)

The problem asks to show that the original problem (without external storage) has no feasible solution.
In the original problem, the constraint is:
$$
\sum_{p=1}^{2} I_{p,t} v_p \le 15,000 \quad \forall t
$$
(Assuming all inventory must fit in the 15,000 m³ warehouse).

Let's check the cumulative demand vs. production capacity to see if inventory buildup is forced.
Total Demand for Product I:
$4 \times 10k + 5 \times 30k + 3 \times 100k = 40k + 150k + 300k = 490,000$ units.
Total Demand for Product II:
$5 \times 50k + 7 \times 15k = 250k + 105k = 355,000$ units.
Total Demand = 845,000 units.

Total Production Capacity over 12 months = $12 \times 120,000 = 1,440,000$ units.
Since Total Capacity > Total Demand, it is possible to produce everything. However, the *timing* matters.

Let's look at the peak demand months and the storage requirement.
In Oct, Nov, Dec, Demand for Product I is 100,000/month.
If we produce at max capacity 120,000/month, we can produce 120,000 of Product I in Oct.
However, look at May-Sep. Demand for P1 is 30,000. Demand for P2 is 15,000. Total demand is low.
We can produce up to 120,000.
Let's try to construct a feasible schedule for the *original* problem to see if it fails.

The constraint is $I_{1,t}(0.2) + I_{2,t}(0.4) \le 15,000$.
This implies $I_{1,t} + 2 I_{2,t} \le 75,000$ units equivalent.

Let's look at the end of September.
Cumulative Demand P1 (Jan-Sep) = $4(10k) + 5(30k) = 190,000$.
Cumulative Demand P2 (Jan-Sep) = $2(50k) + 5(15k) = 175,000$.
Total Cumulative Demand = 365,000.
Total Cumulative Capacity (Jan-Sep) = $9 \times 120,000 = 1,080,000$.
We have produced 365,000 + Inventory.
Actually, we don't *have* to produce more than demand. But we *can* produce more to save on costs?
Costs for P1: 5 (Jan-May), 4.5 (Jun-Dec). It is cheaper to produce in Jun-Dec.
Costs for P2: 8 (Jan-May), 7 (Jun-Dec). It is cheaper to produce in Jun-Dec.
So we prefer to produce in the second half of the year.

Let's look at the end of the year.
Total Demand P1 = 490,000.
Total Demand P2 = 355,000.
If we produce exactly what is demanded, inventory is 0.
Is it possible to meet demand without holding inventory?
In Oct, Demand P1 = 100,000.
If we produce 100,000 of P1 in Oct, we have 20,000 capacity left for P2.
Demand P2 in Oct = 50,000.
We cannot produce enough P2 in Oct to meet demand if we use 100,000 capacity for P1.
We must produce some P2 in Oct.
Let $x_{1,10} + x_{2,10} \le 120,000$.
If we want 0 inventory at end of Oct, $x_{1,10} = 100,000$ and $x_{2,10} = 50,000$.
Sum = 150,000 > 120,000. **Infeasible.**

Therefore, we MUST hold inventory of either P1 or P2 at the end of Oct (or earlier).
Specifically, the "unmet" production in Oct is 30,000 units (150k demand - 120k cap).
This 30,000 units must come from inventory built up in previous months (Jan-Sep).
Similarly for Nov and Dec.
Oct: Need 150k, Cap 120k -> Short 30k.
Nov: Need 150k, Cap 120k -> Short 30k.
Dec: Need 150k, Cap 120k -> Short 30k.
Total short in Q4 = 90,000 units.
These 90,000 units must be in inventory at the end of September.

Let's check the volume of this required inventory.
We have flexibility in *what* to hold in inventory (P1 or P2).
Let $I_{1,9}$ and $I_{2,9}$ be the inventory at end of Sep.
We need to cover the "deficit" in Q4.
The deficit in units is not fixed because we can shift production of P1 vs P2.
However, the total units produced in Q4 is $3 \times 120,000 = 360,000$.
Total demand in Q4 is $3 \times (100,000 + 50,000) = 450,000$.
So, total inventory at end of Sep must be at least $450,000 - 360,000 = 90,000$ units (in terms of total count, but weighted by product mix).
Actually, let $X_{Q4}$ be total production in Q4. $X_{Q4} \le 360,000$.
Let $D_{Q4} = 450,000$.
$I_{1,9} + I_{2,9} + X_{Q4} \ge D_{Q4}$ is not quite right because inventory is specific products.
Balance for P1: $I_{1,9} + x_{1,10} + x_{1,11} + x_{1,12} - (100k+100k+100k) = I_{1,12}$.
Balance for P2: $I_{2,9} + x_{2,10} + x_{2,11} + x_{2,12} - (50k+50k+50k) = I_{2,12}$.
Assume $I_{1,12}=I_{2,12}=0$ (no need to hold inventory after Dec).
Then $I_{1,9} = 300,000 - \sum_{t=10}^{12} x_{1,t}$.
And $I_{2,9} = 150,000 - \sum_{t=10}^{12} x_{2,t}$.
Sum of inventories at end of Sep:
$I_{1,9} + I_{2,9} = 450,000 - \sum_{t=10}^{12} (x_{1,t} + x_{2,t})$.
To minimize inventory volume, we maximize production in Q4.
Max $\sum (x_{1,t} + x_{2,t}) = 360,000$.
Min $I_{1,9} + I_{2,9} = 450,000 - 360,000 = 90,000$ units.

So, we must hold at least 90,000 *units* of combined inventory at end of September.
To minimize the *volume* of this inventory, we should hold the product with the smallest volume per unit.
Product I: 0.2 m³/unit.
Product II: 0.4 m³/unit.
It is more efficient to hold Product I in inventory.
Can we hold 90,000 units of Product I?
This would require $I_{1,9} = 90,000$ and $I_{2,9} = 0$.
Let's check if this is feasible with the production constraints in Q4.
If $I_{1,9} = 90,000$ and $I_{2,9} = 0$:
In Q4, we need to produce $x_{1,t}$ and $x_{2,t}$ such that:
$\sum x_{1,t} = 300,000 - 90,000 = 210,000$.
$\sum x_{2,t} = 150,000 - 0 = 150,000$.
Total production in Q4 = $210,000 + 150,000 = 360,000$.
This fits exactly in the capacity ($3 \times 120,000$).
So, we can schedule production in Q4 to consume exactly this inventory.
For example, in each month of Q4:
Produce 70,000 of P1 and 50,000 of P2. Total 120,000.
Check:
P1: Start 90k. Produce 70k*3=210k. Total avail 300k. Demand 300k. End 0. OK.
P2: Start 0. Produce 50k*3=150k. Total avail 150k. Demand 150k. End 0. OK.

So, the minimum required inventory at end of Sep is 90,000 units of Product I (if we optimize mix).
Volume = $90,000 \times 0.2 = 18,000$ m³.
The in-house warehouse capacity is 15,000 m³.
$18,000 > 15,000$.
Therefore, it is impossible to hold the minimum required inventory in the in-house warehouse.
Thus, the problem has **no feasible solution** without external storage.

### Part (b) Model Formulation

The model defined in sections 1-4 above is the correct formulation for part (b), where external storage allows the volume constraint to be relaxed for the portion exceeding 15,000 m³.

**Final Model Summary for Part (b):**

**Minimize:**
$$ Z = \sum_{t=1}^{12} \sum_{p=1}^{2} C_{p,t} x_{p,t} + \sum_{t=1}^{12} \sum_{p=1}^{2} (1.0 V^{in}_{p,t} + 1.5 V^{ext}_{p,t}) $$

**Subject to:**
1.  **Inventory Balance:**
    $$ I_{p,t} = I_{p,t-1} + x_{p,t} - D_{p,t}, \quad I_{p,0}=0, \quad \forall p, t $$
2.  **Volume Linkage:**
    $$ V^{in}_{p,t} + V^{ext}_{p,t} = I_{p,t} v_p, \quad \forall p, t $$
3.  **Internal Capacity:**
    $$ \sum_{p=1}^{2} V^{in}_{p,t} \le 15,000, \quad \forall t $$
4.  **Production Capacity:**
    $$ \sum_{p=1}^{2} x_{p,t} \le 120,000, \quad \forall t $$
5.  **Non-negativity:**
    $$ x_{p,t}, I_{p,t}, V^{in}_{p,t}, V^{ext}_{p,t} \ge 0 $$