### Model Type Declaration
**Model Type:** LP (Linear Programming)

### 1. Index Sets & Parameters

**Index Sets:**
*   $I = \{1, 2, 3\}$: Set of products (Product I, II, III).
*   $A = \{A1, A2\}$: Set of machines in Stage A.
*   $B = \{B1, B2, B3\}$: Set of machines in Stage B.
*   $M = A \cup B$: Set of all machines.

**Parameters (extracted from Table 1-20):**

*   **Processing Time ($t_{m,i}$ in hours per unit):**
    *   *Stage A:*
        *   $t_{A1,1} = 5$, $t_{A1,2} = 10$, $t_{A1,3} = \infty$ (Product III cannot use A1)
        *   $t_{A2,1} = 7$, $t_{A2,2} = 9$, $t_{A2,3} = 12$
    *   *Stage B:*
        *   $t_{B1,1} = 6$, $t_{B1,2} = 8$, $t_{B1,3} = \infty$ (Product III cannot use B1)
        *   $t_{B2,1} = 4$, $t_{B2,2} = \infty$ (Product II cannot use B2), $t_{B2,3} = 11$
        *   $t_{B3,1} = 7$, $t_{B3,2} = \infty$ (Product II cannot use B3), $t_{B3,3} = \infty$ (Product III cannot use B3)
    *   *Note on Feasibility:* Product III requires Stage A on A2 and Stage B on B2. Product II requires Stage A on A1 or A2, and Stage B on B1. Product I can use any machine in either stage.

*   **Machine Capacity ($C_m$ in hours):**
    *   $C_{A1} = 6000$
    *   $C_{A2} = 10000$
    *   $C_{B1} = 4000$
    *   $C_{B2} = 7000$
    *   $C_{B3} = 4000$

*   **Processing Cost Rate ($r_m$ in yuan/hour):**
    *   $r_{A1} = 0.05$
    *   $r_{A2} = 0.03$
    *   $r_{B1} = 0.06$
    *   $r_{B2} = 0.11$
    *   $r_{B3} = 0.05$

*   **Raw Material Cost ($c_i$ in yuan/unit):**
    *   $c_1 = 0.25$
    *   $c_2 = 0.35$
    *   $c_3 = 0.50$

*   **Selling Price ($p_i$ in yuan/unit):**
    *   $p_1 = 1.25$
    *   $p_2 = 2.00$
    *   $p_3 = 2.80$

### 2. Decision Variables

Let $x_{m,i}$ be the number of units of product $i$ processed on machine $m$.
*   $x_{A1,1}, x_{A1,2} \ge 0$
*   $x_{A2,1}, x_{A2,2}, x_{A2,3} \ge 0$
*   $x_{B1,1}, x_{B1,2} \ge 0$
*   $x_{B2,1}, x_{B2,3} \ge 0$
*   $x_{B3,1} \ge 0$

*Variables corresponding to infeasible assignments (e.g., $x_{A1,3}$, $x_{B2,2}$, $x_{B3,2}$, $x_{B3,3}$, $x_{B1,3}$) are omitted from the model as they are structurally zero.*

### 3. Objective Function

Maximize total Profit ($Z$).
Profit = Total Revenue - Total Processing Cost - Total Raw Material Cost.

$$
\text{MAXIMIZE } Z = \sum_{i \in I} \left( \sum_{m \in A} x_{m,i} + \sum_{m \in B} x_{m,i} \right) \times (p_i - c_i) - \sum_{m \in M} \left( \sum_{i \in I} x_{m,i} \cdot t_{m,i} \right) \cdot r_m
$$

**Expanded Form:**
Let $Q_i$ be the total quantity of product $i$.
$Q_1 = x_{A1,1} + x_{A2,1} + x_{B1,1} + x_{B2,1} + x_{B3,1}$
$Q_2 = x_{A1,2} + x_{A2,2} + x_{B1,2}$
$Q_3 = x_{A2,3} + x_{B2,3}$

Contribution margins (Revenue - Material Cost):
*   $M_1 = 1.25 - 0.25 = 1.00$
*   $M_2 = 2.00 - 0.35 = 1.65$
*   $M_3 = 2.80 - 0.50 = 2.30$

Total Processing Cost:
*   $C_{A1} = 0.05(5 x_{A1,1} + 10 x_{A1,2})$
*   $C_{A2} = 0.03(7 x_{A2,1} + 9 x_{A2,2} + 12 x_{A2,3})$
*   $C_{B1} = 0.06(6 x_{B1,1} + 8 x_{B1,2})$
*   $C_{B2} = 0.11(4 x_{B2,1} + 11 x_{B2,3})$
*   $C_{B3} = 0.05(7 x_{B3,1})$

$$
\begin{aligned}
\text{MAXIMIZE } Z = \;& 1.00 Q_1 + 1.65 Q_2 + 2.30 Q_3 \\
&- [ 0.05(5 x_{A1,1} + 10 x_{A1,2}) \\
&+ 0.03(7 x_{A2,1} + 9 x_{A2,2} + 12 x_{A2,3}) \\
&+ 0.06(6 x_{B1,1} + 8 x_{B1,2}) \\
&+ 0.11(4 x_{B2,1} + 11 x_{B2,3}) \\
&+ 0.05(7 x_{B3,1}) ]
\end{aligned}
$$

### 4. Operational Constraints

**1. Flow Balance Constraints (Stage A output = Stage B input for each product)**
Every unit of product $i$ must pass through Stage A and Stage B exactly once.

*   **Product I:**
    $$ x_{A1,1} + x_{A2,1} = x_{B1,1} + x_{B2,1} + x_{B3,1} $$
*   **Product II:**
    $$ x_{A1,2} + x_{A2,2} = x_{B1,2} $$
    *(Note: Product II can only use B1 in Stage B)*
*   **Product III:**
    $$ x_{A2,3} = x_{B2,3} $$
    *(Note: Product III can only use A2 in Stage A and B2 in Stage B)*

**2. Machine Capacity Constraints**
The total processing time on each machine must not exceed its available hours.

*   **Machine A1:**
    $$ 5 x_{A1,1} + 10 x_{A1,2} \le 6000 $$
*   **Machine A2:**
    $$ 7 x_{A2,1} + 9 x_{A2,2} + 12 x_{A2,3} \le 10000 $$
*   **Machine B1:**
    $$ 6 x_{B1,1} + 8 x_{B1,2} \le 4000 $$
*   **Machine B2:**
    $$ 4 x_{B2,1} + 11 x_{B2,3} \le 7000 $$
*   **Machine B3:**
    $$ 7 x_{B3,1} \le 4000 $$

**3. Non-negativity Constraints**
$$ x_{m,i} \ge 0 \quad \forall m \in M, i \in I \text{ (where defined)} $$