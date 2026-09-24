Here is the mathematical formulation for the Truck Delivery Problem.

### 1. Index Sets & Parameters

**Sets:**
*   $I = \{A, B, C, D, E\}$: Set of customers.
*   $J = \{1, 2, 3, 4\}$: Set of trucks.

**Parameters:**
*   $d_i$: Demand (units of goods) for customer $i \in I$.
    *   $d_A = 1$
    *   $d_B = 2$
    *   $d_C = 3$
    *   $d_D = 4$
    *   $d_E = 8$
*   $K_j$: Capacity of truck $j \in J$.
    *   $K_1 = 2$
    *   $K_2 = 6$
    *   $K_3 = 8$
    *   $K_4 = 11$
*   $c_j$: Cost of using truck $j \in J$.

### 2. Decision Variables

We use a binary decision variable to represent the assignment of a customer to a truck.

*   $x_{ij} \in \{0, 1\}$:
    *   $x_{ij} = 1$ if customer $i$ is assigned to truck $j$.
    *   $x_{ij} = 0$ otherwise.

*Note: Since the problem states "Truck $j$ is used only once" (implied by the fixed cost structure $c_j$ and standard set covering interpretations where cost is incurred if the truck is active), we must also determine which trucks are actually used. However, the cost is associated with the truck $j$. If a truck is not assigned any customers, it should not incur cost. We can handle this by linking the cost to the assignment or using auxiliary binary variables. Given the small size and the "fixed cost per truck" nature, it is cleaner to define a variable for truck usage.*

Let's refine the variables to handle the fixed cost properly:

*   $x_{ij} \in \{0, 1\}$: 1 if customer $i$ is assigned to truck $j$, 0 otherwise.
*   $y_j \in \{0, 1\}$: 1 if truck $j$ is used (i.e., assigned at least one customer), 0 otherwise.

### 3. Objective Function

Minimize the total transportation cost. The cost is incurred only if a truck is used.

$$
\text{Minimize } Z = \sum_{j \in J} c_j y_j
$$

### 4. Operational Constraints

**1. Customer Assignment (Set Covering/Partitioning):**
Each customer must be assigned to exactly one truck.
$$
\sum_{j \in J} x_{ij} = 1 \quad \forall i \in I
$$

**2. Truck Capacity Constraints:**
The total demand of customers assigned to any truck $j$ cannot exceed its capacity $K_j$.
$$
\sum_{i \in I} d_i x_{ij} \le K_j y_j \quad \forall j \in J
$$
*Explanation:* If truck $j$ is not used ($y_j=0$), the RHS is 0, forcing all $x_{ij}=0$. If truck $j$ is used ($y_j=1$), the sum of demands must be within capacity $K_j$. This constraint also ensures the link between $x$ and $y$.

**3. Mutual Exclusion Constraints (Conflict Constraints):**
*   A truck cannot deliver to both Customer A and Customer C.
    $$
    x_{A j} + x_{C j} \le 1 \quad \forall j \in J
    $$
*   A truck cannot deliver to both Customer B and Customer D.
    $$
    x_{B j} + x_{D j} \le 1 \quad \forall j \in J
    $$

**4. Variable Domains:**
$$
x_{ij} \in \{0, 1\} \quad \forall i \in I, j \in J
$$
$$
y_j \in \{0, 1\} \quad \forall j \in J
$$

---

### Verification & Notes

1.  **Objective Direction**: The problem asks to **minimize** total cost. The objective function $\sum c_j y_j$ correctly sums the costs of the trucks that are activated.
2.  **Unit Consistency**: Demands and capacities are both in "units". Consistent.
3.  **Fixed Cost Handling**: By introducing $y_j$ and the constraint $\sum d_i x_{ij} \le K_j y_j$, we ensure that $y_j=1$ only if necessary (if any $x_{ij}=1$, the LHS is positive, forcing $y_j=1$ due to binary constraints and capacity limits, though strictly speaking, if demand is 0, $y_j$ could be 0. But since every customer has demand $\ge 1$, any assigned customer forces $y_j=1$). Conversely, if $y_j=0$, all $x_{ij}$ for that $j$ must be 0. This correctly models the "cost of using truck $j$".
4.  **Conflict Constraints**: The constraints $x_{Aj} + x_{Cj} \le 1$ and $x_{Bj} + x_{Dj} \le 1$ correctly enforce that for any specific truck $j$, it cannot take both conflicting customers.
5.  **Feasibility Check**:
    *   Total Demand = $1+2+3+4+8 = 18$.
    *   Total Capacity = $2+6+8+11 = 27$.
    *   Customer E (8 units) must go to Truck 3 (8) or Truck 4 (11).
    *   If E goes to Truck 3 (Cost $c_3$), remaining demand $1+2+3+4=10$. Trucks 1, 2, 4 available.
    *   Conflicts: A and C separate. B and D separate.
    *   Example Feasible Solution:
        *   Truck 4 (Cap 11): Customer E (8) + Customer C (3) = 11. (Check conflict: E and C OK. C and A separate? Yes, A is elsewhere). Cost $c_4$.
        *   Truck 2 (Cap 6): Customer B (2) + Customer A (1) = 3. (Check conflict: B and D separate? Yes. A and C separate? Yes). Cost $c_2$.
        *   Truck 1 (Cap 2): Customer D (4)? No, Cap 2 < 4.
        *   Let's re-evaluate.
        *   Truck 4 (11): E(8) + B(2) + A(1) = 11. (Conflicts: E-B ok, E-A ok, B-A ok. B-D separate? D is elsewhere. A-C separate? C is elsewhere). Cost $c_4$.
        *   Truck 3 (8): C(3) + D(4) = 7. (Conflicts: C-A separate? A is on T4. D-B separate? B is on T4). Cost $c_3$.
        *   Trucks 1, 2 unused.
        *   Total Cost $c_4 + c_3$. This is a valid assignment.

The model correctly captures all constraints and the objective.