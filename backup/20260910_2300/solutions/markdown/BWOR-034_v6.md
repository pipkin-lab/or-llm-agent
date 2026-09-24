# Warehouse Space Rental Optimization Model

## Model Type: MILP (Mixed-Integer Linear Programming)

> **Note:** While the continuous rental area variables make this technically an LP if areas were continuous, in practice warehouse space is often rented in discrete units (e.g., integer square meters or fixed lot sizes). However, since the problem does not explicitly state that space must be integer, and the required areas are large numbers (1000–2000 m²), we treat the decision variables as **continuous non-negative**. The model is therefore an **LP**. If integer constraints on area are required, it becomes an MILP. Given standard interpretation, we declare it as **LP** with continuous variables, but note that if the solver requires integer domains for physical units, it can be relaxed or tightened accordingly.

Actually, re-examining: the problem says "amount of space rented" without specifying discreteness. Standard practice for such problems: **continuous** is acceptable. We proceed with **LP**.

---

## Index Sets & Parameters

### Index Sets
- $M = \{1, 2, 3, 4\}$: Set of months.
- $D = \{1, 2, 3, 4\}$: Set of possible contract durations (in months).

### Parameters
- $R_m$: Required warehouse area (m²) in month $m$.
  - $R_1 = 1500$
  - $R_2 = 1000$
  - $R_3 = 2000$
  - $R_4 = 1200$

- $c_d$: Rental fee per m² for a contract of duration $d$ months (yuan/m²).
  - $c_1 = 28$
  - $c_2 = 45$
  - $c_3 = 60$
  - $c_4 = 73$

---

## Decision Variables

Let $x_{m,d}$ be the amount of warehouse space (m²) rented at the **beginning** of month $m$ under a contract of duration $d$ months.

- **Domain:** $x_{m,d} \geq 0$ for all $m \in M$, $d \in D$.
- **Validity:** A contract signed at the beginning of month $m$ with duration $d$ covers months $m, m+1, \dots, m+d-1$. Therefore, $x_{m,d}$ is only meaningful if $m + d - 1 \leq 4$ (i.e., the contract does not extend beyond month 4). Contracts that would extend beyond month 4 are not allowed (or equivalently, we restrict the index set such that $m + d - 1 \leq 4$).

Thus, the valid $(m,d)$ pairs are:
- $m=1$: $d=1,2,3,4$
- $m=2$: $d=1,2,3$ (since $2+3-1=4$)
- $m=3$: $d=1,2$ (since $3+2-1=4$)
- $m=4$: $d=1$ (since $4+1-1=4$)

For invalid pairs, $x_{m,d} = 0$ by definition.

---

## Objective Function

Minimize the total rental cost:

$$
\min \sum_{m \in M} \sum_{d \in D} c_d \cdot x_{m,d}
$$

Expanded:
$$
\min \quad 28x_{1,1} + 45x_{1,2} + 60x_{1,3} + 73x_{1,4} + 28x_{2,1} + 45x_{2,2} + 60x_{2,3} + 28x_{3,1} + 45x_{3,2} + 28x_{4,1}
$$

---

## Operational Constraints

### 1. Demand Satisfaction Constraints

For each month $t \in M$, the total space rented from all contracts that are **active** in month $t$ must be **at least** the required space $R_t$.

A contract $(m,d)$ is active in month $t$ if $m \leq t \leq m+d-1$, i.e., $t - d + 1 \leq m \leq t$.

Thus, for each month $t$:

$$
\sum_{\substack{m,d: \\ m \leq t \leq m+d-1}} x_{m,d} \geq R_t, \quad \forall t \in M
$$

Expanded for each month:

- **Month 1:** Contracts active in month 1: $(1,1), (1,2), (1,3), (1,4)$
  $$
  x_{1,1} + x_{1,2} + x_{1,3} + x_{1,4} \geq 1500
  $$

- **Month 2:** Contracts active in month 2: $(1,2), (1,3), (1,4), (2,1), (2,2), (2,3)$
  $$
  x_{1,2} + x_{1,3} + x_{1,4} + x_{2,1} + x_{2,2} + x_{2,3} \geq 1000
  $$

- **Month 3:** Contracts active in month 3: $(1,3), (1,4), (2,2), (2,3), (3,1), (3,2)$
  $$
  x_{1,3} + x_{1,4} + x_{2,2} + x_{2,3} + x_{3,1} + x_{3,2} \geq 2000
  $$

- **Month 4:** Contracts active in month 4: $(1,4), (2,3), (3,2), (4,1)$
  $$
  x_{1,4} + x_{2,3} + x_{3,2} + x_{4,1} \geq 1200
  $$

### 2. Non-negativity Constraints

$$
x_{m,d} \geq 0 \quad \forall (m,d) \text{ with } m+d-1 \leq 4
$$

---

## Feasibility Sanity Check

- Total required space over 4 months: $1500 + 1000 + 2000 + 1200 = 5700$ m²-months.
- The model allows overlapping contracts, so the total rented area-months will be at least 5700.
- No upper bounds on $x_{m,d}$, so feasibility is not an issue.
- The cost structure encourages longer contracts for larger discounts, but the per-month effective cost of longer contracts is lower:
  - $d=1$: 28 yuan/m²/month
  - $d=2$: 45/2 = 22.5 yuan/m²/month
  - $d=3$: 60/3 = 20 yuan/m²/month
  - $d=4$: 73/4 = 18.25 yuan/m²/month
- This suggests longer contracts are more cost-effective per month, which aligns with the discount structure.

The model is feasible and bounded below (by 0), so an optimal solution exists.