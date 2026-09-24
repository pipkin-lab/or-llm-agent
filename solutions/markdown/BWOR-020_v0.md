# Truck Delivery Problem (Set Covering / Assignment)

## Model Type Declaration
**MILP** (Mixed Integer Linear Program). The decision variables are binary (assignment of customers to trucks), and the objective and constraints are linear.

## MANDATORY COST INVENTORY (PRE-MODELING STEP)
| Cost Figure | Entity Modified | Interpretation |
|---|---|---|
| $c_j$ | Truck $j$ ($j=1,\dots,4$) | Cost of *using* truck $j$ (fixed cost incurred if truck $j$ is assigned any delivery) |

The problem statement explicitly gives the cost parameter symbolically as $c_j$ ("The cost of using truck $j$ is $c_j$"). No numeric values for $c_1, c_2, c_3, c_4$ are provided in the text. These are the objective coefficients. Since the problem asks to *formulate* the model (not solve it), the symbolic parameters $c_j$ are the intended objective coefficients. I will retain them as parameters $c_1, c_2, c_3, c_4$ with the annotation that no numeric values were provided in the problem text.

Re-scan of the entire text: The only numeric values present are the delivery quantities (1, 2, 3, 4, 8) and truck capacities (2, 6, 8, 11). No dollar amounts or cost figures are given. Therefore $c_j$ remains symbolic.

## Index Sets & Parameters

**Index Sets:**
- $C = \{A, B, C, D, E\}$: set of customers, indexed by $i$.
- $J = \{1, 2, 3, 4\}$: set of trucks, indexed by $j$.
- $P = \{(A,C), (B,D)\}$: set of forbidden customer pairs.

**Parameters:**
- $q_i$: units of goods to deliver to customer $i$.
  - $q_A = 1$, $q_B = 2$, $q_C = 3$, $q_D = 4$, $q_E = 8$.
- $u_j$: capacity of truck $j$ (in units).
  - $u_1 = 2$, $u_2 = 6$, $u_3 = 8$, $u_4 = 11$.
- $c_j$: cost of using truck $j$.
  - $c_1 = c_1$ [NOT_PROVIDED], $c_2 = c_2$ [NOT_PROVIDED], $c_3 = c_3$ [NOT_PROVIDED], $c_4 = c_4$ [NOT_PROVIDED].
  - *Note:* These are symbolic parameters as given in the problem statement. The problem asks for a formulation, not a numerical solution.

## Decision Variables

- $x_{ij} \in \{0, 1\}$: binary variable for each customer $i \in C$ and truck $j \in J$.
  - $x_{ij} = 1$ if customer $i$'s delivery is assigned to truck $j$, and $0$ otherwise.
  - Domain: $x_{ij} \geq 0$ is implied by the binary domain, but explicitly: $x_{ij} \in \{0,1\} \implies 0 \leq x_{ij} \leq 1$ and $x_{ij}$ integer.

- $y_j \in \{0, 1\}$: binary variable for each truck $j \in J$.
  - $y_j = 1$ if truck $j$ is used (assigned at least one customer), and $0$ otherwise.
  - Domain: $y_j \in \{0,1\}$.

## Objective Function

$$\min \sum_{j \in J} c_j \, y_j$$

**Objective Parameter Cross-Reference:**
| Parameter | Value in Text | Status |
|---|---|---|
| $c_1$ | "The cost of using truck $j$ is $c_j$" | Symbolic, as given |
| $c_2$ | same | Symbolic, as given |
| $c_3$ | same | Symbolic, as given |
| $c_4$ | same | Symbolic, as given |

All objective parameters are the symbolic $c_j$ as explicitly stated in the problem. No numeric values are provided; the problem requests a formulation.

## Operational Constraints

### 1. Each customer is assigned to exactly one truck
$$\sum_{j \in J} x_{ij} = 1 \quad \forall \, i \in C$$

This ensures every customer's delivery is made by exactly one truck.

### 2. Truck capacity constraint
$$\sum_{i \in C} q_i \, x_{ij} \leq u_j \quad \forall \, j \in J$$

Expanded:
- $j=1$: $1 \cdot x_{A1} + 2 \cdot x_{B1} + 3 \cdot x_{C1} + 4 \cdot x_{D1} + 8 \cdot x_{E1} \leq 2$
- $j=2$: $1 \cdot x_{A2} + 2 \cdot x_{B2} + 3 \cdot x_{C2} + 4 \cdot x_{D2} + 8 \cdot x_{E2} \leq 6$
- $j=3$: $1 \cdot x_{A3} + 2 \cdot x_{B3} + 3 \cdot x_{C3} + 4 \cdot x_{D3} + 8 \cdot x_{E3} \leq 8$
- $j=4$: $1 \cdot x_{A4} + 2 \cdot x_{B4} + 3 \cdot x_{C4} + 4 \cdot x_{D4} + 8 \cdot x_{E4} \leq 11$

### 3. Forbidden pair constraints (same truck cannot serve both customers in a forbidden pair)
$$x_{i_1 j} + x_{i_2 j} \leq 1 \quad \forall \, (i_1, i_2) \in P, \; \forall \, j \in J$$

Explicitly:
- **A and C cannot be on the same truck:**
  - $x_{A1} + x_{C1} \leq 1$
  - $x_{A2} + x_{C2} \leq 1$
  - $x_{A3} + x_{C3} \leq 1$
  - $x_{A4} + x_{C4} \leq 1$
- **B and D cannot be on the same truck:**
  - $x_{B1} + x_{D1} \leq 1$
  - $x_{B2} + x_{D2} \leq 1$
  - $x_{B3} + x_{D3} \leq 1$
  - $x_{B4} + x_{D4} \leq 1$

### 4. Linking constraints (truck usage indicator)
$$x_{ij} \leq y_j \quad \forall \, i \in C, \; \forall \, j \in J$$

This ensures $y_j = 1$ whenever any customer is assigned to truck $j$. Combined with the minimization objective (positive costs), $y_j$ will be 0 when no customer is assigned to truck $j$.

### 5. Domain / Non-negativity
$$x_{ij} \in \{0, 1\} \quad \forall \, i \in C, \; j \in J$$
$$y_j \in \{0, 1\} \quad \forall \, j \in J$$

## Feasibility Sanity Check

- Total units to deliver: $1 + 2 + 3 + 4 + 8 = 18$.
- Total truck capacity: $2 + 6 + 8 + 11 = 27 \geq 18$. Capacity is sufficient in aggregate.
- Customer E requires 8 units. Only Truck 3 (cap 8) or Truck 4 (cap 11) can serve E alone, or a combination is impossible since each customer goes to exactly one truck. So E must be assigned to Truck 3 or Truck 4.
- The forbidden pair constraints do not make the problem infeasible; they only restrict certain co-assignments.
- The model is feasible for any non-negative $c_j$.