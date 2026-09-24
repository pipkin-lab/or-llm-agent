### 1. Index Sets & Parameters

**Index Sets:**
- $J = \{1, 2, 3\}$: Set of components ($A_1, A_2, A_3$).
- $K = \{1, 2, 3\}$: Set of possible numbers of spare parts for each component.

**Parameters:**
- $C_{j,k}$: Cost (in thousand yuan) of allocating $k$ spare parts to component $j$.
  - Row 1 ($k=1$): $C_{1,1}=1, C_{2,1}=3, C_{3,1}=2$
  - Row 2 ($k=2$): $C_{1,2}=2, C_{2,2}=5, C_{3,2}=3$
  - Row 3 ($k=3$): $C_{1,3}=3, C_{2,3}=6, C_{3,3}=4$
- $R_{j,k}$: Reliability of component $j$ when $k$ spare parts are allocated.
  - Row 1 ($k=1$): $R_{1,1}=0.3, R_{2,1}=0.2, R_{3,1}=0.1$
  - Row 2 ($k=2$): $R_{1,2}=0.4, R_{2,2}=0.5, R_{3,2}=0.2$
  - Row 3 ($k=3$): $R_{1,3}=0.5, R_{2,3}=0.9, R_{3,3}=0.7$
- $L_{j,k}$: Logarithm of reliability, $L_{j,k} = \ln(R_{j,k})$.
  - $L_{1,1} = \ln(0.3) \approx -1.2040$
  - $L_{1,2} = \ln(0.4) \approx -0.9163$
  - $L_{1,3} = \ln(0.5) \approx -0.6931$
  - $L_{2,1} = \ln(0.2) \approx -1.6094$
  - $L_{2,2} = \ln(0.5) \approx -0.6931$
  - $L_{2,3} = \ln(0.9) \approx -0.1054$
  - $L_{3,1} = \ln(0.1) \approx -2.3026$
  - $L_{3,2} = \ln(0.2) \approx -1.6094$
  - $L_{3,3} = \ln(0.7) \approx -0.3567$
- $B$: Total budget limit (8 thousand yuan).

### 2. Decision Variables

Define binary decision variables:
- $x_{j,k} \in \{0, 1\}$ for all $j \in J, k \in K$.
  - $x_{j,k} = 1$ if component $j$ is allocated exactly $k$ spare parts.
  - $x_{j,k} = 0$ otherwise.

### 3. Objective Function

The goal is to maximize the equipment's operational reliability. Since the components work in series, the total reliability is the product of individual reliabilities: $P = R_1 \cdot R_2 \cdot R_3$.
Maximizing $P$ is equivalent to maximizing $\ln(P) = \ln(R_1) + \ln(R_2) + \ln(R_3)$.

**Solver Objective (Linear in variables):**
$$ \text{Maximize } Z = \sum_{j=1}^{3} \sum_{k=1}^{3} L_{j,k} \cdot x_{j,k} $$

*Note: The final reported answer should be the product of the optimal reliabilities, but the solver optimizes the sum of logs.*

### 4. Operational Constraints

**1. Allocation Completeness Constraint:**
Each component must be assigned exactly one number of spare parts (from the available options 1, 2, or 3).
$$ \sum_{k=1}^{3} x_{j,k} = 1, \quad \forall j \in \{1, 2, 3\} $$

**2. Budget Constraint:**
The total cost must not exceed the budget limit of 8 thousand yuan.
$$ \sum_{j=1}^{3} \sum_{k=1}^{3} C_{j,k} \cdot x_{j,k} \le 8 $$

**3. Variable Bounds:**
$$ x_{j,k} \in \{0, 1\}, \quad \forall j \in J, k \in K $$

---

### Mathematical Formulation Summary

**Sets:**
$J = \{1, 2, 3\}$, $K = \{1, 2, 3\}$

**Parameters:**
$C_{1,1}=1, C_{2,1}=3, C_{3,1}=2, C_{1,2}=2, C_{2,2}=5, C_{3,2}=3, C_{1,3}=3, C_{2,3}=6, C_{3,3}=4$
$L_{1,1}=\ln(0.3), L_{1,2}=\ln(0.4), L_{1,3}=\ln(0.5)$
$L_{2,1}=\ln(0.2), L_{2,2}=\ln(0.5), L_{2,3}=\ln(0.9)$
$L_{3,1}=\ln(0.1), L_{3,2}=\ln(0.2), L_{3,3}=\ln(0.7)$

**Variables:**
$x_{j,k} \in \{0, 1\}$

**Model:**
$$ \text{Maximize } Z = \sum_{j=1}^{3} \sum_{k=1}^{3} L_{j,k} x_{j,k} $$

Subject to:
$$ \sum_{k=1}^{3} x_{1,k} = 1 $$
$$ \sum_{k=1}^{3} x_{2,k} = 1 $$
$$ \sum_{k=1}^{3} x_{3,k} = 1 $$
$$ 1x_{1,1} + 3x_{2,1} + 2x_{3,1} + 2x_{1,2} + 5x_{2,2} + 3x_{3,2} + 3x_{1,3} + 6x_{2,3} + 4x_{3,3} \le 8 $$
$$ x_{j,k} \in \{0, 1\} \quad \forall j,k $$