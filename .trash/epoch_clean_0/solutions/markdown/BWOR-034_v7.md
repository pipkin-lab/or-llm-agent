# Mathematical Optimization Model: Warehouse Rental Planning

## Model Type Declaration
**LP (Linear Program)**

The objective function and all constraints are linear in the decision variables. No non-linear terms (products of variables, squares, etc.) are present.

---

## Index Sets & Parameters

### Index Sets
- $t \in \{1, 2, 3, 4\}$: Set of months (periods).
- $d \in \{1, 2, 3, 4\}$: Set of possible contract durations (in months).

### Parameters

**Required warehouse area (m²) for month $t$:**
| $t$ | 1 | 2 | 3 | 4 |
|-----|-------|-------|-------|-------|
| $R_t$ | 1,500 | 1,000 | 2,000 | 1,200 |

**Rental fee per m² for a contract of duration $d$ (yuan/m²), signed at the beginning of month $t$:**

| $d$ | 1 | 2 | 3 | 4 |
|-----|------|------|------|------|
| $c_d$ | 28 | 45 | 60 | 73 |

> **Note on timing convention:** A contract signed at the **beginning** of month $t$ with duration $d$ covers months $t, t+1, \ldots, t+d-1$. Therefore, a contract of duration $d$ signed at the beginning of month $t$ is only feasible if $t + d - 1 \leq 4$, i.e., $t \leq 5 - d$.

---

## Decision Variables

Let $x_{t,d}$ be the **continuous** non-negative variable representing the area (in m²) of warehouse space rented under a contract of duration $d$ months, signed at the beginning of month $t$.

**Domain:**
$$x_{t,d} \geq 0, \quad \forall \, t \in \{1,2,3,4\}, \, d \in \{1,2,3,4\} \text{ such that } t + d - 1 \leq 4$$

The valid $(t,d)$ pairs are:
- $t=1$: $d \in \{1,2,3,4\}$
- $t=2$: $d \in \{1,2,3\}$
- $t=3$: $d \in \{1,2\}$
- $t=4$: $d \in \{1\}$

Total of $4+3+2+1 = 10$ decision variables.

---

## Objective Function

**Minimize** the total rental cost:

$$\min \; Z = \sum_{t=1}^{4} \sum_{d=1}^{4-d+1} c_d \cdot x_{t,d}$$

Expanded:
$$Z = 28\,x_{1,1} + 45\,x_{1,2} + 60\,x_{1,3} + 73\,x_{1,4} + 28\,x_{2,1} + 45\,x_{2,2} + 60\,x_{2,3} + 28\,x_{3,1} + 45\,x_{3,2} + 28\,x_{4,1}$$

---

## Operational Constraints

### 1. Demand Satisfaction Constraints

For each month $t$, the total area covered by all active contracts must be **at least** the required area $R_t$.

A contract $x_{t',d}$ is active in month $t$ if and only if $t' \leq t \leq t' + d - 1$.

$$\sum_{\substack{t'=1 \\ t' \leq t}}^{4} \sum_{\substack{d=1 \\ t' + d - 1 \geq t}}^{4} x_{t',d} \;\geq\; R_t, \quad \forall \, t \in \{1,2,3,4\}$$

Expanded by month:

**Month 1** ($t=1$): Active contracts are those with $t'=1$ and any $d \geq 1$.
$$x_{1,1} + x_{1,2} + x_{1,3} + x_{1,4} \;\geq\; 1500$$

**Month 2** ($t=2$): Active contracts are those with $t'=1, d \geq 2$ and $t'=2, d \geq 1$.
$$x_{1,2} + x_{1,3} + x_{1,4} + x_{2,1} + x_{2,2} + x_{2,3} \;\geq\; 1000$$

**Month 3** ($t=3$): Active contracts are those with $t'=1, d \geq 3$; $t'=2, d \geq 2$; and $t'=3, d \geq 1$.
$$x_{1,3} + x_{1,4} + x_{2,2} + x_{2,3} + x_{3,1} + x_{3,2} \;\geq\; 2000$$

**Month 4** ($t=4$): Active contracts are those with $t'=1, d=4$; $t'=2, d=3$; $t'=3, d=2$; and $t'=4, d=1$.
$$x_{1,4} + x_{2,3} + x_{3,2} + x_{4,1} \;\geq\; 1200$$

### 2. Non-negativity Constraints

$$x_{t,d} \;\geq\; 0, \quad \forall \, (t,d) \text{ with } t + d - 1 \leq 4$$

---

## Feasibility Sanity Check

- **Total demand over 4 months:** $1500 + 1000 + 2000 + 1200 = 5700$ m²-months.
- **Cheapest per m²-month rate:** A 1-month contract costs 28 yuan/m² for 1 month → 28 yuan/m²-month. All longer contracts have higher per-month rates (45/2=22.5, 60/3=20, 73/4≈18.25 yuan/m²-month). Wait—let me recompute:
  - $d=1$: 28/1 = 28 yuan/m²-month
  - $d=2$: 45/2 = 22.5 yuan/m²-month
  - $d=3$: 60/3 = 20 yuan/m²-month
  - $d=4$: 73/4 = 18.25 yuan/m²-month
  
  The **longer** the contract, the **lower** the per-month rate. This is consistent with the problem statement ("greater discounts" for longer periods).

- **Feasibility:** The problem is feasible. For example, signing a 4-month contract of 2,000 m² at $t=1$ costs $73 \times 2000 = 146{,}000$ and covers all months (since 2000 ≥ 1500, 1000, 2000, 1200). Additional short-term contracts can fill any gaps. No capacity upper bounds are imposed, so the model is always feasible.

- **No supply-side inequality issue:** This is a pure cost-minimization problem with demand-side lower bounds. There is no "excess supply" to dispose of, so the use of $\geq$ on the demand constraints is appropriate. The solver will naturally set $x_{t,d}=0$ for any contract that is not cost-effective, and the optimal solution will use exactly the required area (no more), since all costs are positive.