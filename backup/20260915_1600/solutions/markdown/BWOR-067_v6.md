Based on the problem description, we need to formulate a Non-Linear Programming (NLP) model to minimize the total cost, which includes convex production costs and linear inventory holding costs.

### 1. MANDATORY COST INVENTORY
*   **Production Cost Rate**: The cost is $x^2$ per month, where $x$ is the quantity produced. This is a non-linear term in the objective function.
*   **Inventory Holding Cost**: 1 yuan per unit per month. This applies to the ending inventory of each month.
*   **Demand**: $d_1 = 100$, $d_2 = 110$, $d_3 = 120$.
*   **Initial/Final Inventory**: $s_0 = 0$, $s_3 = 0$.

### 2. MODEL FORMULATION

**Model Type:** NON-LINEAR (QP - Quadratic Programming, specifically a convex Quadratic Program due to the $x^2$ terms).

#### Index Sets & Parameters
*   **Set $T$**: Set of months, $T = \{1, 2, 3\}$.
*   **Parameter $d_t$**: Demand for month $t$.
    *   $d_1 = 100$
    *   $d_2 = 110$
    *   $d_3 = 120$
*   **Parameter $h$**: Holding cost per unit per month.
    *   $h = 1$
*   **Parameter $s_0$**: Initial inventory.
    *   $s_0 = 0$

#### Decision Variables
*   $x_t$: Quantity of Product A produced in month $t$ for $t \in \{1, 2, 3\}$.
    *   Domain: $x_t \ge 0$ (Continuous, as production quantities can be continuous in this context unless specified as discrete units; given the quadratic cost, it is treated as a continuous variable).
*   $s_t$: Inventory level at the end of month $t$ for $t \in \{1, 2, 3\}$.
    *   Domain: $s_t \ge 0$ (Continuous).

#### Objective Function
Minimize the total cost, which is the sum of production costs and inventory holding costs over the 3 months.
$$ \text{Minimize } Z = \sum_{t=1}^{3} \left( x_t^2 + h \cdot s_t \right) $$
Substituting $h=1$:
$$ \text{Minimize } Z = x_1^2 + x_2^2 + x_3^2 + s_1 + s_2 + s_3 $$

#### Operational Constraints
1.  **Inventory Balance Constraints**:
    The inventory at the end of month $t$ equals the inventory at the beginning of month $t$ (which is $s_{t-1}$) plus production in month $t$ ($x_t$) minus demand in month $t$ ($d_t$).
    
    *   For $t=1$:
        $$ s_1 = s_0 + x_1 - d_1 $$
        $$ s_1 = 0 + x_1 - 100 \implies x_1 - s_1 = 100 $$
        
    *   For $t=2$:
        $$ s_2 = s_1 + x_2 - d_2 $$
        $$ s_2 = s_1 + x_2 - 110 \implies x_2 - s_2 + s_1 = 110 $$
        
    *   For $t=3$:
        $$ s_3 = s_2 + x_3 - d_3 $$
        Given $s_3 = 0$:
        $$ 0 = s_2 + x_3 - 120 \implies x_3 - s_2 = 120 $$

2.  **Non-negativity Constraints**:
    $$ x_t \ge 0, \quad \forall t \in \{1, 2, 3\} $$
    $$ s_t \ge 0, \quad \forall t \in \{1, 2, 3\} $$

*(Note: The constraint $s_3=0$ is incorporated directly into the third balance equation. The constraint $s_0=0$ is incorporated into the first balance equation.)*

### SUMMARY OF THE MATHEMATICAL MODEL

**Objective:**
$$ \min Z = x_1^2 + x_2^2 + x_3^2 + s_1 + s_2 + s_3 $$

**Subject to:**
1.  $x_1 - s_1 = 100$
2.  $x_2 - s_2 + s_1 = 110$
3.  $x_3 - s_2 = 120$
4.  $x_1, x_2, x_3 \ge 0$
5.  $s_1, s_2, s_3 \ge 0$

This is a convex Quadratic Programming problem. A non-linear solver (or a specialized QP solver) is required to find the optimal production quantities $x_1, x_2, x_3$.