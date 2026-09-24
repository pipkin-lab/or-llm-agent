## Model Type Declaration
**Model Type:** LP (Linear Programming)

All decision variables are continuous (production quantities can be fractional in the general formulation, though integer constraints could be added if discrete units are required; the problem does not specify integrality, so we assume continuous for standard LP). The objective and all constraints are linear.

---

## Index Sets & Parameters

### Sets
- $P = \{I, II, III\}$: Set of products.
- $A = \{A_1, A_2\}$: Set of Stage A machines.
- $B = \{B_1, B_2, B_3\}$: Set of Stage B machines.
- $M = A \cup B$: Set of all machines.

### Parameters (from Table 1-18)

**Processing time per unit (hours):** $t_{m,p}$
- $t_{A_1, I} = 5$, $t_{A_1, II} = 10$, $t_{A_1, III} = \infty$ (not allowed)
- $t_{A_2, I} = 7$, $t_{A_2, II} = 9$, $t_{A_2, III} = 12$
- $t_{B_1, I} = 6$, $t_{B_1, II} = 8$, $t_{B_1, III} = \infty$ (not allowed)
- $t_{B_2, I} = 4$, $t_{B_2, II} = \infty$ (not allowed), $t_{B_2, III} = 11$
- $t_{B_3, I} = 7$, $t_{B_3, II} = \infty$ (not allowed), $t_{B_3, III} = \infty$ (not allowed)

**Available machine hours:** $H_m$
- $H_{A_1} = 6000$, $H_{A_2} = 10000$
- $H_{B_1} = 4000$, $H_{B_2} = 7000$, $H_{B_3} = 4000$

**Machine processing cost (dollars/hour):** $c_m$
- $c_{A_1} = 0.05$, $c_{A_2} = 0.03$
- $c_{B_1} = 0.06$, $c_{B_2} = 0.11$, $c_{B_3} = 0.05$

**Raw material cost (dollars/unit):** $r_p$
- $r_I = 0.25$, $r_{II} = 0.35$, $r_{III} = 0.50$

**Selling price (dollars/unit):** $s_p$
- $s_I = 1.25$, $s_{II} = 2.00$, $s_{III} = 2.80$

### Derived Parameters: Variable Processing Cost per Unit
For each product $p$ and machine $m$, the processing cost per unit is:
$$\text{procCost}_{m,p} = t_{m,p} \cdot c_m$$

Computing these:
- **Stage A:**
  - $A_1$: Product I: $5 \times 0.05 = 0.25$; Product II: $10 \times 0.05 = 0.50$
  - $A_2$: Product I: $7 \times 0.03 = 0.21$; Product II: $9 \times 0.03 = 0.27$; Product III: $12 \times 0.03 = 0.36$
- **Stage B:**
  - $B_1$: Product I: $6 \times 0.06 = 0.36$; Product II: $8 \times 0.06 = 0.48$
  - $B_2$: Product I: $4 \times 0.11 = 0.44$; Product III: $11 \times 0.11 = 1.21$
  - $B_3$: Product I: $7 \times 0.05 = 0.35$

---

## Decision Variables

Let $x_{a,b,p}$ be the number of units of product $p$ processed on machine $a \in A$ for Stage A and machine $b \in B$ for Stage B.

**Domain:** $x_{a,b,p} \geq 0$ (continuous) for all valid combinations where both $t_{a,p}$ and $t_{b,p}$ are finite.

Valid variable indices (only where both stages are allowed):
- Product I: All 6 combinations: $(A_1,B_1), (A_1,B_2), (A_1,B_3), (A_2,B_1), (A_2,B_2), (A_2,B_3)$
- Product II: $a \in \{A_1, A_2\}$, $b = B_1$ only → 2 combinations: $(A_1,B_1), (A_2,B_1)$
- Product III: $a = A_2$, $b = B_2$ only → 1 combination: $(A_2,B_2)$

Total: 9 decision variables.

For clarity, let us define:
- $x_{11}^I, x_{12}^I, x_{13}^I$ : Product I on $(A_1, B_1), (A_1, B_2), (A_1, B_3)$
- $x_{21}^I, x_{22}^I, x_{23}^I$ : Product I on $(A_2, B_1), (A_2, B_2), (A_2, B_3)$
- $x_{11}^{II}, x_{21}^{II}$ : Product II on $(A_1, B_1), (A_2, B_1)$
- $x_{22}^{III}$ : Product III on $(A_2, B_2)$

All variables $\geq 0$.

---

## Objective Function

**Maximize Total Profit = Total Revenue − Total Processing Costs − Total Raw Material Costs**

For each unit of product $p$ routed through $(a,b)$, the profit contribution is:
$$\pi_{a,b,p} = s_p - r_p - t_{a,p} \cdot c_a - t_{b,p} \cdot c_b$$

Computing profit per unit for each valid route:

**Product I** ($s_I = 1.25, r_I = 0.25$):
- $(A_1, B_1)$: $1.25 - 0.25 - 0.25 - 0.36 = 0.39$
- $(A_1, B_2)$: $1.25 - 0.25 - 0.25 - 0.44 = 0.31$
- $(A_1, B_3)$: $1.25 - 0.25 - 0.25 - 0.35 = 0.40$
- $(A_2, B_1)$: $1.25 - 0.25 - 0.21 - 0.36 = 0.43$
- $(A_2, B_2)$: $1.25 - 0.25 - 0.21 - 0.44 = 0.35$
- $(A_2, B_3)$: $1.25 - 0.25 - 0.21 - 0.35 = 0.44$

**Product II** ($s_{II} = 2.00, r_{II} = 0.35$):
- $(A_1, B_1)$: $2.00 - 0.35 - 0.50 - 0.48 = 0.67$
- $(A_2, B_1)$: $2.00 - 0.35 - 0.27 - 0.48 = 0.90$

**Product III** ($s_{III} = 2.80, r_{III} = 0.50$):
- $(A_2, B_2)$: $2.80 - 0.50 - 0.36 - 1.21 = 0.73$

**Objective:**
$$\max Z = 0.39 x_{11}^I + 0.31 x_{12}^I + 0.40 x_{13}^I + 0.43 x_{21}^I + 0.35 x_{22}^I + 0.44 x_{23}^I + 0.67 x_{11}^{II} + 0.90 x_{21}^{II} + 0.73 x_{22}^{III}$$

---

## Operational Constraints

### Machine Capacity Constraints

**Stage A – Machine $A_1$** (available: 6000 h):
$$5 x_{11}^I + 10 x_{11}^{II} \leq 6000$$

**Stage A – Machine $A_2$** (available: 10000 h):
$$7 x_{21}^I + 9 x_{21}^{II} + 12 x_{22}^{III} \leq 10000$$

**Stage B – Machine $B_1$** (available: 4000 h):
$$6 x_{11}^I + 8 x_{11}^{II} \leq 4000$$

**Stage B – Machine $B_2$** (available: 7000 h):
$$4 x_{12}^I + 11 x_{22}^{III} \leq 7000$$

**Stage B – Machine $B_3$** (available: 4000 h):
$$7 x_{13}^I \leq 4000$$

### Non-negativity Constraints
$$x_{11}^I, x_{12}^I, x_{13}^I, x_{21}^I, x_{22}^I, x_{23}^I, x_{11}^{II}, x_{21}^{II}, x_{22}^{III} \geq 0$$

---

## Feasibility Sanity Check

- Total Stage A capacity: $6000 + 10000 = 16000$ hours.
- Total Stage B capacity: $4000 + 7000 + 4000 = 15000$ hours.
- All profit margins are positive, so the model will produce positive quantities.
- No supply/demand balance issues — this is a pure production planning problem with no external demand constraints, only capacity constraints. The model is feasible (e.g., all-zero solution is feasible, and positive production levels are achievable within capacities).