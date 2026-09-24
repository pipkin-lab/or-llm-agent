## Model Type Declaration

**MODEL TYPE: MILP (Mixed-Integer Linear Program)**

This is a two-machine flow-shop scheduling problem (12 jobs, machines A then B) requiring a job sequence that minimizes makespan.

## Index Sets & Parameters

**Index Sets:**
- $J = \{1, 2, \ldots, 12\}$: set of jobs
- $M = \{A, B\}$: set of machines (A is first, B is second)
- $P = \{1, 2, \ldots, 12\}$: set of positions in the sequence

**Parameters (Processing Times):**

| Job $j$ | $a_j$ (Machine A) | $b_j$ (Machine B) |
|---------|-------------------|-------------------|
| 1       | 5                 | 5                 |
| 2       | 8                 | 9                 |
| 3       | 11                | 4                 |
| 4       | 2                 | 3                 |
| 5       | 7                 | 7                 |
| 6       | 6                 | 9                 |
| 7       | 3                 | 5                 |
| 8       | 9                 | 4                 |
| 9       | 8                 | 9                 |
| 10      | 3                 | 5                 |
| 11      | 6                 | 3                 |
| 12      | 10                | 4                 |

## Decision Variables

**Binary Assignment Variables:**
- $x_{j,p} \in \{0, 1\}$: 1 if job $j$ is assigned to position $p$ in the sequence, 0 otherwise, for all $j \in J, p \in P$

**Continuous Timing Variables:**
- $S_A(p) \geq 0$: start time of the job at position $p$ on Machine A, for all $p \in P$
- $C_A(p) \geq 0$: completion time of the job at position $p$ on Machine A, for all $p \in P$
- $S_B(p) \geq 0$: start time of the job at position $p$ on Machine B, for all $p \in P$
- $C_B(p) \geq 0$: completion time of the job at position $p$ on Machine B, for all $p \in P$
- $T \geq 0$: makespan (total processing time)

## Objective Function

$$\min \quad T$$

## Operational Constraints

**1. Each job is assigned to exactly one position:**
$$\sum_{p=1}^{12} x_{j,p} = 1 \quad \forall j \in J$$

**2. Each position is assigned exactly one job:**
$$\sum_{j=1}^{12} x_{j,p} = 1 \quad \forall p \in P$$

**3. Machine A processing (sequential, no overlap):**
$$S_A(1) = 0$$
$$C_A(p) = S_A(p) + \sum_{j=1}^{12} a_j \cdot x_{j,p} \quad \forall p \in P$$
$$S_A(p+1) \geq C_A(p) \quad \forall p = 1, \ldots, 11$$

**4. Machine B processing (sequential, no overlap, and flow-shop constraint):**
$$S_B(p) \geq C_A(p) \quad \forall p \in P \quad \text{(job must finish on A before starting on B)}$$
$$S_B(1) \geq C_A(1) \quad \text{(first job on B waits for A)}$$
$$S_B(p+1) \geq C_B(p) \quad \forall p = 1, \ldots, 11 \quad \text{(sequential on B)}$$
$$C_B(p) = S_B(p) + \sum_{j=1}^{12} b_j \cdot x_{j,p} \quad \forall p \in P$$

**5. Makespan definition:**
$$T \geq C_B(p) \quad \forall p \in P$$
Since jobs are processed sequentially on B, the last job completes last:
$$T = C_B(12)$$

## Solution via Johnson's Rule

This is a classic 2-machine flow-shop problem, optimally solvable by Johnson's Rule:

**Step 1: Classify jobs**
- Jobs with $a_j \leq b_j$: {1(5≤5), 2(8≤9), 5(7≤7), 7(3≤5), 9(8≤9), 10(3≤5)}
- Jobs with $a_j > b_j$: {3(11>4), 4(2<3? No, 2≤3 → actually $a_4=2 \leq b_4=3$, so Job 4 is in first set)}

Let me re-classify carefully:
- $a_j \leq b_j$: Job 1(5,5), Job 2(8,9), Job 4(2,3), Job 5(7,7), Job 7(3,5), Job 9(8,9), Job 10(3,5)
- $a_j > b_j$: Job 3(11,4), Job 6(6,9? No, 6≤9), Job 8(9,4), Job 11(6,3), Job 12(10,4)

Re-check: Job 6: a=6, b=9 → $a \leq b$ → first set. Job 8: a=9, b=4 → $a > b$ → second set.

- Set 1 ($a_j \leq b_j$): {1, 2, 4, 5, 6, 7, 9, 10}
- Set 2 ($a_j > b_j$): {3, 8, 11, 12}

**Step 2: Sort Set 1 by increasing $a_j$, Set 2 by decreasing $b_j$**

Set 1 sorted by $a_j$ ascending: Job 4(2), Job 7(3), Job 10(3), Job 1(5), Job 6(6), Job 5(7), Job 2(8), Job 9(8)

Set 2 sorted by $b_j$ descending: Job 3(4), Job 8(4), Job 12(4), Job 11(3)

**Step 3: Final Sequence**

Jobs in order: **4, 7, 10, 1, 6, 5, 2, 9, 3, 8, 12, 11**

**Makespan Calculation:**

| Pos | Job | $a_j$ | $b_j$ | $C_A$ | $S_B$ | $C_B$ |
|-----|-----|-------|-------|-------|-------|-------|
| 1   | 4   | 2     | 3     | 2     | 2     | 5     |
| 2   | 7   | 3     | 5     | 5     | 5     | 10    |
| 3   | 10  | 3     | 5     | 8     | 8     | 13    |
| 4   | 1   | 5     | 5     | 13    | 13    | 18    |
| 5   | 6   | 6     | 9     | 19    | 19    | 28    |
| 6   | 5   | 7     | 7     | 26    | 26    | 33    |
| 7   | 2   | 8     | 9     | 34    | 34    | 43    |
| 8   | 9   | 8     | 9     | 42    | 43    | 52    |
| 9   | 3   | 11    | 4     | 53    | 53    | 57    |
| 10  | 8   | 9     | 4     | 62    | 62    | 66    |
| 11  | 12  | 10    | 4     | 72    | 72    | 76    |
| 12  | 11  | 6     | 3     | 78    | 78    | 81    |

**Optimal Sequence:** 4 → 7 → 10 → 1 → 6 → 5 → 2 → 9 → 3 → 8 → 12 → 11

**Total Makespan: 81 time units**