**Model Type:** LP (Linear Programming)

### 1. Index Sets & Parameters

**Sets:**
*   $P = \{A, B, C, D\}$: Set of chemical plants.
*   $R = \{I, II, III, IV, V, VI\}$: Set of sales regions.

**Parameters (converted to consistent units: Tons, Yuan):**

*   **Plant Capacities ($S_i$ in tons):**
    *   $S_A = 200$
    *   $S_B = 300$
    *   $S_C = 400$
    *   $S_D = 100$
    *   Total Supply = $1000$ tons.

*   **Region Demands ($D_j$ in tons):**
    *   $D_I = 200$
    *   $D_{II} = 150$
    *   $D_{III} = 400$
    *   $D_{IV} = 100$
    *   $D_V = 150$
    *   $D_{VI} = 150$
    *   Total Demand = $1150$ tons.
    *   *Note: Total Supply (1000) < Total Demand (1150). Therefore, not all demand can be met. The supply side is the binding constraint.*

*   **Unit Production Costs ($c_i$ in yuan/kg):**
    *   $c_A = 1.2$
    *   $c_B = 1.4$
    *   $c_C = 1.1$
    *   $c_D = 1.5$

*   **Unit Sales Prices ($p_j$ in yuan/kg):**
    *   $p_I = 2.0$
    *   $p_{II} = 2.4$
    *   $p_{III} = 1.8$
    *   $p_{IV} = 2.2$
    *   $p_V = 1.6$
    *   $p_{VI} = 2.0$

*   **Unit Transportation Costs ($t_{ij}$ in yuan/kg):**
    *   From Table 3-18:
        *   $t_{A,I}=0.5, t_{A,II}=0.4, t_{A,III}=0.3, t_{A,IV}=0.4, t_{A,V}=0.3, t_{A,VI}=0.1$
        *   $t_{B,I}=0.3, t_{B,II}=0.8, t_{B,III}=0.9, t_{B,IV}=0.5, t_{B,V}=0.6, t_{B,VI}=0.2$
        *   $t_{C,I}=0.7, t_{C,II}=0.7, t_{C,III}=0.3, t_{C,IV}=0.7, t_{C,V}=0.4, t_{C,VI}=0.4$
        *   $t_{D,I}=0.6, t_{D,II}=0.4, t_{D,III}=0.2, t_{D,IV}=0.6, t_{D,V}=0.5, t_{D,VI}=0.8$

*   **Derived Net Profit Coefficients ($\pi_{ij}$):**
    The profit per kg for shipping from plant $i$ to region $j$ is calculated as:
    $$ \pi_{ij} = p_j - c_i - t_{ij} $$

    Let's calculate $\pi_{ij}$ for all pairs to ensure the objective function is correctly scaled and to check for negative profits (which might imply we should *not* ship to certain regions if supply were unlimited, but here supply is limited, so we must ship all supply to maximize total revenue minus costs).

    **Plant A ($c_A=1.2$):**
    *   $\pi_{A,I} = 2.0 - 1.2 - 0.5 = 0.3$
    *   $\pi_{A,II} = 2.4 - 1.2 - 0.4 = 0.8$
    *   $\pi_{A,III} = 1.8 - 1.2 - 0.3 = 0.3$
    *   $\pi_{A,IV} = 2.2 - 1.2 - 0.4 = 0.6$
    *   $\pi_{A,V} = 1.6 - 1.2 - 0.3 = 0.1$
    *   $\pi_{A,VI} = 2.0 - 1.2 - 0.1 = 0.7$

    **Plant B ($c_B=1.4$):**
    *   $\pi_{B,I} = 2.0 - 1.4 - 0.3 = 0.3$
    *   $\pi_{B,II} = 2.4 - 1.4 - 0.8 = 0.2$
    *   $\pi_{B,III} = 1.8 - 1.4 - 0.9 = -0.5$
    *   $\pi_{B,IV} = 2.2 - 1.4 - 0.5 = 0.3$
    *   $\pi_{B,V} = 1.6 - 1.4 - 0.6 = -0.4$
    *   $\pi_{B,VI} = 2.0 - 1.4 - 0.2 = 0.4$

    **Plant C ($c_C=1.1$):**
    *   $\pi_{C,I} = 2.0 - 1.1 - 0.7 = 0.2$
    *   $\pi_{C,II} = 2.4 - 1.1 - 0.7 = 0.6$
    *   $\pi_{C,III} = 1.8 - 1.1 - 0.3 = 0.4$
    *   $\pi_{C,IV} = 2.2 - 1.1 - 0.7 = 0.4$
    *   $\pi_{C,V} = 1.6 - 1.1 - 0.4 = 0.1$
    *   $\pi_{C,VI} = 2.0 - 1.1 - 0.4 = 0.5$

    **Plant D ($c_D=1.5$):**
    *   $\pi_{D,I} = 2.0 - 1.5 - 0.6 = -0.1$
    *   $\pi_{D,II} = 2.4 - 1.5 - 0.4 = 0.5$
    *   $\pi_{D,III} = 1.8 - 1.5 - 0.2 = 0.1$
    *   $\pi_{D,IV} = 2.2 - 1.5 - 0.6 = 0.1$
    *   $\pi_{D,V} = 1.6 - 1.5 - 0.5 = -0.4$
    *   $\pi_{D,VI} = 2.0 - 1.5 - 0.8 = -0.3$

    *Observation:* Some profit coefficients are negative (e.g., $\pi_{B,III} = -0.5$, $\pi_{D,I} = -0.1$). Since Total Supply (1000) < Total Demand (1150), the company is *forced* to ship all 1000 tons (assuming production is fixed or sunk cost is not considered in marginal profit, but usually "maximize profit" with fixed supply means we must allocate the supply to the highest profit opportunities). However, if shipping to a specific region yields a *negative* net profit (loss), an unconstrained optimization would prefer *not* to ship there. But the problem states plants have outputs (capacities) and regions have demands. Usually, in such transportation problems, "output" implies available supply that *can* be sold, and "demand" implies willingness to buy.
    
    *Crucial Interpretation Check:* Does "outputs of 200, 300..." mean maximum capacity or actual production? "Outputs... are..." usually implies available supply. If we can choose *not* to produce/ship, we would only ship to regions where $\pi_{ij} > 0$. However, standard transportation problems with $Supply < Demand$ assume all supply is shipped because holding inventory or not producing is often assumed to be zero-cost or the supply is already produced. Given the phrasing "determine the product transportation plan that maximizes the company's profit", and the explicit demands, it is standard to assume the 1000 tons must be distributed. If we were allowed to leave supply unshipped, we would add a dummy destination with 0 cost/profit. Let's assume all supply must be shipped (standard assumption for "transportation plan" given fixed outputs). If the problem implied we could discard supply, it would typically state "unused capacity has no penalty". Given the specific constraint "at least 100 tons must be supplied to Region III" and "Region IV must be fully satisfied", these are hard constraints on the flow.

    Let's re-read carefully: "four chemical plants... with respective outputs of... These supply six regions... with respective demands...". This implies a flow from plants to regions.
    Constraint 1: $\sum_{i \in P} x_{i,III} \ge 100$
    Constraint 2: $\sum_{i \in P} x_{i,IV} = 100$ (Fully satisfied)
    
    Since Supply (1000) < Demand (1150), the demand constraints for other regions will be $\le D_j$.
    Since Supply is fixed at 1000 (sum of plant outputs), we have $\sum_{j} x_{ij} = S_i$.

### 2. Decision Variables

*   $x_{ij}$: The amount of chemical (in tons) shipped from plant $i \in P$ to region $j \in R$.
    *   Domain: $x_{ij} \ge 0$ (Continuous, as tons can be fractional in such large-scale chemical distributions).

### 3. Objective Function

Maximize Total Profit ($Z$):
$$ Z = \sum_{i \in P} \sum_{j \in R} \pi_{ij} x_{ij} $$

Where $\pi_{ij}$ are the net profit coefficients calculated above (yuan/kg * 1000 kg/ton = yuan/ton? No, careful with units).
*   Prices/Costs are in Yuan/kg.
*   Quantities are in Tons.
*   1 Ton = 1000 kg.
*   Profit per ton = $(p_j - c_i - t_{ij}) \times 1000$.
*   Alternatively, keep costs in Yuan/kg and convert $x_{ij}$ to kg in the objective, or convert coefficients to Yuan/ton.
    Let's use **Yuan/ton** for coefficients to match $x_{ij}$ in tons.
    $\Pi_{ij} = 1000 \times \pi_{ij}$

    **Objective Coefficients ($\Pi_{ij}$ in Yuan/ton):**

    *   **Plant A:**
        *   $\Pi_{A,I} = 300$
        *   $\Pi_{A,II} = 800$
        *   $\Pi_{A,III} = 300$
        *   $\Pi_{A,IV} = 600$
        *   $\Pi_{A,V} = 100$
        *   $\Pi_{A,VI} = 700$
    *   **Plant B:**
        *   $\Pi_{B,I} = 300$
        *   $\Pi_{B,II} = 200$
        *   $\Pi_{B,III} = -500$
        *   $\Pi_{B,IV} = 300$
        *   $\Pi_{B,V} = -400$
        *   $\Pi_{B,VI} = 400$
    *   **Plant C:**
        *   $\Pi_{C,I} = 200$
        *   $\Pi_{C,II} = 600$
        *   $\Pi_{C,III} = 400$
        *   $\Pi_{C,IV} = 400$
        *   $\Pi_{C,V} = 100$
        *   $\Pi_{C,VI} = 500$
    *   **Plant D:**
        *   $\Pi_{D,I} = -100$
        *   $\Pi_{D,II} = 500$
        *   $\Pi_{D,III} = 100$
        *   $\Pi_{D,IV} = 100$
        *   $\Pi_{D,V} = -400$
        *   $\Pi_{D,VI} = -300$

    $$ \text{Maximize } Z = 300x_{A,I} + 800x_{A,II} + 300x_{A,III} + 600x_{A,IV} + 100x_{A,V} + 700x_{A,VI} $$
    $$ + 300x_{B,I} + 200x_{B,II} - 500x_{B,III} + 300x_{B,IV} - 400x_{B,V} + 400x_{B,VI} $$
    $$ + 200x_{C,I} + 600x_{C,II} + 400x_{C,III} + 400x_{C,IV} + 100x_{C,V} + 500x_{C,VI} $$
    $$ - 100x_{D,I} + 500x_{D,II} + 100x_{D,III} + 100x_{D,IV} - 400x_{D,V} - 300x_{D,VI} $$

### 4. Operational Constraints

**1. Supply Constraints (Plants):**
The total amount shipped from each plant must equal its output capacity (since we assume all output must be distributed to maximize profit, and supply < total demand, there is no reason to hold back if there are positive profit opportunities, but even with negative profits, if we *must* ship the output, these are equalities. If we *can* choose not to ship, they would be $\le$. Given "outputs are...", these are treated as fixed supplies to be allocated).

*   $\sum_{j \in R} x_{A,j} = 200$
*   $\sum_{j \in R} x_{B,j} = 300$
*   $\sum_{j \in R} x_{C,j} = 400$
*   $\sum_{j \in R} x_{D,j} = 100$

**2. Demand Constraints (Regions):**
The total amount received by each region cannot exceed its demand.

*   Region I: $\sum_{i \in P} x_{i,I} \le 200$
*   Region II: $\sum_{i \in P} x_{i,II} \le 150$
*   Region III: $\sum_{i \in P} x_{i,III} \le 400$ (General demand cap)
*   Region IV: $\sum_{i \in P} x_{i,IV} \le 100$ (General demand cap)
*   Region V: $\sum_{i \in P} x_{i,V} \le 150$
*   Region VI: $\sum_{i \in P} x_{i,VI} \le 150$

**3. Specific Problem Constraints:**

*   **Region III Minimum Supply:** "at least 100 tons must be supplied to Region III"
    *   $\sum_{i \in P} x_{i,III} \ge 100$

*   **Region IV Full Satisfaction:** "demand in Region IV must be fully satisfied"
    *   $\sum_{i \in P} x_{i,IV} = 100$
    *   *(Note: This overrides/reinforces the $\le 100$ constraint above. The equality is stricter.)*

**4. Non-negativity:**
*   $x_{ij} \ge 0$ for all $i \in P, j \in R$.

### Final Model Summary

**Model Type:** LP

**Index Sets:**
*   $P = \{A, B, C, D\}$
*   $R = \{I, II, III, IV, V, VI\}$

**Parameters (Yuan/ton):**
*   $S = [200, 300, 400, 100]$
*   $D = [200, 150, 400, 100, 150, 150]$
*   $\Pi_{ij}$ matrix (calculated as $1000 \times (p_j - c_i - t_{ij})$):
    $$
    \begin{bmatrix}
    300 & 800 & 300 & 600 & 100 & 700 \\
    300 & 200 & -500 & 300 & -400 & 400 \\
    200 & 600 & 400 & 400 & 100 & 500 \\
    -100 & 500 & 100 & 100 & -400 & -300
    \end{bmatrix}
    $$
    (Rows: A, B, C, D; Cols: I, II, III, IV, V, VI)

**Variables:**
*   $x_{ij} \in \mathbb{R}_{\ge 0}$ for all $i \in P, j \in R$.

**Objective:**
$$ \text{Maximize } Z = \sum_{i \in P} \sum_{j \in R} \Pi_{ij} x_{ij} $$

**Constraints:**
1.  **Supply:**
    *   $\sum_{j \in R} x_{A,j} = 200$
    *   $\sum_{j \in R} x_{B,j} = 300$
    *   $\sum_{j \in R} x_{C,j} = 400$
    *   $\sum_{j \in R} x_{D,j} = 100$

2.  **Demand:**
    *   $\sum_{i \in P} x_{i,I} \le 200$
    *   $\sum_{i \in P} x_{i,II} \le 150$
    *   $\sum_{i \in P} x_{i,III} \le 400$
    *   $\sum_{i \in P} x_{i,IV} = 100$  *(Must be fully satisfied)*
    *   $\sum_{i \in P} x_{i,V} \le 150$
    *   $\sum_{i \in P} x_{i,VI} \le 150$

3.  **Specific Constraints:**
    *   $\sum_{i \in P} x_{i,III} \ge 100$ *(At least 100 tons to Region III)*

4.  **Bounds:**
    *   $x_{ij} \ge 0$