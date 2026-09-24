## Model Type Declaration
**MILP** (Mixed Integer Linear Programming). 
The decision variables represent the number of spare parts, which are discrete quantities (integers). The objective function and constraints are linear.

## Index Sets & Parameters

**Index Sets:**
- $J = \{1, 2, 3\}$: Set of spare part types ($E_1, E_2, E_3$).
- $K = \{1, 2, 3\}$: Set of possible quantity levels for each part type.

**Parameters (from Table 7-10):**
*Note: The cost column in the table header is "Cost (thousand yuan)". The investment limit is 8,000 yuan, which is 8 thousand yuan. We will work in units of **thousand yuan**.*

- $B = 8$: Total budget limit (thousand yuan).
- $r_{j,k}$: Increase in reliability for part type $j$ when $k$ spares are held.
  - $r_{1,1} = 0.3, \quad r_{2,1} = 0.2, \quad r_{3,1} = 0.1$
  - $r_{1,2} = 0.4, \quad r_{2,2} = 0.5, \quad r_{3,2} = 0.2$
  - $r_{1,3} = 0.5, \quad r_{2,3} = 0.9, \quad r_{3,3} = 0.7$
- $c_{j,k}$: Cost (thousand yuan) for part type $j$ when $k$ spares are held.
  - $c_{1,1} = 1, \quad c_{2,1} = 3, \quad c_{3,1} = 2$
  - $c_{1,2} = 2, \quad c_{2,2} = 5, \quad c_{3,2} = 3$
  - $c_{1,3} = 3, \quad c_{2,3} = 6, \quad c_{3,3} = 4$

## Decision Variables

Let $x_{j,k}$ be a binary variable:
$$
x_{j,k} = 
\begin{cases} 
1 & \text{if part type } j \text{ is allocated exactly } k \text{ spares} \\
0 & \text{otherwise}
\end{cases}
$$
for all $j \in J, k \in K$.

## Objective Function

Maximize the total increase in reliability:
$$
\text{Maximize } Z = \sum_{j=1}^{3} \sum_{k=1}^{3} r_{j,k} \cdot x_{j,k}
$$

## Operational Constraints

**1. Exactly one quantity level must be chosen for each part type:**
For each $j \in \{1, 2, 3\}$:
$$
\sum_{k=1}^{3} x_{j,k} = 1
$$
*(Note: The problem implies we must keep spares of three types. The table provides options for z=1,2,3. It is standard in such "level selection" problems that a specific level must be selected. If "0 spares" were an option, it would typically be listed as z=0 with 0 reliability/cost. Since it is not listed, we assume at least 1 spare of each type is required, or that the options 1-3 are the exclusive choices. Given the phrasing "keep three types... increasing number... improves reliability", and the table starts at z=1, we assume the decision is among 1, 2, or 3. If 0 were allowed, it would be a 4th option with 0 cost/reliability. However, usually, these problems imply choosing from the given discrete states. Let's assume the choice is restricted to the given levels 1, 2, 3. If the problem allowed 0, the cost/reliability would be 0. Let's re-read carefully: "keep three types... increasing the number...". It doesn't explicitly forbid 0, but the table only lists 1-3. In standard OR problems of this type (knapsack/discrete choice), if 0 is not listed, it's often not an option, OR it's implicitly 0. However, "keep three types" suggests at least one of each. Let's look at the costs. If we could choose 0, the cost would be 0. If we must choose from 1,2,3, the constraint $\sum x_{j,k}=1$ holds. If 0 is allowed, we add an option $k=0$ with $r=0, c=0$. Given "keep three types", it is safer to assume at least 1 is required. If the optimal solution wants 0, the budget constraint would allow it, but the "keep" language suggests presence. Let's stick to the provided table options 1, 2, 3.)*

**2. Budget Constraint:**
The total cost must not exceed the investment limit $B$.
$$
\sum_{j=1}^{3} \sum_{k=1}^{3} c_{j,k} \cdot x_{j,k} \le 8
$$

**3. Variable Domains:**
$$
x_{j,k} \in \{0, 1\}, \quad \forall j \in \{1, 2, 3\}, k \in \{1, 2, 3\}
$$

---
### Verification of Parameter Extraction
- **Budget**: 8,000 yuan = 8 thousand yuan. (Matches table unit).
- **Reliability values**: Extracted directly from table.
- **Cost values**: Extracted directly from table.
- **Objective**: Maximize sum of reliability increases.
- **Constraints**: One choice per item, total cost $\le$ 8.

### Feasibility Check
Minimum cost scenario (choose k=1 for all):
Cost = $1 + 3 + 2 = 6 \le 8$. Feasible.
Maximum cost scenario (choose k=3 for all):
Cost = $3 + 6 + 4 = 13 > 8$. Infeasible.
So the budget constraint is binding for some combinations.

### Final Model Summary

**Model Type:** MILP

**Sets:**
$J = \{1, 2, 3\}$
$K = \{1, 2, 3\}$

**Parameters:**
$r_{j,k}$ and $c_{j,k}$ as listed above.
$B = 8$.

**Variables:**
$x_{j,k} \in \{0, 1\}$

**Objective:**
Maximize $\sum_{j=1}^3 \sum_{k=1}^3 r_{j,k} x_{j,k}$

**Subject to:**
1. $\sum_{k=1}^3 x_{j,k} = 1, \quad \forall j \in J$
2. $\sum_{j=1}^3 \sum_{k=1}^3 c_{j,k} x_{j,k} \le 8$
3. $x_{j,k} \in \{0, 1\}, \quad \forall j \in J, k \in K$