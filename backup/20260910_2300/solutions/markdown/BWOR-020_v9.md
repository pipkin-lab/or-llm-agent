**Model Type:** MILP (Mixed Integer Linear Programming)

### 1. Index Sets & Parameters

**Sets:**
*   $C = \{A, B, C, D, E\}$: Set of customers.
*   $T = \{1, 2, 3, 4\}$: Set of trucks.

**Parameters:**
*   $d_i$: Demand for customer $i$ (units).
    *   $d_A = 1$
    *   $d_B = 2$
    *   $d_C = 3$
    *   $d_D = 4$
    *   $d_E = 8$
*   $K_j$: Capacity of truck $j$ (units).
    *   $K_1 = 2$
    *   $K_2 = 6$
    *   $K_3 = 8$
    *   $K_4 = 11$
*   $c_j$: Cost of using truck $j$.
    *   $c_1, c_2, c_3, c_4$ are given costs (values not explicitly numerically defined in the prompt, so they remain as parameters $c_j$).

### 2. Decision Variables

*   $y_{ij} \in \{0, 1\}$: Binary variable where $y_{ij} = 1$ if Truck $j$ delivers to Customer $i$, and $0$ otherwise.
*   $z_j \in \{0, 1\}$: Binary variable where $z_j = 1$ if Truck $j$ is used, and $0$ otherwise.

### 3. Objective Function

Minimize the total transportation cost:

$$
\text{Minimize } Z = \sum_{j \in T} c_j z_j
$$

### 4. Operational Constraints

**1. Demand Satisfaction:**
Each customer must receive exactly their required demand. Since the problem implies discrete deliveries and trucks are used "only once" (implying a single trip per truck), and no explicit quantity variables are introduced for partial deliveries, we assume that if a truck is assigned to a customer, it fulfills the *entire* demand of that customer. *Note: In standard set covering/partitioning formulations for this specific textbook problem type (5.12), it is typically assumed that a customer is served by exactly one truck, or the formulation allows splitting. However, given the "Set Covering" title and small integer demands vs capacities, and the constraint "Truck j is used only once", the standard interpretation is that we assign customers to trucks. Let's verify if splitting is allowed. Usually, "delivery to customer" implies satisfying the demand. If a truck is assigned to Customer E (demand 8), it must carry 8 units. Truck 1 (cap 2) cannot serve E. Truck 2 (cap 6) cannot serve E. Truck 3 (cap 8) can serve E. Truck 4 (cap 11) can serve E.
If splitting were allowed, we would need continuous variables $x_{ij}$ for amount delivered. However, the term "Set Covering" and the binary nature of "deliver to" usually implies an assignment model where each customer is assigned to one or more trucks. Given the capacities are small integers and demands are small integers, and the constraints are on *which* customers a truck serves, the most robust formulation that respects "Truck j used only once" (single trip) is that a truck carries a subset of customers, and the sum of their demands must not exceed capacity. Does a truck deliver the *full* demand of the customer? Yes, typically in these problems, you don't split a customer's order across multiple trucks unless specified (like "can be split"). If splitting is not allowed, each customer is assigned to exactly one truck. Let's assume **non-splitting** (each customer assigned to exactly one truck) as is standard for "assign deliveries" without explicit split variables.

*Constraint: Each customer is assigned to exactly one truck.*
$$
\sum_{j \in T} y_{ij} = 1 \quad \forall i \in C
$$

**2. Truck Capacity Constraints:**
The total demand of customers assigned to truck $j$ cannot exceed its capacity.
$$
\sum_{i \in C} d_i y_{ij} \leq K_j \quad \forall j \in T
$$

**3. Linking Truck Usage to Assignment:**
If a truck is used ($z_j=1$), it must serve at least one customer. If it serves a customer, it is used.
$$
\sum_{i \in C} y_{ij} \leq M z_j \quad \forall j \in T
$$
(Where $M$ is a large constant, e.g., $|C|=5$. Alternatively, since $y_{ij}$ are binary, $\sum y_{ij} \le 5 z_j$ works. Or simply, if $z_j=0$, all $y_{ij}=0$).

**4. Conflict Constraints:**
*   A truck cannot deliver to both Customer A and Customer C.
    $$
    y_{A,j} + y_{C,j} \leq 1 \quad \forall j \in T
    $$
*   A truck cannot deliver to both Customer B and Customer D.
    $$
    y_{B,j} + y_{D,j} \leq 1 \quad \forall j \in T
    $$

**5. Domain Constraints:**
$$
y_{ij} \in \{0, 1\} \quad \forall i \in C, j \in T
$$
$$
z_j \in \{0, 1\} \quad \forall j \in T
$$

### Feasibility Sanity Check
*   **Total Demand:** $1+2+3+4+8 = 18$ units.
*   **Total Capacity:** $2+6+8+11 = 27$ units.
*   Supply > Demand, so capacity is not the primary bottleneck, but individual truck capacities restrict assignments.
*   **Customer E (8 units):** Can only be served by Truck 3 (cap 8) or Truck 4 (cap 11).
    *   If E is served by Truck 3, Truck 3 has 0 remaining capacity.
    *   If E is served by Truck 4, Truck 4 has 3 remaining capacity.
*   **Customer D (4 units):** Can be served by Truck 2 (cap 6, rem 2), Truck 3 (cap 8, rem 4), or Truck 4 (cap 11, rem 7). Cannot be served by Truck 1 (cap 2).
*   **Customer C (3 units):** Can be served by Truck 2, 3, or 4.
*   **Customer B (2 units):** Can be served by Truck 1, 2, 3, or 4.
*   **Customer A (1 unit):** Can be served by Truck 1, 2, 3, or 4.

The model is feasible. For example:
*   Truck 3 serves E (8/8).
*   Truck 4 serves D (4) and C (3)? No, conflict? No, D and C don't conflict. But wait, Truck 4 cap 11. D(4)+C(3)=7 <= 11. OK.
*   Truck 2 serves B (2) and A (1)? Cap 6. 2+1=3 <= 6. OK.
*   Truck 1 unused? Or Truck 1 serves A?
    *   Let's check conflicts.
    *   If Truck 4 serves D and C: OK (no conflict between C and D).
    *   If Truck 2 serves B and A: OK (no conflict between A and B).
    *   Truck 3 serves E: OK.
    *   Truck 1 unused ($z_1=0$).
    *   Total Cost = $c_2 + c_3 + c_4$.

Another option:
*   Truck 4 serves E (8). Remaining 3.
*   Truck 3 serves D (4). Remaining 4.
*   Truck 2 serves C (3). Remaining 3.
*   Truck 1 serves B (2). Remaining 0.
*   Customer A (1) needs a truck.
    *   Truck 1 full? No, B(2) fills Truck 1 (cap 2).
    *   Truck 2 has 3 left. Can take A? A(1) <= 3. Yes.
    *   So Truck 2 serves C and A. Conflict? A and C cannot be on same truck. **Violation.**
    *   So Truck 2 cannot serve both A and C.
    *   Try: Truck 2 serves B (2). Truck 1 serves A (1).
    *   Truck 4 serves E (8) and D (4)? 8+4=12 > 11. No.
    *   Truck 4 serves E (8). Truck 3 serves D (4). Truck 2 serves C (3). Truck 1 serves A (1) and B (2)? 1+2=3 > 2. No.
    *   Truck 1 serves A (1). Truck 2 serves B (2). Truck 3 serves C (3). Truck 4 serves D (4) and E (8)? 12>11. No.
    *   Truck 4 serves E (8) and A (1)? 9<=11. OK.
    *   Truck 3 serves D (4). OK.
    *   Truck 2 serves C (3) and B (2)? 5<=6. OK. Conflict B/D? No. Conflict A/C? No.
    *   Truck 1 unused.
    *   Assignment:
        *   T4: E, A
        *   T3: D
        *   T2: C, B
        *   T1: None
    *   Check Conflicts:
        *   T4: A, E. (A,C conflict? No C on T4. B,D conflict? No B,D on T4). OK.
        *   T3: D. OK.
        *   T2: C, B. (A,C conflict? No A on T2. B,D conflict? No D on T2). OK.
    *   This is a feasible solution.

The formulation is correct.

### Final Formulation Summary

**Model Type:** MILP

**Sets:**
*   $I = \{A, B, C, D, E\}$
*   $J = \{1, 2, 3, 4\}$

**Parameters:**
*   $d_A=1, d_B=2, d_C=3, d_D=4, d_E=8$
*   $K_1=2, K_2=6, K_3=8, K_4=11$
*   $c_1, c_2, c_3, c_4$

**Variables:**
*   $y_{ij} \in \{0,1\}$ for $i \in I, j \in J$
*   $z_j \in \{0,1\}$ for $j \in J$

**Objective:**
$$ \min \sum_{j=1}^4 c_j z_j $$

**Constraints:**
1.  $\sum_{j=1}^4 y_{ij} = 1, \quad \forall i \in I$
2.  $\sum_{i \in I} d_i y_{ij} \leq K_j, \quad \forall j \in J$
3.  $\sum_{i \in I} y_{ij} \leq 5 z_j, \quad \forall j \in J$
4.  $y_{A,j} + y_{C,j} \leq 1, \quad \forall j \in J$
5.  $y_{B,j} + y_{D,j} \leq 1, \quad \forall j \in J$