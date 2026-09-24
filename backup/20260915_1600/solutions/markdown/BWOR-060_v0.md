To formulate this problem, we first identify the structure: it is a **Facility Location Problem** (specifically, an uncapacitated facility location problem with a fixed number of facilities). We need to select exactly 2 villages to host schools such that the total weighted Euclidean distance from all students to their nearest school is minimized.

### MANDATORY COST INVENTORY & PARAMETER COMPLETENESS
1.  **Coordinates**: Extracted from Table 5-14.
    *   Village 1: $(0, 0)$, Students: 60
    *   Village 2: $(10, 3)$, Students: 80
    *   Village 3: $(12, 15)$, Students: 100
    *   Village 4: $(14, 13)$, Students: 120
    *   Village 5: $(16, 9)$, Students: 80
    *   Village 6: $(18, 6)$, Students: 60
    *   Village 7: $(8, 12)$, Students: 40
    *   Village 8: $(6, 10)$, Students: 80
2.  **Distances**: The problem states "Walking distance is calculated using Euclidean distance." Thus, the cost $c_{ij}$ for village $i$ to school in village $j$ is $\sqrt{(x_i - x_j)^2 + (y_i - y_j)^2}$.
3.  **Objective**: Minimize total walking distance = $\sum_{i} \sum_{j} n_i \cdot d_{ij} \cdot y_{ij}$, where $y_{ij}$ indicates if village $i$ is assigned to school $j$.
4.  **Constraint**: Exactly 2 schools must be built.

This is a **Mixed Integer Linear Programming (MILP)** problem if we linearize the assignment, but since the distances are fixed parameters calculated from coordinates, and the assignment is binary, it is a **Binary Integer Program** (subset of MILP). However, standard facility location formulations are often solved as MILPs. Since the objective function coefficients are constant (distances are pre-calculated parameters, not variables interacting non-linearly in the objective in a way that requires QP solvers *if* we use the standard assignment variables), it can be modeled as an **ILP/MILP**.

*Note on Linearity*: The term $y_{ij}$ is binary. The distance $d_{ij}$ is a constant parameter. The product $d_{ij} y_{ij}$ is linear. Therefore, this is a **Linear** Integer Program (ILP).

**Model Type**: MILP (or ILP)

---

## Formal Mathematical Model

### 1. Index Sets & Parameters

**Index Sets:**
*   $I = \{1, 2, 3, 4, 5, 6, 7, 8\}$: Set of villages (potential school locations and student origins).
*   $J = \{1, 2, 3, 4, 5, 6, 7, 8\}$: Set of potential school locations (same as $I$).

**Parameters:**
*   $x_i, y_i$: Coordinates of village $i \in I$.
    *   $x = [0, 10, 12, 14, 16, 18, 8, 6]$
    *   $y = [0, 3, 15, 13, 9, 6, 12, 10]$
*   $n_i$: Number of students in village $i \in I$.
    *   $n_1=60, n_2=80, n_3=100, n_4=120, n_5=80, n_6=60, n_7=40, n_8=80$
*   $d_{ij}$: Euclidean distance between village $i$ and village $j$, defined as:
    $$ d_{ij} = \sqrt{(x_i - x_j)^2 + (y_i - y_j)^2} \quad \forall i, j \in I $$
    *(Note: These are constant parameters computed from the coordinates.)*
*   $K = 2$: The exact number of schools to be built.

### 2. Decision Variables

*   $S_j \in \{0, 1\}$: Binary variable.
    *   $S_j = 1$ if a school is built in village $j$, 0 otherwise.
*   $A_{ij} \in \{0, 1\}$: Binary variable.
    *   $A_{ij} = 1$ if village $i$ is assigned to the school in village $j$, 0 otherwise.

### 3. Objective Function

Minimize the total weighted walking distance for all students:

$$ \text{Minimize } Z = \sum_{i \in I} \sum_{j \in I} n_i \cdot d_{ij} \cdot A_{ij} $$

### 4. Operational Constraints

**1. Exactly K schools are built:**
$$ \sum_{j \in J} S_j = 2 $$

**2. Each village is assigned to exactly one school:**
$$ \sum_{j \in J} A_{ij} = 1 \quad \forall i \in I $$

**3. Assignment feasibility (A village can only be assigned to a location where a school is built):**
$$ A_{ij} \leq S_j \quad \forall i \in I, \forall j \in J $$

**4. Variable Domains:**
$$ S_j \in \{0, 1\} \quad \forall j \in J $$
$$ A_{ij} \in \{0, 1\} \quad \forall i \in I, \forall j \in J $$

---

### Feasibility & Sanity Check

1.  **Feasibility**: Since $K=2$ and there are 8 villages, it is possible to choose any 2 distinct villages to build schools. Every village will be assigned to one of them. The model is feasible.
2.  **Objective Magnitude**:
    *   Total students $N = 60+80+100+120+80+60+40+80 = 620$.
    *   Distances are in the range of roughly 0 to $\sqrt{18^2+15^2} \approx 23$.
    *   Expected total distance is roughly $620 \times \text{avg\_distance}$. If average distance is ~10, total Z ~ 6200. This is a reasonable magnitude for the sum of distances.
3.  **Unit Consistency**: All distances are in the same coordinate units. Student counts are integers. The objective is in "student-units of distance". This matches the request to "minimize the total walking distance".

### Parameter Verification
*   $n_i$: All values present in text.
*   $x_i, y_i$: All values present in text.
*   $K=2$: Explicitly stated ("build one primary school in each of two villages").
*   $d_{ij}$: Calculated from provided coordinates.

The model is complete and ready for solution.