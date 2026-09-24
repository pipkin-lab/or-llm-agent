### Index Sets & Parameters

**Index Sets:**
- $G = \{1, 2, 3\}$: Set of base liquor grades (Grade I, Grade II, Grade III).
- $P = \{R, Y, B\}$: Set of branded products (Red, Yellow, Blue).
- $GP = \{(g, p) \mid g \in G, p \in P\}$: Set of all possible grade-product pairs.

**Parameters:**

*Supply and Cost (Base Liquors):*
- $S_g$: Daily maximum supply of Grade $g$ (kg).
  - $S_1 = 1500$, $S_2 = 2000$, $S_3 = 1000$
- $C_g$: Cost per kg of Grade $g$ (Yuan).
  - $C_1 = 6.0$, $C_2 = 4.5$, $C_3 = 3.0$

*Product Data:*
- $Price_p$: Selling price per kg of Brand $p$ (Yuan).
  - $Price_R = 5.5$, $Price_Y = 5.0$, $Price_B = 4.8$
- $MinProd_p$: Minimum required production quantity for Brand $p$ (kg).
  - $MinProd_R = 2000$, $MinProd_Y = 0$, $MinProd_B = 0$

*Blending Constraints (Proportions):*
Let $L^{low}_{g,p}$ and $U^{up}_{g,p}$ denote the lower and upper bounds for the percentage of Grade $g$ in Brand $p$. The problem specifies specific bounds for Grade I and Grade III. Grade II is unconstrained except by the summation of proportions to 100%.

For **Red ($R$)**:
- Grade I: $> 50\% \implies L^{low}_{1,R} = 0.50$, $U^{up}_{1,R} = 1.0$ (implicitly, but constrained by others)
- Grade III: $< 10\% \implies L^{low}_{3,R} = 0$, $U^{up}_{3,R} = 0.10$
- Grade II: No explicit bounds, determined by remainder.

For **Yellow ($Y$)**:
- Grade I: $> 20\% \implies L^{low}_{1,Y} = 0.20$, $U^{up}_{1,Y} = 1.0$
- Grade III: $< 70\% \implies L^{low}_{3,Y} = 0$, $U^{up}_{3,Y} = 0.70$
- Grade II: No explicit bounds.

For **Blue ($B$)**:
- Grade I: $> 10\% \implies L^{low}_{1,B} = 0.10$, $U^{up}_{1,B} = 1.0$
- Grade III: $< 50\% \implies L^{low}_{3,B} = 0$, $U^{up}_{3,B} = 0.50$
- Grade II: No explicit bounds.

*Note on Strict Inequalities:* In linear programming, strict inequalities ($<$ or $>$) are handled by replacing them with non-strict inequalities ($\le$ or $\ge$) and adding a small epsilon $\epsilon$ if necessary to ensure feasibility, or simply using non-strict bounds if the context implies "at least/at most" in a practical sense. Given standard OR modeling conventions for blending, we interpret "$< 10\%$" as $\le 10\%$ and "$> 50\%$" as $\ge 50\%$ unless exact boundary exclusion is critical. However, strictly speaking, to model "strictly follow", we use the bounds provided. Let's define the bounds explicitly for the constraints below.

---

### Decision Variables

Let $x_{g,p}$ be the amount (in kg) of Grade $g$ base liquor blended into Brand $p$.

- **Domain**: $x_{g,p} \in \mathbb{R}_{\ge 0}$ for all $g \in G, p \in P$.
  - Since the quantities are in kilograms and can be fractional (continuous resource), we use **continuous** variables.

Let $z_p$ be the total quantity (in kg) of Brand $p$ produced.
- **Domain**: $z_p \in \mathbb{R}_{\ge 0}$ for all $p \in P$.

*(Note: $z_p$ can be defined as $\sum_{g \in G} x_{g,p}$, but defining it explicitly simplifies the objective and minimum production constraints.)*

---

### Objective Function

The problem has prioritized conditions. Condition 1 (Blending Proportions) and Condition 3 (Min Production) are **hard constraints**. Condition 2 (Maximize Profit) is the **objective function**.

Maximize Total Profit ($Z$):
$$
\text{Maximize } Z = \sum_{p \in P} \left( Price_p \cdot z_p - \sum_{g \in G} C_g \cdot x_{g,p} \right)
$$

Substituting the specific values:
$$
\text{Maximize } Z = 5.5 z_R + 5.0 z_Y + 4.8 z_B - \sum_{g \in G} C_g \left( \sum_{p \in P} x_{g,p} \right)
$$

Or expanded by grade cost:
$$
\text{Maximize } Z = 5.5 z_R + 5.0 z_Y + 4.8 z_B - 6.0 \sum_{p \in P} x_{1,p} - 4.5 \sum_{p \in P} x_{2,p} - 3.0 \sum_{p \in P} x_{3,p}
$$

---

### Operational Constraints

#### 1. Production Definition Constraints
The total production of each brand must equal the sum of its components.
$$
z_p = \sum_{g \in G} x_{g,p} \quad \forall p \in P
$$

#### 2. Minimum Production Constraints (Priority 3)
At least 2,000 kg of Red brand must be produced. No minimums for Yellow or Blue.
$$
z_R \ge 2000
$$
$$
z_Y \ge 0
$$
$$
z_B \ge 0
$$

#### 3. Supply Constraints
The total usage of each grade cannot exceed its daily supply.
$$
\sum_{p \in P} x_{1,p} \le 1500 \quad \text{(Grade I)}
$$
$$
\sum_{p \in P} x_{2,p} \le 2000 \quad \text{(Grade II)}
$$
$$
\sum_{p \in P} x_{3,p} \le 1000 \quad \text{(Grade III)}
$$

#### 4. Blending Proportion Constraints (Priority 1)
These constraints ensure the ratio of each grade to the total brand production $z_p$ meets the requirements.
To avoid non-linearity (division by variable $z_p$), we multiply the proportion constraints by $z_p$. Note: If $z_p=0$, these constraints become $0 \le 0$, which is valid.

**For Red Brand ($R$):**
- Grade I $> 50\%$:
  $$
  x_{1,R} \ge 0.50 z_R
  $$
- Grade III $< 10\%$:
  $$
  x_{3,R} \le 0.10 z_R
  $$
- *Implicit Constraint for Grade II*: Since $x_{1,R} + x_{2,R} + x_{3,R} = z_R$, and $x_{1,R} \ge 0.5 z_R, x_{3,R} \le 0.1 z_R$, it follows that $x_{2,R} \le 0.5 z_R$ and $x_{2,R} \ge 0$. No explicit separate constraint is needed for Grade II other than non-negativity and the sum constraint, but we must ensure feasibility.

**For Yellow Brand ($Y$):**
- Grade I $> 20\%$:
  $$
  x_{1,Y} \ge 0.20 z_Y
  $$
- Grade III $< 70\%$:
  $$
  x_{3,Y} \le 0.70 z_Y
  $$

**For Blue Brand ($B$):**
- Grade I $> 10\%$:
  $$
  x_{1,B} \ge 0.10 z_B
  $$
- Grade III $< 50\%$:
  $$
  x_{3,B} \le 0.50 z_B
  $$

#### 5. Non-negativity
$$
x_{g,p} \ge 0 \quad \forall g \in G, p \in P
$$
$$
z_p \ge 0 \quad \forall p \in P
$$

---

### Summary of the Mathematical Model

**Maximize:**
$$
Z = 5.5 z_R + 5.0 z_Y + 4.8 z_B - 6.0 \sum_{p \in P} x_{1,p} - 4.5 \sum_{p \in P} x_{2,p} - 3.0 \sum_{p \in P} x_{3,p}
$$

**Subject to:**

1.  **Mass Balance:**
    $$
    z_R = x_{1,R} + x_{2,R} + x_{3,R}
    $$
    $$
    z_Y = x_{1,Y} + x_{2,Y} + x_{3,Y}
    $$
    $$
    z_B = x_{1,B} + x_{2,B} + x_{3,B}
    $$

2.  **Minimum Production:**
    $$
    z_R \ge 2000
    $$

3.  **Supply Limits:**
    $$
    x_{1,R} + x_{1,Y} + x_{1,B} \le 1500
    $$
    $$
    x_{2,R} + x_{2,Y} + x_{2,B} \le 2000
    $$
    $$
    x_{3,R} + x_{3,Y} + x_{3,B} \le 1000
    $$

4.  **Blending Ratios (Red):**
    $$
    x_{1,R} \ge 0.50 z_R
    $$
    $$
    x_{3,R} \le 0.10 z_R
    $$

5.  **Blending Ratios (Yellow):**
    $$
    x_{1,Y} \ge 0.20 z_Y
    $$
    $$
    x_{3,Y} \le 0.70 z_Y
    $$

6.  **Blending Ratios (Blue):**
    $$
    x_{1,B} \ge 0.10 z_B
    $$
    $$
    x_{3,B} \le 0.50 z_B
    $$

7.  **Non-negativity:**
    $$
    x_{g,p} \ge 0, \quad z_p \ge 0 \quad \forall g \in G, p \in P
    $$