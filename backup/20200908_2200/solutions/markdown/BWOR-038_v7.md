### 1. Index Sets & Parameters

**Sets:**
*   $P = \{1, 2, 3\}$: Set of products (I, II, III).
*   $M_A = \{A_1, A_2\}$: Set of machines in Stage A.
*   $M_B = \{B_1, B_2, B_3\}$: Set of machines in Stage B.
*   $M = M_A \cup M_B$: Set of all machines.

**Parameters:**
*   $a_{m,p}$: Processing time (hours) of product $p$ on machine $m$. If product $p$ cannot be processed on machine $m$, $a_{m,p} = 0$ (or undefined, handled by variable bounds).
*   $C_m$: Processing cost per hour on machine $m$ (yuan/hour).
*   $T_m$: Available time on machine $m$ (hours).
*   $r_p$: Raw material cost per unit of product $p$ (yuan/unit).
*   $S_p$: Selling price per unit of product $p$ (yuan/unit).

**Data Extraction from Table 1-20:**

| Parameter | $A_1$ | $A_2$ | $B_1$ | $B_2$ | $B_3$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Time $a_{m,p}$ for Prod I** | 5 | 7 | 6 | 4 | 7 |
| **Time $a_{m,p}$ for Prod II** | 10 | 9 | **Infeasible** | **Infeasible** | **Infeasible** |
| **Time $a_{m,p}$ for Prod III** | **Infeasible** | 12 | **Infeasible** | 11 | **Infeasible** |
| **Available Time $T_m$** | 6,000 | 10,000 | 4,000 | 7,000 | 4,000 |
| **Cost Rate $C_m$** | 0.05 | 0.03 | 0.06 | 0.11 | 0.05 |

*Note on Feasibility based on Problem Text:*
*   **Product I**: Can be processed on any machine in A ($A_1, A_2$) and any machine in B ($B_1, B_2, B_3$).
*   **Product II**: Can be processed on any A machine ($A_1, A_2$), but in Stage B **only** on $B_2$.
    *   *Conflict Check*: The table shows blanks for Product II on $B_1, B_2, B_3$. However, the text explicitly states "in stage B it can only be processed on machine $B_2$". Usually, blank cells mean infeasible. But if $B_2$ is blank in the table for Product II, there is a conflict. Let's re-read carefully.
    *   Table Row "II": $A_1=10$, $A_2=9$, $B_1=$ (blank), $B_2=$ (blank), $B_3=$ (blank).
    *   Text: "Product II ... in stage B it can only be processed on machine $B_2$".
    *   *Resolution*: The text provides a specific constraint that overrides the general "blank = infeasible" interpretation for $B_2$ if the table is incomplete, OR the table has a typo. However, looking at standard OR problems of this type (likely from a Chinese textbook given the currency "yuan"), the table usually contains the data. Let's look at Product III.
    *   Product III: Text says "only processed on $A_2$ and $B_2$". Table shows $A_2=12$, $B_2=11$. This matches.
    *   Product II: Text says "only $B_2$". Table shows blank for $B_2$. This is a direct contradiction.
    *   *Re-evaluating Table Structure*: Sometimes columns/rows are misaligned in HTML conversions.
        *   Row II: 10, 9, (blank), (blank), (blank).
        *   If the text says it *must* use $B_2$, and the table is blank, we have missing data.
        *   *Alternative Interpretation*: Did the text mean "Product II ... only on $B_1$?" No, it says $B_2$.
        *   *Standard Practice for this Specific Problem (Hongsheng Factory)*: This is a classic problem (e.g., from *Operations Research* by Tsay or similar). In many versions of this specific problem, the table for Product II on $B_2$ is **8** hours. Let's check the table again.
        *   Row B1: 6, 8, (blank). Wait.
        *   Let's look at the HTML source provided in the prompt again.
            *   Row B1: `<td>6</td><td>8</td><td></td>` -> Prod I=6, Prod II=8, Prod III=blank.
            *   Row B2: `<td>4</td><td></td><td>11</td>` -> Prod I=4, Prod II=blank, Prod III=11.
            *   Row B3: `<td>7</td><td></td><td></td>` -> Prod I=7, Prod II=blank, Prod III=blank.
    *   **CRITICAL DATA DISCREPANCY**:
        *   Text: "Product II ... in stage B it can only be processed on machine $B_2$".
        *   Table: Product II has a time of **8** on **$B_1$** (Row B1, Col II is 8). Product II has **no** time listed on $B_2$ (Row B2, Col II is blank).
        *   If we follow the **TEXT** strictly: Product II must use $B_2$. But Table has no time for II on $B_2$.
        *   If we follow the **TABLE** strictly: Product II can use $B_1$ (time 8). It cannot use $B_2$ (blank).
        *   *Conflict Resolution Rule*: "Treat the TABLE as the primary source of truth for numerical parameters... Treat BLANK cells as INFEASIBLE".
        *   However, the text *also* defines the feasibility logic. "Product II ... only ... on $B_2$".
        *   Let's look at the other products.
            *   Prod III: Text says only $A_2, B_2$. Table has $A_2=12, B_2=11$. Consistent.
            *   Prod I: Text says any. Table has all entries. Consistent.
        *   It is highly probable that the **Text contains a typo** and meant $B_1$ for Product II, OR the **Table has a typo** and the 8 belongs to $B_2$.
        *   Let's check the cost implications.
            *   If Prod II uses $B_1$ (Time 8, Cost 0.06): Cost = $8 \times 0.06 = 0.48$.
            *   If Prod II uses $B_2$ (Time ? , Cost 0.11): If time were, say, 8, Cost = $8 \times 0.11 = 0.88$.
        *   Let's re-read the table header mapping.
            *   `<tr><td>B1</td><td>6</td><td>8</td><td></td>...`
            *   Col 1: Machine. Col 2: Prod I. Col 3: Prod II. Col 4: Prod III.
            *   So, $a_{B_1, 2} = 8$. $a_{B_2, 2} = \text{blank}$.
        *   The text says "Product II ... only ... on $B_2$".
        *   If I must choose, the **Table** provides the numerical processing time (8 hours) on $B_1$. The text's constraint "only on $B_2$" contradicts the data availability.
        *   *Hypothesis*: The text likely contains a typo and should say "only on $B_1$" OR the table's column for B1/B2 is shifted.
        *   Let's look at Product III again. Text: "only $A_2$ and $B_2$". Table: $A_2=12, B_2=11$. This fits perfectly.
        *   Let's look at Product II again. If the text is right, we are missing the processing time for II on $B_2$. If the table is right, the text is wrong about the machine.
        *   Given "DATA COMPLETENESS CHECK": If numbers are missing, I must state the assumption.
        *   *Most Likely Scenario in Textbooks*: The text description of constraints often summarizes the table. If the table shows time 8 on $B_1$ and blank elsewhere for Product II, the constraint is implicitly "Product II can be processed on $B_1$". The text saying "$B_2$" is likely a typo for "$B_1$".
        *   **Decision**: I will model based on the **TABLE** data for processing times and feasibility (Blank = Infeasible), as the numerical parameters (8 hours) are explicitly present on $B_1$. I will add a note about the conflict. If I force it to $B_2$, I have no processing time $a_{B_2, 2}$. I cannot invent a number. Therefore, the only solvable model uses $B_1$ for Product II in Stage B.

    *   **Revised Feasibility based on Table Data (Primary Source):**
        *   **Product I**:
            *   Stage A: $A_1$ (5h), $A_2$ (7h)
            *   Stage B: $B_1$ (6h), $B_2$ (4h), $B_3$ (7h)
        *   **Product II**:
            *   Stage A: $A_1$ (10h), $A_2$ (9h)
            *   Stage B: $B_1$ (8h). ($B_2, B_3$ are infeasible/blank).
        *   **Product III**:
            *   Stage A: $A_2$ (12h). ($A_1$ is infeasible/blank).
            *   Stage B: $B_2$ (11h). ($B_1, B_3$ are infeasible/blank).

**Unit Economics (Profit per unit):**
Profit = Selling Price - Raw Material Cost - Total Processing Cost.
Since processing cost depends on the machine chosen, the objective function will sum costs directly rather than using a fixed unit profit.
Objective: Maximize $\sum (\text{Revenue}) - \sum (\text{Raw Cost}) - \sum (\text{Processing Cost})$.

### 2. Decision Variables

Let $x_{m,p}$ be the number of units of product $p$ processed on machine $m$.

Since each product must go through both Stage A and Stage B, we define variables for each stage separately to ensure flow conservation.

**Stage A Variables ($x^A_{m,p}$):**
*   $x^{A}_{A_1, 1}, x^{A}_{A_2, 1}$: Units of Product I on $A_1, A_2$.
*   $x^{A}_{A_1, 2}, x^{A}_{A_2, 2}$: Units of Product II on $A_1, A_2$.
*   $x^{A}_{A_2, 3}$: Units of Product III on $A_2$. ($A_1$ infeasible).

**Stage B Variables ($x^B_{m,p}$):**
*   $x^{B}_{B_1, 1}, x^{B}_{B_2, 1}, x^{B}_{B_3, 1}$: Units of Product I on $B_1, B_2, B_3$.
*   $x^{B}_{B_1, 2}$: Units of Product II on $B_1$. ($B_2, B_3$ infeasible based on table).
*   $x^{B}_{B_2, 3}$: Units of Product III on $B_2$. ($B_1, B_3$ infeasible).

**Domain:**
All $x \ge 0$ and Continuous.
*(Note: While "units" are discrete, production planning problems of this scale (thousands of hours) typically assume continuous flow or large enough batches that LP relaxation is the standard academic expectation. If integer constraints were required, the problem would usually specify "integer number of units". Given the large available hours (6000-10000), continuous variables are appropriate.)*

### 3. Objective Function

Maximize Total Profit $Z$:

$$
Z = \sum_{p=1}^{3} (S_p \cdot Q_p) - \sum_{p=1}^{3} (r_p \cdot Q_p) - \sum_{m \in M} \sum_{p \in P} (C_m \cdot a_{m,p} \cdot x_{m,p})
$$

Where $Q_p$ is the total quantity of product $p$ produced.
Since every unit produced must pass through both Stage A and Stage B, $Q_p$ is equal to the total flow out of Stage A for product $p$ (which equals the total flow into Stage B).

Let's expand the terms:

**Revenue:**
$1.25 (\sum_{m \in M_A} x^A_{m,1}) + 2.00 (\sum_{m \in M_A} x^A_{m,2}) + 2.80 (\sum_{m \in M_A} x^A_{m,3})$

**Raw Material Cost:**
$0.25 (\sum_{m \in M_A} x^A_{m,1}) + 0.35 (\sum_{m \in M_A} x^A_{m,2}) + 0.50 (\sum_{m \in M_A} x^A_{m,3})$

**Net Contribution per Unit (before processing):**
*   Prod I: $1.25 - 0.25 = 1.00$
*   Prod II: $2.00 - 0.35 = 1.65$
*   Prod III: $2.80 - 0.50 = 2.30$

**Processing Cost (Variable):**
Sum over all machines $m$ of $C_m \cdot a_{m,p} \cdot x_{m,p}$.

*   $A_1$: $0.05 \cdot 5 \cdot x^A_{A_1,1} + 0.05 \cdot 10 \cdot x^A_{A_1,2} = 0.25 x^A_{A_1,1} + 0.50 x^A_{A_1,2}$
*   $A_2$: $0.03 \cdot 7 \cdot x^A_{A_2,1} + 0.03 \cdot 9 \cdot x^A_{A_2,2} + 0.03 \cdot 12 \cdot x^A_{A_2,3} = 0.21 x^A_{A_2,1} + 0.27 x^A_{A_2,2} + 0.36 x^A_{A_2,3}$
*   $B_1$: $0.06 \cdot 6 \cdot x^B_{B_1,1} + 0.06 \cdot 8 \cdot x^B_{B_1,2} = 0.36 x^B_{B_1,1} + 0.48 x^B_{B_1,2}$
*   $B_2$: $0.11 \cdot 4 \cdot x^B_{B_2,1} + 0.11 \cdot 11 \cdot x^B_{B_2,3} = 0.44 x^B_{B_2,1} + 1.21 x^B_{B_2,3}$
*   $B_3$: $0.05 \cdot 7 \cdot x^B_{B_3,1} = 0.35 x^B_{B_3,1}$

**Full Objective Function:**

$$
\begin{aligned}
\text{Max } Z = \quad & 1.00 (x^A_{A_1,1} + x^A_{A_2,1}) + 1.65 (x^A_{A_1,2} + x^A_{A_2,2}) + 2.30 (x^A_{A_2,3}) \\
& - [ 0.25 x^A_{A_1,1} + 0.50 x^A_{A_1,2} + 0.21 x^A_{A_2,1} + 0.27 x^A_{A_2,2} + 0.36 x^A_{A_2,3} ] \\
& - [ 0.36 x^B_{B_1,1} + 0.48 x^B_{B_1,2} + 0.44 x^B_{B_2,1} + 1.21 x^B_{B_2,3} + 0.35 x^B_{B_3,1} ]
\end{aligned}
$$

**Simplified Coefficients:**

*   **Product I:**
    *   $x^A_{A_1,1}$: $1.00 - 0.25 = 0.75$
    *   $x^A_{A_2,1}$: $1.00 - 0.21 = 0.79$
    *   $x^B_{B_1,1}$: $-0.36$
    *   $x^B_{B_2,1}$: $-0.44$
    *   $x^B_{B_3,1}$: $-0.35$
*   **Product II:**
    *   $x^A_{A_1,2}$: $1.65 - 0.50 = 1.15$
    *   $x^A_{A_2,2}$: $1.65 - 0.27 = 1.38$
    *   $x^B_{B_1,2}$: $-0.48$
*   **Product III:**
    *   $x^A_{A_2,3}$: $2.30 - 0.36 = 1.94$
    *   $x^B_{B_2,3}$: $-1.21$

$$
\begin{aligned}
\text{Max } Z = \quad & 0.75 x^A_{A_1,1} + 0.79 x^A_{A_2,1} - 0.36 x^B_{B_1,1} - 0.44 x^B_{B_2,1} - 0.35 x^B_{B_3,1} \\
& + 1.15 x^A_{A_1,2} + 1.38 x^A_{A_2,2} - 0.48 x^B_{B_1,2} \\
& + 1.94 x^A_{A_2,3} - 1.21 x^B_{B_2,3}
\end{aligned}
$$

### 4. Operational Constraints

**1. Flow Balance Constraints (Conservation of Mass):**
The quantity of each product entering Stage B must equal the quantity leaving Stage A.

*   **Product I:**
    $$ x^A_{A_1,1} + x^A_{A_2,1} = x^B_{B_1,1} + x^B_{B_2,1} + x^B_{B_3,1} $$
*   **Product II:**
    $$ x^A_{A_1,2} + x^A_{A_2,2} = x^B_{B_1,2} $$
    *(Note: Based on table data, only $B_1$ is feasible for II in Stage B)*
*   **Product III:**
    $$ x^A_{A_2,3} = x^B_{B_2,3} $$
    *(Note: Based on table data, only $B_2$ is feasible for III in Stage B)*

**2. Machine Capacity Constraints:**
Total processing time on each machine cannot exceed available hours.

*   **Machine $A_1$:**
    $$ 5 x^A_{A_1,1} + 10 x^A_{A_1,2} \le 6000 $$
*   **Machine $A_2$:**
    $$ 7 x^A_{A_2,1} + 9 x^A_{A_2,2} + 12 x^A_{A_2,3} \le 10000 $$
*   **Machine $B_1$:**
    $$ 6 x^B_{B_1,1} + 8 x^B_{B_1,2} \le 4000 $$
*   **Machine $B_2$:**
    $$ 4 x^B_{B_2,1} + 11 x^B_{B_2,3} \le 7000 $$
*   **Machine $B_3$:**
    $$ 7 x^B_{B_3,1} \le 4000 $$

**3. Non-negativity Constraints:**

$$
\begin{aligned}
& x^A_{A_1,1}, x^A_{A_2,1}, x^A_{A_1,2}, x^A_{A_2,2}, x^A_{A_2,3} \ge 0 \\
& x^B_{B_1,1}, x^B_{B_2,1}, x^B_{B_3,1}, x^B_{B_1,2}, x^B_{B_2,3} \ge 0
\end{aligned}
$$

### Notes on Data Conflict Resolution
The problem statement text states Product II can be processed in Stage B *only* on $B_2$. However, the provided Table 1-20 lists a processing time of **8 hours** for Product II on **$B_1$** and leaves **$B_2$ blank** for Product II.
*   According to the **DATA COMPLETENESS CHECK** and **MACHINE ASSIGNMENT** rules, the Table is the primary source for numerical parameters.
*   A blank cell is treated as **Infeasible**.
*   Therefore, the model assumes Product II is processed on **$B_1$** in Stage B.
*   If the text is correct and the table has a typo (i.e., the '8' should be under $B_2$), the model would need to shift the variable $x^B_{B_1,2}$ to $x^B_{B_2,2}$, change the coefficient in the objective to $0.11 \times 8 = 0.88$, and add $8 x^B_{B_2,2}$ to the $B_2$ capacity constraint. However, without explicit instruction to override the table's numerical placement, the table's explicit "8" under $B_1$ is the most defensible data point.