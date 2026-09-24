# Goal Programming Model for Jinyuan Company Production Planning

## Model Type Declaration
**Model Type:** MILP (Mixed-Integer Linear Programming)
*Note: While the underlying structure is linear, production quantities are discrete physical units. However, given the large scale of demands (hundreds to thousands), **LP (Linear Programming)** is also acceptable if fractional production is permitted. Given standard interpretation of "quantity of products" in such textbook contexts, we assume **continuous variables** are acceptable for production quantities to allow for exact goal attainment where possible, but strictly speaking, integer constraints are appropriate. Below, we specify **continuous non-negative variables** as the primary formulation, noting that integer constraints can be added if required. Given the large numbers, LP is the standard approach for this type of goal programming problem.*

**Correction on Model Type:** The problem involves minimizing weighted deviations. This is a **Linear Goal Programming** model. Since all relationships are linear, it is an **LP** (or MILP if integer production is enforced). We will formulate as **LP** for clarity, as fractional units are often assumed in aggregate production planning unless "integer" is explicitly stated for discrete items like machines. Here, "products" are generic, so **LP** is appropriate.

## Index Sets & Parameters

**Index Sets:**
*   $P = \{1, 2, 3\}$: Set of products (Product 1, Product 2, Product 3)
*   $T = \{1, 2, 3\}$: Set of planning stages (Stage 1, Stage 2, Stage 3)

**Parameters (from Tables 4-16 and 4-17):**

**Demand ($D_{p,t}$) in units:**
*   Stage 1: $D_{1,1}=500$, $D_{2,1}=750$, $D_{3,1}=900$
*   Stage 2: $D_{1,2}=680$, $D_{2,2}=800$, $D_{3,2}=800$
*   Stage 3: $D_{1,3}=800$, $D_{2,3}=950$, $D_{3,3}=1000$

**Resource Consumption Coefficients:**
*   Equipment Working Hours ($a_{p}$) per unit (hours):
    *   $a_1 = 2.0$, $a_2 = 1.0$, $a_3 = 3.1$
*   Working Capital ($b_{p}$) per unit (yuan):
    *   $b_1 = 40$, $b_2 = 20$, $b_3 = 55$

**Resource Limits per Stage:**
*   Equipment Hours Limit ($H$) = 5000 hours
*   Working Capital Limit ($W$) = 93,000 yuan

**Goal Priorities & Weights:**
*   Priority 1: Minimize stockouts (unmet demand).
    *   Weight for Product 3 ($w_3$) = 2
    *   Weight for Product 1 ($w_1$) = 1
    *   Weight for Product 2 ($w_2$) = 1
*   Priority 2: Minimize overloading of equipment.
    *   Weight for equipment overloading = 1 (default, as no specific weight is given, just "minimize").
*   Priority 3: Ensure working capital usage does not exceed the limit.
    *   This is typically a hard constraint or a very high priority goal. The problem states "Ensure that... does not exceed", which implies a **hard constraint** or a Priority 3 goal with 0 tolerance for violation. Given the phrasing "prioritized objectives", we treat this as Goal 3. However, "Ensure... does not exceed" strongly suggests it should be treated as a constraint $g_{3}^- = 0$ or a hard constraint. Let's look at the standard goal programming structure. Usually, "ensure" implies a hard constraint. But since it's listed as a prioritized objective, we model it as a goal to be met, with the deviation variable for exceeding the limit being minimized at the lowest priority. *Correction*: In many textbook contexts, "Ensure X does not exceed Y" is a hard constraint. However, if it's listed as objective 3, it might be a soft constraint. Let's assume it is a **hard constraint** first. If the model is infeasible, it becomes a goal. Given the resources:
        *   Max possible production based on capital in one stage: $93000 / \min(40,20,55) = 4650$ units (if only prod 2).
        *   Total demand in one stage: $500+750+900 = 2150$ units.
        *   Capital needed for all demand in Stage 1: $500(40) + 750(20) + 900(55) = 20000 + 15000 + 49500 = 84500 \le 93000$.
        *   Capital needed for all demand in Stage 3: $800(40) + 950(20) + 1000(55) = 32000 + 19000 + 55000 = 106000 > 93000$.
        *   So, for Stage 3, meeting all demand violates the capital limit. Thus, the capital limit is **binding**. It must be treated as a **Goal** (Priority 3) or a Hard Constraint that makes the problem infeasible if we also demand zero stockouts. Since we have priorities, we treat it as a Goal: Minimize the amount by which capital exceeds the limit.

## Decision Variables

1.  **Production Variables:**
    *   $x_{p,t}$: Quantity of product $p$ produced in stage $t$.
    *   Domain: $x_{p,t} \ge 0$ for all $p \in P, t \in T$.

2.  **Deviation Variables for Goal 1 (Stockouts):**
    *   $s_{p,t}^-$: Amount of demand for product $p$ in stage $t$ **not** met (stockout).
    *   $s_{p,t}^+$: Amount of demand for product $p$ in stage $t$ met in excess (overproduction/surplus inventory).
    *   Domain: $s_{p,t}^-, s_{p,t}^+ \ge 0$.
    *   *Note:* The problem states "initial and final inventories are zero". This implies we produce exactly what is needed plus/minus the deviation. It does not explicitly allow carrying inventory between stages to meet future demand. Usually, "production plan... determine quantity... at each stage" with "initial/final inventory zero" implies **independent stages** or that production in stage $t$ is for demand in stage $t$ only. If inventory carrying were allowed, the problem would typically specify holding costs or inventory variables. Given the structure "Demand at Each Stage" and separate resource limits per stage, it is standard to assume **production in stage $t$ satisfies demand in stage $t$**. We will model $x_{p,t}$ as production for stage $t$ demand.
    *   Equation: $x_{p,t} + s_{p,t}^- - s_{p,t}^+ = D_{p,t}$

3.  **Deviation Variables for Goal 2 (Equipment Overloading):**
    *   $e_t^-$: Underutilization of equipment hours in stage $t$ (slack).
    *   $e_t^+$: Overloading of equipment hours in stage $t$ (violation).
    *   Domain: $e_t^-, e_t^+ \ge 0$.
    *   Equation: $\sum_{p \in P} a_p x_{p,t} + e_t^- - e_t^+ = H$

4.  **Deviation Variables for Goal 3 (Working Capital):**
    *   $c_t^-$: Unused working capital in stage $t$ (slack).
    *   $c_t^+$: Excess working capital usage in stage $t$ (violation).
    *   Domain: $c_t^-, c_t^+ \ge 0$.
    *   Equation: $\sum_{p \in P} b_p x_{p,t} + c_t^- - c_t^+ = W$

## Objective Function

The problem specifies three **prioritized** objectives. This requires a **preemptive (lexicographic) goal programming** approach. We cannot simply sum the deviations with weights because "Priority 1" is more important than "Priority 2", etc.

**Priority Level 1:** Minimize weighted stockouts.
*   Weights: $w_1=1, w_2=1, w_3=2$.
*   Objective: $Z_1 = \sum_{t \in T} \sum_{p \in P} w_p s_{p,t}^-$
    *   $Z_1 = 1(s_{1,1}^- + s_{1,2}^- + s_{1,3}^-) + 1(s_{2,1}^- + s_{2,2}^- + s_{2,3}^-) + 2(s_{3,1}^- + s_{3,2}^- + s_{3,3}^-)$

**Priority Level 2:** Minimize equipment overloading.
*   Objective: $Z_2 = \sum_{t \in T} e_t^+$
    *   $Z_2 = e_1^+ + e_2^+ + e_3^+$

**Priority Level 3:** Minimize working capital excess.
*   Objective: $Z_3 = \sum_{t \in T} c_t^+$
    *   $Z_3 = c_1^+ + c_2^+ + c_3^+$

**Overall Optimization Strategy:**
1.  Solve the LP to minimize $Z_1$. Let the optimal value be $Z_1^*$.
2.  Add constraint $Z_1 = Z_1^*$ (or $Z_1 \le Z_1^* + \epsilon$).
3.  Solve the LP to minimize $Z_2$. Let the optimal value be $Z_2^*$.
4.  Add constraint $Z_2 = Z_2^*$.
5.  Solve the LP to minimize $Z_3$.

Alternatively, if a single weighted objective is required (non-preemptive), the problem statement "prioritized objectives" strongly implies lexicographic ordering. However, for the purpose of providing a single solvable mathematical model structure, we often present it as a **weighted sum with large weights** (Big-M method for priorities) or simply state the lexicographic sequence. Given the instruction to "formulate a mathematical model", the lexicographic formulation is the most accurate representation of "prioritized".

If a single linear objective is strictly required for a standard solver interface without multi-stage solving, we can approximate with:
$$ \text{Minimize } Z = M_1 \sum_{t,p} w_p s_{p,t}^- + M_2 \sum_{t} e_t^+ + M_3 \sum_{t} c_t^+ $$
where $M_1 \gg M_2 \gg M_3$ (e.g., $M_1=10^6, M_2=10^3, M_3=1$).

However, the standard OR formulation for "prioritized" is **Lexicographic Goal Programming**.

## Operational Constraints

**1. Demand Balance Constraints (for all $p \in P, t \in T$):**
$$ x_{p,t} + s_{p,t}^- - s_{p,t}^+ = D_{p,t} $$
*   This ensures that production plus unmet demand minus surplus equals total demand.

**2. Equipment Hours Balance Constraints (for all $t \in T$):**
$$ \sum_{p=1}^{3} a_p x_{p,t} + e_t^- - e_t^+ = 5000 $$
*   Expanded for Stage 1: $2.0 x_{1,1} + 1.0 x_{2,1} + 3.1 x_{3,1} + e_1^- - e_1^+ = 5000$
*   Expanded for Stage 2: $2.0 x_{1,2} + 1.0 x_{2,2} + 3.1 x_{3,2} + e_2^- - e_2^+ = 5000$
*   Expanded for Stage 3: $2.0 x_{1,3} + 1.0 x_{2,3} + 3.1 x_{3,3} + e_3^- - e_3^+ = 5000$

**3. Working Capital Balance Constraints (for all $t \in T$):**
$$ \sum_{p=1}^{3} b_p x_{p,t} + c_t^- - c_t^+ = 93000 $$
*   Expanded for Stage 1: $40 x_{1,1} + 20 x_{2,1} + 55 x_{3,1} + c_1^- - c_1^+ = 93000$
*   Expanded for Stage 2: $40 x_{1,2} + 20 x_{2,2} + 55 x_{3,2} + c_2^- - c_2^+ = 93000$
*   Expanded for Stage 3: $40 x_{1,3} + 20 x_{2,3} + 55 x_{3,3} + c_3^- - c_3^+ = 93000$

**4. Non-negativity Constraints:**
$$ x_{p,t} \ge 0, \quad s_{p,t}^- \ge 0, \quad s_{p,t}^+ \ge 0, \quad e_t^- \ge 0, \quad e_t^+ \ge 0, \quad c_t^- \ge 0, \quad c_t^+ \ge 0 $$
for all $p \in P, t \in T$.

## Summary of the Model Structure for Solving

To solve this, one would typically use a **lexicographic sequence**:

1.  **Stage 1 of Optimization:**
    $$ \text{Minimize } Z_1 = \sum_{t=1}^3 (1 \cdot s_{1,t}^- + 1 \cdot s_{2,t}^- + 2 \cdot s_{3,t}^-) $$
    Subject to:
    *   $x_{p,t} + s_{p,t}^- - s_{p,t}^+ = D_{p,t}$
    *   $2.0 x_{1,t} + 1.0 x_{2,t} + 3.1 x_{3,t} \le 5000$ (Note: For pure minimization of stockouts, if equipment is a hard constraint, we use the inequality directly. If it's a goal, we use the equality with deviations. Since Goal 2 is about *overloading*, the hard constraint is effectively the limit 5000. We can replace the equality with $\sum a_p x_{p,t} \le 5000$ for the first stage, as we don't care about underutilization yet, only ensuring we don't exceed it if possible, or if we must exceed it, that's Goal 2. Actually, standard goal programming keeps the equality. Let's stick to the equality form for consistency).
    *   $40 x_{1,t} + 20 x_{2,t} + 55 x_{3,t} \le 93000$ (Similarly, if capital is Goal 3, we might treat it as a hard constraint in the first pass to see if demand can be met within capital limits. If not, the excess is measured in Goal 3. To be safe and consistent with Goal Programming, we keep the deviation variables in the model but only optimize the specific priority terms).

    *Refined Approach for Implementation:*
    Since the problem asks to "formulate a mathematical model", the most robust formulation is the **Preemptive Goal Programming Model**.

    **Model:**
    $$
    \begin{aligned}
    &\text{Lexicographically Minimize } \quad \mathbf{Z} = [ Z_1, Z_2, Z_3 ] \\
    \text{Where:} \\
    Z_1 &= \sum_{t=1}^3 \left( 1 \cdot s_{1,t}^- + 1 \cdot s_{2,t}^- + 2 \cdot s_{3,t}^- \right) \\
    Z_2 &= \sum_{t=1}^3 e_t^+ \\
    Z_3 &= \sum_{t=1}^3 c_t^+
    \end{aligned}
    $$
    **Subject to:**
    1.  $x_{p,t} + s_{p,t}^- - s_{p,t}^+ = D_{p,t} \quad \forall p \in \{1,2,3\}, t \in \{1,2,3\}$
    2.  $2.0 x_{1,t} + 1.0 x_{2,t} + 3.1 x_{3,t} + e_t^- - e_t^+ = 5000 \quad \forall t \in \{1,2,3\}$
    3.  $40 x_{1,t} + 20 x_{2,t} + 55 x_{3,t} + c_t^- - c_t^+ = 93000 \quad \forall t \in \{1,2,3\}$
    4.  $x_{p,t}, s_{p,t}^-, s_{p,t}^+, e_t^-, e_t^+, c_t^-, c_t^+ \ge 0$

    **Parameter Values:**
    *   $D_{1,1}=500, D_{2,1}=750, D_{3,1}=900$
    *   $D_{1,2}=680, D_{2,2}=800, D_{3,2}=800$
    *   $D_{1,3}=800, D_{2,3}=950, D_{3,3}=1000$
    *   $H=5000$
    *   $W=93000$
    *   $a = [2.0, 1.0, 3.1]$
    *   $b = [40, 20, 55]$
    *   Weights for $Z_1$: $w_1=1, w_2=1, w_3=2$