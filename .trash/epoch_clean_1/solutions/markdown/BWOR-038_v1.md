# Operations Research Model: Hongsheng Factory Production Planning

## 1. Analysis and Data Extraction

**Objective:** Maximize Total Profit.
**Profit Calculation:**
Profit per unit = Selling Price - Raw Material Cost - Total Processing Cost.
Since processing costs are given per hour and depend on the specific machine used, the objective function will be formulated directly using revenue and explicit cost terms (raw material + machine processing time $\times$ machine rate).

**Data from Table 1-20:**

*   **Products:** $I, II, III$
*   **Machines:**
    *   Stage A: $A_1, A_2$
    *   Stage B: $B_1, B_2, B_3$
*   **Processing Times (hours/unit):**
    *   Product I: $A_1=5, A_2=7$; $B_1=6, B_2=4, B_3=7$
    *   Product II: $A_1=10, A_2=9$; $B_2=8$ (Only $B_2$ allowed)
    *   Product III: $A_2=12$ (Only $A_2$ allowed); $B_2=11$ (Only $B_2$ allowed)
    *   *Note: Empty cells in the table indicate the product cannot be processed on that machine.*
*   **Machine Available Hours:**
    *   $A_1: 6,000$
    *   $A_2: 10,000$
    *   $B_1: 4,000$
    *   $B_2: 7,000$
    *   $B_3: 4,000$
*   **Processing Cost Rates (yuan/hour):**
    *   $A_1: 0.05$
    *   $A_2: 0.03$
    *   $B_1: 0.06$
    *   $B_2: 0.11$
    *   $B_3: 0.05$
*   **Raw Material Cost (yuan/unit):**
    *   $I: 0.25$
    *   $II: 0.35$
    *   $III: 0.50$
*   **Selling Price (yuan/unit):**
    *   $I: 1.25$
    *   $II: 2.00$
    *   $III: 2.80$

**Variable Nature:**
Production quantities are continuous (standard assumption for such LP problems unless "integer" is specified, as units are divisible in aggregate planning contexts; however, if discrete units are required, they would be integer. Given the scale (thousands of hours), continuous variables are standard for this type of textbook LP problem). We will define them as continuous non-negative variables.

## 2. Index Sets & Parameters

### Sets
*   $P = \{1, 2, 3\}$: Set of products (I, II, III).
*   $M_A = \{A_1, A_2\}$: Set of Stage A machines.
*   $M_B = \{B_1, B_2, B_3\}$: Set of Stage B machines.
*   $M = M_A \cup M_B$: Set of all machines.

### Parameters
*   $p_k$: Selling price of product $k$ (yuan/unit).
    *   $p_1 = 1.25, p_2 = 2.00, p_3 = 2.80$
*   $r_k$: Raw material cost of product $k$ (yuan/unit).
    *   $r_1 = 0.25, r_2 = 0.35, r_3 = 0.50$
*   $c_m$: Processing cost rate of machine $m$ (yuan/hour).
    *   $c_{A_1}=0.05, c_{A_2}=0.03, c_{B_1}=0.06, c_{B_2}=0.11, c_{B_3}=0.05$
*   $t_{k,m}$: Processing time of product $k$ on machine $m$ (hours/unit).
    *   If product $k$ cannot be processed on machine $m$, $t_{k,m}$ is undefined (variable will be 0).
    *   $t_{1,A_1}=5, t_{1,A_2}=7, t_{1,B_1}=6, t_{1,B_2}=4, t_{1,B_3}=7$
    *   $t_{2,A_1}=10, t_{2,A_2}=9, t_{2,B_2}=8$
    *   $t_{3,A_2}=12, t_{3,B_2}=11$
*   $H_m$: Available hours for machine $m$.
    *   $H_{A_1}=6000, H_{A_2}=10000, H_{B_1}=4000, H_{B_2}=7000, H_{B_3}=4000$

## 3. Decision Variables

Let $x_{k,m}$ be the quantity of product $k$ processed on machine $m$.
Since each product must go through one Stage A machine and one Stage B machine, we can define variables for the specific paths or simply for the assignment to machines. It is more efficient to define variables for the amount of product $k$ assigned to machine $m$.

*   $x_{k,m} \ge 0$ for all valid pairs $(k,m)$.

**Valid Assignments (Non-zero variables possible):**
*   **Stage A:**
    *   Product 1: $x_{1,A_1}, x_{1,A_2}$
    *   Product 2: $x_{2,A_1}, x_{2,A_2}$
    *   Product 3: $x_{3,A_2}$
*   **Stage B:**
    *   Product 1: $x_{1,B_1}, x_{1,B_2}, x_{1,B_3}$
    *   Product 2: $x_{2,B_2}$
    *   Product 3: $x_{3,B_2}$

**Total Production Quantity Constraints:**
For each product $k$, the total quantity processed in Stage A must equal the total quantity processed in Stage B (flow conservation).
Let $Q_k$ be the total production of product $k$.
$Q_1 = x_{1,A_1} + x_{1,A_2} = x_{1,B_1} + x_{1,B_2} + x_{1,B_3}$
$Q_2 = x_{2,A_1} + x_{2,A_2} = x_{2,B_2}$
$Q_3 = x_{3,A_2} = x_{3,B_2}$

## 4. Objective Function

Maximize Total Profit $Z$.
Profit = Total Revenue - Total Raw Material Cost - Total Processing Cost.

$$
Z = \sum_{k \in P} Q_k (p_k - r_k) - \sum_{m \in M} c_m \left( \sum_{k \in P} t_{k,m} x_{k,m} \right)
$$

Expanding for clarity:

**Revenue - Raw Material (Contribution Margin per unit):**
*   Product 1: $1.25 - 0.25 = 1.00$
*   Product 2: $2.00 - 0.35 = 1.65$
*   Product 3: $2.80 - 0.50 = 2.30$

$$
Z = 1.00 Q_1 + 1.65 Q_2 + 2.30 Q_3 - \left( 0.05 \sum_{k} t_{k,A_1}x_{k,A_1} + 0.03 \sum_{k} t_{k,A_2}x_{k,A_2} + 0.06 \sum_{k} t_{k,B_1}x_{k,B_1} + 0.11 \sum_{k} t_{k,B_2}x_{k,B_2} + 0.05 \sum_{k} t_{k,B_3}x_{k,B_3} \right)
$$

Substituting specific terms:
$$
\begin{aligned}
\text{Max } Z = \ & 1.00(x_{1,A_1} + x_{1,A_2}) + 1.65(x_{2,A_1} + x_{2,A_2}) + 2.30(x_{3,A_2}) \\
& - 0.05(5x_{1,A_1} + 10x_{2,A_1}) \\
& - 0.03(7x_{1,A_2} + 9x_{2,A_2} + 12x_{3,A_2}) \\
& - 0.06(6x_{1,B_1}) \\
& - 0.11(4x_{1,B_2} + 8x_{2,B_2} + 11x_{3,B_2}) \\
& - 0.05(7x_{1,B_3})
\end{aligned}
$$

Simplifying coefficients for each variable in the objective function:
*   $x_{1,A_1}$: $1.00 - 0.05(5) = 1.00 - 0.25 = 0.75$
*   $x_{1,A_2}$: $1.00 - 0.03(7) = 1.00 - 0.21 = 0.79$
*   $x_{2,A_1}$: $1.65 - 0.05(10) = 1.65 - 0.50 = 1.15$
*   $x_{2,A_2}$: $1.65 - 0.03(9) = 1.65 - 0.27 = 1.38$
*   $x_{3,A_2}$: $2.30 - 0.03(12) = 2.30 - 0.36 = 1.94$
*   $x_{1,B_1}$: $-0.06(6) = -0.36$ (Note: Revenue/Raw is counted once per unit produced, so we don't add it here again if we sum by machine. Alternatively, we can sum by product unit. Let's stick to the expanded form above to avoid double counting errors in interpretation. The standard way is: $\sum Q_k(p_k-r_k) - \sum \text{Processing Costs}$. The expansion above is correct.)

Let's refine the objective to be a single linear expression in terms of $x_{k,m}$ variables directly, ensuring each unit of product contributes its net margin once and incurs processing costs for both stages.

$$
\text{Max } Z = \sum_{k} Q_k (p_k - r_k) - \sum_{m \in M_A} c_m \sum_{k} t_{k,m} x_{k,m} - \sum_{m \in M_B} c_m \sum_{k} t_{k,m} x_{k,m}
$$

Using $Q_1 = x_{1,A_1}+x_{1,A_2}$, etc.

## 5. Operational Constraints

### 1. Flow Conservation (Production Balance)
The amount of product $k$ entering Stage B must equal the amount leaving Stage A.
1.  **Product I:**
    $$x_{1,A_1} + x_{1,A_2} = x_{1,B_1} + x_{1,B_2} + x_{1,B_3}$$
2.  **Product II:**
    $$x_{2,A_1} + x_{2,A_2} = x_{2,B_2}$$
3.  **Product III:**
    $$x_{3,A_2} = x_{3,B_2}$$

### 2. Machine Capacity Constraints
For each machine $m$, the total processing time required by all assigned products must not exceed available hours $H_m$.

1.  **Machine $A_1$:**
    $$5x_{1,A_1} + 10x_{2,A_1} \le 6,000$$
2.  **Machine $A_2$:**
    $$7x_{1,A_2} + 9x_{2,A_2} + 12x_{3,A_2} \le 10,000$$
3.  **Machine $B_1$:**
    $$6x_{1,B_1} \le 4,000$$
4.  **Machine $B_2$:**
    $$4x_{1,B_2} + 8x_{2,B_2} + 11x_{3,B_2} \le 7,000$$
5.  **Machine $B_3$:**
    $$7x_{1,B_3} \le 4,000$$

### 3. Non-negativity Constraints
$$x_{k,m} \ge 0 \quad \forall k \in P, m \in M \text{ where assignment is valid.}$$

Specifically:
$$x_{1,A_1}, x_{1,A_2}, x_{1,B_1}, x_{1,B_2}, x_{1,B_3} \ge 0$$
$$x_{2,A_1}, x_{2,A_2}, x_{2,B_2} \ge 0$$
$$x_{3,A_2}, x_{3,B_2} \ge 0$$

---

### Final Mathematical Formulation

**Decision Variables:**
*   $x_{1,A_1}, x_{1,A_2}, x_{1,B_1}, x_{1,B_2}, x_{1,B_3} \ge 0$
*   $x_{2,A_1}, x_{2,A_2}, x_{2,B_2} \ge 0$
*   $x_{3,A_2}, x_{3,B_2} \ge 0$

**Objective Function:**
Maximize
$$
\begin{aligned}
Z = \ & 0.75 x_{1,A_1} + 0.79 x_{1,A_2} + 1.15 x_{2,A_1} + 1.38 x_{2,A_2} + 1.94 x_{3,A_2} \\
& - 0.36 x_{1,B_1} - 0.44 x_{1,B_2} - 0.35 x_{1,B_3} \\
& - 0.88 x_{2,B_2} - 1.21 x_{3,B_2}
\end{aligned}
$$
*(Note: The coefficients for B-stage variables are negative because they represent costs subtracted from the gross margin calculated on the A-stage side or overall. To be precise, let's write it in the additive form to ensure correctness:)*

**Corrected Objective (Additive Form):**
$$
\begin{aligned}
\text{Max } Z = \ & (1.00)(x_{1,A_1} + x_{1,A_2}) + (1.65)(x_{2,A_1} + x_{2,A_2}) + (2.30)(x_{3,A_2}) \\
& - 0.05(5x_{1,A_1} + 10x_{2,A_1}) \\
& - 0.03(7x_{1,A_2} + 9x_{2,A_2} + 12x_{3,A_2}) \\
& - 0.06(6x_{1,B_1}) \\
& - 0.11(4x_{1,B_2} + 8x_{2,B_2} + 11x_{3,B_2}) \\
& - 0.05(7x_{1,B_3})
\end{aligned}
$$

**Subject to:**

1.  **Balance Constraints:**
    $$x_{1,A_1} + x_{1,A_2} - x_{1,B_1} - x_{1,B_2} - x_{1,B_3} = 0$$
    $$x_{2,A_1} + x_{2,A_2} - x_{2,B_2} = 0$$
    $$x_{3,A_2} - x_{3,B_2} = 0$$

2.  **Capacity Constraints:**
    $$5x_{1,A_1} + 10x_{2,A_1} \le 6,000$$
    $$7x_{1,A_2} + 9x_{2,A_2} + 12x_{3,A_2} \le 10,000$$
    $$6x_{1,B_1} \le 4,000$$
    $$4x_{1,B_2} + 8x_{2,B_2} + 11x_{3,B_2} \le 7,000$$
    $$7x_{1,B_3} \le 4,000$$

3.  **Non-negativity:**
    $$x_{i,j} \ge 0 \quad \text{for all defined variables.}$$