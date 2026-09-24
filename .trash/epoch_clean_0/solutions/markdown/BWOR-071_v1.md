# Optimization Model: Machine Tool Production Profit Maximization

## 1. Problem Analysis & Pre-processing

*   **Objective:** Maximize Total Profit.
    *   Note: The problem provides "costs" and "selling prices". Profit = Total Revenue - Total Cost.
    *   The problem states the machine *must* operate 5 hours. This implies a capacity constraint that is likely binding (equality) or a hard limit. Given "must operate 5 hours", we treat the total time used as exactly 5 hours (or $\le 5$ with the implication that using more time generates profit, so it will be fully utilized. However, strictly speaking, "must operate" implies $x_1 + x_2 = 5$). Let's verify if producing 5 units is optimal. Since marginal profit might drop, we should check if the constraint is an equality or inequality. Usually, "available working time" implies $\le$. But "must operate 5 hours" is a specific instruction. Let's look at the profit function. If marginal profit becomes negative, we would prefer to produce less. However, standard interpretation of "machine has 5 hours available" is a capacity constraint ($\le$). The phrase "must operate 5 hours" is slightly ambiguous. Let's re-read carefully: "A machine tool has 5 hours of available working time per day... If the machine must operate 5 hours per day". This strongly suggests an equality constraint on time usage: $x_1 + x_2 = 5$.
    *   *Correction/Refinement:* In many textbook OR problems, "must operate" implies the machine is paid for or has a fixed commitment, so you *must* fill the time. Let's assume $x_1 + x_2 = 5$. If it were just "available", it would be $\le$. Given the explicit "must operate 5 hours", I will model it as an equality constraint.

*   **Revenue Function:**
    *   Product A: $R_1 = x_1 \cdot p_1 = x_1(12 - x_1) = 12x_1 - x_1^2$
    *   Product B: $R_2 = x_2 \cdot p_2 = x_2(13 - 2x_2) = 13x_2 - 2x_2^2$
    *   Total Revenue $R(x_1, x_2) = 12x_1 - x_1^2 + 13x_2 - 2x_2^2$

*   **Cost Function:**
    *   Cost A: $4x_1$
    *   Cost B: $3x_2$
    *   Total Cost $C(x_1, x_2) = 4x_1 + 3x_2$

*   **Profit Function ($Z$):**
    *   $Z = R - C = (12x_1 - x_1^2 + 13x_2 - 2x_2^2) - (4x_1 + 3x_2)$
    *   $Z = -x_1^2 + 8x_1 - 2x_2^2 + 10x_2$

*   **Variable Domain:**
    *   $x_1, x_2$ represent quantities of products. The problem does not explicitly state if they must be integers. However, "units" often implies discrete counts. But demand functions $p=12-x$ are continuous linear approximations often used in continuous optimization contexts. Let's check the nature of the problem. If $x$ must be integer, this is a Non-Linear Integer Program (NLP/UNLP). If $x$ can be continuous, it is a Non-Linear Program (NLP).
    *   Standard textbook problems with linear demand curves like $p = a - bx$ usually allow continuous variables unless "integer units" is explicitly stressed or the numbers are small enough to check manually. Given the quadratic objective, this is a **Quadratic Programming (QP)** problem if continuous, or a **Non-Linear Integer Program** if discrete.
    *   Let's look at the coefficients. $x_1, x_2$ are "units". Usually, in such economic models, unless specified "integer", we treat them as continuous for the derivation, but the final answer should be interpreted. However, "how many units" often implies integers. Let's assume **Continuous** variables first to find the optimal point, then check if rounding is necessary or if the problem implies integer constraints. *Self-Correction*: The prompt asks for a formal model. I will define them as **Continuous** variables because the demand functions are linear and defined for real numbers, which is standard for this type of profit maximization problem in operations research textbooks (often solved via calculus or KKT conditions). If integer constraints were required, the problem would typically specify "integer units". I will add a note about integrality. *Actually*, looking at typical OR problems of this specific style (linear price, quadratic profit), they are often treated as continuous. I will define $x_1, x_2 \in \mathbb{R}_+$.

## 2. Mathematical Model

### Index Sets & Parameters

**Parameters:**
*   $T = 5$: Total available/required machine time (hours)
*   $t_1 = 1$: Time per unit of Product A (hours/unit)
*   $t_2 = 1$: Time per unit of Product B (hours/unit)
*   $c_1 = 4$: Production cost per unit of Product A (yuan/unit)
*   $c_2 = 3$: Production cost per unit of Product B (yuan/unit)
*   $a_1 = 12, b_1 = 1$: Parameters for Product A price function $p_1 = a_1 - b_1 x_1$
*   $a_2 = 13, b_2 = 2$: Parameters for Product B price function $p_2 = a_2 - b_2 x_2$

**Derived Parameters:**
*   Profit coefficients for the quadratic objective function:
    *   $A_1 = -1$ (coefficient of $x_1^2$)
    *   $B_1 = 12 - 4 = 8$ (coefficient of $x_1$)
    *   $A_2 = -2$ (coefficient of $x_2^2$)
    *   $B_2 = 13 - 3 = 10$ (coefficient of $x_2$)

### Decision Variables

Let:
*   $x_1$: Quantity of Product A produced (units)
*   $x_2$: Quantity of Product B produced (units)

**Domains:**
*   $x_1 \ge 0$
*   $x_2 \ge 0$
*   *(Note: If discrete units are strictly required, $x_1, x_2 \in \mathbb{Z}_{\ge 0}$. Based on the continuous nature of the demand curves, continuous variables are the standard formulation.)*

### Objective Function

Maximize Total Profit $Z$:

$$
\text{Maximize } Z = (12x_1 - x_1^2) - 4x_1 + (13x_2 - 2x_2^2) - 3x_2
$$

Simplified:
$$
\text{Maximize } Z = -x_1^2 + 8x_1 - 2x_2^2 + 10x_2
$$

### Operational Constraints

**1. Machine Time Constraint:**
The problem states the machine *must* operate 5 hours.
$$
1x_1 + 1x_2 = 5
$$

**2. Non-negativity Constraints:**
$$
x_1 \ge 0
$$
$$
x_2 \ge 0
$$

**3. Price Positivity (Implicit/Valid Range):**
Prices must be non-negative for the model to be physically meaningful (though not always strictly required as a constraint if the optimum lies within the positive price region, it is good practice to define the valid domain).
$$
12 - x_1 \ge 0 \implies x_1 \le 12
$$
$$
13 - 2x_2 \ge 0 \implies x_2 \le 6.5
$$
*(Note: Given $x_1 + x_2 = 5$, $x_1$ and $x_2$ are automatically $\le 5$, so these constraints are redundant but valid.)*

---

### Final Formal Model

$$
\begin{aligned}
\text{Maximize} \quad & Z = -x_1^2 + 8x_1 - 2x_2^2 + 10x_2 \\
\text{Subject to} \quad & x_1 + x_2 = 5 \\
& x_1 \ge 0 \\
& x_2 \ge 0
\end{aligned}
$$