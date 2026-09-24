# Multi-Choice Knapsack Problem (MCKP) Formulation

## Model Type Declaration
**MILP** (Mixed-Integer Linear Program). The decision variables are binary (selecting exactly one plan per factory), and the objective and constraints are linear. A standard MILP solver (e.g., Gurobi, CPLEX, or SCIP) is required.

---

## Index Sets & Parameters

### Index Sets
- $I = \{1, 2, 3\}$: Set of factories.
- $J_i$: Set of available plans for factory $i$.
  - $J_1 = \{1, 2, 3\}$ (Plans 1, 2, 3 are available for Factory 1)
  - $J_2 = \{1, 2, 3, 4\}$ (Plans 1, 2, 3, 4 are available for Factory 2)
  - $J_3 = \{1, 2\}$ (Plans 1, 2 are available for Factory 3)
- $J = \{(i, j) \mid i \in I, j \in J_i\}$: Set of all valid (factory, plan) pairs.

### Parameters
- $B = 5$: Total available budget (million yuan).
- $c_{ij}$: Investment cost for plan $j$ at factory $i$ (million yuan).
- $r_{ij}$: Expected return for plan $j$ at factory $i$ (million yuan).

**Parameter Values (extracted from Table 7-4):**

| Factory $i$ | Plan $j$ | Investment $c_{ij}$ | Return $r_{ij}$ |
| :--- | :---: | :---: | :---: |
| 1 | 1 | 0 | 0 |
| 1 | 2 | 1 | 5 |
| 1 | 3 | 2 | 6 |
| 2 | 1 | 0 | 0 |
| 2 | 2 | 2 | 8 |
| 2 | 3 | 3 | 9 |
| 2 | 4 | 4 | 12 |
| 3 | 1 | 0 | 0 |
| 3 | 2 | 1 | 3 |

*Note: Plans marked with "–" are excluded from the model as they are not available.*

---

## Decision Variables

Let $x_{ij}$ be a binary variable for each valid (factory, plan) pair:

$$
x_{ij} = 
\begin{cases} 
1 & \text{if plan } j \text{ is selected for factory } i \\
0 & \text{otherwise}
\end{cases}
\quad \forall i \in I, \, j \in J_i
$$

**Domain:**
$$
x_{ij} \in \{0, 1\} \quad \forall i \in I, \, j \in J_i
$$

---

## Objective Function

Maximize the total expected return:

$$
\max Z = \sum_{i \in I} \sum_{j \in J_i} r_{ij} x_{ij}
$$

Expanded form:
$$
\max Z = 5x_{12} + 6x_{13} + 8x_{22} + 9x_{23} + 12x_{24} + 3x_{32}
$$
*(Note: $x_{11}, x_{21}, x_{31}$ have zero coefficients since Plan 1 yields 0 return.)*

---

## Operational Constraints

### 1. Exactly One Plan Per Factory
Each factory must select exactly one plan (including the "do nothing" Plan 1 if no investment is made):

$$
\sum_{j \in J_i} x_{ij} = 1 \quad \forall i \in I
$$

Expanded:
- Factory 1: $x_{11} + x_{12} + x_{13} = 1$
- Factory 2: $x_{21} + x_{22} + x_{23} + x_{24} = 1$
- Factory 3: $x_{31} + x_{32} = 1$

### 2. Budget Constraint
Total investment must not exceed the available budget of 5 million yuan:

$$
\sum_{i \in I} \sum_{j \in J_i} c_{ij} x_{ij} \leq B
$$

Expanded:
$$
1x_{12} + 2x_{13} + 2x_{22} + 3x_{23} + 4x_{24} + 1x_{32} \leq 5
$$
*(Note: $x_{11}, x_{21}, x_{31}$ have zero coefficients since Plan 1 requires 0 investment.)*

### 3. Domain Constraints
$$
x_{ij} \in \{0, 1\} \quad \forall i \in I, \, j \in J_i
$$

---

## Feasibility & Sanity Check

- **Budget:** 5 million yuan is sufficient to select at least one plan per factory (e.g., selecting Plan 1 for all factories costs 0, which is feasible).
- **Objective Magnitude:** The maximum possible return is bounded by the sum of the highest-return plans that fit within the budget. For example, selecting Plan 3 for Factory 1 (cost 2, return 6), Plan 4 for Factory 2 (cost 4, return 12), and Plan 1 for Factory 3 (cost 0, return 0) costs 6, which exceeds the budget. A feasible high-return combination might be Plan 2 for Factory 1 (cost 1, return 5), Plan 3 for Factory 2 (cost 3, return 9), and Plan 2 for Factory 3 (cost 1, return 3), totaling cost 5 and return 17. The optimal value will be a reasonable double-digit number, consistent with the problem's scale.
- **No Infeasibility:** The constraints are mutually compatible, and a feasible solution always exists (e.g., $x_{11}=x_{21}=x_{31}=1$).