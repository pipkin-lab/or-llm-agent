# Model Type: LP (Linear Programming)

## Index Sets & Parameters

**Sets:**
- $P = \{I, II, III\}$: Set of products.
- $A = \{A_1, A_2\}$: Set of machines for Stage A.
- $B = \{B_1, B_2, B_3\}$: Set of machines for Stage B.

**Parameters (from Table 1-18):**

*Processing Times (hours/unit):*
- $t_{p,m}^A$: Time to process product $p$ on machine $m \in A$ (blank/undefined if not allowed).
  - Product I: $t_{I,A_1}^A = 5$, $t_{I,A_2}^A = 7$
  - Product II: $t_{II,A_1}^A = 10$, $t_{II,A_2}^A = 9$
  - Product III: $t_{III,A_2}^A = 12$ (Only $A_2$ allowed)
  
- $t_{p,m}^B$: Time to process product $p$ on machine $m \in B$ (blank/undefined if not allowed).
  - Product I: $t_{I,B_1}^B = 6$, $t_{I,B_2}^B = 4$, $t_{I,B_3}^B = 7$
  - Product II: $t_{II,B_1}^B = 8$ (Only $B_1$ allowed)
  - Product III: $t_{III,B_2}^B = 11$ (Only $B_2$ allowed)

*Machine Capacities (hours):*
- $H_{A_1} = 6000$
- $H_{A_2} = 10000$
- $H_{B_1} = 4000$
- $H_{B_2} = 7000$
- $H_{B_3} = 4000$

*Processing Costs (dollars/hour):*
- $c_{A_1} = 0.05$
- $c_{A_2} = 0.03$
- $c_{B_1} = 0.06$
- $c_{B_2} = 0.11$
- $c_{B_3} = 0.05$

*Raw Material Costs (dollars/unit):*
- $r_I = 0.25$
- $r_{II} = 0.35$
- $r_{III} = 0.50$

*Selling Prices (dollars/unit):*
- $s_I = 1.25$
- $s_{II} = 2.00$
- $s_{III} = 2.80$

## Decision Variables

Let $x_{p,m}^A$ be the quantity of product $p$ processed on machine $m$ in Stage A.
Let $x_{p,m}^B$ be the quantity of product $p$ processed on machine $m$ in Stage B.

**Domains:**
- $x_{I,A_1}^A, x_{I,A_2}^A \ge 0$
- $x_{II,A_1}^A, x_{II,A_2}^A \ge 0$
- $x_{III,A_2}^A \ge 0$
- $x_{I,B_1}^B, x_{I,B_2}^B, x_{I,B_3}^B \ge 0$
- $x_{II,B_1}^B \ge 0$
- $x_{III,B_2}^B \ge 0$
- All other $x$ variables are implicitly 0 (excluded from model).

*Note: Since a unit of product must pass through both Stage A and Stage B to be sold, we define the total production quantity of product $p$ as $Q_p$. The flow balance requires that the amount processed in Stage A equals the amount processed in Stage B for each product.*

## Objective Function

Maximize Total Profit ($Z$):
$$ Z = \sum_{p \in P} \left( s_p Q_p - r_p Q_p - \sum_{m \in A} c_m t_{p,m}^A x_{p,m}^A - \sum_{m \in B} c_m t_{p,m}^B x_{p,m}^B \right) $$

Substituting the specific variables and parameters:

$$
\begin{aligned}
\text{Max } Z = & \quad (1.25 - 0.25)Q_I - (0.05 \cdot 5)x_{I,A_1}^A - (0.03 \cdot 7)x_{I,A_2}^A - (0.06 \cdot 6)x_{I,B_1}^B - (0.11 \cdot 4)x_{I,B_2}^B - (0.05 \cdot 7)x_{I,B_3}^B \\
&+ (2.00 - 0.35)Q_{II} - (0.05 \cdot 10)x_{II,A_1}^A - (0.03 \cdot 9)x_{II,A_2}^A - (0.06 \cdot 8)x_{II,B_1}^B \\
&+ (2.80 - 0.50)Q_{III} - (0.03 \cdot 12)x_{III,A_2}^A - (0.11 \cdot 11)x_{III,B_2}^B
\end{aligned}
$$

Simplifying coefficients:
- Product I Contribution: $1.00 Q_I - 0.25 x_{I,A_1}^A - 0.21 x_{I,A_2}^A - 0.36 x_{I,B_1}^B - 0.44 x_{I,B_2}^B - 0.35 x_{I,B_3}^B$
- Product II Contribution: $1.65 Q_{II} - 0.50 x_{II,A_1}^A - 0.27 x_{II,A_2}^A - 0.48 x_{II,B_1}^B$
- Product III Contribution: $2.30 Q_{III} - 0.36 x_{III,A_2}^A - 1.21 x_{III,B_2}^B$

## Operational Constraints

**1. Flow Balance Constraints (Production Consistency)**
The total quantity of each product processed in Stage A must equal the total quantity processed in Stage B (and equals the total sold quantity $Q_p$).

For Product I:
$$ x_{I,A_1}^A + x_{I,A_2}^A = Q_I $$
$$ x_{I,B_1}^B + x_{I,B_2}^B + x_{I,B_3}^B = Q_I $$
*(Implies: $x_{I,A_1}^A + x_{I,A_2}^A = x_{I,B_1}^B + x_{I,B_2}^B + x_{I,B_3}^B$)*

For Product II:
$$ x_{II,A_1}^A + x_{II,A_2}^A = Q_{II} $$
$$ x_{II,B_1}^B = Q_{II} $$
*(Implies: $x_{II,A_1}^A + x_{II,A_2}^A = x_{II,B_1}^B$)*

For Product III:
$$ x_{III,A_2}^A = Q_{III} $$
$$ x_{III,B_2}^B = Q_{III} $$
*(Implies: $x_{III,A_2}^A = x_{III,B_2}^B$)*

**2. Machine Capacity Constraints**
Total processing time on each machine cannot exceed available hours.

Stage A:
- Machine $A_1$: $5 x_{I,A_1}^A + 10 x_{II,A_1}^A \le 6000$
- Machine $A_2$: $7 x_{I,A_2}^A + 9 x_{II,A_2}^A + 12 x_{III,A_2}^A \le 10000$

Stage B:
- Machine $B_1$: $6 x_{I,B_1}^B + 8 x_{II,B_1}^B \le 4000$
- Machine $B_2$: $4 x_{I,B_2}^B + 11 x_{III,B_2}^B \le 7000$
- Machine $B_3$: $7 x_{I,B_3}^B \le 4000$

**3. Non-negativity Constraints**
$$ x_{p,m}^A \ge 0, \quad x_{p,m}^B \ge 0, \quad Q_p \ge 0 \quad \forall p \in P, m \in \{A,B\} $$