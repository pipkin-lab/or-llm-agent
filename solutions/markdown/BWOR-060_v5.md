## Model Type: MILP (Mixed-Integer Linear Programming)

*(Note: The underlying problem is a non-linear Quadratic Assignment/Location problem due to Euclidean distances. However, since the distance matrix is pre-computable and the objective becomes linear in the assignment variables once distances are fixed, this can be solved as a standard MILP or even a pure integer program.)*

### 1. Index Sets & Parameters

**Index Sets:**
*   $N$: Set of all villages, $\{1, 2, 3, 4, 5, 6, 7, 8\}$.
*   $S$: Set of school sites to be selected (size $|S|=2$).

**Parameters:**
*   $n_i$: Number of students in village $i$ (from Table 5-14).
    *   $n_1 = 60, n_2 = 80, n_3 = 100, n_4 = 120, n_5 = 80, n_6 = 60, n_7 = 40, n_8 = 80$.
*   $(x_i, y_i)$: Coordinates of village $i$.
    *   $V_1: (0, 0)$
    *   $V_2: (10, 3)$
    *   $V_3: (12, 15)$
    *   $V_4: (14, 13)$
    *   $V_5: (16, 9)$
    *   $V_6: (18, 6)$
    *   $V_7: (8, 12)$
    *   $V_8: (6, 10)$
*   $d_{ij}$: Euclidean distance between village $i$ and village $j$, calculated as $\sqrt{(x_i - x_j)^2 + (y_i - y_j)^2}$.
    *   *Note: $d_{ij}$ is a fixed parameter derived from the coordinates. If a school is built in village $j$, students from village $i$ walk distance $d_{ij}$.*

### 2. Decision Variables

Let $x_{ij}$ be a binary variable:
$$
x_{ij} = 
\begin{cases} 
1 & \text{if the school assigned to serve village } i \text{ is located in village } j \\
0 & \text{otherwise}
\end{cases}
$$
For all $i \in N, j \in N$.

*(Alternative simpler formulation: Let $y_j$ be binary, 1 if a school is built in village $j$. Then we need assignment variables to link students to schools. The $x_{ij}$ formulation above directly assigns each village's students to a specific school site. Since there are only 2 schools, this works well.)*

Actually, a more standard and efficient formulation for "p-median" style problems is:
Let $y_j \in \{0,1\}$ for $j \in N$, where $y_j=1$ if a school is built in village $j$.
Let $z_{ij} \in \{0,1\}$ for $i \in N, j \in N$, where $z_{ij}=1$ if the students from village $i$ are assigned to the school in village $j$.

### 3. Objective Function

Minimize the total weighted walking distance for all students:

$$
\text{Minimize } Z = \sum_{i \in N} \sum_{j \in N} n_i \cdot d_{ij} \cdot z_{ij}
$$

### 4. Operational Constraints

1.  **Exactly two schools are built:**
    $$
    \sum_{j \in N} y_j = 2
    $$

2.  **Each village's students are assigned to exactly one school:**
    $$
    \sum_{j \in N} z_{ij} = 1 \quad \forall i \in N
    $$

3.  **Students can only be assigned to a school if one is built there:**
    $$
    z_{ij} \le y_j \quad \forall i \in N, \forall j \in N
    $$
    *(This ensures $z_{ij}=0$ if $y_j=0$.)*

4.  **Variable Domains:**
    $$
    y_j \in \{0, 1\} \quad \forall j \in N
    $$
    $$
    z_{ij} \in \{0, 1\} \quad \forall i \in N, \forall j \in N
    $$

### Parameter Completeness & Verification

*   **Costs/Parameters:** All student counts $n_i$ and coordinates $(x_i, y_i)$ are provided in Table 5-14.
*   **Distances:** $d_{ij}$ are calculated from the provided coordinates.
    *   Example: $d_{1,2} = \sqrt{(10-0)^2 + (3-0)^2} = \sqrt{109} \approx 10.44$
    *   Example: $d_{1,3} = \sqrt{(12-0)^2 + (15-0)^2} = \sqrt{144+225} = \sqrt{369} \approx 19.21$
    *   All $d_{ij}$ values are deterministic and derived from the problem data.
*   **Objective Units:** The objective $Z$ is in "student-distance units". This matches the problem's request to "minimize the total walking distance for all primary school students".
*   **Feasibility:** We need to choose 2 sites out of 8. There are $\binom{8}{2}=28$ possible pairs. For each pair, the optimal assignment is trivially each village assigning to the closer of the two schools (or either if equidistant). The MILP formulation handles this automatically.

This formulation is a standard **2-median problem** on a graph where nodes are villages and edge weights are Euclidean distances, with node weights being the number of students.