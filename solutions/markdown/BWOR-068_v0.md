## Model Type: MILP

### Index Sets & Parameters

**Index Set:**
- $t \in \{1, 2, 3, 4, 5, 6\}$: Months, where $t=1$ is October, $t=2$ is November, $t=3$ is December, $t=4$ is January, $t=5$ is February, $t=6$ is March.

**Parameters:**
- $D_t$: Demand in month $t$ (pairs).
  - $D_1 = 40$
  - $D_2 = 20$
  - $D_3 = 30$
  - $D_4 = 40$
  - $D_5 = 30$
  - $D_6 = 20$
- $Q$: Set of allowed order quantities per month, $Q = \{10, 20, 30, 40, 50\}$.
- $C_q$: Variable order cost for quantity $q$ (yuan).
  - $C_{10} = 48$
  - $C_{20} = 86$
  - $C_{30} = 118$
  - $C_{40} = 138$
  - $C_{50} = 160$
- $h$: Holding cost rate (yuan/pair/month) = $0.2$
- $F$: Fixed ordering cost per order (yuan) = $10$
- $I_{max}$: Maximum end-of-month inventory (pairs) = $40$

### Decision Variables

1. **Ordering Variables (Binary):**
   - $y_{t,q} \in \{0, 1\}$ for all $t \in \{1, \dots, 6\}$ and $q \in Q$.
     - $y_{t,q} = 1$ if an order of exactly $q$ pairs is placed in month $t$, 0 otherwise.

2. **Inventory Variables (Continuous/Integer):**
   - $I_t \ge 0$ for $t \in \{1, \dots, 6\}$.
     - $I_t$ represents the inventory level at the **end** of month $t$ (pairs).

### Objective Function

Minimize Total Cost (Ordering Cost + Holding Cost):

$$
\text{Minimize } Z = \sum_{t=1}^{6} \sum_{q \in Q} \left( C_q + F \cdot y_{t,q} \right) + \sum_{t=1}^{6} h \cdot I_t
$$

Substituting the specific values:
$$
Z = \sum_{t=1}^{6} \left[ 48 y_{t,10} + 86 y_{t,20} + 118 y_{t,30} + 138 y_{t,40} + 160 y_{t,50} + 10 \left( \sum_{q \in Q} y_{t,q} \right) \right] + 0.2 \sum_{t=1}^{6} I_t
$$

### Operational Constraints

1. **One Order Constraint (per month):**
   The problem implies a single ordering decision per month. While it doesn't explicitly forbid multiple small orders, the phrase "possible order quantities per month are limited to..." combined with standard inventory modeling conventions for this type of problem usually implies one shipment per period. Furthermore, the fixed cost is per "order". If multiple orders were allowed, the model would need to allow $\sum y_{t,q} > 1$. However, given the discrete set of batch sizes and the context of "order quantities" (singular/plural ambiguity in translation but standard OR problems of this type usually imply one setup/order event per period), we assume at most one order event per month. If multiple orders of different sizes were intended to be combined, the variable definition would be different. Let's assume **at most one order per month** is the standard interpretation for "order quantity per month".
   $$
   \sum_{q \in Q} y_{t,q} \le 1, \quad \forall t \in \{1, \dots, 6\}
   $$
   *(Note: If the problem allowed multiple orders in a month, the LHS would be $\ge 1$ if an order is placed, or we would need separate variables for each order slot. Given the discrete choices 10-50, it is most likely a single order decision per month.)*

2. **Inventory Balance Constraint:**
   For each month $t$, the inventory at the end of the month is the beginning inventory plus incoming orders minus demand.
   Let $I_0 = 0$ (Beginning inventory of peak season is zero).
   $$
   I_t = I_{t-1} + \sum_{q \in Q} q \cdot y_{t,q} - D_t, \quad \forall t \in \{1, \dots, 6\}
   $$
   Where $I_0 = 0$.

3. **End-of-Season Inventory Constraint:**
   The inventory at the end of the peak season (end of March, $t=6$) must be zero.
   $$
   I_6 = 0
   $$

4. **Inventory Capacity Constraint:**
   End-of-month inventory must not exceed 40 pairs.
   $$
   I_t \le 40, \quad \forall t \in \{1, \dots, 6\}
   $$

5. **Non-negativity:**
   $$
   I_t \ge 0, \quad \forall t \in \{1, \dots, 6\}
   $$
   (Inventory cannot be negative, implying demand is fully met from available inventory/orders in that month).

### Summary of Formulation

- **Model Type:** MILP
- **Variables:** 30 binary variables ($6 \text{ months} \times 5 \text{ quantities}$) and 6 continuous/integer inventory variables.
- **Objective:** Minimize sum of variable order costs, fixed order costs, and holding costs.
- **Key Logic:** Inventory flows from month to month. Holding cost is applied to the ending inventory of each month. Demand is satisfied in the same month.