To formulate the Linear Programming (LP) model for this candy factory problem, we must carefully interpret the table data, specifically the "content proportions" which define the composition constraints for each brand.

### 1. Problem Analysis & Data Extraction

**Products:**
- Brand X ($x$)
- Brand Y ($y$)
- Brand Z ($z$)

**Raw Materials:** A, B, C

**Parameters from Table 1-17:**

*   **Raw Material Costs ($c_i$):**
    *   $c_A = 2.00$
    *   $c_B = 1.50$
    *   $c_C = 1.00$
*   **Monthly Usage Limits ($U_i$):**
    *   $U_A = 2000$ kg
    *   $U_B = 2500$ kg
    *   $U_C = 1200$ kg
*   **Processing Costs ($p_j$):**
    *   $p_X = 0.50$
    *   $p_Y = 0.40$
    *   $p_Z = 0.30$
*   **Selling Prices ($s_j$):**
    *   $s_X = 3.40$
    *   $s_Y = 2.85$
    *   $s_Z = 2.25$

**Composition Constraints (Interpreting the Table):**
The table lists specific percentage bounds for Raw Materials A and C. It is standard in such formulations that if a material is not explicitly bounded by a percentage in a specific brand, it is either unconstrained by that specific percentage rule or implied to be the remainder. However, looking closely at the table structure:
- **Brand X**: $A \ge 60\%$, $C \le 20\%$.
- **Brand Y**: $A \ge 30\%$, $C \le 50\%$.
- **Brand Z**: $C \le 60\%$.

*Implicit Assumption:* The sum of proportions for A, B, and C in any brand must equal 100% (1.0).
Therefore:
- **For Brand X**:
  - $A_X \ge 0.60$
  - $C_X \le 0.20$
  - $B_X = 1 - A_X - C_X$
- **For Brand Y**:
  - $A_Y \ge 0.30$
  - $C_Y \le 0.50$
  - $B_Y = 1 - A_Y - C_Y$
- **For Brand Z**:
  - $C_Z \le 0.60$
  - There are no explicit lower/upper bounds given for A or B in the table for Z, other than non-negativity and the sum-to-1 constraint. To maximize profit, the solver will determine the optimal mix of A and B given the cost differences. Note: Since A ($2.00) is more expensive than B ($1.50), the model will naturally minimize A in Z unless required by other constraints (which are absent for Z's A).

### 2. Decision Variables

Since the exact composition of each brand can vary within the specified ranges, we should define variables for the **amount of each raw material used in each brand**. This allows the model to optimize the specific recipe.

Let:
- $a_x, b_x, c_x$: kg of raw materials A, B, C used in Brand X.
- $a_y, b_y, c_y$: kg of raw materials A, B, C used in Brand Y.
- $a_z, b_z, c_z$: kg of raw materials A, B, C used in Brand Z.

Alternatively, and often more compactly for LP solvers, we can define the **total production quantity** of each brand ($X, Y, Z$) and the **proportion** of each material. However, using material quantities directly is linear and straightforward. Let's use the material quantity variables.

Let:
- $x_A, x_B, x_C$: Amount of material A, B, C in Brand X (kg).
- $y_A, y_B, y_C$: Amount of material A, B, C in Brand Y (kg).
- $z_A, z_B, z_C$: Amount of material A, B, C in Brand Z (kg).

The total production of each brand is the sum of its components:
- $X_{total} = x_A + x_B + x_C$
- $Y_{total} = y_A + y_B + y_C$
- $Z_{total} = z_A + z_B + z_C$

### 3. Objective Function

**Profit = Total Revenue - Total Raw Material Cost - Total Processing Cost**

1.  **Revenue:**
    $R = 3.40(x_A + x_B + x_C) + 2.85(y_A + y_B + y_C) + 2.25(z_A + z_B + z_C)$

2.  **Raw Material Cost:**
    $C_{mat} = 2.00(x_A + y_A + z_A) + 1.50(x_B + y_B + z_B) + 1.00(x_C + y_C + z_C)$

3.  **Processing Cost:**
    $C_{proc} = 0.50(x_A + x_B + x_C) + 0.40(y_A + y_B + y_C) + 0.30(z_A + z_B + z_C)$

**Maximize Profit ($Z_{obj}$):**
$$
\begin{aligned}
\text{Maximize } Z_{obj} = & \sum_{j \in \{X,Y,Z\}} (S_j - P_j) \sum_{i \in \{A,B,C\}} m_{ij} - \sum_{i \in \{A,B,C\}} c_i \sum_{j \in \{X,Y,Z\}} m_{ij} \\
\end{aligned}
$$
Expanding by variable for clarity in the final formulation:

For **Brand X**:
Contribution per kg of A: $3.40 - 0.50 - 2.00 = 0.90$
Contribution per kg of B: $3.40 - 0.50 - 1.50 = 1.40$
Contribution per kg of C: $3.40 - 0.50 - 1.00 = 1.90$

For **Brand Y**:
Contribution per kg of A: $2.85 - 0.40 - 2.00 = 0.45$
Contribution per kg of B: $2.85 - 0.40 - 1.50 = 0.95$
Contribution per kg of C: $2.85 - 0.40 - 1.00 = 1.45$

For **Brand Z**:
Contribution per kg of A: $2.25 - 0.30 - 2.00 = -0.05$
Contribution per kg of B: $2.25 - 0.30 - 1.50 = 0.45$
Contribution per kg of C: $2.25 - 0.30 - 1.00 = 0.95$

$$
\text{Maximize } Z = 0.90x_A + 1.40x_B + 1.90x_C + 0.45y_A + 0.95y_B + 1.45y_C - 0.05z_A + 0.45z_B + 0.95z_C
$$

### 4. Constraints

**A. Composition Constraints (Proportions)**

*For Brand X ($X_T = x_A+x_B+x_C$):*
1.  $A \ge 60\% \implies x_A \ge 0.60(x_A + x_B + x_C) \implies 0.40x_A - 0.60x_B - 0.60x_C \ge 0$
2.  $C \le 20\% \implies x_C \le 0.20(x_A + x_B + x_C) \implies -0.20x_A - 0.20x_B + 0.80x_C \le 0$

*For Brand Y ($Y_T = y_A+y_B+y_C$):*
3.  $A \ge 30\% \implies y_A \ge 0.30(y_A + y_B + y_C) \implies 0.70y_A - 0.30y_B - 0.30y_C \ge 0$
4.  $C \le 50\% \implies y_C \le 0.50(y_A + y_B + y_C) \implies -0.50y_A - 0.50y_B + 0.50y_C \le 0$

*For Brand Z ($Z_T = z_A+z_B+z_C$):*
5.  $C \le 60\% \implies z_C \le 0.60(z_A + z_B + z_C) \implies -0.60z_A - 0.60z_B + 0.40z_C \le 0$

*(Note: Non-negativity of ingredients ensures proportions are $\le 100\%$ implicitly if the sum is consistent, but the sum-to-1 is handled by the definition of the variables as components of the total. The constraints above ensure the relative ratios.)*

**B. Raw Material Availability Constraints**

Total usage of each raw material across all brands cannot exceed the monthly limit.

6.  **Material A:** $x_A + y_A + z_A \le 2000$
7.  **Material B:** $x_B + y_B + z_B \le 2500$
8.  **Material C:** $x_C + y_C + z_C \le 1200$

**C. Non-negativity Constraints**

All material usage variables must be non-negative.
9.  $x_A, x_B, x_C, y_A, y_B, y_C, z_A, z_B, z_C \ge 0$

### Final Mathematical Formulation

**Model Type:** Linear Programming (LP)

**Index Sets:**
- $I = \{A, B, C\}$: Set of raw materials.
- $J = \{X, Y, Z\}$: Set of candy brands.

**Parameters:**
- $c_i$: Cost of raw material $i$ ($\$/\text{kg}$).
  - $c_A = 2.00, c_B = 1.50, c_C = 1.00$
- $U_i$: Monthly limit of raw material $i$ (kg).
  - $U_A = 2000, U_B = 2500, U_C = 1200$
- $p_j$: Processing cost of brand $j$ ($\$/\text{kg}$).
  - $p_X = 0.50, p_Y = 0.40, p_Z = 0.30$
- $s_j$: Selling price of brand $j$ ($\$/\text{kg}$).
  - $s_X = 3.40, s_Y = 2.85, s_Z = 2.25$

**Decision Variables:**
- $m_{ij} \ge 0$: Amount (kg) of raw material $i$ used in brand $j$.

**Objective Function:**
Maximize Total Profit $Z$:
$$
\begin{aligned}
\text{Maximize } Z = & \quad (3.40 - 0.50 - 2.00)m_{AX} + (3.40 - 0.50 - 1.50)m_{BX} + (3.40 - 0.50 - 1.00)m_{CX} \\
& + (2.85 - 0.40 - 2.00)m_{AY} + (2.85 - 0.40 - 1.50)m_{BY} + (2.85 - 0.40 - 1.00)m_{CY} \\
& + (2.25 - 0.30 - 2.00)m_{AZ} + (2.25 - 0.30 - 1.50)m_{BZ} + (2.25 - 0.30 - 1.00)m_{CZ}
\end{aligned}
$$
Simplifying coefficients:
$$
\begin{aligned}
\text{Maximize } Z = & \quad 0.90m_{AX} + 1.40m_{BX} + 1.90m_{CX} \\
& + 0.45m_{AY} + 0.95m_{BY} + 1.45m_{CY} \\
& - 0.05m_{AZ} + 0.45m_{BZ} + 0.95m_{CZ}
\end{aligned}
$$

**Subject to:**

**1. Composition Constraints:**
For Brand X:
$$
\begin{aligned}
0.40m_{AX} - 0.60m_{BX} - 0.60m_{CX} &\ge 0 \quad (\text{A} \ge 60\%) \\
-0.20m_{AX} - 0.20m_{BX} + 0.80m_{CX} &\le 0 \quad (\text{C} \le 20\%)
\end{aligned}
$$

For Brand Y:
$$
\begin{aligned}
0.70m_{AY} - 0.30m_{BY} - 0.30m_{CY} &\ge 0 \quad (\text{A} \ge 30\%) \\
-0.50m_{AY} - 0.50m_{BY} + 0.50m_{CY} &\le 0 \quad (\text{C} \le 50\%)
\end{aligned}
$$

For Brand Z:
$$
-0.60m_{AZ} - 0.60m_{BZ} + 0.40m_{CZ} \le 0 \quad (\text{C} \le 60\%)
$$

**2. Resource Availability Constraints:**
$$
\begin{aligned}
m_{AX} + m_{AY} + m_{AZ} &\le 2000 \quad (\text{Limit A}) \\
m_{BX} + m_{BY} + m_{BZ} &\le 2500 \quad (\text{Limit B}) \\
m_{CX} + m_{CY} + m_{CZ} &\le 1200 \quad (\text{Limit C})
\end{aligned}
$$

**3. Non-negativity Constraints:**
$$
m_{ij} \ge 0 \quad \forall i \in \{A,B,C\}, j \in \{X,Y,Z\}
$$