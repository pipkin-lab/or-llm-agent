### 1. Index Sets & Parameters

**Index Sets:**
*   $t \in \{1, 2, 3, 4\}$: The set of months.
*   $d \in \{1, 2, 3, 4\}$: The set of possible contract durations (in months).

**Parameters:**
*   $R_t$: Required warehouse space (in $m^2$) for month $t$.
    *   $R_1 = 1500$
    *   $R_2 = 1000$
    *   $R_3 = 2000$
    *   $R_4 = 1200$
*   $C_d$: Total rental cost (in yuan) per $m^2$ for a contract with duration $d$ months.
    *   $C_1 = 28$
    *   $C_2 = 45$
    *   $C_3 = 60$
    *   $C_4 = 73$

### 2. Decision Variables

Let $x_{t,d}$ be the amount of warehouse space (in $m^2$) rented at the beginning of month $t$ with a contract duration of $d$ months.

**Domain:**
*   $x_{t,d} \ge 0$ for all $t \in \{1, 2, 3, 4\}$ and $d \in \{1, 2, 3, 4\}$, subject to the constraint that the contract must fit within the planning horizon.
    *   Specifically, a contract starting at month $t$ with duration $d$ is valid only if $t + d - 1 \le 4$.
    *   Valid pairs $(t, d)$:
        *   $t=1$: $d \in \{1, 2, 3, 4\}$
        *   $t=2$: $d \in \{1, 2, 3\}$
        *   $t=3$: $d \in \{1, 2\}$
        *   $t=4$: $d \in \{1\}$

*Note: Since warehouse space can be rented in continuous units (fractional $m^2$) and the scale is large (hundreds/thousands of $m^2$), continuous variables are appropriate.*

### 3. Objective Function

Minimize the total rental cost:

$$
\text{Minimize } Z = \sum_{t=1}^{4} \sum_{d \in D_t} C_d \cdot x_{t,d}
$$

Where $D_t$ is the set of valid durations for month $t$. Explicitly:

$$
Z = 28(x_{1,1} + x_{2,1} + x_{3,1} + x_{4,1}) + 45(x_{1,2} + x_{2,2} + x_{3,2}) + 60(x_{1,3} + x_{2,3}) + 73(x_{1,4})
$$

### 4. Operational Constraints

The total space rented from all contracts active in month $t$ must be at least the required space $R_t$.

A contract $x_{i,d}$ (signed at month $i$ with duration $d$) is active in month $t$ if $i \le t \le i + d - 1$.

**Month 1 Constraints:**
Only contracts starting in Month 1 are active.
$$
x_{1,1} + x_{1,2} + x_{1,3} + x_{1,4} \ge 1500
$$

**Month 2 Constraints:**
Contracts starting in Month 1 (with $d \ge 2$) and Month 2 (with $d \ge 1$) are active.
$$
x_{1,2} + x_{1,3} + x_{1,4} + x_{2,1} + x_{2,2} + x_{2,3} \ge 1000
$$

**Month 3 Constraints:**
Contracts starting in Month 1 (with $d \ge 3$), Month 2 (with $d \ge 2$), and Month 3 (with $d \ge 1$) are active.
$$
x_{1,3} + x_{1,4} + x_{2,2} + x_{2,3} + x_{3,1} + x_{3,2} \ge 2000
$$

**Month 4 Constraints:**
Contracts starting in Month 1 (with $d \ge 4$), Month 2 (with $d \ge 3$), Month 3 (with $d \ge 2$), and Month 4 (with $d \ge 1$) are active.
$$
x_{1,4} + x_{2,3} + x_{3,2} + x_{4,1} \ge 1200
$$

**Non-negativity Constraints:**
$$
x_{t,d} \ge 0 \quad \forall (t,d) \text{ where } t+d-1 \le 4
$$