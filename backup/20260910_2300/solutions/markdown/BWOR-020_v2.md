### Index Sets & Parameters

**Sets:**
*   $C = \{A, B, C, D, E\}$: The set of customers.
*   $T = \{1, 2, 3, 4\}$: The set of available trucks.

**Parameters:**
*   $d_i$: Demand (units of goods) for customer $i \in C$.
    *   $d_A = 1$
    *   $d_B = 2$
    *   $d_C = 3$
    *   $d_D = 4$
    *   $d_E = 8$
*   $K_j$: Capacity of truck $j \in T$ (in units).
    *   $K_1 = 2$
    *   $K_2 = 6$
    *   $K_3 = 8$
    *   $K_4 = 11$
*   $c_j$: Cost of using truck $j \in T$.

**Logical Conflict Constraints (Incompatibility Pairs):**
*   Truck $j$ cannot serve both Customer A and Customer C.
*   Truck $j$ cannot serve both Customer B and Customer D.

### Decision Variables

*   $x_{ij}$: Binary variable where:
    $$
    x_{ij} = \begin{cases} 
    1 & \text{if truck } j \text{ delivers to customer } i \\
    0 & \text{otherwise}
    \end{cases}
    $$
    for all $i \in C, j \in T$.

*   $y_j$: Binary variable where:
    $$
    y_j = \begin{cases} 
    1 & \text{if truck } j \text{ is used (assigned to at least one customer)} \\
    0 & \text{otherwise}
    \end{cases}
    $$
    for all $j \in T$.

**Variable Domains:**
*   $x_{ij} \in \{0, 1\} \quad \forall i \in C, j \in T$
*   $y_j \in \{0, 1\} \quad \forall j \in T$

### Objective Function

Minimize the total transportation cost. Since the cost is incurred only if a truck is used, the objective is:

$$
\text{Minimize } Z = \sum_{j \in T} c_j y_j
$$

### Operational Constraints

**1. Demand Satisfaction (Set Covering/Partitioning):**
Each customer must be served by exactly one truck. This ensures the full demand $d_i$ is met by a single assignment (consistent with the "truck cannot deliver to both..." logic implying discrete assignment per customer).

$$
\sum_{j \in T} x_{ij} = 1 \quad \forall i \in C
$$

**2. Truck Capacity Constraints:**
The total demand assigned to a truck cannot exceed its capacity. Note that if $y_j=0$, all $x_{ij}=0$ (enforced by constraint 3), so capacity is 0, which is $\le K_j$.

$$
\sum_{i \in C} d_i x_{ij} \le K_j y_j \quad \forall j \in T
$$

*Alternative formulation (without big-M if $y_j$ is implied):*
Since $x_{ij}$ are binary and linked to $y_j$, we can also write:
$$
\sum_{i \in C} d_i x_{ij} \le K_j \quad \forall j \in T
$$
*However, this must be combined with the logic that if no customer is assigned, the truck isn't used. The constraint $\sum_{i} x_{ij} \le y_j$ ensures $y_j=1$ if any $x_{ij}=1$. The capacity constraint above is valid on its own for the physical limit, but we need to link cost to usage. The standard linking is:*

**3. Linking Constraints (Truck Usage):**
A truck is considered "used" ($y_j=1$) if and only if it is assigned to at least one customer.

$$
\sum_{i \in C} x_{ij} \le y_j \quad \forall j \in T
$$
*(Note: Since $y_j$ is binary and we minimize cost, $y_j$ will naturally take the smallest value possible. If $\sum x_{ij} \ge 1$, then $y_j \ge 1 \implies y_j=1$. If $\sum x_{ij} = 0$, then $y_j$ can be 0.)*

**4. Incompatibility Constraints:**
*   A truck cannot deliver to both Customer A and Customer C:
    $$
    x_{A,j} + x_{C,j} \le 1 \quad \forall j \in T
    $$
*   A truck cannot deliver to both Customer B and Customer D:
    $$
    x_{B,j} + x_{D,j} \le 1 \quad \forall j \in T
    $$

**5. Non-negativity and Integrality:**
$$
x_{ij} \in \{0, 1\} \quad \forall i \in C, j \in T
$$
$$
y_j \in \{0, 1\} \quad \forall j \in T
$$