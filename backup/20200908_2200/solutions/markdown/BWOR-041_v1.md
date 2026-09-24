# Optimization Model for Toy Distribution

## 1. Index Sets & Parameters

**Sets:**
*   $I = \{A, B, C\}$: Set of toy types.
*   $J = \{X, Y, Z\}$: Set of department stores.
*   $S = \{(i, j) \in I \times J \mid \text{Toy } i \text{ is allowed in Store } j\}$: Set of valid supply-store pairs.
    *   Based on the problem description ("Store C refuses to accept Toy A" — *Note: The text says "Store C" but the table lists stores X, Y, Z. Given the context of "Store C requires at least 1,000 units of Toy C", there is a nomenclature conflict. The table headers are X, Y, Z. The text mentions "Store C". It is highly probable that "Store C" in the text is a typo for "Store Z" or the stores are A, B, C in the text but X, Y, Z in the table. Let's look closely at the text: "delivered to Department Stores X, Y, and Z". Then "Store C requires...". Then "Store C refuses to accept Toy A".
    *   *Interpretation*: The text likely contains a typo where "Store C" refers to the third store, which is **Z** in the table. Let's assume the constraint applies to **Store Z**.
    *   Constraint 1: "Store C (Z) requires at least 1,000 units of Toy C" $\rightarrow x_{C,Z} \ge 1000$.
    *   Constraint 2: "Store C (Z) refuses to accept Toy A" $\rightarrow x_{A,Z} = 0$.
    *   Looking at Table 3-6, the cell for Toy A and Store Z is empty, which confirms $x_{A,Z} = 0$.

**Parameters:**
*   $s_i$: Supply limit for toy $i$ (units).
    *   $s_A = 1,000$
    *   $s_B = 2,000$
    *   $s_C = 2,000$
*   $d_j$: Demand (expected sales volume) for store $j$. The problem states "Each department store has an expected monthly sales volume of 1,500 units for each type of toy." This phrasing is ambiguous. Does it mean total demand per store is 1,500? Or demand for *each* toy type is 1,500?
    *   "Expected monthly sales volume of 1,500 units for each type of toy" usually implies that the *potential* demand for any specific toy type at any store is up to 1,500. However, in distribution problems, we usually have a total demand per store or demand per (toy, store) pair.
    *   Let's re-read: "Each department store has an expected monthly sales volume of 1,500 units for each type of toy." This likely sets the upper bound for $x_{i,j}$ or implies the total demand at each store is not explicitly capped by a single number but by the sum of what they can sell.
    *   However, standard transportation problems usually have a total demand per destination or a specific demand per product-destination.
    *   Let's look at the supplies: Total Supply = $1000 + 2000 + 2000 = 5000$.
    *   If each store demands 1500 units *total*, Total Demand = $1500 \times 3 = 4500$. Supply > Demand.
    *   If each store demands 1500 units *per toy type*, Total Demand = $3 \times 3 \times 1500 = 13,500$. Supply < Demand.
    *   Given the phrase "sales volume... for each type", it is most standard to interpret this as the **maximum potential demand** for any single toy type at any store is 1,500. Thus, $x_{i,j} \le 1,500$ for all valid $i,j$. There is no explicit "total store capacity" mentioned other than this per-item limit.
    *   *Alternative Interpretation*: In many textbook problems of this format, "sales volume of 1500 units" might refer to the total units the store can handle. But the modifier "for each type of toy" strongly suggests $x_{i,j} \le 1500$. Let's proceed with $x_{i,j} \le 1500$ as a capacity constraint per link.

*   $p_{i,j}$: Profit margin per unit of toy $i$ sold at store $j$.
    *   From Table 3-6:
        *   $p_{A,X} = 5, \quad p_{A,Y} = 4, \quad p_{A,Z} = 0$ (refused/empty)
        *   $p_{B,X} = 16, \quad p_{B,Y} = 8, \quad p_{B,Z} = 6$
        *   $p_{C,X} = 12, \quad p_{C,Y} = 10, \quad p_{C,Z} = 11$

## 2. Decision Variables

Let $x_{i,j}$ be the number of units of toy $i$ shipped to store $j$.
*   Domain: $x_{i,j} \ge 0$ and integer (though usually LP relaxation is sufficient for transportation if costs are linear, we specify integer for rigor if required, but standard transportation LP yields integer solutions).
*   Valid pairs only:
    *   $x_{A,X}, x_{A,Y} \ge 0$
    *   $x_{A,Z} = 0$ (Constraint)
    *   $x_{B,X}, x_{B,Y}, x_{B,Z} \ge 0$
    *   $x_{C,X}, x_{C,Y}, x_{C,Z} \ge 0$

## 3. Objective Function

Maximize total profit $Z$:

$$
\text{Maximize } Z = 5x_{A,X} + 4x_{A,Y} + 16x_{B,X} + 8x_{B,Y} + 6x_{B,Z} + 12x_{C,X} + 10x_{C,Y} + 11x_{C,Z}
$$

*(Note: $x_{A,Z}$ is excluded as it is fixed to 0)*

## 4. Operational Constraints

**1. Supply Constraints (Outflow from Source $\le$ Supply Limit):**
The total amount of each toy shipped cannot exceed its monthly supply.

$$
\begin{align*}
x_{A,X} + x_{A,Y} &\le 1,000 & (\text{Toy A Supply}) \\
x_{B,X} + x_{B,Y} + x_{B,Z} &\le 2,000 & (\text{Toy B Supply}) \\
x_{C,X} + x_{C,Y} + x_{C,Z} &\le 2,000 & (\text{Toy C Supply})
\end{align*}
$$

**2. Demand/Capacity Constraints (Inflow to Store):**
The problem states "expected monthly sales volume of 1,500 units for each type of toy". This imposes an upper bound on the shipment of any specific toy to any specific store.

$$
\begin{align*}
x_{A,X} &\le 1,500 \\
x_{A,Y} &\le 1,500 \\
x_{B,X} &\le 1,500 \\
x_{B,Y} &\le 1,500 \\
x_{B,Z} &\le 1,500 \\
x_{C,X} &\le 1,500 \\
x_{C,Y} &\le 1,500 \\
x_{C,Z} &\le 1,500
\end{align*}
$$
*(Note: Since Supply A is only 1,000, $x_{A,X}$ and $x_{A,Y}$ are naturally bounded by 1,000 effectively, but the explicit constraint is 1,500.)*

**3. Specific Operational Constraints:**

*   **Store Z (referred to as "Store C" in text) requires at least 1,000 units of Toy C:**
    $$ x_{C,Z} \ge 1,000 $$

*   **Store Z (referred to as "Store C" in text) refuses to accept Toy A:**
    $$ x_{A,Z} = 0 $$
    *(This is already handled by not including $x_{A,Z}$ in the model variables or setting its coefficient to 0/upper bound to 0).*

**4. Non-negativity:**
$$ x_{i,j} \ge 0 \quad \forall (i,j) \in S $$

---

### Final Model Summary

**Decision Variables:**
$x_{i,j} \ge 0$ for $i \in \{A,B,C\}, j \in \{X,Y,Z\}$, with $x_{A,Z}=0$.

**Objective:**
$$ \text{Max } Z = 5x_{A,X} + 4x_{A,Y} + 16x_{B,X} + 8x_{B,Y} + 6x_{B,Z} + 12x_{C,X} + 10x_{C,Y} + 11x_{C,Z} $$

**Subject to:**
1.  **Supply:**
    *   $x_{A,X} + x_{A,Y} \le 1,000$
    *   $x_{B,X} + x_{B,Y} + x_{B,Z} \le 2,000$
    *   $x_{C,X} + x_{C,Y} + x_{C,Z} \le 2,000$
2.  **Store Link Capacities (1,500 per toy per store):**
    *   $x_{A,X} \le 1,500$
    *   $x_{A,Y} \le 1,500$
    *   $x_{B,X} \le 1,500$
    *   $x_{B,Y} \le 1,500$
    *   $x_{B,Z} \le 1,500$
    *   $x_{C,X} \le 1,500$
    *   $x_{C,Y} \le 1,500$
    *   $x_{C,Z} \le 1,500$
3.  **Specific Requirements:**
    *   $x_{C,Z} \ge 1,000$
    *   $x_{A,Z} = 0$