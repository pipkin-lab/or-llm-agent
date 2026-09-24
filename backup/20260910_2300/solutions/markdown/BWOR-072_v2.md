Here is the formal mathematical optimization model for the spare parts allocation problem.

### 1. Index Sets & Parameters

**Index Sets:**
*   $i$: Set of spare part types, $i \in \{1, 2, 3\}$ corresponding to $E_1, E_2, E_3$.
*   $k$: Set of possible discrete levels (number of spares) for each type, $k \in \{1, 2, 3\}$.

**Parameters (derived from Table 7-10):**
*   $B$: Total budget limit in thousand yuan. $B = 8$.
*   $r_{i,k}$: Increase in reliability for type $i$ when selecting level $k$.
    *   $r_{1,1}=0.3, r_{1,2}=0.4, r_{1,3}=0.5$
    *   $r_{2,1}=0.2, r_{2,2}=0.5, r_{2,3}=0.9$
    *   $r_{3,1}=0.1, r_{3,2}=0.2, r_{3,3}=0.7$
*   $c_{i,k}$: Cost (in thousand yuan) for type $i$ when selecting level $k$.
    *   $c_{1,1}=1, c_{1,2}=2, c_{1,3}=3$
    *   $c_{2,1}=3, c_{2,2}=5, c_{2,3}=6$
    *   $c_{3,1}=2, c_{3,2}=3, c_{3,3}=4$

### 2. Decision Variables

We use binary variables to select exactly one discrete level of spares for each part type.

*   $x_{i,k} \in \{0, 1\}$ for all $i \in \{1,2,3\}, k \in \{1,2,3\}$.
    *   $x_{i,k} = 1$ if we choose level $k$ (i.e., $k$ spares) for part type $i$.
    *   $x_{i,k} = 0$ otherwise.

### 3. Objective Function

Maximize the total increase in reliability of the equipment.

$$
\text{Maximize } Z = \sum_{i=1}^{3} \sum_{k=1}^{3} r_{i,k} x_{i,k}
$$

### 4. Operational Constraints

**Constraint 1: Selection Constraint**
Exactly one level (number of spares) must be selected for each part type.
$$
\sum_{k=1}^{3} x_{i,k} = 1 \quad \forall i \in \{1, 2, 3\}
$$

**Constraint 2: Budget Constraint**
The total cost of the selected spares must not exceed the budget limit ($8,000$ yuan = $8$ thousand yuan).
$$
\sum_{i=1}^{3} \sum_{k=1}^{3} c_{i,k} x_{i,k} \le 8
$$

**Constraint 3: Domain Constraints**
$$
x_{i,k} \in \{0, 1\} \quad \forall i \in \{1, 2, 3\}, k \in \{1, 2, 3\}
$$