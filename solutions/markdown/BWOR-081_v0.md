# Production Planning Optimization Model

## Model Type: LP (Linear Programming)

### Parameter Inventory (Pre-Modeling Step)

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Material A supply | 6 | t (tonnes) | Table C-5 |
| Material B supply | 8 | t (tonnes) | Table C-5 |
| Material A price | 9.9 | thousand yuan/t | Table C-5 |
| Material B price | 6.6 | thousand yuan/t | Table C-5 |
| Product I wholesale price | 30 | thousand yuan / thousand boxes | Table C-5 |
| Product II wholesale price | 20 | thousand yuan / thousand boxes | Table C-5 |
| A per unit Product I | 1 | kg / thousand boxes | Table C-5 |
| B per unit Product I | 2 | kg / thousand boxes | Table C-5 |
| A per unit Product II | 2 | kg / thousand boxes | Table C-5 |
| B per unit Product II | 1 | kg / thousand boxes | Table C-5 |
| Max sales of Product II | 2 | thousand boxes | Problem text |
| Max excess of II over I | 1 | thousand boxes | Problem text |

**Unit Conversion:**
- Material supply is in tonnes (t). 1 t = 1000 kg.
- Consumption is in kg per thousand boxes.
- Therefore, supply in kg: A = 6,000 kg; B = 8,000 kg.
- Decision variables are in thousand boxes, so consumption in kg = (kg/thousand boxes) × (thousand boxes).
- Revenue is in thousand yuan.

**Note on Material Prices:** The material prices (9.9 and 6.6 thousand yuan/t) are provided in the table. However, the objective asks for **maximum wholesale revenue**, not profit. Wholesale revenue is simply the sales revenue from selling the two products. Material costs would only enter the objective if the problem asked for **profit** (revenue − cost). Since the task explicitly says "maximum possible wholesale revenue," material prices are contextual data not needed in the objective function.

---

## Index Sets & Parameters

**Index Sets:**
- $P = \{I, II\}$: set of products
- $R = \{A, B\}$: set of raw materials

**Parameters (all values extracted from problem text):**

| Symbol | Description | Value | Unit |
|--------|-------------|-------|------|
| $a_{A,I}$ | Material A consumption per unit of Product I | 1 | kg / thousand boxes |
| $a_{A,II}$ | Material A consumption per unit of Product II | 2 | kg / thousand boxes |
| $a_{B,I}$ | Material B consumption per unit of Product I | 2 | kg / thousand boxes |
| $a_{B,II}$ | Material B consumption per unit of Product II | 1 | kg / thousand boxes |
| $S_A$ | Monthly supply of Material A | 6000 | kg |
| $S_B$ | Monthly supply of Material B | 8000 | kg |
| $p_I$ | Wholesale price of Product I | 30 | thousand yuan / thousand boxes |
| $p_{II}$ | Wholesale price of Product II | 20 | thousand yuan / thousand boxes |
| $U_{II}$ | Upper bound on sales of Product II | 2 | thousand boxes |
| $D_{diff}$ | Max allowed excess of II over I | 1 | thousand boxes |

---

## Decision Variables

| Variable | Description | Domain |
|----------|-------------|--------|
| $x_I$ | Monthly production/sales volume of Product I | $x_I \geq 0$, continuous |
| $x_{II}$ | Monthly production/sales volume of Product II | $x_{II} \geq 0$, continuous |

Both variables are continuous (production can be fractional in aggregate planning context, measured in thousand boxes).

---

## Objective Function

**MAXIMIZE** Wholesale Revenue:

$$\max \quad Z = 30 \, x_I + 20 \, x_{II}$$

**Objective Parameter Cross-Reference:**
- $p_I = 30$: Found in Table C-5, "Wholesale Price" row, column I. ✓
- $p_{II} = 20$: Found in Table C-5, "Wholesale Price" row, column II. ✓

**Magnitude Sanity Check:** If we produce 1 thousand boxes of I and 1 thousand boxes of II, revenue = 30 + 20 = 50 thousand yuan. This is a reasonable scale for the answer (tens of thousand yuan). ✓

---

## Operational Constraints

### 1. Raw Material A Constraint
Total A used ≤ Supply of A:
$$1 \cdot x_I + 2 \cdot x_{II} \leq 6000$$

### 2. Raw Material B Constraint
Total B used ≤ Supply of B:
$$2 \cdot x_I + 1 \cdot x_{II} \leq 8000$$

### 3. Market Demand Constraint for Product II
Monthly sales of Product II do not exceed 2 thousand boxes:
$$x_{II} \leq 2$$

### 4. Sales Volume Difference Constraint
Sales volume of Product II does not exceed that of Product I by more than 1 thousand boxes, i.e., $x_{II} - x_I \leq 1$:
$$x_{II} - x_I \leq 1$$

### 5. Non-negativity
$$x_I \geq 0, \quad x_{II} \geq 0$$

---

## Feasibility Sanity Check

- Constraint 3 limits $x_{II} \leq 2$.
- Constraint 4 then limits $x_I \geq x_{II} - 1$, so $x_I \geq -1$ (redundant with $x_I \geq 0$ when $x_{II} \leq 2$).
- Material constraints: With $x_{II} \leq 2$ and $x_I \geq 0$:
  - A: $x_I + 2x_{II} \leq 6000$ → easily satisfied since max LHS ≈ $x_I + 4$.
  - B: $2x_I + x_{II} \leq 8000$ → easily satisfied.
- The binding constraints will be the market constraints (3 and 4), not the material constraints.
- Feasible region is non-empty (e.g., $x_I = 0, x_{II} = 0$ is feasible). ✓

**Aggregate Check:** Total material demand at the market-constraint boundary ($x_I = 1, x_{II} = 2$): A = 1 + 4 = 5 kg, B = 2 + 2 = 4 kg. Both far below supplies of 6000 and 8000 kg. Material constraints are non-binding. The problem is feasible and the optimum will be determined by the market constraints.

---

## Complete Formulation Summary

$$\max \quad Z = 30 x_I + 20 x_{II}$$

$$\text{subject to:}$$
$$x_I + 2 x_{II} \leq 6000 \quad \text{(Material A)}$$
$$2 x_I + x_{II} \leq 8000 \quad \text{(Material B)}$$
$$x_{II} \leq 2 \quad \text{(Market cap on II)}$$
$$-x_I + x_{II} \leq 1 \quad \text{(II does not exceed I by more than 1)}$$
$$x_I \geq 0, \quad x_{II} \geq 0$$