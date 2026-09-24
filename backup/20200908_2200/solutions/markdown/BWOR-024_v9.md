### 1. Index Sets & Parameters

**Index Sets:**
*   $J = \{1, 2, 3, 4, 5, 6\}$: Set of jobs.
*   $M = \{A, B\}$: Set of machines.
*   $K = \{1, 2, 3, 4, 5, 6\}$: Set of sequence positions (slots).

**Parameters:**
*   $a_j$: Processing time of job $j$ on Machine A (minutes).
    *   $a_1=30, a_2=60, a_3=60, a_4=20, a_5=80, a_6=90$
*   $b_j$: Processing time of job $j$ on Machine B (minutes).
    *   $b_1=70, b_2=70, b_3=50, b_4=60, b_5=30, b_6=40$
*   $T = |J| = 6$: Total number of jobs.

### 2. Decision Variables

Since the scale is small ($n=6$), we use binary variables to represent the sequence. We define variables based on the position of each job in the sequence.

*   $x_{jk} \in \{0, 1\}$: Binary variable where $x_{jk} = 1$ if job $j$ is assigned to position $k$ in the sequence, and 0 otherwise.
*   $C_{j}^{A}$: Continuous variable representing the completion time of job $j$ on Machine A.
*   $C_{j}^{B}$: Continuous variable representing the completion time of job $j$ on Machine B.
*   $Z$: Continuous variable representing the makespan (total processing time).

### 3. Objective Function

Minimize the total processing time (Makespan), which is the completion time of the last job on Machine B.

$$ \text{Minimize } Z $$

### 4. Operational Constraints

**1. Assignment Constraints (Each job in exactly one position, each position has exactly one job):**
$$ \sum_{k=1}^{T} x_{jk} = 1 \quad \forall j \in J $$
$$ \sum_{j \in J} x_{jk} = 1 \quad \forall k \in K $$

**2. Machine A Scheduling Logic:**
Job $j$ starts on Machine A at time $S_j^A$. Since there is no setup time and Machine A is the first stage, the start time depends only on the jobs preceding it in the sequence.
We can formulate the completion time $C_j^A$ directly using the sequence positions.
$$ C_j^A = \sum_{k=1}^{T} k \cdot x_{jk} \cdot a_j \quad \text{(This is incorrect, need cumulative sum)} $$

*Correction for Scheduling Logic:*
It is more robust to define start times or use pairwise disjunctive constraints, but for a 2-machine flow shop, we can use the following linear formulation based on the sequence index.

Let $S_j^A$ be the start time of job $j$ on Machine A.
$$ S_j^A \ge \sum_{k=1}^{T} k \cdot x_{jk} \cdot a_j - \sum_{m \in J} a_m \cdot M \cdot (1 - \dots) $$
*Actually, a cleaner approach for small $n$ is to use the position variables to calculate cumulative times.*

Let's use the standard formulation for 2-machine flow shop minimization of makespan.

**Constraint Set 1: Completion on Machine A**
The completion time of job $j$ on Machine A is the sum of processing times of all jobs $i$ that are scheduled before or equal to job $j$ in the sequence.
$$ C_j^A = \sum_{i \in J} a_i \cdot \delta_{ij} $$
Where $\delta_{ij} = 1$ if job $i$ is scheduled at or before the position of job $j$.
To linearize this without $\delta$, we can use the property that if job $i$ is at position $p$ and job $j$ is at position $q$, job $i$ finishes before job $j$ starts on A if $p < q$.

A simpler linear formulation for $C_j^A$:
$$ C_j^A = \sum_{k=1}^{T} \sum_{i \in J} a_i \cdot x_{ik} \cdot y_{k,j} $$
This is getting complex. Let's use the **Start Time** formulation which is standard and linear.

Let $S_j^A$ = Start time of job $j$ on Machine A.
Let $S_j^B$ = Start time of job $j$ on Machine B.

**Constraint 2: Machine A Non-Overlapping (Sequence Definition)**
For any pair of distinct jobs $i, j \in J$ ($i < j$):
If job $i$ is before job $j$ in the sequence, then job $j$ cannot start on A until job $i$ finishes.
We introduce binary variables $y_{ij} \in \{0,1\}$ where $y_{ij}=1$ if job $i$ is scheduled before job $j$.
$$ y_{ij} + y_{ji} = 1 \quad \forall i, j \in J, i < j $$

**Constraint 3: Machine A Start Times**
$$ S_j^A \ge S_i^A + a_i - M(1 - y_{ij}) \quad \forall i, j \in J, i \neq j $$
*(Note: This ensures if $y_{ij}=1$ (i before j), then $S_j^A \ge S_i^A + a_i$. If $y_{ij}=0$, the constraint is relaxed by M.)*
Also, $S_j^A \ge 0$.

**Constraint 4: Machine B Precedence (Flow Shop)**
Job $j$ cannot start on Machine B until it is finished on Machine A.
$$ S_j^B \ge S_j^A + a_j \quad \forall j \in J $$

**Constraint 5: Machine B Non-Overlapping**
$$ S_j^B \ge S_i^B + b_i - M(1 - y_{ij}) \quad \forall i, j \in J, i \neq j $$
*(Note: The precedence order on Machine B is the same as Machine A in a standard flow shop. Thus, we use the same binary variables $y_{ij}$.)*

**Constraint 6: Makespan Definition**
The makespan $Z$ is the completion time of the last job on Machine B.
$$ Z \ge S_j^B + b_j \quad \forall j \in J $$

**Bounds:**
$S_j^A, S_j^B \ge 0$
$M$ should be a valid upper bound on total processing time.
$M = \sum_{j \in J} a_j + \sum_{j \in J} b_j = (30+60+60+20+80+90) + (70+70+50+60+30+40) = 340 + 320 = 660$.

---

### Alternative Simpler Formulation (Using Position Variables directly for $n=6$)

Given the small size, we can also formulate this using position variables $x_{jk}$ directly in the objective and constraints, avoiding the pairwise $y_{ij}$ variables if we calculate times carefully. However, the $y_{ij}$ formulation is the standard "disjunctive programming" approach for flow shops.

Let's stick to the **Pairwise Binary Formulation** as it is the most standard OR model for this problem type.

**Refined Model Summary:**

**Sets & Parameters:**
*   $J = \{1,..,6\}$
*   $a_j, b_j$: As defined above.
*   $M = 660$ (Big-M constant)

**Decision Variables:**
*   $y_{ij} \in \{0, 1\}$ for all $i, j \in J, i < j$. ($y_{ij}=1$ if $i$ before $j$).
*   $S_j^A \ge 0$: Continuous, start time of job $j$ on A.
*   $S_j^B \ge 0$: Continuous, start time of job $j$ on B.
*   $Z \ge 0$: Continuous, makespan.

**Objective:**
$$ \text{Minimize } Z $$

**Constraints:**
1.  **Precedence on A:**
    $$ S_j^A \ge S_i^A + a_i - M(1 - y_{ij}) \quad \forall i, j \in J, i < j $$
    $$ S_i^A \ge S_j^A + a_j - M y_{ij} \quad \forall i, j \in J, i < j $$
    *(Note: Using both ensures that if $y_{ij}=1$, first holds; if $y_{ij}=0$, second holds. Actually, just one pair per $i,j$ is needed if we define $y_{ij}$ clearly. Let's use the standard form:)*
    
    For all $i, j \in J, i \neq j$:
    $$ S_j^A \ge S_i^A + a_i - M(1 - z_{ij}) $$
    $$ S_i^A \ge S_j^A + a_j - M z_{ij} $$
    Where $z_{ij} \in \{0,1\}$ and $z_{ij} + z_{ji} = 1$.

2.  **Flow Shop Link (A to B):**
    $$ S_j^B \ge S_j^A + a_j \quad \forall j \in J $$

3.  **Precedence on B:**
    $$ S_j^B \ge S_i^B + b_i - M(1 - z_{ij}) \quad \forall i, j \in J, i \neq j $$
    *(Note: Since it's a flow shop, the sequence is the same on A and B, so we reuse the same sequencing variables $z_{ij}$.)*

4.  **Makespan:**
    $$ Z \ge S_j^B + b_j \quad \forall j \in J $$

5.  **Bounds:**
    $$ S_j^A, S_j^B, Z \ge 0 $$
    $$ z_{ij} \in \{0, 1\} $$
    $$ z_{ij} + z_{ji} = 1 \quad \forall i < j $$

*(Self-Correction: The problem asks for "optimal job sequence". While the variables above model the times, the solution $z_{ij}$ defines the sequence. This is a valid MILP formulation.)*

### Final Answer Structure

**1. Index Sets & Parameters**
*   **Sets:**
    *   $J = \{1, 2, 3, 4, 5, 6\}$: Set of jobs.
    *   $P = \{(i,j) \mid i, j \in J, i < j\}$: Set of job pairs.
*   **Parameters:**
    *   $a_j$: Processing time on Machine A for job $j$ (min).
        *   $a = [30, 60, 60, 20, 80, 90]$
    *   $b_j$: Processing time on Machine B for job $j$ (min).
        *   $b = [70, 70, 50, 60, 30, 40]$
    *   $M$: A large constant (Big-M), set to $\sum a_j + \sum b_j = 660$.

**2. Decision Variables**
*   $z_{ij} \in \{0, 1\}$: Binary variable. $z_{ij} = 1$ if job $i$ is processed before job $j$ on both machines (for all $i, j \in J, i \neq j$).
*   $S_j^A \in \mathbb{R}^+$: Continuous variable. Start time of job $j$ on Machine A.
*   $S_j^B \in \mathbb{R}^+$: Continuous variable. Start time of job $j$ on Machine B.
*   $Z \in \mathbb{R}^+$: Continuous variable. Makespan (total completion time).

**3. Objective Function**
$$ \text{Minimize } Z $$

**4. Operational Constraints**

**(1) Sequencing Constraints (Machine A):**
$$ S_j^A \ge S_i^A + a_i - M(1 - z_{ij}) \quad \forall (i,j) \in J^2, i \neq j $$
$$ S_i^A \ge S_j^A + a_j - M z_{ij} \quad \forall (i,j) \in J^2, i \neq j $$
*(Alternatively, define $z_{ij}$ only for $i<j$ with $z_{ij}+z_{ji}=1$ and use single-direction constraints, but the symmetric form above is more compact in description if $z_{ij}$ is defined for all ordered pairs with $z_{ij}=1 \iff i$ before $j$.)*

*Refined for clarity in output:*
Let $z_{ij} \in \{0,1\}$ for all $i < j$. $z_{ij}=1$ if $i$ before $j$.
$$ S_j^A \ge S_i^A + a_i - M(1 - z_{ij}) \quad \forall i < j $$
$$ S_i^A \ge S_j^A + a_j - M z_{ij} \quad \forall i < j $$

**(2) Flow Constraints (A to B):**
$$ S_j^B \ge S_j^A + a_j \quad \forall j \in J $$

**(3) Sequencing Constraints (Machine B):**
$$ S_j^B \ge S_i^B + b_i - M(1 - z_{ij}) \quad \forall i < j $$
$$ S_i^B \ge S_j^B + b_j - M z_{ij} \quad \forall i < j $$

**(4) Makespan Definition:**
$$ Z \ge S_j^B + b_j \quad \forall j \in J $$

**(5) Variable Bounds:**
$$ S_j^A \ge 0, \quad S_j^B \ge 0, \quad Z \ge 0 \quad \forall j \in J $$
$$ z_{ij} \in \{0, 1\} \quad \forall i < j $$