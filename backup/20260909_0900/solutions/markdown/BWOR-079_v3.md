### 1. Index Sets & Parameters

**Index Sets:**
*   $t \in \{1, 2, 3, 4, 5\}$: Set of time periods in a day.
    *   $t=1$: 6:00–10:00
    *   $t=2$: 10:00–14:00
    *   $t=3$: 14:00–18:00
    *   $t=4$: 18:00–22:00
    *   $t=5$: 22:00–6:00 (next day)
*   $s \in \{1, 2, 3, 4, 5\}$: Set of shifts.
    *   Shift 1: 2:00–10:00
    *   Shift 2: 6:00–14:00
    *   Shift 3: 10:00–18:00
    *   Shift 4: 14:00–22:00
    *   Shift 5: 18:00–2:00 (next day)
*   $d \in \{1, 2, 3, 4, 5, 6, 7\}$: Set of days in a week (Monday to Sunday).

**Parameters:**
*   $R_t$: Minimum number of nurses required in time period $t$.
    *   $R_1 = 18$
    *   $R_2 = 20$
    *   $R_3 = 19$
    *   $R_4 = 17$
    *   $R_5 = 12$
*   $A_{s,t}$: Binary parameter indicating if Shift $s$ covers Time Period $t$.
    *   Shift 1 (2:00–10:00) covers $t=1$ (6-10) and part of $t=5$ (2-6, but $t=5$ is 22-6, so 2-6 is covered). Wait, let's map carefully.
        *   $t=1$ (6-10): Covered by Shift 1 (2-10) and Shift 2 (6-14).
        *   $t=2$ (10-14): Covered by Shift 2 (6-14) and Shift 3 (10-18).
        *   $t=3$ (14-18): Covered by Shift 3 (10-18) and Shift 4 (14-22).
        *   $t=4$ (18-22): Covered by Shift 4 (14-22) and Shift 5 (18-2).
        *   $t=5$ (22-6): Covered by Shift 5 (18-2) and Shift 1 (2-10).
    *   Thus:
        *   $A_{1,1}=1, A_{1,5}=1$
        *   $A_{2,1}=1, A_{2,2}=1$
        *   $A_{3,2}=1, A_{3,3}=1$
        *   $A_{4,3}=1, A_{4,4}=1$
        *   $A_{5,4}=1, A_{5,5}=1$
        *   All other $A_{s,t} = 0$.

### 2. Decision Variables

Let $x_{d,s}$ be the number of nurses starting their 5-day work week on day $d$ assigned to start with Shift $s$ on that day.
*   However, the problem states "Plan 1: Each nurse works 5 consecutive days... cycling through Shift 1 to Shift 5 in sequence."
*   This implies a nurse's schedule is fully determined by the **start day** and the **start shift**.
*   If a nurse starts on day $d$ with Shift $s$, on day $d+k$ (for $k=0..4$), she works Shift $(s+k) \pmod 5$ (with appropriate indexing $1..5$).
*   Let $N_{d,s}$ be the number of nurses who begin their 5-day block on day $d$ starting with Shift $s$.
*   Since the pattern is fixed (cycling 1->2->3->4->5), the shift worked on any specific day $d'$ by a nurse who started on day $d$ is determined.
*   Actually, a simpler formulation is to define variables based on the **starting day of the work block**.
*   Let $y_{d}$ be the number of nurses who start their 5-day work cycle on day $d$.
*   Wait, does the starting shift matter? "cycling through Shift 1 to Shift 5 in sequence".
    *   Nurse A starts Mon with Shift 1. Mon=S1, Tue=S2, Wed=S3, Thu=S4, Fri=S5.
    *   Nurse B starts Mon with Shift 2. Mon=S2, Tue=S3, Wed=S4, Thu=S5, Fri=S1.
    *   The problem says "works a different shift each day, cycling through Shift 1 to Shift 5 in sequence." It does *not* explicitly say every nurse *must* start with Shift 1. It says "For example... If a nurse starts on Monday, she works Shift 1 on Monday...". This suggests the starting shift can vary or is part of the schedule design. To minimize total nurses, we should allow flexibility in which shift is assigned to the first day of the 5-day block, as long as the sequence is consecutive.
    *   Let $x_{d, s_{start}}$ be the number of nurses starting their 5-day block on day $d$ with Shift $s_{start}$ on day $d$.
    *   Total nurses $Z = \sum_{d=1}^7 \sum_{s_{start}=1}^5 x_{d, s_{start}}$.
    *   Note: Nurses work 5 days, off 2. In a 7-day week, the pattern repeats every week. We assume a steady-state weekly schedule.

**Variable Definition:**
*   $x_{d, s} \in \mathbb{Z}^+$: Number of nurses who start their 5-day work period on day $d$ ($d \in \{1..7\}$) and are assigned Shift $s$ ($s \in \{1..5\}$) on that first day.
*   $Z$: Total number of nurses (objective variable).

### 3. Objective Function

Minimize the total number of nurses:
$$ \text{Minimize } Z = \sum_{d=1}^{7} \sum_{s=1}^{5} x_{d, s} $$

### 4. Operational Constraints

**1. Nurse Coverage Constraints:**
For each day $d \in \{1..7\}$ and each time period $t \in \{1..5\}$, the total number of nurses on duty must meet the requirement $R_t$.

A nurse represented by variable $x_{d', s'}$ (started on day $d'$, first shift $s'$) works on day $d$ if:
*   The day $d$ falls within the 5-day block starting at $d'$.
*   Let $k$ be the offset such that $d \equiv d' + k \pmod 7$. The nurse works if $k \in \{0, 1, 2, 3, 4\}$.
*   If the nurse works on day $d$, the shift she works is $s_{work} = (s' - 1 + k) \pmod 5 + 1$.
*   She covers time period $t$ on day $d$ if $A_{s_{work}, t} = 1$.

Let $Cov(d, t, d', s')$ be a binary parameter equal to 1 if a nurse starting on day $d'$ with initial shift $s'$ covers time period $t$ on day $d$, and 0 otherwise.

Constraint for each day $d$ and period $t$:
$$ \sum_{d'=1}^{7} \sum_{s'=1}^{5} Cov(d, t, d', s') \cdot x_{d', s'} \ge R_t, \quad \forall d \in \{1..7\}, t \in \{1..5\} $$

**2. Variable Bounds:**
$$ x_{d, s} \ge 0, \quad x_{d, s} \in \mathbb{Z} \quad \forall d \in \{1..7\}, s \in \{1..5\} $$

**Logic for $Cov(d, t, d', s')$:**
1.  Calculate day offset $k = (d - d') \pmod 7$.
2.  If $k > 4$, $Cov = 0$ (nurse is off).
3.  If $k \le 4$:
    *   Current Shift $s_{cur} = ((s' - 1 + k) \pmod 5) + 1$.
    *   If $A_{s_{cur}, t} = 1$, $Cov = 1$.
    *   Else $Cov = 0$.

**Explicit Coverage Matrix Construction (Example for Day 1, Period 1):**
Period 1 (6:00-10:00) is covered by Shift 1 and Shift 2.
We need $\sum (\text{Nurses on Shift 1 on Day 1} + \text{Nurses on Shift 2 on Day 1}) \ge 18$.

Who is on Shift 1 on Day 1?
- Started Day 1 ($d'=1$) with $s'=1$ ($k=0 \rightarrow S1$).
- Started Day 7 ($d'=7$) with $s'=5$ ($k=1 \rightarrow S5+1=S1$? No. $S5 \rightarrow S1$ is next cycle. Let's check indices.
  - Seq: 1,2,3,4,5. Next is 1.
  - If start $s'=5$, day 0 is S5. Day 1 ($k=1$) is S1.
  - So $d'=7, s'=5$ works on Day 1 with Shift 1.
- Started Day 6 ($d'=6$) with $s'=4$ ($k=2 \rightarrow S4+2 \rightarrow S1$? $S4 \xrightarrow{k=1} S5 \xrightarrow{k=2} S1$. Yes.)
- Started Day 5 ($d'=5$) with $s'=3$ ($k=3 \rightarrow S3 \xrightarrow{1} S4 \xrightarrow{2} S5 \xrightarrow{3} S1$. Yes.)
- Started Day 4 ($d'=4$) with $s'=2$ ($k=4 \rightarrow S2 \xrightarrow{1} S3 \xrightarrow{2} S4 \xrightarrow{3} S5 \xrightarrow{4} S1$. Yes.)
- Started Day 3 ($d'=3$) with $s'=?$ $k=5$ (off).

So, Nurses on Shift 1 on Day 1 = $x_{1,1} + x_{7,5} + x_{6,4} + x_{5,3} + x_{4,2}$.
Similarly, Nurses on Shift 2 on Day 1 = $x_{1,2} + x_{7,1} + x_{6,5} + x_{5,4} + x_{4,3}$.

Constraint for Day 1, Period 1:
$$ (x_{1,1} + x_{7,5} + x_{6,4} + x_{5,3} + x_{4,2}) + (x_{1,2} + x_{7,1} + x_{6,5} + x_{5,4} + x_{4,3}) \ge 18 $$

This structure applies to all 35 constraints (7 days $\times$ 5 periods).

### Final Model Summary

**Sets:**
*   $D = \{1, ..., 7\}$ (Days)
*   $T = \{1, ..., 5\}$ (Time Periods)
*   $S = \{1, ..., 5\}$ (Shifts)

**Parameters:**
*   $R_t$: Required nurses in period $t$ ($18, 20, 19, 17, 12$).
*   $A_{s,t}$: Shift $s$ covers period $t$ (as defined above).

**Variables:**
*   $x_{d,s}$: Integer $\ge 0$, number of nurses starting week on day $d$ with initial shift $s$.

**Objective:**
$$ \min \sum_{d=1}^7 \sum_{s=1}^5 x_{d,s} $$

**Constraints:**
For each day $d \in D$ and period $t \in T$:
$$ \sum_{d' \in D} \sum_{s' \in S} \delta(d, t, d', s') x_{d', s'} \ge R_t $$

Where $\delta(d, t, d', s') = 1$ if a nurse starting on $d'$ with shift $s'$ works shift $s_{cur}$ on day $d$ such that $A_{s_{cur}, t}=1$, and 0 otherwise.
Specifically, let $k = (d - d' + 7) \pmod 7$.
If $0 \le k \le 4$:
   $s_{cur} = ((s' - 1 + k) \pmod 5) + 1$
   $\delta = A_{s_{cur}, t}$
Else:
   $\delta = 0$