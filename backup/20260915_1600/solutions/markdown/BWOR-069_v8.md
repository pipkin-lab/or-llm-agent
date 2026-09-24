# Mathematical Optimization Model

## Model Type
**MILP** (Mixed-Integer Linear Program) — The decision variables represent the number of physical pieces of each product to produce/ship, which must be non-negative integers.

## Index Sets & Parameters

**Index Set:**
- $i \in \{1, 2, 3\}$: set of product types.

**Parameters (all values extracted from Table 7-8 and problem text):**

| Parameter | Description | Values |
|-----------|-------------|--------|
| $w_i$ | Weight per piece of product $i$ (tons) | $w_1 = 2$, $w_2 = 3$, $w_3 = 4$ |
| $p_i$ | Profit per piece of product $i$ (yuan) | $p_1 = 100$, $p_2 = 140$, $p_3 = 180$ |
| $W$ | Total transportation capacity (tons) | $W = 10$ |

**MANDATORY COST INVENTORY:**
- Product 1: profit = 100 yuan/piece → objective coefficient for $x_1$
- Product 2: profit = 140 yuan/piece → objective coefficient for $x_2$
- Product 3: profit = 180 yuan/piece → objective coefficient for $x_3$

All three product entities have exactly one associated profit figure each, matching the count of decision variables. These are the objective coefficients.

**TABLE SCALE FACTOR VERIFICATION:** The table header states "Weight (t/piece)" and "Profit (yuan/piece)" — no hidden multiplier (e.g., "in hundreds" or "×10"). Values are used at face value.

## Decision Variables

- $x_i \in \mathbb{Z}_{\geq 0}$ for $i \in \{1, 2, 3\}$: number of pieces of product $i$ to produce and ship.

**Explicit Bounds:**
- $x_1 \geq 0$, integer
- $x_2 \geq 0$, integer
- $x_3 \geq 0$, integer

## Objective Function

**MAXIMIZE** total profit:

$$\max \quad Z = 100\, x_1 + 140\, x_2 + 180\, x_3$$

*Unit check:* The objective is in **yuan**, which is the natural unit of the profit figures. The problem asks to maximize profit, so $Z$ directly equals the reported answer.

## Operational Constraints

**Transportation capacity constraint (weight limit):**

$$2\, x_1 + 3\, x_2 + 4\, x_3 \leq 10$$

**Non-negativity and integrality:**

$$x_1, x_2, x_3 \in \mathbb{Z}_{\geq 0}$$

## Feasibility Sanity Check

- Total capacity: 10 tons.
- Maximum possible pieces if only Product 1: $\lfloor 10/2 \rfloor = 5$ pieces → profit = 500 yuan.
- Maximum possible pieces if only Product 3: $\lfloor 10/4 \rfloor = 2$ pieces → profit = 360 yuan.
- A mix (e.g., $x_1=2, x_2=0, x_3=1$: weight = 4+0+4 = 8 ≤ 10, profit = 200+180 = 380) is feasible.
- The feasible region is non-empty (e.g., $x_1=x_2=x_3=0$ is feasible).

**Greedy/sanity objective estimate:** The best profit-per-ton ratio is Product 1 (100/2 = 50 yuan/t), then Product 2 (140/3 ≈ 46.7 yuan/t), then Product 3 (180/4 = 45 yuan/t). A reasonable optimum is around 500 yuan (e.g., 5 × Product 1 = 500 yuan, using all 10 tons). The objective magnitude is in the hundreds of yuan, consistent with the problem scale.

**OBJECTIVE PARAMETER CROSS-REFERENCE:**
- $p_1 = 100$ ✓ (Table 7-8, row 1)
- $p_2 = 140$ ✓ (Table 7-8, row 2)
- $p_3 = 180$ ✓ (Table 7-8, row 3)

All objective parameters confirmed. No [NOT_PROVIDED] values.