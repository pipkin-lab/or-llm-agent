## 1. Index Sets & Parameters

**Index Sets:**
*   $I = \{1, 2, 3, 4\}$: Set of quarters in the year.

**Parameters:**
*   $C_i$: Production capacity in quarter $i$ (units).
    *   $C_1 = 25, C_2 = 35, C_3 = 30, C_4 = 20$
*   $D_i$: Required delivery quantity in quarter $i$ (units).
    *   $D_1 = 15, D_2 = 20, D_3 = 25, D_4 = 20$
*   $p_i$: Production cost per unit in quarter $i$ (thousand yuan/unit).
    *   $p_1 = 12.0, p_2 = 11.0, p_3 = 11.5, p_4 = 12.5$
*   $h$: Holding (storage and maintenance) cost per unit per quarter (thousand yuan/unit/quarter).
    *   $h = 0.1$

## 2. Decision Variables

Let $x_{i,t}$ be the number of units produced in quarter $i$ and delivered in quarter $t$, where $t \ge i$.
*   **Domain**: $x_{i,t} \ge 0$ for all $i \in I, t \in I, t \ge i$.
*   **Note**: Since production and demand are integer-valued and the constraint matrix for this transportation-like problem is totally unimodular, the optimal solution will naturally be integer. Thus, continuous variables are sufficient.

## 3. Objective Function

Minimize the total annual cost, which consists of production costs and holding costs.
The holding cost for units produced in quarter $i$ and delivered in quarter $t$ is $h \times (t - i)$.
The total cost per unit produced in $i$ and delivered in $t$ is $p_i + h(t-i)$.

$$
\text{Minimize } Z = \sum_{i=1}^{4} \sum_{t=i}^{4} \left( p_i + h(t-i) \right) x_{i,t}
$$

Expanding the coefficients for clarity:
*   Quarter 1 production ($i=1$):
    *   Delivered in Q1 ($t=1$): Cost $12.0 + 0.1(0) = 12.0$
    *   Delivered in Q2 ($t=2$): Cost $12.0 + 0.1(1) = 12.1$
    *   Delivered in Q3 ($t=3$): Cost $12.0 + 0.1(2) = 12.2$
    *   Delivered in Q4 ($t=4$): Cost $12.0 + 0.1(3) = 12.3$
*   Quarter 2 production ($i=2$):
    *   Delivered in Q2 ($t=2$): Cost $11.0 + 0.1(0) = 11.0$
    *   Delivered in Q3 ($t=3$): Cost $11.0 + 0.1(1) = 11.1$
    *   Delivered in Q4 ($t=4$): Cost $11.0 + 0.1(2) = 11.2$
*   Quarter 3 production ($i=3$):
    *   Delivered in Q3 ($t=3$): Cost $11.5 + 0.1(0) = 11.5$
    *   Delivered in Q4 ($t=4$): Cost $11.5 + 0.1(1) = 11.6$
*   Quarter 4 production ($i=4$):
    *   Delivered in Q4 ($t=4$): Cost $12.5 + 0.1(0) = 12.5$

$$
Z = 12.0x_{1,1} + 12.1x_{1,2} + 12.2x_{1,3} + 12.3x_{1,4} + 11.0x_{2,2} + 11.1x_{2,3} + 11.2x_{2,4} + 11.5x_{3,3} + 11.6x_{3,4} + 12.5x_{4,4}
$$

## 4. Operational Constraints

**1. Production Capacity Constraints:**
The total units produced in quarter $i$ (for all future delivery quarters $t \ge i$) cannot exceed the production capacity $C_i$.

$$
\sum_{t=i}^{4} x_{i,t} \le C_i, \quad \forall i \in \{1, 2, 3, 4\}
$$

Specifically:
*   $x_{1,1} + x_{1,2} + x_{1,3} + x_{1,4} \le 25$
*   $x_{2,2} + x_{2,3} + x_{2,4} \le 35$
*   $x_{3,3} + x_{3,4} \le 30$
*   $x_{4,4} \le 20$

**2. Delivery Demand Constraints:**
The total units delivered in quarter $t$ (from all previous production quarters $i \le t$) must exactly meet the delivery requirement $D_t$.

$$
\sum_{i=1}^{t} x_{i,t} = D_t, \quad \forall t \in \{1, 2, 3, 4\}
$$

Specifically:
*   $x_{1,1} = 15$
*   $x_{1,2} + x_{2,2} = 20$
*   $x_{1,3} + x_{2,3} + x_{3,3} = 25$
*   $x_{1,4} + x_{2,4} + x_{3,4} + x_{4,4} = 20$

**3. Non-negativity Constraints:**
$$
x_{i,t} \ge 0, \quad \forall i \in I, t \in I, t \ge i
$$