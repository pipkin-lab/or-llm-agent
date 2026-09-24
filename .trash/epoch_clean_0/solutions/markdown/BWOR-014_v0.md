Based on the problem description, this is a **Goal Programming (GP)** problem. The objective is to minimize the weighted sum of deviations from the established goals, prioritizing the achievement of minimum vitamin requirements over minimizing cholesterol and cost.

Here is the formal mathematical formulation.

### 1. Index Sets & Parameters

**Indices:**
*   $f$: Set of food items, $f \in \{M, B, E\}$ (Milk, Beef, Eggs).
*   $g$: Set of goals, $g \in \{1, 2, 3\}$.
    *   $g=1$: Vitamin Requirements (Goal 1)
    *   $g=2$: Cholesterol Intake (Goal 2)
    *   $g=3$: Food Cost (Goal 3)
*   $v$: Set of vitamins, $v \in \{A, C, D\}$.

**Parameters (from Table 4-15):**

*   **Nutritional Content Matrix $a_{v,f}$ (mg per 500g):**
    *   Vitamin A: $a_{A,M}=1, a_{A,B}=1, a_{A,E}=10$
    *   Vitamin C: $a_{C,M}=100, a_{C,B}=10, a_{C,E}=10$
    *   Vitamin D: $a_{D,M}=10, a_{D,B}=100, a_{D,E}=10$
*   **Minimum Daily Vitamin Requirements $R_v$ (mg):**
    *   $R_A = 1$
    *   $R_C = 30$
    *   $R_D = 10$
*   **Cholesterol Content $c_f$ (units per 500g):**
    *   $c_M = 70, c_B = 50, c_E = 120$
*   **Cost per Unit $p_f$ (Yuan per 500g):**
    *   $p_M = 1.5, p_B = 8, p_E = 4$
*   **Goal Targets:**
    *   Target Cholesterol ($T_{chol}$): Not explicitly given as a hard cap, but the goal is to *minimize*. In standard GP, we set a target value $T_2$ (often 0 or a reasonable low value, but typically modeled as minimizing the positive deviation from a target of 0 or just minimizing the variable itself if it's a secondary goal). However, standard GP formulation for "minimize $X$" uses a target $T$ and minimizes $d^+$. If no specific target is given, we can set the target to 0 or treat the minimization of the variable directly via deviation from 0. Let's assume the target for cholesterol is 0 (ideal) or simply minimize the positive deviation from a low baseline. Given the context of "Minimize", we define the goal as $Z_{chol} \le T_{chol}$. Let's assume a target $T_{chol} = 0$ (ideal minimum) or simply minimize the positive deviation. A more robust interpretation for "Minimize Cost/Cholesterol" in GP is to set a target and penalize exceeding it. Since no target is given, we minimize the positive deviation from 0.
    *   Target Cost ($T_{cost}$): Similarly, minimize positive deviation from 0.

**Priorities/Weights:**
The problem lists three goals. Usually, "Meet minimum requirements" is a hard constraint or Priority 1. "Minimize cholesterol" and "Minimize cost" are secondary.
*   **Priority 1 ($P_1$):** Satisfy minimum vitamin requirements. We penalize the negative deviation ($d^-$) of the vitamin constraints.
*   **Priority 2 ($P_2$):** Minimize Cholesterol. We penalize the positive deviation ($d^+$) from a target (or simply minimize the value).
*   **Priority 3 ($P_3$):** Minimize Cost. We penalize the positive deviation ($d^+$) from a target (or simply minimize the value).

*Note: In many textbook GP examples of this type, if specific weights are not given, we assume lexicographic ordering: Priority 1 > Priority 2 > Priority 3.*

### 2. Decision Variables

**Primary Variables:**
*   $x_M, x_B, x_E \ge 0$: Amount of Milk, Beef, and Eggs consumed (in units of 500g).

**Deviation Variables:**
*   **For Vitamin A:**
    *   $d_A^- \ge 0$: Amount by which Vitamin A intake is *below* the requirement.
    *   $d_A^+ \ge 0$: Amount by which Vitamin A intake is *above* the requirement.
*   **For Vitamin C:**
    *   $d_C^- \ge 0$: Amount by which Vitamin C intake is *below* the requirement.
    *   $d_C^+ \ge 0$: Amount by which Vitamin C intake is *above* the requirement.
*   **For Vitamin D:**
    *   $d_D^- \ge 0$: Amount by which Vitamin D intake is *below* the requirement.
    *   $d_D^+ \ge 0$: Amount by which Vitamin D intake is *above* the requirement.
*   **For Cholesterol:**
    *   $d_{chol}^+ \ge 0$: Amount by which Cholesterol intake exceeds the target (Target = 0).
    *   $d_{chol}^- \ge 0$: Amount by which Cholesterol intake is below the target (Target = 0).
*   **For Cost:**
    *   $d_{cost}^+ \ge 0$: Amount by which Cost exceeds the target (Target = 0).
    *   $d_{cost}^- \ge 0$: Amount by which Cost is below the target (Target = 0).

### 3. Objective Function

We use a lexicographic goal programming objective. We minimize the weighted sum of deviations, prioritizing higher-priority goals.

$$ \text{Minimize } Z = P_1 (d_A^- + d_C^- + d_D^-) + P_2 (d_{chol}^+) + P_3 (d_{cost}^+) $$

Where $P_1 \gg P_2 \gg P_3$.

*(Note: If a single weighted sum is required instead of lexicographic, weights $w_1, w_2, w_3$ would be applied. Given the phrasing "Meet... 2. Minimize... 3. Minimize", lexicographic or hierarchical minimization is standard.)*

### 4. Operational Constraints

**1. System Constraints (Vitamin Intake Balance):**
The actual intake equals the requirement plus the net deviation.
$$ 1 x_M + 1 x_B + 10 x_E + d_A^- - d_A^+ = 1 $$
$$ 100 x_M + 10 x_B + 10 x_E + d_C^- - d_C^+ = 30 $$
$$ 10 x_M + 100 x_B + 10 x_E + d_D^- - d_D^+ = 10 $$

**2. System Constraints (Cholesterol Intake Balance):**
We define the goal as keeping cholesterol as low as possible. We model this by setting a target of 0 and penalizing the positive deviation (intake above 0).
$$ 70 x_M + 50 x_B + 120 x_E + d_{chol}^- - d_{chol}^+ = 0 $$
*(Note: Since $x_i \ge 0$, LHS $\ge 0$, so $d_{chol}^- = 0$ effectively. The constraint simplifies to $70 x_M + 50 x_B + 120 x_E = d_{chol}^+$.)*

**3. System Constraints (Cost Balance):**
Similarly, we set a target cost of 0 and penalize the positive deviation (cost above 0).
$$ 1.5 x_M + 8 x_B + 4 x_E + d_{cost}^- - d_{cost}^+ = 0 $$
*(Note: Since $x_i \ge 0$, LHS $\ge 0$, so $d_{cost}^- = 0$ effectively. The constraint simplifies to $1.5 x_M + 8 x_B + 4 x_E = d_{cost}^+$.)*

**4. Non-negativity Constraints:**
$$ x_M, x_B, x_E \ge 0 $$
$$ d_A^-, d_A^+, d_C^-, d_C^+, d_D^-, d_D^+, d_{chol}^-, d_{chol}^+, d_{cost}^-, d_{cost}^+ \ge 0 $$

### Summary of the Model

**Sets:**
$F = \{M, B, E\}$, $V = \{A, C, D\}$

**Parameters:**
$a_{A,M}=1, a_{A,B}=1, a_{A,E}=10$
$a_{C,M}=100, a_{C,B}=10, a_{C,E}=10$
$a_{D,M}=10, a_{D,B}=100, a_{D,E}=10$
$R_A=1, R_C=30, R_D=10$
$chol_M=70, chol_B=50, chol_E=120$
$cost_M=1.5, cost_B=8, cost_E=4$

**Variables:**
$x_M, x_B, x_E \ge 0$
$d_A^-, d_A^+, d_C^-, d_C^+, d_D^-, d_D^+, d_{chol}^+, d_{cost}^+ \ge 0$
*(Negative deviations for cholesterol and cost are redundant due to non-negativity of x, so they are omitted from the final simplified model for clarity, though they can be included for formal completeness.)*

**Objective:**
Minimize $Z = P_1(d_A^- + d_C^- + d_D^-) + P_2(d_{chol}^+) + P_3(d_{cost}^+)$

**Constraints:**
1.  $x_M + x_B + 10x_E + d_A^- - d_A^+ = 1$
2.  $100x_M + 10x_B + 10x_E + d_C^- - d_C^+ = 30$
3.  $10x_M + 100x_B + 10x_E + d_D^- - d_D^+ = 10$
4.  $70x_M + 50x_B + 120x_E - d_{chol}^+ = 0$
5.  $1.5x_M + 8x_B + 4x_E - d_{cost}^+ = 0$
6.  $x_M, x_B, x_E, d_A^-, d_A^+, d_C^-, d_C^+, d_D^-, d_D^+, d_{chol}^+, d_{cost}^+ \ge 0$