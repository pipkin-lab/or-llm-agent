**Model Type:** LP (Linear Programming)

### 1. Index Sets & Parameters

**Index Sets:**
- $T = \{1, 2, 3, 4\}$ representing the years 2003, 2004, 2005, 2006.
- $B = \{A, B, C\}$ representing the specific bond investment opportunities.

**Parameters:**
- $D_t$: Loan amount required at the **beginning** of year $t$ (in thousand dollars).
  - $D_1 = 100$ (2003)
  - $D_2 = 150$ (2004)
  - $D_3 = 120$ (2005)
  - $D_4 = 110$ (2006)
- $R_b$: Total return multiplier for bond $b$ (principal + interest).
  - $R_A = 1.40$
  - $R_B = 1.25$
  - $R_C = 1.30$
- $M_b$: Maximum investment limit for bond $b$ (in thousand dollars).
  - $M_A = 60$
  - $M_B = 90$
  - $M_C = 50$
- $r$: Annual bank interest rate = $0.04$.
- $R_{bank} = 1 + r = 1.04$.

### 2. Decision Variables

Let:
- $S$: Total amount of funds raised at the end of 2002 (in thousand dollars). This is the variable to be minimized.
- $x_A, x_B, x_C$: Amount invested in Bond A, B, and C respectively (in thousand dollars).
- $y_1, y_2, y_3, y_4$: Amount of surplus funds deposited in the bank at the **beginning** of years 1, 2, 3, and 4 respectively (in thousand dollars).

**Domains:**
- $S \ge 0$
- $x_A, x_B, x_C \ge 0$
- $y_1, y_2, y_3, y_4 \ge 0$

### 3. Objective Function

Minimize the total initial capital raised:
$$ \text{Minimize } Z = S $$

### 4. Operational Constraints

**Budget Constraints (Cash Flow Balance):**
The funds available at the beginning of each year must cover the loan requirement ($D_t$), any bond purchases initiated that year, and any bank deposits. The funds available are the initial raise ($S$) plus returns from bonds maturing in that year plus interest from the previous year's bank deposit.

*Note on Timing:*
- Bonds purchased at the beginning of Year $t$ return funds at the **beginning** of Year $t + \text{term}$.
  - Bond A (3-year term, bought Start 2003): Returns at Start 2006 (Year 4).
  - Bond B (2-year term, bought Start 2003): Returns at Start 2005 (Year 3).
  - Bond C (2-year term, bought Start 2004): Returns at Start 2006 (Year 4).
- Bank deposits made at the beginning of Year $t$ yield interest at the **end** of Year $t$, which is effectively the **beginning** of Year $t+1$. Thus, $y_t \times 1.04$ is added to the funds available at the start of Year $t+1$.

**Year 1 (2003) Balance:**
Funds Available: $S$ (Initial)
Funds Used: $D_1$ (Loan) + $x_A$ (Bond A) + $x_B$ (Bond B) + $y_1$ (Bank)
$$ S \ge D_1 + x_A + x_B + y_1 $$
$$ S \ge 100 + x_A + x_B + y_1 $$

**Year 2 (2004) Balance:**
Funds Available: $1.04 y_1$ (Return from Bank Year 1)
Funds Used: $D_2$ (Loan) + $x_C$ (Bond C) + $y_2$ (Bank)
*Note: No bonds mature in 2004.*
$$ 1.04 y_1 \ge D_2 + x_C + y_2 $$
$$ 1.04 y_1 \ge 150 + x_C + y_2 $$

**Year 3 (2005) Balance:**
Funds Available: $1.04 y_2$ (Return from Bank Year 2) + $1.25 x_B$ (Bond B matures)
Funds Used: $D_3$ (Loan) + $y_3$ (Bank)
*Note: No new bonds are purchased in 2005 as per the problem description (only A, B at 2003 and C at 2004 are listed).*
$$ 1.04 y_2 + 1.25 x_B \ge D_3 + y_3 $$
$$ 1.04 y_2 + 1.25 x_B \ge 120 + y_3 $$

**Year 4 (2006) Balance:**
Funds Available: $1.04 y_3$ (Return from Bank Year 3) + $1.40 x_A$ (Bond A matures) + $1.30 x_C$ (Bond C matures)
Funds Used: $D_4$ (Loan) + $y_4$ (Bank)
*Note: The problem asks to minimize funds raised at end of 2002. Any surplus remaining at the end of 2006 is not part of the "needed" funds for the project, but the constraint ensures the loan is covered. We do not need to force $y_4=0$, but minimizing $S$ will naturally minimize idle cash if possible, though $y_4$ just acts as a slack variable for the final year's balance.*
$$ 1.04 y_3 + 1.40 x_A + 1.30 x_C \ge D_4 + y_4 $$
$$ 1.04 y_3 + 1.40 x_A + 1.30 x_C \ge 110 + y_4 $$

**Investment Limits:**
$$ x_A \le 60 $$
$$ x_B \le 90 $$
$$ x_C \le 50 $$

**Non-negativity:**
$$ S, x_A, x_B, x_C, y_1, y_2, y_3, y_4 \ge 0 $$

### Summary of Model

**Minimize**
$$ S $$

**Subject to:**
1. $S - x_A - x_B - y_1 \ge 100$
2. $-x_C - y_2 - 1.04 y_1 \le -150$  (Rearranged for standard form clarity, or kept as $1.04 y_1 - x_C - y_2 \ge 150$)
3. $1.25 x_B - y_3 - 1.04 y_2 \ge -120$ (Rearranged: $1.04 y_2 + 1.25 x_B - y_3 \ge 120$)
4. $1.40 x_A + 1.30 x_C - y_4 - 1.04 y_3 \ge -110$ (Rearranged: $1.04 y_3 + 1.40 x_A + 1.30 x_C - y_4 \ge 110$)
5. $x_A \le 60$
6. $x_B \le 90$
7. $x_C \le 50$
8. All variables $\ge 0$