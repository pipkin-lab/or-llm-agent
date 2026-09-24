## Mathematical Optimization Model

### Model Type
**LP** (Linear Program)

---

### Index Sets & Parameters

**Sets:**
- Origins (supply nodes): $I = \{1, 2, 3\}$
- Destinations (demand nodes): $J = \{A, B, C\}$

**Parameters:**

| Parameter | Description | Value |
|-----------|-------------|-------|
| $c_{ij}$ | Unit shipping cost from origin $i$ to destination $j$ | $c_{1A}=1, c_{1B}=2, c_{1C}=2$ |
|           |                                                       | $c_{2A}=1, c_{2B}=4, c_{2C}=5$ |
|           |                                                       | $c_{3A}=2, c_{3B}=3, c_{3C}=3$ |
| $s_i$ | Supply at origin $i$ | $s_1=20, s_2=40, s_3=30$ |
| $d_j$ | Demand at destination $j$ | $d_A=30, d_B=20, d_C=20$ |
| $h_i$ | Unit storage cost for unsent goods at origin $i$ | $h_1=5, h_2=4, h_3=3$ |
| $L_2$ | Minimum shipment from origin 2 | $L_2 = 38$ |
| $L_3$ | Minimum shipment from origin 3 | $L_3 = 27$ |

**Feasibility Note:** Total supply $= 20+40+30 = 90$. Total demand $= 30+20+20 = 50$. Since supply exceeds demand, 40 units will remain unshipped and incur storage costs.

---

### Decision Variables

- $x_{ij} \in \mathbb{R}_{\geq 0}$: Quantity shipped from origin $i$ to destination $j$, for all $i \in I, j \in J$
- $u_i \in \mathbb{R}_{\geq 0}$: Quantity of goods from origin $i$ that is not shipped (stored), for all $i \in I$

---

### Objective Function

**MINIMIZE** total cost (shipping + storage):

$$\min \sum_{i \in I} \sum_{j \in J} c_{ij} \, x_{ij} + \sum_{i \in I} h_i \, u_i$$

Expanded:

$$\min (1x_{1A} + 2x_{1B} + 2x_{1C}) + (1x_{2A} + 4x_{2B} + 5x_{2C}) + (2x_{3A} + 3x_{3B} + 3x_{3C}) + 5u_1 + 4u_2 + 3u_3$$

---

### Operational Constraints

**1. Supply Balance (Equality — all supply must be either shipped or stored):**

$$\sum_{j \in J} x_{ij} + u_i = s_i, \quad \forall i \in I$$

- $x_{1A} + x_{1B} + x_{1C} + u_1 = 20$
- $x_{2A} + x_{2B} + x_{2C} + u_2 = 40$
- $x_{3A} + x_{3B} + x_{3C} + u_3 = 30$

**2. Demand Satisfaction (Equality — all demand must be met):**

$$\sum_{i \in I} x_{ij} = d_j, \quad \forall j \in J$$

- $x_{1A} + x_{2A} + x_{3A} = 30$
- $x_{1B} + x_{2B} + x_{3B} = 20$
- $x_{1C} + x_{2C} + x_{3C} = 20$

**3. Minimum Shipment Constraints:**

Total shipped from origin 2 must be at least 38:
$$x_{2A} + x_{2B} + x_{2C} \geq 38$$

Total shipped from origin 3 must be at least 27:
$$x_{3A} + x_{3B} + x_{3C} \geq 27$$

**4. Non-negativity Bounds:**

$$x_{ij} \geq 0, \quad \forall i \in I, j \in J$$
$$u_i \geq 0, \quad \forall i \in I$$

---

### Feasibility Sanity Check

- Total supply = 90, total demand = 50 → 40 units will be stored.
- Minimum shipment constraints: origin 2 ships $\geq 38$ (leaves $u_2 \leq 2$), origin 3 ships $\geq 27$ (leaves $u_3 \leq 3$).
- Origin 1 must supply the remainder: total shipped = 50, so origin 1 ships $50 - (\text{ship}_2) - (\text{ship}_3) \leq 50 - 38 - 27 = -15$.

Wait — this reveals a conflict. Let me re-examine: if origin 2 ships at least 38 and origin 3 ships at least 27, their combined minimum is 65, which exceeds total demand of 50. This is **infeasible** as stated.

However, re-reading the problem: the minimum shipment constraints are lower bounds on what must be shipped from those origins. Since total demand is only 50, and origins 2 and 3 together must ship at least $38+27=65 > 50$, the problem as literally stated is **infeasible**.

**Re-examination:** The problem likely intends these as binding operational requirements that override the standard transportation structure. Given this is a textbook exercise, the most reasonable interpretation is that the minimum shipment constraints are hard requirements, and the model remains feasible only if we accept that the demand equalities and supply equalities must hold simultaneously. Let me verify:

- If $x_{2,\cdot} \geq 38$ and $x_{3,\cdot} \geq 27$, then total shipped $\geq 65$, but total demand = 50. **Contradiction.**

Given the problem states "solve for the optimal solution," the intended interpretation must be that the minimum shipment constraints apply, and the problem is feasible because the supply balance allows it — meaning the demand constraints should still be satisfied. This is only possible if the minimum shipment values are interpreted relative to the available supply after accounting for the other origin. 

Upon careful re-reading, the problem is from a standard OR textbook context where such constraints are meant to be added to a balanced transportation problem. The correct interpretation is that these are **additional lower-bound constraints** on the row sums. The problem is feasible because:

- Origin 2 can ship at most 40 (its supply), origin 3 at most 30.
- $38 + 27 = 65 > 50$ total demand → **still infeasible**.

Given the problem explicitly asks to "solve for the optimal solution," I will proceed with the formulation as stated. The solver will detect infeasibility, or the intended values may have a typo. The formulation above is the correct mathematical representation of the problem as described.