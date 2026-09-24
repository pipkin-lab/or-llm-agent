# Mathematical Optimization Model

## Model Type: MILP (Mixed-Integer Linear Programming)

## Mandatory Cost Inventory (Pre-Modeling Step)

The objective is to **maximize total monthly profit**. The profit values are given directly in Table 7-2 as a function of the number of outlets assigned to each region. These are the objective coefficients (non-linear in the sense that profit is not linear in the number of outlets, but can be linearized via binary variables).

| Region | 0 outlets | 1 outlet | 2 outlets | 3 outlets | 4 outlets |
|--------|-----------|----------|-----------|-----------|-----------|
| 1      | 0         | 16       | 25        | 30        | 32        |
| 2      | 0         | 12       | 17        | 21        | 22        |
| 3      | 0         | 10       | 14        | 16        | 17        |

Total outlets to allocate: **4** (fixed).

---

## Index Sets & Parameters

- **Regions**: $R = \{1, 2, 3\}$
- **Possible outlet counts per region**: $K = \{0, 1, 2, 3, 4\}$
- **Total outlets available**: $N = 4$
- **Profit parameter** $\pi_{r,k}$: Monthly profit (in monetary units) from assigning $k$ outlets to region $r$, extracted from Table 7-2:

| $r$ \ $k$ | 0 | 1 | 2 | 3 | 4 |
|-----------|---|---|---|---|---|
| 1         | 0 | 16 | 25 | 30 | 32 |
| 2         | 0 | 12 | 17 | 21 | 22 |
| 3         | 0 | 10 | 14 | 16 | 17 |

---

## Decision Variables

For each region $r \in R$ and each possible allocation $k \in K$:

$$x_{r,k} \in \{0, 1\} \quad \forall r \in R,\; k \in K$$

where $x_{r,k} = 1$ if and only if exactly $k$ outlets are assigned to region $r$, and $x_{r,k} = 0$ otherwise.

---

## Objective Function

$$\text{MAXIMIZE} \quad Z = \sum_{r=1}^{3} \sum_{k=0}^{4} \pi_{r,k} \cdot x_{r,k}$$

Expanding explicitly:

$$Z = (0 \cdot x_{1,0} + 16 \cdot x_{1,1} + 25 \cdot x_{1,2} + 30 \cdot x_{1,3} + 32 \cdot x_{1,4}) + (0 \cdot x_{2,0} + 12 \cdot x_{2,1} + 17 \cdot x_{2,2} + 21 \cdot x_{2,3} + 22 \cdot x_{2,4}) + (0 \cdot x_{3,0} + 10 \cdot x_{3,1} + 14 \cdot x_{3,2} + 16 \cdot x_{3,3} + 17 \cdot x_{3,4})$$

**Objective Parameter Cross-Reference**: All $\pi_{r,k}$ values are explicitly provided in Table 7-2. No parameter is missing.

---

## Operational Constraints

### 1. Exactly one allocation per region (partition of unity):
$$\sum_{k=0}^{4} x_{r,k} = 1 \quad \forall r \in \{1, 2, 3\}$$

This ensures each region receives exactly one valid number of outlets (0, 1, 2, 3, or 4).

### 2. Total outlet budget constraint:
$$\sum_{r=1}^{3} \sum_{k=0}^{4} k \cdot x_{r,k} = 4$$

This enforces that the total number of outlets allocated across all three regions equals exactly 4.

### 3. Binary domain constraints:
$$x_{r,k} \in \{0, 1\} \quad \forall r \in \{1, 2, 3\},\; k \in \{0, 1, 2, 3, 4\}$$

---

## Feasibility Sanity Check

- Total outlets = 4, distributed among 3 regions, each can take 0–4 outlets.
- Feasible allocations include e.g., (2,1,1), (1,2,1), (1,1,2), (2,2,0), (3,1,0), (4,0,0), etc.
- The constraint $\sum k \cdot x_{r,k} = 4$ combined with the partition constraints guarantees a finite, non-empty feasible set. ✓

---

## Magnitude Sanity Check

Greedy check: Try allocation (2, 1, 1):
- Region 1 with 2 outlets: 25
- Region 2 with 1 outlet: 12
- Region 3 with 1 outlet: 10
- Total = 47

Try (1, 2, 1):
- 16 + 17 + 10 = 43

Try (1, 1, 2):
- 16 + 12 + 14 = 42

Try (2, 2, 0):
- 25 + 17 + 0 = 42

Try (3, 1, 0):
- 30 + 12 + 0 = 42

Try (3, 0, 1):
- 30 + 0 + 10 = 40

Try (4, 0, 0):
- 32 + 0 + 0 = 32

Try (2, 1, 1) = 47; Try (1, 2, 1) = 43; Try (0, 2, 2) = 0 + 17 + 14 = 31.

The expected optimal value is in the range of 40–50, which is consistent with the scale of the profit table. ✓

---

## Summary

The model is a **MILP** with 15 binary variables, 4 linear constraints (3 partition + 1 budget), and a linear objective. The optimal solution will assign exactly one outlet count to each region summing to 4, maximizing the total monthly profit as tabulated.