This is a **Mixed Integer Linear Programming (MILP)** problem because we need to decide *which* equipment to operate (binary decisions) and *how much* to produce (continuous/integer production quantities). Since production quantities are typically integer units in garment manufacturing, we will use integer variables for production, though in large-scale LP relaxations they are often treated as continuous. Given the context of "designing a production plan" with specific equipment, binary variables for equipment usage are critical.

### **MODEL TYPE DECLARATION**
**MILP** (Mixed Integer Linear Programming)

---

### **Index Sets & Parameters**

**1. Index Sets:**
*   $P = \{1, 2, 3\}$: Set of products.
    *   $1$: Shirt
    *   $2$: T-shirt
    *   $3$: Casual Wear

**2. Parameters (from Table 5-10 and text):**

| Parameter Symbol | Description | Product 1 (Shirt) | Product 2 (T-shirt) | Product 3 (Casual Wear) |
| :--- | :--- | :---: | :---: | :---: |
| $a_i$ | Labor per unit | 3 | 2 | 6 |
| $b_i$ | Material per unit | 4 | 3 | 6 |
| $p_i$ | Selling price per unit | 120 | 80 | 180 |
| $c_i$ | Variable cost per unit | 60 | 40 | 80 |
| $F_i$ | Fixed cost for equipment | 2,000 | 1,500 | 1,000 |

**Resource Availability:**
*   $L_{total} = 150$: Total weekly labor units available.
*   $M_{total} = 160$: Total weekly material units available.

**Derived Parameter:**
*   $m_i = p_i - c_i$: Unit contribution margin (profit per unit before fixed costs).
    *   $m_1 = 120 - 60 = 60$
    *   $m_2 = 80 - 40 = 40$
    *   $m_3 = 180 - 80 = 100$

---

### **Decision Variables**

1.  **Production Quantities:**
    *   $x_i \ge 0$: Integer variable representing the number of units of product $i$ produced per week, for $i \in P$.
    *   *Note: If fractional production is allowed (e.g., large batches), these can be continuous. However, "units" usually implies integers. We will define them as **Integer** to be safe for physical units, though the LP relaxation is often acceptable in textbook OR contexts. Given the small numbers, integer is appropriate.*

2.  **Equipment Operation Indicators:**
    *   $y_i \in \{0, 1\}$: Binary variable for equipment of product $i$.
        *   $y_i = 1$ if the specialized equipment for product $i$ is operated (i.e., if we produce any amount of product $i$).
        *   $y_i = 0$ if the equipment is not operated (i.e., production is zero).

---

### **Objective Function**

Maximize total weekly profit.
Profit = (Total Contribution Margin) - (Total Fixed Costs)

$$
\text{Maximize } Z = \sum_{i=1}^{3} m_i x_i - \sum_{i=1}^{3} F_i y_i
$$

Substituting values:
$$
\text{Maximize } Z = 60 x_1 + 40 x_2 + 100 x_3 - 2000 y_1 - 1500 y_2 - 1000 y_3
$$

---

### **Operational Constraints**

**1. Resource Constraints:**
The total labor and material used by all produced items cannot exceed the weekly availability.

*   **Labor Constraint:**
    $$
    3 x_1 + 2 x_2 + 6 x_3 \le 150
    $$

*   **Material Constraint:**
    $$
    4 x_1 + 3 x_2 + 6 x_3 \le 160
    $$

**2. Logical Linking Constraints (Big-M / Linking):**
Production of product $i$ is only possible if the corresponding equipment is operated ($y_i = 1$). Conversely, if $y_i = 0$, then $x_i$ must be 0.
We need an upper bound $U_i$ for each $x_i$ to link $x_i$ and $y_i$. We can determine a simple upper bound for each $x_i$ based on the most restrictive resource if produced in isolation.

*   **Upper Bound for Shirt ($x_1$):**
    *   Labor limit: $150 / 3 = 50$
    *   Material limit: $160 / 4 = 40$
    *   $U_1 = 40$
    *   Constraint: $x_1 \le 40 y_1$

*   **Upper Bound for T-shirt ($x_2$):**
    *   Labor limit: $150 / 2 = 75$
    *   Material limit: $160 / 3 = 53.33 \rightarrow 53$
    *   $U_2 = 53$
    *   Constraint: $x_2 \le 53 y_2$

*   **Upper Bound for Casual Wear ($x_3$):**
    *   Labor limit: $150 / 6 = 25$
    *   Material limit: $160 / 6 = 26.66 \rightarrow 26$
    *   $U_3 = 25$ (Labor is more restrictive here)
    *   Constraint: $x_3 \le 25 y_3$

**3. Non-negativity and Integrality:**
*   $x_i \in \mathbb{Z}^+ \cup \{0\}$ for $i = 1, 2, 3$ (Non-negative integers)
*   $y_i \in \{0, 1\}$ for $i = 1, 2, 3$ (Binary)

---

### **Final Model Summary**

**Model Type:** MILP

**Sets & Indices:**
*   $i \in \{1, 2, 3\}$ corresponding to Shirt, T-shirt, Casual Wear.

**Parameters:**
*   Contribution Margins: $m = [60, 40, 100]$
*   Fixed Costs: $F = [2000, 1500, 1000]$
*   Labor Coefficients: $a = [3, 2, 6]$
*   Material Coefficients: $b = [4, 3, 6]$
*   Resource Limits: $L_{max} = 150, M_{max} = 160$
*   Max Production Bounds (for linking): $U = [40, 53, 25]$

**Variables:**
*   $x_1, x_2, x_3$: Non-negative integers.
*   $y_1, y_2, y_3$: Binary variables.

**Objective:**
$$ \text{Max } Z = 60x_1 + 40x_2 + 100x_3 - 2000y_1 - 1500y_2 - 1000y_3 $$

**Subject to:**
1.  $3x_1 + 2x_2 + 6x_3 \le 150$  (Labor)
2.  $4x_1 + 3x_2 + 6x_3 \le 160$  (Material)
3.  $x_1 \le 40 y_1$
4.  $x_2 \le 53 y_2$
5.  $x_3 \le 25 y_3$
6.  $x_1, x_2, x_3 \ge 0$ and integer
7.  $y_1, y_2, y_3 \in \{0, 1\}$