# Diet Problem: Livestock Feed Formulation

## Model Type Declaration
**Model Type: LP** (Linear Programming)
- All decision variables are continuous (feed weights in kg can be fractional).
- Objective and all constraints are linear.

---

## Mandatory Cost Inventory (Pre-Modeling Step)

| Entity | Parameter | Value | Source in Text |
|---|---|---|---|
| Feed 1 | Price $c_1$ | 0.20 dollar/kg | Table, row "1", col "Price" |
| Feed 2 | Price $c_2$ | 0.70 dollar/kg | Table, row "2", col "Price" |
| Feed 3 | Price $c_3$ | 0.40 dollar/kg | Table, row "3", col "Price" |
| Feed 4 | Price $c_4$ | 0.30 dollar/kg | Table, row "4", col "Price" |
| Feed 5 | Price $c_5$ | 0.80 dollar/kg | Table, row "5", col "Price" |

Count of distinct cost figures = 5 = count of feed types. These ARE the objective coefficients. ✓

Nutritional requirement parameters:
| Nutrient | Requirement | Unit |
|---|---|---|
| Protein | 700 | g/day |
| Minerals | 30 | g/day |
| Vitamins | 100 | mg/day |

Nutritional content per kg (from Table 1-22):

| Feed | Protein (g/kg) | Minerals (g/kg) | Vitamins (mg/kg) |
|---|---|---|---|
| 1 | 3 | 1.0 | 0.5 |
| 2 | 2 | 0.5 | 1.0 |
| 3 | 1 | 0.2 | 0.2 |
| 4 | 6 | 2.0 | 2.0 |
| 5 | 18 | 0.5 | 0.8 |

All units are already consistent (g for protein and minerals; mg for vitamins; dollars for price; kg for quantity). No unit conversion needed.

---

## Index Sets & Parameters

**Index Set:**
- $i \in I = \{1, 2, 3, 4, 5\}$ — set of feed types

**Parameters (all values explicitly provided):**

| Symbol | Description | Value |
|---|---|---|
| $c_i$ | Price of feed $i$ (dollar/kg) | $c_1=0.20,\; c_2=0.70,\; c_3=0.40,\; c_4=0.30,\; c_5=0.80$ |
| $p_i$ | Protein content of feed $i$ (g/kg) | $p_1=3,\; p_2=2,\; p_3=1,\; p_4=6,\; p_5=18$ |
| $m_i$ | Mineral content of feed $i$ (g/kg) | $m_1=1.0,\; m_2=0.5,\; m_3=0.2,\; m_4=2.0,\; m_5=0.5$ |
| $v_i$ | Vitamin content of feed $i$ (mg/kg) | $v_1=0.5,\; v_2=1.0,\; v_3=0.2,\; v_4=2.0,\; v_5=0.8$ |
| $P_{req}$ | Minimum daily protein requirement | 700 g |
| $M_{req}$ | Minimum daily mineral requirement | 30 g |
| $V_{req}$ | Minimum daily vitamin requirement | 100 mg |

---

## Decision Variables

| Symbol | Description | Domain |
|---|---|---|
| $x_i$ | Daily amount of feed $i$ used (kg/day) | $x_i \geq 0,\;\; i \in I$ (CONTINUOUS) |

Feed quantities are continuous resources (measured in kg), so continuous variables are appropriate.

---

## Objective Function

$$\min \quad Z = 0.20\,x_1 + 0.70\,x_2 + 0.40\,x_3 + 0.30\,x_4 + 0.80\,x_5$$

**Objective Parameter Cross-Reference:**
- $c_1 = 0.20$ → Table row 1, Price column ✓
- $c_2 = 0.70$ → Table row 2, Price column ✓
- $c_3 = 0.40$ → Table row 3, Price column ✓
- $c_4 = 0.30$ → Table row 4, Price column ✓
- $c_5 = 0.80$ → Table row 5, Price column ✓

All objective coefficients are located in the source text. No parameter is [NOT_PROVIDED].

**Magnitude Sanity Check (Rule 11):** The problem asks to "minimize the cost" — a total dollar amount, not a per-unit rate or normalized figure. The objective is in dollars/day, which is the natural unit. A greedy solution using only Feed 4 (cheapest protein-dense feed at $0.30/kg) to meet protein (700/6 ≈ 116.7 kg) would cost ≈ $35/day, but would exceed mineral and vitamin requirements, requiring additional feeds. The expected optimal cost is on the order of tens of dollars per day — a reasonable magnitude for the question as posed. No normalization division is needed. ✓

---

## Operational Constraints

### 1. Protein Requirement (≥ 700 g/day)
$$3\,x_1 + 2\,x_2 + 1\,x_3 + 6\,x_4 + 18\,x_5 \;\geq\; 700$$

### 2. Mineral Requirement (≥ 30 g/day)
$$1.0\,x_1 + 0.5\,x_2 + 0.2\,x_3 + 2.0\,x_4 + 0.5\,x_5 \;\geq\; 30$$

### 3. Vitamin Requirement (≥ 100 mg/day)
$$0.5\,x_1 + 1.0\,x_2 + 0.2\,x_3 + 2.0\,x_4 + 0.8\,x_5 \;\geq\; 100$$

### 4. Non-negativity Bounds
$$x_i \;\geq\; 0, \quad \forall\, i \in \{1, 2, 3, 4, 5\}$$

---

## Feasibility Sanity Check (Rule 7)

- **Protein:** Feed 4 alone provides 6 g protein/kg. To meet 700 g: $x_4 \geq 700/6 \approx 116.7$ kg. This also provides $116.7 \times 2.0 = 233.3$ g minerals (≥ 30 ✓) and $116.7 \times 2.0 = 233.3$ mg vitamins (≥ 100 ✓). So a feasible solution exists using Feed 4 alone.
- **Minerals:** Feed 4 provides 2.0 g/kg. Even $x_4 = 15$ kg gives 30 g minerals.
- **Vitamins:** Feed 4 provides 2.0 mg/kg. Even $x_4 = 50$ kg gives 100 mg vitamins.

The three constraints are mutually satisfiable. The model is **FEASIBLE**. No additional capacity or upper-bound constraints are specified in the problem, so none are added.

---

## Complete Formulation Summary

$$
\boxed{
\begin{aligned}
\min \quad & 0.20\,x_1 + 0.70\,x_2 + 0.40\,x_3 + 0.30\,x_4 + 0.80\,x_5 \\[6pt]
\text{s.t.} \quad & 3\,x_1 + 2\,x_2 + 1\,x_3 + 6\,x_4 + 18\,x_5 \;\geq\; 700 && \text{(Protein)} \\
& 1.0\,x_1 + 0.5\,x_2 + 0.2\,x_3 + 2.0\,x_4 + 0.5\,x_5 \;\geq\; 30 && \text{(Minerals)} \\
& 0.5\,x_1 + 1.0\,x_2 + 0.2\,x_3 + 2.0\,x_4 + 0.8\,x_5 \;\geq\; 100 && \text{(Vitamins)} \\
& x_1, x_2, x_3, x_4, x_5 \;\geq\; 0
\end{aligned}
}
$$

This is a standard linear diet problem (a special case of linear programming) with 5 continuous decision variables, 3 nutritional lower-bound constraints, and 5 non-negativity constraints. A standard LP solver (e.g., simplex or interior-point) will yield the optimal feed mix and minimum daily cost.