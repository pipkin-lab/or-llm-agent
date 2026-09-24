# Production Planning Problem

## MANDATORY COST INVENTORY

| # | Cost Item | Value | Entity Modified |
|---|-----------|-------|-----------------|
| 1 | Production cost | 10,000 yuan per 100 units (i.e., 100 yuan per unit) | Applied to every unit produced in any month |
| 2 | Fixed operating expense | 4,000 yuan | Paid in any month where production > 0 |
| 3 | Storage cost | 1,000 yuan per 100 units per month (i.e., 10 yuan per unit per month) | Applied to inventory held at end of each month (months 1–5) |

All three cost figures are explicitly stated in the problem text. No [NOT_PROVIDED] parameters.

---

## Model Type

**MILP** (Mixed Integer Linear Programming)

- Continuous variables: production quantities $P_t$, inventory levels $I_t$
- Binary variables: $y_t \in \{0, 1\}$ to capture the fixed operating expense (production is continuous, but the fixed cost is triggered by a binary indicator)

---

## Index Sets & Parameters

**Sets:**
- $T = \{1, 2, 3, 4, 5, 6\}$: set of months (January through June)

**Parameters (all in base units: units, yuan):**

| Parameter | Symbol | Value | Source |
|-----------|--------|-------|--------|
| Monthly production capacity | $U$ | 400 units | "production capacity is 400 units per month" |
| Warehouse storage capacity | $W$ | 300 units | "warehouse storage capacity is 300 units" |
| Variable production cost | $c$ | 100 yuan/unit | "10,000 yuan per 100 units" |
| Fixed production cost | $F$ | 4,000 yuan | "fixed operating expenses of 4,000 yuan" |
| Holding cost | $h$ | 10 yuan/unit/month | "1,000 yuan per 100 units per month" |
| Delivery demand (units) | $d_t$ | $d_1=100,\; d_2=200,\; d_3=500,\; d_4=300,\; d_5=200,\; d_6=100$ | Table 7-5 (values in hundreds of units × 100) |

**Aggregate check:** Total demand = $100+200+500+300+200+100 = 1400$ units. Total production capacity over 6 months = $6 \times 400 = 2400$ units. Feasible.

---

## Decision Variables

| Variable | Domain | Description |
|----------|--------|-------------|
| $P_t \;\forall t \in T$ | $P_t \geq 0$, continuous | Units produced in month $t$ |
| $I_t \;\forall t \in T$ | $I_t \geq 0$, continuous | Units in inventory at the **end** of month $t$ |
| $y_t \;\forall t \in T$ | $y_t \in \{0, 1\}$, binary | $y_t = 1$ if production occurs in month $t$ ($P_t > 0$), else 0 |

---

## Objective Function

**MINIMIZE** total cost:

$$\min \quad \sum_{t=1}^{6} \left( c \, P_t + F \, y_t + h \, I_t \right)$$

Substituting numeric values:

$$\min \quad 100 \sum_{t=1}^{6} P_t \;+\; 4000 \sum_{t=1}^{6} y_t \;+\; 10 \sum_{t=1}^{6} I_t$$

**Note on $I_6$:** The problem states "none remaining after the final delivery at the end of June," so $I_6 = 0$ is enforced by constraint below. The holding cost term for $I_6$ will therefore contribute zero, but it is retained in the sum for uniformity (it will be zero at optimality due to the constraint $I_6 = 0$).

---

## Operational Constraints

### 1. Inventory Balance (for each month $t = 1, \ldots, 6$)

$$I_t = I_{t-1} + P_t - d_t, \quad \forall t \in T$$

with the initial condition $I_0 = 0$ ("no inventory at the beginning").

Explicitly:
- $I_1 = P_1 - 100$
- $I_2 = I_1 + P_2 - 200$
- $I_3 = I_2 + P_3 - 500$
- $I_4 = I_3 + P_4 - 300$
- $I_5 = I_4 + P_5 - 200$
- $I_6 = I_5 + P_6 - 100$

### 2. End-of-Horizon Inventory Constraint

$$I_6 = 0$$

("none remaining after the final delivery at the end of June")

### 3. Production Capacity (for each month $t = 1, \ldots, 6$)

$$P_t \leq U = 400, \quad \forall t \in T$$

### 4. Warehouse Storage Capacity (for each month $t = 1, \ldots, 6$)

$$I_t \leq W = 300, \quad \forall t \in T$$

(Since $I_6 = 0$, this is automatically satisfied for $t=6$; it is binding for $t = 1, \ldots, 5$.)

### 5. Fixed Cost Linking (Big-M) — for each month $t = 1, \ldots, 6$

$$P_t \leq U \cdot y_t, \quad \forall t \in T$$

i.e., $P_t \leq 400 \, y_t$. This ensures $y_t = 1$ whenever $P_t > 0$, and allows $y_t = 0$ only when $P_t = 0$.

### 6. Non-negativity and Domain Bounds

$$P_t \geq 0, \quad \forall t \in T$$
$$I_t \geq 0, \quad \forall t \in T$$
$$y_t \in \{0, 1\}, \quad \forall t \in T$$

---

## Feasibility Sanity Check

- **Total demand:** 1400 units over 6 months.
- **Total capacity:** 6 × 400 = 2400 units ≥ 1400. ✓
- **Peak single-month demand:** 500 units (month 3). Since 500 > 400 (capacity), the factory **cannot** meet month-3 demand from current-month production alone; it must build inventory in prior months.
- **Storage constraint check:** To meet month-3 demand of 500 from production of at most 400, the factory needs at least 100 units of inventory entering month 3. The warehouse holds up to 300 units, so this is feasible. ✓
- **Backward feasibility:** Month 3 needs $I_2 + P_3 = 500$. With $P_3 \leq 400$, we need $I_2 \geq 100$. Month 2: $I_1 + P_2 = 200 + I_2$, so $I_1 + P_2 \geq 300$. With $P_2 \leq 400$, we need $I_1 \geq -100$ (trivially satisfied, $I_1 \geq 0$). So $I_2 = I_1 + P_2 - 200$ can reach 100 with $P_2 = 300, I_1 = 0$, or $P_2 = 200, I_1 = 100$, etc. All within bounds. ✓
- The model is **feasible**.

---

## Objective Parameter Cross-Reference

| Parameter in Objective | Numeric Value | Located in Text? |
|------------------------|--------------|-----------------|
| $c$ (variable production cost) | 100 yuan/unit | ✓ "production cost for every 100 units is 10,000 yuan" |
| $F$ (fixed cost) | 4,000 yuan | ✓ "fixed operating expenses of 4,000 yuan" |
| $h$ (holding cost) | 10 yuan/unit/month | ✓ "storage cost is 1,000 yuan per 100 units per month" |

All objective parameters confirmed. No [NOT_PROVIDED] values.

---

## Magnitude Sanity Check

**Trivial greedy solution estimate:** Produce exactly what is needed each month (backlog to meet month-3 demand).

- Month 1: $P_1 = 100$, $I_1 = 0$. Cost: $100 \times 100 + 4000 = 14{,}000$
- Month 2: $P_2 = 300$, $I_2 = 100$. Cost: $300 \times 100 + 4000 + 10 \times 100 = 35{,}000$
- Month 3: $P_3 = 400$, $I_3 = 0$. Cost: $400 \times 100 + 4000 = 44{,}000$
- Month 4: $P_4 = 300$, $I_4 = 0$. Cost: $300 \times 100 + 4000 = 34{,}000$
- Month 5: $P_5 = 200$, $I_5 = 0$. Cost: $200 \times 100 + 4000 = 24{,}000$
- Month 6: $P_6 = 100$, $I_6 = 0$. Cost: $100 \times 100 + 4000 = 14{,}000$

Total ≈ 165,000 yuan. This is a reasonable magnitude for a 6-month production plan with these cost levels. The problem asks for total cost in yuan — the objective is in yuan. ✓