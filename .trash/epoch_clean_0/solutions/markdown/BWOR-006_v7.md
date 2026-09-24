# Model Type: LP (Linear Programming)

## Index Sets & Parameters

**Sets:**
- $P = \{I, II, III\}$: Set of products.
- $M_A = \{A_1, A_2\}$: Set of machines for Stage A.
- $M_B = \{B_1, B_2, B_3\}$: Set of machines for Stage B.
- $M = M_A \cup M_B$: Set of all machines.

**Parameters (from Table 1-18):**

Let $t_{m,p}$ denote the processing time (hours) for product $p$ on machine $m$. If a product cannot be processed on a machine, $t_{m,p} = \infty$ (or the variable is restricted to 0).

| Machine $m$ | $t_{m,I}$ | $t_{m,II}$ | $t_{m,III}$ | Available Hours $H_m$ | Cost $c_m$ ($/hr) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| $A_1$ | 5 | 10 | - | 6,000 | 0.05 |
| $A_2$ | 7 | 9 | 12 | 10,000 | 0.03 |
| $B_1$ | 6 | 8 | - | 4,000 | 0.06 |
| $B_2$ | 4 | - | 11 | 7,000 | 0.11 |
| $B_3$ | 7 | - | - | 4,000 | 0.05 |

**Other Parameters:**
- Raw Material Cost $r_p$ ($/unit):
  - $r_I = 0.25$
  - $r_{II} = 0.35$
  - $r_{III} = 0.50$
- Selling Price $s_p$ ($/unit):
  - $s_I = 1.25$
  - $s_{II} = 2.00$
  - $s_{III} = 2.80$

**Processing Route Logic:**
- **Product I**:
  - Stage A: Can use $A_1$ or $A_2$.
  - Stage B: Can use $B_1$, $B_2$, or $B_3$.
- **Product II**:
  - Stage A: Can use $A_1$ or $A_2$.
  - Stage B: Can use $B_1$ only.
- **Product III**:
  - Stage A: Can use $A_2$ only.
  - Stage B: Can use $B_2$ only.

## Decision Variables

Let $x_{m,p}$ be the number of units of product $p$ processed on machine $m$.
- $x_{m,p}$ is **CONTINUOUS** and $\ge 0$ for all valid pairs $(m,p)$.
- $x_{m,p}$ is fixed at 0 (or excluded from the model) for invalid pairs.

Specifically, we define the following non-zero variables:
- **Stage A:**
  - $x_{A_1, I}, x_{A_1, II}$
  - $x_{A_2, I}, x_{A_2, II}, x_{A_2, III}$
- **Stage B:**
  - $x_{B_1, I}, x_{B_1, II}$
  - $x_{B_2, I}, x_{B_2, III}$
  - $x_{B_3, I}$

*Note: Since every unit of a product must pass through exactly one Stage A machine and exactly one Stage B machine, we must ensure flow conservation. However, in this specific "production planning" context where we are maximizing profit based on final output, it is more standard to define variables based on the **final output** of each product and allocate the processing costs. But because costs are per machine-hour, we need to know *which* machines are used to calculate the total processing cost. Therefore, defining variables per machine-product pair is the correct approach to capture the cost structure accurately.*

To ensure that the units processed in Stage A match the units processed in Stage B for each product, we introduce auxiliary logic or simply define the variables such that the sum of Stage A units equals the sum of Stage B units for each product.

Let $X_p$ be the total production of product $p$.
$X_p = \sum_{m \in M_A} x_{m,p} = \sum_{m \in M_B} x_{m,p}$.

Actually, a cleaner formulation for LP is to keep the split variables and add equality constraints to balance the flow for each product between Stage A and Stage B.

**Revised Decision Variables:**
- $x_{m,p} \ge 0$: Number of units of product $p$ processed on machine $m$.
  - Valid $(m,p)$ pairs are those where processing is possible.

## Objective Function

Maximize Total Profit = Total Revenue - Total Raw Material Cost - Total Processing Cost.

$$
\text{Maximize } Z = \sum_{p \in P} (s_p \cdot X_p) - \sum_{p \in P} (r_p \cdot X_p) - \sum_{m \in M} (c_m \cdot \sum_{p \in P} t_{m,p} \cdot x_{m,p})
$$

Where $X_p$ is the total production of product $p$. Since $X_p$ is determined by the flow balance, we can substitute $X_p = \sum_{m \in M_A} x_{m,p}$ (or the B side, they are equal).

Substituting $X_p = \sum_{m' \in M_A} x_{m',p}$:

$$
Z = \sum_{p \in P} (s_p - r_p) \left( \sum_{m' \in M_A} x_{m',p} \right) - \sum_{m \in M} \sum_{p \in P} c_m \cdot t_{m,p} \cdot x_{m,p}
$$

Let's calculate the coefficient for each variable $x_{m,p}$ in the objective function.
Profit per unit of product $p$ (before machine processing cost) is $\pi_p = s_p - r_p$.
- $\pi_I = 1.25 - 0.25 = 1.00$
- $\pi_{II} = 2.00 - 0.35 = 1.65$
- $\pi_{III} = 2.80 - 0.50 = 2.30$

The processing cost for unit $p$ on machine $m$ is $k_{m,p} = c_m \cdot t_{m,p}$.

The objective becomes:
$$
\text{Maximize } Z = \sum_{m \in M_A} \sum_{p \in P} (\pi_p - k_{m,p}) x_{m,p} - \sum_{m \in M_B} \sum_{p \in P} k_{m,p} x_{m,p}
$$
*Wait, this formulation double counts the profit if we sum over both A and B. The profit $\pi_p$ is realized once per unit produced. The processing cost is incurred on both A and B.*

Correct Objective Formulation:
$$
\text{Maximize } Z = \sum_{p \in P} \pi_p X_p - \sum_{m \in M} \sum_{p \in P} k_{m,p} x_{m,p}
$$
Subject to flow balance: $\sum_{m \in M_A} x_{m,p} = X_p$ and $\sum_{m \in M_B} x_{m,p} = X_p$.

To make this a single LP without auxiliary $X_p$ variables, we can express the revenue term using the Stage A variables (since $X_p = \sum_{m \in M_A} x_{m,p}$):

$$
\text{Maximize } Z = \sum_{m \in M_A} \sum_{p \in P} \pi_p x_{m,p} - \sum_{m \in M} \sum_{p \in P} k_{m,p} x_{m,p}
$$

Let's expand the coefficients for the final LP formulation.

**Coefficients for Stage A Variables ($x_{m,p}$ for $m \in M_A$):**
Contribution = $\pi_p - k_{m,p} = (s_p - r_p) - c_m t_{m,p}$

- **Product I:**
  - $x_{A_1, I}$: $1.00 - (0.05 \times 5) = 1.00 - 0.25 = 0.75$
  - $x_{A_2, I}$: $1.00 - (0.03 \times 7) = 1.00 - 0.21 = 0.79$
- **Product II:**
  - $x_{A_1, II}$: $1.65 - (0.05 \times 10) = 1.65 - 0.50 = 1.15$
  - $x_{A_2, II}$: $1.65 - (0.03 \times 9) = 1.65 - 0.27 = 1.38$
- **Product III:**
  - $x_{A_2, III}$: $2.30 - (0.03 \times 12) = 2.30 - 0.36 = 1.94$

**Coefficients for Stage B Variables ($x_{m,p}$ for $m \in M_B$):**
Contribution = $-k_{m,p} = -c_m t_{m,p}$ (Revenue is already accounted for in Stage A variables)

- **Product I:**
  - $x_{B_1, I}$: $-(0.06 \times 6) = -0.36$
  - $x_{B_2, I}$: $-(0.11 \times 4) = -0.44$
  - $x_{B_3, I}$: $-(0.05 \times 7) = -0.35$
- **Product II:**
  - $x_{B_1, II}$: $-(0.06 \times 8) = -0.48$
- **Product III:**
  - $x_{B_2, III}$: $-(0.11 \times 11) = -1.21$

**Final Objective Function:**
$$
\begin{aligned}
\text{Maximize } Z = \ & 0.75 x_{A_1, I} + 0.79 x_{A_2, I} + 1.15 x_{A_1, II} + 1.38 x_{A_2, II} + 1.94 x_{A_2, III} \\
& - 0.36 x_{B_1, I} - 0.44 x_{B_2, I} - 0.35 x_{B_3, I} - 0.48 x_{B_1, II} - 1.21 x_{B_2, III}
\end{aligned}
$$

## Operational Constraints

### 1. Flow Balance Constraints
For each product $p$, the total units processed in Stage A must equal the total units processed in Stage B.

- **Product I:**
  $$ x_{A_1, I} + x_{A_2, I} = x_{B_1, I} + x_{B_2, I} + x_{B_3, I} $$
- **Product II:**
  $$ x_{A_1, II} + x_{A_2, II} = x_{B_1, II} $$
- **Product III:**
  $$ x_{A_2, III} = x_{B_2, III} $$

### 2. Machine Capacity Constraints
For each machine $m$, the total processing time used must not exceed the available hours $H_m$.

- **Machine $A_1$** (Capacity: 6,000 h):
  $$ 5 x_{A_1, I} + 10 x_{A_1, II} \le 6000 $$
- **Machine $A_2$** (Capacity: 10,000 h):
  $$ 7 x_{A_2, I} + 9 x_{A_2, II} + 12 x_{A_2, III} \le 10000 $$
- **Machine $B_1$** (Capacity: 4,000 h):
  $$ 6 x_{B_1, I} + 8 x_{B_1, II} \le 4000 $$
- **Machine $B_2$** (Capacity: 7,000 h):
  $$ 4 x_{B_2, I} + 11 x_{B_2, III} \le 7000 $$
- **Machine $B_3$** (Capacity: 4,000 h):
  $$ 7 x_{B_3, I} \le 4000 $$

### 3. Non-negativity Constraints
All decision variables must be non-negative.
$$ x_{m,p} \ge 0 \quad \forall m, p \text{ where processing is possible.} $$

## Summary of Model Structure

- **Model Type:** Linear Programming (LP)
- **Variables:** 10 continuous non-negative variables.
- **Objective:** Linear function maximizing profit.
- **Constraints:**
  - 3 equality constraints (flow balance).
  - 5 inequality constraints (machine capacity).
  - 10 non-negativity constraints.

This formulation ensures that production is feasible only if the units entering Stage B match those exiting Stage A, and all machine time limits are respected. The profit calculation correctly attributes revenue to the completion of the product (linked to Stage A output in the algebraic derivation, but logically equivalent to total production) and subtracts processing costs from both stages.