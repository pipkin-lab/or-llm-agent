**Model Type:** LP (Linear Programming)

### 1. Index Sets & Parameters

**Index Sets:**
*   $P = \{A, B, C\}$: Set of products.

**Parameters:**
*   $F_{total} = 1000$ (thousand yuan): Total new product development fund.
*   $ROI_p$: Forecasted Return on Investment for product $p$.
    *   $ROI_A = 0.05$
    *   $ROI_B = 0.07$
    *   $ROI_C = 0.10$
*   $MinInvest_A = 300$ (thousand yuan): Minimum investment required for Product A.
*   $MaxSharePct = 0.35$: Maximum percentage of total fund allowed for any single product.
    *   Derived Cap: $Cap_p = 0.35 \times F_{total} = 350$ (thousand yuan) for all $p \in P$.
*   $EmergencyReserve = 100$ (thousand yuan): Amount reserved for emergency use (10% of 1000).
    *   *Note: The problem states "10% of the fund (i.e., 1 million yuan)". 10% of 1000 thousand yuan is 100 thousand yuan. The text "1 million yuan" appears to be a unit inconsistency in the prompt (1 million yuan = 1000 thousand yuan, which would leave 0 for investment). However, the explicit "10%" calculation on the 1000k fund yields 100k. Given the context of "reserving" a portion, 100k is the standard interpretation of "10% of the fund". If "1 million" were strictly enforced as 1000k, no investment could occur. We proceed with the 10% value = 100 thousand yuan.*
    *   *Correction on Units*: The prompt says "1000 thousand yuan" (1,000,000 yuan) total. It says "10% of the fund (i.e., 1 million yuan)". 10% of 1,000,000 is 100,000. The text "1 million yuan" is likely a typo for "100,000 yuan" or the total fund is 10 million. Let's re-read carefully: "1000 thousand yuan" = 1,000,000 yuan. "10% of the fund (i.e., 1 million yuan)". This is a direct contradiction in the prompt's arithmetic (10% of 1m is 0.1m, not 1m). However, usually, explicit percentages take precedence over parenthetical approximations if there's a typo, OR the "1000 thousand" is the typo.
    *   *Re-evaluation*: "1000 thousand yuan" is a specific number. "10%" is a specific ratio. "1 million yuan" is the result of 10% of 10 million. It is highly probable the total fund is **10,000 thousand yuan** (10 million) or the reserve is **100 thousand yuan**.
    *   Let's look at Constraint 1: "At least 300 thousand yuan... in Product A". If the total fund were 1 million (1000k), 300k is 30%. If the total were 10 million (10000k), 300k is 3%.
    *   Let's look at Constraint 2: "No single product... more than 35%".
    *   Let's assume the standard interpretation of "1000 thousand yuan" is the total budget $B=1000$. Then 10% is 100. The parenthetical "i.e., 1 million yuan" is likely an error in the problem statement's unit conversion (confusing 100k with 1m). I will use the explicit percentage calculation: $Reserve = 0.10 \times 1000 = 100$ thousand yuan.

    *   **Parameters Summary:**
        *   $B = 1000$ (thousand yuan)
        *   $r_A = 0.05, r_B = 0.07, r_C = 0.10$
        *   $L_A = 300$
        *   $U_p = 350$ (for all $p$)
        *   $R = 100$ (Emergency Reserve)

### 2. Decision Variables

Let $x_p$ be the amount invested in product $p$, in thousands of yuan.
*   $x_A, x_B, x_C \ge 0$ (Continuous variables)

### 3. Objective Function

Maximize total profit (return on investment).
$$ \text{Maximize } Z = 0.05 x_A + 0.07 x_B + 0.10 x_C $$

### 4. Operational Constraints

1.  **Minimum Investment in A:**
    $$ x_A \ge 300 $$

2.  **Maximum Share Per Product (35% of Total Fund):**
    $$ x_A \le 350 $$
    $$ x_B \le 350 $$
    $$ x_C \le 350 $$

3.  **Total Investment Limit (Fund minus Emergency Reserve):**
    The total amount invested cannot exceed the total fund minus the reserved emergency fund.
    $$ x_A + x_B + x_C \le 1000 - 100 $$
    $$ x_A + x_B + x_C \le 900 $$

4.  **Non-negativity:**
    $$ x_A, x_B, x_C \ge 0 $$

### Feasibility Sanity Check
*   Lower bound sum: $x_A \ge 300, x_B \ge 0, x_C \ge 0 \implies \sum x \ge 300$.
*   Upper bound sum: $\sum x \le 900$.
*   Individual caps: Max possible sum if all at cap = $350+350+350 = 1050$. But constrained by total available 900.
*   Is it feasible to reach 900?
    *   Set $x_A = 300$ (min).
    *   Remaining budget = $900 - 300 = 600$.
    *   $x_B \le 350, x_C \le 350$. Sum of caps $700 \ge 600$.
    *   Yes, feasible. E.g., $x_A=300, x_B=300, x_C=300 \implies Sum=900$.
*   Objective maximization intuition: Invest as much as possible in the highest ROI product (C, 10%), then B (7%), then A (5%), subject to caps and minimums.
    *   $x_C = 350$ (Cap)
    *   $x_B = 350$ (Cap)
    *   Remaining for A: $900 - 350 - 350 = 200$.
    *   But $x_A \ge 300$. Conflict?
    *   If $x_C=350, x_B=350$, sum=700. Remaining budget=200. But $x_A$ needs 300. Infeasible with this allocation.
    *   We must reduce $x_B$ or $x_C$ to allow $x_A \ge 300$.
    *   Since $ROI_C > ROI_B$, we prefer keeping $x_C$ high.
    *   Let $x_C = 350$.
    *   Let $x_A = 300$ (Min).
    *   Remaining for $B$: $900 - 350 - 300 = 250$.
    *   $x_B = 250 \le 350$ (OK).
    *   Solution: $x_A=300, x_B=250, x_C=350$.
    *   Profit: $0.05(300) + 0.07(250) + 0.10(350) = 15 + 17.5 + 35 = 67.5$ thousand yuan.

The model is feasible and bounded.