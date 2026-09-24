### Index Sets & Parameters

**Index Sets:**
*   $T = \{2003, 2004, 2005, 2006\}$: Set of years.

**Parameters (in thousands of dollars):**
*   $D_t$: Loan demand at the beginning of year $t$.
    *   $D_{2003} = 100$
    *   $D_{2004} = 150$
    *   $D_{2005} = 120$
    *   $D_{2006} = 110$
*   $U_{bond}$: Maximum investment limit for each bond.
    *   $U_A = 60$ (Bond A)
    *   $U_B = 90$ (Bond B)
    *   $U_C = 50$ (Bond C)
*   $R_{bond}$: Total return multiplier (principal + interest) upon maturity.
    *   $R_A = 1.40$ (Bond A, matures end of 2005)
    *   $R_B = 1.25$ (Bond B, matures end of 2004)
    *   $R_C = 1.30$ (Bond C, matures end of 2005)
*   $r_{bank}$: Bank annual interest rate = $0.04$.
    *   Bank return multiplier $R_{bank} = 1 + r_{bank} = 1.04$.

### Decision Variables

Let the variables represent the amount of capital allocated to each investment option. Since money is fungible and can be divided, these are **continuous** variables.

1.  **Initial Capital:**
    *   $C$: Total amount of money raised at the end of 2002 (to be minimized).

2.  **Investments (Amounts in thousands of dollars):**
    *   $x_A$: Amount invested in Bond A at the beginning of 2003.
    *   $x_B$: Amount invested in Bond B at the beginning of 2003.
    *   $x_C$: Amount invested in Bond C at the beginning of 2004.
    *   $b_{2003}$: Amount deposited in the bank at the beginning of 2003.
    *   $b_{2004}$: Amount deposited in the bank at the beginning of 2004.
    *   $b_{2005}$: Amount deposited in the bank at the beginning of 2005.
    *   $b_{2006}$: Amount deposited in the bank at the beginning of 2006.

**Domains:**
*   $C \ge 0$
*   $x_A, x_B, x_C, b_{2003}, b_{2004}, b_{2005}, b_{2006} \ge 0$

### Objective Function

Minimize the total initial capital raised:

$$ \text{Minimize } Z = C $$

### Operational Constraints

**1. Cash Flow Balance at the Beginning of Each Year**

The cash available at the beginning of any year $t$ comes from the initial capital (if $t=2003$) or the maturities of investments from previous years. This cash must cover the loan demand $D_t$ for that year, and any surplus is allocated to investments available at that time (Bonds or Bank).

*   **Year 2003 (Beginning):**
    The company has raised $C$. It must pay loan $D_{2003}$. The remaining funds are invested in Bond A, Bond B, or Bank.
    $$ C - D_{2003} = x_A + x_B + b_{2003} $$
    $$ C - 100 = x_A + x_B + b_{2003} $$

*   **Year 2004 (Beginning):**
    Cash inflows:
    - Maturity from Bank deposit in 2003: $1.04 \cdot b_{2003}$
    - *Note: Bond A (3-year) and Bond B (2-year) do not mature yet.*
    Cash outflows:
    - Loan demand $D_{2004}$.
    - Investment in Bond C ($x_C$).
    - Investment in Bank ($b_{2004}$).
    
    $$ 1.04 b_{2003} - D_{2004} = x_C + b_{2004} $$
    $$ 1.04 b_{2003} - 150 = x_C + b_{2004} $$

*   **Year 2005 (Beginning):**
    Cash inflows:
    - Maturity from Bond B (invested start of 2003, 2-year term): $1.25 \cdot x_B$
    - Maturity from Bank deposit in 2004: $1.04 \cdot b_{2004}$
    Cash outflows:
    - Loan demand $D_{2005}$.
    - Investment in Bank ($b_{2005}$).
    - *Note: Bond A (3-year) and Bond C (2-year) do not mature yet.*

    $$ 1.25 x_B + 1.04 b_{2004} - D_{2005} = b_{2005} $$
    $$ 1.25 x_B + 1.04 b_{2004} - 120 = b_{2005} $$

*   **Year 2006 (Beginning):**
    Cash inflows:
    - Maturity from Bond A (invested start of 2003, 3-year term): $1.40 \cdot x_A$
    - Maturity from Bond C (invested start of 2004, 2-year term): $1.30 \cdot x_C$
    - Maturity from Bank deposit in 2005: $1.04 \cdot b_{2005}$
    Cash outflows:
    - Loan demand $D_{2006}$.
    - Investment in Bank ($b_{2006}$).
    - *Note: Any remaining cash after paying the 2006 loan is not needed for project loans, but the problem implies we minimize the initial raise. Usually, in such minimization problems, we assume no leftover cash is required to be "held" unless specified, or we can allow surplus to sit in the bank. However, since the goal is minimizing initial capital, any surplus at the end of 2006 is irrelevant to the constraint as long as the loan is paid. To be precise, the equation balances the cash available against the loan and any final bank deposit. If we assume no money needs to be kept after the project, $b_{2006}$ can be 0, but it's safer to include it in the balance equation allowing it to be non-negative.*

    $$ 1.40 x_A + 1.30 x_C + 1.04 b_{2005} - D_{2006} = b_{2006} $$
    $$ 1.40 x_A + 1.30 x_C + 1.04 b_{2005} - 110 = b_{2006} $$

**2. Investment Limits**

*   Bond A Limit:
    $$ x_A \le 60 $$
*   Bond B Limit:
    $$ x_B \le 90 $$
*   Bond C Limit:
    $$ x_C \le 50 $$

**3. Non-negativity**

$$ C, x_A, x_B, x_C, b_{2003}, b_{2004}, b_{2005}, b_{2006} \ge 0 $$