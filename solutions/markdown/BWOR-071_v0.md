## Model Type
**NON-LINEAR (Quadratic Programming / QP)**

The objective function contains revenue terms that are products of decision variables (price $\times$ quantity), resulting in quadratic terms. A non-linear solver (e.g., `scipy.optimize.minimize` with SLSQP or `cvxpy` with a concave maximization formulation) is required.

---

## Index Sets & Parameters

| Symbol | Description | Value |
|--------|-------------|-------|
| $i$ | Product index, $i \in \{1, 2\}$ | 1 = Product A, 2 = Product B |
| $T$ | Total available machine time per day (hours) | 5 |
| $t_i$ | Machine time required per unit of product $i$ (hours/unit) | $t_1 = 1$, $t_2 = 1$ |
| $c_i$ | Variable production cost per unit of product $i$ (yuan/unit) | $c_1 = 4$, $c_2 = 3$ |
| $a_i$ | Intercept of the linear demand/price function for product $i$ (yuan) | $a_1 = 12$, $a_2 = 13$ |
| $b_i$ | Slope (price sensitivity) of the demand/price function for product $i$ (yuan/unit) | $b_1 = 1$, $b_2 = 2$ |

**Price functions:**
$$p_1(x_1) = 12 - x_1, \quad p_2(x_2) = 13 - 2x_2$$

---

## Decision Variables

| Variable | Description | Domain |
|----------|-------------|--------|
| $x_1$ | Number of units of Product A produced per day | Continuous, $x_1 \geq 0$ |
| $x_2$ | Number of units of Product B produced per day | Continuous, $x_2 \geq 0$ |

> **Note on integrality:** The problem does not explicitly state that $x_1, x_2$ must be integers. Since the quantities are relatively small and the price functions are linear, we treat them as continuous variables. If integer production is required, this would become a non-linear integer program; however, the standard interpretation of this classic problem is continuous.

---

## Objective Function

**MAXIMIZE** total profit:

$$\max \quad Z = \underbrace{p_1(x_1) \cdot x_1 - c_1 x_1}_{\text{Profit from A}} + \underbrace{p_2(x_2) \cdot x_2 - c_2 x_2}_{\text{Profit from B}}$$

Substituting the price functions:

$$\max \quad Z = (12 - x_1)x_1 - 4x_1 + (13 - 2x_2)x_2 - 3x_2$$

Simplified:

$$\max \quad Z = 12x_1 - x_1^2 - 4x_1 + 13x_2 - 2x_2^2 - 3x_2$$

$$\boxed{\max \quad Z = 8x_1 - x_1^2 + 10x_2 - 2x_2^2}$$

This is a **concave quadratic** objective (negative definite Hessian), so any local maximum is global.

---

## Operational Constraints

### 1. Machine Capacity Constraint (Equality)

The machine **must** operate for exactly 5 hours per day:

$$x_1 \cdot t_1 + x_2 \cdot t_2 = T$$

$$\boxed{x_1 + x_2 = 5}$$

> The problem states "the machine must operate 5 hours per day," which is an equality constraint. Each unit of A or B requires 1 hour.

### 2. Non-negativity Constraints

$$x_1 \geq 0, \quad x_2 \geq 0$$

### 3. Price Non-negativity (Implicit Feasibility)

For the price functions to represent valid selling prices (non-negative), we require:
$$p_1 = 12 - x_1 \geq 0 \implies x_1 \leq 12$$
$$p_2 = 13 - 2x_2 \geq 0 \implies x_2 \leq 6.5$$

However, given $x_1 + x_2 = 5$ and $x_1, x_2 \geq 0$, the maximum any single variable can take is 5, which is well within these bounds. Thus, these are **non-binding** and need not be added explicitly.

---

## Complete Formulation

$$
\begin{aligned}
\max_{x_1, x_2} \quad & 8x_1 - x_1^2 + 10x_2 - 2x_2^2 \\
\text{subject to} \quad & x_1 + x_2 = 5 \\
& x_1 \geq 0 \\
& x_2 \geq 0
\end{aligned}
$$

---

## Feasibility Sanity Check

- Total required capacity: 5 hours. Total available: 5 hours. $\checkmark$
- With $x_1 + x_2 = 5$ and non-negativity, the feasible region is the line segment from $(0, 5)$ to $(5, 0)$.
- At $x_1 = 5, x_2 = 0$: $Z = 8(5) - 25 + 0 = 15$
- At $x_1 = 0, x_2 = 5$: $Z = 0 + 10(5) - 2(25) = 50 - 50 = 0$
- The objective is concave, so the maximum lies at an interior point (or boundary). The model is well-posed and feasible.