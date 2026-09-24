# Goal Programming Model for Dietary Optimization

## 1. Index Sets & Parameters

**Sets:**
*   $F = \{1, 2, 3\}$: Set of food items, where $1$ = Milk, $2$ = Beef, $3$ = Eggs.
*   $V = \{1, 2, 3\}$: Set of vitamins, where $1$ = Vitamin A, $2$ = Vitamin C, $3$ = Vitamin D.

**Parameters:**
*   $a_{v,f}$: Amount of vitamin $v$ (mg) per 500g unit of food $f$.
    *   $a_{1,1}=1, a_{1,2}=1, a_{1,3}=10$ (Vitamin A)
    *   $a_{2,1}=100, a_{2,2}=10, a_{2,3}=10$ (Vitamin C)
    *   $a_{3,1}=10, a_{3,2}=100, a_{3,3}=10$ (Vitamin D)
*   $b_v$: Minimum daily requirement for vitamin $v$ (mg).
    *   $b_1=1, b_2=30, b_3=10$
*   $c_f$: Cholesterol content (units) per 500g unit of food $f$.
    *   $c_1=70, c_2=50, c_3=120$
*   $p_f$: Cost (Yuan) per 500g unit of food $f$.
    *   $p_1=1.5, p_2=8, p_3=4$

**Goal Priorities (Assumed Hierarchy):**
Since the problem lists goals in a specific order without explicit weights, standard Goal Programming assumes a lexicographic hierarchy based on the order of importance. Typically, nutritional safety (meeting minimums) is the highest priority, followed by health optimization (cholesterol), and finally economic optimization (cost).
*   $P_1$: Priority 1 (Highest) - Meet minimum vitamin requirements.
*   $P_2$: Priority 2 - Minimize cholesterol intake.
*   $P_3$: Priority 3 (Lowest) - Minimize cost.

## 2. Decision Variables

**Primary Decision Variables:**
*   $x_f \ge 0$: Continuous variable representing the number of 500g units of food $f$ consumed daily ($f \in F$).

**Deviation Variables:**
For each goal, we define negative deviation ($d_k^-$) and positive deviation ($d_k^+$) variables.

**Goal 1: Vitamin Requirements (3 sub-goals)**
*   $d_{v}^-, d_{v}^+ \ge 0$: Deviation variables for vitamin $v$ ($v \in V$).
    *   $d_v^-$: Amount by which the intake falls short of the minimum requirement (underachievement).
    *   $d_v^+$: Amount by which the intake exceeds the minimum requirement (overachievement).

**Goal 2: Cholesterol Intake**
*   Let $C_{target}$ be the target cholesterol level. In minimization goals without a specific target value, the target is effectively 0 (or the minimum possible). However, standard GP formulation for "minimize a quantity" often sets the target to 0 or a specific threshold. If no threshold is given, we minimize the total cholesterol directly. To fit the GP structure strictly, we can define the goal as: $Total Cholesterol = 0$ is impossible, so we minimize the positive deviation from a target $T_c$.
    *   *Alternative Standard Approach*: If no specific target is given for cholesterol, we treat it as a secondary objective to be minimized. In a weighted GP model, we minimize $d_c^+$. If we assume the "target" is the absolute minimum possible (which is 0, though biologically impossible), $d_c^+$ represents the total cholesterol.
    *   Let's define the equation: $\sum c_f x_f + d_c^- - d_c^+ = T_c$.
    *   Since we want to *minimize* cholesterol, and there is no lower bound target other than 0, we set $T_c = 0$. Then $d_c^+$ represents the total cholesterol consumed. We minimize $d_c^+$.
    *   $d_c^- \ge 0, d_c^+ \ge 0$: Deviation variables for cholesterol.

**Goal 3: Food Cost**
*   Let $Cost_{target}$ be the target cost. Similarly, we want to minimize cost.
    *   Equation: $\sum p_f x_f + d_{cost}^- - d_{cost}^+ = T_{cost}$.
    *   Set $T_{cost} = 0$. Then $d_{cost}^+$ represents the total cost. We minimize $d_{cost}^+$.
    *   $d_{cost}^- \ge 0, d_{cost}^+ \ge 0$: Deviation variables for cost.

## 3. Objective Function

We use a **Lexicographic Goal Programming** objective function, minimizing the deviations in order of priority.

$$ \min Z = \left( P_1 \sum_{v \in V} d_v^-, \quad P_2 d_c^+, \quad P_3 d_{cost}^+ \right) $$

**Explanation:**
1.  **Priority 1 ($P_1$)**: Minimize the sum of under-achievements for all vitamins ($\sum d_v^-$). We do *not* penalize over-achievement ($d_v^+$) for vitamins, as consuming more than the minimum is generally acceptable or beneficial, unless specified otherwise.
2.  **Priority 2 ($P_2$)**: Minimize the positive deviation of cholesterol from the target of 0 ($d_c^+$), which effectively minimizes total cholesterol intake.
3.  **Priority 3 ($P_3$)**: Minimize the positive deviation of cost from the target of 0 ($d_{cost}^+$), which effectively minimizes total cost.

*(Note: If a Weighted Goal Programming approach is preferred, the objective would be a single scalar: $Z = w_1 \sum d_v^- + w_2 d_c^+ + w_3 d_{cost}^+$, where $w_1 \gg w_2 \gg w_3$.)*

## 4. Operational Constraints

**1. System Constraints (Linking Decision Variables to Deviations)**

**Vitamin Constraints:**
For each vitamin $v \in \{1, 2, 3\}$:
$$ \sum_{f \in F} a_{v,f} x_f + d_v^- - d_v^+ = b_v $$

Explicitly:
*   **Vitamin A**: $1x_1 + 1x_2 + 10x_3 + d_A^- - d_A^+ = 1$
*   **Vitamin C**: $100x_1 + 10x_2 + 10x_3 + d_C^- - d_C^+ = 30$
*   **Vitamin D**: $10x_1 + 100x_2 + 10x_3 + d_D^- - d_D^+ = 10$

**Cholesterol Constraint:**
Target $T_c = 0$ (to minimize intake):
$$ 70x_1 + 50x_2 + 120x_3 + d_c^- - d_c^+ = 0 $$
*Since $x_f \ge 0$ and $c_f > 0$, the sum $70x_1 + 50x_2 + 120x_3$ is always non-negative. Therefore, $d_c^-$ must be 0, and $d_c^+$ equals the total cholesterol.*

**Cost Constraint:**
Target $T_{cost} = 0$ (to minimize cost):
$$ 1.5x_1 + 8x_2 + 4x_3 + d_{cost}^- - d_{cost}^+ = 0 $$
*Similarly, $d_{cost}^-$ must be 0, and $d_{cost}^+$ equals the total cost.*

**2. Non-negativity Constraints**

$$ x_f \ge 0, \quad \forall f \in F $$
$$ d_v^-, d_v^+ \ge 0, \quad \forall v \in V $$
$$ d_c^-, d_c^+ \ge 0 $$
$$ d_{cost}^-, d_{cost}^+ \ge 0 $$

### Summary of the Final Model

**Variables:**
$x_1, x_2, x_3 \ge 0$
$d_A^-, d_A^+, d_C^-, d_C^+, d_D^-, d_D^+, d_c^-, d_c^+, d_{cost}^-, d_{cost}^+ \ge 0$

**Objective:**
Minimize Lexicographically:
1.  $Z_1 = d_A^- + d_C^- + d_D^-$
2.  $Z_2 = d_c^+$
3.  $Z_3 = d_{cost}^+$

**Subject to:**
1.  $x_1 + x_2 + 10x_3 + d_A^- - d_A^+ = 1$
2.  $100x_1 + 10x_2 + 10x_3 + d_C^- - d_C^+ = 30$
3.  $10x_1 + 100x_2 + 10x_3 + d_D^- - d_D^+ = 10$
4.  $70x_1 + 50x_2 + 120x_3 + d_c^- - d_c^+ = 0$
5.  $1.5x_1 + 8x_2 + 4x_3 + d_{cost}^- - d_{cost}^+ = 0$
6.  All variables $\ge 0$