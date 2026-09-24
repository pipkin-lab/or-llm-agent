Based on the problem description, this is a **Goal Programming** problem. The decision-maker has specified prioritized conditions:
1.  **Priority 1**: Strictly follow blending proportions.
2.  **Priority 2**: Maximize profit.
3.  **Priority 3**: Produce at least 2,000 kg of Red brand liquor.

Since the conditions are prioritized, we cannot simply maximize profit (Priority 2) while ignoring the strict adherence to blending ratios (Priority 1) in a standard LP. Instead, we must minimize the deviations from the Priority 1 goals first, then maximize profit within the set of solutions that satisfy Priority 1 (or minimize its deviation if infeasible, but here "strictly follow" implies equality constraints or zero deviation targets), and finally satisfy the Red brand minimum.

However, "Strictly follow its specified blending proportions" usually implies that these are hard constraints or the highest priority goals. Given the phrasing "prioritized conditions," a **Lexicographic Goal Programming** formulation is appropriate.

Let's refine the interpretation:
-   **Goal 1 (Priority $P_1$)**: The blend ratios for each brand must match the specified bounds. Wait, the table gives inequalities ("Grade III < 10%", "Grade I > 50%"). "Strictly follow" likely means satisfying these inequality constraints. If they are hard constraints, they are not "goals" in the sense of having deviations, but rather restrictions. However, in Goal Programming, if a condition is "must strictly follow," it is often treated as a goal with zero tolerance for deviation, or simply as a hard constraint. Let's look at the next conditions.
-   **Goal 2 (Priority $P_2$)**: Maximize Profit.
-   **Goal 3 (Priority $P_3$)**: Red production $\ge 2000$.

If Condition 1 is a hard constraint (blending ratios must be within the specified ranges), then the model is a **Multi-Objective / Lexicographic Optimization** problem.
1.  First, we must ensure the blending ratios are respected. Since these are inequalities, any solution satisfying them is "feasible" with respect to Priority 1.
2.  Second, among those, we maximize profit.
3.  Third, we want Red $\ge 2000$.

Actually, standard Goal Programming treats all targets as soft constraints with deviation variables.
Let's define the goals:
1.  **Blending Constraints**: These are typically hard constraints in blending problems because a product that doesn't meet the spec cannot be sold as that brand. The phrase "strictly follow" reinforces this. Let's treat the blending percentage requirements as **Hard Constraints**.
2.  **Profit Maximization**: This is the objective.
3.  **Red Production**: This is a target.

If Condition 1 is a hard constraint, the problem reduces to:
Maximize Profit
Subject to:
-   Supply constraints
-   Blending ratio constraints (Hard)
-   **Goal 3**: Red $\ge 2000$ (This is a priority, so it's a soft constraint in a GP model, or a hard constraint if we interpret "prioritized" as "satisfy P3 before P2"? No, P2 is Profit, P3 is Red. Usually, higher priority means more important. So P1 > P2 > P3.
    -   P1: Blending ratios.
    -   P2: Max Profit.
    -   P3: Red $\ge 2000$.

If we treat this as a **Lexicographic Goal Program**:
-   **Level 1**: Minimize deviation from blending specs? Or are they hard? If hard, the level is trivial (deviation=0). Let's assume they are hard constraints because "strictly follow" is strong language. If they were soft, it would say "aim for" or "try to keep".
-   **Level 2**: Maximize Profit.
-   **Level 3**: Minimize underachievement of Red production (i.e., $x_{Red} \ge 2000$).

However, a single objective function is required for standard solver output unless specified as a multi-objective solver. A common way to handle "prioritized" conditions in a single LP/MILP context for such textbook problems is often **Preemptive Goal Programming**.

Let's formulate it as a **Goal Programming** model with lexicographic weights $M_1 \gg M_2 \gg M_3$.

**Model Type**: LP (Linear Programming) with Goal Programming structure.

### 1. Index Sets & Parameters

**Sets:**
-   $G = \{1, 2, 3\}$: Set of base liquor grades (I, II, III).
-   $B = \{R, Y, Bl\}$: Set of branded liquors (Red, Yellow, Blue).

**Parameters (from Table 4-13):**
-   $S_g$: Daily supply of grade $g$ (kg).
    -   $S_1 = 1500$
    -   $S_2 = 2000$
    -   $S_3 = 1000$
-   $C_g$: Cost per kg of grade $g$ (Yuan).
    -   $C_1 = 6.0$
    -   $C_2 = 4.5$
    -   $C_3 = 3.0$

**Parameters (from Table 4-14):**
-   $P_b$: Selling price per kg of brand $b$ (Yuan).
    -   $P_R = 5.5$
    -   $P_Y = 5.0$
    -   $P_{Bl} = 4.8$

**Blending Requirements (Inequalities):**
-   **Red ($R$)**:
    -   Grade III < 10% $\Rightarrow \frac{x_{3,R}}{X_R} < 0.10$
    -   Grade I > 50% $\Rightarrow \frac{x_{1,R}}{X_R} > 0.50$
-   **Yellow ($Y$)**:
    -   Grade III < 70% $\Rightarrow \frac{x_{3,Y}}{X_Y} < 0.70$
    -   Grade I > 20% $\Rightarrow \frac{x_{1,Y}}{X_Y} > 0.20$
-   **Blue ($Bl$)**:
    -   Grade III < 50% $\Rightarrow \frac{x_{3,Bl}}{X_{Bl}} < 0.50$
    -   Grade I > 10% $\Rightarrow \frac{x_{1,Bl}}{X_{Bl}} > 0.10$

*Note: To convert these non-linear ratio constraints into linear constraints, we multiply by the total production of the brand. Let $X_b$ be the total kg of brand $b$ produced. Also note that $X_b = \sum_{g \in G} x_{g,b}$.*

**Goal Targets:**
-   Target for Red production: $T_R = 2000$ kg.

**Priority Weights:**
-   $M_1$: Weight for Priority 1 (Blending compliance). Since these are "strict", we treat them as hard constraints. If modeled as goals, the deviation should be 0.
-   $M_2$: Weight for Priority 2 (Profit).
-   $M_3$: Weight for Priority 3 (Red production minimum).
-   We assume $M_1 \gg M_2 \gg M_3$. In a standard LP formulation for a single solver pass, if P1 is hard, we just include the constraints. Then we maximize profit. But P3 is also a condition.
    -   Interpretation A: Lexicographic. Solve max profit s.t. blending constraints AND Red >= 2000. If infeasible, relax?
    -   Interpretation B: Weighted Goal Programming.
        -   Goal 1: Blending ratios met. (Hard constraints usually).
        -   Goal 2: Max Profit.
        -   Goal 3: Red >= 2000.
    
    If we treat Blending as Hard Constraints, the objective is to maximize Profit while trying to satisfy Red >= 2000. But Priority 2 (Profit) is higher than Priority 3 (Red Min). This means we maximize profit *first*, and *then* ensure Red >= 2000? No, that's not how lexicographic works.
    
    Lexicographic Order:
    1.  Minimize deviation from P1 goals.
    2.  Subject to P1 goals satisfied, Maximize P2 (Profit).
    3.  Subject to P1 and P2 optimized, Satisfy P3 (Red >= 2000).
    
    Wait, "Maximize Profit" is an objective, not a target to "satisfy". In Goal Programming, you usually have a target profit or maximize it as the final objective.
    
    Let's look at the structure again.
    1.  **P1**: Blending proportions. (Hard Constraints).
    2.  **P2**: Maximize Profit.
    3.  **P3**: Red >= 2000.
    
    If P2 is "Maximize Profit", it is the primary objective function.
    If P3 is "Red >= 2000" and it has *lower* priority than Profit, it means we should maximize profit, and *if* there is a trade-off, we favor Profit over the Red minimum. However, "At least 2000" is a constraint. If it's lower priority, it becomes a soft constraint.
    
    So the objective function is:
    **Minimize** $Z = M_1 d_{blend}^+ + M_2 (\text{negative profit deviation?}) + M_3 d_{Red}^-$
    
    Actually, maximizing profit is equivalent to minimizing the deviation from a "large" target profit, or simply including $-\text{Profit}$ in the minimization objective with a weight.
    
    Let's define the Goal Programming Formulation:
    
    **Goal 1 (Blending):**
    Since these are "strictly follow", we model them as **Hard Constraints**.
    $x_{3,R} \le 0.10 X_R$
    $x_{1,R} \ge 0.50 X_R$
    ... etc.
    
    **Goal 2 (Profit):**
    Maximize Profit. In a minimization GP framework, we minimize the "underachievement" of profit. Let $\pi$ be the profit. We want to maximize $\pi$. This is equivalent to minimizing $-\pi$ (or maximizing $\pi$).
    
    **Goal 3 (Red Production):**
    $X_R \ge 2000$.
    Deviation variables: $d_R^-$ (underachievement), $d_R^+$ (overachievement).
    We want to minimize $d_R^-$.
    
    **Priority Structure:**
    The problem states conditions are prioritized.
    P1: Blending (Hard).
    P2: Profit (Max).
    P3: Red Min (Soft, lower priority than Profit).
    
    This implies: We want the solution that maximizes Profit, among all solutions that satisfy Blending and Red >= 2000?
    NO. If P3 is lower priority than P2, it means Profit is more important than the Red minimum. So we maximize Profit. The Red minimum is a "nice to have" or a constraint that can be violated if it hurts Profit?
    Usually, "At least X" is a hard constraint unless specified as a goal. But here it is listed as a "prioritized condition".
    
    Let's assume the standard **Preemptive Goal Programming** approach:
    Objective: Min $Z = M_2 \cdot (\text{deviation from max profit}) + M_3 \cdot d_R^-$
    Subject to:
    -   Blending constraints (Hard, from P1)
    -   Supply constraints (Hard)
    -   Goal equation for Profit: $\text{Profit} + d_\pi^- - d_\pi^+ = \text{Target Profit}$? No, we don't have a target profit. We just want to maximize it.
    
    Alternative interpretation:
    The "Prioritized conditions" define the lexicographic order of the objectives.
    1.  Satisfy Blending (Hard).
    2.  Maximize Profit.
    3.  Satisfy Red >= 2000.
    
    If we use a weighted sum with big-M:
    $\text{Minimize } Z = M_2 (-\text{Profit}) + M_3 d_R^-$
    Where $M_2 \gg M_3$.
    
    Wait, if $M_2$ is huge, we minimize $-\text{Profit}$ (i.e., Maximize Profit) primarily. $d_R^-$ is only minimized if there are multiple solutions with the same maximum profit.
    
    Let's verify the "Profit" calculation.
    $\text{Profit} = \sum_{b \in B} P_b X_b - \sum_{g \in G} C_g (\sum_{b \in B} x_{g,b})$
    
    Let's refine the variables.
    $x_{g,b}$: kg of Grade $g$ used in Brand $b$.
    $X_b = \sum_{g} x_{g,b}$.
    
    **Constraints:**
    1.  **Supply**:
        $\sum_{b \in B} x_{g,b} \le S_g, \forall g \in G$.
    2.  **Blending (Hard, P1)**:
        Red:
        $x_{3,R} \le 0.10 (x_{1,R} + x_{2,R} + x_{3,R}) \Rightarrow 0.90 x_{3,R} - 0.10 x_{1,R} - 0.10 x_{2,R} \le 0$
        $x_{1,R} \ge 0.50 (x_{1,R} + x_{2,R} + x_{3,R}) \Rightarrow 0.50 x_{1,R} - 0.50 x_{2,R} - 0.50 x_{3,R} \ge 0$
        
        Yellow:
        $x_{3,Y} \le 0.70 X_Y \Rightarrow 0.30 x_{3,Y} - 0.70 x_{1,Y} - 0.70 x_{2,Y} \le 0$
        $x_{1,Y} \ge 0.20 X_Y \Rightarrow 0.80 x_{1,Y} - 0.20 x_{2,Y} - 0.20 x_{3,Y} \ge 0$
        
        Blue:
        $x_{3,Bl} \le 0.50 X_{Bl} \Rightarrow 0.50 x_{3,Bl} - 0.50 x_{1,Bl} - 0.50 x_{2,Bl} \le 0$
        $x_{1,Bl} \ge 0.10 X_{Bl} \Rightarrow 0.90 x_{1,Bl} - 0.10 x_{2,Bl} - 0.10 x_{3,Bl} \ge 0$
        
    3.  **Red Production Goal (P3)**:
        $X_R + d_R^- - d_R^+ = 2000$
        We want to minimize $d_R^-$ (underproduction).
        
    4.  **Profit Maximization (P2)**:
        We want to maximize $\Pi = \sum P_b X_b - \sum C_g \sum x_{g,b}$.
        In the objective function (Minimization), we include $-M_2 \Pi$.
        
    **Objective Function:**
    $\text{Minimize } Z = -M_2 \Pi + M_3 d_R^-$
    With $M_2 \gg M_3$.
    
    Note: Since $\Pi$ can be large, and we are minimizing $-M_2 \Pi$, this effectively maximizes $\Pi$.
    
    Is there any deviation variable for Profit? No, because we are maximizing it directly in the objective.
    
    **Variables:**
    $x_{g,b} \ge 0$ for all $g, b$.
    $d_R^-, d_R^+ \ge 0$.
    
    **Parameters:**
    $M_2$ and $M_3$ are large constants. $M_2$ should be large enough to dominate the profit term relative to the deviation term if we were summing deviations, but here we are mixing a continuous profit variable with a deviation variable.
    Actually, to make the weights work, we can normalize or just pick $M_2$ large.
    However, a cleaner formulation for "Prioritized" where P2 is Max Profit and P3 is Min Underproduction is:
    
    $\text{Minimize } Z = M \cdot d_R^- - \Pi$
    Where $M$ is a sufficiently large number such that the minimization of $d_R^-$ is secondary to the maximization of $\Pi$?
    NO. Priority 2 is Profit. Priority 3 is Red.
    This means Profit is **more** important than Red.
    So we maximize Profit.
    If there are ties in Profit, we minimize $d_R^-$.
    
    So the objective is:
    $\text{Maximize } \Pi$
    Subject to:
    ...
    And if we want to enforce the priority in a single pass:
    $\text{Minimize } Z = M \cdot d_R^- - \Pi$
    Here, $- \Pi$ is the dominant term (since we want to make it as small/negative as possible, i.e., $\Pi$ large). $M \cdot d_R^-$ is the secondary term.
    For this to work, $M$ must be small enough not to disrupt the primary objective?
    No. In lexicographic optimization:
    1. Max $\Pi$. Let $\Pi^*$ be the optimal value.
    2. Min $d_R^-$ subject to $\Pi = \Pi^*$.
    
    A single-objective approximation is:
    $\text{Minimize } Z = -\Pi + \epsilon d_R^-$
    Where $\epsilon$ is very small.
    
    Let's check the units.
    Profit is in Yuan.
    $d_R^-$ is in kg.
    We need to scale them.
    Max possible profit:
    Max price ~ 5.5. Max supply ~ 4500 kg. Max Profit ~ 24,750 Yuan.
    Max deviation $d_R^-$ ~ 2000 kg.
    If we use $Z = -\Pi + \epsilon d_R^-$, $\epsilon$ should be small, e.g., $10^{-4}$.
    
    However, often in these textbook problems, "Prioritized" implies a Goal Programming model with deviation variables for **all** goals.
    
    Let's stick to the most robust interpretation: **Lexicographic Goal Programming**.
    
    **Objective Function (Weighted Sum with Big M):**
    $\text{Minimize } Z = M_1 (\text{Blending Deviations}) + M_2 (-\Pi) + M_3 d_R^-$
    
    If Blending is "Strict", deviations are 0. So $M_1$ term is 0.
    So $\text{Minimize } Z = M_2 (-\Pi) + M_3 d_R^-$
    With $M_2 \gg M_3$.
    
    Let's define the values.
    $M_2 = 1000$ (Arbitrary large number relative to scale).
    $M_3 = 1$.
    
    Wait, if $M_2$ is large, $M_2 (-\Pi)$ dominates. We minimize $-\Pi \rightarrow$ Maximize $\Pi$.
    Then $d_R^-$ is minimized.
    
    This fits the priority: Profit (P2) is higher than Red Min (P3).
    
    **Final Model Structure:**
    
    **Model Type**: LP
    
    **Index Sets**:
    -   $G = \{1, 2, 3\}$ (Grades I, II, III)
    -   $B = \{R, Y, Bl\}$ (Brands Red, Yellow, Blue)
    
    **Parameters**:
    -   $S = [1500, 2000, 1000]$ (Supply)
    -   $C = [6.0, 4.5, 3.0]$ (Cost)
    -   $P = [5.5, 5.0, 4.8]$ (Price)
    -   $Target_R = 2000$
    -   $M = 1000$ (Big-M weight for Profit priority)
    
    **Decision Variables**:
    -   $x_{g,b} \ge 0$: Amount of Grade $g$ in Brand $b$.
    -   $d_R^- \ge 0$: Underachievement of Red production target.
    -   $d_R^+ \ge 0$: Overachievement of Red production target (usually not penalized, but defined for equality).
    
    **Objective Function**:
    $$ \text{Minimize } Z = -1000 \times \left( \sum_{b \in B} P_b \sum_{g \in G} x_{g,b} - \sum_{g \in G} C_g \sum_{b \in B} x_{g,b} \right) + 1 \times d_R^- $$
    
    *Note: The coefficient -1000 ensures that maximizing profit is the primary goal. The coefficient 1 on $d_R^-$ ensures that, among solutions with the same profit, we minimize the shortfall in Red production.*
    
    **Constraints**:
    
    1.  **Supply Constraints**:
        $$ \sum_{b \in B} x_{g,b} \le S_g, \quad \forall g \in G $$
        -   $x_{1,R} + x_{1,Y} + x_{1,Bl} \le 1500$
        -   $x_{2,R} + x_{2,Y} + x_{2,Bl} \le 2000$
        -   $x_{3,R} + x_{3,Y} + x_{3,Bl} \le 1000$
        
    2.  **Blending Constraints (Hard, Priority 1)**:
        
        **Red**:
        -   Grade III < 10%: $x_{3,R} \le 0.10 (x_{1,R} + x_{2,R} + x_{3,R})$
            $\Rightarrow 0.90 x_{3,R} - 0.10 x_{1,R} - 0.10 x_{2,R} \le 0$
        -   Grade I > 50%: $x_{1,R} \ge 0.50 (x_{1,R} + x_{2,R} + x_{3,R})$
            $\Rightarrow 0.50 x_{1,R} - 0.50 x_{2,R} - 0.50 x_{3,R} \ge 0$
            
        **Yellow**:
        -   Grade III < 70%: $x_{3,Y} \le 0.70 (x_{1,Y} + x_{2,Y} + x_{3,Y})$
            $\Rightarrow 0.30 x_{3,Y} - 0.70 x_{1,Y} - 0.70 x_{2,Y} \le 0$
        -   Grade I > 20%: $x_{1,Y} \ge 0.20 (x_{1,Y} + x_{2,Y} + x_{3,Y})$
            $\Rightarrow 0.80 x_{1,Y} - 0.20 x_{2,Y} - 0.20 x_{3,Y} \ge 0$
            
        **Blue**:
        -   Grade III < 50%: $x_{3,Bl} \le 0.50 (x_{1,Bl} + x_{2,Bl} + x_{3,Bl})$
            $\Rightarrow 0.50 x_{3,Bl} - 0.50 x_{1,Bl} - 0.50 x_{2,Bl} \le 0$
        -   Grade I > 10%: $x_{1,Bl} \ge 0.10 (x_{1,Bl} + x_{2,Bl} + x_{3,Bl})$
            $\Rightarrow 0.90 x_{1,Bl} - 0.10 x_{2,Bl} - 0.10 x_{3,Bl} \ge 0$
            
    3.  **Red Production Goal (Priority 3)**:
        $$ (x_{1,R} + x_{2,R} + x_{3,R}) + d_R^- - d_R^+ = 2000 $$
        
    4.  **Non-negativity**:
        $$ x_{g,b} \ge 0, \quad d_R^- \ge 0, \quad d_R^+ \ge 0 $$

    **Feasibility Check**:
    Can we produce 2000 kg of Red?
    Red needs >50% Grade I. So need >1000 kg Grade I.
    Total Grade I supply is 1500 kg.
    Remaining 500 kg Grade I for Yellow and Blue.
    Yellow needs >20% Grade I.
    Blue needs >10% Grade I.
    
    Red needs <10% Grade III.
    Total Grade III is 1000 kg.
    
    It seems feasible.
    
    **Magnitude Check for Objective**:
    Profit per kg approx:
    Red: 5.5 - (mix cost). Mix cost approx 4-5. Profit ~ 0.5-1.5.
    Total Profit ~ 2000*1 + 2000*1 + 500*1 ~ 4500 Yuan.
    Objective: $-1000 * 4500 + 0 = -4,500,000$.
    
    This looks correct.

### Final Formulation

**Model Type**: LP (Linear Programming)

**Index Sets & Parameters**
-   $G = \{1, 2, 3\}$: Base liquor grades (I, II, III).
-   $B = \{R, Y, Bl\}$: Branded liquors (Red, Yellow, Blue).
-   $S = [1500, 2000, 1000]$: Daily supply (kg) for grades 1, 2, 3.
-   $C = [6.0, 4.5, 3.0]$: Cost (Yuan/kg) for grades 1, 2, 3.
-   $P = [5.5, 5.0, 4.8]$: Selling price (Yuan/kg) for brands R, Y, Bl.
-   $T_R = 2000$: Target production for Red brand (kg).
-   $W = 1000$: Weight for profit maximization (Big-M to ensure priority over Red deviation).

**Decision Variables**
-   $x_{g,b} \ge 0$: Quantity (kg) of base liquor grade $g$ blended into brand $b$.
-   $d_R^- \ge 0$: Underachievement deviation for Red brand production (kg).
-   $d_R^+ \ge 0$: Overachievement deviation for Red brand production (kg).

**Objective Function**
Minimize the weighted sum of negative profit (to maximize profit, Priority 2) and underachievement of Red production (Priority 3).
$$ \text{Minimize } Z = -W \left( \sum_{b \in B} P_b \sum_{g \in G} x_{g,b} - \sum_{g \in G} C_g \sum_{b \in B} x_{g,b} \right) + d_R^- $$

**Operational Constraints**

1.  **Supply Constraints**:
    $$ \sum_{b \in B} x_{g,b} \le S_g, \quad \forall g \in G $$
    -   $x_{1,R} + x_{1,Y} + x_{1,Bl} \le 1500$
    -   $x_{2,R} + x_{2,Y} + x_{2,Bl} \le 2000$
    -   $x_{3,R} + x_{3,Y} + x_{3,Bl} \le 1000$

2.  **Blending Requirements (Hard Constraints, Priority 1)**:
    
    *Red Brand ($R$):*
    -   Grade III < 10%: $0.90 x_{3,R} - 0.10 x_{1,R} - 0.10 x_{2,R} \le 0$
    -   Grade I > 50%: $0.50 x_{1,R} - 0.50 x_{2,R} - 0.50 x_{3,R} \ge 0$
    
    *Yellow Brand ($Y$):*
    -   Grade III < 70%: $0.30 x_{3,Y} - 0.70 x_{1,Y} - 0.70 x_{2,Y} \le 0$
    -   Grade I > 20%: $0.80 x_{1,Y} - 0.20 x_{2,Y} - 0.20 x_{3,Y} \ge 0$
    
    *Blue Brand ($Bl$):*
    -   Grade III < 50%: $0.50 x_{3,Bl} - 0.50 x_{1,Bl} - 0.50 x_{2,Bl} \le 0$
    -   Grade I > 10%: $0.90 x_{1,Bl} - 0.10 x_{2,Bl} - 0.10 x_{3,Bl} \ge 0$

3.  **Red Production Goal (Priority 3)**:
    $$ (x_{1,R} + x_{2,R} + x_{3,R}) + d_R^- - d_R^+ = 2000 $$