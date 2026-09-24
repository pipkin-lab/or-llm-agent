To formulate the optimal replacement strategy for the machine over the 4-year period, we will use a **Linear Programming (LP)** model based on a "buy-and-sell" flow balance approach. This approach is superior to discrete state-based integer programming for this specific horizon because it naturally handles the continuous nature of the asset value and ensures that every unit of "machine life" is accounted for from purchase to final disposal.

### 1. Model Type Declaration
**Model Type:** Linear Programming (LP)
**Reasoning:** The decision variables represent the quantity of machines (or flow of machine-years) bought at specific times and sold at specific later times. Since the problem implies a single machine unit, the variables will effectively be 0 or 1, but the linear structure allows us to solve this as an LP, which will yield integer solutions due to the network flow structure of the problem (total unimodularity).

### 2. Index Sets & Parameters

**Index Sets:**
*   $t \in \{1, 2, 3, 4\}$: The years in the planning horizon.
*   $k \in \{1, 2, 3, 4\}$: The age of the machine in years (service lifespan duration).

**Parameters (Extracted from Table 8-7 and Text):**

*   **Purchase Prices ($P_t$)** at the beginning of year $t$ (thousand yuan):
    *   $P_1 = 2.5$
    *   $P_2 = 2.6$
    *   $P_3 = 2.8$
    *   $P_4 = 3.1$
*   **Salvage Values ($S_k$)** after $k$ years of service (thousand yuan):
    *   $S_1 = 2.0$
    *   $S_2 = 1.6$
    *   $S_3 = 1.3$
    *   $S_4 = 1.1$
*   **Operating & Maintenance Costs ($M_k$)** for a machine in its $k$-th year of life (thousand yuan):
    *   $M_1 = 0.3$ (First year of life)
    *   $M_2 = 0.8$ (Second year of life)
    *   $M_3 = 1.5$ (Third year of life)
    *   $M_4 = 2.0$ (Fourth year of life)

**Derived Parameter:**
*   **Net Cost of Holding a Machine for $k$ Years Starting in Year $t$**:
    Let $C_{t,k}$ be the total net cost associated with buying a new machine at the start of year $t$, operating it for $k$ years (covering years $t, t+1, \dots, t+k-1$), and selling it at the end of year $t+k-1$.
    $$ C_{t,k} = P_t - S_k + \sum_{i=1}^{k} M_i $$
    *Note: The salvage value $S_k$ is received at the end of the $k$-th year of service. The operating costs are incurred in each year of service.*

    Let's calculate the specific net costs for valid $(t, k)$ pairs where $t+k-1 \le 4$:

    *   **Life of 1 year ($k=1$):**
        *   Cost component: $P_t - S_1 + M_1 = P_t - 2.0 + 0.3 = P_t - 1.7$
        *   $C_{1,1} = 2.5 - 1.7 = 0.8$
        *   $C_{2,1} = 2.6 - 1.7 = 0.9$
        *   $C_{3,1} = 2.8 - 1.7 = 1.1$
        *   $C_{4,1} = 3.1 - 1.7 = 1.4$

    *   **Life of 2 years ($k=2$):**
        *   Cost component: $P_t - S_2 + M_1 + M_2 = P_t - 1.6 + 0.3 + 0.8 = P_t - 0.5$
        *   $C_{1,2} = 2.5 - 0.5 = 2.0$
        *   $C_{2,2} = 2.6 - 0.5 = 2.1$
        *   $C_{3,2} = 2.8 - 0.5 = 2.3$
        *   ($C_{4,2}$ is invalid as it exceeds year 4)

    *   **Life of 3 years ($k=3$):**
        *   Cost component: $P_t - S_3 + M_1 + M_2 + M_3 = P_t - 1.3 + 0.3 + 0.8 + 1.5 = P_t + 1.3$
        *   $C_{1,3} = 2.5 + 1.3 = 3.8$
        *   $C_{2,3} = 2.6 + 1.3 = 3.9$
        *   ($C_{3,3}$ is invalid)

    *   **Life of 4 years ($k=4$):**
        *   Cost component: $P_t - S_4 + M_1 + M_2 + M_3 + M_4 = P_t - 1.1 + 0.3 + 0.8 + 1.5 + 2.0 = P_t + 3.5$
        *   $C_{1,4} = 2.5 + 3.5 = 6.0$
        *   ($C_{2,4}$ is invalid)

### 3. Decision Variables

Let $x_{t,k}$ be a binary variable (modeled as continuous $[0,1]$ in LP) defined as:
$$
x_{t,k} = \begin{cases} 
1 & \text{if a machine is purchased at the beginning of year } t \text{ and sold at the end of year } t+k-1 \\
0 & \text{otherwise}
\end{cases}
$$
Domain: $x_{t,k} \in [0, 1]$ for all valid $(t, k)$ such that $1 \le t \le 4$ and $1 \le k \le 5-t$.

Valid indices $(t,k)$:
$(1,1), (1,2), (1,3), (1,4)$
$(2,1), (2,2), (2,3)$
$(3,1), (3,2)$
$(4,1)$

### 4. Objective Function

Minimize the total net cost. The total cost is the sum of the net costs of all machine lifecycles selected. Since we only have one machine, we select a set of non-overlapping lifecycles that cover the entire 4-year period.

$$ \text{Minimize } Z = \sum_{t=1}^{4} \sum_{k=1}^{5-t} C_{t,k} x_{t,k} $$

Substituting the calculated $C_{t,k}$ values:
$$ Z = 0.8x_{1,1} + 2.0x_{1,2} + 3.8x_{1,3} + 6.0x_{1,4} + 0.9x_{2,1} + 2.1x_{2,2} + 3.9x_{2,3} + 1.1x_{3,1} + 2.3x_{3,2} + 1.4x_{4,1} $$

### 5. Operational Constraints

The core constraint is that for every year $t$ in the horizon, the machine must be in operation. A machine purchased at year $i$ with a lifespan of $k$ years covers the years $i, i+1, \dots, i+k-1$. Therefore, for each year $t$, the sum of all $x_{i,k}$ such that the interval $[i, i+k-1]$ includes $t$ must equal 1.

**Year 1 Coverage:**
Machines covering year 1 are those with start $i=1$.
$$ x_{1,1} + x_{1,2} + x_{1,3} + x_{1,4} = 1 $$

**Year 2 Coverage:**
Machines covering year 2 are those with start $i=1, k \ge 2$ OR start $i=2, k \ge 1$.
$$ x_{1,2} + x_{1,3} + x_{1,4} + x_{2,1} + x_{2,2} + x_{2,3} = 1 $$

**Year 3 Coverage:**
Machines covering year 3 are those with start $i=1, k \ge 3$ OR start $i=2, k \ge 2$ OR start $i=3, k \ge 1$.
$$ x_{1,3} + x_{1,4} + x_{2,2} + x_{2,3} + x_{3,1} + x_{3,2} = 1 $$

**Year 4 Coverage:**
Machines covering year 4 are those with start $i=1, k=4$ OR start $i=2, k=3$ OR start $i=3, k=2$ OR start $i=4, k=1$.
$$ x_{1,4} + x_{2,3} + x_{3,2} + x_{4,1} = 1 $$

**Non-negativity / Domain Constraints:**
$$ x_{t,k} \ge 0 \quad \forall (t,k) \in \text{Valid Indices} $$
*(Note: In a practical implementation, $x_{t,k} \le 1$ is implied by the coverage constraints summing to 1, but explicit bounds $0 \le x_{t,k} \le 1$ are good practice.)*

### 6. Feasibility Sanity Check

Let's check if a feasible solution exists.
Consider the strategy: Buy at Year 1, keep for 4 years.
$x_{1,4} = 1$, all others 0.
- Year 1: $1 = 1$ (OK)
- Year 2: $1 = 1$ (OK)
- Year 3: $1 = 1$ (OK)
- Year 4: $1 = 1$ (OK)
Cost: $6.0$.

Consider strategy: Buy Year 1, sell end Y1, Buy Y2, sell end Y2, Buy Y3, sell end Y3, Buy Y4, sell end Y4.
$x_{1,1}=1, x_{2,1}=1, x_{3,1}=1, x_{4,1}=1$.
- Year 1: $1=1$
- Year 2: $1=1$
- Year 3: $1=1$
- Year 4: $1=1$
Cost: $0.8 + 0.9 + 1.1 + 1.4 = 4.2$.

The constraints are consistent and feasible. The model correctly captures the trade-off between higher purchase prices in later years and higher operating costs for older machines.

### Final Model Summary

**Model Type:** LP

**Parameters:**
$C_{1,1}=0.8, C_{1,2}=2.0, C_{1,3}=3.8, C_{1,4}=6.0$
$C_{2,1}=0.9, C_{2,2}=2.1, C_{2,3}=3.9$
$C_{3,1}=1.1, C_{3,2}=2.3$
$C_{4,1}=1.4$

**Variables:**
$x_{t,k} \in [0,1]$ for all valid $(t,k)$.

**Objective:**
$$ \text{Min } Z = 0.8x_{1,1} + 2.0x_{1,2} + 3.8x_{1,3} + 6.0x_{1,4} + 0.9x_{2,1} + 2.1x_{2,2} + 3.9x_{2,3} + 1.1x_{3,1} + 2.3x_{3,2} + 1.4x_{4,1} $$

**Constraints:**
1.  $x_{1,1} + x_{1,2} + x_{1,3} + x_{1,4} = 1$
2.  $x_{1,2} + x_{1,3} + x_{1,4} + x_{2,1} + x_{2,2} + x_{2,3} = 1$
3.  $x_{1,3} + x_{1,4} + x_{2,2} + x_{2,3} + x_{3,1} + x_{3,2} = 1$
4.  $x_{1,4} + x_{2,3} + x_{3,2} + x_{4,1} = 1$
5.  $x_{t,k} \ge 0$