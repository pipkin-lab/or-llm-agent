To formulate this production planning problem, we must account for the fixed costs associated with producing each product. Since fixed costs are incurred only if a product is produced (i.e., production quantity > 0), this is a Mixed Integer Linear Programming (MILP) problem.

### Model Type Declaration
**Model Type:** MILP (Mixed Integer Linear Programming)

### 1. Index Sets & Parameters

**Index Sets:**
*   $P = \{1, 2, 3\}$: Set of products (I, II, III).
*   $R = \{A, B, C\}$: Set of resources.

**Parameters (extracted from Table 5-6):**

*   $a_{rp}$: Unit consumption of resource $r$ for product $p$.
    *   $a_{A,1}=2, a_{A,2}=4, a_{A,3}=8$
    *   $a_{B,1}=2, a_{B,2}=3, a_{B,3}=4$
    *   $a_{C,1}=1, a_{C,2}=2, a_{C,3}=3$
*   $R_r$: Available amount of resource $r$.
    *   $R_A=500, R_B=300, R_C=100$
*   $v_p$: Variable cost per unit for product $p$.
    *   $v_1=4, v_2=5, v_3=6$
*   $F_p$: Fixed cost for organizing production of product $p$.
    *   $F_1=100, F_2=150, F_3=200$
*   $s_p$: Selling price per unit for product $p$.
    *   $s_1=8, s_2=10, s_3=12$

**Derived Parameter:**
*   $m_p = s_p - v_p$: Contribution margin per unit for product $p$.
    *   $m_1 = 8 - 4 = 4$
    *   $m_2 = 10 - 5 = 5$
    *   $m_3 = 12 - 6 = 6$

### 2. Decision Variables

*   $x_p$: Continuous variable representing the quantity of product $p$ produced.
    *   Domain: $x_p \ge 0, \quad \forall p \in P$
*   $y_p$: Binary variable indicating whether product $p$ is produced.
    *   Domain: $y_p \in \{0, 1\}, \quad \forall p \in P$
    *   $y_p = 1$ if $x_p > 0$, $y_p = 0$ if $x_p = 0$.

### 3. Objective Function

Maximize total profit, which is the total contribution margin minus total fixed costs.

$$ \text{Maximize } Z = \sum_{p \in P} m_p x_p - \sum_{p \in P} F_p y_p $$

Substituting values:
$$ Z = 4x_1 + 5x_2 + 6x_3 - 100y_1 - 150y_2 - 200y_3 $$

### 4. Operational Constraints

**1. Resource Availability Constraints:**
The total consumption of each resource must not exceed the available amount.

*   Resource A:
    $$ 2x_1 + 4x_2 + 8x_3 \le 500 $$
*   Resource B:
    $$ 2x_1 + 3x_2 + 4x_3 \le 300 $$
*   Resource C:
    $$ 1x_1 + 2x_2 + 3x_3 \le 100 $$

**2. Linking Constraints (Fixed Cost Logic):**
If a product is produced ($x_p > 0$), the binary variable $y_p$ must be 1. If $y_p = 0$, then $x_p$ must be 0. We use the "Big-M" method. We need an upper bound $U_p$ for $x_p$ to link $x_p$ and $y_p$.

Let's determine a tight upper bound $U_p$ for each product based on the most restrictive resource constraint alone (ignoring other products for the bound, which is valid for Big-M).
*   For Product 1:
    *   Limit by A: $2x_1 \le 500 \Rightarrow x_1 \le 250$
    *   Limit by B: $2x_1 \le 300 \Rightarrow x_1 \le 150$
    *   Limit by C: $1x_1 \le 100 \Rightarrow x_1 \le 100$
    *   So, $U_1 = 100$.
*   For Product 2:
    *   Limit by A: $4x_2 \le 500 \Rightarrow x_2 \le 125$
    *   Limit by B: $3x_2 \le 300 \Rightarrow x_2 \le 100$
    *   Limit by C: $2x_2 \le 100 \Rightarrow x_2 \le 50$
    *   So, $U_2 = 50$.
*   For Product 3:
    *   Limit by A: $8x_3 \le 500 \Rightarrow x_3 \le 62.5$
    *   Limit by B: $4x_3 \le 300 \Rightarrow x_3 \le 75$
    *   Limit by C: $3x_3 \le 100 \Rightarrow x_3 \le 33.33...$
    *   So, $U_3 = 33.33$ (or simply use 33.34 to be safe, or keep it as fraction $100/3$). Let's use $U_3 = 33.34$.

Linking constraints:
$$ x_1 \le 100 y_1 $$
$$ x_2 \le 50 y_2 $$
$$ x_3 \le 33.34 y_3 $$

*(Note: Using tighter bounds improves solver performance. The bounds derived above are valid individual maxima.)*

### Final Model Summary

**Model Type:** MILP

**Maximize:**
$$ Z = 4x_1 + 5x_2 + 6x_3 - 100y_1 - 150y_2 - 200y_3 $$

**Subject to:**

**Resource Constraints:**
1.  $2x_1 + 4x_2 + 8x_3 \le 500$
2.  $2x_1 + 3x_2 + 4x_3 \le 300$
3.  $x_1 + 2x_2 + 3x_3 \le 100$

**Linking Constraints:**
4.  $x_1 \le 100 y_1$
5.  $x_2 \le 50 y_2$
6.  $x_3 \le 33.34 y_3$

**Variable Domains:**
*   $x_1, x_2, x_3 \ge 0$ (Continuous)
*   $y_1, y_2, y_3 \in \{0, 1\}$ (Binary)