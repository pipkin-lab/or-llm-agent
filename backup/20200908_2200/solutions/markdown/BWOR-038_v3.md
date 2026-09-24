# Operations Research Model: Production Planning for Hongsheng Factory

## 1. Problem Analysis & Data Verification

**Objective:** Maximize Total Profit.
**Profit Definition:** $\text{Profit} = \text{Total Revenue} - \text{Total Costs}$.
*   **Revenue:** Selling Price $\times$ Units Produced.
*   **Costs:**
    1.  Raw Material Cost (per unit).
    2.  Processing Cost (per hour $\times$ Hours Used).

**Data Extraction from Table 1-20:**

*   **Products:** $P_1$ (I), $P_2$ (II), $P_3$ (III).
*   **Machines:**
    *   Stage A: $A_1, A_2$
    *   Stage B: $B_1, B_2, B_3$
*   **Processing Times (hours/unit):**
    *   *Product I:* Can use any A ($A_1, A_2$) and any B ($B_1, B_2, B_3$).
        *   $t_{I, A1}=5, t_{I, A2}=7, t_{I, B1}=6, t_{I, B2}=4, t_{I, B3}=7$.
    *   *Product II:* Can use any A ($A_1, A_2$), but **only** $B_2$ for Stage B.
        *   $t_{II, A1}=10, t_{II, A2}=9, t_{II, B2}=8$. (Note: Table shows "8" under Product II for row B1? Let's re-read carefully.
        *   *Re-reading Table Row B1:* Product I=6, Product II=8, Product III=blank.
        *   *Re-reading Table Row B2:* Product I=4, Product II=**blank**, Product III=11.
        *   *Re-reading Table Row B3:* Product I=7, Product II=**blank**, Product III=**blank**.
        *   *Conflict Check:* The text says "Product II ... in stage B it can only be processed on machine B2". However, the table shows a processing time of **8** for Product II on machine **B1** and blank for B2 and B3.
        *   *Resolution:* In standard OR problem conventions, a blank cell usually implies "cannot be processed" or "infinite time/infeasible". However, the text explicitly states "Product II ... can only be processed on machine B2".
        *   Let's look at the table again.
            *   Row B1: Prod I=6, Prod II=8, Prod III=(blank).
            *   Row B2: Prod I=4, Prod II=(blank), Prod III=11.
            *   Row B3: Prod I=7, Prod II=(blank), Prod III=(blank).
        *   There is a direct contradiction between the text description ("Product II... only on B2") and the table data (Time 8 on B1, Blank on B2).
        *   *Standard Interpretation Strategy:* Usually, explicit text constraints override implicit table blanks if the blank is ambiguous, OR the table is the source of truth for parameters and the text describes the *intended* logic which might have a typo in the table or text.
        *   Let's look at Product III. Text: "Product III can only be processed on A2 and B2".
            *   Table A2: Prod III = 12. (Matches).
            *   Table B2: Prod III = 11. (Matches).
            *   Table A1: Prod III = (blank).
            *   Table B1, B3: Prod III = (blank).
            *   This matches perfectly.
        *   Let's look at Product I. Text: "any machine in both stages".
            *   Table A1: 5, A2: 7.
            *   Table B1: 6, B2: 4, B3: 7.
            *   This matches perfectly.
        *   Let's look at Product II again.
            *   Text: "any A machine" -> Table A1: 10, A2: 9. (Matches).
            *   Text: "stage B ... only on B2".
            *   Table B1: 8. Table B2: (blank). Table B3: (blank).
        *   *Hypothesis:* It is highly likely that the value "8" in the table for Product II / Machine B1 is a typo or misalignment, and the blank in B2 is the error, OR the text is correct and the table entry for B1 should be ignored/zero, while B2 should have a value.
        *   *Alternative Hypothesis:* The text is wrong and the table is right? If the table is right, Product II can only be processed on B1 (Time 8). But the text says "only on B2".
        *   *Most Likely Scenario in Textbooks:* Often, blanks mean "not allowed". If the table has an 8 on B1 and blank on B2, it implies Product II is processed on B1. The text saying "only on B2" contradicts the table's "8 on B1".
        *   *Decision:* I will follow the **Table Data** for processing times because specific numerical parameters in tables are usually the ground truth for calculation, while descriptive text might contain a typo regarding the machine ID (confusing B1 and B2). **HOWEVER**, looking closely at the provided HTML table structure:
            `<tr><td>B1</td><td>6</td><td>8</td><td></td>...` -> Prod II on B1 is 8.
            `<tr><td>B2</td><td>4</td><td></td><td>11</td>...` -> Prod II on B2 is blank.
            
            If I strictly follow the table, Product II can only be processed on $B_1$ in Stage B.
            If I strictly follow the text, Product II can only be processed on $B_2$ in Stage B.
            
            Let's check the costs.
            Cost B1 = 0.06. Cost B2 = 0.11.
            If the text is correct (Use B2), the cost is higher. If the table is correct (Use B1), the cost is lower.
            
            *Correction/Refinement:* In many such problems, a blank means "infeasible". If the text says "only on B2", it is a hard constraint. The table showing "8" on B1 might be a distractor or a typo in the problem source. However, without a processing time for B2, we cannot calculate the cost if we force it to B2. **Wait**, if the cell is blank, we don't know the time. We cannot formulate a constraint with an unknown parameter.
            
            Let's re-read the table carefully.
            Row B1: I=6, II=8, III=blank.
            Row B2: I=4, II=blank, III=11.
            
            Is it possible the columns are misaligned?
            Headers: I, II, III.
            Row B1: 6 (I), 8 (II), blank (III).
            Row B2: 4 (I), blank (II), 11 (III).
            
            If the text is correct ("II only on B2"), then the table MUST have a value for II on B2. It has a blank.
            If the table is correct ("II on B1"), then the text has a typo ("B2" should be "B1").
            
            Given that "8" is a specific number and "blank" is an absence, it is safer to assume the **Table represents the feasible set**. The text description "Product II ... only on B2" is likely a typo for "Product II ... only on B1" OR the table entry "8" under B1 for Product II is the valid one, and the text is wrong.
            
            **BUT**, let's look at Product III. Text: "only on A2 and B2". Table: A2 has 12, B2 has 11. Blanks elsewhere. This is consistent.
            
            Let's look at the source of this problem (common OR textbook problem). In many versions of this specific "Hongsheng Factory" problem, **Product II is processed on B2**. If so, the table in the prompt might have a transcription error where the "8" is in the wrong cell or the blank is in the wrong cell.
            
            *However*, as an AI, I must model what is given.
            **Assumption:** The table is the primary source for parameters.
            - Product II, Stage B: Feasible on $B_1$ (Time=8). Not feasible on $B_2, B_3$ (Blank).
            - *Contradiction Handling:* The text says "only on B2". This is a major conflict.
            - *Let's look at the costs again.*
            - If I assume the text is right, I lack the processing time for II on B2. I cannot solve it.
            - If I assume the table is right, I have all data. The text contains a typo ("B2" instead of "B1").
            - *Decision:* I will model based on the **Table Data** (Product II uses $B_1$) because it provides a complete, solvable parameter set. I will add a note about this discrepancy. *Self-Correction*: Actually, looking at the layout, sometimes "8" under B1 for Product II is correct, and the text is just wrong. Or, more likely, the "8" belongs to B2? No, it's clearly in the B1 row.
            
            *Alternative Interpretation:* Maybe the columns are shifted?
            Row B1: 6, 8, (blank).
            Row B2: 4, (blank), 11.
            If the blank in B2 for Product II is actually meant to be the "8"? No, the 8 is in B1.
            
            Let's try one more check. Is it possible Product II uses **both** B1 and B2? No, "only on...".
            
            **Final Decision for Modeling:** I will follow the **Table** strictly.
            - Product II can be processed on $A_1, A_2$ in Stage A.
            - Product II can be processed on $B_1$ in Stage B (Time = 8).
            - *Note:* The text stating "only on B2" contradicts the table. Given the table provides the specific time "8" for B1 and "blank" for B2, and "blank" implies infeasibility, I will assume **Product II is processed on $B_1$**. (If the intended answer relies on B2, the problem is unsolvable as stated due to missing time parameter).

**Parameters Summary:**

| Machine | Product I Time | Product II Time | Product III Time | Avail Hours | Cost (yuan/hr) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| $A_1$ | 5 | 10 | - | 6,000 | 0.05 |
| $A_2$ | 7 | 9 | 12 | 10,000 | 0.03 |
| $B_1$ | 6 | 8 | - | 4,000 | 0.06 |
| $B_2$ | 4 | - | 11 | 7,000 | 0.11 |
| $B_3$ | 7 | - | - | 4,000 | 0.05 |

*   **Raw Material Cost ($c_{RM}$):**
    *   $P_1$: 0.25
    *   $P_2$: 0.35
    *   $P_3$: 0.50
*   **Selling Price ($p$):**
    *   $P_1$: 1.25
    *   $P_2$: 2.00
    *   $P_3$: 2.80

## 2. Index Sets & Parameters

**Sets:**
*   $P = \{1, 2, 3\}$: Set of products (I, II, III).
*   $M_A = \{A_1, A_2\}$: Set of Stage A machines.
*   $M_B = \{B_1, B_2, B_3\}$: Set of Stage B machines.
*   $M = M_A \cup M_B$: Set of all machines.

**Parameters:**
*   $T_{i, m}$: Processing time (hours) of product $i$ on machine $m$. If not specified in the table (blank), $T_{i, m} = \infty$ (infeasible) or the variable is not defined/forced to 0.
    *   *Specific Values:*
        *   $T_{1, A1}=5, T_{1, A2}=7, T_{1, B1}=6, T_{1, B2}=4, T_{1, B3}=7$
        *   $T_{2, A1}=10, T_{2, A2}=9, T_{2, B1}=8$ (Based on table correction/interpretation)
        *   $T_{3, A2}=12, T_{3, B2}=11$
*   $H_m$: Available hours on machine $m$.
    *   $H_{A1}=6000, H_{A2}=10000, H_{B1}=4000, H_{B2}=7000, H_{B3}=4000$.
*   $C_m$: Processing cost (yuan/hour) on machine $m$.
    *   $C_{A1}=0.05, C_{A2}=0.03, C_{B1}=0.06, C_{B2}=0.11, C_{B3}=0.05$.
*   $R_i$: Raw material cost (yuan/unit) for product $i$.
    *   $R_1=0.25, R_2=0.35, R_3=0.50$.
*   $S_i$: Selling price (yuan/unit) for product $i$.
    *   $S_1=1.25, S_2=2.00, S_3=2.80$.

## 3. Decision Variables

Let $x_{i, m}$ be the number of units of product $i$ processed on machine $m$.
Since each product must undergo Stage A and Stage B exactly once, we define variables for each feasible machine-product pair.

**Stage A Variables:**
*   $x_{1, A1}, x_{1, A2}$: Units of Product I on $A_1, A_2$.
*   $x_{2, A1}, x_{2, A2}$: Units of Product II on $A_1, A_2$.
*   $x_{3, A2}$: Units of Product III on $A_2$. (Only feasible on $A_2$).

**Stage B Variables:**
*   $x_{1, B1}, x_{1, B2}, x_{1, B3}$: Units of Product I on $B_1, B_2, B_3$.
*   $x_{2, B1}$: Units of Product II on $B_1$. (Based on table data; *Note: Text says B2, Table says B1. Model uses Table.*).
*   $x_{3, B2}$: Units of Product III on $B_2$. (Only feasible on $B_2$).

**Total Production Variables (for convenience/objective):**
*   $X_i$: Total units of product $i$ produced.
    *   $X_1 = x_{1, A1} + x_{1, A2} = x_{1, B1} + x_{1, B2} + x_{1, B3}$
    *   $X_2 = x_{2, A1} + x_{2, A2} = x_{2, B1}$
    *   $X_3 = x_{3, A2} = x_{3, B2}$

**Domain:**
*   $x_{i, m} \ge 0$ (Continuous variables are assumed unless integer production is specified; typically production quantities in such LP contexts are continuous or integer. Given the large scale, LP is standard. If integer is required, add $\mathbb{Z}^+$). *Assumption: Continuous non-negative real numbers.*

## 4. Objective Function

Maximize Total Profit $Z$.

$$ Z = \sum_{i \in P} X_i (S_i - R_i) - \sum_{m \in M} (\text{Total Hours on } m) \times C_m $$

Expanding the terms:

**Revenue - Raw Material Cost (Contribution Margin per unit):**
*   Product I: $1.25 - 0.25 = 1.00$
*   Product II: $2.00 - 0.35 = 1.65$
*   Product III: $2.80 - 0.50 = 2.30$

**Processing Costs:**
*   Cost = $\sum_{i,m} x_{i,m} T_{i,m} C_m$

**Objective Function:**
$$
\begin{aligned}
\text{Maximize } Z = & \; 1.00 X_1 + 1.65 X_2 + 2.30 X_3 \\
& - [ 5(0.05)x_{1,A1} + 7(0.03)x_{1,A2} \\
& + 10(0.05)x_{2,A1} + 9(0.03)x_{2,A2} \\
& + 12(0.03)x_{3,A2} \\
& + 6(0.06)x_{1,B1} + 4(0.11)x_{1,B2} + 7(0.05)x_{1,B3} \\
& + 8(0.06)x_{2,B1} \\
& + 11(0.11)x_{3,B2} ]
\end{aligned}
$$

Simplifying the processing cost coefficients:
*   $A_1, P1: 5 \times 0.05 = 0.25$
*   $A_2, P1: 7 \times 0.03 = 0.21$
*   $A_1, P2: 10 \times 0.05 = 0.50$
*   $A_2, P2: 9 \times 0.03 = 0.27$
*   $A_2, P3: 12 \times 0.03 = 0.36$
*   $B_1, P1: 6 \times 0.06 = 0.36$
*   $B_2, P1: 4 \times 0.11 = 0.44$
*   $B_3, P1: 7 \times 0.05 = 0.35$
*   $B_1, P2: 8 \times 0.06 = 0.48$
*   $B_2, P3: 11 \times 0.11 = 1.21$

**Final Objective:**
$$
\text{Max } Z = 1.00 X_1 + 1.65 X_2 + 2.30 X_3 - (0.25 x_{1,A1} + 0.21 x_{1,A2} + 0.50 x_{2,A1} + 0.27 x_{2,A2} + 0.36 x_{3,A2} + 0.36 x_{1,B1} + 0.44 x_{1,B2} + 0.35 x_{1,B3} + 0.48 x_{2,B1} + 1.21 x_{3,B2})
$$

*Note: $X_i$ are defined by the flow balance constraints below.*

## 5. Operational Constraints

### A. Flow Balance Constraints (Conservation of Flow)
Each unit of product must pass through one machine in Stage A and one machine in Stage B.

**Product I:**
1.  Stage A Total = Stage B Total = Total Production $X_1$
    $$ X_1 = x_{1,A1} + x_{1,A2} $$
    $$ X_1 = x_{1,B1} + x_{1,B2} + x_{1,B3} $$
    *(Implies $x_{1,A1} + x_{1,A2} = x_{1,B1} + x_{1,B2} + x_{1,B3}$)*

**Product II:**
2.  Stage A Total = Stage B Total = Total Production $X_2$
    $$ X_2 = x_{2,A1} + x_{2,A2} $$
    $$ X_2 = x_{2,B1} $$
    *(Implies $x_{2,A1} + x_{2,A2} = x_{2,B1}$)*

**Product III:**
3.  Stage A Total = Stage B Total = Total Production $X_3$
    $$ X_3 = x_{3,A2} $$
    $$ X_3 = x_{3,B2} $$
    *(Implies $x_{3,A2} = x_{3,B2}$)*

### B. Machine Capacity Constraints
The total processing time for all products on a specific machine must not exceed the available hours.

**Stage A Machines:**
4.  Machine $A_1$:
    $$ 5 x_{1,A1} + 10 x_{2,A1} \le 6000 $$
5.  Machine $A_2$:
    $$ 7 x_{1,A2} + 9 x_{2,A2} + 12 x_{3,A2} \le 10000 $$

**Stage B Machines:**
6.  Machine $B_1$:
    $$ 6 x_{1,B1} + 8 x_{2,B1} \le 4000 $$
7.  Machine $B_2$:
    $$ 4 x_{1,B2} + 11 x_{3,B2} \le 7000 $$
8.  Machine $B_3$:
    $$ 7 x_{1,B3} \le 4000 $$

### C. Non-negativity Constraints
All decision variables must be non-negative.
$$ x_{i,m} \ge 0 \quad \forall i \in P, m \in M \text{ where } x_{i,m} \text{ is defined} $$
$$ X_i \ge 0 \quad \forall i \in P $$

---

### Summary of the Mathematical Model

**Sets:**
$P=\{1,2,3\}$
$M_A=\{A_1, A_2\}$
$M_B=\{B_1, B_2, B_3\}$

**Variables:**
$x_{1,A1}, x_{1,A2}, x_{1,B1}, x_{1,B2}, x_{1,B3}$
$x_{2,A1}, x_{2,A2}, x_{2,B1}$
$x_{3,A2}, x_{3,B2}$
$X_1, X_2, X_3$

**Objective:**
$$ \text{Max } Z = 1.00 X_1 + 1.65 X_2 + 2.30 X_3 - 0.25 x_{1,A1} - 0.21 x_{1,A2} - 0.50 x_{2,A1} - 0.27 x_{2,A2} - 0.36 x_{3,A2} - 0.36 x_{1,B1} - 0.44 x_{1,B2} - 0.35 x_{1,B3} - 0.48 x_{2,B1} - 1.21 x_{3,B2} $$

**Subject To:**
1.  $X_1 - x_{1,A1} - x_{1,A2} = 0$
2.  $X_1 - x_{1,B1} - x_{1,B2} - x_{1,B3} = 0$
3.  $X_2 - x_{2,A1} - x_{2,A2} = 0$
4.  $X_2 - x_{2,B1} = 0$
5.  $X_3 - x_{3,A2} = 0$
6.  $X_3 - x_{3,B2} = 0$
7.  $5 x_{1,A1} + 10 x_{2,A1} \le 6000$
8.  $7 x_{1,A2} + 9 x_{2,A2} + 12 x_{3,A2} \le 10000$
9.  $6 x_{1,B1} + 8 x_{2,B1} \le 4000$
10. $4 x_{1,B2} + 11 x_{3,B2} \le 7000$
11. $7 x_{1,B3} \le 4000$
12. $x_{i,m} \ge 0, X_i \ge 0$ for all defined variables.