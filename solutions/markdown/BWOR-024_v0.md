## Model Type
**MILP** (Mixed-Integer Linear Programming)

*Note: This is a classic two-machine flow shop scheduling problem ($F2||C_{max}$). While Johnson's Rule provides a polynomial-time heuristic (and exact solution for 2 machines), the general formulation for sequence optimization is an MILP. For $n=6$, the number of possible permutations is $6! = 720$, which is computationally trivial for a MILP solver.*

## Index Sets & Parameters

**Index Sets:**
*   $J = \{1, 2, 3, 4, 5, 6\}$: Set of jobs.
*   $M = \{A, B\}$: Set of machines.
*   $P = \{1, 2, 3, 4, 5, 6\}$: Set of positions in the sequence.

**Parameters (from Table 14-1):**
*   $a_j$: Processing time of job $j$ on machine A (minutes).
    *   $a_1 = 30, a_2 = 60, a_3 = 60, a_4 = 20, a_5 = 80, a_6 = 90$
*   $b_j$: Processing time of job $j$ on machine B (minutes).
    *   $b_1 = 70, b_2 = 70, b_3 = 50, b_4 = 60, b_5 = 30, b_6 = 40$
*   $N = |J| = 6$: Total number of jobs.
*   $T_{max}$: A large constant (Big-M) for linearization.
    *   $T_{max} = \sum_{j \in J} (a_j + b_j) = (30+70) + (60+70) + (60+50) + (20+60) + (80+30) + (90+40) = 100 + 130 + 110 + 80 + 110 + 130 = 660$.

## Decision Variables

1.  **$x_{j,p}$**: Binary variable. Equals 1 if job $j$ is assigned to position $p$ in the sequence, 0 otherwise.
    *   Domain: $x_{j,p} \in \{0, 1\} \quad \forall j \in J, p \in P$
2.  **$s_{j,A}$**: Continuous variable. Start time of job $j$ on machine A.
    *   Domain: $s_{j,A} \ge 0 \quad \forall j \in J$
3.  **$s_{j,B}$**: Continuous variable. Start time of job $j$ on machine B.
    *   Domain: $s_{j,B} \ge 0 \quad \forall j \in J$
4.  **$C_{max}$**: Continuous variable. Makespan (total completion time).
    *   Domain: $C_{max} \ge 0$

## Objective Function

Minimize the total processing time (Makespan):

$$
\text{Minimize } Z = C_{max}
$$

## Operational Constraints

### 1. Assignment Constraints (Each job has exactly one position)
$$
\sum_{p \in P} x_{j,p} = 1 \quad \forall j \in J
$$

### 2. Position Constraints (Each position has exactly one job)
$$
\sum_{j \in J} x_{j,p} = 1 \quad \forall p \in P
$$

### 3. Machine A Precedence (Sequential processing on Machine A)
For any two distinct jobs $j, k$, if job $j$ is scheduled before job $k$ in the sequence, job $j$ must finish on A before job $k$ starts on A. We use the position index to define the order.
Let $p_j$ be the position of job $j$ and $p_k$ be the position of job $k$.
Constraint:
$$
s_{k,A} \ge s_{j,A} + a_j - T_{max} \left( 1 - \sum_{p \in P} p \cdot x_{j,p} + \sum_{p \in P} p \cdot x_{k,p} \right) \quad \forall j, k \in J, j \neq k
$$
*Explanation*: The term $\left( \sum_{p} p \cdot x_{k,p} - \sum_{p} p \cdot x_{j,p} \right)$ is positive if $k$ is after $j$, and negative if $k$ is before $j$. The Big-M formulation ensures the constraint is only active when $k$ is scheduled after $j$ (i.e., pos($k$) > pos($j$)).

*Alternative Simpler Formulation using Start Times directly with sequence variables:*
A more standard and numerically stable approach for small $N$ is to define the start times based on the permutation directly. However, since we don't have a direct "position" variable for each job in the standard assignment, we often use the "disjunctive" constraints:
$$
s_{j,A} \ge s_{k,A} + a_k - T_{max}(1 - y_{j,k})
$$
$$
s_{k,A} \ge s_{j,A} + a_j - T_{max}(y_{j,k})
$$
Where $y_{j,k}$ is a binary variable indicating if $j$ precedes $k$. But linking $y$ to $x$ is complex.

**Recommended Robust Formulation for 2-Machine Flow Shop:**
It is often easier to define the start times on Machine B directly based on the completion on Machine A and the order on Machine B. Since the order is the same on both machines (permutation schedule), we can use the positions $p$.

Let $Pos(j) = \sum_{p \in P} p \cdot x_{j,p}$.

**Start Time on Machine A:**
$$
s_{j,A} = \sum_{k \in J, k \neq j} a_k \cdot \delta_{Pos(k) < Pos(j)}
$$
Since $\delta$ is non-linear, we linearize.
Actually, for a 2-machine flow shop, the completion time of the last job on Machine B is the objective.
$C_{max} = \max_{j \in J} (C_{j,B})$.
$C_{j,B} = s_{j,B} + b_j$.
$s_{j,B} = \max(C_{j,A}, C_{prev(j),B})$.

This max structure is non-linear. We can linearize the recurrence relation for start times using the Big-M method on the sequence.

**Revised Constraints using Big-M on Sequence:**

1.  **Start on A:**
    $$
    s_{j,A} \ge \sum_{k \in J} a_k \cdot \left( \sum_{p \in P} p \cdot x_{k,p} - \sum_{p \in P} p \cdot x_{j,p} + 1 \right) \cdot \mathbb{I}[\dots] \quad \text{(Too complex)}
    $$

    Let's use the standard **Disjunctive Constraints** for the sequence, which is the standard MILP formulation for Flow Shop.
    
    Let $y_{j,k} \in \{0,1\}$ be 1 if job $j$ is processed before job $k$ on **both** machines (which is true for permutation schedules).
    
    **Constraint 1: Precedence on Machine A**
    $$
    s_{k,A} \ge s_{j,A} + a_j - T_{max}(1 - y_{j,k}) \quad \forall j, k \in J, j \neq k
    $$
    $$
    s_{j,A} \ge s_{k,A} + a_k - T_{max}(y_{j,k}) \quad \forall j, k \in J, j \neq k
    $$
    *(Note: $y_{j,k}$ and $y_{k,j}$ are complementary, i.e., $y_{j,k} + y_{k,j} = 1$)*

    **Constraint 2: Precedence on Machine B**
    $$
    s_{k,B} \ge s_{j,B} + b_j - T_{max}(1 - y_{j,k}) \quad \forall j, k \in J, j \neq k
    $$
    $$
    s_{j,B} \ge s_{k,B} + b_k - T_{max}(y_{j,k}) \quad \forall j, k \in J, j \neq k
    $$

    **Constraint 3: Flow Constraint (A to B)**
    Job $j$ cannot start on B until it finishes on A.
    $$
    s_{j,B} \ge s_{j,A} + a_j \quad \forall j \in J
    $$

    **Constraint 4: Objective**
    $$
    C_{max} \ge s_{j,B} + b_j \quad \forall j \in J
    $$

    **Constraint 5: Consistency of Sequence (Permutation Schedule)**
    The variable $y_{j,k}$ defines a total order. For a permutation schedule, the order on A must match the order on B. The disjunctive constraints above enforce this implicitly if we assume a single sequence variable $y$. However, strictly speaking, $y_{j,k}$ just defines an order. To ensure it's a valid permutation (no cycles), we rely on the fact that for 2 machines, an optimal permutation schedule exists. The standard formulation uses $y_{j,k}$ to define the relative order of any pair.
    
    To ensure $y$ represents a valid sequence (acyclic), we typically don't need explicit acyclicity constraints if we are minimizing makespan in a flow shop, as cycles would violate time consistency ($s_{j,A} < s_{k,A}$ and $s_{k,A} < s_{j,A}$ is impossible with positive processing times and the Big-M constraints forcing one direction).
    
    **Bounds:**
    $s_{j,A} \ge 0$
    $s_{j,B} \ge 0$
    $C_{max} \ge 0$
    $y_{j,k} \in \{0,1\}$
    $y_{j,k} + y_{k,j} = 1 \quad \forall j \neq k$