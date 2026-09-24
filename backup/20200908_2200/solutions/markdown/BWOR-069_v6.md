Here is the formal mathematical optimization model for the factory production and shipping problem.

### 1. Index Sets & Parameters

**Index Sets:**
*   $J$: Set of product types, where $J = \{1, 2, 3\}$.

**Parameters:**
*   $w_j$: Weight of one piece of product $j$ (tons/piece).
    *   $w_1 = 2$
    *   $w_2 = 3$
    *   $w_3 = 4$
*   $p_j$: Profit of one piece of product $j$ (yuan/piece).
    *   $p_1 = 100$
    *   $p_2 = 140$
    *   $p_3 = 180$
*   $W_{max}$: Maximum total transportation capacity (tons).
    *   $W_{max} = 10$

### 2. Decision Variables

Let $x_j$ be the number of pieces of product $j$ to be produced and shipped.

*   **Domain:** Since the problem involves counting discrete physical units (pieces) of products, and the quantities involved are small (bounded by $10/2=5$), the variables must be **non-negative integers**.
*   $x_j \in \mathbb{Z}_{\ge 0} \quad \forall j \in J$

### 3. Objective Function

The goal is to **maximize** the total profit.

$$ \text{Maximize } Z = \sum_{j \in J} p_j x_j $$

Substituting the values:
$$ \text{Maximize } Z = 100x_1 + 140x_2 + 180x_3 $$

### 4. Operational Constraints

**Transportation Capacity Constraint:**
The total weight of all shipped products must not exceed the maximum transportation capacity.

$$ \sum_{j \in J} w_j x_j \le W_{max} $$

Substituting the values:
$$ 2x_1 + 3x_2 + 4x_3 \le 10 $$

**Non-negativity and Integrality Constraints:**
The number of pieces produced for each product type must be a non-negative integer.

$$ x_j \in \{0, 1, 2, \dots\} \quad \forall j \in \{1, 2, 3\} $$

---

### Summary of the Model (MILP)

$$
\begin{aligned}
\text{Maximize } \quad & 100x_1 + 140x_2 + 180x_3 \\
\text{Subject to: } \quad & 2x_1 + 3x_2 + 4x_3 \le 10 \\
& x_1, x_2, x_3 \in \mathbb{Z}_{\ge 0}
\end{aligned}
$$

**Verification of Data Completeness:**
*   Weights ($2, 3, 4$) are provided.
*   Profits ($100, 140, 180$) are provided.
*   Capacity limit ($10$) is provided.
*   No other constraints (like minimum production levels or demand limits) are mentioned, so the model is complete based on the provided text.