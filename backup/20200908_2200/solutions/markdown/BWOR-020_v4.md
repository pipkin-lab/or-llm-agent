# Integer Programming Formulation for Truck Delivery Problem

## 1. Index Sets & Parameters

**Sets:**
- $C = \{A, B, C, D, E\}$: Set of customers.
- $J = \{1, 2, 3, 4\}$: Set of trucks.

**Parameters:**
- $d_i$: Demand (units of goods) for customer $i \in C$.
  - $d_A = 1, d_B = 2, d_C = 3, d_D = 4, d_E = 8$.
- $Cap_j$: Capacity of truck $j \in J$.
  - $Cap_1 = 2, Cap_2 = 6, Cap_3 = 8, Cap_4 = 11$.
- $c_j$: Cost of using truck $j \in J$. (Note: Specific numerical values for costs are not provided in the text; they are treated as given parameters $c_j$).

## 2. Decision Variables

We define binary decision variables to represent the assignment of customers to trucks.

- $x_{ij} \in \{0, 1\}$: 
  - $x_{ij} = 1$ if customer $i$ is served by truck $j$.
  - $x_{ij} = 0$ otherwise.
  - Defined for all $i \in C, j \in J$.

- $y_j \in \{0, 1\}$:
  - $y_j = 1$ if truck $j$ is used (i.e., assigned to at least one customer).
  - $y_j = 0$ otherwise.
  - Defined for all $j \in J$.

*Note on "Set Covering" Context:* The problem title mentions "Set Covering," but the structure is actually an **Assignment Problem** with additional compatibility constraints. Since each customer must be served exactly once and each truck can serve multiple customers (up to capacity), we model the assignment of customers to trucks. The "use" of a truck is activated if any customer is assigned to it.

## 3. Objective Function

Minimize the total cost of the trucks used.

$$
\min Z = \sum_{j \in J} c_j y_j
$$

## 4. Operational Constraints

### A. Customer Service Constraints (Each customer served exactly once)
Each customer $i$ must be assigned to exactly one truck $j$.

$$
\sum_{j \in J} x_{ij} = 1, \quad \forall i \in C
$$

### B. Truck Capacity Constraints
The total demand of customers assigned to truck $j$ must not exceed its capacity.

$$
\sum_{i \in C} d_i x_{ij} \leq Cap_j, \quad \forall j \in J
$$

### C. Linking Constraints (Truck Usage)
Truck $j$ is used ($y_j = 1$) if and only if at least one customer is assigned to it. To linearize this, we use two sets of constraints:
1. If a customer is assigned to truck $j$, the truck must be used.
   $$
   x_{ij} \leq y_j, \quad \forall i \in C, \forall j \in J
   $$
2. The truck is used only if the total assigned customers do not exceed the maximum number of customers (trivially satisfied, but strictly, $y_j$ is driven by the first constraint and the objective minimization, which will set $y_j=0$ if no $x_{ij}=1$). 
   *Note: Since the objective is to minimize cost and $c_j \geq 0$, the solver will naturally set $y_j=0$ if no $x_{ij}=1$ due to constraint $x_{ij} \leq y_j$. No upper bound constraint on $y_j$ relative to sum of $x$ is strictly necessary for minimization with positive costs, but for completeness in a generic formulation, one could add $\sum x_{ij} \leq |C| y_j$. However, $x_{ij} \leq y_j$ is sufficient here.*

### D. Compatibility Constraints (Conflict Restrictions)
1. **A truck cannot deliver to both Customer A and Customer C.**
   For any truck $j$, we cannot have $x_{A,j} = 1$ AND $x_{C,j} = 1$.
   $$
   x_{A,j} + x_{C,j} \leq 1, \quad \forall j \in J
   $$

2. **A truck cannot deliver to both Customer B and Customer D.**
   For any truck $j$, we cannot have $x_{B,j} = 1$ AND $x_{D,j} = 1$.
   $$
   x_{B,j} + x_{D,j} \leq 1, \quad \forall j \in J
   $$

### E. Domain Constraints
$$
x_{ij} \in \{0, 1\}, \quad \forall i \in C, j \in J
$$
$$
y_j \in \{0, 1\}, \quad \forall j \in J
$$

---

## Verification & Notes

1.  **Data Completeness**: The costs $c_j$ are symbolic in the problem statement ("cost of using truck j is $c_j$"). The model is formulated in terms of these parameters.
2.  **Integrality**: All variables are binary integers, which is appropriate for assignment problems.
3.  **Objective Direction**: Minimization of total transportation cost.
4.  **Constraint Logic**:
    - The capacity constraints ensure physical feasibility.
    - The compatibility constraints ensure logical feasibility regarding customer pairs.
    - The service constraints ensure all customers are covered.
5.  **Model Type**: This is a 0-1 Integer Linear Programming (ILP) model.