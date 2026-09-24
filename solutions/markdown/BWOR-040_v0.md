# Operations Research Model: Production Planning with Temporary Workers

## Model Type: MILP (Mixed-Integer Linear Programming)

> **Note:** The number of temporary workers must be a non-negative integer (discrete physical units). Production quantities can be continuous (or integer depending on interpretation; here we treat them as continuous since "bundles," "dozens," "boxes" are standard units that can be fractional in aggregate planning).

## Index Sets & Parameters

**Index Sets:**
- $P = \{1, 2, 3\}$: Set of products, where $1$ = manuscript paper, $2$ = diaries, $3$ = exercise books.

**Parameters (all units converted to consistent base units):**

| Parameter | Symbol | Value | Source/Note |
|-----------|--------|-------|-------------|
| Number of permanent workers | $W$ | 100 | Given |
| Monthly supply of white base paper (kg) | $M$ | 30,000 | Given |
| Labor productivity: bundles/person/month (product 1) | $L_1$ | 30 | Given |
| Labor productivity: dozens/person/month (product 2) | $L_2$ | 30 | Given |
| Labor productivity: boxes/person/month (product 3) | $L_3$ | 30 | Given |
| Material consumption: kg/bundle (product 1) | $R_1$ | $3\tfrac{1}{3} = 10/3$ | Given |
| Material consumption: kg/dozen (product 2) | $R_2$ | $13\tfrac{1}{3} = 40/3$ | Given |
| Material consumption: kg/box (product 3) | $R_3$ | $26\tfrac{2}{3} = 80/3$ | Given |
| Profit: yuan/bundle (product 1) | $\pi_1$ | 2 | Given |
| Profit: yuan/dozen (product 2) | $\pi_2$ | 3 | Given |
| Profit: yuan/box (product 3) | $\pi_3$ | 1 | Given |
| Wage cost per temporary worker per month (yuan) | $C_T$ | 40 | Given |

## Decision Variables

- $x_p \geq 0$, continuous, $\forall p \in P$: Monthly production quantity of product $p$ (in its respective unit: bundles, dozens, boxes).
- $T \geq 0$, **integer**: Number of temporary workers to hire per month.

## Objective Function

Maximize net profit:

$$\max \quad Z = 2x_1 + 3x_2 + 1x_3 - 40T$$

## Operational Constraints

### 1. Labor Capacity Constraint
Each product requires labor proportional to its output. With $W + T$ total workers, the total labor capacity (worker-months) is $W + T$. The labor required for each product is $x_p / L_p$ worker-months (since one worker produces $L_p$ units per month).

$$\frac{x_1}{30} + \frac{x_2}{30} + \frac{x_3}{30} \leq 100 + T$$

Equivalently:
$$x_1 + x_2 + x_3 \leq 30(100 + T) = 3000 + 30T$$

### 2. Raw Material Constraint
Total white base paper consumed must not exceed the monthly supply:

$$\frac{10}{3}x_1 + \frac{40}{3}x_2 + \frac{80}{3}x_3 \leq 30000$$

Equivalently (multiply by 3):
$$10x_1 + 40x_2 + 80x_3 \leq 90000$$

### 3. Non-negativity and Integrality
$$x_p \geq 0, \quad \forall p \in P$$
$$T \geq 0, \quad T \in \mathbb{Z}$$

## Feasibility Sanity Check

- **Without temporary workers ($T=0$):** Labor capacity = 3000 units (sum of outputs), Material capacity allows up to 9000 units of the lightest product. The binding constraint depends on the product mix.
- **With temporary workers:** Each additional worker adds 30 units of labor capacity at a cost of 40 yuan. The marginal profit per unit of labor capacity must exceed $40/30 \approx 1.33$ yuan/unit to justify hiring.
  - Product 1: profit per labor-unit = $2/1 = 2$ yuan → justifies hiring
  - Product 2: profit per labor-unit = $3/1 = 3$ yuan → justifies hiring
  - Product 3: profit per labor-unit = $1/1 = 1$ yuan → does NOT justify hiring (below 1.33)
- The model will determine the optimal $T$ by balancing the marginal gain from additional labor against the wage cost, subject to the material constraint.

## Parameter Completeness Verification

| Parameter Symbol | Value | Located in Text? |
|-----------------|-------|-----------------|
| $W$ | 100 | ✅ "100 workers" |
| $M$ | 30,000 | ✅ "30,000 kg" |
| $L_1, L_2, L_3$ | 30, 30, 30 | ✅ "each person per month can produce 30 bundles... 30 dozens... 30 boxes" |
| $R_1$ | $10/3$ | ✅ "$3\tfrac{1}{3}$ kg" |
| $R_2$ | $40/3$ | ✅ "$13\tfrac{1}{3}$ kg" |
| $R_3$ | $80/3$ | ✅ "$26\tfrac{2}{3}$ kg" |
| $\pi_1, \pi_2, \pi_3$ | 2, 3, 1 | ✅ "profit... 2 yuan... 3 yuan... 1 yuan" |
| $C_T$ | 40 | ✅ "wage cost of 40 yuan per person per month" |

All parameters are explicitly provided. No [NOT_PROVIDED] values required.