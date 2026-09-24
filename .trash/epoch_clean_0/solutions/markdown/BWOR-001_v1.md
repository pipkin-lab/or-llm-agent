Based on the problem description and the data provided in Table 1-17, here is the formal Linear Programming (LP) model.

### 1. Index Sets & Parameters

**Sets:**
*   $R = \{A, B, C\}$: Set of raw materials.
*   $P = \{X, Y, Z\}$: Set of candy brands (products).

**Parameters:**

*   **Raw Material Costs ($c_r$):** Cost per kg of raw material $r$.
    *   $c_A = 2.00$
    *   $c_B = 1.50$
    *   $c_C = 1.00$
*   **Monthly Usage Limits ($U_r$):** Maximum available kg of raw material $r$.
    *   $U_A = 2000$
    *   $U_B = 2500$
    *   $U_C = 1200$
*   **Processing Costs ($p_p$):** Cost per kg of processing product $p$.
    *   $p_X = 0.50$
    *   $p_Y = 0.40$
    *   $p_Z = 0.30$
*   **Selling Prices ($s_p$):** Revenue per kg of product $p$.
    *   $s_X = 3.40$
    *   $s_Y = 2.85$
    *   $s_Z = 2.25$
*   **Composition Requirements:**
    *   Let $l_{r,p}$ be the lower bound percentage of material $r$ in product $p$.
    *   Let $u_{r,p}$ be the upper bound percentage of material $r$ in product $p$.
    *   If a cell is blank in the table, it implies no specific bound is explicitly stated for that ratio, but the sum of all material proportions must equal 100%. However, looking closely at the table:
        *   **Brand X:** $A \geq 60\%$, $C \leq 20\%$. Since $A+B+C=100\%$, and $A \geq 0.6, C \leq 0.2$, then $B = 1 - A - C$. The constraint $B \geq 0$ implies $A+C \leq 1$.
        *   **Brand Y:** $A \geq 30\%$, $C \leq 50\%$.
        *   **Brand Z:** $C \leq 60\%$. There are no explicit lower bounds for A or B in Z other than non-negativity, and no upper bounds for A or B other than implied by the sum being 100%. Note: The table has blank cells for A and B in Brand Z. This means the only explicit constraint on Z's composition is $C \leq 60\%$. The remaining $40\%$ can be any mix of A and B.

### 2. Decision Variables

Since the composition of the raw materials within each brand can vary (they are not fixed, only bounded), we need variables representing the amount of each raw material used in each brand.

Let $x_{r,p}$ be the amount (in kg) of raw material $r$ used in the production of brand $p$ per month.

*   $x_{A,X}, x_{B,X}, x_{C,X} \geq 0$
*   $x_{A,Y}, x_{B,Y}, x_{C,Y} \geq 0$
*   $x_{A,Z}, x_{B,Z}, x_{C,Z} \geq 0$

Alternatively, to make the model more compact, we can define:
*   $x_p$ = Total kg of brand $p$ produced.
*   $y_{r,p}$ = Fraction (proportion) of raw material $r$ in brand $p$.
*   Then the actual usage is $x_{r,p} = y_{r,p} \cdot x_p$.

However, because the objective function is linear in terms of total material usage, it is often easier to work directly with the mass variables $x_{r,p}$ to avoid non-linear products ($y \cdot x$). Let's stick to **mass variables** $x_{r,p}$ as they are linear.

**Decision Variables:**
$x_{r,p} \in \mathbb{R}^+$ for all $r \in R, p \in P$.
Specifically:
*   $x_{A,X}, x_{B,X}, x_{C,X}$
*   $x_{A,Y}, x_{B,Y}, x_{C,Y}$
*   $x_{A,Z}, x_{B,Z}, x_{C,Z}$

### 3. Objective Function

The goal is to **maximize profit**.
Profit = Total Revenue - Total Raw Material Cost - Total Processing Cost.

Total Revenue for brand $p$ = Selling Price $\times$ Total Mass of Brand $p$.
Total Mass of Brand $p$ = $\sum_{r \in R} x_{r,p}$.

Total Raw Material Cost = $\sum_{p \in P} \sum_{r \in R} c_r \cdot x_{r,p}$.

Total Processing Cost = $\sum_{p \in P} p_p \cdot (\text{Total Mass of Brand } p) = \sum_{p \in P} p_p \left( \sum_{r \in R} x_{r,p} \right)$.

Let's combine the cost terms for a single unit of material $r$ in product $p$.
The cost incurred for using $x_{r,p}$ kg of material $r$ in product $p$ is $c_r \cdot x_{r,p}$.
The revenue generated is distributed over the total mass. It is cleaner to group by product mass.

Let $M_p = \sum_{r \in R} x_{r,p}$ be the total production of brand $p$.

$$ \text{Maximize } Z = \sum_{p \in P} \left[ s_p \cdot M_p - p_p \cdot M_p - \sum_{r \in R} c_r x_{r,p} \right] $$

Substituting $M_p = \sum_{r \in R} x_{r,p}$:

$$ Z = \sum_{p \in P} \left[ (s_p - p_p) \sum_{r \in R} x_{r,p} - \sum_{r \in R} c_r x_{r,p} \right] $$

$$ Z = \sum_{p \in P} \sum_{r \in R} (s_p - p_p - c_r) x_{r,p} $$

Let's calculate the coefficient for each $x_{r,p}$:

**Brand X ($s_X=3.40, p_X=0.50 \Rightarrow s_X - p_X = 2.90$):**
*   $x_{A,X}$: $2.90 - c_A = 2.90 - 2.00 = 0.90$
*   $x_{B,X}$: $2.90 - c_B = 2.90 - 1.50 = 1.40$
*   $x_{C,X}$: $2.90 - c_C = 2.90 - 1.00 = 1.90$

**Brand Y ($s_Y=2.85, p_Y=0.40 \Rightarrow s_Y - p_Y = 2.45$):**
*   $x_{A,Y}$: $2.45 - c_A = 2.45 - 2.00 = 0.45$
*   $x_{B,Y}$: $2.45 - c_B = 2.45 - 1.50 = 0.95$
*   $x_{C,Y}$: $2.45 - c_C = 2.45 - 1.00 = 1.45$

**Brand Z ($s_Z=2.25, p_Z=0.30 \Rightarrow s_Z - p_Z = 1.95$):**
*   $x_{A,Z}$: $1.95 - c_A = 1.95 - 2.00 = -0.05$
*   $x_{B,Z}$: $1.95 - c_B = 1.95 - 1.50 = 0.45$
*   $x_{C,Z}$: $1.95 - c_C = 1.95 - 1.00 = 0.95$

**Objective Function:**
$$ \text{Maximize } Z = 0.90 x_{A,X} + 1.40 x_{B,X} + 1.90 x_{C,X} + 0.45 x_{A,Y} + 0.95 x_{B,Y} + 1.45 x_{C,Y} - 0.05 x_{A,Z} + 0.45 x_{B,Z} + 0.95 x_{C,Z} $$

### 4. Operational Constraints

**A. Raw Material Usage Limits (Supply Constraints)**
The total usage of each raw material across all brands cannot exceed the monthly limit.

1.  **Material A:**
    $$ x_{A,X} + x_{A,Y} + x_{A,Z} \leq 2000 $$
2.  **Material B:**
    $$ x_{B,X} + x_{B,Y} + x_{B,Z} \leq 2500 $$
3.  **Material C:**
    $$ x_{C,X} + x_{C,Y} + x_{C,Z} \leq 1200 $$

**B. Composition Constraints**
These constraints ensure the proportion of each raw material in each brand meets the requirements. We express ratios as linear inequalities by multiplying both sides by the total mass of the brand ($M_p = \sum_{r} x_{r,p}$).

*Note: Since $x_{r,p} \geq 0$, $M_p \geq 0$. If $M_p=0$, the constraints are trivially satisfied or undefined, but in LP formulations, these are standard linear inequalities derived from $a \cdot x_r \leq b \cdot M_p$.*

**Brand X Constraints:**
*   $A \geq 60\% \Rightarrow x_{A,X} \geq 0.60 (x_{A,X} + x_{B,X} + x_{C,X})$
    $$ 0.40 x_{A,X} - 0.60 x_{B,X} - 0.60 x_{C,X} \geq 0 \quad \text{(or } 2x_{A,X} \geq 3x_{B,X} + 3x_{C,X} \text{)} $$
*   $C \leq 20\% \Rightarrow x_{C,X} \leq 0.20 (x_{A,X} + x_{B,X} + x_{C,X})$
    $$ -0.20 x_{A,X} - 0.20 x_{B,X} + 0.80 x_{C,X} \leq 0 \quad \text{(or } x_{C,X} \leq 0.25 x_{A,X} + 0.25 x_{B,X} \text{)} $$
*   (Implicit: $B \geq 0$ is handled by variable bounds. $A+C \leq 100\%$ is implied by $B \geq 0$).

**Brand Y Constraints:**
*   $A \geq 30\% \Rightarrow x_{A,Y} \geq 0.30 (x_{A,Y} + x_{B,Y} + x_{C,Y})$
    $$ 0.70 x_{A,Y} - 0.30 x_{B,Y} - 0.30 x_{C,Y} \geq 0 \quad \text{(or } 7x_{A,Y} \geq 3x_{B,Y} + 3x_{C,Y} \text{)} $$
*   $C \leq 50\% \Rightarrow x_{C,Y} \leq 0.50 (x_{A,Y} + x_{B,Y} + x_{C,Y})$
    $$ -0.50 x_{A,Y} - 0.50 x_{B,Y} + 0.50 x_{C,Y} \leq 0 \quad \text{(or } x_{C,Y} \leq x_{A,Y} + x_{B,Y} \text{)} $$

**Brand Z Constraints:**
*   $C \leq 60\% \Rightarrow x_{C,Z} \leq 0.60 (x_{A,Z} + x_{B,Z} + x_{C,Z})$
    $$ -0.60 x_{A,Z} - 0.60 x_{B,Z} + 0.40 x_{C,Z} \leq 0 \quad \text{(or } 2x_{C,Z} \leq 3x_{A,Z} + 3x_{B,Z} \text{)} $$
*   No other explicit bounds on A or B proportions for Z.

**C. Non-negativity Constraints**
$$ x_{r,p} \geq 0 \quad \forall r \in R, p \in P $$

---

### Summary of the Linear Programming Model

**Maximize:**
$$ Z = 0.90 x_{A,X} + 1.40 x_{B,X} + 1.90 x_{C,X} + 0.45 x_{A,Y} + 0.95 x_{B,Y} + 1.45 x_{C,Y} - 0.05 x_{A,Z} + 0.45 x_{B,Z} + 0.95 x_{C,Z} $$

**Subject to:**

**1. Material Supply:**
$$ x_{A,X} + x_{A,Y} + x_{A,Z} \leq 2000 $$
$$ x_{B,X} + x_{B,Y} + x_{B,Z} \leq 2500 $$
$$ x_{C,X} + x_{C,Y} + x_{C,Z} \leq 1200 $$

**2. Composition Ratios:**
*(Brand X)*
$$ 2x_{A,X} - 3x_{B,X} - 3x_{C,X} \geq 0 $$
$$ x_{C,X} - 0.25x_{A,X} - 0.25x_{B,X} \leq 0 $$

*(Brand Y)*
$$ 7x_{A,Y} - 3x_{B,Y} - 3x_{C,Y} \geq 0 $$
$$ x_{C,Y} - x_{A,Y} - x_{B,Y} \leq 0 $$

*(Brand Z)*
$$ 2x_{C,Z} - 3x_{A,Z} - 3x_{B,Z} \leq 0 $$

**3. Non-negativity:**
$$ x_{A,X}, x_{B,X}, x_{C,X}, x_{A,Y}, x_{B,Y}, x_{C,Y}, x_{A,Z}, x_{B,Z}, x_{C,Z} \geq 0 $$