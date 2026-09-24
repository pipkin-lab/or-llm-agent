To solve this problem, we must model a **2-Machine Flow Shop Scheduling Problem** with the objective of minimizing the **Makespan** (total processing time from the start of the first job on Machine A to the completion of the last job on Machine B).

### 1. Index Sets & Parameters

**Index Sets:**
*   $J = \{1, 2, 3, 4, 5, 6\}$: Set of jobs.
*   $M = \{A, B\}$: Set of machines.

**Parameters:**
*   $a_j$: Processing time of job $j$ on Machine A (minutes).
*   $b_j$: Processing time of job $j$ on Machine B (minutes).

**Data from Table:**
| Job ($j$) | $a_j$ (Min A) | $b_j$ (Min B) |
| :--- | :---: | :---: |
| 1 | 30 | 70 |
| 2 | 60 | 70 |
| 3 | 60 | 50 |
| 4 | 20 | 60 |
| 5 | 80 | 30 |
| 6 | 90 | 40 |

### 2. Decision Variables

We use a **Position-Based** formulation which is standard for small-scale flow shop problems ($n \le 6$).

*   $x_{j,k} \in \{0, 1\}$: Binary variable where $x_{j,k} = 1$ if Job $j$ is scheduled in position $k$ in the sequence, and 0 otherwise.
*   $S_{k}^{A} \ge 0$: Continuous variable representing the **start time** of the job in position $k$ on Machine A.
*   $C_{k}^{A} \ge 0$: Continuous variable representing the **completion time** of the job in position $k$ on Machine A.
*   $S_{k}^{B} \ge 0$: Continuous variable representing the **start time** of the job in position $k$ on Machine B.
*   $C_{k}^{B} \ge 0$: Continuous variable representing the **completion time** of the job in position $k$ on Machine B.
*   $Z \ge 0$: Continuous variable representing the Makespan (objective value).

### 3. Objective Function

Minimize the total completion time of the last job on Machine B:

$$
\text{Minimize } Z = C_{n}^{B}
$$
*(Where $n=6$ is the total number of jobs)*

### 4. Operational Constraints

#### A. Assignment Constraints
Each job must be assigned to exactly one position, and each position must contain exactly one job.

1.  **Job Assignment:**
    $$ \sum_{k=1}^{n} x_{j,k} = 1, \quad \forall j \in J $$
2.  **Position Assignment:**
    $$ \sum_{j=1}^{n} x_{j,k} = 1, \quad \forall k \in \{1, \dots, n\} $$

#### B. Machine A Scheduling Constraints
Since Machine A is the first stage, there is no idle time constraint from a previous machine, but jobs must be processed sequentially. We can define the start times directly based on the sequence.

3.  **Start Time of First Job on A:**
    $$ S_{1}^{A} = 0 $$
4.  **Sequential Processing on A:**
    The start time of job at position $k$ on A equals the completion time of job at position $k-1$ on A.
    $$ S_{k}^{A} = C_{k-1}^{A}, \quad \forall k \in \{2, \dots, n\} $$
5.  **Completion Time on A:**
    The completion time of job at position $k$ on A is the start time plus the processing time of the job assigned to that position.
    $$ C_{k}^{A} = S_{k}^{A} + \sum_{j \in J} a_j x_{j,k}, \quad \forall k \in \{1, \dots, n\} $$

#### C. Machine B Scheduling Constraints
Machine B has two constraints:
1.  **Precedence:** A job cannot start on B until it is finished on A.
2.  **Sequentiality:** Jobs must be processed one after another on B.

6.  **Start Time of First Job on B:**
    The first job on B cannot start until it is done on A.
    $$ S_{1}^{B} = C_{1}^{A} $$
7.  **Sequential Processing on B:**
    The start time of the job at position $k$ on B must be at least the completion time of the job at position $k-1$ on B.
    $$ S_{k}^{B} \ge C_{k-1}^{B}, \quad \forall k \in \{2, \dots, n\} $$
8.  **Precedence Constraint (A before B):**
    The job at position $k$ cannot start on B until it is complete on A.
    $$ S_{k}^{B} \ge C_{k}^{A}, \quad \forall k \in \{1, \dots, n\} $$
    *(Note: Combining constraints 7 and 8, we can write $S_{k}^{B} = \max(C_{k-1}^{B}, C_{k}^{A})$. In MILP, this is handled by the two inequalities above.)*
9.  **Completion Time on B:**
    $$ C_{k}^{B} = S_{k}^{B} + \sum_{j \in J} b_j x_{j,k}, \quad \forall k \in \{1, \dots, n\} $$

#### D. Objective Linking

10. **Makespan Definition:**
    $$ Z \ge C_{n}^{B} $$
    *(Since we are minimizing, $Z$ will take the exact value of $C_{n}^{B}$).*

### Summary of Model Structure

This is a **Mixed Integer Linear Programming (MILP)** model.

*   **Binary Variables:** $x_{j,k}$ (36 variables for 6 jobs $\times$ 6 positions).
*   **Continuous Variables:** $S_k^A, C_k^A, S_k^B, C_k^B, Z$ (25 variables).
*   **Constraints:**
    *   12 Assignment constraints.
    *   5 Sequential A constraints.
    *   6 Completion A equations.
    *   1 First B start constraint.
    *   5 Sequential B constraints.
    *   6 Precedence B constraints.
    *   6 Completion B equations.
    *   1 Objective link.

This formulation guarantees a valid permutation schedule for all 6 jobs that respects the flow shop constraints (A $\to$ B) and minimizes the makespan. For $N=6$, this model is computationally trivial for any standard solver.