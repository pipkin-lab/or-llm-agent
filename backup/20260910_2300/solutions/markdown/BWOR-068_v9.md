# Model Type: MILP (Mixed Integer Linear Programming)

## Index Sets & Parameters

**Index Sets:**
- $t \in \{1, 2, 3, 4, 5, 6\}$: Index set for the months in the peak season.
  - $t=1$: October
  - $t=2$: November
  - $t=3$: December
  - $t=4$: January
  - $t=5$: February
  - $t=6$: March

**Parameters:**
- $D_t$: Forecasted demand for month $t$ (pairs).
  - $D_1 = 40$
  - $D_2 = 20$
  - $D_3 = 30$
  - $D_4 = 40$
  - $D_5 = 30$
  - $D_6 = 20$
- $K$: Fixed ordering cost per order (yuan).
  - $K = 10$
- $C_q$: Variable cost for ordering quantity $q$ (yuan), where $q \in \{10, 20, 30, 40, 50\}$.
  - $C_{10} = 48$
  - $C_{20} = 86$
  - $C_{30} = 118$
  - $C_{40} = 138$
  - $C_{50} = 160$
- $h$: Storage cost per pair per month (yuan).
  - $h = 0.2$
- $I_{max}$: Maximum end-of-month inventory capacity (pairs).
  - $I_{max} = 40$
- $I_0$: Initial inventory at the beginning of the season (pairs).
  - $I_0 = 0$

## Decision Variables

Let $x_{t,q}$ be a binary variable indicating whether an order of size $q$ is placed in month $t$.
- Domain: $x_{t,q} \in \{0, 1\}$ for all $t \in \{1, \dots, 6\}$ and $q \in \{10, 20, 30, 40, 50\}$.

Let $y_t$ be a binary variable indicating whether any order is placed in month $t$ (used to model the fixed cost).
- Domain: $y_t \in \{0, 1\}$ for all $t \in \{1, \dots, 6\}$.

Let $I_t$ be the inventory level at the end of month $t$ (pairs).
- Domain: $I_t \ge 0$ (continuous, though effectively integer due to integer demands/orders).

## Objective Function

Minimize the total cost over the season, which includes variable ordering costs, fixed ordering costs, and storage costs.

$$
\text{Minimize } Z = \sum_{t=1}^{6} \left( \sum_{q \in \{10,20,30,40,50\}} C_q x_{t,q} + K y_t + h I_t \right)
$$

## Operational Constraints

1. **Single Order Type Per Month:**
   At most one order quantity can be selected per month.
   $$
   \sum_{q \in \{10,20,30,40,50\}} x_{t,q} \le 1, \quad \forall t \in \{1, \dots, 6\}
   $$

2. **Fixed Cost Linkage:**
   A fixed cost is incurred if and only if an order is placed.
   $$
   y_t \ge x_{t,q}, \quad \forall t \in \{1, \dots, 6\}, \forall q \in \{10,20,30,40,50\}
   $$
   *(Note: Since $K > 0$, the solver will set $y_t = 0$ if no $x_{t,q}=1$ to minimize cost, and $y_t=1$ if any $x_{t,q}=1$ is required.)*

3. **Inventory Balance:**
   Inventory at the end of month $t$ is the previous inventory plus incoming orders minus demand.
   $$
   I_t = I_{t-1} + \sum_{q \in \{10,20,30,40,50\}} q x_{t,q} - D_t, \quad \forall t \in \{1, \dots, 6\}
   $$
   *(With $I_0 = 0$)*

4. **Inventory Capacity:**
   End-of-month inventory must not exceed 40 pairs.
   $$
   I_t \le 40, \quad \forall t \in \{1, \dots, 6\}
   $$

5. **Final Inventory Condition:**
   Inventory at the end of the peak season (end of March) must be zero.
   $$
   I_6 = 0
   $$

6. **Non-negativity:**
   $$
   I_t \ge 0, \quad \forall t \in \{1, \dots, 6\}
   $$
   $$
   x_{t,q} \in \{0, 1\}, \quad \forall t, q
   $$
   $$
   y_t \in \{0, 1\}, \quad \forall t
   $$