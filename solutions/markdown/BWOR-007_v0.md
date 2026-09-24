**Model Type:** LP (Linear Programming)

### 1. Index Sets & Parameters

**Index Sets:**
- $t \in \{1, 2, \dots, 12\}$: The 12 months of the year.

**Parameters (in thousand yuan):**
- $c_t$: Net cash flow for month $t$.
    - $c_1 = -12$
    - $c_2 = -10$
    - $c_3 = -8$
    - $c_4 = -10$
    - $c_5 = -4$
    - $c_6 = 5$
    - $c_7 = -7$
    - $c_8 = -2$
    - $c_9 = 15$
    - $c_{10} = 12$
    - $c_{11} = -7$
    - $c_{12} = 45$
- $r_A$: Monthly interest rate for Annual Loan = $0.01$.
- $r_S$: Monthly interest rate for Short-term Monthly Loan = $0.015$.
- $r_D$: Monthly interest rate for Short-term Deposit = $0.004$.

### 2. Decision Variables

- $A$: Principal amount of the Annual Loan (continuous, $A \ge 0$).
    - *Note:* This loan is taken at the end of the previous year (start of month 1).
- $B_t$: Principal amount of the Short-term Monthly Loan taken at the beginning of month $t$ (continuous, $B_t \ge 0$ for $t=1,\dots,12$).
- $D_t$: Principal amount of the Short-term Deposit made at the beginning of month $t$ (continuous, $D_t \ge 0$ for $t=1,\dots,12$).
    - *Note:* Deposits are withdrawn at the end of month $t$ (start of month $t+1$).

### 3. Objective Function

Maximize the total cash available at the beginning of next year (start of month 13).

Let $Z$ be the cash available at the beginning of month 13.
The cash available is the sum of:
1.  Cash remaining from month 12 operations.
2.  Principal and interest from the deposit $D_{12}$ (made at start of month 12, withdrawn at end of month 12/start of month 13).
3.  *Note on Repayments:* All loans ($A$ and $B_t$) are fully repaid by the end of month 12 or earlier, so they do not contribute to the final cash balance directly, only through the cash flow constraints. The Annual Loan is repaid at the end of January next year (which is effectively the start of February next year, or simply after the "beginning of next year" snapshot if we define next year as Feb 1st? Let's clarify timing).

**Timing Clarification:**
- "Beginning of next year" usually means the start of Month 1 of the *following* year.
- The Annual Loan is repaid at the **end of January next year**. This is the same time point as the **beginning of February next year**.
- The Short-term loans $B_t$ are repaid at the beginning of month $t+1$. The last one, $B_{12}$, is repaid at the beginning of month 13 (next year, month 1).
- The deposits $D_t$ are withdrawn at the end of month $t$. The last one, $D_{12}$, is withdrawn at the end of month 12 (beginning of next year).

Therefore, the "cash available at the beginning of next year" is the cash on hand after all transactions at the beginning of month 13 (next year's month 1) have been settled, but *before* any new operations of next year.
Actually, let's trace the cash balance $C_t$ at the **beginning** of month $t$.
- $C_1$: Cash at start of Month 1.
- The factory must have $C_t \ge 0$ for all $t$.
- The goal is to maximize the cash at the **beginning of next year**. Let's call this $C_{13}$.

How is $C_{13}$ determined?
At the beginning of month 13:
1.  We receive the principal and interest from deposit $D_{12}$ (deposited at start of month 12, withdrawn at end of month 12). Amount: $D_{12}(1 + r_D)$.
2.  We pay off the short-term loan $B_{12}$ (taken at start of month 12, repaid at start of month 13). Amount: $B_{12}(1 + r_S)$.
3.  We do NOT pay off the Annual Loan $A$ yet? The problem says "repay the principal plus the final interest payment at the end of January next year".
    - End of January next year = Beginning of February next year.
    - The question asks for cash at the **beginning of next year** (Beginning of January next year? Or Beginning of Month 1 of next year? Usually "next year" implies the start of the calendar year, i.e., Month 1).
    - Let's assume "beginning of next year" means the start of Month 1 of the following year.
    - At this specific instant (Start of Month 1, Next Year):
        - We have the cash left over from the end of Month 12 of the current year.
        - We receive $D_{12}(1+r_D)$.
        - We pay $B_{12}(1+r_S)$.
        - The Annual Loan $A$ is still outstanding. It is repaid later (End of Jan Next Year). Does the "cash available" include the ability to borrow or is it just the liquid cash on hand? "Maximize the total amount of cash ... available". This implies liquid cash on hand. The outstanding debt $A$ is a liability, but the cash on hand is what's "available". However, usually in these problems, "cash available" refers to the net cash position or the cash on hand. Given the context of "covering shortfalls", it refers to the cash balance $C_{13}$.
        - Wait, if we are at the start of Month 1 Next Year, we haven't paid the annual loan yet. So the cash on hand is just the residual from previous months plus the deposit return minus the short-term loan repayment.

Let's define the cash balance recursion $C_t$ (cash at the **beginning** of month $t$).

**Initial State (Beginning of Month 1):**
- Receive Annual Loan: $+A$
- Take Short-term Loan: $+B_1$
- Make Deposit: $-D_1$
- Cash Flow $c_1$ occurs during the month? Or is $c_t$ the net change during the month?
  - "Cash flow c ... in that month". Usually means net inflow/outflow during the month.
  - So, Cash at End of Month 1 = $C_1 + A + B_1 - D_1 + c_1$.
  - BUT, loans/deposits have specific timing.
  - "Annual Loan: ... full loan amount is received at once [start of month 1]."
  - "Short-term Monthly Loan: taken at the beginning of any month."
  - "Deposits: made at the beginning of the month, withdrawn at the end of the same month."

Let's refine the timing for Month $t$:
1.  **Beginning of Month $t$**:
    - Cash available from previous period: $C_t$ (Let's redefine $C_t$ as cash at **End** of month $t$ to make it easier, or stick to Beginning).
    - Let $C_t$ = Cash at **Beginning** of Month $t$.
    - Actions at Beginning of Month $t$:
        - Borrow Short-term: $+B_t$
        - Deposit: $-D_t$ (Cash leaves, returns end of month)
        - *Note:* Annual Loan $A$ is only at $t=1$. So $+A$ only if $t=1$.
    - Cash available for operations during Month $t$: $C_t + B_t - D_t + (A \text{ if } t=1)$.
    - This cash must cover the net cash flow requirement?
    - Actually, $c_t$ is the net cash flow. If $c_t$ is negative, we need cash. If positive, we have excess.
    - Constraint: The cash available at the beginning of the month (after borrowing/depositing) must be sufficient to cover the outflows during the month? Or does the cash balance just evolve?
    - Standard formulation:
      $C_{t+1}$ (Cash at End of Month $t$ / Beginning of Month $t+1$)
      $= C_t$ (Start Cash)
      $+ B_t$ (New Short-term Loan)
      $- D_t$ (New Deposit)
      $+ (A \text{ if } t=1)$
      $+ c_t$ (Net Cash Flow of Month $t$)
      $- \text{Repayments of previous short-term loans?}$
      $+ \text{Returns from previous deposits?}$

    Let's trace the flows carefully.
    
    **Month 1:**
    - Start Cash: $C_1$ (Assume 0 initial cash, or is it determined? Usually, we start with 0 or a given amount. The problem doesn't give an initial cash balance. We assume the factory starts with 0 cash, or rather, the decision variables determine the starting position. However, $C_1$ is the cash *before* taking the annual loan?
    - Let's assume the factory starts the year with 0 cash.
    - At Beginning of Month 1:
        - Receive Annual Loan: $+A$.
        - Take Short-term Loan: $+B_1$.
        - Make Deposit: $-D_1$.
        - Cash on hand: $A + B_1 - D_1$.
    - During Month 1, net cash flow is $c_1 = -12$.
    - End of Month 1 Cash: $C_{end,1} = A + B_1 - D_1 + c_1$.
    - Constraint: We need enough cash to cover the outflow. Since $c_1$ is negative, we need $A + B_1 - D_1 \ge -c_1$? Or is $C_{end,1}$ just the balance?
    - The constraint is that the cash balance must never be negative.
    - Also, at the **End** of Month 1 (Beginning of Month 2):
        - Withdraw Deposit $D_1$: $+D_1(1+r_D)$.
        - Repay Short-term Loan $B_1$: $-B_1(1+r_S)$.
        - *Note:* The problem says Short-term loan is repaid at the **beginning** of the following month. So at the transition from Month 1 to Month 2, we pay $B_1(1+r_S)$.
        - The problem says Deposit is withdrawn at the **end** of the same month. So at the transition from Month 1 to Month 2, we receive $D_1(1+r_D)$.
    
    So, the Cash at **Beginning of Month $t+1$** ($C_{t+1}$) is:
    $C_{t+1} = C_{end, t} + \text{Deposits Withdrawn} - \text{Loans Repaid}$
    
    Let's combine everything into a single balance equation for $C_{t+1}$ in terms of $C_t$ and decisions in month $t$.
    
    $C_t$: Cash at Beginning of Month $t$ (before any new borrowing/depositing in month $t$).
    
    **Transactions at Beginning of Month $t$:**
    1. Borrow $B_t$.
    2. Deposit $D_t$.
    3. (If $t=1$, Borrow $A$).
    
    **Cash Available for Month $t$ Operations:**
    $CashAvail_t = C_t + B_t - D_t + (A \cdot \delta_{t,1})$
    
    **End of Month $t$ Balance (before settling previous month's loans/deposits? No, let's settle at the boundary):**
    
    Let's define $C_t$ as the cash in the bank at the **instant** just after all transactions (borrowing, depositing, loan repayment, deposit withdrawal) for the transition from $t-1$ to $t$ have been completed, but **before** the new borrowing/depositing for month $t$.
    
    Actually, it is cleaner to define $C_t$ as the cash balance at the **end** of month $t$.
    
    Let $C_t$ = Cash at **End** of Month $t$.
    
    **Month 1:**
    - Start with 0.
    - Borrow $A$, $B_1$. Deposit $D_1$.
    - Cash available: $A + B_1 - D_1$.
    - Net flow: $c_1$.
    - Cash at End of Month 1 (before settling Month 1's loans/deposits? No, settlements happen at boundaries).
    - Let's say $C_t$ is the cash **available** at the beginning of month $t$ **after** all previous settlements but **before** new month $t$ decisions.
    
    Let's stick to the simplest interpretation used in such textbook problems:
    $C_t$ = Cash balance at the **beginning** of month $t$.
    
    **Constraint for Month $t$:**
    The cash available at the beginning of month $t$ ($C_t$) plus new borrowings ($B_t$) plus annual loan (if $t=1$) minus new deposits ($D_t$) must be sufficient to cover the net cash outflow if $c_t$ is negative?
    Actually, the cash flow $c_t$ is the net change during the month.
    So, Cash at **End** of Month $t$ (let's call it $C_{end,t}$) is:
    $C_{end,t} = C_t + B_t - D_t + (A \text{ if } t=1) + c_t$.
    
    **Transition to Beginning of Month $t+1$ ($C_{t+1}$):**
    At the end of Month $t$ / Beginning of Month $t+1$:
    1. Withdraw Deposit $D_t$: $+D_t(1+r_D)$.
    2. Repay Loan $B_t$: $-B_t(1+r_S)$.
    3. (If $t=12$, repay Annual Loan $A$? No, Annual Loan is repaid at end of Jan *next* year. If our year ends at Month 12 (Dec), then end of Jan next year is *after* the 12 months. So $A$ is NOT repaid in the 12-month horizon. It is repaid later. So no repayment of $A$ in the $C_{13}$ calculation? Wait.
    
    Let's check the Annual Loan repayment timing again.
    "Repay the principal plus the final interest payment at the end of January next year."
    Our planning horizon is Month 1 to Month 12.
    "Next year" means the year following Month 1-12.
    End of January Next Year is the end of Month 1 of the *next* year.
    The question asks for cash at the **beginning of next year**.
    Beginning of Next Year = Start of Month 1 of the next year.
    At this point (Start of Month 1 Next Year):
    - The Annual Loan $A$ has **not** been repaid yet (repayment is at *End* of Jan Next Year).
    - The Short-term Loan $B_{12}$ (taken at Start of Month 12) is repaid at **Beginning** of Month 13 (Next Year Month 1). So $B_{12}$ IS repaid at the target time.
    - The Deposit $D_{12}$ (made at Start of Month 12) is withdrawn at **End** of Month 12 (Beginning of Next Year). So $D_{12}$ IS withdrawn at the target time.
    
    So, Cash at Beginning of Next Year ($C_{13}$) is:
    $C_{13} = C_{end,12} + D_{12}(1+r_D) - B_{12}(1+r_S)$.
    
    Where $C_{end,12} = C_{12} + B_{12} - D_{12} + c_{12}$.
    
    Substituting:
    $C_{13} = (C_{12} + B_{12} - D_{12} + c_{12}) + D_{12}(1+r_D) - B_{12}(1+r_S)$
    $C_{13} = C_{12} + c_{12} + D_{12}(1+r_D) - D_{12} - B_{12}(1+r_S) + B_{12}$
    $C_{13} = C_{12} + c_{12} + D_{12} \cdot r_D - B_{12} \cdot r_S$.
    
    This looks correct. The principal parts of $B_{12}$ and $D_{12}$ cancel out with the initial outflow, leaving only the interest impact on the final balance, added to the base flow.
    
    **General Recursion for $C_{t+1}$ (Cash at Beginning of Month $t+1$):**
    For $t = 1, \dots, 11$:
    $C_{t+1} = C_t + B_t - D_t + c_t + D_t(1+r_D) - B_t(1+r_S)$
    $C_{t+1} = C_t + c_t + D_t(1+r_D) - D_t - B_t(1+r_S) + B_t$
    $C_{t+1} = C_t + c_t + D_t \cdot r_D - B_t \cdot r_S$.
    
    Wait, is this correct?
    Let's re-verify the cash flow logic.
    $C_t$: Cash at Beginning of Month $t$.
    We borrow $B_t$ and deposit $D_t$.
    Cash available for operations: $C_t + B_t - D_t$.
    End of Month $t$ Cash (before settlement): $C_t + B_t - D_t + c_t$.
    Settlement at End of Month $t$:
    - Receive $D_t(1+r_D)$.
    - Pay $B_t(1+r_S)$.
    Cash at Beginning of Month $t+1$:
    $C_{t+1} = (C_t + B_t - D_t + c_t) + D_t(1+r_D) - B_t(1+r_S)$.
    $C_{t+1} = C_t + c_t + B_t - B_t(1+r_S) - D_t + D_t(1+r_D)$.
    $C_{t+1} = C_t + c_t - B_t \cdot r_S + D_t \cdot r_D$.
    
    This recursion holds for $t=1$ to $11$.
    
    **For $t=1$:**
    We also have the Annual Loan $A$.
    $C_2 = C_1 + c_1 - B_1 \cdot r_S + D_1 \cdot r_D$.
    But where is $A$?
    $A$ is received at Start of Month 1.
    So $C_1$ should include $A$?
    Let's define $C_1$ as the cash at the **very beginning** of Month 1, **before** taking the annual loan.
    Assume $C_1 = 0$ (no initial cash).
    Then, at Start of Month 1, we receive $A$.
    So the "Cash Available" for the recursion should include $A$.
    
    Let's adjust the recursion for $t=1$:
    Cash at Beginning of Month 1 (after Annual Loan, before Short-term/Deposit): $A$.
    Let's define $C_t$ as Cash at Beginning of Month $t$, **after** all long-term/annual adjustments but **before** short-term decisions? No, that's messy.
    
    Let's define $C_t$ as Cash at Beginning of Month $t$.
    $C_1 = A$ (Assuming 0 initial cash, plus Annual Loan).
    Then for $t=1$:
    $C_2 = C_1 + c_1 - B_1 r_S + D_1 r_D$.
    
    For $t=2, \dots, 11$:
    $C_{t+1} = C_t + c_t - B_t r_S + D_t r_D$.
    
    For $t=12$:
    We want $C_{13}$ (Beginning of Next Year).
    $C_{13} = C_{12} + c_{12} - B_{12} r_S + D_{12} r_D$.
    (Note: $A$ is not repaid, so no $-A(1+12r_A)$ term here. The interest on $A$ is paid monthly?
    "Starting from the end of February, the factory must pay 1% interest each month".
    This implies interest payments on $A$ occur at the **end** of months 2, 3, ..., 12? And "repay principal plus final interest at end of January next year".
    Does "pay 1% interest each month" mean the interest is a cash outflow during the month?
    Yes. "Pay interest ... each month".
    So, for $t=2, \dots, 12$, there is an additional cash outflow of $A \cdot r_A$.
    What about Month 1? "Starting from the end of February". So no interest payment in Month 1.
    What about "End of January next year"? That is the final repayment.
    So, cash outflows for Annual Loan Interest:
    - Month 1: 0
    - Month 2: $A \cdot 0.01$
    - Month 3: $A \cdot 0.01$
    - ...
    - Month 12: $A \cdot 0.01$
    - End of Month 12 / Beginning of Next Year: Repayment of Principal $A$ + Final Interest?
    The text says: "repay the principal plus the final interest payment at the end of January next year".
    This implies the interest for January Next Year is paid then.
    Does this affect the "Cash at Beginning of Next Year"?
    Beginning of Next Year is *before* End of January Next Year.
    So the principal $A$ and the final interest are **not** paid at the time we measure the cash.
    Therefore, the only impact of the Annual Loan on our 12-month cash balances is the monthly interest payments during Months 2 through 12.
    
    So, modify the cash flow $c_t$ to include these interest payments?
    Let $c'_t$ be the adjusted net cash flow.
    $c'_1 = c_1$.
    $c'_t = c_t - A \cdot r_A$ for $t = 2, \dots, 12$.
    
    Then the recursion becomes:
    $C_1 = A$.
    $C_{t+1} = C_t + c'_t - B_t r_S + D_t r_D$ for $t=1, \dots, 12$.
    
    Let's verify the "Beginning of Next Year" cash $C_{13}$.
    $C_{13} = C_{12} + c'_{12} - B_{12} r_S + D_{12} r_D$.
    This represents the cash in the bank at the start of Month 1 Next Year.
    The liability $A$ is still outstanding. The question asks to "maximize the total amount of cash ... available". This usually means the liquid cash balance $C_{13}$.
    
    **Constraints:**
    1.  **Non-negativity of Cash:**
        The cash balance at the beginning of any month must be sufficient to cover the operations?
        Actually, the constraint is usually that the cash balance **during** the month doesn't go negative.
        Since we assume flows happen throughout the month, a standard approximation is that the **End** of month balance (or Beginning of next month) must be non-negative?
        Or that the cash available at the start (after borrowing) must be non-negative?
        Usually, $C_t \ge 0$ is not sufficient if $c_t$ is large negative.
        The constraint is:
        Cash Available at Start of Month $t$ (after new borrowing/deposit) $\ge$ Max(0, -c_t) ?
        Or simply: The cash balance at the **end** of the month (before settlement) must be $\ge 0$?
        Let's look at the standard "cash budgeting" constraint.
        Usually: $C_t + B_t - D_t + c_t \ge 0$ is NOT the constraint, because $B_t$ and $D_t$ are decisions.
        The constraint is that the factory must have enough cash to meet obligations.
        If $c_t$ is negative, it's an outflow.
        Constraint: $C_t + B_t - D_t + (A \text{ if } t=1) + c_t \ge 0$?
        This ensures that the cash on hand at the end of the month (before settling loans/deposits) is non-negative.
        Let's check if this is the right interpretation.
        If $c_t = -100$, and $C_t=0$, we must borrow $B_t \ge 100$.
        Then $0 + B_t - D_t - 100 \ge 0 \Rightarrow B_t - D_t \ge 100$.
        This makes sense.
        
        So, for each month $t$:
        $C_t + B_t - D_t + (A \text{ if } t=1) + c_t - (A \cdot r_A \text{ if } t \ge 2) \ge 0$.
        
        Let's substitute $C_{t+1}$ definition to simplify?
        $C_{t+1} = C_t + c'_t - B_t r_S + D_t r_D$.
        The constraint is $C_t + B_t - D_t + c'_t \ge 0$.
        Note that $c'_t$ includes the annual loan interest deduction.
        
        Let's rewrite the constraint in terms of $C_{t+1}$?
        $C_t + c'_t = C_{t+1} + B_t r_S - D_t r_D$.
        So, $C_{t+1} + B_t r_S - D_t r_D + B_t - D_t \ge 0$.
        $C_{t+1} + B_t(1+r_S) - D_t(1+r_D) \ge 0$.
        This is an equivalent way to write it, but the direct form is clearer.
        
        Let's stick to:
        $C_t + B_t - D_t + c'_t \ge 0$ for all $t=1,\dots,12$.
        
        Where:
        $c'_1 = -12$
        $c'_t = c_t - 0.01 A$ for $t=2,\dots,12$.
        
        And $C_1 = A$.
        
        So for $t=1$:
        $A + B_1 - D_1 - 12 \ge 0$.
        
        For $t=2$:
        $C_2 + B_2 - D_2 + (c_2 - 0.01 A) \ge 0$.
        Substitute $C_2 = A + c_1 - B_1 r_S + D_1 r_D$?
        It is better to keep $C_t$ as variables or substitute them out to have a single model without state variables if possible, but state variables are fine for an LP.
        
        **Variables:**
        $A, B_1, \dots, B_{12}, D_1, \dots, D_{12}, C_1, \dots, C_{13}$.
        Actually, $C_1$ is fixed to $A$.
        
        **Objective:**
        Maximize $C_{13}$.
        
        **Constraints:**
        1.  $C_1 = A$.
        2.  For $t=1, \dots, 11$:
            $C_{t+1} = C_t + c'_t - B_t r_S + D_t r_D$.
        3.  $C_{13} = C_{12} + c'_{12} - B_{12} r_S + D_{12} r_D$.
        4.  For $t=1, \dots, 12$:
            $C_t + B_t - D_t + c'_t \ge 0$.
        5.  $A, B_t, D_t \ge 0$.
        
        Let's double check the $c'_t$ definition.
        $c_t$ is the net cash flow.
        Interest on $A$ is paid at the **end** of the month? "Pay 1% interest each month".
        If it's paid at the end of the month, it is part of the cash outflow of that month.
        So yes, $c'_t = c_t - 0.01 A$ for $t=2,\dots,12$.
        
        Is there any other cost?
        Short-term loan interest is handled in the $C_{t+1}$ recursion (as a net cost of borrowing).
        Deposit interest is handled in the $C_{t+1}$ recursion (as a net gain from depositing).
        
        One detail: "Short-term Monthly Loan: ... repaid at the beginning of the following month."
        My recursion:
        $C_{t+1} = C_t + c'_t - B_t r_S + D_t r_D$.
        This assumes the principal $B_t$ and $D_t$ cancel out, leaving only the interest cost/gain.
        Let's re-verify the algebra.
        Cash End Month $t$ (pre-settlement) = $C_t + B_t - D_t + c'_t$.
        Settlement: $+ D_t(1+r_D) - B_t(1+r_S)$.
        $C_{t+1} = C_t + B_t - D_t + c'_t + D_t + D_t r_D - B_t - B_t r_S$.
        $C_{t+1} = C_t + c'_t + D_t r_D - B_t r_S$.
        Correct.

### 4. Operational Constraints

1.  **Initial Cash:**
    $$C_1 = A$$

2.  **Cash Balance Recursion (for $t = 1, \dots, 11$):**
    $$C_{t+1} = C_t + c'_t - 0.015 B_t + 0.004 D_t$$

3.  **Final Cash Balance (for $t = 12$):**
    $$C_{13} = C_{12} + c'_{12} - 0.015 B_{12} + 0.004 D_{12}$$

4.  **Non-negativity of Cash Flow (Solvency Constraint) for $t = 1, \dots, 12$:**
    $$C_t + B_t - D_t + c'_t \ge 0$$
    
    Where $c'_t$ is defined as:
    $$c'_1 = -12$$
    $$c'_t = c_t - 0.01 A \quad \text{for } t = 2, \dots, 12$$
    
    Substituting $c_t$ values:
    - $t=1: C_1 + B_1 - D_1 - 12 \ge 0$
    - $t=2: C_2 + B_2 - D_2 - 10 - 0.01 A \ge 0$
    - $t=3: C_3 + B_3 - D_3 - 8 - 0.01 A \ge 0$
    - $t=4: C_4 + B_4 - D_4 - 10 - 0.01 A \ge 0$
    - $t=5: C_5 + B_5 - D_5 - 4 - 0.01 A \ge 0$
    - $t=6: C_6 + B_6 - D_6 + 5 - 0.01 A \ge 0$
    - $t=7: C_7 + B_7 - D_7 - 7 - 0.01 A \ge 0$
    - $t=8: C_8 + B_8 - D_8 - 2 - 0.01 A \ge 0$
    - $t=9: C_9 + B_9 - D_9 + 15 - 0.01 A \ge 0$
    - $t=10: C_{10} + B_{10} - D_{10} + 12 - 0.01 A \ge 0$
    - $t=11: C_{11} + B_{11} - D_{11} - 7 - 0.01 A \ge 0$
    - $t=12: C_{12} + B_{12} - D_{12} + 45 - 0.01 A \ge 0$

5.  **Non-negativity of Decision Variables:**
    $$A \ge 0$$
    $$B_t \ge 0, \quad D_t \ge 0 \quad \text{for } t=1, \dots, 12$$

6.  **Non-negativity of Cash Balances:**
    $$C_t \ge 0 \quad \text{for } t=1, \dots, 13$$
    *(Note: The solvency constraint $C_t + B_t - D_t + c'_t \ge 0$ implies the cash during the month is non-negative. $C_t \ge 0$ is also required physically.)*

### Summary of Parameters for Code Agent
- $c = [-12, -10, -8, -10, -4, 5, -7, -2, 15, 12, -7, 45]$
- $r_A = 0.01$
- $r_S = 0.015$
- $r_D = 0.004$
- $N = 12$

### Objective
Maximize $C_{13}$.