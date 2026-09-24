**Model Type:** MILP (Multi-Objective Lexicographic Optimization, solved sequentially as a series of MILPs)

**Problem Analysis & Strategy:**
The problem requires satisfying three prioritized goals. Since these are prioritized (lexicographic), we solve them in sequence:
1.  **Level 1:** Minimize weighted stockouts. This determines the "minimum acceptable" stockout level, denoted as $Z_1^*$.
2.  **Level 2:** Minimize equipment overloading, subject to stockouts not exceeding $Z_1^*$. This determines the "minimum acceptable" overload level, denoted as $Z_2^*$.
3.  **Level 3:** Ensure working capital usage does not exceed the limit. This is a hard constraint in the final model, or the third priority level if capital *could* be exceeded (but the prompt says "Ensure... does not exceed", implying a hard constraint or a very high priority goal. Given the phrasing "prioritized objectives" and "ensure", it is safest to treat Capital as a hard constraint in all models, or as the 3rd priority if the problem implies capital *can* be exceeded but is less important than the other two. However, "Ensure that working capital usage does not exceed the limit" usually implies a hard constraint in standard OR problems unless "minimize capital violation" is specified. Let's look at the data.
    *   Max demand per stage: P1(800), P2(950), P3(1000).
    *   Max capital usage if meeting all demand:
        *   Stage 1: $500(40) + 750(20) + 900(55) = 20000 + 15000 + 49500 = 84500 \le 93000$.
        *   Stage 2: $680(40) + 800(20) + 800(55) = 27200 + 16000 + 44000 = 87200 \le 93000$.
        *   Stage 3: $800(40) + 950(20) + 1000(55) = 32000 + 19000 + 55000 = 106000 > 93000$.
    *   Since Stage 3 demand exceeds capital limits, we *cannot* meet all demand within capital limits. Therefore, "Ensure working capital usage does not exceed the limit" is a **hard constraint**. The stockouts in Level 1 will be driven by both equipment and capital constraints. The "overloading" in Level 2 refers to exceeding the 5000 hours limit.

    **Revised Strategy:**
    1.  **Model 1 (Priority 1):** Minimize weighted stockouts.
        *   Variables: Production $x_{i,t}$, Stockout $s_{i,t}$.
        *   Constraints: Inventory balance, Equipment Hours $\le$ 5000 (Hard constraint? No, Priority 2 is minimizing overloading. This implies equipment *can* be overloaded, i.e., hours $> 5000$. If equipment couldn't be overloaded, it would be a hard constraint. The fact that "Minimize overloading" is a priority suggests the 5000h is a soft limit or a target that can be violated. Similarly, Capital is "Ensure... does not exceed", which sounds like a hard constraint. Let's assume:
            *   **Capital:** Hard Constraint ($\le 93000$).
            *   **Equipment:** Soft Constraint (Overloading is penalized in Priority 2).
            *   **Demand:** Soft Constraint (Stockouts are penalized in Priority 1).
    
    Let's refine the variable definitions.
    *   $x_{i,t}$: Quantity of product $i$ produced in stage $t$. (Integer, $\ge 0$)
    *   $I_{i,t}$: Inventory of product $i$ at end of stage $t$. (Integer, $\ge 0$)
    *   $S_{i,t}$: Stockout (unmet demand) of product $i$ in stage $t$. (Integer, $\ge 0$)
    *   $O_t$: Overloading of equipment in stage $t$ (hours over 5000). (Continuous/Integer, $\ge 0$)

    **Priority 1 Objective:** Minimize $Z_1 = \sum_{t=1}^3 \sum_{i=1}^3 w_i S_{i,t}$.
    Weights: $w_1=1, w_2=1, w_3=2$.

    **Priority 2 Objective:** Minimize $Z_2 = \sum_{t=1}^3 O_t$.
    Constraint from Priority 1: $Z_1 \le Z_1^*$.

    **Priority 3 Constraint:** Capital usage $\le 93000$ at each stage.

    **Inventory Balance:**
    $I_{i,t-1} + x_{i,t} - S_{i,t} = D_{i,t} + I_{i,t}$?
    Standard form: $I_{i,t} = I_{i,t-1} + x_{i,t} - D_{i,t}$.
    If $I_{i,t} < 0$, it becomes backorder/stockout.
    Let's define $S_{i,t}$ as the amount of demand in period $t$ that is NOT met by production $x_{i,t}$ and available inventory $I_{i,t-1}$.
    Equation: $x_{i,t} + I_{i,t-1} + S_{i,t} = D_{i,t} + I_{i,t}$.
    With $I_{i,0}=0$ and $I_{i,3}=0$ (final inventory zero).
    Note: If stockouts are backorders, they carry over. If they are lost sales, they don't. "Timely delivery to meet demand, minimizing stockouts" usually implies backorders in multi-period problems unless "lost sales" is specified. However, "initial and final inventories are zero" suggests a flow. Let's assume standard backorder logic where unmet demand in $t$ is satisfied in $t+1$ if possible, OR $S_{i,t}$ is simply the shortfall in period $t$ that is permanently lost or just a deviation.
    Given "minimizing stockouts" as a priority, and typically in such textbook problems, stockout variables $S_{i,t}$ represent the portion of demand $D_{i,t}$ not covered by $x_{i,t} + I_{i,t-1}$.
    Constraint: $x_{i,t} + I_{i,t-1} + S_{i,t} = D_{i,t} + I_{i,t}$.
    This allows $S_{i,t} > 0$ if supply < demand.

    **Equipment Constraint (Soft):**
    Total hours in stage $t$: $H_t = 2.0 x_{1,t} + 1.0 x_{2,t} + 3.1 x_{3,t}$.
    Overload $O_t = \max(0, H_t - 5000)$.
    Linearization:
    $H_t - 5000 \le O_t$
    $O_t \ge 0$
    (Minimization of $O_t$ will drive it to 0 if $H_t \le 5000$).

    **Capital Constraint (Hard):**
    $40 x_{1,t} + 20 x_{2,t} + 55 x_{3,t} \le 93000$ for $t=1,2,3$.

    **Final Model Formulation:**
    We will present the lexicographic optimization model.

### Index Sets & Parameters

**Sets:**
*   $I = \{1, 2, 3\}$: Set of products.
*   $T = \{1, 2, 3\}$: Set of planning stages (periods).

**Parameters:**
*   $D_{i,t}$: Demand for product $i$ in stage $t$ (units).
    *   $D_{1,1}=500, D_{1,2}=680, D_{1,3}=800$
    *   $D_{2,1}=750, D_{2,2}=800, D_{2,3}=950$
    *   $D_{3,1}=900, D_{3,2}=800, D_{3,3}=1000$
*   $a_{i}$: Equipment hours required per unit of product $i$ (hours/unit).
    *   $a_1=2.0, a_2=1.0, a_3=3.1$
*   $b_{i}$: Working capital required per unit of product $i$ (yuan/unit).
    *   $b_1=40, b_2=20, b_3=55$
*   $K_{eq}$: Equipment capacity limit per stage (hours).
    *   $K_{eq} = 5000$
*   $K_{cap}$: Working capital limit per stage (yuan).
    *   $K_{cap} = 93000$
*   $w_i$: Weight for stockout penalty of product $i$.
    *   $w_1=1, w_2=1, w_3=2$

### Decision Variables

*   $x_{i,t} \in \mathbb{Z}_{\ge 0}$: Quantity of product $i$ produced in stage $t$.
*   $I_{i,t} \in \mathbb{Z}_{\ge 0}$: Inventory of product $i$ at the end of stage $t$.
*   $S_{i,t} \in \mathbb{Z}_{\ge 0}$: Stockout (unmet demand) of product $i$ in stage $t$.
*   $O_t \in \mathbb{R}_{\ge 0}$: Amount of equipment overload (hours) in stage $t$.

### Objective Function

This is a **Lexicographic Multi-Objective** problem. We solve in three sequential steps.

**Step 1: Minimize Weighted Stockouts**
$$ \text{Minimize } Z_1 = \sum_{t \in T} \sum_{i \in I} w_i S_{i,t} $$
$$ Z_1 = 1 S_{1,1} + 1 S_{2,1} + 2 S_{3,1} + 1 S_{1,2} + 1 S_{2,2} + 2 S_{3,2} + 1 S_{1,3} + 1 S_{2,3} + 2 S_{3,3} $$

**Step 2: Minimize Equipment Overloading**
$$ \text{Minimize } Z_2 = \sum_{t \in T} O_t = O_1 + O_2 + O_3 $$
Subject to the constraint that the objective value of Step 1 is fixed at its optimal value $Z_1^*$:
$$ \sum_{t \in T} \sum_{i \in I} w_i S_{i,t} = Z_1^* $$

**Step 3: Ensure Capital Constraint**
The third priority is "Ensure that working capital usage does not exceed the limit." This is modeled as a hard constraint in the final feasible region. If the problem implies that capital *could* be exceeded in lower priorities but must be respected in the final solution, it is a hard constraint. If it were a soft constraint to be minimized, the objective would be different. Given the phrasing "Ensure...", it is a hard constraint.

### Operational Constraints

**1. Inventory Balance Constraints**
For each product $i \in I$ and stage $t \in T$:
$$ x_{i,t} + I_{i,t-1} + S_{i,t} = D_{i,t} + I_{i,t} $$
*Note: $I_{i,0} = 0$ for all $i$.*
*Note: $I_{i,3} = 0$ for all $i$ (Final inventory is zero).*

**2. Equipment Capacity Constraints (Soft)**
For each stage $t \in T$:
$$ 2.0 x_{1,t} + 1.0 x_{2,t} + 3.1 x_{3,t} - 5000 \le O_t $$
$$ O_t \ge 0 $$

**3. Working Capital Constraints (Hard)**
For each stage $t \in T$:
$$ 40 x_{1,t} + 20 x_{2,t} + 55 x_{3,t} \le 93000 $$

**4. Non-negativity and Integrality**
$$ x_{i,t} \in \mathbb{Z}_{\ge 0} \quad \forall i \in I, t \in T $$
$$ I_{i,t} \in \mathbb{Z}_{\ge 0} \quad \forall i \in I, t \in T $$
$$ S_{i,t} \in \mathbb{Z}_{\ge 0} \quad \forall i \in I, t \in T $$
$$ O_t \in \mathbb{R}_{\ge 0} \quad \forall t \in T $$