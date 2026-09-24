### Model Type Declaration
**MILP (Mixed-Integer Linear Program)**

The problem involves production quantities which can be continuous (if we assume divisible units or large batches where integrality is negligible) or integer (if discrete physical units are strict). However, the presence of **fixed costs** for operating equipment implies that if a product is produced, a fixed cost is incurred. This introduces binary variables to determine whether the production line for a specific product is active. Therefore, the model is a Mixed-Integer Linear Program.

*Note: In many textbook contexts for this specific problem type (production planning with fixed costs), if the production volumes are expected to be large, continuous variables are often used for quantities $x_i$, but binary variables $y_i$ are strictly required to model the fixed cost logic correctly ($x_i > 0 \implies y_i = 1$).*

---

### Index Sets & Parameters

**Sets:**
- $P = \{1, 2, 3\}$: Set of products.
  - $1$: Shirt
  - $2$: T-shirt
  - $3$: Casual Wear

**Parameters:**
- $a_{1i}$: Labor requirement per unit for product $i$
  - $a_{11} = 3$ (Shirt)
  - $a_{12} = 2$ (T-shirt)
  - $a_{13} = 6$ (Casual Wear)
- $a_{2i}$: Material requirement per unit for product $i$
  - $a_{21} = 4$ (Shirt)
  - $a_{22} = 3$ (T-shirt)
  - $a_{23} = 6$ (Casual Wear)
- $p_i$: Selling price per unit for product $i$
  - $p_1 = 120$
  - $p_2 = 80$
  - $p_3 = 180$
- $c_{var, i}$: Variable cost per unit for product $i$
  - $c_{var, 1} = 60$
  - $c_{var, 2} = 40$
  - $c_{var, 3} = 80$
- $F_i$: Fixed cost per week for operating equipment for product $i$
  - $F_1 = 2000$
  - $F_2 = 1500$
  - $F_3 = 1000$
- $L_{avail}$: Total weekly available labor units
  - $L_{avail} = 150$
- $M_{avail}$: Total weekly available material units
  - $M_{avail} = 160$
- $U_i$: Upper bound on production for product $i$.
  - Since not explicitly provided, we can derive a theoretical upper bound based on resource constraints or set it to a large number $M$. However, for model completeness, let's determine a tight upper bound for each product based on the limiting resource to help the solver.
    - Shirt max by labor: $150/3 = 50$; by material: $160/4 = 40$. So $U_1 = 40$.
    - T-shirt max by labor: $150/2 = 75$; by material: $160/3 \approx 53.33$. So $U_2 = 53$ (if integer) or $53.33$ (if continuous). Let's use $U_2 = 53.33$ for continuous or just define $M$ as a large constant if integrality is not enforced. Given "production plan", discrete units are likely intended, but standard LP/MILP formulations often allow continuous $x$ with binary $y$. Let's assume **continuous** production quantities for simplicity unless specified otherwise, but the binary structure remains. If integer production is required, $x_i \in \mathbb{Z}^+$. Let's assume **Continuous** for now as is common in initial LP/MILP setups, but note that $x_i$ must be bounded by $U_i$ for the Big-M constraint. Let $U_i$ be the max possible production of product $i$ if produced exclusively.
      - $U_1 = \min(150/3, 160/4) = 40$
      - $U_2 = \min(150/2, 160/3) = 53.33...$
      - $U_3 = \min(150/6, 160/6) = 25$

**Derived Parameter:**
- $\pi_i$: Profit per unit (contribution margin) for product $i$
  - $\pi_1 = 120 - 60 = 60$
  - $\pi_2 = 80 - 40 = 40$
  - $\pi_3 = 180 - 80 = 100$

---

### Decision Variables

- $x_i$: Quantity of product $i$ produced per week.
  - Domain: $x_i \ge 0$ (Continuous) or $x_i \in \mathbb{Z}^+$ (Integer).
  - *Note: The problem asks for a "production plan". In industrial contexts, shirts are discrete. However, without explicit "integer" instruction, standard OR textbook problems of this type often treat $x$ as continuous to allow for linear programming solvers, or explicitly state MILP. Given the fixed costs, it is an **MILP** if $x$ is integer, or a **Mixed-Integer Linear Program** if $x$ is continuous and $y$ is binary. Let's define $x_i$ as **Continuous** for the main formulation, but the binary variables make it a MILP. If the user requires integer units, the domain changes to $\mathbb{Z}^+$. I will provide the formulation with $x_i \ge 0$ (continuous) as it is the more general case for "plan design" unless "units" implies indivisibility. Actually, "shirts" are clearly discrete. I will specify **$x_i \in \mathbb{Z}^+$** to be safe, making it a pure **MILP** (if we consider binary as integer) or **Mixed-Integer**. Let's stick to **$x_i \ge 0$** continuous for the mathematical clarity of the LP relaxation, but note that in practice $x_i$ would be integer. *Correction*: Standard practice for "production plan" with small numbers (like 150 labor) usually implies integer units. I will define **$x_i \ge 0$, continuous** for the primary model structure, but explicitly state that if discrete units are required, $x_i \in \mathbb{Z}^+$. The binary variables $y_i$ are the critical discrete elements for the fixed costs.

- $y_i$: Binary variable indicating whether product $i$ is produced.
  - $y_i = 1$ if product line $i$ is active (production occurs).
  - $y_i = 0$ if product line $i$ is inactive (no production).
  - Domain: $y_i \in \{0, 1\}$ for all $i \in P$.

---

### Objective Function

Maximize total weekly profit $Z$.
Profit = (Total Revenue - Total Variable Cost) - Total Fixed Cost.

$$
\text{Maximize } Z = \sum_{i=1}^{3} (\pi_i x_i - F_i y_i)
$$

Substituting values:
$$
\text{Maximize } Z = 60x_1 + 40x_2 + 100x_3 - 2000y_1 - 1500y_2 - 1000y_3
$$

---

### Operational Constraints

**1. Resource Constraints (Labor and Material)**
Total labor used must not exceed available labor.
Total material used must not exceed available material.

$$
\sum_{i=1}^{3} a_{1i} x_i \le L_{avail} \implies 3x_1 + 2x_2 + 6x_3 \le 150
$$

$$
\sum_{i=1}^{3} a_{2i} x_i \le M_{avail} \implies 4x_1 + 3x_2 + 6x_3 \le 160
$$

**2. Linking Constraints (Fixed Cost Activation)**
If a product is produced ($x_i > 0$), the fixed cost must be incurred ($y_i = 1$). If no product is produced, $y_i$ can be 0. This is modeled using the Big-M method.
$x_i \le U_i y_i$ for all $i \in P$, where $U_i$ is an upper bound on $x_i$.

Using the derived upper bounds $U_1=40, U_2=53.33, U_3=25$ (or simply a large number $M$ if bounds are not tight, but tight bounds help solvers):

$$
x_1 \le 40 y_1
$$
$$
x_2 \le 53.33 y_2 \quad (\text{or } x_2 \le 54 y_2 \text{ if integer})
$$
$$
x_3 \le 25 y_3
$$

*Note: If $x_i$ are continuous, using 53.33 is precise. If $x_i$ are integers, 53 is the max integer quantity possible for T-shirts alone, so $x_2 \le 53 y_2$.*

**3. Non-negativity and Domain Constraints**

$$
x_i \ge 0 \quad \forall i \in \{1, 2, 3\}
$$
(Or $x_i \in \mathbb{Z}^+$ if integer production is required)

$$
y_i \in \{0, 1\} \quad \forall i \in \{1, 2, 3\}
$$

---

### Feasibility Sanity Check

Let's check if it's possible to produce all three.
Max labor for all: $3(40) + 2(53.33) + 6(25) = 120 + 106.66 + 150 = 376.66 > 150$. Infeasible to produce max of all.
The constraints will naturally restrict the combination.

Check if any single product is feasible with its fixed cost:
- Shirt: Max 40 units. Profit from variable = $40 \times 60 = 2400$. Fixed = 2000. Net = 400. Feasible.
- T-shirt: Max 53.33 units. Profit from variable = $53.33 \times 40 = 2133.2$. Fixed = 1500. Net = 633.2. Feasible.
- Casual: Max 25 units. Profit from variable = $25 \times 100 = 2500$. Fixed = 1000. Net = 1500. Feasible.

It is likely optimal to produce a mix or a subset. The model correctly captures the trade-off between variable profit and fixed cost entry barriers.

### Final Model Summary

**Model Type:** MILP (assuming integer units for shirts) or Mixed-Integer Linear Program (if continuous quantities allowed). Given the context of "shirts", **Integer** production is physically realistic. I will present the model with **$x_i \in \mathbb{Z}^+$** as the primary interpretation for a "production plan" of discrete goods, but the structure holds for continuous $x_i$ as well.

**Sets:**
$P = \{1, 2, 3\}$ corresponding to Shirt, T-shirt, Casual Wear.

**Parameters:**
- $a_{1} = [3, 2, 6]$ (Labor)
- $a_{2} = [4, 3, 6]$ (Material)
- $p = [120, 80, 180]$ (Price)
- $c = [60, 40, 80]$ (Variable Cost)
- $F = [2000, 1500, 1000]$ (Fixed Cost)
- $L_{avail} = 150$
- $M_{avail} = 160$
- $\pi = [60, 40, 100]$ (Unit Profit)
- $U = [40, 53, 25]$ (Upper bounds for Big-M, using integer maxes)

**Variables:**
- $x_i \in \mathbb{Z}^+$ for $i=1,2,3$ (Production quantity)
- $y_i \in \{0, 1\}$ for $i=1,2,3$ (Production activation)

**Objective:**
$$ \text{Max } Z = 60x_1 + 40x_2 + 100x_3 - 2000y_1 - 1500y_2 - 1000y_3 $$

**Constraints:**
1. $3x_1 + 2x_2 + 6x_3 \le 150$
2. $4x_1 + 3x_2 + 6x_3 \le 160$
3. $x_1 \le 40 y_1$
4. $x_2 \le 53 y_2$
5. $x_3 \le 25 y_3$
6. $x_i \ge 0, \text{ integer}$
7. $y_i \in \{0, 1\}$