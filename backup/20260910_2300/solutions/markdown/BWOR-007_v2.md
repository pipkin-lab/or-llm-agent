### Index Sets & Parameters

**Index Sets:**
*   $t \in \{1, 2, \dots, 12\}$: Set of months in the planning horizon (January to December).
*   $t^+ = t + 1$: The next month. For $t=12$, the "next month" corresponds to the beginning of the next year.

**Parameters:**
*   $C_t$: Net cash flow for month $t$ (in thousand yuan).
    *   $C = [-12, -10, -8, -10, -4, 5, -7, -2, 15, 12, -7, 45]$
*   $r_{annual}$: Monthly interest rate for the Annual Loan = $0.01$.
*   $r_{short}$: Monthly interest rate for Short-term Monthly Loan = $0.015$.
*   $r_{dep}$: Monthly interest rate for Short-term Deposits = $0.004$.

**Derived Parameters:**
*   $C_{cumulative}$: Cumulative cash flow up to month $t$ without any borrowing or investing, defined as $\sum_{k=1}^{t} C_k$.
    *   However, it is cleaner to track the **Available Cash Balance** directly in the constraints rather than pre-calculating cumulative sums, to handle the timing of loans and deposits correctly.

### Decision Variables

Let the following variables represent the financial activities. All variables are continuous, as monetary amounts are treated as continuous quantities in LP models.

1.  **Annual Loan:**
    *   $A$: Total principal amount of the annual loan (thousand yuan).
        *   *Timing Note:* The problem states it is "Borrowed at the end of the previous year, the full loan amount is received at once." This implies the cash $A$ is available at the **beginning of Month 1**.
        *   Domain: $A \ge 0$

2.  **Short-term Monthly Loans:**
    *   $B_t$: Principal amount of the short-term loan taken at the **beginning** of month $t$ (thousand yuan).
        *   *Timing Note:* Taken at beginning of $t$, repaid with interest at beginning of $t+1$.
        *   Domain: $B_t \ge 0$ for all $t \in \{1, \dots, 12\}$.

3.  **Short-term Deposits:**
    *   $D_t$: Principal amount deposited at the **beginning** of month $t$ (thousand yuan).
        *   *Timing Note:* Deposited at beginning of $t$, withdrawn at **end** of month $t$ (which is effectively the beginning of $t+1$ for cash availability). Earns interest over the month.
        *   Domain: $D_t \ge 0$ for all $t \in \{1, \dots, 12\}$.

4.  **Cash Balance:**
    *   $Cash_t$: The available cash balance at the **end** of month $t$ (which is equivalent to the cash available at the **beginning** of month $t+1$).
        *   Domain: $Cash_t \ge 0$ for all $t \in \{1, \dots, 12\}$.
        *   *Note:* The objective is to maximize the cash available at the beginning of the next year, which is exactly $Cash_{12}$.

### Objective Function

Maximize the total cash available at the beginning of the next year (end of Month 12).

$$
\text{Maximize } Z = Cash_{12}
$$

### Operational Constraints

The core logic is a cash flow balance equation for each month. We must account for:
1.  **Inflows:** Previous month's ending cash, new loans (Annual at start of Jan, Short-term at start of month), deposits withdrawn (from previous month).
2.  **Outflows:** Repayment of short-term loans (principal + interest), deposits made (principal), monthly operating cash flow $C_t$ (if negative, it's an outflow; if positive, it's an inflow).
3.  **Annual Loan Interest:** The problem states "pay 1% interest each month" starting from the end of February. This is slightly ambiguous. Does it mean interest is paid monthly in cash, or accrued? "pay 1% interest each month... and then repay the principal plus the final interest payment at the end of January next year".
    *   *Interpretation:* "Pay 1% interest each month" usually implies a cash outflow for interest. However, the second part says "repay the principal plus the *final* interest payment". This suggests interest might be accrued and paid at the end, OR paid monthly. Let's look closely: "Starting from the end of February... pay 1% interest each month". This implies a cash outflow of $0.01 A$ at the end of Feb, Mar, ..., Dec? Or Jan?
    *   Let's re-read carefully: "Starting from the end of February, the factory must pay 1% interest each month, and then repay the principal plus the final interest payment at the end of January next year".
    *   This phrasing is tricky. Usually, "pay interest each month" means a recurring cash flow. If I pay interest at the end of Feb, Mar, Apr, ..., Dec, and Jan, that's 11 payments? Or is "final interest payment" the Jan one, and the others are just "pay interest"?
    *   Let's assume standard amortization or bullet repayment with monthly interest payments.
    *   Months with interest payment: End of Feb ($t=2$), End of Mar ($t=3$), ..., End of Dec ($t=12$)?
    *   Wait, the loan is for the "upcoming year".
    *   Let's assume the interest is paid in cash at the end of the specified months.
    *   Interest Payments for Annual Loan:
        *   End of Month 2: $0.01 A$
        *   End of Month 3: $0.01 A$
        *   ...
        *   End of Month 12: $0.01 A$?
        *   Beginning of Month 1 (Next Year): Repay Principal $A$ + Final Interest?
        *   Actually, if the loan is for the current year, and repaid "at the end of January next year", the interest periods are likely Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec, Jan.
        *   Let's simplify based on the text "pay 1% interest each month... starting from end of February".
        *   Cash Outflow for Annual Interest:
            *   $t=2$ to $t=12$: Outflow of $0.01 A$.
            *   $t=13$ (End of Jan Next Year): Repayment of Principal $A$ + Final Interest? The problem says "repay the principal plus the final interest payment". This might mean the Jan interest is also paid then, or it's included in the final lump sum.
            *   Since our horizon ends at Month 12, we only care about cash flows *within* the year for the balance constraints. The repayment of Principal $A$ happens *after* our horizon (beginning of next year). Does it reduce $Cash_{12}$?
            *   "Maximize ... cash available at the beginning of next year".
            *   If the loan is repaid at the beginning of next year, that happens *before* we count the final cash? Or is the "cash available" the net position after settling all debts due at that moment?
            *   Usually, "cash available" implies the free cash on hand. If you owe money immediately, your available cash is reduced.
            *   However, the Annual Loan principal is due "at the end of January next year". The Short-term loan from Dec is due "at the beginning of the following month" (Jan).
            *   Let's assume $Cash_{12}$ is the cash *before* the final settlement of the annual principal, or we must deduct the principal if it's due "at the beginning of next year".
            *   "Beginning of next year" = End of Month 12.
            *   So, at $t=12$ (end), we must repay:
                1.  Short-term loan $B_{12}$ (taken start of Dec, due start of Jan) + Interest.
                2.  Annual Loan Principal $A$? The text says "repay the principal... at the end of January next year". This is *after* the beginning of January. So the principal repayment is likely outside the 12-month horizon's immediate "beginning of next year" snapshot, or it occurs at the very end of Jan.
                3.  Let's look at the Short-term loan timing: "repaid at the beginning of the following month". So $B_{12}$ is repaid at the beginning of Month 1 (Next Year). This is exactly the time $Cash_{12}$ represents. So $B_{12}(1+r_{short})$ MUST be deducted from $Cash_{12}$ to find the *net* available cash.
                4.  What about Annual Loan Principal? "End of January next year". This is 1 month later. So we do *not* deduct $A$ from $Cash_{12}$. We only deduct the interest due?
                5.  Interest on Annual Loan: "pay 1% interest each month... starting from end of February".
                    *   End Feb ($t=2$): Pay $0.01 A$.
                    *   End Mar ($t=3$): Pay $0.01 A$.
                    *   ...
                    *   End Dec ($t=12$): Pay $0.01 A$.
                    *   End Jan Next Year: Pay Final Interest + Principal.
                    *   So, in our model (months 1-12), we have cash outflows of $0.01 A$ at the end of months $t=2, 3, \dots, 12$.

**Constraint Equations:**

**1. Cash Balance Recurrence (for $t=1$):**
At the beginning of Month 1:
*   Inflow: Annual Loan $A$.
*   Inflow: Deposit from previous month? No, it's the start.
*   Inflow: Loan $B_1$ (taken at beginning of Month 1).
*   Outflow: Deposit $D_1$ (made at beginning of Month 1).
*   Operating Flow: $C_1$.
*   Outflow: Repayment of $B_0$? No, no prior loans.
*   End of Month 1 Cash ($Cash_1$):
    $$ Cash_1 = A + B_1 - D_1 + C_1 $$
    *(Note: $B_1$ is taken at beg of 1, so it adds to cash. $D_1$ is deposited at beg of 1, so it subtracts from cash.)*

**2. Cash Balance Recurrence (for $t=2, \dots, 12$):**
At the beginning of Month $t$:
*   Inflow: $Cash_{t-1}$ (Cash from end of previous month).
*   Inflow: New Short-term Loan $B_t$.
*   Outflow: Repayment of previous Short-term Loan $B_{t-1}$ with interest ($B_{t-1} \times (1 + r_{short})$).
*   Outflow: Deposit made at beginning of Month $t$, $D_t$.
*   Inflow: Withdrawal of deposit from previous month $D_{t-1}$ with interest ($D_{t-1} \times (1 + r_{dep})$).
*   Operating Flow: $C_t$.
*   Outflow: Annual Loan Interest (if $t \ge 2$): $0.01 A$.
*   End of Month $t$ Cash ($Cash_t$):

$$
Cash_t = Cash_{t-1} + B_t - B_{t-1}(1 + r_{short}) - D_t + D_{t-1}(1 + r_{dep}) + C_t - I_{annual, t}
$$

Where:
*   $I_{annual, t} = 0.01 A$ if $t \in \{2, 3, \dots, 12\}$
*   $I_{annual, 1} = 0$
*   For $t=1$, the formula simplifies to: $Cash_1 = A + B_1 - D_1 + C_1$ (consistent with above if we define $B_0=0, D_0=0, Cash_0=0$).

Let's unify the constraints for all $t=1, \dots, 12$ using dummy variables $B_0=0, D_0=0, Cash_0=0$:

$$
Cash_t = Cash_{t-1} + B_t - (1 + r_{short})B_{t-1} - D_t + (1 + r_{dep})D_{t-1} + C_t - I_t
$$

Subject to:
*   $I_t = 0.01 A$ for $t = 2, \dots, 12$
*   $I_1 = 0$

**3. Non-negativity Constraints:**
*   $Cash_t \ge 0$ for all $t=1, \dots, 12$
*   $A \ge 0$
*   $B_t \ge 0$ for all $t=1, \dots, 12$
*   $D_t \ge 0$ for all $t=1, \dots, 12$

**4. Objective Clarification:**
The objective is to maximize cash at the beginning of next year.
The variable $Cash_{12}$ represents the cash at the **end** of Month 12, which is the **beginning** of Month 1 (Next Year).
Does this cash balance already account for the repayment of $B_{12}$?
Let's check the constraint for $t=12$:
$$ Cash_{12} = Cash_{11} + B_{12} - (1 + r_{short})B_{11} - D_{12} + (1 + r_{dep})D_{11} + C_{12} - 0.01 A $$
This equation calculates the cash *after* all transactions occurring in Month 12 (including taking loan $B_{12}$ and repaying loan $B_{11}$).
However, the loan $B_{12}$ is taken at the **beginning** of Month 12 and repaid at the **beginning** of Month 1 (Next Year).
In our model, $B_{12}$ is added to cash at the start of Month 12. It is *not* subtracted in the $t=12$ balance equation.
Therefore, $Cash_{12}$ includes the principal of the loan $B_{12}$ which is still outstanding.
To find the *net* available cash at the beginning of next year, we must subtract the repayment due for $B_{12}$.
Repayment due at beginning of next year for $B_{12}$ is $B_{12}(1 + r_{short})$.
Also, are there any other debts?
The Annual Loan principal $A$ is due "end of January next year". This is *after* the beginning of January. So we do not subtract $A$.
The Annual Loan interest for January (next year) is due "end of January". Not subtracted.
The Annual Loan interest for Dec was already paid in the $t=12$ constraint.

So, the final objective value $Z$ is:
$$ Z = Cash_{12} - (1 + r_{short})B_{12} $$

Wait, let's re-read the Short-term loan rule: "repaid at the beginning of the following month".
So $B_{12}$ is repaid at the beginning of Month 1 (Next Year).
$B_{11}$ is repaid at the beginning of Month 12. This was handled in the $t=12$ constraint (term $-(1+r_{short})B_{11}$).
So yes, $Cash_{12}$ is the cash on hand *before* repaying $B_{12}$.
Thus, the free cash available is $Cash_{12} - (1 + r_{short})B_{12}$.

**Revised Objective Function:**
$$ \text{Maximize } Z = Cash_{12} - (1 + r_{short})B_{12} $$

**Summary of Constraints:**

1.  **For $t=1$:**
    $$ Cash_1 = A + B_1 - D_1 + C_1 $$
    *(Implicitly $Cash_1 \ge 0$)*

2.  **For $t=2, \dots, 11$:**
    $$ Cash_t = Cash_{t-1} + B_t - (1.015)B_{t-1} - D_t + (1.004)D_{t-1} + C_t - 0.01 A $$
    *(Implicitly $Cash_t \ge 0$)*

3.  **For $t=12$:**
    $$ Cash_{12} = Cash_{11} + B_{12} - (1.015)B_{11} - D_{12} + (1.004)D_{11} + C_{12} - 0.01 A $$
    *(Implicitly $Cash_{12} \ge 0$)*

4.  **Variable Bounds:**
    $$ A, B_1, \dots, B_{12}, D_1, \dots, D_{12} \ge 0 $$
    $$ Cash_1, \dots, Cash_{12} \ge 0 $$

5.  **Objective:**
    $$ \text{Maximize } Cash_{12} - 1.015 B_{12} $$