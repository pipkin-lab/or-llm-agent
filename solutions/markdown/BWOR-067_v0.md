## Model Type Declaration
**Model Type:** QP (Quadratic Program)
*Note: The production cost function $x^2$ is convex and non-linear. A non-linear solver (e.g., `scipy.optimize`, Gurobi, CPLEX) is required.*

## Index Sets & Parameters

**Index Sets:**
- $t$: Set of months, $t \in \{1, 2, 3\}$

**Parameters:**
- $d_t$: Demand in month $t$
  - $d_1 = 100$
  - $d_2 = 110$
  - $d_3 = 120$
- $h$: Inventory holding cost per unit per month
  - $h = 1$ yuan
- $s_0$: Initial inventory at the beginning of month 1
  - $s_0 = 0$
- $s_3$: Required ending inventory at the end of month 3
  - $s_3 = 0$

## Decision Variables

- $x_t$: Quantity of Product A produced in month $t$.
  - Domain: $x_t \in \mathbb{R}_{\ge 0}$ for $t \in \{1, 2, 3\}$
- $s_t$: Inventory level at the end of month $t$.
  - Domain: $s_t \in \mathbb{R}_{\ge 0}$ for $t \in \{1, 2, 3\}$

## Objective Function

Minimize the total cost, which is the sum of production costs and inventory holding costs over the 3-month horizon.

$$ \text{Minimize } Z = \sum_{t=1}^{3} \left( x_t^2 + h \cdot s_t \right) $$

Substituting $h=1$:
$$ Z = x_1^2 + x_2^2 + x_3^2 + s_1 + s_2 + s_3 $$

**Unit & Magnitude Verification:**
- Costs are in Yuan.
- The objective sums production costs (Yuan) and holding costs (Yuan).
- No normalization is required as the question asks for the production quantities, and the objective is the standard total cost.

## Operational Constraints

**1. Inventory Balance Constraints**
For each month $t$, the ending inventory is the beginning inventory plus production minus demand.
Beginning inventory of month $t$ is the ending inventory of month $t-1$ ($s_{t-1}$).

- **Month 1:**
  $$ s_1 = s_0 + x_1 - d_1 $$
  $$ s_1 = 0 + x_1 - 100 $$
  $$ s_1 = x_1 - 100 $$

- **Month 2:**
  $$ s_2 = s_1 + x_2 - d_2 $$
  $$ s_2 = s_1 + x_2 - 110 $$

- **Month 3:**
  $$ s_3 = s_2 + x_3 - d_3 $$
  $$ s_3 = s_2 + x_3 - 120 $$

**2. Terminal Inventory Constraint**
The problem specifies the ending inventory at the end of the third month is 0.
$$ s_3 = 0 $$
*(Note: This is already enforced by the balance equation for Month 3 combined with the parameter $s_3=0$, but it is explicitly stated here for clarity. Substituting $s_3=0$ into the Month 3 balance gives: $0 = s_2 + x_3 - 120$).*

**3. Non-negativity Constraints**
Production and inventory levels cannot be negative.
$$ x_t \ge 0, \quad \forall t \in \{1, 2, 3\} $$
$$ s_t \ge 0, \quad \forall t \in \{1, 2, 3\} $$

### Final Formulation Summary

**Minimize:**
$$ Z = x_1^2 + x_2^2 + x_3^2 + s_1 + s_2 + s_3 $$

**Subject to:**
1. $s_1 - x_1 = -100$
2. $s_2 - s_1 - x_2 = -110$
3. $s_3 - s_2 - x_3 = -120$
4. $s_3 = 0$
5. $x_1, x_2, x_3, s_1, s_2, s_3 \ge 0$