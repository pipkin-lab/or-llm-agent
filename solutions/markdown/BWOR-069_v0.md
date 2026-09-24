# Operations Research Model: Product Mix Selection

## Model Type: MILP (Mixed Integer Linear Program)

**Rationale:** The decision involves the number of *pieces* (discrete physical units) of each product to ship, so decision variables must be integer. The objective and constraints are linear.

---

## MANDATORY COST INVENTORY (Pre-Modeling Step)

| Parameter | Entity | Value | Role |
|-----------|--------|-------|------|
| 2 t/piece | Product 1 weight | 2 | Constraint coefficient |
| 3 t/piece | Product 2 weight | 3 | Constraint coefficient |
| 4 t/piece | Product 3 weight | 4 | Constraint coefficient |
| 100 yuan/piece | Product 1 profit | 100 | Objective coefficient |
| 140 yuan/piece | Product 2 profit | 140 | Objective coefficient |
| 180 yuan/piece | Product 3 profit | 180 | Objective coefficient |
| 10 tons | Total transport capacity | 10 | Constraint RHS |

All objective parameters are matched to specific figures in the table. No parameter is missing.

---

## Index Sets & Parameters

**Index Set:**
- $i \in I = \{1, 2, 3\}$: Set of product types.

**Parameters:**

| Symbol | Description | Value | Unit |
|--------|-------------|-------|------|
| $w_i$ | Weight per piece of product $i$ | $w_1=2,\; w_2=3,\; w_3=4$ | tons/piece |
| $p_i$ | Profit per piece of product $i$ | $p_1=100,\; p_2=140,\; p_3=180$ | yuan/piece |
| $W$ | Total transportation capacity | $10$ | tons |

---

## Decision Variables

$$x_i \in \mathbb{Z}_{\geq 0}, \quad \forall i \in I$$

| Variable | Description | Domain |
|----------|-------------|--------|
| $x_i$ | Number of pieces of product $i$ to ship | Non-negative integer ($x_i \geq 0$, $x_i \in \mathbb{Z}$) |

---

## Objective Function

**MAXIMIZE** total profit:

$$\max \quad Z = 100\,x_1 + 140\,x_2 + 180\,x_3$$

**Unit Verification:** The objective yields total profit in **yuan**, which is the natural unit of the problem's final answer (total profit from shipping).

**Magnitude Sanity Check (Greedy Solution):** The most profitable product per ton is Product 1 (100/2 = 50 yuan/ton), followed by Product 2 (140/3 ≈ 46.67 yuan/ton), then Product 3 (180/4 = 45 yuan/ton). A greedy solution would ship 5 pieces of Product 1 (using all 10 tons): $Z = 5 \times 100 = 500$ yuan. The optimal integer solution will be close to this magnitude (hundreds of yuan), which is consistent with the problem's scale. ✓

---

## Operational Constraints

### 1. Transportation Capacity Constraint

The total weight of all shipped products must not exceed the available capacity:

$$2\,x_1 + 3\,x_2 + 4\,x_3 \leq 10$$

### 2. Non-negativity and Integrality Bounds

$$x_1, x_2, x_3 \in \mathbb{Z}_{\geq 0}$$

Equivalently: $x_i \geq 0$ and $x_i$ is an integer for all $i \in \{1, 2, 3\}$.

---

## Feasibility Sanity Check

- **Total capacity:** 10 tons.
- **Minimum weight per piece:** 2 tons (Product 1).
- **Maximum possible pieces:** 5 (all Product 1), using exactly 10 tons.
- The feasible region is bounded and non-empty (e.g., $x_1=x_2=x_3=0$ is feasible).
- No conflicting constraints. The problem is **feasible**. ✓

---

## Complete Formulation Summary

$$\boxed{
\begin{aligned}
\text{maximize} \quad & 100\,x_1 + 140\,x_2 + 180\,x_3 \\[4pt]
\text{subject to} \quad & 2\,x_1 + 3\,x_2 + 4\,x_3 \leq 10 \\
& x_1, x_2, x_3 \in \mathbb{Z}_{\geq 0}
\end{aligned}
}
$$