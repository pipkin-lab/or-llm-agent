### 1. Index Sets & Parameters

**Index Sets:**
*   $P = \{1, 2, 3\}$: Set of products (I, II, III).
*   $M_A = \{1, 2\}$: Set of Stage A machines ($A_1, A_2$).
*   $M_B = \{1, 2, 3\}$: Set of Stage B machines ($B_1, B_2, B_3$).
*   $R_{A,p}$: Set of Stage A machines feasible for product $p$.
*   $R_{B,p}$: Set of Stage B machines feasible for product $p$.

**Parameters (from Table 1-18):**

*   $t_{A, m, p}$: Processing time (hours) of product $p$ on Stage A machine $m$.
    *   $t_{A, 1, 1} = 5, \quad t_{A, 2, 1} = 7$
    *   $t_{A, 1, 2} = 10, \quad t_{A, 2, 2} = 9$
    *   $t_{A, 2, 3} = 12$ (Product III only on $A_2$)
    *   $t_{A, m, p} = 0$ (or undefined/infeasible) if $p \notin R_{A,m}$. Specifically, Product III cannot use $A_1$.
*   $t_{B, m, p}$: Processing time (hours) of product $p$ on Stage B machine $m$.
    *   $t_{B, 1, 1} = 6, \quad t_{B, 2, 1} = 4, \quad t_{B, 3, 1} = 7$
    *   $t_{B, 1, 2} = 8$ (Product II only on $B_1$)
    *   $t_{B, 2, 3} = 11$ (Product III only on $B_2$)
    *   $t_{B, m, p} = 0$ (or undefined/infeasible) otherwise. Specifically:
        *   Product III cannot use $B_1$ or $B_3$.
        *   Product II cannot use $B_2$ or $B_3$.
*   $H_{A, m}$: Available hours for Stage A machine $m$.
    *   $H_{A, 1} = 6000$
    *   $H_{A, 2} = 10000$
*   $H_{B, m}$: Available hours for Stage B machine $m$.
    *   $H_{B, 1} = 4000$
    *   $H_{B, 2} = 7000$
    *   $H_{B, 3} = 4000$
*   $c_{A, m}$: Processing cost per hour on Stage A machine $m$.
    *   $c_{A, 1} = 0.05$
    *   $c_{A, 2} = 0.03$
*   $c_{B, m}$: Processing cost per hour on Stage B machine $m$.
    *   $c_{B, 1} = 0.06$
    *   $c_{B, 2} = 0.11$
    *   $c_{B, 3} = 0.05$
*   $r_p$: Raw material cost per unit of product $p$.
    *   $r_1 = 0.25$
    *   $r_2 = 0.35$
    *   $r_3 = 0.50$
*   $s_p$: Selling price per unit of product $p$.
    *   $s_1 = 1.25$
    *   $s_2 = 2.00$
    *   $s_3 = 2.80$

### 2. Decision Variables

Let $x_{A, m, p}$ be the number of units of product $p$ processed on Stage A machine $m$.
Let $x_{B, m, p}$ be the number of units of product $p$ processed on Stage B machine $m$.

**Domains:**
*   $x_{A, m, p} \ge 0, \quad \forall m \in M_A, p \in P$.
    *   Note: $x_{A, 1, 3} = 0$ (Product III cannot use $A_1$).
*   $x_{B, m, p} \ge 0, \quad \forall m \in M_B, p \in P$.
    *   Note: $x_{B, 2, 2} = x_{B, 3, 2} = 0$ (Product II cannot use $B_2, B_3$).
    *   Note: $x_{B, 1, 3} = x_{B, 3, 3} = 0$ (Product III cannot use $B_1, B_3$).

*(Note: Since the scale is large (hours in thousands) and no explicit integer requirement is stated for units, standard Linear Programming (LP) continuous variables are appropriate.)*

### 3. Objective Function

Maximize Total Profit $Z$.

Profit per unit of product $p$ produced via specific machines is:
$$ \text{Revenue} - \text{Raw Material Cost} - \text{Stage A Processing Cost} - \text{Stage B Processing Cost} $$

For a unit of product $p$ processed on Stage A machine $m_A$ and Stage B machine $m_B$:
$$ \text{Profit}_{m_A, m_B, p} = s_p - r_p - (t_{A, m_A, p} \cdot c_{A, m_A}) - (t_{B, m_B, p} \cdot c_{B, m_B}) $$

The total objective function sums the profit contributions from all feasible product-machine combinations:

$$
\begin{aligned}
\max Z = & \sum_{p \in P} \sum_{m_A \in R_{A,p}} \sum_{m_B \in R_{B,p}} \left[ s_p - r_p - (t_{A, m_A, p} c_{A, m_A}) - (t_{B, m_B, p} c_{B, m_B}) \right] \cdot x_{A, m_A, p} \cdot \frac{x_{B, m_B, p}}{x_{A, m_A, p}} \quad \text{(Incorrect coupling)}
\end{aligned}
$$

**Correction on Objective Linearity:**
The variables $x_{A, m, p}$ and $x_{B, m, p}$ represent flow. For a valid production unit, it must pass through *one* A-machine and *one* B-machine. However, in linear programming, we cannot easily link specific units from A to B without additional variables or assumptions unless we assume independent routing decisions or aggregate flow.

Standard approach for this type of "production plan" problem:
Let $y_p$ be the total production of product $p$.
However, costs depend on *which* machine is used.
Let's define the variables as the flow of product $p$ on specific machines.
Let $x_{A, m, p}$ be units of $p$ on $A_m$.
Let $x_{B, m, p}$ be units of $p$ on $B_m$.

Constraint: Total units of $p$ processed on Stage A must equal total units processed on Stage B (Flow Conservation).
$$ \sum_{m_A \in M_A} x_{A, m_A, p} = \sum_{m_B \in M_B} x_{B, m_B, p} = Q_p \quad \forall p \in P $$

The objective function is linear in terms of these variables if we sum the costs separately:
$$
\begin{aligned}
Z = & \sum_{p \in P} \sum_{m_A \in M_A} (s_p - r_p) x_{A, m_A, p} \\
& - \sum_{p \in P} \sum_{m_A \in M_A} (t_{A, m_A, p} c_{A, m_A}) x_{A, m_A, p} \\
& - \sum_{p \in P} \sum_{m_B \in M_B} (t_{B, m_B, p} c_{B, m_B}) x_{B, m_B, p}
\end{aligned}
$$
*Wait*, if we sum revenue on $x_A$ and costs on $x_B$, we must ensure $x_A$ and $x_B$ are balanced. The above formulation assumes we can choose revenue based on A-flow and costs based on B-flow independently, which is valid *only if* the flow conservation constraint $\sum x_A = \sum x_B$ is enforced. The revenue is per unit produced, regardless of which B machine it went through, but the *cost* depends on the B machine.

So, the correct linear objective is:
$$
\max Z = \sum_{p \in P} \sum_{m_A \in M_A} (s_p - r_p) x_{A, m_A, p} - \sum_{p \in P} \sum_{m_A \in M_A} (t_{A, m_A, p} c_{A, m_A}) x_{A, m_A, p} - \sum_{p \in P} \sum_{m_B \in M_B} (t_{B, m_B, p} c_{B, m_B}) x_{B, m_B, p}
$$

This can be simplified by combining the A-stage terms:
$$
\max Z = \sum_{p \in P} \sum_{m_A \in M_A} (s_p - r_p - t_{A, m_A, p} c_{A, m_A}) x_{A, m_A, p} - \sum_{p \in P} \sum_{m_B \in M_B} (t_{B, m_B, p} c_{B, m_B}) x_{B, m_B, p}
$$

### 4. Operational Constraints

**1. Flow Conservation (Production Balance):**
The total number of units of product $p$ processed on Stage A must equal the total number of units processed on Stage B.
$$
\sum_{m_A \in M_A} x_{A, m_A, p} = \sum_{m_B \in M_B} x_{B, m_B, p}, \quad \forall p \in P
$$

**2. Machine Capacity Constraints (Stage A):**
$$
\sum_{p \in P} t_{A, m_A, p} x_{A, m_A, p} \le H_{A, m_A}, \quad \forall m_A \in M_A
$$
*Specifics:*
*   $A_1$: $5 x_{A, 1, 1} + 10 x_{A, 1, 2} \le 6000$ (Note: $x_{A, 1, 3}=0$)
*   $A_2$: $7 x_{A, 2, 1} + 9 x_{A, 2, 2} + 12 x_{A, 2, 3} \le 10000$

**3. Machine Capacity Constraints (Stage B):**
$$
\sum_{p \in P} t_{B, m_B, p} x_{B, m_B, p} \le H_{B, m_B}, \quad \forall m_B \in M_B
$$
*Specifics:*
*   $B_1$: $6 x_{B, 1, 1} + 8 x_{B, 1, 2} \le 4000$ (Note: $x_{B, 1, 3}=0$)
*   $B_2$: $4 x_{B, 2, 1} + 11 x_{B, 2, 3} \le 7000$ (Note: $x_{B, 2, 2}=0$)
*   $B_3$: $7 x_{B, 3, 1} \le 4000$ (Note: $x_{B, 3, 2}=0, x_{B, 3, 3}=0$)

**4. Non-negativity and Feasibility:**
$$
x_{A, m_A, p} \ge 0, \quad x_{B, m_B, p} \ge 0
$$
With specific zero bounds for infeasible routes:
*   $x_{A, 1, 3} = 0$
*   $x_{B, 2, 2} = 0, \quad x_{B, 3, 2} = 0$
*   $x_{B, 1, 3} = 0, \quad x_{B, 3, 3} = 0$