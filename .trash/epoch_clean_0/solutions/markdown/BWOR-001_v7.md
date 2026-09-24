### 1. Index Sets & Parameters

**Index Sets:**
*   $I = \{A, B, C\}$: Set of raw materials.
*   $J = \{X, Y, Z\}$: Set of candy brands.

**Parameters:**
*   $c_i$: Unit cost of raw material $i$ (dollars/kg).
    *   $c_A = 2.00$
    *   $c_B = 1.50$
    *   $c_C = 1.00$
*   $L_i$: Monthly usage limit for raw material $i$ (kg).
    *   $L_A = 2000$
    *   $L_B = 2500$
    *   $L_C = 1200$
*   $p_j$: Selling price per kg of brand $j$ (dollars/kg).
    *   $p_X = 3.40$
    *   $p_Y = 2.85$
    *   $p_Z = 2.25$
*   $q_j$: Unit processing cost for brand $j$ (dollars/kg).
    *   $q_X = 0.50$
    *   $q_Y = 0.40$
    *   $q_Z = 0.30$

**Derived Parameters (Unit Contribution Margin):**
*   $m_j = p_j - q_j$: Contribution margin before raw material costs.
    *   $m_X = 3.40 - 0.50 = 2.90$
    *   $m_Y = 2.85 - 0.40 = 2.45$
    *   $m_Z = 2.25 - 0.30 = 1.95$

**Composition Constraints (Proportions):**
*   **Brand X:**
    *   Min proportion of A: $0.60$
    *   Max proportion of C: $0.20$
    *   *Implicit:* Since $A \ge 0.60$ and $C \le 0.20$, the remaining component is B. The minimum proportion of B is $1 - 0.60 - 0.20 = 0.20$ (if A is maxed at some point? No, A is min, C is max).
    *   Actually, let's look at the table structure carefully.
        *   Row A: X has $\ge 60\%$.
        *   Row C: X has $\le 20\%$.
        *   This implies the rest is B. So $B_X \ge 1 - 0.60 - 0.20 = 0.20$ is not strictly fixed, but $A_X + B_X + C_X = 1$.
        *   Constraint 1: $A_X \ge 0.60$
        *   Constraint 2: $C_X \le 0.20$
        *   Constraint 3: $B_X = 1 - A_X - C_X$. Since $A_X \ge 0.60$ and $C_X \le 0.20$, the minimum $B_X$ occurs when $A_X$ is max and $C_X$ is min? No, we don't have explicit max for A or min for C. However, typically in these problems, if only one bound is given for a component, the others are determined by the sum.
        *   Let's check Brand Y:
            *   Row A: Y has $\ge 30\%$.
            *   Row C: Y has $\le 50\%$.
            *   Implicitly, B is the remainder.
        *   Let's check Brand Z:
            *   Row C: Z has $\le 60\%$.
            *   The table has empty cells for A and B for Brand Z. Usually, this implies there are **no specific proportion constraints** on A and B for Brand Z, other than non-negativity and summing to 1. Or, it might imply that the *only* constraint is on C. Let's assume standard interpretation: Only the explicitly listed percentages are constraints.
            *   Wait, looking at the table again:
                *   Row A: X ($\ge 60\%$), Y ($\ge 30\%$), Z (Empty)
                *   Row B: X (Empty), Y (Empty), Z (Empty)
                *   Row C: X ($\le 20\%$), Y ($\le 50\%$), Z ($\le 60\%$)
            *   This implies:
                *   For X: $A_X \ge 0.60$, $C_X \le 0.20$.
                *   For Y: $A_Y \ge 0.30$, $C_Y \le 0.50$.
                *   For Z: $C_Z \le 0.60$. (No explicit constraints on $A_Z$ or $B_Z$ other than non-negativity).

### 2. Decision Variables

Let $x_{ij}$ be the amount (kg) of raw material $i$ used in the production of brand $j$.

*   $x_{AX}, x_{BX}, x_{CX}$: kg of materials A, B, C in Brand X.
*   $x_{AY}, x_{BY}, x_{CY}$: kg of materials A, B, C in Brand Y.
*   $x_{AZ}, x_{BZ}, x_{CZ}$: kg of materials A, B, C in Brand Z.

**Domains:**
$x_{ij} \ge 0$ for all $i \in I, j \in J$.

*Note on Total Production:*
Let $P_j$ be the total kg of brand $j$ produced.
$P_X = x_{AX} + x_{BX} + x_{CX}$
$P_Y = x_{AY} + x_{BY} + x_{CY}$
$P_Z = x_{AZ} + x_{BZ} + x_{CZ}$

### 3. Objective Function

Maximize total profit $Z$.
Profit = (Total Revenue) - (Total Raw Material Cost) - (Total Processing Cost)

$$
\text{Maximize } Z = \sum_{j \in J} \left( p_j P_j - q_j P_j \right) - \sum_{i \in I} c_i \left( \sum_{j \in J} x_{ij} \right)
$$

Substituting $P_j$ with the sum of ingredients:
$$
Z = 3.40(x_{AX}+x_{BX}+x_{CX}) - 2.00 x_{AX} - 1.50 x_{BX} - 1.00 x_{CX} - 0.50(x_{AX}+x_{BX}+x_{CX})
+ 2.85(x_{AY}+x_{BY}+x_{CY}) - 2.00 x_{AY} - 1.50 x_{BY} - 1.00 x_{CY} - 0.40(x_{AY}+x_{BY}+x_{CY})
+ 2.25(x_{AZ}+x_{BZ}+x_{CZ}) - 2.00 x_{AZ} - 1.50 x_{BZ} - 1.00 x_{CZ} - 0.30(x_{AZ}+x_{BZ}+x_{CZ})
$$

Simplifying coefficients for each variable $x_{ij}$:
Coefficient = $p_j - q_j - c_i$

*   **Brand X:**
    *   $x_{AX}: 3.40 - 0.50 - 2.00 = 0.90$
    *   $x_{BX}: 3.40 - 0.50 - 1.50 = 1.40$
    *   $x_{CX}: 3.40 - 0.50 - 1.00 = 1.90$
*   **Brand Y:**
    *   $x_{AY}: 2.85 - 0.40 - 2.00 = 0.45$
    *   $x_{BY}: 2.85 - 0.40 - 1.50 = 0.95$
    *   $x_{CY}: 2.85 - 0.40 - 1.00 = 1.45$
*   **Brand Z:**
    *   $x_{AZ}: 2.25 - 0.30 - 2.00 = -0.05$
    *   $x_{BZ}: 2.25 - 0.30 - 1.50 = 0.45$
    *   $x_{CZ}: 2.25 - 0.30 - 1.00 = 0.95$

**Objective Function:**
$$
\text{Maximize } Z = 0.90 x_{AX} + 1.40 x_{BX} + 1.90 x_{CX} + 0.45 x_{AY} + 0.95 x_{BY} + 1.45 x_{CY} - 0.05 x_{AZ} + 0.45 x_{BZ} + 0.95 x_{CZ}
$$

### 4. Operational Constraints

**1. Raw Material Availability Constraints:**
The total usage of each raw material across all brands cannot exceed the monthly limit.

*   Material A:
    $$ x_{AX} + x_{AY} + x_{AZ} \le 2000 $$
*   Material B:
    $$ x_{BX} + x_{BY} + x_{BZ} \le 2500 $$
*   Material C:
    $$ x_{CX} + x_{CY} + x_{CZ} \le 1200 $$

**2. Product Composition Constraints:**
These constraints define the proportions of ingredients within each brand. We express them as linear inequalities using the total production volume $P_j$.

*   **Brand X ($P_X = x_{AX} + x_{BX} + x_{CX}$):**
    *   $A_X \ge 60\% \Rightarrow x_{AX} \ge 0.60 P_X$
        $$ x_{AX} \ge 0.60 (x_{AX} + x_{BX} + x_{CX}) \Rightarrow 0.40 x_{AX} - 0.60 x_{BX} - 0.60 x_{CX} \ge 0 $$
        Or more simply:
        $$ x_{AX} - 0.60 x_{BX} - 0.60 x_{CX} \ge 0 \quad (\text{divided by } 0.6? \text{ No, just linear form}) $$
        Let's keep it simple:
        $$ x_{AX} \ge 0.60 x_{AX} + 0.60 x_{BX} + 0.60 x_{CX} $$
        $$ 0.40 x_{AX} - 0.60 x_{BX} - 0.60 x_{CX} \ge 0 $$
    *   $C_X \le 20\% \Rightarrow x_{CX} \le 0.20 P_X$
        $$ x_{CX} \le 0.20 (x_{AX} + x_{BX} + x_{CX}) $$
        $$ 0.80 x_{CX} - 0.20 x_{AX} - 0.20 x_{BX} \le 0 $$
        Or:
        $$ -0.20 x_{AX} - 0.20 x_{BX} + 0.80 x_{CX} \le 0 $$

*   **Brand Y ($P_Y = x_{AY} + x_{BY} + x_{CY}$):**
    *   $A_Y \ge 30\% \Rightarrow x_{AY} \ge 0.30 P_Y$
        $$ x_{AY} \ge 0.30 (x_{AY} + x_{BY} + x_{CY}) $$
        $$ 0.70 x_{AY} - 0.30 x_{BY} - 0.30 x_{CY} \ge 0 $$
    *   $C_Y \le 50\% \Rightarrow x_{CY} \le 0.50 P_Y$
        $$ x_{CY} \le 0.50 (x_{AY} + x_{BY} + x_{CY}) $$
        $$ 0.50 x_{CY} - 0.50 x_{AY} - 0.50 x_{BY} \le 0 $$
        Or:
        $$ -0.50 x_{AY} - 0.50 x_{BY} + 0.50 x_{CY} \le 0 $$

*   **Brand Z ($P_Z = x_{AZ} + x_{BZ} + x_{CZ}$):**
    *   $C_Z \le 60\% \Rightarrow x_{CZ} \le 0.60 P_Z$
        $$ x_{CZ} \le 0.60 (x_{AZ} + x_{BZ} + x_{CZ}) $$
        $$ 0.40 x_{CZ} - 0.60 x_{AZ} - 0.60 x_{BZ} \le 0 $$
        Or:
        $$ -0.60 x_{AZ} - 0.60 x_{BZ} + 0.40 x_{CZ} \le 0 $$

**3. Non-negativity Constraints:**
$$ x_{ij} \ge 0 \quad \forall i \in \{A,B,C\}, j \in \{X,Y,Z\} $$

---

### Summary of the Linear Programming Model

**Variables:**
$x_{AX}, x_{BX}, x_{CX}, x_{AY}, x_{BY}, x_{CY}, x_{AZ}, x_{BZ}, x_{CZ} \ge 0$

**Objective:**
$$
\begin{aligned}
\text{Maximize } Z = \;& 0.90 x_{AX} + 1.40 x_{BX} + 1.90 x_{CX} \\
& + 0.45 x_{AY} + 0.95 x_{BY} + 1.45 x_{CY} \\
& - 0.05 x_{AZ} + 0.45 x_{BZ} + 0.95 x_{CZ}
\end{aligned}
$$

**Subject to:**

**Material Limits:**
1.  $x_{AX} + x_{AY} + x_{AZ} \le 2000$
2.  $x_{BX} + x_{BY} + x_{BZ} \le 2500$
3.  $x_{CX} + x_{CY} + x_{CZ} \le 1200$

**Composition Constraints:**
4.  $0.40 x_{AX} - 0.60 x_{BX} - 0.60 x_{CX} \ge 0$  (X: A $\ge$ 60%)
5.  $-0.20 x_{AX} - 0.20 x_{BX} + 0.80 x_{CX} \le 0$  (X: C $\le$ 20%)
6.  $0.70 x_{AY} - 0.30 x_{BY} - 0.30 x_{CY} \ge 0$  (Y: A $\ge$ 30%)
7.  $-0.50 x_{AY} - 0.50 x_{BY} + 0.50 x_{CY} \le 0$  (Y: C $\le$ 50%)
8.  $-0.60 x_{AZ} - 0.60 x_{BZ} + 0.40 x_{CZ} \le 0$  (Z: C $\le$ 60%)