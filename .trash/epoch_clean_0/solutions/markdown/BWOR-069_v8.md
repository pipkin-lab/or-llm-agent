## Model Type: MILP (Mixed Integer Linear Programming)

### Index Sets & Parameters

**Index Sets:**
- $I = \{1, 2, 3\}$ : set of product types

**Parameters:**
- $w_i$ : weight of one piece of product $i$ (tons/piece)
  - $w_1 = 2$, $w_2 = 3$, $w_3 = 4$
- $p_i$ : profit of one piece of product $i$ (yuan/piece)
  - $p_1 = 100$, $p_2 = 140$, $p_3 = 180$
- $W = 10$ : total transportation capacity (tons)

### Decision Variables

- $x_i$ : number of pieces of product $i$ to produce and ship, for each $i \in I$
  - Domain: $x_i \in \mathbb{Z}_{\geq 0}$ (non-negative integers, since products are discrete physical units)

### Objective Function

**MAXIMIZE** total profit:

$$\max \quad Z = 100 \, x_1 + 140 \, x_2 + 180 \, x_3$$

### Operational Constraints

**1. Transportation Capacity Constraint:**

The total weight of all shipped products must not exceed the transportation capacity of 10 tons:

$$2 \, x_1 + 3 \, x_2 + 4 \, x_3 \leq 10$$

**2. Non-negativity and Integrality Bounds:**

$$x_1, x_2, x_3 \in \mathbb{Z}_{\geq 0}$$

### Feasibility Sanity Check

- All weights are positive and the capacity is 10 tons, so there exist feasible solutions (e.g., $x_1=x_2=x_3=0$).
- The constraint is a single knapsack-type inequality. Since all coefficients are positive integers and the capacity is small, the feasible region is finite and non-empty.
- No conflicting or mutually exclusive constraints are present. The model is feasible.