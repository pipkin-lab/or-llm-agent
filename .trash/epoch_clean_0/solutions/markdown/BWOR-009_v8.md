Here is the formal mathematical optimization model for the equipment production and delivery scheduling problem.

### 1. Index Sets & Parameters

**Index Sets:**
*   $t \in \{1, 2, 3, 4\}$: Set of quarters in the year.

**Parameters:**
*   $C_t$: Production capacity in quarter $t$ (units).
    *   $C_1 = 25$
    *   $C_2 = 35$
    *   $C_3 = 30$
    *   $C_4 = 20$
*   $D_t$: Delivery quantity (demand) required at the end of quarter $t$ (units).
    *   $D_1 = 15$
    *   $D_2 = 20$
    *   $D_3 = 25$
    *   $D_4 = 20$
*   $c_t$: Production cost per unit in quarter $t$ (thousand yuan).
    *   $c_1 = 12.0$
    *   $c_2 = 11.0$
    *   $c_3 = 11.5$
    *   $c_4 = 12.5$
*   $h$: Storage and maintenance fee per unit per quarter (thousand yuan).
    *   $h = 0.1$

### 2. Decision Variables

*   $x_{t, k}$: Quantity of equipment produced in quarter $t$ and delivered in quarter $k$, where $t \le k$.
    *   Domain: $x_{t, k} \ge 0$, continuous (LP relaxation is standard for aggregate production planning unless integrality is explicitly required; given the small integer inputs, the LP solution will naturally be integer, but the model is formulated as LP).
    *   Note: $x_{t, k}$ is only defined for pairs $(t, k)$ where $1 \le t \le k \le 4$. If $t > k$, $x_{t, k} = 0$ (cannot produce in the future to deliver in the past).

### 3. Objective Function

Minimize the total annual cost, which includes production costs and storage costs.

$$
\text{Minimize } Z = \sum_{t=1}^{4} \sum_{k=t}^{4} (c_t + h \cdot (k - t)) x_{t, k}
$$

**Expanded Cost Coefficients $(c_t + h(k-t))$:**
*   **Produced in Q1 ($t=1$):**
    *   Delivered in Q1 ($k=1$): $12.0 + 0.1(0) = 12.0$
    *   Delivered in Q2 ($k=2$): $12.0 + 0.1(1) = 12.1$
    *   Delivered in Q3 ($k=3$): $12.0 + 0.1(2) = 12.2$
    *   Delivered in Q4 ($k=4$): $12.0 + 0.1(3) = 12.3$
*   **Produced in Q2 ($t=2$):**
    *   Delivered in Q2 ($k=2$): $11.0 + 0.1(0) = 11.0$
    *   Delivered in Q3 ($k=3$): $11.0 + 0.1(1) = 11.1$
    *   Delivered in Q4 ($k=4$): $11.0 + 0.1(2) = 11.2$
*   **Produced in Q3 ($t=3$):**
    *   Delivered in Q3 ($k=3$): $11.5 + 0.1(0) = 11.5$
    *   Delivered in Q4 ($k=4$): $11.5 + 0.1(1) = 11.6$
*   **Produced in Q4 ($t=4$):**
    *   Delivered in Q4 ($k=4$): $12.5 + 0.1(0) = 12.5$

$$
Z = 12.0 x_{1,1} + 12.1 x_{1,2} + 12.2 x_{1,3} + 12.3 x_{1,4} + 11.0 x_{2,2} + 11.1 x_{2,3} + 11.2 x_{2,4} + 11.5 x_{3,3} + 11.6 x_{3,4} + 12.5 x_{4,4}
$$

### 4. Operational Constraints

**A. Production Capacity Constraints**
The total quantity produced in each quarter $t$ cannot exceed the capacity $C_t$.

$$
\sum_{k=t}^{4} x_{t, k} \le C_t, \quad \forall t \in \{1, 2, 3, 4\}
$$

*   $t=1$: $x_{1,1} + x_{1,2} + x_{1,3} + x_{1,4} \le 25$
*   $t=2$: $x_{2,2} + x_{2,3} + x_{2,4} \le 35$
*   $t=3$: $x_{3,3} + x_{3,4} \le 30$
*   $t=4$: $x_{4,4} \le 20$

**B. Delivery Demand Constraints**
The total quantity delivered in each quarter $k$ must exactly meet the demand $D_k$.

$$
\sum_{t=1}^{k} x_{t, k} = D_k, \quad \forall k \in \{1, 2, 3, 4\}
$$

*   $k=1$: $x_{1,1} = 15$
*   $k=2$: $x_{1,2} + x_{2,2} = 20$
*   $k=3$: $x_{1,3} + x_{2,3} + x_{3,3} = 25$
*   $k=4$: $x_{1,4} + x_{2,4} + x_{3,4} + x_{4,4} = 20$

**C. Non-negativity Constraints**

$$
x_{t, k} \ge 0, \quad \forall t, k \text{ such that } 1 \le t \le k \le 4
$$