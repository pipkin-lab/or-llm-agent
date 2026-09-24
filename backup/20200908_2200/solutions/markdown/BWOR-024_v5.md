This is a **Two-Machine Flow Shop Scheduling Problem** ($2||C_{max}$).

**Problem Analysis:**
1.  **Objective:** Minimize the total processing time (Makespan, $C_{max}$).
2.  **Precedence:** Each job $j$ must be processed on Machine A first, then on Machine B.
3.  **Structure:** This is a specific case of the Traveling Salesman Problem (TSP) with a distance matrix derived from the processing times, or more simply, it can be solved using **Johnson's Rule** for optimality. However, the request is for a formal mathematical model (MILP/LP).
4.  **Variables:** Since the number of jobs is small ($n=6$), we can use a binary sequencing variable approach or a position-based assignment approach. A robust MILP formulation for flow shop scheduling typically uses binary variables $x_{jt}$ indicating if job $j$ is scheduled at position $t$, or relative ordering variables. Given $n=6$, an assignment-based model is clean and exact.

**Model Formulation:**

### 1. Index Sets & Parameters

*   **Sets:**
    *   $J = \{1, 2, 3, 4, 5, 6\}$: Set of jobs.
    *   $P = \{1, 2, 3, 4, 5, 6\}$: Set of positions in the sequence.
*   **Parameters:**
    *   $a_j$: Processing time of job $j$ on Machine A (minutes).
        *   $a_1=30, a_2=60, a_3=60, a_4=20, a_5=80, a_6=90$
    *   $b_j$: Processing time of job $j$ on Machine B (minutes).
        *   $b_1=70, b_2=70, b_3=50, b_4=60, b_5=30, b_6=40$

### 2. Decision Variables

*   $x_{jp} \in \{0, 1\}$ for all $j \in J, p \in P$:
    *   $x_{jp} = 1$ if job $j$ is assigned to position $p$ in the sequence.
    *   $x_{jp} = 0$ otherwise.

*   $C_A^p \in \mathbb{R}_+$ for all $p \in P$:
    *   The completion time of the job in position $p$ on Machine A.

*   $C_B^p \in \mathbb{R}_+$ for all $p \in P$:
    *   The completion time of the job in position $p$ on Machine B.

*   $T \in \mathbb{R}_+$:
    *   The total makespan (maximum completion time on Machine B).

### 3. Objective Function

Minimize the total processing time (Makespan):
$$ \min Z = T $$

### 4. Operational Constraints

**A. Assignment Constraints (Each job in exactly one position, each position has exactly one job):**

1.  Each job is assigned to exactly one position:
    $$ \sum_{p \in P} x_{jp} = 1 \quad \forall j \in J $$

2.  Each position is assigned exactly one job:
    $$ \sum_{j \in J} x_{jp} = 1 \quad \forall p \in P $$

**B. Machine A Scheduling Constraints:**
Machine A processes jobs sequentially. The completion time of the job at position $p$ is the completion time of the job at position $p-1$ plus the processing time of the job at position $p$.

3.  For the first position ($p=1$):
    $$ C_A^1 = \sum_{j \in J} a_j x_{j1} $$

4.  For subsequent positions ($p > 1$):
    $$ C_A^p = C_A^{p-1} + \sum_{j \in J} a_j x_{jp} \quad \forall p \in P, p > 1 $$

**C. Machine B Scheduling Constraints:**
Machine B processes jobs sequentially, but a job cannot start on Machine B until it has finished on Machine A.
The start time of job at position $p$ on Machine B is $\max(C_A^p, C_B^{p-1})$.
Thus, the completion time is $\max(C_A^p, C_B^{p-1}) + \text{processing time on B}$.
Since $C_B^p$ is a variable, we must linearize the max function or use the recursive property of the flow shop.
For a flow shop, $C_B^p = \max(C_B^{p-1}, C_A^p) + b_{job\_at\_p}$.
To linearize this in a standard LP/MILP without big-M for the max, we can use the standard recursive definition if we define start times, or use the following equivalent constraint formulation which is standard for $2||C_{max}$:

Let $S_B^p$ be the start time of the job at position $p$ on Machine B.
$S_B^1 = C_A^1$
$S_B^p = \max(S_B^{p-1} + b_{job\_at\_p-1}, C_A^p)$? No, simpler:
$C_B^p = \max(C_B^{p-1}, C_A^p) + \sum_{j \in J} b_j x_{jp}$

To avoid non-linear max, we use the property that for a flow shop, the completion time on the last machine is the objective. We can define $C_B^p$ recursively with linear constraints by observing that:
$C_B^p \ge C_B^{p-1} + \sum_{j \in J} b_j x_{jp}$ (Machine B must finish previous job before starting next)
$C_B^p \ge C_A^p + \sum_{j \in J} b_j x_{jp}$ (Job must finish on A before starting on B)

However, simply using $\ge$ constraints for the objective $T \ge C_B^6$ will result in the solver picking the *minimum* feasible value for $C_B^p$ if we minimize $T$. Wait, if we minimize $T$, and $C_B^p$ are only bounded from below, the solver might set them to 0 unless constrained from above or linked tightly.
Actually, the standard linear formulation for Makespan in a flow shop uses the recursive relation:
$C_B^p = \max(C_B^{p-1}, C_A^p) + b_{p}$
This equality is non-linear.
**Correction:** In a minimization problem where $C_B^p$ represents the actual completion time, we can use the following system of linear inequalities which forces $C_B^p$ to take the minimum possible value consistent with the constraints, provided the objective minimizes the final time.
Actually, a safer standard MILP formulation for small $n$ uses the **preemption-free flow shop** constraints directly:

For $p=1$:
$$ C_B^1 = C_A^1 + \sum_{j \in J} b_j x_{j1} $$

For $p > 1$:
$$ C_B^p \ge C_B^{p-1} + \sum_{j \in J} b_j x_{jp} $$
$$ C_B^p \ge C_A^p + \sum_{j \in J} b_j x_{jp} $$

Because the objective is to minimize $T$ (and $T \ge C_B^6$), and there are no costs associated with delaying jobs unnecessarily (idle time is not penalized directly, but makespan is), the solver will push $C_B^p$ down to the tightest bound imposed by the $\ge$ constraints. *Wait*, this logic holds if there are no other constraints pushing $C_B^p$ up. In a flow shop, the completion time is indeed the earliest possible start time given the sequence. The "earliest possible" is defined by the max of the previous machine's completion and the previous job's completion on the current machine. The inequalities above correctly model that $C_B^p$ *cannot be earlier* than these times. Since we are minimizing the final $T$, and $T$ is coupled to the chain $C_B^6 \ge \dots$, the variables $C_B^p$ will naturally settle at their lower bounds (the actual completion times) because making them larger would only increase $T$.

**D. Objective Linking Constraint:**
5.  The makespan is the completion time of the last job on the last machine:
    $$ T \ge C_B^6 $$
    *(Note: Since we minimize T, $T$ will equal $C_B^6$)*

### Summary of the Model

**Minimize**
$$ Z = T $$

**Subject to:**
1.  $$ \sum_{p=1}^{6} x_{jp} = 1 \quad \forall j \in \{1..6\} $$
2.  $$ \sum_{j=1}^{6} x_{jp} = 1 \quad \forall p \in \{1..6\} $$
3.  $$ C_A^1 = \sum_{j=1}^{6} a_j x_{j1} $$
4.  $$ C_A^p = C_A^{p-1} + \sum_{j=1}^{6} a_j x_{jp} \quad \forall p \in \{2..6\} $$
5.  $$ C_B^1 = C_A^1 + \sum_{j=1}^{6} b_j x_{j1} $$
6.  $$ C_B^p \ge C_B^{p-1} + \sum_{j=1}^{6} b_j x_{jp} \quad \forall p \in \{2..6\} $$
7.  $$ C_B^p \ge C_A^p + \sum_{j=1}^{6} b_j x_{jp} \quad \forall p \in \{2..6\} $$
8.  $$ T \ge C_B^6 $$
9.  $$ x_{jp} \in \{0, 1\} \quad \forall j, p $$
10. $$ C_A^p, C_B^p, T \ge 0 $$

*(Note: For $p=1$, the constraint $C_B^1 \ge C_A^1 + b$ is an equality because there is no previous job on B. For $p>1$, the two inequalities capture the $\max$ function behavior under minimization.)*