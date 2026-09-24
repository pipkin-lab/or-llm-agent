Here is the linear programming model for the candy factory production problem.

### 1. Index Sets & Parameters

**Sets:**
*   $R = \{A, B, C\}$: Set of raw materials.
*   $P = \{X, Y, Z\}$: Set of candy brands (products).

**Parameters:**
*   $c_r$: Cost of raw material $r$ per kg.
    *   $c_A = 2.00$, $c_B = 1.50$, $c_C = 1.00$.
*   $M_r$: Monthly usage limit (supply) of raw material $r$ (kg).
    *   $M_A = 2000$, $M_B = 2500$, $M_C = 1200$.
*   $p_j$: Selling price of brand $j$ per kg.
    *   $p_X = 3.40$, $p_Y = 2.85$, $p_Z = 2.25$.
*   $q_j$: Processing cost of brand $j$ per kg.
    *   $q_X = 0.50$, $q_Y = 0.40$, $q_Z = 0.30$.

**Composition Constraints (Proportions):**
Let $x_{r,j}$ be the amount of material $r$ used in brand $j$.
Let $X_j$ be the total production of brand $j$.

*   **Brand X ($j=X$):**
    *   Material A: $\geq 60\%$ of $X_X$
    *   Material C: $\leq 20\%$ of $X_X$
    *   *Implied Material B:* Since A and C have bounds, B fills the rest. Note that the table leaves B blank for X, implying no specific constraint on B other than non-negativity and the balance equation, but typically in these problems, if A and C are constrained, B is the remainder. However, looking at the table structure:
        *   Row A: $\ge 60\%$ for X.
        *   Row C: $\le 20\%$ for X.
        *   Row B: Blank for X.
        *   This implies $x_{A,X} \ge 0.60 X_X$ and $x_{C,X} \le 0.20 X_X$.
        *   Since $x_{A,X} + x_{B,X} + x_{C,X} = X_X$, the constraint on B is implicit.

*   **Brand Y ($j=Y$):**
    *   Material A: $\geq 30\%$ of $X_Y$
    *   Material C: $\leq 50\%$ of $X_Y$
    *   *Implied Material B:* Remainder.

*   **Brand Z ($j=Z$):**
    *   Material C: $\leq 60\%$ of $X_Z$
    *   *Implied Materials A and B:* The table leaves A and B blank for Z. Usually, this means there are **no** specific minimum or maximum percentage constraints on A and B for Z, other than non-negativity and the sum constraint.

### 2. Decision Variables

To handle the composition ratios linearly, we define the decision variables as the specific amounts of each raw material used in each product.

*   $x_{r,j}$: Amount (kg) of raw material $r$ used to produce brand $j$.
    *   Domain: $x_{r,j} \ge 0$ for all $r \in R, j \in P$.

*(Note: We could also define total production $X_j$ as a variable, but it is redundant as $X_j = \sum_{r} x_{r,j}$. Defining $x_{r,j}$ directly allows us to write the ratio constraints as linear inequalities involving the sum.)*

### 3. Objective Function

**Goal:** Maximize Profit.

Profit = Total Revenue - Total Raw Material Cost - Total Processing Cost.

Total Revenue:
$$ \sum_{j \in P} p_j \left( \sum_{r \in R} x_{r,j} \right) $$

Total Raw Material Cost:
$$ \sum_{r \in R} c_r \left( \sum_{j \in P} x_{r,j} \right) $$

Total Processing Cost:
$$ \sum_{j \in P} q_j \left( \sum_{r \in R} x_{r,j} \right) $$

**Maximize $Z$:**
$$ Z = \sum_{j \in P} \sum_{r \in R} \left( p_j - q_j - c_r \right) x_{r,j} $$

Let's calculate the coefficients $(p_j - q_j - c_r)$ for each term:

*   **For Brand X ($p_X=3.40, q_X=0.50$):**
    *   Term for A: $3.40 - 0.50 - 2.00 = 0.90$
    *   Term for B: $3.40 - 0.50 - 1.50 = 1.40$
    *   Term for C: $3.40 - 0.50 - 1.00 = 1.90$

*   **For Brand Y ($p_Y=2.85, q_Y=0.40$):**
    *   Term for A: $2.85 - 0.40 - 2.00 = 0.45$
    *   Term for B: $2.85 - 0.40 - 1.50 = 0.95$
    *   Term for C: $2.85 - 0.40 - 1.00 = 1.45$

*   **For Brand Z ($p_Z=2.25, q_Z=0.30$):**
    *   Term for A: $2.25 - 0.30 - 2.00 = -0.05$
    *   Term for B: $2.25 - 0.30 - 1.50 = 0.45$
    *   Term for C: $2.25 - 0.30 - 1.00 = 0.95$

**Objective Function:**
$$ \text{Maximize } Z = 0.90 x_{A,X} + 1.40 x_{B,X} + 1.90 x_{C,X} + 0.45 x_{A,Y} + 0.95 x_{B,Y} + 1.45 x_{C,Y} - 0.05 x_{A,Z} + 0.45 x_{B,Z} + 0.95 x_{C,Z} $$

### 4. Operational Constraints

**1. Raw Material Supply Constraints:**
The total amount of each raw material used across all brands cannot exceed the monthly limit.

*   Material A:
    $$ x_{A,X} + x_{A,Y} + x_{A,Z} \le 2000 $$
*   Material B:
    $$ x_{B,X} + x_{B,Y} + x_{B,Z} \le 2500 $$
*   Material C:
    $$ x_{C,X} + x_{C,Y} + x_{C,Z} \le 1200 $$

**2. Composition (Ratio) Constraints:**
These constraints ensure the specific brand requirements. We express percentages as fractions of the total production of that brand ($\sum_r x_{r,j}$).

*   **Brand X:**
    *   $A \ge 60\%$:
        $$ x_{A,X} \ge 0.60 (x_{A,X} + x_{B,X} + x_{C,X}) $$
        $$ \Rightarrow 0.40 x_{A,X} - 0.60 x_{B,X} - 0.60 x_{C,X} \ge 0 $$
    *   $C \le 20\%$:
        $$ x_{C,X} \le 0.20 (x_{A,X} + x_{B,X} + x_{C,X}) $$
        $$ \Rightarrow -0.20 x_{A,X} - 0.20 x_{B,X} + 0.80 x_{C,X} \le 0 $$

*   **Brand Y:**
    *   $A \ge 30\%$:
        $$ x_{A,Y} \ge 0.30 (x_{A,Y} + x_{B,Y} + x_{C,Y}) $$
        $$ \Rightarrow 0.70 x_{A,Y} - 0.30 x_{B,Y} - 0.30 x_{C,Y} \ge 0 $$
    *   $C \le 50\%$:
        $$ x_{C,Y} \le 0.50 (x_{A,Y} + x_{B,Y} + x_{C,Y}) $$
        $$ \Rightarrow -0.50 x_{A,Y} - 0.50 x_{B,Y} + 0.50 x_{C,Y} \le 0 $$

*   **Brand Z:**
    *   $C \le 60\%$:
        $$ x_{C,Z} \le 0.60 (x_{A,Z} + x_{B,Z} + x_{C,Z}) $$
        $$ \Rightarrow -0.60 x_{A,Z} - 0.60 x_{B,Z} + 0.40 x_{C,Z} \le 0 $$
    *   *(No other explicit ratio constraints for Z in the table)*.

**3. Non-negativity Constraints:**
$$ x_{r,j} \ge 0 \quad \forall r \in \{A,B,C\}, j \in \{X,Y,Z\} $$

### Summary of the Model

**Variables:**
$x_{A,X}, x_{B,X}, x_{C,X}, x_{A,Y}, x_{B,Y}, x_{C,Y}, x_{A,Z}, x_{B,Z}, x_{C,Z} \ge 0$

**Maximize:**
$$ Z = 0.90 x_{A,X} + 1.40 x_{B,X} + 1.90 x_{C,X} + 0.45 x_{A,Y} + 0.95 x_{B,Y} + 1.45 x_{C,Y} - 0.05 x_{A,Z} + 0.45 x_{B,Z} + 0.95 x_{C,Z} $$

**Subject to:**
1.  $x_{A,X} + x_{A,Y} + x_{A,Z} \le 2000$
2.  $x_{B,X} + x_{B,Y} + x_{B,Z} \le 2500$
3.  $x_{C,X} + x_{C,Y} + x_{C,Z} \le 1200$
4.  $0.40 x_{A,X} - 0.60 x_{B,X} - 0.60 x_{C,X} \ge 0$
5.  $-0.20 x_{A,X} - 0.20 x_{B,X} + 0.80 x_{C,X} \le 0$
6.  $0.70 x_{A,Y} - 0.30 x_{B,Y} - 0.30 x_{C,Y} \ge 0$
7.  $-0.50 x_{A,Y} - 0.50 x_{B,Y} + 0.50 x_{C,Y} \le 0$
8.  $-0.60 x_{A,Z} - 0.60 x_{B,Z} + 0.40 x_{C,Z} \le 0$