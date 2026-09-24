To formulate the Goal Programming (GP) model for this problem, we must first identify the decision variables, the goals with their specific targets and priorities, and the system constraints.

### 1. Problem Analysis

**Decision Variables:**
Let $x_1, x_2, x_3$ be the quantities (in units of 500g) of Milk, Beef, and Eggs consumed daily, respectively. Since food can be consumed in continuous amounts, these are continuous variables ($x_j \ge 0$).

**Goals:**
The problem lists three goals. In standard Goal Programming, unless explicit priority weights ($P_1, P_2, \dots$) are given, we typically assume a lexicographic ordering based on the listing order or treat it as a weighted sum if weights are implied. However, usually, "Meet minimum requirement" is a hard constraint or a high-priority goal, while "Minimize cost/cholesterol" are lower priority.
*   **Goal 1:** Meet minimum daily requirements for Vitamins A, C, and D.
    *   Vitamin A: $1x_1 + 1x_2 + 10x_3 \ge 1$
    *   Vitamin C: $100x_1 + 10x_2 + 10x_3 \ge 30$
    *   Vitamin D: $10x_1 + 100x_2 + 10x_3 \ge 10$
    *   *Note:* In GP, these are typically modeled as goals to be satisfied as much as possible. We introduce negative deviation variables ($d_k^-$) to capture any shortage below the requirement.
*   **Goal 2:** Minimize daily cholesterol intake.
    *   Cholesterol: $70x_1 + 50x_2 + 120x_3$. We want to minimize this. We introduce a positive deviation variable ($d_4^+$) representing excess cholesterol above a target (or simply minimizing the total amount). Usually, in GP, we set a target $T_{chol}$ and minimize the excess $d^+$. If no target is given, we can treat the total cholesterol as a variable to minimize directly in the objective, or set a target of 0 and minimize $d^+$. Given the structure, it is cleaner to minimize the actual value or the deviation from a low target. Let's assume we want to keep it as low as possible.
*   **Goal 3:** Minimize daily food cost.
    *   Cost: $1.5x_1 + 8x_2 + 4x_3$. Similarly, we want to minimize this.

**Priority Structure:**
Standard textbook problems of this type often imply a priority order:
1.  **Priority 1 ($P_1$):** Satisfy nutritional requirements (minimize under-consumption of vitamins).
2.  **Priority 2 ($P_2$):** Minimize cholesterol.
3.  **Priority 3 ($P_3$):** Minimize cost.

*Note: If the problem does not specify priorities, one might assume equal weights, but "Meet minimum requirement" is usually the primary constraint/goal. I will formulate it as a standard hierarchical Goal Programming model where $P_1 \gg P_2 \gg P_3$. If a single-weighted objective is required, weights $w_k$ would be needed. Given the phrasing "The following three goals are set:", it implies a prioritized list.*

**Deviation Variables:**
For each goal equation, we add a negative deviation ($d^-$) and a positive deviation ($d^+$).
*   $d^- \ge 0$: Amount by which the goal is *under*-achieved (shortage).
*   $d^+ \ge 0$: Amount by which the goal is *over*-achieved (surplus).

**Goal Equations & Deviations to Minimize:**

1.  **Vitamin A:** Target 1 mg.
    Equation: $1x_1 + 1x_2 + 10x_3 + d_1^- - d_1^+ = 1$
    Goal: Minimize shortage $\rightarrow$ Minimize $d_1^-$

2.  **Vitamin C:** Target 30 mg.
    Equation: $100x_1 + 10x_2 + 10x_3 + d_2^- - d_2^+ = 30$
    Goal: Minimize shortage $\rightarrow$ Minimize $d_2^-$

3.  **Vitamin D:** Target 10 mg.
    Equation: $10x_1 + 100x_2 + 10x_3 + d_3^- - d_3^+ = 10$
    Goal: Minimize shortage $\rightarrow$ Minimize $d_3^-$

4.  **Cholesterol:** We want to minimize the total cholesterol.
    Let's set a target of 0 (or simply minimize the total amount).
    Equation: $70x_1 + 50x_2 + 120x_3 + d_4^- - d_4^+ = 0$? No, this forces cholesterol to be 0.
    Better approach: Define the cholesterol amount as the variable to be minimized in the objective function directly, or set a target $T_C$ and minimize $d^+$. Since "Minimize daily cholesterol intake" is the goal, we can simply put the cholesterol expression in the objective function with a negative sign (for maximization) or positive sign (for minimization) in the relevant priority level.
    However, standard GP formulates everything as $f(x) + d^- - d^+ = Target$.
    If we set Target = 0, then $70x_1 + 50x_2 + 120x_3 = d_4^+ - d_4^-$. Since LHS $\ge 0$, $d_4^- = 0$ and $d_4^+ = \text{Cholesterol Amount}$.
    So, minimizing Cholesterol is equivalent to minimizing $d_4^+$.
    Equation: $70x_1 + 50x_2 + 120x_3 - d_4^+ = 0$ (implicitly $d_4^- = 0$ because cholesterol cannot be negative relative to 0).
    Actually, it is safer to write: $70x_1 + 50x_2 + 120x_3 + d_4^- - d_4^+ = 0$. Since LHS $\ge 0$, $d_4^-$ will be 0. We minimize $d_4^+$.

5.  **Cost:** We want to minimize cost.
    Equation: $1.5x_1 + 8x_2 + 4x_3 + d_5^- - d_5^+ = 0$.
    Similarly, $d_5^- = 0$. We minimize $d_5^+$.

**Objective Function:**
Minimize $Z = P_1 (d_1^- + d_2^- + d_3^-) + P_2 (d_4^+) + P_3 (d_5^+)$
*(Note: If the problems implies equal importance or doesn't specify hierarchy, weights might be used. However, "Meet requirements" is logically superior to "Minimize cost". I will present the hierarchical model as it is the standard interpretation of such lists in OR textbooks.)*

### Formal Model

**Model Type:** Goal Programming (Linear)

**Index Sets & Parameters:**

*   **Foods ($j$):** $1$ (Milk), $2$ (Beef), $3$ (Eggs)
*   **Vitamins ($k$):** $1$ (Vit A), $2$ (Vit C), $3$ (Vit D)
*   **Parameters from Table 4-15:**
    *   **Vitamin Content ($a_{kj}$) (mg per 500g):**
        *   $a_{1,1}=1, a_{1,2}=1, a_{1,3}=10$ (Vit A)
        *   $a_{2,1}=100, a_{2,2}=10, a_{2,3}=10$ (Vit C)
        *   $a_{3,1}=10, a_{3,2}=100, a_{3,3}=10$ (Vit D)
    *   **Minimum Daily Requirements ($R_k$) (mg):**
        *   $R_1 = 1, R_2 = 30, R_3 = 10$
    *   **Cholesterol Content ($c_j$) (units per 500g):**
        *   $c_1=70, c_2=50, c_3=120$
    *   **Cost Content ($p_j$) (Yuan per 500g):**
        *   $p_1=1.5, p_2=8, p_3=4$
*   **Priorities:** $P_1$ (Nutrition), $P_2$ (Cholesterol), $P_3$ (Cost)

**Decision Variables:**
*   $x_j$: Quantity of food $j$ consumed (in 500g units), $x_j \ge 0, \forall j \in \{1,2,3\}$
*   $d_{1}^-, d_{1}^+$: Deviation variables for Vitamin A goal
*   $d_{2}^-, d_{2}^+$: Deviation variables for Vitamin C goal
*   $d_{3}^-, d_{3}^+$: Deviation variables for Vitamin D goal
*   $d_{4}^-, d_{4}^+$: Deviation variables for Cholesterol goal
*   $d_{5}^-, d_{5}^+$: Deviation variables for Cost goal
*   All $d \ge 0$.

**Objective Function:**
Minimize the lexicographic vector:
$$ \text{Min } Z = [ \; P_1 (d_1^- + d_2^- + d_3^-) \; , \; P_2 (d_4^+) \; , \; P_3 (d_5^+) \; ] $$

**Operational Constraints:**

1.  **Vitamin A Goal:**
    $$ 1x_1 + 1x_2 + 10x_3 + d_1^- - d_1^+ = 1 $$
2.  **Vitamin C Goal:**
    $$ 100x_1 + 10x_2 + 10x_3 + d_2^- - d_2^+ = 30 $$
3.  **Vitamin D Goal:**
    $$ 10x_1 + 100x_2 + 10x_3 + d_3^- - d_3^+ = 10 $$
4.  **Cholesterol Goal (Minimize Intake):**
    $$ 70x_1 + 50x_2 + 120x_3 - d_4^+ = 0 $$
    *(Note: $d_4^-$ is omitted as cholesterol cannot be negative, or included with $d_4^- = 0$ implied by non-negativity and LHS $\ge 0$. To be strictly formal: $70x_1 + 50x_2 + 120x_3 + d_4^- - d_4^+ = 0$)*
5.  **Cost Goal (Minimize Cost):**
    $$ 1.5x_1 + 8x_2 + 4x_3 + d_5^- - d_5^+ = 0 $$
    *(Note: $d_5^-$ is 0. We minimize $d_5^+$ which equals the total cost.)*

6.  **Non-negativity:**
    $$ x_j \ge 0, \quad d_i^\pm \ge 0 \quad \forall i, j $$

*(Self-Correction/Refinement on Cholesterol/Cost Goals)*:
In many GP formulations, if the goal is purely "Minimize $f(x)$", we don't necessarily need a target value of 0. We can just put $f(x)$ in the objective function directly if we are minimizing. However, to maintain the standard GP structure where all goals are equalities with deviations, setting the target to 0 and minimizing the positive deviation $d^+$ is the mathematically rigorous way to convert "Minimize $f(x)$" into a GP constraint.
Since $x_j \ge 0$, Cholesterol $\ge 0$ and Cost $\ge 0$.
For Cholesterol: $Chol + d_4^- - d_4^+ = 0$. Since $Chol \ge 0$, $d_4^- = 0$ and $d_4^+ = Chol$. Minimizing $d_4^+$ is equivalent to Minimizing Cholesterol.
For Cost: $Cost + d_5^- - d_5^+ = 0$. Since $Cost \ge 0$, $d_5^- = 0$ and $d_5^+ = Cost$. Minimizing $d_5^+$ is equivalent to Minimizing Cost.

This formulation is consistent.

### Final Output

**Model Type:** Goal Programming (Lexicographic)

**Index Sets & Parameters**
*   $J = \{1, 2, 3\}$: Set of foods (1=Milk, 2=Beef, 3=Eggs)
*   $K = \{1, 2, 3\}$: Set of vitamins (1=A, 2=C, 3=D)
*   $a_{k,j}$: Amount of vitamin $k$ (mg) in 500g of food $j$
    *   $a_{1,1}=1, a_{1,2}=1, a_{1,3}=10$
    *   $a_{2,1}=100, a_{2,2}=10, a_{2,3}=10$
    *   $a_{3,1}=10, a_{3,2}=100, a_{3,3}=10$
*   $R_k$: Minimum daily requirement for vitamin $k$ (mg)
    *   $R_1=1, R_2=30, R_3=10$
*   $c_j$: Cholesterol content (units) in 500g of food $j$
    *   $c_1=70, c_2=50, c_3=120$
*   $p_j$: Cost (Yuan) of 500g of food $j$
    *   $p_1=1.5, p_2=8, p_3=4$
*   $P_1, P_2, P_3$: Priority weights where $P_1 \gg P_2 \gg P_3$

**Decision Variables**
*   $x_j$: Amount of food $j$ consumed (in 500g units), $x_j \in \mathbb{R}^+$
*   $d_{1}^-, d_{1}^+$: Negative/Positive deviation for Vitamin A goal
*   $d_{2}^-, d_{2}^+$: Negative/Positive deviation for Vitamin C goal
*   $d_{3}^-, d_{3}^+$: Negative/Positive deviation for Vitamin D goal
*   $d_{4}^-, d_{4}^+$: Negative/Positive deviation for Cholesterol goal
*   $d_{5}^-, d_{5}^+$: Negative/Positive deviation for Cost goal
*   All deviation variables $d \in \mathbb{R}^+$

**Objective Function**
Minimize the lexicographic objective vector:
$$ \text{Min } Z = \left( \sum_{k=1}^{3} d_{k}^- , \quad d_{4}^+ , \quad d_{5}^+ \right) $$
*(This corresponds to Priority 1: Minimize vitamin shortages; Priority 2: Minimize cholesterol; Priority 3: Minimize cost)*

**Operational Constraints**
1.  **Vitamin A Goal:**
    $$ 1x_1 + 1x_2 + 10x_3 + d_1^- - d_1^+ = 1 $$
2.  **Vitamin C Goal:**
    $$ 100x_1 + 10x_2 + 10x_3 + d_2^- - d_2^+ = 30 $$
3.  **Vitamin D Goal:**
    $$ 10x_1 + 100x_2 + 10x_3 + d_3^- - d_3^+ = 10 $$
4.  **Cholesterol Goal:**
    $$ 70x_1 + 50x_2 + 120x_3 + d_4^- - d_4^+ = 0 $$
5.  **Cost Goal:**
    $$ 1.5x_1 + 8x_2 + 4x_3 + d_5^- - d_5^+ = 0 $$
6.  **Non-negativity:**
    $$ x_j \ge 0, \quad d_{i}^-, d_{i}^+ \ge 0 \quad \forall i \in \{1,..,5\}, j \in \{1,2,3\} $$