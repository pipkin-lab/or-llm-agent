# Mathematical Optimization Model: Machine Replacement Problem

## 1. Index Sets & Parameters

**Sets:**
- $T = \{1, 2, 3, 4\}$: Set of years (time periods).
- $S = \{1, 2, 3, 4\}$: Set of possible service lifespans (years a machine can be kept before replacement).

**Parameters:**
- $P_t$: Purchase price of a new machine at the beginning of year $t$ (thousand yuan).
  - $P_1 = 2.5$
  - $P_2 = 2.6$
  - $P_3 = 2.8$
  - $P_4 = 3.1$
- $SV_j$: Salvage value at the end of year $j$ if the machine has been in service for $j$ years (thousand yuan).
  - $SV_1 = 2.0$
  - $SV_2 = 1.6$
  - $SV_3 = 1.3$
  - $SV_4 = 1.1$
- $C_j$: Operating and maintenance cost for a machine in its $j$-th year of service (thousand yuan).
  - $C_1 = 0.3$
  - $C_2 = 0.8$
  - $C_3 = 1.5$
  - $C_4 = 2.0$

**Derived Parameters:**
Let $K_{t, t+d}$ be the total cost of buying a new machine at the beginning of year $t$ and keeping it for $d$ years (selling it at the end of year $t+d-1$ or end of horizon if $t+d-1 = 4$).
The cost components for keeping a machine from start of year $t$ for $d$ years are:
1. Purchase at start of $t$: $P_t$
2. Operating costs for years $t, t+1, \dots, t+d-1$: $\sum_{k=1}^{d} C_k$
3. Salvage value received at end of year $t+d-1$ (reduces cost): $-SV_d$

Thus, the net cost of a replacement cycle starting at $t$ with duration $d$ is:
$$ K_{t, d} = P_t + \sum_{k=1}^{d} C_k - SV_d $$
*Note: The salvage value depends only on the age $d$ of the machine, not the calendar year, based on the table structure "Salvage Value after j Years".*

## 2. Decision Variables

Let $x_{t, d}$ be a binary variable defined for all $t \in T$ and valid durations $d$:
$$ x_{t, d} = \begin{cases} 
1 & \text{if a new machine is purchased at the beginning of year } t \text{ and kept for exactly } d \text{ years} \\
0 & \text{otherwise}
\end{cases} $$

**Domain Constraints for Indices:**
- $t \in \{1, 2, 3, 4\}$
- $d \in \{1, 2, 3, 4\}$
- Validity Condition: The machine must not exceed the end of the planning horizon (Year 4). Therefore, we only consider pairs $(t, d)$ such that $t + d - 1 \le 4$.
  - If $t=1$, $d \in \{1, 2, 3, 4\}$ (Ends in year $1+d-1$)
  - If $t=2$, $d \in \{1, 2, 3\}$ (Ends in year $2+d-1$)
  - If $t=3$, $d \in \{1, 2\}$
  - If $t=4$, $d \in \{1\}$

## 3. Objective Function

Minimize the total cost over the 4-year period.

$$ \text{Minimize } Z = \sum_{t=1}^{4} \sum_{d=1}^{4-t+1} K_{t, d} \cdot x_{t, d} $$

Where $K_{t, d}$ is calculated as:
$$ K_{t, d} = P_t + \sum_{k=1}^{d} C_k - SV_d $$

## 4. Operational Constraints

**Coverage Constraint:**
The strategy must ensure that exactly one machine is in service at the beginning of each year. This implies that the sum of the durations of the replacement cycles must exactly cover the timeline from Year 1 to Year 4.

This is a "Covering the Time Horizon" constraint. A new machine is bought at year $t$ if and only if the previous machine's cycle ended at year $t-1$.

A standard way to model this in MILP for replacement problems is to ensure that the intervals defined by the selected $(t, d)$ pairs form a partition of the time interval $[1, 4]$.

Let's define the constraint more explicitly using the logic that "Year 1 must start with a purchase" and "If a purchase happens at $t>1$, the previous cycle must have ended at $t-1$".

Alternatively, and more simply for this specific small-scale problem, we can use a **Path/Chain** formulation or simply enforce that the intervals do not overlap and cover the range.

**Constraint 1: Start of Planning Horizon**
A machine must be purchased at the beginning of Year 1.
$$ \sum_{d=1}^{4} x_{1, d} = 1 $$

**Constraint 2: Continuity / No Overlap / No Gap**
For any year $t \in \{2, 3, 4\}$, a new machine is purchased at the beginning of year $t$ if and only if the machine purchased in a previous year $t' < t$ has a duration $d$ such that $t' + d - 1 = t - 1$ (i.e., it ends exactly at the end of year $t-1$).

This can be formulated as:
$$ \sum_{d=1}^{5-t} x_{t, d} = \sum_{t' = 1}^{t-1} \sum_{d=1}^{4-t'+1} x_{t', d} \cdot \delta_{t' + d - 1, t - 1} $$
Where $\delta$ is 1 if the condition holds, 0 otherwise.

Let's expand this for each year $t$:

*   **For Year 2 ($t=2$):**
    A purchase at Year 2 happens if the Year 1 machine lasted exactly 1 year ($1+1-1=1$).
    $$ x_{2,1} + x_{2,2} + x_{2,3} = x_{1,1} $$
    *(Note: $x_{2,d}$ is only defined for $d \le 3$)*

*   **For Year 3 ($t=3$):**
    A purchase at Year 3 happens if the Year 1 machine lasted 2 years ($1+2-1=2$) OR the Year 2 machine lasted 1 year ($2+1-1=2$).
    $$ x_{3,1} + x_{3,2} = x_{1,2} + x_{2,1} $$
    *(Note: $x_{3,d}$ is only defined for $d \le 2$)*

*   **For Year 4 ($t=4$):**
    A purchase at Year 4 happens if the Year 1 machine lasted 3 years ($1+3-1=3$) OR the Year 2 machine lasted 2 years ($2+2-1=3$) OR the Year 3 machine lasted 1 year ($3+1-1=3$).
    $$ x_{4,1} = x_{1,3} + x_{2,2} + x_{3,1} $$

*   **End of Horizon Check ($t=5$):**
    The planning ends at the end of Year 4. No purchase is made at Year 5. The sum of durations of active cycles must end exactly at Year 4.
    The cycles ending at Year 4 are those where $t + d - 1 = 4$.
    These are: $(1,4), (2,3), (3,2), (4,1)$.
    The constraint is implicitly satisfied if the continuity constraints above hold and the initial constraint holds, ensuring the "chain" reaches the end. We can add a final balance check:
    $$ x_{1,4} + x_{2,3} + x_{3,2} + x_{4,1} = 1 $$
    *(This ensures exactly one machine is in service during the final year and the plan terminates correctly.)*

**Binary Constraints:**
$$ x_{t, d} \in \{0, 1\} \quad \forall t, d \text{ such that } t+d-1 \le 4 $$

---

### Model Summary for Implementation

**Variables:**
- $x_{1,1}, x_{1,2}, x_{1,3}, x_{1,4}$
- $x_{2,1}, x_{2,2}, x_{2,3}$
- $x_{3,1}, x_{3,2}$
- $x_{4,1}$

**Objective Coefficients ($K_{t,d}$):**
Calculate $K_{t,d} = P_t + \sum_{k=1}^d C_k - SV_d$.

Example Calculation for $K_{1,1}$:
$P_1 = 2.5$
$\sum_{k=1}^1 C_k = C_1 = 0.3$
$SV_1 = 2.0$
$K_{1,1} = 2.5 + 0.3 - 2.0 = 0.8$

Example Calculation for $K_{1,2}$:
$P_1 = 2.5$
$\sum_{k=1}^2 C_k = 0.3 + 0.8 = 1.1$
$SV_2 = 1.6$
$K_{1,2} = 2.5 + 1.1 - 1.6 = 2.0$

(The solver will handle the summation in the objective function using these pre-calculated or on-the-fly calculated coefficients).

**Constraints:**
1. $\sum_{d=1}^{4} x_{1, d} = 1$
2. $\sum_{d=1}^{3} x_{2, d} = x_{1, 1}$
3. $\sum_{d=1}^{2} x_{3, d} = x_{1, 2} + x_{2, 1}$
4. $x_{4, 1} = x_{1, 3} + x_{2, 2} + x_{3, 1}$
5. $x_{1, 4} + x_{2, 3} + x_{3, 2} + x_{4, 1} = 1$
6. $x_{t, d} \in \{0, 1\}$