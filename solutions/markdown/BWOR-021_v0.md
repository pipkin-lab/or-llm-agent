## Model Type: MILP

This is a **Mixed-Integer Linear Programming (MILP)** problem. The decision involves allocating discrete units of capital (thousand yuan) to projects, where the benefit function is defined only at specific integer investment levels (0, 1, 2, 3, 4 thousand yuan). Since benefits are non-linear (discrete table values), we use binary indicator variables to select the investment level for each project.

---

## Index Sets & Parameters

### Index Sets
- $P = \{A, B, C\}$: Set of projects, indexed by $p$
- $K = \{0, 1, 2, 3, 4\}$: Set of possible investment levels (in thousand yuan), indexed by $k$

### Parameters
| Parameter | Description | Value |
|-----------|-------------|-------|
| $B_{p,k}$ | Benefit (thousand yuan) from investing $k$ thousand yuan in project $p$ | See table below |
| $C_{total}$ | Total available capital (thousand yuan) | 4 |

**Benefit Table ($B_{p,k}$):**

| $p \backslash k$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| A | 0 | 41 | 48 | 60 | 66 |
| B | 0 | 42 | 50 | 60 | 66 |
| C | 0 | 64 | 68 | 78 | 76 |

---

## Decision Variables

- $y_{p,k} \in \{0, 1\}$: Binary variable for each project $p$ and investment level $k$.
  - $y_{p,k} = 1$ if project $p$ receives exactly $k$ thousand yuan
  - $y_{p,k} = 0$ otherwise

**Domain:** $y_{p,k} \in \{0, 1\} \quad \forall p \in P, \forall k \in K$

---

## Objective Function

**Maximize total benefit:**

$$\max Z = \sum_{p \in P} \sum_{k \in K} B_{p,k} \cdot y_{p,k}$$

Expanded:
$$Z = \sum_{k=0}^{4} B_{A,k} y_{A,k} + \sum_{k=0}^{4} B_{B,k} y_{B,k} + \sum_{k=0}^{4} B_{C,k} y_{C,k}$$

---

## Operational Constraints

### 1. Exactly One Investment Level Per Project
Each project must be assigned exactly one investment level:

$$\sum_{k=0}^{4} y_{p,k} = 1 \quad \forall p \in P$$

This gives 3 constraints:
- $\sum_{k=0}^{4} y_{A,k} = 1$
- $\sum_{k=0}^{4} y_{B,k} = 1$
- $\sum_{k=0}^{4} y_{C,k} = 1$

### 2. Total Capital Constraint
The sum of investments across all projects must not exceed the total available capital:

$$\sum_{p \in P} \sum_{k \in K} k \cdot y_{p,k} \leq 4$$

Expanded:
$$1 \cdot y_{A,1} + 2 \cdot y_{A,2} + 3 \cdot y_{A,3} + 4 \cdot y_{A,4} + 1 \cdot y_{B,1} + 2 \cdot y_{B,2} + 3 \cdot y_{B,3} + 4 \cdot y_{B,4} + 1 \cdot y_{C,1} + 2 \cdot y_{C,2} + 3 \cdot y_{C,3} + 4 \cdot y_{C,4} \leq 4$$

### 3. Non-negativity / Domain
$$y_{p,k} \in \{0, 1\} \quad \forall p \in \{A, B, C\}, \forall k \in \{0, 1, 2, 3, 4\}$$

---

## Feasibility Sanity Check

- Total capital = 4 thousand yuan
- Minimum investment per project = 0 (allowed, since $k=0$ is in $K$)
- Maximum possible investment = 4 (all to one project)
- The constraint $\sum k \cdot y_{p,k} \leq 4$ is satisfiable (e.g., invest 0,0,0 uses 0; invest 4,0,0 uses 4)
- The "exactly one level" constraints are always satisfiable independently
- **Feasible region is non-empty.** ✓

---

## Solution Outline (for verification)

The optimal allocation can be found by enumerating all feasible combinations $(k_A, k_B, k_C)$ with $k_A + k_B + k_C \leq 4$:

| $k_A$ | $k_B$ | $k_C$ | Total Inv | $B_A$ | $B_B$ | $B_C$ | Total Benefit |
|-------|-------|-------|-----------|-------|-------|-------|---------------|
| 0 | 0 | 4 | 4 | 0 | 0 | 76 | 76 |
| 0 | 1 | 3 | 4 | 0 | 42 | 78 | 120 |
| 0 | 2 | 2 | 4 | 0 | 50 | 68 | 118 |
| 0 | 3 | 1 | 4 | 0 | 60 | 64 | 124 |
| 0 | 4 | 0 | 4 | 0 | 66 | 0 | 66 |
| 1 | 0 | 3 | 4 | 41 | 0 | 78 | 119 |
| 1 | 1 | 2 | 4 | 41 | 42 | 68 | 151 |
| 1 | 2 | 1 | 4 | 41 | 50 | 64 | 155 |
| 1 | 3 | 0 | 4 | 41 | 60 | 0 | 101 |
| 2 | 0 | 2 | 4 | 48 | 0 | 68 | 116 |
| 2 | 1 | 1 | 4 | 48 | 42 | 64 | 154 |
| 2 | 2 | 0 | 4 | 48 | 50 | 0 | 98 |
| 3 | 0 | 1 | 4 | 60 | 0 | 64 | 124 |
| 3 | 1 | 0 | 4 | 60 | 42 | 0 | 102 |
| 4 | 0 | 0 | 4 | 66 | 0 | 0 | 66 |
| 1 | 1 | 1 | 3 | 41 | 42 | 64 | 147 |
| 2 | 1 | 0 | 3 | 48 | 42 | 0 | 90 |
| 0 | 2 | 1 | 3 | 0 | 50 | 64 | 114 |
| 0 | 1 | 2 | 3 | 0 | 42 | 68 | 110 |
| 1 | 2 | 0 | 3 | 41 | 50 | 0 | 91 |
| 0 | 3 | 0 | 3 | 0 | 60 | 0 | 60 |
| 0 | 0 | 3 | 3 | 0 | 0 | 78 | 78 |
| 2 | 0 | 1 | 3 | 48 | 0 | 64 | 112 |
| 1 | 0 | 2 | 3 | 41 | 0 | 68 | 109 |
| 3 | 0 | 0 | 3 | 60 | 0 | 0 | 60 |
| 0 | 0 | 2 | 2 | 0 | 0 | 68 | 68 |
| 1 | 0 | 1 | 2 | 41 | 0 | 64 | 105 |
| 0 | 1 | 1 | 2 | 0 | 42 | 64 | 106 |
| 0 | 0 | 1 | 1 | 0 | 0 | 64 | 64 |
| 1 | 0 | 0 | 1 | 41 | 0 | 0 | 41 |
| 0 | 1 | 0 | 1 | 0 | 42 | 0 | 42 |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**Optimal solution:** $k_A = 1, k_B = 2, k_C = 1$ with total benefit = **155** thousand yuan.

(Second best: $k_A=2, k_B=1, k_C=1$ with benefit 154.)