## Mathematical Model Formulation

### Model Type: **LP** (Linear Program)

All decision variables are continuous (production quantities can be fractional in the aggregate sense; the problem does not require integrality).

---

### MANDATORY COST INVENTORY (PRE-MODELING STEP)

| Numeric Value | Entity | Role |
|---|---|---|
| 2 yuan | 1 bundle of manuscript paper | Profit coefficient (objective) |
| 3 yuan | 1 dozen of diaries | Profit coefficient (objective) |
| 1 yuan | 1 box of exercise books | Profit coefficient (objective) |
| 30 bundles/person/month | Labor productivity – manuscript paper | Constraint coefficient |
| 30 dozens/person/month | Labor productivity – diaries | Constraint coefficient |
| 30 boxes/person/month | Labor productivity – exercise books | Constraint coefficient |
| 100 persons | Total labor supply | Constraint RHS |
| 30,000 kg | Monthly paper supply | Constraint RHS |
| 10/3 kg (≈3.333) | Paper per bundle of manuscript paper | Constraint coefficient |
| 40/3 kg (≈13.333) | Paper per dozen of diaries | Constraint coefficient |
| 80/3 kg (≈26.667) | Paper per box of exercise books | Constraint coefficient |

All three objective parameters (2, 3, 1) are located in the text. No parameter is missing.

---

### Index Sets & Parameters

**Index Sets:**
- $j \in J = \{1, 2, 3\}$: product types, where
  - $j=1$: manuscript paper (unit: bundle)
  - $j=2$: diaries (unit: dozen)
  - $j=3$: exercise books (unit: box)

**Parameters:**

| Symbol | Value | Description |
|---|---|---|
| $p_1$ | 2 | Profit per bundle of manuscript paper (yuan) |
| $p_2$ | 3 | Profit per dozen of diaries (yuan) |
| $p_3$ | 1 | Profit per box of exercise books (yuan) |
| $L$ | 100 | Total available workers (persons) |
| $P$ | 30,000 | Total available white base paper (kg) |
| $\ell_1$ | 30 | Labor productivity: bundles per person per month |
| $\ell_2$ | 30 | Labor productivity: dozens per person per month |
| $\ell_3$ | 30 | Labor productivity: boxes per person per month |
| $m_1$ | $\frac{10}{3}$ | Paper consumption per bundle of manuscript paper (kg) |
| $m_2$ | $\frac{40}{3}$ | Paper consumption per dozen of diaries (kg) |
| $m_3$ | $\frac{80}{3}$ | Paper consumption per box of exercise books (kg) |

---

### Decision Variables

| Variable | Domain | Description |
|---|---|---|
| $x_1$ | $x_1 \geq 0$, continuous | Monthly production quantity of manuscript paper (bundles) |
| $x_2$ | $x_2 \geq 0$, continuous | Monthly production quantity of diaries (dozens) |
| $x_3$ | $x_3 \geq 0$, continuous | Monthly production quantity of exercise books (boxes) |

---

### Objective Function

**MAXIMIZE** total monthly profit (yuan):

$$\max \quad Z = 2\,x_1 + 3\,x_2 + 1\,x_3$$

---

### Operational Constraints

**1. Labor constraint** (total worker-months consumed ≤ 100):

Each person can produce 30 units of any single product type per month. The labor required (in person-months) for product $j$ is $x_j / \ell_j$.

$$\frac{x_1}{30} + \frac{x_2}{30} + \frac{x_3}{30} \;\leq\; 100$$

Equivalently (multiplying through by 30):

$$x_1 + x_2 + x_3 \;\leq\; 3000$$

**2. Raw material constraint** (total paper consumed ≤ 30,000 kg):

$$\frac{10}{3}\,x_1 \;+\; \frac{40}{3}\,x_2 \;+\; \frac{80}{3}\,x_3 \;\leq\; 30000$$

Equivalently (multiplying through by 3):

$$10\,x_1 \;+\; 40\,x_2 \;+\; 80\,x_3 \;\leq\; 90000$$

**3. Non-negativity:**

$$x_1,\; x_2,\; x_3 \;\geq\; 0$$

---

### Feasibility Sanity Check

- **Labor-only bound:** If only labor were binding, max total units = 3000. The most profitable product per labor unit is diaries (3 yuan / (1/30) person = 90 yuan/person-month). Producing 3000 dozens of diaries uses $3000 \times \frac{40}{3} = 40{,}000$ kg of paper, which **exceeds** the 30,000 kg supply. So the paper constraint is binding.
- **Paper-only bound:** If only paper were binding, the most profitable product per kg is manuscript paper (2 yuan / (10/3) kg = 0.6 yuan/kg). Producing $\frac{30000}{10/3} = 9000$ bundles uses $9000/30 = 300$ person-months, which **exceeds** the 100-person labor supply. So the labor constraint is also binding.
- Both constraints are expected to be active in the optimal solution, making the problem well-posed and feasible (the origin $(0,0,0)$ is trivially feasible).

### Objective Parameter Cross-Reference

| Parameter | Value in text | ✓ |
|---|---|---|
| $p_1$ | "profit for producing one bundle of manuscript paper is 2 yuan" | ✓ |
| $p_2$ | "one dozen of diaries is 3 yuan" | ✓ |
| $p_3$ | "one box of exercise books is 1 yuan" | ✓ |

All objective coefficients are confirmed. No `[NOT_PROVIDED]` parameters.

### Magnitude Sanity Check

A greedy solution: produce only diaries (highest profit per labor unit at 90 yuan/person-month). Labor allows 3000 dozens, but paper allows only $30000 / (40/3) = 2250$ dozens. Profit = $2250 \times 3 = 6750$ yuan. This is a reasonable double-digit-to-four-digit yuan answer, consistent with the problem's scale (100 workers, 30,000 kg). No normalization division is needed — the question asks for the production plan and maximum profit in yuan.