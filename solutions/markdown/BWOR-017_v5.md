# Production Planning with Fixed Costs (MILP)

## MANDATORY COST INVENTORY (PRE-MODELING STEP)

Extracting every numeric value representing costs, prices, or charges:

| Parameter | Product I | Product II | Product III |
|---|---|---|---|
| Variable cost per unit | 4 | 5 | 6 |
| Fixed cost (one-time, if produced) | 100 | 150 | 200 |
| Selling price per unit | 8 | 10 | 12 |

Net contribution margin per unit (price − variable cost):
- Product I: 8 − 4 = **4**
- Product II: 10 − 5 = **5**
- Product III: 12 − 6 = **6**

These are the objective coefficients. Fixed costs are incurred only if a product is produced (binary activation).

## MANDATORY RE-SCAN

All parameters are explicitly provided in Table 5-6. Resource availability: A=500, B=300, C=100. No values are missing.

## MODEL TYPE

**MILP** (Mixed-Integer Linear Program) — continuous production quantities coupled with binary activation variables for fixed costs.

---

## Index Sets & Parameters

**Sets:**
- $P = \{1, 2, 3\}$: set of products (I, II, III)
- $R = \{1, 2, 3\}$: set of resources (A, B, C)

**Parameters (all from Table 5-6):**

| Symbol | Meaning | Values |
|---|---|---|
| $a_{r,p}$ | Unit consumption of resource $r$ per unit of product $p$ | $a_{1,\cdot}=(2,4,8),\; a_{2,\cdot}=(2,3,4),\; a_{3,\cdot}=(1,2,3)$ |
| $b_r$ | Available amount of resource $r$ | $b_1=500,\; b_2=300,\; b_3=100$ |
| $c_p$ | Variable cost per unit of product $p$ | $c=(4,5,6)$ |
| $s_p$ | Selling price per unit of product $p$ | $s=(8,10,12)$ |
| $F_p$ | Fixed cost of organizing production of product $p$ | $F=(100,150,200)$ |
| $M_p$ | Upper bound on production of product $p$ (big-M) | $M_1=250,\; M_2=75,\; M_3=33\overline{3}$ |

**Derivation of Big-M values** (tightest valid upper bounds from resource constraints, assuming a single product uses all of one resource):
- Product 1: $\min(500/2,\; 300/2,\; 100/1) = \min(250, 150, 100) = 100$. But we need a safe M; use the tightest single-resource bound: $M_1 = 100$ (from resource C). Actually, to be safe and tight: $M_1 = \min(250, 150, 100) = 100$.
- Product 2: $\min(500/4,\; 300/3,\; 100/2) = \min(125, 100, 50) = 50$. So $M_2 = 50$.
- Product 3: $\min(500/8,\; 300/4,\; 100/3) = \min(62.5, 75, 33.\overline{3}) = 33.\overline{3}$. So $M_3 = 100/3 \approx 33.333$.

We use these tight M values.

## Decision Variables

- $x_p \geq 0$, **continuous**, $\forall p \in P$: production quantity of product $p$.
- $y_p \in \{0, 1\}$, **binary**, $\forall p \in P$: $y_p = 1$ if product $p$ is produced (fixed cost incurred), $0$ otherwise.

## Objective Function

**MAXIMIZE** total profit:

$$\max \quad \sum_{p \in P} (s_p - c_p)\, x_p \;-\; \sum_{p \in P} F_p\, y_p$$

Expanded:

$$\max \quad 4\,x_1 + 5\,x_2 + 6\,x_3 \;-\; 100\,y_1 - 150\,y_2 - 200\,y_3$$

## Operational Constraints

### 1. Resource Availability Constraints (for each resource $r \in R$)

$$\sum_{p \in P} a_{r,p}\, x_p \;\leq\; b_r, \quad \forall\, r \in R$$

Explicitly:
- Resource A: $\quad 2x_1 + 4x_2 + 8x_3 \;\leq\; 500$
- Resource B: $\quad 2x_1 + 3x_2 + 4x_3 \;\leq\; 300$
- Resource C: $\quad x_1 + 2x_2 + 3x_3 \;\leq\; 100$

### 2. Linking Constraints (Fixed Cost Activation, for each product $p \in P$)

$$x_p \;\leq\; M_p\, y_p, \quad \forall\, p \in P$$

Explicitly:
- $x_1 \;\leq\; 100\, y_1$
- $x_2 \;\leq\; 50\, y_2$
- $x_3 \;\leq\; 33.333\, y_3$  (i.e., $x_3 \leq \frac{100}{3}\, y_3$)

### 3. Variable Bounds

$$x_p \;\geq\; 0, \quad \forall\, p \in P$$

$$y_p \;\in\; \{0, 1\}, \quad \forall\, p \in P$$

## FEASIBILITY SANITY CHECK

- If only Product 1 is produced: max $x_1 = \min(250, 150, 100) = 100$. Profit = $4(100) - 100 = 300 > 0$. ✓
- If only Product 2 is produced: max $x_2 = \min(125, 100, 50) = 50$. Profit = $5(50) - 150 = 100 > 0$. ✓
- If only Product 3 is produced: max $x_3 = \min(62.5, 75, 33.\overline{3}) = 33.\overline{3}$. Profit = $6(33.\overline{3}) - 200 = 200 - 200 = 0$. Break-even. ✓
- All three together are constrained by resource C most tightly. The model is feasible (e.g., $x=0, y=0$ is trivially feasible with profit 0).

## OBJECTIVE PARAMETER CROSS-REFERENCE

| Parameter in Objective | Value | Source |
|---|---|---|
| $s_1 - c_1 = 4$ | ✓ | Table: price 8, var. cost 4 |
| $s_2 - c_2 = 5$ | ✓ | Table: price 10, var. cost 5 |
| $s_3 - c_3 = 6$ | ✓ | Table: price 12, var. cost 6 |
| $F_1 = 100$ | ✓ | Table: fixed cost row |
| $F_2 = 150$ | ✓ | Table: fixed cost row |
| $F_3 = 200$ | ✓ | Table: fixed cost row |

All objective parameters are confirmed present. No [NOT_PROVIDED] values.