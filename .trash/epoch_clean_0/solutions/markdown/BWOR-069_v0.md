### 1. Index Sets & Parameters

**Index Sets:**
- $I$: Set of product types, $I = \{1, 2, 3\}$.

**Parameters:**
- $w_i$: Weight of product type $i$ (tons/piece).
  - $w_1 = 2$
  - $w_2 = 3$
  - $w_3 = 4$
- $p_i$: Profit of product type $i$ (yuan/piece).
  - $p_1 = 100$
  - $p_2 = 140$
  - $p_3 = 180$
- $W_{max}$: Total transportation capacity (tons).
  - $W_{max} = 10$

### 2. Decision Variables

Let $x_i$ be the number of pieces of product type $i$ to be produced and shipped, for all $i \in I$.

**Domain:**
- Since the problem involves shipping discrete pieces of products, $x_i$ must be non-negative integers.
- $x_i \in \mathbb{Z}^{+}$ for all $i \in I$ (i.e., $x_i \ge 0$ and integer).

### 3. Objective Function

Maximize the total profit.

$$ \text{Maximize } Z = \sum_{i \in I} p_i x_i $$

Substituting the parameter values:
$$ \text{Maximize } Z = 100 x_1 + 140 x_2 + 180 x_3 $$

### 4. Operational Constraints

**Transportation Capacity Constraint:**
The total weight of all shipped products must not exceed the transportation capacity.

$$ \sum_{i \in I} w_i x_i \le W_{max} $$

Substituting the parameter values:
$$ 2 x_1 + 3 x_2 + 4 x_3 \le 10 $$

**Non-negativity and Integrality Constraints:**
$$ x_1, x_2, x_3 \in \mathbb{Z}^{+} $$
$$ x_1 \ge 0, \quad x_2 \ge 0, \quad x_3 \ge 0 $$