# Multi-Period Production Planning with Inventory and Late Delivery Penalties

## Model Type
**LP** (Linear Programming)

## Index Sets & Parameters

**Sets:**
- $P = \{1, 2, 3\}$: Products (I, II, III)
- $T = \{1, 2, 3, 4\}$: Quarters

**Parameters:**

| Parameter | Description | Values |
|-----------|-------------|--------|
| $d_{p,t}$ | Contract order (demand) for product $p$ in quarter $t$ | See table below |
| $H_t$ | Working hours available in quarter $t$ | 15,000 for all $t$ |
| $h_p$ | Hours required per unit of product $p$ | $h_1=2, h_2=4, h_3=3$ |
| $L_p$ | Late delivery penalty per unit per quarter | $L_1=20, L_2=20, L_3=10$ |
| $I_c$ | Inventory holding cost per unit per quarter | 5 |

**Demand Matrix $d_{p,t}$:**

| $p \backslash t$ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| 1 (I) | 1500 | 1000 | 2000 | 1200 |
| 2 (II) | 1500 | 1500 | 1200 | 1500 |
| 3 (III) | 1000 | 2000 | 1500 | 2500 |

**Initial Inventory:** $S_{p,0} = 0$ for all $p$

**Final Inventory Requirement:** $S_{p,4} = 150$ for all $p$

**Production Restriction:** Product I cannot be produced in Q2.

## Decision Variables

- $x_{p,t} \geq 0$, continuous: Units of product $p$ produced in quarter $t$
- $S_{p,t} \geq 0$, continuous: Inventory of product $p$ at the **end** of quarter $t$ (before late-delivery resolution)
- $L_{p,t} \geq 0$, continuous: Units of product $p$ delivered **late** (backlog) at the end of quarter $t$. These are units whose delivery deadline (quarter $t$) has passed but have not yet been fulfilled.

**Domain Restrictions:**
- $x_{1,2} = 0$ (Product I not producible in Q2)
- All variables $\geq 0$

## Objective Function

**MINIMIZE** total cost = inventory holding costs + late delivery penalties

$$\min \sum_{t=1}^{4} \sum_{p=1}^{3} I_c \cdot S_{p,t} \;+\; \sum_{t=1}^{4} \sum_{p=1}^{3} L_p \cdot L_{p,t}$$

Substituting values:

$$\min \sum_{t=1}^{4} \sum_{p=1}^{3} 5 \cdot S_{p,t} \;+\; \sum_{t=1}^{4} \sum_{p=1}^{3} L_p \cdot L_{p,t}$$

where $L_1 = 20, L_2 = 20, L_3 = 10$.

> **Note on timing:** $S_{p,t}$ is the inventory carried from end of quarter $t$ to start of quarter $t+1$ (incurring holding cost for quarter $t$). $L_{p,t}$ is the backlog of undelivered units at the end of quarter $t$ (incurring penalty for quarter $t$). At the end of Q4, all backlogs must be zero (see constraint below), so $L_{p,4}=0$ is enforced.

## Operational Constraints

### 1. Inventory Balance (for each product $p$, quarter $t$)

$$S_{p,t} = S_{p,t-1} + x_{p,t} - d_{p,t} + L_{p,t-1} - L_{p,t}$$

for all $p \in P$, $t \in T$, with $S_{p,0} = 0$ and $L_{p,0} = 0$.

**Interpretation:** End-of-quarter inventory = beginning inventory + production − demand + beginning backlog − ending backlog.

When $S_{p,t} > 0$, the product was over-produced and carried forward. When $S_{p,t} = 0$ and $L_{p,t} > 0$, there is a backlog of unmet demand. The constraint ensures that $S_{p,t}$ and $L_{p,t}$ cannot both be positive simultaneously (complementary slackness is enforced by the objective: since both incur costs, the optimizer will set one to zero).

### 2. Working Hours Constraint (for each quarter $t$)

$$\sum_{p=1}^{3} h_p \cdot x_{p,t} \leq H_t$$

Substituting values:

$$2 x_{1,t} + 4 x_{2,t} + 3 x_{3,t} \leq 15000, \quad \forall\, t \in \{1,2,3,4\}$$

### 3. Production Restriction

$$x_{1,2} = 0$$

(Product I cannot be produced in Q2)

### 4. Final Inventory Requirement (end of Q4)

$$S_{p,4} = 150, \quad \forall\, p \in \{1, 2, 3\}$$

### 5. Backlog Clearance (end of Q4)

All late deliveries must be resolved by the end of Q4 (the planning horizon ends; no further production is allowed after Q4 to clear backlogs):

$$L_{p,4} = 0, \quad \forall\, p \in \{1, 2, 3\}$$

### 6. Non-negativity

$$x_{p,t} \geq 0, \quad S_{p,t} \geq 0, \quad L_{p,t} \geq 0, \quad \forall\, p \in P,\; t \in T$$

## Feasibility Sanity Check

- **Total demand:** $(1500+1000+2000+1200) + (1500+1500+1200+1500) + (1000+2000+1500+2500) = 5700 + 5700 + 7000 = 18400$
- **Required final inventory:** $3 \times 150 = 450$
- **Total units to produce:** $18400 + 450 = 18850$
- **Total hours required (if all produced at minimum-hour product):** $18850 \times 2 = 37700$ hours minimum
- **Total hours available:** $4 \times 15000 = 60000$ hours
- Since $37700 < 60000$, the problem is feasible from a capacity standpoint. The specific mix will determine whether the hour constraints are binding in individual quarters.

## Parameter Completeness Verification

| Parameter | Value | Source |
|-----------|-------|--------|
| $d_{1,1}, d_{1,2}, d_{1,3}, d_{1,4}$ | 1500, 1000, 2000, 1200 | Table 1-10 |
| $d_{2,1}, d_{2,2}, d_{2,3}, d_{2,4}$ | 1500, 1500, 1200, 1500 | Table 1-10 |
| $d_{3,1}, d_{3,2}, d_{3,3}, d_{3,4}$ | 1000, 2000, 1500, 2500 | Table 1-10 |
| $H_t$ | 15000 | Problem text |
| $h_1, h_2, h_3$ | 2, 4, 3 | Problem text |
| $L_1, L_2, L_3$ | 20, 20, 10 | Problem text |
| $I_c$ | 5 | Problem text |
| Final inventory | 150 per product | Problem text |
| Initial inventory | 0 | Problem text |
| Prod. restriction | $x_{1,2}=0$ | Problem text |

All parameters are fully specified. No `[NOT_PROVIDED]` values.