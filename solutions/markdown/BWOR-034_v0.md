# Warehouse Rental Optimization Model

## Model Type: LP (Linear Programming)

All decision variables (rented areas) are continuous, and both the objective function and all constraints are linear.

---

## Index Sets & Parameters

**Index Sets:**
- $t \in \{1, 2, 3, 4\}$: Set of months (start of contract signing)
- $d \in \{1, 2, 3, 4\}$: Set of possible contract durations (in months)

**Parameters (all values extracted from problem text):**

| Parameter | Description | Values |
|-----------|-------------|--------|
| $R_t$ | Required warehouse area in month $t$ (m²) | $R_1=1500,\; R_2=1000,\; R_3=2000,\; R_4=1200$ |
| $c_d$ | Total rental fee per m² for a contract of duration $d$ months (yuan/m²) | $c_1=28,\; c_2=45,\; c_3=60,\; c_4=73$ |

> **Note on pricing structure:** The rental fee $c_d$ is the **total** cost per square meter over the entire $d$-month contract period (not a per-month rate). This is confirmed by the fact that $c_d$ is strictly increasing with $d$ while the marginal cost per additional month decreases (28 → 17 → 15 → 13 yuan/m² per month), reflecting the discount for longer commitments.

**Valid contract start-duration pairs:**
A contract of duration $d$ started at month $t$ is only feasible if $t + d - 1 \leq 4$, i.e., it ends within the planning horizon. Valid pairs $(t, d)$:
- $t=1$: $d \in \{1, 2, 3, 4\}$
- $t=2$: $d \in \{1, 2, 3\}$
- $t=3$: $d \in \{1, 2\}$
- $t=4$: $d \in \{1\}$

---

## Decision Variables

Let $x_{t,d}$ = amount of warehouse space (in m²) rented via a contract of duration $d$ months, signed at the beginning of month $t$.

**Domain:**
$$x_{t,d} \geq 0 \quad \forall (t,d) \in \{(1,1),(1,2),(1,3),(1,4),(2,1),(2,2),(2,3),(3,1),(3,2),(4,1)\}$$

Total: **10 continuous variables.**

---

## Objective Function

**MINIMIZE** total rental cost:

$$\min \; Z = \sum_{t=1}^{4} \sum_{d=1}^{4-d_{\min}(t)} c_d \cdot x_{t,d}$$

where the inner sum runs only over valid durations for month $t$. Explicitly:

$$Z = 28\,x_{1,1} + 45\,x_{1,2} + 60\,x_{1,3} + 73\,x_{1,4} + 45\,x_{2,2} + 60\,x_{2,3} + 28\,x_{2,1} + 60\,x_{3,2} + 28\,x_{3,1} + 28\,x_{4,1}$$

Rearranged by cost coefficient:

$$Z = 28(x_{1,1} + x_{2,1} + x_{3,1} + x_{4,1}) + 45(x_{1,2} + x_{2,2}) + 60(x_{1,3} + x_{2,3} + x_{3,2}) + 73(x_{1,4})$$

---

## Operational Constraints

**Warehouse coverage constraints:** For each month $m \in \{1, 2, 3, 4\}$, the total space available from all active contracts must meet or exceed the required area $R_m$.

A contract $(t,d)$ is **active** in month $m$ if and only if $t \leq m \leq t + d - 1$.

**Month 1** ($m=1$): Contracts active are those with $t=1$ and $d \geq 1$.
$$x_{1,1} + x_{1,2} + x_{1,3} + x_{1,4} \geq 1500$$

**Month 2** ($m=2$): Contracts active are $(1,d)$ with $d \geq 2$, and $(2,d)$ with $d \geq 1$.
$$x_{1,2} + x_{1,3} + x_{1,4} + x_{2,1} + x_{2,2} + x_{2,3} \geq 1000$$

**Month 3** ($m=3$): Contracts active are $(1,d)$ with $d \geq 3$, $(2,d)$ with $d \geq 2$, and $(3,d)$ with $d \geq 1$.
$$x_{1,3} + x_{1,4} + x_{2,2} + x_{2,3} + x_{3,1} + x_{3,2} \geq 2000$$

**Month 4** ($m=4$): Contracts active are $(1,4)$, $(2,3)$, $(3,2)$, and $(4,1)$.
$$x_{1,4} + x_{2,3} + x_{3,2} + x_{4,1} \geq 1200$$

---

## Complete Formulation (Summary)

$$\min \; Z = 28\sum_{t=1}^{4}x_{t,1} + 45(x_{1,2}+x_{2,2}) + 60(x_{1,3}+x_{2,3}+x_{3,2}) + 73\,x_{1,4}$$

subject to:

$$
\begin{aligned}
&x_{1,1} + x_{1,2} + x_{1,3} + x_{1,4} \geq 1500 \\
&x_{1,2} + x_{1,3} + x_{1,4} + x_{2,1} + x_{2,2} + x_{2,3} \geq 1000 \\
&x_{1,3} + x_{1,4} + x_{2,2} + x_{2,3} + x_{3,1} + x_{3,2} \geq 2000 \\
&x_{1,4} + x_{2,3} + x_{3,2} + x_{4,1} \geq 1200 \\
&x_{t,d} \geq 0 \quad \forall (t,d)
\end{aligned}
$$

---

## Feasibility Sanity Check

- **Total required space over 4 months:** $1500 + 1000 + 2000 + 1200 = 5700$ m²-months.
- **Cheapest option:** 1-month contracts at 28 yuan/m² each. Total cost if all met by 1-month contracts: $28 \times 5700 = 159{,}600$ yuan.
- **Most expensive option:** 4-month contract at 73 yuan/m² covers 4 m²-months. Effective rate: $73/4 = 18.25$ yuan/m²/month, which is cheaper per month than the 1-month rate (28). So longer contracts are strictly more economical per month, making the problem well-posed with a bounded optimal solution.
- **Feasibility:** The constraints are clearly feasible (e.g., rent exactly $R_m$ via 1-month contracts each month satisfies all constraints).

## Objective Unit Verification

The objective is in **yuan** (total rental cost). The problem asks to "minimize the total rental cost," so the objective is an absolute total, not a per-unit or normalized quantity. No normalization is needed. The magnitude (~100,000–160,000 yuan) is consistent with renting ~1,000–2,000 m² for several months at rates of 28–73 yuan/m².