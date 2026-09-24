# Mathematical Optimization Model: Loan Fund Planning

## 1. Index Sets & Parameters

**Sets:**
- $T = \{1, 2, 3, 4\}$: Set of years (2003, 2004, 2005, 2006). Let $t=1$ correspond to 2003, $t=2$ to 2004, etc.
- $B = \{A, B, C\}$: Set of bond investment options.

**Parameters:**
- $D_t$: Loan amount required at the beginning of year $t$ (in thousands of dollars).
  - $D_1 = 100$ (2003)
  - $D_2 = 150$ (2004)
  - $D_3 = 120$ (2005)
  - $D_4 = 110$ (2006)
- $U_b$: Maximum investment limit for bond $b$ (in thousands of dollars).
  - $U_A = 60$ (Bond A, 3-year term)
  - $U_B = 90$ (Bond B, 2-year term)
  - $U_C = 50$ (Bond C, 2-year term)
- $R_b$: Total return multiplier for bond $b$ upon maturity.
  - $R_A = 1.40$ (140%)
  - $R_B = 1.25$ (125%)
  - $R_C = 1.30$ (130%)
- $r_{bank} = 1.04$: Bank interest rate (4%).

**Maturity Schedule (Cash Inflow Timing):**
- **Bond A**: Purchased at $t=1$, matures at $t=4$ (3 years later). Return $1.40 x_A$ received at beginning of 2006 ($t=4$).
- **Bond B**: Purchased at $t=1$, matures at $t=3$ (2 years later). Return $1.25 x_B$ received at beginning of 2005 ($t=3$).
- **Bond C**: Purchased at $t=2$, matures at $t=4$ (2 years later). Return $1.30 x_C$ received at beginning of 2006 ($t=4$).
- **Bank Deposits**: Deposits made at the beginning of year $t$ earn 4% interest and are available at the **end** of year $t$ (or equivalently, the beginning of year $t+1$).
  - Let $y_t$ be the amount deposited in the bank at the beginning of year $t$.
  - The return $1.04 y_t$ is available at the beginning of year $t+1$ for $t=1,2,3$.
  - Note: Funds needed for loans are drawn at the *beginning* of the year. The bank interest is paid at the *end* of the year. This implies the bank return from year $t$ is available to pay for the loan in year $t+1$.

## 2. Decision Variables

Let all variables represent monetary amounts in thousands of dollars.

- $F$: Total funds raised at the end of 2002 (Decision Variable to Minimize).
- $x_A$: Amount invested in Bond A at the beginning of 2003.
- $x_B$: Amount invested in Bond B at the beginning of 2003.
- $x_C$: Amount invested in Bond C at the beginning of 2004.
- $y_1$: Amount deposited in the bank at the beginning of 2003.
- $y_2$: Amount deposited in the bank at the beginning of 2004.
- $y_3$: Amount deposited in the bank at the beginning of 2005.
  - *Note: No bank deposit is needed/modeled for the beginning of 2006 ($t=4$) because the horizon ends with the final loan payment, and there is no subsequent period to earn interest on funds sitting idle after the last payment. Any surplus after the last payment in 2006 is irrelevant to the minimization of initial capital.*

**Domains:**
- $F, x_A, x_B, x_C, y_1, y_2, y_3 \ge 0$ (Continuous variables)

## 3. Objective Function

Minimize the total initial capital raised:
$$ \min Z = F $$

## 4. Operational Constraints

### Cash Flow Constraints
For each year $t$, the total funds available at the beginning of the year must be sufficient to cover the loan requirement $D_t$ and any investments (bonds + bank deposits) made at that time.

**Year 2003 ($t=1$):**
Available funds: $F$ (initial raise).
Uses: Loan $D_1$, Bond A ($x_A$), Bond B ($x_B$), Bank ($y_1$).
$$ F \ge D_1 + x_A + x_B + y_1 $$
$$ F - x_A - x_B - y_1 \ge 100 $$

**Year 2004 ($t=2$):**
Available funds: Bank return from $y_1$ ($1.04 y_1$).
Uses: Loan $D_2$, Bond C ($x_C$), Bank ($y_2$).
$$ 1.04 y_1 \ge D_2 + x_C + y_2 $$
$$ 1.04 y_1 - x_C - y_2 \ge 150 $$

**Year 2005 ($t=3$):**
Available funds: Bank return from $y_2$ ($1.04 y_2$) + Bond B maturity ($1.25 x_B$).
Uses: Loan $D_3$, Bank ($y_3$).
$$ 1.04 y_2 + 1.25 x_B \ge D_3 + y_3 $$
$$ 1.04 y_2 + 1.25 x_B - y_3 \ge 120 $$

**Year 2006 ($t=4$):**
Available funds: Bank return from $y_3$ ($1.04 y_3$) + Bond A maturity ($1.40 x_A$) + Bond C maturity ($1.30 x_C$).
Uses: Loan $D_4$.
$$ 1.04 y_3 + 1.40 x_A + 1.30 x_C \ge D_4 $$
$$ 1.04 y_3 + 1.40 x_A + 1.30 x_C \ge 110 $$

### Investment Limit Constraints
$$ x_A \le 60 $$
$$ x_B \le 90 $$
$$ x_C \le 50 $$

### Non-negativity
$$ F, x_A, x_B, x_C, y_1, y_2, y_3 \ge 0 $$

---

### Summary of the Linear Program

**Minimize:**
$$ F $$

**Subject to:**
1.  $F - x_A - x_B - y_1 \ge 100$
2.  $1.04 y_1 - x_C - y_2 \ge 150$
3.  $1.04 y_2 + 1.25 x_B - y_3 \ge 120$
4.  $1.04 y_3 + 1.40 x_A + 1.30 x_C \ge 110$
5.  $x_A \le 60$
6.  $x_B \le 90$
7.  $x_C \le 50$
8.  $F, x_A, x_B, x_C, y_1, y_2, y_3 \ge 0$