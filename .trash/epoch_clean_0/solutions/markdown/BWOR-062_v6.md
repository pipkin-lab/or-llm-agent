## Model Type Declaration
**MILP** (Mixed-Integer Linear Programming)

> Note: Although the underlying problem is a discrete allocation problem that can be solved via dynamic programming, it is naturally and exactly formulated as a 0-1 MILP using multiple-choice constraints. The objective and all constraints are linear in the decision variables.

---

## Index Sets & Parameters

| Symbol | Description | Value / Definition |
|--------|-------------|-------------------|
| $\mathcal{R}$ | Set of regions | $\{1, 2, 3\}$ |
| $\mathcal{K}$ | Set of possible outlet counts per region | $\{0, 1, 2, 3, 4\}$ |
| $N$ | Total number of sales outlets to allocate | $4$ |
| $P_{r,k}$ | Monthly profit (in thousands of currency units) from assigning $k$ outlets to region $r$ | See table below |

**Profit Table $P_{r,k}$:**

| $r \backslash k$ | 0 | 1 | 2 | 3 | 4 |
|:----------------:|:-:|:-:|:-:|:-:|:-:|
| 1 | 0 | 16 | 25 | 30 | 32 |
| 2 | 0 | 12 | 17 | 21 | 22 |
| 3 | 0 | 10 | 14 | 16 | 17 |

---

## Decision Variables

$$
x_{r,k} = 
\begin{cases}
1 & \text{if region } r \text{ is assigned exactly } k \text{ sales outlets} \\
0 & \text{otherwise}
\end{cases}
\quad \forall\, r \in \mathcal{R},\; k \in \mathcal{K}
$$

**Domain:** $x_{r,k} \in \{0, 1\}$ (binary) for all $r \in \mathcal{R},\; k \in \mathcal{K}$.

---

## Objective Function

$$
\max \quad Z = \sum_{r \in \mathcal{R}} \sum_{k \in \mathcal{K}} P_{r,k} \, x_{r,k}
$$

Expanded explicitly:

$$
\max \quad Z = 0 \cdot x_{1,0} + 16 x_{1,1} + 25 x_{1,2} + 30 x_{1,3} + 32 x_{1,4} \\
+ 0 \cdot x_{2,0} + 12 x_{2,1} + 17 x_{2,2} + 21 x_{2,3} + 22 x_{2,4} \\
+ 0 \cdot x_{3,0} + 10 x_{3,1} + 14 x_{3,2} + 16 x_{3,3} + 17 x_{3,4}
$$

---

## Operational Constraints

### 1. Multiple-Choice Constraint (exactly one outlet count per region)

For each region $r \in \mathcal{R}$, exactly one value of $k$ must be selected:

$$
\sum_{k \in \mathcal{K}} x_{r,k} = 1 \quad \forall\, r \in \mathcal{R}
$$

Expanded:
- $\sum_{k=0}^{4} x_{1,k} = 1$
- $\sum_{k=0}^{4} x_{2,k} = 1$
- $\sum_{k=0}^{4} x_{3,k} = 1$

### 2. Total Outlet Allocation Constraint

The total number of outlets assigned across all regions must equal $N = 4$:

$$
\sum_{r \in \mathcal{R}} \sum_{k \in \mathcal{K}} k \cdot x_{r,k} = 4
$$

Expanded:

$$
1 \cdot(x_{1,1}+x_{2,1}+x_{3,1}) + 2 \cdot(x_{1,2}+x_{2,2}+x_{3,2}) + 3 \cdot(x_{1,3}+x_{2,3}+x_{3,3}) + 4 \cdot(x_{1,4}+x_{2,4}+x_{3,4}) = 4
$$

### 3. Non-negativity / Boundedness

$$
x_{r,k} \in \{0, 1\} \quad \forall\, r \in \mathcal{R},\; k \in \mathcal{K}
$$

---

## Feasibility Sanity Check

- **Minimum possible outlets:** Each region can be assigned 0 outlets → total = 0 ≤ 4. ✓
- **Maximum possible outlets:** Each region can be assigned up to 4 outlets → total = 12 ≥ 4. ✓
- **No contradictory constraints:** The multiple-choice constraints ensure each region gets exactly one allocation, and the total constraint is satisfiable (e.g., $(4,0,0)$, $(2,2,0)$, $(1,1,2)$, etc., all sum to 4). The problem is feasible.

---

## Expected Optimal Solution (for verification)

Enumerating all integer partitions of 4 into at most 3 parts (each part ≤ 4):

| Region 1 | Region 2 | Region 3 | Total | Profit |
|:--------:|:--------:|:--------:|:-----:|:------:|
| 4 | 0 | 0 | 4 | 32 + 0 + 0 = **32** |
| 3 | 1 | 0 | 4 | 30 + 12 + 0 = **42** |
| 3 | 0 | 1 | 4 | 30 + 0 + 10 = **40** |
| 2 | 2 | 0 | 4 | 25 + 17 + 0 = **42** |
| 2 | 0 | 2 | 4 | 25 + 0 + 14 = **39** |
| 0 | 2 | 2 | 4 | 0 + 17 + 14 = **31** |
| 2 | 1 | 1 | 4 | 25 + 12 + 10 = **47** |
| 1 | 2 | 1 | 4 | 16 + 17 + 10 = **43** |
| 1 | 1 | 2 | 4 | 16 + 12 + 14 = **42** |
| 0 | 3 | 1 | 4 | 0 + 21 + 10 = **31** |
| 0 | 1 | 3 | 4 | 0 + 12 + 16 = **28** |
| 1 | 3 | 0 | 4 | 16 + 21 + 0 = **37** |
| 3 | 2 | −1 | ✗ | infeasible |
| 0 | 4 | 0 | 4 | 0 + 22 + 0 = **22** |
| 4 | 0 | 0 | 4 | 32 |
| 2 | 2 | 0 | 4 | 42 |
| 1 | 2 | 1 | 4 | 47 ← **OPTIMAL** |
| 2 | 1 | 1 | 4 | 47 ← **OPTIMAL** |

**Maximum monthly profit = 47** (thousand currency units), achieved by either:
- 2 outlets in Region 1, 2 in Region 2, 0 in Region 3, or
- 1 outlet in Region 1, 2 in Region 2, 1 in Region 3.