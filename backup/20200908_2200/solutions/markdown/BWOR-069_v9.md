### 1. Index Sets & Parameters

**Index Sets:**
*   $i \in \{1, 2, 3\}$: Set of product types.

**Parameters:**
*   $w_i$: Weight of product type $i$ (tons/piece).
    *   $w_1 = 2$
    *   $w_2 = 3$
    *   $w_3 = 4$
*   $p_i$: Profit of product type $i$ (yuan/piece).
    *   $p_1 = 100$
    *   $p_2 = 140$
    *   $p_3 = 180$
*   $W_{max}$: Maximum total transportation capacity (tons).
    *   $W_{max} = 10$

### 2. Decision Variables

Let $x_i$ be the number of pieces of product type $i$ to be produced/shipped.

*   **Domain**: Since we are dealing with discrete items (pieces of product) and the scale is small (maximum possible units for product 1 is 5), the variables must be **Non-negative Integers**.
    *   $x_i \in \mathbb{Z}_{\ge 0}, \quad \forall i \in \{1, 2, 3\}$

### 3. Objective Function

Maximize the total profit $Z$.

$$ \text{Maximize } Z = 100x_1 + 140x_2 + 180x_3 $$

### 4. Operational Constraints

**Capacity Constraint:**
The total weight of all shipped products must not exceed the transportation capacity of 10 tons.

$$ 2x_1 + 3x_2 + 4x_3 \le 10 $$

**Non-negativity and Integrality Constraints:**
$$ x_1, x_2, x_3 \in \mathbb{Z}_{\ge 0} $$

***

**Model Summary (MILP):**

$$
\begin{aligned}
\text{Maximize} \quad & Z = 100x_1 + 140x_2 + 180x_3 \\
\text{Subject to} \quad & 2x_1 + 3x_2 + 4x_3 \le 10 \\
& x_1, x_2, x_3 \in \mathbb{Z}_{\ge 0}
\end{aligned}
$$