# Cargo Loading Optimization Model

## 1. Index Sets & Parameters

**Index Sets:**
*   $I = \{A, B, C\}$: Set of cargo types.
*   $J = \{F, M, R\}$: Set of compartments (Front, Middle, Rear).

**Parameters (from Tables 1-24 and 1-25):**

*   $CapW_j$: Maximum allowable load (weight) for compartment $j$ (tons).
    *   $CapW_F = 2000$, $CapW_M = 3000$, $CapW_R = 1500$.
*   $CapV_j$: Maximum volume for compartment $j$ ($m^3$).
    *   $CapV_F = 4000$, $CapV_M = 5000$, $CapV_R = 1500$.
*   $Q_i$: Total available quantity of cargo type $i$ (pieces).
    *   $Q_A = 600$, $Q_B = 1000$, $Q_C = 800$.
*   $v_i$: Volume per piece of cargo type $i$ ($m^3$/piece).
    *   $v_A = 10$, $v_B = 5$, $v_C = 7$.
*   $w_i$: Weight per piece of cargo type $i$ (tons/piece).
    *   $w_A = 8$, $w_B = 6$, $w_C = 4$.
*   $p_i$: Freight rate (revenue) per piece of cargo type $i$ (dollars/piece).
    *   $p_A = 1000$, $p_B = 700$, $p_C = 600$.

**Derived Balance Parameters:**
*   Target weight ratio Front/Middle: $R_{FM} = CapW_F / CapW_M = 2000 / 3000 = 2/3$.
*   Target weight ratio Rear/Middle: $R_{RM} = CapW_R / CapW_M = 1500 / 3000 = 1/2$.
*   Target weight ratio Front/Rear: $R_{FR} = CapW_F / CapW_R = 2000 / 1500 = 4/3$.
*   Deviation tolerance $\epsilon_{FM} = 0.15$, $\epsilon_{RM} = 0.15$, $\epsilon_{FR} = 0.10$.

## 2. Decision Variables

Let $x_{ij}$ be the number of pieces of cargo type $i$ loaded in compartment $j$.

*   $x_{ij} \in \mathbb{Z}_{\ge 0}$ for all $i \in I, j \in J$.
    *(Note: Since cargo is counted in "pieces", integer variables are appropriate. However, given the large quantities, this is often treated as an LP relaxation in practice, but strictly "pieces" implies integrality. Given the prompt asks for an LP model formulation, we will define them as continuous variables $x_{ij} \ge 0$ but note that they represent counts. Standard LP formulations for this classic problem usually assume divisibility or large enough quantities that integrality is not binding, or it is solved as an ILP. I will specify **Integer** variables to be physically correct, but note that if a strict LP is required, the domain is Continuous. Given "pieces", **Integer** is the rigorous choice.)*

    **Domain Correction:** The problem asks to "formulate the linear programming model". In many textbook contexts for this specific cargo problem, if the numbers are large, it is often solved as an LP. However, "pieces" are discrete. I will define them as **Non-negative Integers** to be safe, but if the solver requires a pure LP, they are Continuous. Let's stick to **Non-negative Real Numbers** (Continuous) as is standard for "Linear Programming" unless "Integer Programming" is explicitly requested, but I will add a note. Actually, looking at standard OR practice for "how many pieces", it is an ILP. But the prompt says "formulate the linear programming model". I will use **Continuous** variables $x_{ij} \ge 0$ as the standard interpretation of "LP model", but acknowledge they represent counts.

    *Refined Decision:* I will define $x_{ij}$ as **Continuous** variables ($x_{ij} \ge 0$) because the prompt explicitly asks for a **Linear Programming** model. If integer constraints were required, it would typically ask for an Integer Linear Programming model.

## 3. Objective Function

Maximize total revenue:

$$
\text{Maximize } Z = \sum_{i \in I} \sum_{j \in J} p_i x_{ij}
$$

Expanded:
$$
Z = 1000(x_{AF} + x_{AM} + x_{AR}) + 700(x_{BF} + x_{BM} + x_{BR}) + 600(x_{CF} + x_{CM} + x_{CR})
$$

## 4. Operational Constraints

### A. Volume Constraints
The total volume of cargo loaded in each compartment must not exceed the compartment's volume capacity.

For each compartment $j \in J$:
$$
\sum_{i \in I} v_i x_{ij} \le CapV_j
$$

Specifically:
1.  **Front:** $10 x_{AF} + 5 x_{BF} + 7 x_{CF} \le 4000$
2.  **Middle:** $10 x_{AM} + 5 x_{BM} + 7 x_{CM} \le 5000$
3.  **Rear:** $10 x_{AR} + 5 x_{BR} + 7 x_{CR} \le 1500$

### B. Weight Constraints
The total weight of cargo loaded in each compartment must not exceed the compartment's maximum allowable load.

For each compartment $j \in J$:
$$
\sum_{i \in I} w_i x_{ij} \le CapW_j
$$

Specifically:
1.  **Front:** $8 x_{AF} + 6 x_{BF} + 4 x_{CF} \le 2000$
2.  **Middle:** $8 x_{AM} + 6 x_{BM} + 4 x_{CM} \le 3000$
3.  **Rear:** $8 x_{AR} + 6 x_{BR} + 4 x_{CR} \le 1500$

### C. Supply Constraints
The total quantity of each cargo type loaded across all compartments cannot exceed the available quantity.

For each cargo type $i \in I$:
$$
\sum_{j \in J} x_{ij} \le Q_i
$$

Specifically:
1.  **Cargo A:** $x_{AF} + x_{AM} + x_{AR} \le 600$
2.  **Cargo B:** $x_{BF} + x_{BM} + x_{BR} \le 1000$
3.  **Cargo C:** $x_{CF} + x_{CM} + x_{CR} \le 800$

### D. Balance Constraints (Linearized)
Let $W_F, W_M, W_R$ be the total weights in Front, Middle, and Rear compartments.
$W_F = 8 x_{AF} + 6 x_{BF} + 4 x_{CF}$
$W_M = 8 x_{AM} + 6 x_{BM} + 4 x_{CM}$
$W_R = 8 x_{AR} + 6 x_{BR} + 4 x_{CR}$

The problem states:
1.  $W_F / W_M$ must not deviate by more than 15% from $R_{FM} = 2/3$.
    $$ 0.85 \left(\frac{2}{3}\right) W_M \le W_F \le 1.15 \left(\frac{2}{3}\right) W_M $$
    $$ \frac{17}{45} W_M \le W_F \le \frac{23}{45} W_M $$
    (Note: $0.85 \times 2/3 = 1.7/6 = 17/60$? No. $0.85 * (2/3) = 1.7/6 = 17/60$. Wait. $2/3 \approx 0.666$. $0.85 * 0.666 = 0.566$. $17/30 = 0.566$. Let's use decimals for clarity in the linear form or exact fractions.
    $0.85 \times \frac{2}{3} = \frac{17}{60}$.
    $1.15 \times \frac{2}{3} = \frac{23}{60}$.
    
    So:
    $$ \frac{17}{60} W_M \le W_F \implies 60 W_F - 17 W_M \ge 0 $$
    $$ W_F \le \frac{23}{60} W_M \implies 60 W_F - 23 W_M \le 0 $$

2.  $W_R / W_M$ must not deviate by more than 15% from $R_{RM} = 1/2$.
    $$ 0.85 \left(\frac{1}{2}\right) W_M \le W_R \le 1.15 \left(\frac{1}{2}\right) W_M $$
    $$ \frac{17}{40} W_M \le W_R \le \frac{23}{40} W_M $$
    (Note: $0.85/2 = 0.425 = 17/40$. $1.15/2 = 0.575 = 23/40$.)
    
    So:
    $$ W_R \ge \frac{17}{40} W_M \implies 40 W_R - 17 W_M \ge 0 $$
    $$ W_R \le \frac{23}{40} W_M \implies 40 W_R - 23 W_M \le 0 $$

3.  $W_F / W_R$ must not deviate by more than 10% from $R_{FR} = 4/3$.
    $$ 0.90 \left(\frac{4}{3}\right) W_R \le W_F \le 1.10 \left(\frac{4}{3}\right) W_R $$
    $$ \frac{36}{30} W_R \le W_F \le \frac{44}{30} W_R $$
    Simplifying fractions: $36/30 = 6/5 = 1.2$. $44/30 = 22/15 \approx 1.466$.
    
    So:
    $$ W_F \ge \frac{6}{5} W_R \implies 5 W_F - 6 W_R \ge 0 $$
    $$ W_F \le \frac{22}{15} W_R \implies 15 W_F - 22 W_R \le 0 $$

Substituting the linear expressions for $W_F, W_M, W_R$ into these inequalities yields the final linear balance constraints.

**Summary of Balance Constraints (Expanded):**

1.  **Front >= 15% Low of Ratio to Middle:**
    $$ 60(8 x_{AF} + 6 x_{BF} + 4 x_{CF}) - 17(8 x_{AM} + 6 x_{BM} + 4 x_{CM}) \ge 0 $$
    $$ 480 x_{AF} + 360 x_{BF} + 240 x_{CF} - 136 x_{AM} - 102 x_{BM} - 68 x_{CM} \ge 0 $$

2.  **Front <= 15% High of Ratio to Middle:**
    $$ 60(8 x_{AF} + 6 x_{BF} + 4 x_{CF}) - 23(8 x_{AM} + 6 x_{BM} + 4 x_{CM}) \le 0 $$
    $$ 480 x_{AF} + 360 x_{BF} + 240 x_{CF} - 184 x_{AM} - 138 x_{BM} - 92 x_{CM} \le 0 $$

3.  **Rear >= 15% Low of Ratio to Middle:**
    $$ 40(8 x_{AR} + 6 x_{BR} + 4 x_{CR}) - 17(8 x_{AM} + 6 x_{BM} + 4 x_{CM}) \ge 0 $$
    $$ 320 x_{AR} + 240 x_{BR} + 160 x_{CR} - 136 x_{AM} - 102 x_{BM} - 68 x_{CM} \ge 0 $$

4.  **Rear <= 15% High of Ratio to Middle:**
    $$ 40(8 x_{AR} + 6 x_{BR} + 4 x_{CR}) - 23(8 x_{AM} + 6 x_{BM} + 4 x_{CM}) \le 0 $$
    $$ 320 x_{AR} + 240 x_{BR} + 160 x_{CR} - 184 x_{AM} - 138 x_{BM} - 92 x_{CM} \le 0 $$

5.  **Front >= 10% Low of Ratio to Rear:**
    $$ 5(8 x_{AF} + 6 x_{BF} + 4 x_{CF}) - 6(8 x_{AR} + 6 x_{BR} + 4 x_{CR}) \ge 0 $$
    $$ 40 x_{AF} + 30 x_{BF} + 20 x_{CF} - 48 x_{AR} - 36 x_{BR} - 24 x_{CR} \ge 0 $$

6.  **Front <= 10% High of Ratio to Rear:**
    $$ 15(8 x_{AF} + 6 x_{BF} + 4 x_{CF}) - 22(8 x_{AR} + 6 x_{BR} + 4 x_{CR}) \le 0 $$
    $$ 120 x_{AF} + 90 x_{BF} + 60 x_{CF} - 176 x_{AR} - 132 x_{BR} - 88 x_{CR} \le 0 $$

### E. Non-negativity
$$ x_{ij} \ge 0 \quad \forall i \in I, j \in J $$

*(Note: If integer solutions are strictly required, add $x_{ij} \in \mathbb{Z}$).*