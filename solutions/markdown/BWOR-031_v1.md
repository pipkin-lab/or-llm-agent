## MANDATORY COST INVENTORY (PRE-MODELING STEP)

Let me extract every numeric value that represents a cost, fee, price, rate, or income:

| # | Value | Entity | Role |
|---|-------|--------|------|
| 1 | 400 yuan | Per dairy cow (investment) | Cost (capital) |
| 2 | 3 yuan | Per chicken (investment) | Cost (capital) |
| 3 | 400 yuan | Per dairy cow | **Net income (objective coefficient)** |
| 4 | 2 yuan | Per chicken | **Net income (objective coefficient)** |
| 5 | 2.1 yuan/person-day | Spring/summer wage income | **Income (objective coefficient for unused labor)** |
| 6 | 1.8 yuan/person-day | Autumn/winter wage income | **Income (objective coefficient for unused labor)** |
| 7 | 175 yuan/hm² | Soybeans | **Net income (objective coefficient)** |
| 8 | 300 yuan/hm² | Corn | **Net income (objective coefficient)** |
| 9 | 120 yuan/hm² | Wheat | **Net income (objective coefficient)** |

All objective parameters are matched. The objective is to **maximize** annual net income.

## OBJECTIVE PARAMETER CROSS-REFERENCE

- $c_{soy} = 175$ ✓
- $c_{corn} = 300$ ✓
- $c_{wheat} = 120$ ✓
- $c_{cow} = 400$ ✓
- $c_{chicken} = 2$ ✓
- $w_{AW} = 1.8$ (wage for unused autumn/winter labor) ✓
- $w_{SS} = 2.1$ (wage for unused spring/summer labor) ✓

All confirmed from the text.

## FEASIBILITY SANITY CHECK

- Land: 100 hm² total. Cows need 1.5 hm² each, max 32 cows → max 48 hm² for forage. Remaining 52+ hm² for crops. Feasible.
- Capital: 15,000 yuan. 32 cows × 400 = 12,800. 3,000 chickens × 3 = 9,000. Total if max of both = 21,800 > 15,000. So capital is binding — not all max animals can be funded. Feasible with trade-offs.
- Labor: AW = 3,500 person-days, SS = 4,000 person-days. Cows: 32×100=3,200 AW, 32×50=1,600 SS. Chickens: 3,000×0.6=1,800 AW, 3,000×0.3=900 SS. Combined max: 5,000 AW, 2,500 SS. AW exceeds 3,500, so not all max animals + crops fit. Feasible with trade-offs.

Model is feasible.

---

# Mathematical Optimization Model

**Model Type:** MILP (Mixed-Integer Linear Program)

**Justification:** Number of dairy cows and chickens are discrete physical units (integer variables). Crop areas are continuous (land can be divided fractionally). The objective and all constraints are linear.

---

## Index Sets & Parameters

**Sets:**
- $C = \{\text{soy}, \text{corn}, \text{wheat}\}$ — crop types
- $A = \{\text{cow}, \text{chicken}\}$ — animal types

**Parameters (all values extracted from problem statement):**

| Parameter | Value | Description |
|-----------|-------|-------------|
| $L_{total}$ | 100 hm² | Total land available |
| $K$ | 15,000 yuan | Total capital available |
| $P_{AW}$ | 3,500 person-days | Autumn/winter labor supply |
| $P_{SS}$ | 4,000 person-days | Spring/summer labor supply |
| $w_{AW}$ | 1.8 yuan/person-day | Wage income for unused AW labor |
| $w_{SS}$ | 2.1 yuan/person-day | Wage income for unused SS labor |

**Crop parameters (per hm²):**

| Parameter | Soybeans | Corn | Wheat |
|-----------|----------|------|-------|
| $a^C_c$ (AW labor, person-days/hm²) | 20 | 35 | 10 |
| $a^S_c$ (SS labor, person-days/hm²) | 50 | 75 | 40 |
| $r_c$ (net income, yuan/hm²) | 175 | 300 | 120 |

**Animal parameters:**

| Parameter | Dairy Cow | Chicken |
|-----------|-----------|---------|
| $k_a$ (investment, yuan/unit) | 400 | 3 |
| $\ell_a$ (land, hm²/unit) | 1.5 | 0 |
| $b^C_a$ (AW labor, person-days/unit) | 100 | 0.6 |
| $b^S_a$ (SS labor, person-days/unit) | 50 | 0.3 |
| $r_a$ (net income, yuan/unit) | 400 | 2 |
| $U_a$ (max number) | 32 | 3,000 |

---

## Decision Variables

| Variable | Domain | Description |
|----------|--------|-------------|
| $x_{\text{soy}}$ | $\mathbb{R}_{\geq 0}$ | Hectares planted with soybeans |
| $x_{\text{corn}}$ | $\mathbb{R}_{\geq 0}$ | Hectares planted with corn |
| $x_{\text{wheat}}$ | $\mathbb{R}_{\geq 0}$ | Hectares planted with wheat |
| $y_{\text{cow}}$ | $\mathbb{Z}_{\geq 0}$ | Number of dairy cows raised |
| $y_{\text{chicken}}$ | $\mathbb{Z}_{\geq 0}$ | Number of chickens raised |
| $u_{AW}$ | $\mathbb{R}_{\geq 0}$ | Unused (external) autumn/winter labor (person-days) |
| $u_{SS}$ | $\mathbb{R}_{\geq 0}$ | Unused (external) spring/summer labor (person-days) |

**Bounds:**
$$x_{\text{soy}},\, x_{\text{corn}},\, x_{\text{wheat}} \geq 0$$
$$y_{\text{cow}} \in \{0, 1, 2, \ldots, 32\}$$
$$y_{\text{chicken}} \in \{0, 1, 2, \ldots, 3000\}$$
$$u_{AW} \geq 0, \quad u_{SS} \geq 0$$

---

## Objective Function

**MAXIMIZE** total annual net income (yuan):

$$\max \quad Z = 175\,x_{\text{soy}} + 300\,x_{\text{corn}} + 120\,x_{\text{wheat}} + 400\,y_{\text{cow}} + 2\,y_{\text{chicken}} + 1.8\,u_{AW} + 2.1\,u_{SS}$$

**Magnitude sanity check (trivial/greedy solution):** Suppose we plant 100 hm² of corn (highest crop income): $300 \times 100 = 30{,}000$ yuan. Add a few cows and chickens. Total income should be in the range of 30,000–40,000 yuan. The objective coefficients are in yuan, and the answer will be in **yuan** (base unit). ✓

---

## Operational Constraints

### 1. Land Constraint
Total land used by crops plus forage for cows cannot exceed available land:
$$x_{\text{soy}} + x_{\text{corn}} + x_{\text{wheat}} + 1.5\,y_{\text{cow}} \leq 100$$

### 2. Capital Constraint
Total investment in animals cannot exceed available funds:
$$400\,y_{\text{cow}} + 3\,y_{\text{chicken}} \leq 15{,}000$$

### 3. Autumn/Winter Labor Constraint
Total AW labor used (crops + animals) plus external AW labor cannot exceed total AW labor supply:
$$20\,x_{\text{soy}} + 35\,x_{\text{corn}} + 10\,x_{\text{wheat}} + 100\,y_{\text{cow}} + 0.6\,y_{\text{chicken}} + u_{AW} \leq 3{,}500$$

### 4. Spring/Summer Labor Constraint
Total SS labor used (crops + animals) plus external SS labor cannot exceed total SS labor supply:
$$50\,x_{\text{soy}} + 75\,x_{\text{corn}} + 40\,x_{\text{wheat}} + 50\,y_{\text{cow}} + 0.3\,y_{\text{chicken}} + u_{SS} \leq 4{,}000$$

### 5. Animal Capacity Constraints
$$y_{\text{cow}} \leq 32$$
$$y_{\text{chicken}} \leq 3{,}000$$

### 6. Non-negativity and Integrality
$$x_{\text{soy}},\, x_{\text{corn}},\, x_{\text{wheat}},\, u_{AW},\, u_{SS} \geq 0$$
$$y_{\text{cow}} \in \mathbb{Z}_{\geq 0}, \quad y_{\text{chicken}} \in \mathbb{Z}_{\geq 0}$$

---

## Summary of Model Structure

| Aspect | Detail |
|--------|--------|
| **Model Type** | MILP |
| **Objective** | Maximize annual net income (yuan) |
| **Continuous variables** | 5 (3 crop areas + 2 unused labor variables) |
| **Integer variables** | 2 (cows, chickens) |
| **Constraints** | 6 groups (land, capital, 2 labor, 2 capacity) |
| **Key modeling insight** | Unused labor is a decision variable $u$ with positive income coefficients in the objective, naturally incentivizing the solver to allocate all farm labor to the most productive internal use (crops/animals) and only send workers out for the residual. This correctly captures "if labor is not fully used, workers can go out to work." |