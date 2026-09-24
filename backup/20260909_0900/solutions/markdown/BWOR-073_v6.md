### 1. Index Sets & Parameters

**Index Sets:**
*   $K = \{1, 2, 3, 4\}$: The set of warehouses (stages in the dynamic programming sense).
*   $U = \{2, 3, 4\}$: The set of possible numbers of patrol units that can be assigned to a single warehouse.
*   $S = \{8, 9, 10, 11, 12\}$: The set of possible remaining units for the subproblems (since min total is $4 \times 2 = 8$ and max is $4 \times 4 = 16$, but we have exactly 12 units to distribute, the subproblem states range from 8 to 12).

**Parameters:**
*   $N = 12$: Total number of patrol units.
*   $c_{k, u}$: The expected number of accidents per year for warehouse $k$ when assigned $u$ patrol units. Based on Table 7-11:

    | $u$ | $c_{1, u}$ (W1) | $c_{2, u}$ (W2) | $c_{3, u}$ (W3) | $c_{4, u}$ (W4) |
    | :--- | :---: | :---: | :---: | :---: |
    | 2 | 18 | 38 | 14 | 34 |
    | 3 | 16 | 36 | 12 | 31 |
    | 4 | 12 | 30 | 11 | 25 |

### 2. Decision Variables

Since this is a Dynamic Programming problem, the "decision" at each stage is discrete. We define the decision variable for each stage $k$ as:
*   $u_k$: The number of patrol units assigned to warehouse $k$.
    *   Domain: $u_k \in \{2, 3, 4\}$ for $k \in \{1, 2, 3, 4\}$.

*Note: While the prompt asks for a formal model, Dynamic Programming is often solved via recursive stages rather than a single global MILP. However, to satisfy the requirement of a formal optimization structure that captures the DP logic or allows for a MILP equivalent solution:*

**MILP Equivalent Formulation (for solver compatibility if DP is not used directly):**
*   $u_k$: Integer variable representing units assigned to warehouse $k$, $u_k \in \{2, 3, 4\}$.

### 3. Objective Function

**Minimize** the total expected number of accidents:

$$ \text{Minimize } Z = \sum_{k=1}^{4} c_{k, u_k} $$

Where $c_{k, u_k}$ is the specific accident value from the table corresponding to warehouse $k$ and assigned units $u_k$.

**Dynamic Programming Recursion:**
Let $f_k(s)$ be the minimum total expected accidents for warehouses $k, k+1, \dots, 4$ given that there are $s$ patrol units remaining to be distributed among them.

*   **Boundary Condition (Stage 4):**
    $$ f_4(s) = c_{4, s} \quad \text{for } s \in \{2, 3, 4\} $$
    (If $s < 2$ or $s > 4$, $f_4(s) = \infty$)

*   **Recursive Step (Stage $k$ to $k-1$):**
    $$ f_k(s) = \min_{u \in \{2, 3, 4\}} \left( c_{k, u} + f_{k+1}(s - u) \right) $$
    Subject to: $s - u \ge 2$ (enough units for remaining warehouses) and $s - u \le 4(5-k)$ (enough units to satisfy max capacity of remaining warehouses, though here the lower bound is the binding constraint for feasibility).

*   **Final Answer:**
    $$ Z^* = f_1(12) $$

### 4. Operational Constraints

1.  **Total Unit Constraint:**
    The sum of units assigned to all warehouses must equal the total available units.
    $$ \sum_{k=1}^{4} u_k = 12 $$

2.  **Per-Warehouse Bounds:**
    Each warehouse must receive between 2 and 4 units.
    $$ 2 \le u_k \le 4, \quad \forall k \in \{1, 2, 3, 4\} $$

3.  **Integrality:**
    Patrol units are discrete entities.
    $$ u_k \in \mathbb{Z}^+ $$

---

### Model Verification & Solution Path (DP Logic)

To ensure the model yields the correct result, let's trace the DP logic briefly to confirm feasibility and optimality structure.

**Stage 4 (Warehouse 4):**
*   $f_4(2) = c_{4,2} = 34$
*   $f_4(3) = c_{4,3} = 31$
*   $f_4(4) = c_{4,4} = 25$

**Stage 3 (Warehouse 3):**
We need to distribute $s$ units between W3 and W4.
*   $f_3(6) = \min [ c_{3,2}+f_4(4), c_{3,3}+f_4(3), c_{3,4}+f_4(2) ]$
    $= \min [ 14+25, 12+31, 11+34 ] = \min [ 39, 43, 45 ] = 39$ (Assign 2 to W3, 4 to W4)
*   $f_3(7) = \min [ c_{3,2}+f_4(5-\text{invalid}), c_{3,3}+f_4(4), c_{3,4}+f_4(3) ]$
    $= \min [ \infty, 12+25, 11+31 ] = \min [ \infty, 37, 42 ] = 37$ (Assign 3 to W3, 4 to W4)
*   $f_3(8) = \min [ c_{3,2}+f_4(6-\text{invalid}), c_{3,3}+f_4(5-\text{invalid}), c_{3,4}+f_4(4) ]$
    Wait, max units for W4 is 4.
    $f_3(8) = \min [ \infty, \infty, 11+25 ] = 36$ (Assign 4 to W3, 4 to W4)
    *Correction*: For $f_3(s)$, the remaining units for W4 is $s-u$.
    If $s=6$: $u=2 \to W4=4$ (OK), $u=3 \to W4=3$ (OK), $u=4 \to W4=2$ (OK).
    If $s=7$: $u=2 \to W4=5$ (Invalid), $u=3 \to W4=4$ (OK), $u=4 \to W4=3$ (OK).
    If $s=8$: $u=2 \to W4=6$ (Invalid), $u=3 \to W4=5$ (Invalid), $u=4 \to W4=4$ (OK).

**Stage 2 (Warehouse 2):**
Need $f_2(s)$ for $s$ such that $s - u_2$ is a valid state for stage 3 (min 6, max 8).
So $s$ for stage 2 must be between $6+2=8$ and $8+4=12$.
We need $f_2(8), f_2(9), f_2(10), f_2(11), f_2(12)$.

*   $f_2(8) = \min [ c_{2,2}+f_3(6), c_{2,3}+f_3(5-\text{inv}), c_{2,4}+f_3(4-\text{inv}) ]$
    $= \min [ 38+39, \infty, \infty ] = 77$ (Assign 2 to W2)
*   $f_2(9) = \min [ c_{2,2}+f_3(7), c_{2,3}+f_3(6), c_{2,4}+f_3(5-\text{inv}) ]$
    $= \min [ 38+37, 36+39, \infty ] = \min [ 75, 75, \infty ] = 75$ (Assign 2 or 3 to W2)
*   $f_2(10) = \min [ c_{2,2}+f_3(8), c_{2,3}+f_3(7), c_{2,4}+f_3(6) ]$
    $= \min [ 38+36, 36+37, 30+39 ] = \min [ 74, 73, 69 ] = 69$ (Assign 4 to W2)
*   $f_2(11) = \min [ \infty, c_{2,3}+f_3(8), c_{2,4}+f_3(7) ]$ (W3 min is 6, so $11-u \ge 6 \implies u \le 5$)
    $= \min [ \infty, 36+36, 30+37 ] = \min [ \infty, 72, 67 ] = 67$ (Assign 4 to W2)
*   $f_2(12) = \min [ \infty, \infty, c_{2,4}+f_3(8) ]$ (W3 min 6, max 8. $12-u \le 8 \implies u \ge 4$)
    $= \min [ \infty, \infty, 30+36 ] = 66$ (Assign 4 to W2)

**Stage 1 (Warehouse 1):**
Total units = 12.
$f_1(12) = \min_{u_1 \in \{2,3,4\}} [ c_{1, u_1} + f_2(12 - u_1) ]$

*   If $u_1 = 2$: Remaining for W2-W4 is 10. Cost = $c_{1,2} + f_2(10) = 18 + 69 = 87$.
*   If $u_1 = 3$: Remaining for W2-W4 is 9. Cost = $c_{1,3} + f_2(9) = 16 + 75 = 91$.
*   If $u_1 = 4$: Remaining for W2-W4 is 8. Cost = $c_{1,4} + f_2(8) = 12 + 77 = 89$.

**Optimal Decision:**
Assign **2 units** to Warehouse 1.
Remaining cost 69 comes from $f_2(10)$, which was achieved by assigning **4 units** to Warehouse 2.
Remaining cost 39 comes from $f_3(6)$ (inside $f_2(10)$ calculation: $f_2(10)$ used $u_2=4$, so remaining for W3-W4 is $10-4=6$).
Inside $f_3(6)$, the optimal choice was $u_3=2$ (cost 14) leaving 4 for W4 (cost 25).

**Final Allocation:**
*   Warehouse 1: 2 units
*   Warehouse 2: 4 units
*   Warehouse 3: 2 units
*   Warehouse 4: 4 units
*   **Total Accidents:** $18 + 30 + 14 + 25 = 87$.