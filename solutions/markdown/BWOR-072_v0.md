# Multi-Choice Knapsack Problem Formulation

## Model Type Declaration
**MILP** (Mixed Integer Linear Program). The decision variables represent discrete counts of spare parts (integers), and all objective/constraint terms are linear.

## Cost & Parameter Inventory (Pre-Modeling)
Extracting all numeric values from Table 7-10:
- **Budget Limit:** 8,000 yuan = 8 (thousand yuan).
- **Reliability Gains ($\Delta R$):**
  - $E_1$: $z=1 \to 0.3$, $z=2 \to 0.4$, $z=3 \to 0.5$
  - $E_2$: $z=1 \to 0.2$, $z=2 \to 0.5$, $z=3 \to 0.9$
  - $E_3$: $z=1 \to 0.1$, $z=2 \to 0.2$, $z=3 \to 0.7$
- **Costs ($C$, in thousand yuan):**
  - $E_1$: $z=1 \to 1$, $z=2 \to 2$, $z=3 \to 3$
  - $E_2$: $z=1 \to 3$, $z=2 \to 5$, $z=3 \to 6$
  - $E_3$: $z=1 \to 2$, $z=2 \to 3$, $z=3 \to 4$

*Note: The table provides marginal/level-specific data for $z=1, 2, 3$. In standard multi-choice knapsack formulations for this type of problem, the values in the "z=k" row represent the **total** reliability gain and **total** cost for purchasing $k$ units of that part type. If they were marginal, the problem would typically specify "additional". Given the context of "Increase in Reliability" listed alongside specific counts, and standard textbook conventions for this specific problem type (often found in Chinese OR textbooks), these are the **total** attributes for selecting exactly $z$ units. We model $x_{i,z} = 1$ if we select option $z$ for part $i$.*

## Index Sets & Parameters

**Index Sets:**
- $I = \{1, 2, 3\}$: Set of spare part types ($E_1, E_2, E_3$).
- $Z = \{1, 2, 3\}$: Set of possible quantity levels (number of spares).

**Parameters:**
- $B = 8$: Maximum total investment (thousand yuan).
- $r_{i,z}$: Total increase in reliability for part type $i$ when selecting quantity $z$ (from Table 7-10).
  - $r_{1,1}=0.3, r_{1,2}=0.4, r_{1,3}=0.5$
  - $r_{2,1}=0.2, r_{2,2}=0.5, r_{2,3}=0.9$
  - $r_{3,1}=0.1, r_{3,2}=0.2, r_{3,3}=0.7$
- $c_{i,z}$: Total cost (thousand yuan) for part type $i$ when selecting quantity $z$ (from Table 7-10).
  - $c_{1,1}=1, c_{1,2}=2, c_{1,3}=3$
  - $c_{2,1}=3, c_{2,2}=5, c_{2,3}=6$
  - $c_{3,1}=2, c_{3,2}=3, c_{3,3}=4$

## Decision Variables
Let $x_{i,z}$ be a binary variable defined for all $i \in I, z \in Z$:
$$
x_{i,z} = 
\begin{cases} 
1 & \text{if quantity } z \text{ is selected for part type } i \\
0 & \text{otherwise}
\end{cases}
$$
**Domain:** $x_{i,z} \in \{0, 1\} \quad \forall i \in I, z \in Z$.

*Note: The problem implies we must select exactly one quantity level for each part type. It does not explicitly state $z=0$ is allowed, but "keep three types of spare parts" suggests at least one of each might be required, OR it could mean we choose from the available options. However, standard interpretation of "optimal number of spares" with a table of options $z=1,2,3$ usually implies choosing one of these specific stock levels. Does $z=0$ exist? The table starts at $z=1$. If $z=0$ is allowed, it would have $r=0, c=0$. Let us assume the choice is restricted to the table entries $z \in \{1, 2, 3\}$. If the problem allowed 0 spares, it would usually be listed or implied by "up to". Given "keep three types", it is safer to assume we must pick one of the listed positive integers. If 0 were allowed, it would be a 4th option. Let's look at the phrasing: "optimal number of spares... shown in Table". The table only shows 1, 2, 3. We will constrain the choice to $z \in \{1, 2, 3\}$. If the optimal solution requires 0, the model as defined (forcing a choice of 1,2,3) would be incorrect. However, usually "spare parts" implies $z \ge 1$. Let's assume the domain of choice is strictly $\{1, 2, 3\}$ based on the table provided.*

## Objective Function
Maximize the total increase in reliability:
$$
\text{Maximize } Z_{obj} = \sum_{i \in I} \sum_{z \in Z} r_{i,z} x_{i,z}
$$
Substituting values:
$$
\text{Maximize } Z_{obj} = 0.3x_{1,1} + 0.4x_{1,2} + 0.5x_{1,3} + 0.2x_{2,1} + 0.5x_{2,2} + 0.9x_{2,3} + 0.1x_{3,1} + 0.2x_{3,2} + 0.7x_{3,3}
$$

## Operational Constraints

**1. Selection Constraint (Exactly one level per part type):**
For each part type $i$, exactly one quantity level $z$ must be chosen.
$$
\sum_{z \in Z} x_{i,z} = 1 \quad \forall i \in I
$$
Explicitly:
$$
x_{1,1} + x_{1,2} + x_{1,3} = 1
$$
$$
x_{2,1} + x_{2,2} + x_{2,3} = 1
$$
$$
x_{3,1} + x_{3,2} + x_{3,3} = 1
$$

**2. Budget Constraint:**
The total cost must not exceed the budget limit of 8 thousand yuan.
$$
\sum_{i \in I} \sum_{z \in Z} c_{i,z} x_{i,z} \le 8
$$
Explicitly:
$$
1x_{1,1} + 2x_{1,2} + 3x_{1,3} + 3x_{2,1} + 5x_{2,2} + 6x_{2,3} + 2x_{3,1} + 3x_{3,2} + 4x_{3,3} \le 8
$$

**3. Variable Bounds:**
$$
x_{i,z} \in \{0, 1\} \quad \forall i \in \{1, 2, 3\}, z \in \{1, 2, 3\}
$$

---
### Feasibility Sanity Check
Let's check if the constraint that $z \ge 1$ makes sense.
Minimum cost per part if we pick the cheapest option for each:
- $E_1$: min cost 1 ($z=1$)
- $E_2$: min cost 3 ($z=1$)
- $E_3$: min cost 2 ($z=1$)
Total min cost = $1+3+2 = 6 \le 8$. Feasible.

If $z=0$ were allowed, we could potentially save cost to buy more of others, but the table doesn't define $z=0$. In many such textbook problems, the "number of spares" is chosen from the discrete set provided. If the problem intended $z \in \{0,1,2,3\}$, the $z=0$ row would typically be implicit (cost 0, gain 0). However, since the table explicitly lists "Number of Spares" starting at 1, and the prompt asks for the "optimal number", it is standard to interpret the available options as those listed. If the optimal solution turns out to be a combination of the lowest levels, that is the answer.

### Objective Parameter Cross-Reference
- $r_{1,1}=0.3$ (Found in Table)
- $r_{1,2}=0.4$ (Found in Table)
- $r_{1,3}=0.5$ (Found in Table)
- $r_{2,1}=0.2$ (Found in Table)
- $r_{2,2}=0.5$ (Found in Table)
- $r_{2,3}=0.9$ (Found in Table)
- $r_{3,1}=0.1$ (Found in Table)
- $r_{3,2}=0.2$ (Found in Table)
- $r_{3,3}=0.7$ (Found in Table)
- $B=8$ (Found in text "8,000 yuan")

All parameters are accounted for. No [NOT_PROVIDED] values.

### Final Answer Structure
The optimal solution will be a vector $(z_1^*, z_2^*, z_3^*)$ where $z_i^*$ is the index $z$ such that $x_{i,z_i^*}=1$.