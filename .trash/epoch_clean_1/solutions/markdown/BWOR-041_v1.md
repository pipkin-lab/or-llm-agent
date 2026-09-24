# Operations Research Model: Toy Distribution Problem

## 1. Problem Analysis & Pre-processing

**Entities:**
- **Products (Toys):** A, B, C
- **Stores (Demand Locations):** X, Y, Z

**Data Extraction from Table 3-6 (Profit Margins per unit):**
- Toy A: $p_{A,X}=5$, $p_{A,Y}=4$, $p_{A,Z}=\text{N/A}$
- Toy B: $p_{B,X}=16$, $p_{B,Y}=8$, $p_{B,Z}=6$
- Toy C: $p_{C,X}=12$, $p_{C,Y}=10$, $p_{C,Z}=11$

**Supply Capacities (Source Limits):**
- Toy A: 1,000 units
- Toy B: 2,000 units
- Toy C: 2,000 units

**Demand Requirements (Store Limits):**
- The problem states "expected monthly sales volume of 1,500 units for *each* type of toy". In distribution problems, this typically implies that the total demand for each toy type across all stores is 1,500 units. Alternatively, it could mean each store wants 1,500 of each toy, but since total supply is limited (1000, 2000, 2000), we must treat these as **demand limits** (maximum sales) or **exact demands** if the supply were sufficient.
    - *Correction/Refinement:* Standard interpretation of "sales volume of 1,500 units for each type" in the context of limited supply usually means the **total market demand** for Toy A is 1,500, for Toy B is 1,500, and for Toy C is 1,500. However, looking at the supply (1000, 2000, 2000), Toy A supply (1000) < Demand (1500). Toys B and C have Supply > Demand.
    - *Alternative Interpretation:* The text says "Each department store has an expected monthly sales volume of 1,500 units for each type of toy." This phrasing is ambiguous. It could mean $D_{i,j} = 1500$ for all $i,j$. If so, Total Demand for A = 4500, B = 4500, C = 4500. But Supply is only 1000/2000/2000. This would make the problem infeasible if demands are hard constraints, or simply means we sell as much as possible up to these caps.
    - *Most Logical Interpretation for OR Models:* The "1,500 units" usually refers to the **total demand per toy type** in the market, OR the **maximum capacity of each store to sell a specific toy**. Given the phrasing "Each department store... 1,500 units for each type", it likely means each store has a **maximum sales capacity of 1,500 units for any single toy type**.
    - Let's assume **Demand Constraints**: The total amount of Toy $i$ sold to Store $j$ cannot exceed 1,500. Also, the total amount of Toy $i$ sold cannot exceed the Supply.
    - *Wait, let's re-read carefully:* "Each department store has an expected monthly sales volume of 1,500 units for each type of toy." This is a standard way of describing **Demand**. Usually, if supply < demand, we maximize profit subject to supply limits. If supply > demand, we satisfy demand.
    - Let's look at the specific constraints:
        1. Store Z (referred to as "Store C" in the text constraint, but the table headers are X, Y, Z. The text says "Store C requires... Store C refuses...". This is a typo in the problem statement. The stores are X, Y, Z. The constraint says "Store C requires at least 1,000 units of Toy C". It is highly probable that "Store C" in the text refers to **Store Z** (the third store) or there is a naming mismatch. Let's look at the table: Stores are X, Y, Z. The text says "Store C". Given the order X, Y, Z, and the constraint "Store C refuses to accept Toy A", let's check the table. Toy A has no value for Z (blank). This strongly implies **Store Z** is the one that refuses Toy A. Therefore, **"Store C" in the text constraints is a typo for "Store Z"**.
        2. Constraint: Store Z requires at least 1,000 units of Toy C.
        3. Constraint: Store Z refuses Toy A ($x_{A,Z} = 0$).

**Assumptions for Formulation:**
1.  **Variables:** Continuous or Integer? Toys are discrete units. However, in large-scale LP formulations for such problems, they are often treated as continuous for simplicity, but since units are small (1000s), **Integer** is technically correct. Given the request for LP/MILP, and "units" are discrete, we will define them as **Non-negative Integers**. *Self-correction*: In many textbook examples of this size, if not specified, Continuous is often accepted for LP, but "units" implies Integer. I will specify **Integer** to be rigorous, but note that if the solver treats them as continuous, the solution will likely be integer anyway due to the totally unimodular nature of transportation problems (if balanced). Since supply/demand are integers, the LP relaxation yields integer solutions. I will define them as **Continuous** for the standard Transportation LP formulation, as this is the standard OR approach for this problem type, but add a note. Actually, Rule 2 says "Use INTEGER variables for discrete physical units". I will use **Integer**.

2.  **Demand/Sales Limits:**
    - Supply limits for each Toy $i$: $\sum_j x_{i,j} \le S_i$.
    - Sales limits: The text says "expected monthly sales volume of 1,500 units for each type of toy" for *each* store. This implies a constraint $x_{i,j} \le 1500$ for all $i,j$.
    - Is there a total demand constraint? Usually, if there is a "sales volume", it acts as an upper bound on sales. We want to maximize profit, so we will sell as much as possible up to these limits and supply limits.

3.  **Specific Constraints:**
    - $x_{A,Z} = 0$ (Store Z refuses Toy A).
    - $x_{C,Z} \ge 1000$ (Store Z requires at least 1,000 units of Toy C).

## 2. Mathematical Formulation

### Index Sets
-   $I = \{A, B, C\}$ : Set of toy types.
-   $J = \{X, Y, Z\}$ : Set of department stores.

### Parameters
-   $c_{i,j}$ : Profit margin (in currency units) for selling one unit of toy $i$ to store $j$.
    -   From Table 3-6:
        -   $c_{A,X}=5, c_{A,Y}=4, c_{A,Z}=-\infty$ (or handled via constraint)
        -   $c_{B,X}=16, c_{B,Y}=8, c_{B,Z}=6$
        -   $c_{C,X}=12, c_{C,Y}=10, c_{C,Z}=11$
-   $S_i$ : Maximum monthly supply (units) for toy $i$.
    -   $S_A = 1000$
    -   $S_B = 2000$
    -   $S_C = 2000$
-   $D_{i,j}$ : Maximum monthly sales capacity (units) for toy $i$ at store $j$.
    -   $D_{i,j} = 1500$ for all $i \in I, j \in J$.
-   $L_{C,Z}$ : Minimum required units of Toy C for Store Z.
    -   $L_{C,Z} = 1000$

### Decision Variables
-   $x_{i,j}$ : Number of units of toy $i$ shipped from the central supply to store $j$.
    -   Domain: $x_{i,j} \in \mathbb{Z}_{\ge 0}$ (Non-negative Integers)

### Objective Function
Maximize total profit $Z$:

$$
\text{Maximize } Z = \sum_{i \in I} \sum_{j \in J} c_{i,j} x_{i,j}
$$

Expanded:
$$
Z = 5x_{A,X} + 4x_{A,Y} + 16x_{B,X} + 8x_{B,Y} + 6x_{B,Z} + 12x_{C,X} + 10x_{C,Y} + 11x_{C,Z}
$$
*(Note: $x_{A,Z}$ is excluded as it is constrained to 0)*

### Operational Constraints

**1. Supply Constraints (Outflow from Source):**
The total amount of each toy shipped cannot exceed its available supply.

$$
\begin{aligned}
\sum_{j \in J} x_{A,j} &\le 1000 &\Rightarrow \quad x_{A,X} + x_{A,Y} + x_{A,Z} &\le 1000 \\
\sum_{j \in J} x_{B,j} &\le 2000 &\Rightarrow \quad x_{B,X} + x_{B,Y} + x_{B,Z} &\le 2000 \\
\sum_{j \in J} x_{C,j} &\le 2000 &\Rightarrow \quad x_{C,X} + x_{C,Y} + x_{C,Z} &\le 2000
\end{aligned}
$$

**2. Sales Capacity Constraints (Inflow to Stores):**
The amount of any specific toy sold to any specific store cannot exceed the store's sales capacity for that toy (1,500 units).

$$
x_{i,j} \le 1500 \quad \forall i \in I, j \in J
$$

**3. Specific Operational Constraints:**
-   Store Z refuses Toy A:
    $$ x_{A,Z} = 0 $$
-   Store Z requires at least 1,000 units of Toy C:
    $$ x_{C,Z} \ge 1000 $$

**4. Non-negativity and Integrality:**
$$
x_{i,j} \in \mathbb{Z}_{\ge 0} \quad \forall i \in I, j \in J
$$

---

### Final Model Summary

**Sets:**
$I = \{A, B, C\}$, $J = \{X, Y, Z\}$

**Parameters:**
$c_{A,X}=5, c_{A,Y}=4$
$c_{B,X}=16, c_{B,Y}=8, c_{B,Z}=6$
$c_{C,X}=12, c_{C,Y}=10, c_{C,Z}=11$
$S_A=1000, S_B=2000, S_C=2000$
$U_{i,j}=1500 \forall i,j$

**Variables:**
$x_{i,j} \ge 0, \text{ Integer}$

**Objective:**
$$ \text{Maximize } Z = 5x_{A,X} + 4x_{A,Y} + 16x_{B,X} + 8x_{B,Y} + 6x_{B,Z} + 12x_{C,X} + 10x_{C,Y} + 11x_{C,Z} $$

**Subject to:**
1.  **Supply A:** $x_{A,X} + x_{A,Y} \le 1000$
2.  **Supply B:** $x_{B,X} + x_{B,Y} + x_{B,Z} \le 2000$
3.  **Supply C:** $x_{C,X} + x_{C,Y} + x_{C,Z} \le 2000$
4.  **Store Capacity:** $x_{i,j} \le 1500$ for all $i \in I, j \in J$
5.  **Refusal:** $x_{A,Z} = 0$
6.  **Minimum Demand:** $x_{C,Z} \ge 1000$
7.  **Integrality:** $x_{i,j} \in \mathbb{Z}^+$