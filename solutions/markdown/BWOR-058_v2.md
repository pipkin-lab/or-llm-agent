# Operations Research Model: Mall Lease Allocation

## Model Type Declaration
**Model Type:** MILP (Mixed Integer Linear Programming)
*Note: The objective function is linear in the decision variables. The constraints are linear. The decision variables are integers (number of stores). Therefore, a MILP solver (e.g., Gurobi, CPLEX, or SCIP) is required. No non-linear solver is needed.*

## 1. Index Sets & Parameters

### Index Sets
- $J = \{1, 2, 3, 4, 5\}$: Set of store types.
  - 1: Jewelry
  - 2: Shoes & Hats
  - 3: Department Store
  - 4: Bookstore
  - 5: Catering

### Parameters
Let $k \in J$ be the index for store type.

- $A_{total} = 5000$: Total available area for lease (m²).
- $r = 0.20$: Rent rate (20% of annual profit).
- $a_k$: Area required per store of type $k$ (m²).
- $L_k$: Minimum number of stores of type $k$.
- $U_k$: Maximum number of stores of type $k$.
- $p_{k,m}$: Annual profit (in thousand Yuan) per store of type $k$ when exactly $m$ stores of that type are leased.

**Extracted Data from Table 5-12:**

| Type $k$ | Store Name | $a_k$ (m²) | $L_k$ (Min) | $U_k$ (Max) | $p_{k,1}$ | $p_{k,2}$ | $p_{k,3}$ |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | Jewelry | 250 | 1 | 3 | 9 | 8 | 7 |
| 2 | Shoes & Hats | 350 | 1 | 2 | 10 | 9 | N/A |
| 3 | Department Store | 800 | 1 | 3 | 27 | 21 | 20 |
| 4 | Bookstore | 400 | 0 | 2 | 16 | 10 | N/A |
| 5 | Catering | 500 | 1 | 3 | 17 | 15 | 12 |

*Note: For types with max count < 3 (Type 2 and 4), the profit for $m=3$ is undefined and not used.*

## 2. Decision Variables

We need to decide the exact number of stores for each type. Since the profit per store depends on the *total* number of stores of that type opened, we cannot simply use a single variable $x_k$ with a constant profit coefficient. We must use binary variables to indicate which "level" of count is chosen for each type.

For each store type $k \in J$, define binary variables:
- $y_{k,m} \in \{0, 1\}$ for $m = 1, \dots, U_k$
  - $y_{k,m} = 1$ if exactly $m$ stores of type $k$ are leased.
  - $y_{k,m} = 0$ otherwise.

**Domain:**
$$ y_{k,m} \in \{0, 1\} \quad \forall k \in J, \, m \in \{1, \dots, U_k\} $$

*(Note: We do not need a variable for $m=0$ explicitly in the binary selection logic if we handle lower bounds carefully, but it is often cleaner to include a $m=0$ option or handle the "none selected" case via constraints. Given $L_4=0$, Type 4 can have 0 stores. Let's refine the variable definition to cover all feasible counts.)*

**Refined Decision Variables:**
For each type $k$, let the feasible counts be $M_k = \{m \mid L_k \le m \le U_k\}$.
However, standard binary selection requires that exactly one option is chosen from the set of possible counts.
Let's define $y_{k,m}$ for all integer $m$ from $0$ to $U_k$.
- $y_{k,m} = 1$ if the number of stores of type $k$ is exactly $m$.
- $y_{k,m} \in \{0, 1\}$.

The actual number of stores of type $k$ is $x_k = \sum_{m=0}^{U_k} m \cdot y_{k,m}$.

**Bounds:**
- $y_{k,m} \in \{0, 1\}$ for all $k \in J, m \in \{0, \dots, U_k\}$.
- Implicitly, $x_k \ge L_k$ will be enforced by the selection constraint and logic.

## 3. Objective Function

The mall receives 20% of the annual profit.
Total Profit for type $k$ if $m$ stores are opened is $m \cdot p_{k,m}$.
Total Rent Income from type $k$ if $m$ stores are opened is $0.20 \cdot m \cdot p_{k,m}$.

We want to **Maximize** Total Rental Income ($Z$).

$$ \text{Maximize } Z = \sum_{k \in J} \sum_{m=0}^{U_k} (0.20 \cdot m \cdot p_{k,m}) \cdot y_{k,m} $$

Let's compute the coefficients $C_{k,m} = 0.20 \cdot m \cdot p_{k,m}$ (in thousand Yuan):

**Type 1 (Jewelry):**
- $m=0$: $0$
- $m=1$: $0.2 \cdot 1 \cdot 9 = 1.8$
- $m=2$: $0.2 \cdot 2 \cdot 8 = 3.2$
- $m=3$: $0.2 \cdot 3 \cdot 7 = 4.2$

**Type 2 (Shoes & Hats):**
- $m=0$: $0$ (Not allowed as $L_2=1$, but included for binary completeness if we allow 0 in index, though constraint will forbid it)
- $m=1$: $0.2 \cdot 1 \cdot 10 = 2.0$
- $m=2$: $0.2 \cdot 2 \cdot 9 = 3.6$

**Type 3 (Department Store):**
- $m=0$: $0$
- $m=1$: $0.2 \cdot 1 \cdot 27 = 5.4$
- $m=2$: $0.2 \cdot 2 \cdot 21 = 8.4$
- $m=3$: $0.2 \cdot 3 \cdot 20 = 12.0$

**Type 4 (Bookstore):**
- $m=0$: $0$
- $m=1$: $0.2 \cdot 1 \cdot 16 = 3.2$
- $m=2$: $0.2 \cdot 2 \cdot 10 = 4.0$

**Type 5 (Catering):**
- $m=0$: $0$
- $m=1$: $0.2 \cdot 1 \cdot 17 = 3.4$
- $m=2$: $0.2 \cdot 2 \cdot 15 = 6.0$
- $m=3$: $0.2 \cdot 3 \cdot 12 = 7.2$

**Objective Function:**
$$ \text{Maximize } Z = 1.8 y_{1,1} + 3.2 y_{1,2} + 4.2 y_{1,3} + 2.0 y_{2,1} + 3.6 y_{2,2} + 5.4 y_{3,1} + 8.4 y_{3,2} + 12.0 y_{3,3} + 3.2 y_{4,1} + 4.0 y_{4,2} + 3.4 y_{5,1} + 6.0 y_{5,2} + 7.2 y_{5,3} $$
*(Note: Terms with $m=0$ contribute 0 to the objective, so they are omitted for brevity, but variables $y_{k,0}$ exist in the model to satisfy "exactly one" constraints if $L_k=0$.)*

## 4. Operational Constraints

### A. Selection Constraints (Exactly one count per type)
For each store type $k$, exactly one number of stores must be chosen.
$$ \sum_{m=0}^{U_k} y_{k,m} = 1 \quad \forall k \in J $$

### B. Minimum Store Requirements
The problem specifies a minimum number of stores for each type. This is enforced by setting the binary variables for counts below the minimum to 0.
- For Type 1 ($L_1=1$): $y_{1,0} = 0$
- For Type 2 ($L_2=1$): $y_{2,0} = 0$
- For Type 3 ($L_3=1$): $y_{3,0} = 0$
- For Type 4 ($L_4=0$): No restriction (can be 0, 1, or 2)
- For Type 5 ($L_5=1$): $y_{5,0} = 0$

Alternatively, these can be written as constraints:
$$ \sum_{m=0}^{L_k - 1} y_{k,m} = 0 \quad \forall k \in J $$
*(Note: If $L_k=0$, the sum is over an empty set or $m=0$ to $-1$, which is 0, so no constraint needed. If $L_k=1$, $y_{k,0}=0$.)*

### C. Total Area Constraint
The total area occupied by all leased stores must not exceed the available area (5,000 m²).
The area occupied by type $k$ when $m$ stores are chosen is $m \cdot a_k$.
$$ \sum_{k \in J} \sum_{m=0}^{U_k} (m \cdot a_k) \cdot y_{k,m} \le 5000 $$

Let's expand this using the area values $a_k$:
- Type 1 ($a_1=250$): $0 y_{1,0} + 250 y_{1,1} + 500 y_{1,2} + 750 y_{1,3}$
- Type 2 ($a_2=350$): $0 y_{2,0} + 350 y_{2,1} + 700 y_{2,2}$
- Type 3 ($a_3=800$): $0 y_{3,0} + 800 y_{3,1} + 1600 y_{3,2} + 2400 y_{3,3}$
- Type 4 ($a_4=400$): $0 y_{4,0} + 400 y_{4,1} + 800 y_{4,2}$
- Type 5 ($a_5=500$): $0 y_{5,0} + 500 y_{5,1} + 1000 y_{5,2} + 1500 y_{5,3}$

**Constraint:**
$$ 250 y_{1,1} + 500 y_{1,2} + 750 y_{1,3} + 350 y_{2,1} + 700 y_{2,2} + 800 y_{3,1} + 1600 y_{3,2} + 2400 y_{3,3} + 400 y_{4,1} + 800 y_{4,2} + 500 y_{5,1} + 1000 y_{5,2} + 1500 y_{5,3} \le 5000 $$

### D. Variable Domains
- $y_{1,m} \in \{0,1\}$ for $m \in \{0,1,2,3\}$
- $y_{2,m} \in \{0,1\}$ for $m \in \{0,1,2\}$
- $y_{3,m} \in \{0,1\}$ for $m \in \{0,1,2,3\}$
- $y_{4,m} \in \{0,1\}$ for $m \in \{0,1,2\}$
- $y_{5,m} \in \{0,1\}$ for $m \in \{0,1,2,3\}$

*(Note: Variables $y_{k,0}$ are included in the domain to satisfy the "sum to 1" constraint for types that allow 0 stores (Type 4) and to formally exclude 0 for other types via constraint B.)*

---

## Summary of the MILP Formulation

**Maximize:**
$$ Z = 1.8 y_{1,1} + 3.2 y_{1,2} + 4.2 y_{1,3} + 2.0 y_{2,1} + 3.6 y_{2,2} + 5.4 y_{3,1} + 8.4 y_{3,2} + 12.0 y_{3,3} + 3.2 y_{4,1} + 4.0 y_{4,2} + 3.4 y_{5,1} + 6.0 y_{5,2} + 7.2 y_{5,3} $$

**Subject to:**

1. **Selection Constraints:**
   - $y_{1,0} + y_{1,1} + y_{1,2} + y_{1,3} = 1$
   - $y_{2,0} + y_{2,1} + y_{2,2} = 1$
   - $y_{3,0} + y_{3,1} + y_{3,2} + y_{3,3} = 1$
   - $y_{4,0} + y_{4,1} + y_{4,2} = 1$
   - $y_{5,0} + y_{5,1} + y_{5,2} + y_{5,3} = 1$

2. **Minimum Count Constraints:**
   - $y_{1,0} = 0$
   - $y_{2,0} = 0$
   - $y_{3,0} = 0$
   - $y_{5,0} = 0$
   - *(Type 4 has no minimum, so $y_{4,0}$ is free to be 0 or 1)*

3. **Area Constraint:**
   - $250 y_{1,1} + 500 y_{1,2} + 750 y_{1,3} + 350 y_{2,1} + 700 y_{2,2} + 800 y_{3,1} + 1600 y_{3,2} + 2400 y_{3,3} + 400 y_{4,1} + 800 y_{4,2} + 500 y_{5,1} + 1000 y_{5,2} + 1500 y_{5,3} \le 5000$

4. **Binary Constraints:**
   - $y_{k,m} \in \{0, 1\}$ for all defined $k, m$.