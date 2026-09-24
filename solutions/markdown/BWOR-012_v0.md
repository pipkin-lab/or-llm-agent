**Model Type:** LP (Linear Programming)

### 1. Index Sets & Parameters

**Index Sets:**
- $G = \{1, 2, 3\}$: Set of base liquor grades (I, II, III).
- $B = \{R, Y, B\}$: Set of branded products (Red, Yellow, Blue).

**Parameters:**

*Base Liquor (Grade) Data:*
- $S_g$: Daily supply limit of grade $g$ (kg).
  - $S_1 = 1500$
  - $S_2 = 2000$
  - $S_3 = 1000$
- $C_g$: Cost per kg of grade $g$ (Yuan/kg).
  - $C_1 = 6.0$
  - $C_2 = 4.5$
  - $C_3 = 3.0$

*Branded Product (Brand) Data:*
- $P_b$: Selling price per kg of brand $b$ (Yuan/kg).
  - $P_R = 5.5$
  - $P_Y = 5.0$
  - $P_B = 4.8$
- $MinQty_R$: Minimum daily production requirement for Red brand (kg).
  - $MinQty_R = 2000$

*Blending Constraints (Percentages converted to decimals):*
For each brand $b$, let $L_{g,b}^{max}$ be the maximum fraction of grade $g$, and $L_{g,b}^{min}$ be the minimum fraction of grade $g$.

**Red ($b=R$):**
- Grade I: $> 50\% \implies L_{1,R}^{min} = 0.50$
- Grade III: $< 10\% \implies L_{3,R}^{max} = 0.10$
- Grade II: No explicit bound (implied by sum to 1).

**Yellow ($b=Y$):**
- Grade I: $> 20\% \implies L_{1,Y}^{min} = 0.20$
- Grade III: $< 70\% \implies L_{3,Y}^{max} = 0.70$
- Grade II: No explicit bound.

**Blue ($b=B$):**
- Grade I: $> 10\% \implies L_{1,B}^{min} = 0.10$
- Grade III: $< 50\% \implies L_{3,B}^{max} = 0.50$
- Grade II: No explicit bound.

*(Note: Strict inequalities $<$ and $>$ in physical blending problems are mathematically treated as $\le$ and $\ge$ in LP formulations, as the difference is infinitesimal and does not affect the optimal integer or continuous solution in practical terms, and LP solvers require closed sets.)*

### 2. Decision Variables

Let $x_{g,b}$ be the amount (in kg) of base liquor grade $g$ used in brand $b$ per day.
- **Domain:** $x_{g,b} \ge 0, \quad \forall g \in G, \forall b \in B$.

### 3. Objective Function

Maximize total profit $Z$.
Profit = Total Revenue - Total Cost.

$$
\text{Maximize } Z = \sum_{b \in B} \left( P_b \sum_{g \in G} x_{g,b} \right) - \sum_{g \in G} \left( C_g \sum_{b \in B} x_{g,b} \right)
$$

Expanding the coefficients for clarity (Revenue Coeff - Cost Coeff):

$$
\begin{aligned}
Z = & (5.5 - 6.0)x_{1,R} + (5.5 - 4.5)x_{2,R} + (5.5 - 3.0)x_{3,R} \\
& + (5.0 - 6.0)x_{1,Y} + (5.0 - 4.5)x_{2,Y} + (5.0 - 3.0)x_{3,Y} \\
& + (4.8 - 6.0)x_{1,B} + (4.8 - 4.5)x_{2,B} + (4.8 - 3.0)x_{3,B}
\end{aligned}
$$

Simplified:
$$
Z = -0.5 x_{1,R} + 1.0 x_{2,R} + 2.5 x_{3,R} - 1.0 x_{1,Y} + 0.5 x_{2,Y} + 2.0 x_{3,Y} - 1.2 x_{1,B} + 0.3 x_{2,B} + 1.8 x_{3,B}
$$

### 4. Operational Constraints

**A. Supply Constraints (Grade Availability)**
The total usage of each grade cannot exceed its daily supply.
$$
\sum_{b \in B} x_{1,b} \le 1500
$$
$$
\sum_{b \in B} x_{2,b} \le 2000
$$
$$
\sum_{b \in B} x_{3,b} \le 1000
$$

**B. Blending Proportion Constraints**
Let $Q_b = \sum_{g \in G} x_{g,b}$ be the total quantity of brand $b$.
The constraints are linearized by moving terms to one side to avoid division by the variable sum.

*For Red Brand ($R$):*
1. Grade I > 50%:
   $$ x_{1,R} \ge 0.50 (x_{1,R} + x_{2,R} + x_{3,R}) \implies 0.50 x_{1,R} - 0.50 x_{2,R} - 0.50 x_{3,R} \ge 0 $$
   Or equivalently: $x_{1,R} \ge x_{2,R} + x_{3,R}$

2. Grade III < 10%:
   $$ x_{3,R} \le 0.10 (x_{1,R} + x_{2,R} + x_{3,R}) \implies -0.10 x_{1,R} - 0.10 x_{2,R} + 0.90 x_{3,R} \le 0 $$
   Or equivalently: $x_{3,R} \le \frac{1}{9} x_{1,R} + \frac{1}{9} x_{2,R}$ (using $x_{1,R}+x_{2,R} \ge 0.9(x_{1,R}+x_{2,R}+x_{3,R})$)

*For Yellow Brand ($Y$):*
1. Grade I > 20%:
   $$ x_{1,Y} \ge 0.20 (x_{1,Y} + x_{2,Y} + x_{3,Y}) \implies 0.80 x_{1,Y} - 0.20 x_{2,Y} - 0.20 x_{3,Y} \ge 0 $$
   Or equivalently: $4 x_{1,Y} \ge x_{2,Y} + x_{3,Y}$

2. Grade III < 70%:
   $$ x_{3,Y} \le 0.70 (x_{1,Y} + x_{2,Y} + x_{3,Y}) \implies -0.70 x_{1,Y} - 0.70 x_{2,Y} + 0.30 x_{3,Y} \le 0 $$
   Or equivalently: $3 x_{3,Y} \le 7 x_{1,Y} + 7 x_{2,Y}$

*For Blue Brand ($B$):*
1. Grade I > 10%:
   $$ x_{1,B} \ge 0.10 (x_{1,B} + x_{2,B} + x_{3,B}) \implies 0.90 x_{1,B} - 0.10 x_{2,B} - 0.10 x_{3,B} \ge 0 $$
   Or equivalently: $9 x_{1,B} \ge x_{2,B} + x_{3,B}$

2. Grade III < 50%:
   $$ x_{3,B} \le 0.50 (x_{1,B} + x_{2,B} + x_{3,B}) \implies -0.50 x_{1,B} - 0.50 x_{2,B} + 0.50 x_{3,B} \le 0 $$
   Or equivalently: $x_{3,B} \le x_{1,B} + x_{2,B}$

**C. Minimum Production Constraint**
At least 2,000 kg of Red brand liquor must be produced.
$$
x_{1,R} + x_{2,R} + x_{3,R} \ge 2000
$$

**D. Non-negativity**
$$
x_{g,b} \ge 0 \quad \forall g \in G, b \in B
$$