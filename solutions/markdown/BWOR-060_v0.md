## Model Type
**MILP** (Mixed-Integer Linear Programming)
*Note: The objective function contains Euclidean distances, which are non-linear. However, in standard facility location problems of this size (8 candidate sites), the problem is typically solved by enumerating the $\binom{8}{2}=28$ possible pairs of schools and calculating the total distance for each, or by using a non-linear solver. Since the prompt asks for a mathematical formulation, we provide the standard **Non-Linear** formulation first, but as this is a discrete location problem with a small number of candidates, it is often treated as a combinatorial optimization problem. Given the strict "LP/MILP/QP/NL" classification, this is a **NON-LINEAR** problem due to the Euclidean distance in the objective. However, to make it solvable by standard MILP solvers, one would linearize the distance or use the enumeration approach. Here, we provide the precise **NON-LINEAR** formulation as it is the direct mathematical translation of the problem statement.*

Actually, looking at standard OR problem sets like this (likely from a textbook like "Operations Research" or similar), these are often solved via enumeration or specialized solvers. Let's provide the **NON-LINEAR** formulation as it is the most direct representation. If a linear model is strictly required, one would need to linearize the Euclidean distance (e.g., using piecewise linear approximations), which is complex. However, given the small size (8 villages), the most robust "model" for a code agent to solve is actually a simple combinatorial search or a non-linear solver.

Let's stick to the **NON-LINEAR** classification because the objective is the sum of Euclidean distances.

## Index Sets & Parameters

**Index Sets:**
- $I$: Set of villages, $I = \{1, 2, 3, 4, 5, 6, 7, 8\}$.
- $J$: Set of candidate school locations, $J = I$ (since schools are built in villages).

**Parameters:**
- $x_i, y_i$: Coordinates of village $i$.
  - $x = [0, 10, 12, 14, 16, 18, 8, 6]$
  - $y = [0, 3, 15, 13, 9, 6, 12, 10]$
- $N_i$: Number of primary school students in village $i$.
  - $N = [60, 80, 100, 120, 80, 60, 40, 80]$
- $K$: Number of schools to build, $K = 2$.
- $d_{ij}$: Euclidean distance between village $i$ and candidate site $j$.
  - $d_{ij} = \sqrt{(x_i - x_j)^2 + (y_i - y_j)^2}$

## Decision Variables

- $z_j \in \{0, 1\}$ for $j \in J$: Binary variable where $z_j = 1$ if a school is built in village $j$, and $0$ otherwise.
- $w_{ij} \in \{0, 1\}$ for $i \in I, j \in J$: Binary variable where $w_{ij} = 1$ if students from village $i$ are assigned to the school in village $j$, and $0$ otherwise.

## Objective Function

Minimize the total walking distance for all students:

$$ \min \sum_{i \in I} \sum_{j \in J} N_i \cdot d_{ij} \cdot w_{ij} $$

## Operational Constraints

1. **Exactly K schools must be built:**
   $$ \sum_{j \in J} z_j = K \quad (K=2) $$

2. **Each student group (village) must be assigned to exactly one school:**
   $$ \sum_{j \in J} w_{ij} = 1 \quad \forall i \in I $$

3. **Students can only be assigned to a village if a school is built there:**
   $$ w_{ij} \le z_j \quad \forall i \in I, \forall j \in J $$

4. **Variable Domains:**
   $$ z_j \in \{0, 1\} \quad \forall j \in J $$
   $$ w_{ij} \in \{0, 1\} \quad \forall i \in I, \forall j \in J $$

---

### **Alternative: Enumeration Approach (Recommended for Implementation)**

Since $N=8$ is very small, the problem is often more efficiently modeled/solved by enumerating all $\binom{8}{2} = 28$ pairs of villages. For each pair $(A, B)$, the cost is calculated by assigning each village $i$ to the closer of $A$ or $B$ (ties can be broken arbitrarily or by splitting, but usually "closer" implies nearest neighbor assignment).

**Cost for a specific pair of school locations $(s_1, s_2)$:**
$$ \text{Cost}(s_1, s_2) = \sum_{i \in I} N_i \cdot \min(d_{i, s_1}, d_{i, s_2}) $$

The optimal solution is the pair $(s_1, s_2)$ that minimizes this cost. This avoids the non-linear variables $w_{ij}$ and the non-linear objective, reducing the problem to a simple exhaustive search over 28 candidates, which is trivial computationally.

However, strictly following the "formulate a mathematical model" instruction, the **NON-LINEAR** formulation above is the direct translation. If a **MILP** is strictly required, the distance $d_{ij}$ is a constant parameter (calculated from coordinates), so the objective is actually **Linear** in the decision variables $w_{ij}$!

**Correction on Model Type:**
The distances $d_{ij}$ are **parameters**, not variables. The coordinates are fixed. Therefore, $d_{ij}$ is a constant number.
The objective is $\min \sum_{i,j} C_{ij} w_{ij}$ where $C_{ij} = N_i \cdot d_{ij}$ is a constant parameter.
The constraints are linear.
The variables are binary.
Therefore, this is a pure **MILP** (or more specifically, an Integer Linear Programming problem). The non-linearity of the distance calculation happens *before* the model is solved, during the parameter extraction phase.

**Revised Model Type: MILP**

## Revised Index Sets & Parameters (with computed constants)

We calculate the distance matrix $D$ where $D_{ij} = \sqrt{(x_i-x_j)^2 + (y_i-y_j)^2}$.
Then the cost coefficient $C_{ij} = N_i \times D_{ij}$.

| i\j | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | 0 | 10.44 | 18.97 | 20.81 | 18.87 | 18.36 | 12.81 | 11.40 |
| **2** | 10.44 | 0 | 12.08 | 10.44 | 6.40 | 8.06 | 9.22 | 7.21 |
| **3** | 18.97 | 12.08 | 0 | 2.83 | 8.06 | 12.81 | 7.21 | 5.66 |
| **4** | 20.81 | 10.44 | 2.83 | 0 | 2.83 | 5.66 | 10.44 | 8.94 |
| **5** | 18.87 | 6.40 | 8.06 | 2.83 | 0 | 2.83 | 7.21 | 4.47 |
| **6** | 18.36 | 8.06 | 12.81 | 5.66 | 2.83 | 0 | 10.44 | 7.21 |
| **7** | 12.81 | 9.22 | 7.21 | 10.44 | 7.21 | 10.44 | 0 | 2.83 |
| **8** | 11.40 | 7.21 | 5.66 | 8.94 | 4.47 | 7.21 | 2.83 | 0 |

*(Distances rounded to 2 decimal places for display, but should be kept as full precision in code)*.

## Final Decision Variables

- $z_j \in \{0, 1\}$ for $j=1,\dots,8$: 1 if school is built in village $j$.
- $w_{ij} \in \{0, 1\}$ for $i=1,\dots,8, j=1,\dots,8$: 1 if students from village $i$ go to school in village $j$.

## Final Objective Function

$$ \min \sum_{i=1}^{8} \sum_{j=1}^{8} C_{ij} w_{ij} $$
Where $C_{ij} = N_i \times \sqrt{(x_i - x_j)^2 + (y_i - y_j)^2}$.

## Final Operational Constraints

1.  **Number of Schools:**
    $$ \sum_{j=1}^{8} z_j = 2 $$

2.  **Assignment Completeness:**
    $$ \sum_{j=1}^{8} w_{ij} = 1 \quad \forall i \in \{1,\dots,8\} $$

3.  **Linking Constraints:**
    $$ w_{ij} \le z_j \quad \forall i, j \in \{1,\dots,8\} $$

4.  **Integrality:**
    $$ z_j, w_{ij} \in \{0, 1\} \quad \forall i, j $$