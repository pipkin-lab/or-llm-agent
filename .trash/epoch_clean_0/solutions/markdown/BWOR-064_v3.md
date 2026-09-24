## Index Sets & Parameters

**Index Sets:**
- $I = \{1, 2, 3\}$: Set of factories.
- $J_i \subseteq J$: Set of available renovation plans for factory $i$.
  - $J_1 = \{1, 2, 3\}$
  - $J_2 = \{1, 2, 3, 4\}$
  - $J_3 = \{1, 2\}$
- $J = \{1, 2, 3, 4\}$: Set of all plan indices.

**Parameters:**
- $C = 5$: Total available budget (million yuan).
- $a_{i,j}$: Investment cost for plan $j$ at factory $i$ (million yuan).
- $r_{i,j}$: Expected return for plan $j$ at factory $i$ (million yuan).

**Data Extraction from Table 7-4:**

| Factory $i$ | Plan $j$ | Investment $a_{i,j}$ | Return $r_{i,j}$ |
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

*Note: Plans marked with "–" are excluded from $J_i$. Plan 1 for all factories represents the "no investment" option with 0 cost and 0 return.*

## Decision Variables

Let $x_{i,j}$ be a binary variable for each factory $i \in I$ and available plan $j \in J_i$:

$$
x_{i,j} = \begin{cases} 
1 & \text{if plan } j \text{ is selected for factory } i \\
0 & \text{otherwise}
\end{cases}
$$

**Domain:**
$$ x_{i,j} \in \{0, 1\} \quad \forall i \in I, \forall j \in J_i $$

## Objective Function

Maximize the total expected return:

$$
\text{Maximize } Z = \sum_{i \in I} \sum_{j \in J_i} r_{i,j} x_{i,j}
$$

Substituting the specific values:
$$
\text{Maximize } Z = 5x_{1,2} + 6x_{1,3} + 8x_{2,2} + 9x_{2,3} + 12x_{2,4} + 3x_{3,2}
$$
*(Note: Terms with $r_{i,j}=0$ such as $x_{1,1}, x_{2,1}, x_{3,1}$ do not affect the objective function value but are necessary for constraints.)*

## Operational Constraints

**1. Single Selection Constraint (Mutual Exclusivity):**
Exactly one plan must be chosen for each factory. This includes the option of choosing Plan 1 (no investment).

$$
\sum_{j \in J_i} x_{i,j} = 1 \quad \forall i \in I
$$

Explicitly:
- Factory 1: $x_{1,1} + x_{1,2} + x_{1,3} = 1$
- Factory 2: $x_{2,1} + x_{2,2} + x_{2,3} + x_{2,4} = 1$
- Factory 3: $x_{3,1} + x_{3,2} = 1$

**2. Budget Constraint:**
The total investment across all factories must not exceed the available budget of 5 million yuan.

$$
\sum_{i \in I} \sum_{j \in J_i} a_{i,j} x_{i,j} \le C
$$

Substituting the specific values:
$$
1x_{1,2} + 2x_{1,3} + 2x_{2,2} + 3x_{2,3} + 4x_{2,4} + 1x_{3,2} \le 5
$$
*(Note: Investment for Plan 1 is 0, so those terms are omitted.)*

**3. Non-negativity and Integrality:**
$$
x_{i,j} \in \{0, 1\} \quad \forall i \in I, \forall j \in J_i
$$