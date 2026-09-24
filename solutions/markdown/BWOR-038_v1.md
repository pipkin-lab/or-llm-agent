# Mathematical Optimization Model for Hongsheng Factory Production Planning

## Model Type
**LP** (Linear Programming)

## Index Sets & Parameters

**Sets:**
- $P = \{1, 2, 3\}$: Set of products (I, II, III)
- $M_A = \{A_1, A_2\}$: Set of Stage A machines
- $M_B = \{B_1, B_2, B_3\}$: Set of Stage B machines
- $M = M_A \cup M_B$: Set of all machines

**Parameters (from Table 1-20):**

*Processing Times (minutes/unit):*
- $t_{A_1,1} = 5$, $t_{A_1,2} = 10$, $t_{A_1,3} = 0$ (not allowed)
- $t_{A_2,1} = 7$, $t_{A_2,2} = 9$, $t_{A_2,3} = 12$
- $t_{B_1,1} = 6$, $t_{B_1,2} = 8$, $t_{B_1,3} = 0$ (not allowed)
- $t_{B_2,1} = 4$, $t_{B_2,2} = 0$ (not allowed), $t_{B_2,3} = 11$
- $t_{B_3,1} = 7$, $t_{B_3,2} = 0$ (not allowed), $t_{B_3,3} = 0$ (not allowed)

*Machine Available Hours (hours):*
- $H_{A_1} = 6000$, $H_{A_2} = 10000$
- $H_{B_1} = 4000$, $H_{B_2} = 7000$, $H_{B_3} = 4000$

*Processing Cost (yuan/hour):*
- $c_{A_1} = 0.05$, $c_{A_2} = 0.03$
- $c_{B_1} = 0.06$, $c_{B_2} = 0.11$, $c_{B_3} = 0.05$

*Raw Material Cost (yuan/unit):*
- $r_1 = 0.25$, $r_2 = 0.35$, $r_3 = 0.50$

*Selling Price (yuan/unit):*
- $p_1 = 1.25$, $p_2 = 2.00$, $p_3 = 2.80$

## Decision Variables

Let $x_{m,p}$ be the number of units of product $p$ processed on machine $m$.

**Domain:** $x_{m,p} \geq 0$ and continuous (production quantities are continuous resources in this aggregate planning context).

Specifically, we define variables only for allowed (machine, product) pairs based on the processing rules:
- **Stage A:**
  - $x_{A_1,1}, x_{A_1,2} \geq 0$ (Product III not allowed on $A_1$)
  - $x_{A_2,1}, x_{A_2,2}, x_{A_2,3} \geq 0$
- **Stage B:**
  - $x_{B_1,1}, x_{B_1,2} \geq 0$ (Product III not allowed on $B_1$)
  - $x_{B_2,1}, x_{B_2,3} \geq 0$ (Product II not allowed on $B_2$)
  - $x_{B_3,1} \geq 0$ (Only Product I allowed on $B_3$)

## Objective Function

Maximize total profit:
$$ \text{Maximize } Z = \sum_{p \in P} \left( p_p - r_p - \sum_{m \in M_A} c_m \cdot \frac{t_{m,p}}{60} - \sum_{m \in M_B} c_m \cdot \frac{t_{m,p}}{60} \right) \cdot \text{TotalProd}_p - \sum_{m \in M} c_m \cdot \frac{1}{60} \sum_{p \in P} t_{m,p} \cdot x_{m,p} $$

Wait, it is cleaner to express the objective directly in terms of the decision variables to handle the machine-specific processing costs correctly.

Let $Q_p$ be the total quantity of product $p$ produced.
$Q_p = \sum_{m \in M_A} x_{m,p} = \sum_{m \in M_B} x_{m,p}$ (due to flow balance).

Revenue: $\sum_{p=1}^3 p_p Q_p$
Raw Material Cost: $\sum_{p=1}^3 r_p Q_p$
Processing Cost: $\sum_{m \in M} c_m \cdot (\text{Total Time used on } m) = \sum_{m \in M} c_m \cdot \frac{1}{60} \sum_{p \in P} t_{m,p} x_{m,p}$

Thus, the objective function is:
$$ \text{Maximize } Z = \sum_{p=1}^3 (p_p - r_p) Q_p - \sum_{m \in M} \frac{c_m}{60} \sum_{p \in P} t_{m,p} x_{m,p} $$

Substituting $Q_p$ with the sum of Stage A variables (or Stage B, they are equal):
$$ Z = \sum_{p=1}^3 (p_p - r_p) \left( \sum_{m \in M_A} x_{m,p} \right) - \sum_{m \in M_A} \frac{c_m}{60} \sum_{p \in P} t_{m,p} x_{m,p} - \sum_{m \in M_B} \frac{c_m}{60} \sum_{p \in P} t_{m,p} x_{m,p} $$

Expanding the coefficients for each variable $x_{m,p}$:
For a variable $x_{m,p}$ where $m \in M_A$, the coefficient in the objective is:
$(p_p - r_p) - \frac{c_m t_{m,p}}{60} - \frac{c_{m',p} t_{m',p}}{60}$ ... wait, the Stage B cost depends on which Stage B machine is used. Since the Stage B machine is a separate decision variable, we cannot simply sum them up without linking them.

Let's refine the objective structure.
Let $x^A_{m,p}$ be units of product $p$ processed on Stage A machine $m$.
Let $x^B_{m,p}$ be units of product $p$ processed on Stage B machine $m$.

**Objective:**
$$ \text{Maximize } Z = \sum_{p=1}^3 (p_p - r_p) \sum_{m \in M_A} x^A_{m,p} - \sum_{m \in M_A} \frac{c_m}{60} \sum_{p \in P} t_{m,p} x^A_{m,p} - \sum_{m \in M_B} \frac{c_m}{60} \sum_{p \in P} t_{m,p} x^B_{m,p} $$

Note: The first term represents net revenue (Sale Price - Raw Material Cost) per unit produced. The subsequent terms subtract the machine-specific processing costs.

## Operational Constraints

### 1. Flow Balance Constraints (Conservation of Mass)
The number of units of each product processed in Stage A must equal the number processed in Stage B.
For each product $p \in \{1, 2, 3\}$:
$$ \sum_{m \in M_A} x^A_{m,p} = \sum_{m \in M_B} x^B_{m,p} $$

Explicitly:
- **Product I:** $x^A_{A_1,1} + x^A_{A_2,1} = x^B_{B_1,1} + x^B_{B_2,1} + x^B_{B_3,1}$
- **Product II:** $x^A_{A_1,2} + x^A_{A_2,2} = x^B_{B_1,2}$ (Only $B_1$ allows Product II? No, check table. Table says Product II on $B_2$ is empty? Let's re-read carefully.)

**Re-reading Table and Rules:**
- **Product I:** Any A, Any B.
- **Product II:** Any A, but in Stage B **only** on machine $B_2$.
  - *Correction on Table Interpretation:* The table has "8" under Product II for Machine $B_1$ and empty for $B_2$ and $B_3$.
  - *Conflict Check:* The text says "Product II ... in stage B it can only be processed on machine $B_2$". The table shows processing time 8 for $B_1$ and empty for $B_2$.
  - *Resolution:* Usually, in such textbook problems, if the text explicitly restricts the machine, that rule overrides or clarifies the table. However, looking at the table:
    - Row $B_1$: Product I (6), Product II (8), Product III (empty).
    - Row $B_2$: Product I (4), Product II (empty), Product III (11).
    - Row $B_3$: Product I (7), Product II (empty), Product III (empty).
  - The text says: "Product II can be processed on any A machine, but in stage B it can only be processed on machine $B_2$."
  - BUT the table has a value (8) for Product II on $B_1$ and empty for $B_2$.
  - AND the text says: "Product III can only be processed on $A_2$ and $B_2$." Table has 12 for $A_2$ (correct) and 11 for $B_2$ (correct).
  - There is a direct contradiction for Product II between the text ("only $B_2$") and the table (value on $B_1$, empty on $B_2$).
  - *Standard Interpretation:* In many OR textbook examples, the text describes the *logical* routing constraints, while the table provides *data*. If the text says "only on B2", but the table gives a time on B1 and none on B2, it's highly likely a typo in the problem source or my reading of the table alignment.
  - Let's look at the table alignment again.
    - Header: Product I, II, III.
    - Row B1: 6, 8, (empty).
    - Row B2: 4, (empty), 11.
  - If I follow the **text**: Product II goes to $B_2$. But table has no time for $B_2$. This is impossible.
  - If I follow the **table**: Product II goes to $B_1$ (time 8). The text might contain a typo ("only on B2" instead of "only on B1"?).
  - Let's check Product III. Text: "only on A2 and B2". Table: A2 has 12, B2 has 11. This matches.
  - Let's check Product I. Text: "any". Table: A1, A2, B1, B2, B3 all have values. This matches.
  - So, for Product II, the text says "only B2", table says "B1 has 8, B2 is empty".
  - *Hypothesis:* The text meant "only on $B_1$" OR the table has a typo where the '8' should be under $B_2$.
  - *Decision:* The table is the primary data source for parameters. The text provides structural rules. If the table has a value for a machine, it is usually allowed. If the table is empty, it is not allowed. The text's "only on B2" for Product II contradicts the table's data (empty B2). However, looking at standard problems of this type, it is possible the text meant "Product II ... only on B1" (matching table) or "Product III ... only on B2" (matching table).
  - Let's re-read the text carefully: "Product II ... in stage B it can only be processed on machine $B_2$".
  - Let's assume the **Table** is correct for *availability* (non-empty = allowed) and the **Text** might have a typo, OR the Text is correct and the Table has a typo.
  - *Alternative View:* Maybe the columns in the table are misaligned? No, Product III fits perfectly with the text. Product I fits perfectly.
  - Let's look at the costs.
  - If Product II *must* use B2, but the table has no time, the model is infeasible or requires a parameter [NOT_PROVIDED].
  - If Product II *uses* B1 (per table), the text is wrong.
  - *Most Likely Scenario in Exam/Textbook Context:* The text description usually takes precedence for *logic* if the table is ambiguous, but here the table is explicit with numbers. However, an empty cell usually means "not allowed". If the text says "only B2", and B2 is empty in the table, it's a broken problem.
  - *Wait*, look at the table again.
    Row B1: 6 (I), 8 (II), blank (III).
    Row B2: 4 (I), blank (II), 11 (III).
    Text: "Product II ... only ... B2".
    Text: "Product III ... only ... B2".
    If Product II and Product III *both* only go to B2, then B2 handles II and III.
    But the table has 11 for III on B2. It has blank for II on B2. It has 8 for II on B1.
    It is overwhelmingly likely that the text contains a typo and meant **"Product II ... only on machine $B_1$"**. Why? Because the table explicitly lists a time (8) for II on B1 and none on B2. And for III, it lists 11 on B2 and none on B1. The text correctly identifies III -> B2. It likely misidentified II -> B2 instead of II -> B1.
    
    **Assumption for Modeling:** I will follow the **Table Data** for allowable machines and processing times, as it is the quantitative source. The textual constraint for Product II is assumed to be a typo for $B_1$.
    *Correction*: Actually, looking at similar online problems for "Hongsheng Factory", the standard version of this problem often has Product II processed on $B_1$ or $B_2$ depending on the variant. Given the explicit "8" in the table for B1/II and "11" for B2/III, and the text's error, I will model based on the **Table's non-zero entries** defining the allowed arcs.
    
    **Allowed (Machine, Product) Pairs based on Table Non-Zero Entries:**
    - $A_1$: I, II
    - $A_2$: I, II, III
    - $B_1$: I, II
    - $B_2$: I, III
    - $B_3$: I

    *Self-Correction*: If I ignore the text's "only B2" for II, I am deviating from the explicit text. But if I follow the text, I have no processing time for II on B2. I cannot model a variable without a processing time parameter. Therefore, the only solvable interpretation is that **Product II is processed on $B_1$** (as per table) and the text has a typo. I will proceed with the Table's implications for feasibility.

### 2. Machine Capacity Constraints
For each machine $m$, the total processing time required by all products assigned to it must not exceed the available hours. Note: Processing times are in minutes, available hours are in hours. Convert available hours to minutes or processing times to hours. Let's convert available hours to minutes for consistency with processing times, or convert processing times to hours.
Let's convert Available Hours to Minutes: $H_m (\text{min}) = H_m (\text{hr}) \times 60$.
- $H_{A_1} = 360,000$ min
- $H_{A_2} = 600,000$ min
- $H_{B_1} = 240,000$ min
- $H_{B_2} = 420,000$ min
- $H_{B_3} = 240,000$ min

Constraints:
1.  **Machine $A_1$:**
    $$ 5 x^A_{A_1,1} + 10 x^A_{A_1,2} \leq 360,000 $$
2.  **Machine $A_2$:**
    $$ 7 x^A_{A_2,1} + 9 x^A_{A_2,2} + 12 x^A_{A_2,3} \leq 600,000 $$
3.  **Machine $B_1$:**
    $$ 6 x^B_{B_1,1} + 8 x^B_{B_1,2} \leq 240,000 $$
4.  **Machine $B_2$:**
    $$ 4 x^B_{B_2,1} + 11 x^B_{B_2,3} \leq 420,000 $$
5.  **Machine $B_3$:**
    $$ 7 x^B_{B_3,1} \leq 240,000 $$

### 3. Non-negativity
$$ x^A_{m,p} \geq 0, \quad x^B_{m,p} \geq 0 \quad \forall m, p \text{ where allowed} $$

## Summary of the Model

**Decision Variables:**
- $x^A_{A_1,1}, x^A_{A_1,2}, x^A_{A_2,1}, x^A_{A_2,2}, x^A_{A_2,3}$
- $x^B_{B_1,1}, x^B_{B_1,2}, x^B_{B_2,1}, x^B_{B_2,3}, x^B_{B_3,1}$

**Objective Function (Maximize Profit):**
$$ \begin{aligned} \text{Max } Z = & \; \sum_{p} (p_p - r_p) Q_p - \sum_{m} \frac{c_m}{60} \sum_{p} t_{m,p} x_{m,p} \\ \text{Where } Q_p = \sum_{m \in M_A} x^A_{m,p} \end{aligned} $$

Expanded by variable coefficients (Profit per unit on specific path):
- For $x^A_{A_1,1}$ (Prod I on A1): Coeff in Obj = $(1.25 - 0.25) - \frac{0.05 \times 5}{60} - \text{(Stage B cost depends on B choice)}$
  *Note:* It is computationally safer to keep the objective as:
  $$ Z = \sum_{p=1}^3 (p_p - r_p) \left( \sum_{m \in M_A} x^A_{m,p} \right) - \sum_{m \in M_A} \frac{c_m}{60} \sum_{p} t_{m,p} x^A_{m,p} - \sum_{m \in M_B} \frac{c_m}{60} \sum_{p} t_{m,p} x^B_{m,p} $$

**Constraints:**
1.  **Flow Balance:**
    - $x^A_{A_1,1} + x^A_{A_2,1} = x^B_{B_1,1} + x^B_{B_2,1} + x^B_{B_3,1}$
    - $x^A_{A_1,2} + x^A_{A_2,2} = x^B_{B_1,2}$  *(Assuming Table correctness for Prod II -> B1)*
    - $x^A_{A_2,3} = x^B_{B_2,3}$

2.  **Capacity (Minutes):**
    - $5 x^A_{A_1,1} + 10 x^A_{A_1,2} \leq 360,000$
    - $7 x^A_{A_2,1} + 9 x^A_{A_2,2} + 12 x^A_{A_2,3} \leq 600,000$
    - $6 x^B_{B_1,1} + 8 x^B_{B_1,2} \leq 240,000$
    - $4 x^B_{B_2,1} + 11 x^B_{B_2,3} \leq 420,000$
    - $7 x^B_{B_3,1} \leq 240,000$

3.  **Bounds:**
    - All $x \geq 0$