**Model Type:** LP (Linear Programming)

### 1. Index Sets & Parameters

**Index Sets:**
*   $G = \{1, 2, 3\}$: Set of base liquor grades (I, II, III).
*   $B = \{R, Y, Bl\}$: Set of branded products (Red, Yellow, Blue).

**Parameters (from Table 4-13 and 4-14):**

*   **Supply Limits ($S_g$ in kg):**
    *   $S_1 = 1500$ (Grade I)
    *   $S_2 = 2000$ (Grade II)
    *   $S_3 = 1000$ (Grade III)

*   **Costs ($c_g$ in Yuan/kg):**
    *   $c_1 = 6.0$
    *   $c_2 = 4.5$
    *   $c_3 = 3.0$

*   **Selling Prices ($p_b$ in Yuan/kg):**
    *   $p_R = 5.5$
    *   $p_Y = 5.0$
    *   $p_{Bl} = 4.8$

*   **Blending Constraints (Percentages converted to decimals):**
    *   *Red ($b=R$):*
        *   Grade III max: $u_{3,R} = 0.10$
        *   Grade I min: $l_{1,R} = 0.50$
    *   *Yellow ($b=Y$):*
        *   Grade III max: $u_{3,Y} = 0.70$
        *   Grade I min: $l_{1,Y} = 0.20$
    *   *Blue ($b=Bl$):*
        *   Grade III max: $u_{3,Bl} = 0.50$
        *   Grade I min: $l_{1,Bl} = 0.10$

*   **Production Requirements:**
    *   Min production for Red: $L_R = 2000$ kg.

### 2. Decision Variables

Let $x_{g,b}$ be the amount of Grade $g$ base liquor (in kg) used to produce Brand $b$ (in kg).

*   **Domain:** $x_{g,b} \geq 0$ for all $g \in G, b \in B$.
*   **Type:** Continuous (since the quantities are in kg and blending is a physical mixing process, continuous variables are appropriate unless integer constraints are explicitly demanded, which they are not here).

We can also define auxiliary variables for total production of each brand to simplify constraints, though they can be substituted directly:
*   $X_b = \sum_{g \in G} x_{g,b}$ for $b \in B$.

### 3. Objective Function

**Goal:** Maximize Profit.
Profit = Total Revenue - Total Cost.

$$
\text{Maximize } Z = \sum_{b \in B} p_b X_b - \sum_{g \in G} c_g \left( \sum_{b \in B} x_{g,b} \right)
$$

Substituting $X_b$:
$$
\text{Maximize } Z = \sum_{b \in B} p_b \left( \sum_{g \in G} x_{g,b} \right) - \sum_{g \in G} c_g \left( \sum_{b \in B} x_{g,b} \right)
$$

Alternatively, grouping by decision variable $x_{g,b}$:
$$
\text{Maximize } Z = \sum_{b \in B} \sum_{g \in G} (p_b - c_g) x_{g,b}
$$

**Expanded Coefficients ($p_b - c_g$):**
*   **Red ($p_R=5.5$):**
    *   Grade I: $5.5 - 6.0 = -0.5$
    *   Grade II: $5.5 - 4.5 = 1.0$
    *   Grade III: $5.5 - 3.0 = 2.5$
*   **Yellow ($p_Y=5.0$):**
    *   Grade I: $5.0 - 6.0 = -1.0$
    *   Grade II: $5.0 - 4.5 = 0.5$
    *   Grade III: $5.0 - 3.0 = 2.0$
*   **Blue ($p_{Bl}=4.8$):**
    *   Grade I: $4.8 - 6.0 = -1.2$
    *   Grade II: $4.8 - 4.5 = 0.3$
    *   Grade III: $4.8 - 3.0 = 1.8$

$$
\text{Maximize } Z = -0.5 x_{1,R} + 1.0 x_{2,R} + 2.5 x_{3,R} \quad \text{(Red terms)}
$$
$$
+ (-1.0) x_{1,Y} + 0.5 x_{2,Y} + 2.0 x_{3,Y} \quad \text{(Yellow terms)}
$$
$$
+ (-1.2) x_{1,Bl} + 0.3 x_{2,Bl} + 1.8 x_{3,Bl} \quad \text{(Blue terms)}
$$

### 4. Operational Constraints

#### A. Supply Constraints
The total amount of each grade used cannot exceed its daily supply.

1.  **Grade I:**
    $$ x_{1,R} + x_{1,Y} + x_{1,Bl} \leq 1500 $$
2.  **Grade II:**
    $$ x_{2,R} + x_{2,Y} + x_{2,Bl} \leq 2000 $$
3.  **Grade III:**
    $$ x_{3,R} + x_{3,Y} + x_{3,Bl} \leq 1000 $$

#### B. Blending Proportion Constraints
These constraints ensure the ratio of specific grades to the total brand production meets the specifications. We use the total production $X_b = \sum_{g} x_{g,b}$ in the denominator. To keep the model linear, we move the denominator to the other side.

**For Red Brand ($R$):**
*   Total Red: $X_R = x_{1,R} + x_{2,R} + x_{3,R}$
*   Constraint 1: Grade III < 10% of Red.
    $$ x_{3,R} \leq 0.10 X_R \implies x_{3,R} \leq 0.10 (x_{1,R} + x_{2,R} + x_{3,R}) $$
    $$ x_{3,R} - 0.10 x_{1,R} - 0.10 x_{2,R} - 0.10 x_{3,R} \leq 0 $$
    $$ -0.10 x_{1,R} - 0.10 x_{2,R} + 0.90 x_{3,R} \leq 0 $$
*   Constraint 2: Grade I > 50% of Red.
    $$ x_{1,R} \geq 0.50 X_R \implies x_{1,R} \geq 0.50 (x_{1,R} + x_{2,R} + x_{3,R}) $$
    $$ x_{1,R} - 0.50 x_{1,R} - 0.50 x_{2,R} - 0.50 x_{3,R} \geq 0 $$
    $$ 0.50 x_{1,R} - 0.50 x_{2,R} - 0.50 x_{3,R} \geq 0 $$
    *(Note: This implies $x_{1,R} \geq x_{2,R} + x_{3,R}$)*

**For Yellow Brand ($Y$):**
*   Total Yellow: $X_Y = x_{1,Y} + x_{2,Y} + x_{3,Y}$
*   Constraint 1: Grade III < 70% of Yellow.
    $$ x_{3,Y} \leq 0.70 X_Y \implies x_{3,Y} \leq 0.70 (x_{1,Y} + x_{2,Y} + x_{3,Y}) $$
    $$ x_{3,Y} - 0.70 x_{1,Y} - 0.70 x_{2,Y} - 0.70 x_{3,Y} \leq 0 $$
    $$ -0.70 x_{1,Y} - 0.70 x_{2,Y} + 0.30 x_{3,Y} \leq 0 $$
*   Constraint 2: Grade I > 20% of Yellow.
    $$ x_{1,Y} \geq 0.20 X_Y \implies x_{1,Y} \geq 0.20 (x_{1,Y} + x_{2,Y} + x_{3,Y}) $$
    $$ x_{1,Y} - 0.20 x_{1,Y} - 0.20 x_{2,Y} - 0.20 x_{3,Y} \geq 0 $$
    $$ 0.80 x_{1,Y} - 0.20 x_{2,Y} - 0.20 x_{3,Y} \geq 0 $$

**For Blue Brand ($Bl$):**
*   Total Blue: $X_{Bl} = x_{1,Bl} + x_{2,Bl} + x_{3,Bl}$
*   Constraint 1: Grade III < 50% of Blue.
    $$ x_{3,Bl} \leq 0.50 X_{Bl} \implies x_{3,Bl} \leq 0.50 (x_{1,Bl} + x_{2,Bl} + x_{3,Bl}) $$
    $$ x_{3,Bl} - 0.50 x_{1,Bl} - 0.50 x_{2,Bl} - 0.50 x_{3,Bl} \leq 0 $$
    $$ -0.50 x_{1,Bl} - 0.50 x_{2,Bl} + 0.50 x_{3,Bl} \leq 0 $$
*   Constraint 2: Grade I > 10% of Blue.
    $$ x_{1,Bl} \geq 0.10 X_{Bl} \implies x_{1,Bl} \geq 0.10 (x_{1,Bl} + x_{2,Bl} + x_{3,Bl}) $$
    $$ x_{1,Bl} - 0.10 x_{1,Bl} - 0.10 x_{2,Bl} - 0.10 x_{3,Bl} \geq 0 $$
    $$ 0.90 x_{1,Bl} - 0.10 x_{2,Bl} - 0.10 x_{3,Bl} \geq 0 $$

#### C. Production Requirement Constraints
*   **Minimum Red Production:**
    $$ x_{1,R} + x_{2,R} + x_{3,R} \geq 2000 $$

#### D. Non-negativity
$$ x_{g,b} \geq 0 \quad \forall g \in G, b \in B $$

---

### Feasibility Sanity Check

1.  **Red Production Check:**
    *   We need to produce at least 2000 kg of Red.
    *   Red requires $>50\%$ Grade I. So we need $>1000$ kg of Grade I for 2000 kg of Red.
    *   Total Grade I supply is 1500 kg.
    *   If we use 1500 kg of Grade I for Red, the maximum Red we can make (given 50% Grade I min) is $1500 / 0.50 = 3000$ kg.
    *   However, Red also has a max 10% Grade III constraint.
    *   Let's check if 2000 kg Red is feasible with available Grade I.
        *   Min Grade I for 2000 kg Red: $>1000$ kg.
        *   Max Grade III for 2000 kg Red: $<200$ kg.
        *   Remaining $2000 - 1000 - 200 = 800$ kg would be Grade II.
        *   This is physically possible if we have enough Grade II. We have 2000 kg Grade II.
        *   So, producing 2000 kg Red is feasible regarding raw materials, *provided* we don't starve other brands or violate other constraints.
    *   Wait, the constraint is "Grade I > 50%". So $x_{1,R} > 1000$.
    *   The constraint is "Grade III < 10%". So $x_{3,R} < 200$.
    *   Is it possible to satisfy $x_{1,R} + x_{2,R} + x_{3,R} = 2000$ with $x_{1,R} > 1000$ and $x_{3,R} < 200$?
        *   Yes. E.g., $x_{1,R}=1100, x_{3,R}=100, x_{2,R}=800$.
        *   Check Grade I supply: 1100 used. Remaining Grade I = $1500 - 1100 = 400$.
        *   Check Grade III supply: 100 used. Remaining Grade III = $1000 - 100 = 900$.
        *   Check Grade II supply: 800 used. Remaining Grade II = $2000 - 800 = 1200$.

2.  **Other Brands:**
    *   Can we produce Yellow or Blue with remaining supplies?
    *   Remaining supplies: $G_I=400, G_{II}=1200, G_{III}=900$.
    *   Yellow requirements: $G_I > 20\%$, $G_{III} < 70\%$.
    *   Blue requirements: $G_I > 10\%$, $G_{III} < 50\%$.
    *   There is no minimum production requirement for Yellow or Blue, so they can be 0.
    *   The model will decide how much to produce based on profit.

3.  **Profitability Check:**
    *   Red profit margins: $G_I$ is negative (-0.5), $G_{II}$ is positive (1.0), $G_{III}$ is positive (2.5).
    *   To maximize profit in Red, we want to use as much $G_{III}$ and $G_{II}$ as possible, and as little $G_I$ as possible (but must satisfy $>50\%$).
    *   Since $G_I$ is the most expensive and yields the lowest margin (or negative) in all brands, the solver will try to minimize $G_I$ usage subject to the lower bound constraints.
    *   For Red, min $G_I$ is just over 50%.
    *   For Yellow, min $G_I$ is just over 20%.
    *   For Blue, min $G_I$ is just over 10%.

    The constraints are consistent. The model is feasible.