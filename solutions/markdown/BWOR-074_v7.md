To determine the optimal sorting order that minimizes the total workload, we must analyze how the "workload" accumulates as items are removed from the pile one grade at a time.

### 1. Problem Analysis

*   **Total Items ($N$):** 50,000.
*   **Grades:** $G = \{A, B, C, D, E\}$.
*   **Proportions ($p_i$):**
    *   $p_A = 0.10$
    *   $p_B = 0.25$
    *   $p_C = 0.30$
    *   $p_D = 0.20$
    *   $p_E = 0.15$
*   **Process:** The computer scans the *entire remaining pile* to identify and remove all sheets of the currently selected grade.
*   **Workload Definition:** The workload for a single scan is proportional to the number of sheets remaining in the pile at the time of that scan. If we sort grade $i$ at step $k$, the workload $W_k$ is the total number of sheets not yet sorted.
*   **Objective:** Minimize the sum of workloads over all 5 steps.

### 2. Mathematical Formulation

Let the sorting order be a permutation $\pi = (\pi_1, \pi_2, \pi_3, \pi_4, \pi_5)$ of the grades $\{A, B, C, D, E\}$.
Let $n_i$ be the number of sheets of grade $i$.
$n_i = N \times p_i$.

At step $k$, we select grade $\pi_k$. The number of sheets removed is $n_{\pi_k}$.
The number of sheets remaining in the pile *before* the $k$-th scan (which represents the workload for that scan) is:
$$ R_k = \sum_{j=k}^{5} n_{\pi_j} $$
*(Note: This includes the items of the current grade being scanned, as they are present during the scan process. Even if we define workload as items *after* removal, the optimization logic remains identical in structure, just shifted by a constant factor. Standard interpretation for "scanning to find" implies processing the current set.)*

The Total Workload $W$ is:
$$ W = \sum_{k=1}^{5} R_k = \sum_{k=1}^{5} \left( \sum_{j=k}^{5} n_{\pi_j} \right) $$

We can rearrange this summation to see the contribution of each grade $i$. If grade $i$ is placed at position $k$ in the permutation (i.e., $\pi_k = i$), it contributes to the workload of scan $k$, scan $k-1$, ..., scan $1$. Wait, let's look closer.
$R_1$ contains all items.
$R_2$ contains all items except $\pi_1$.
$R_3$ contains all items except $\pi_1, \pi_2$.
...
$R_k$ contains items $\pi_k, \dots, \pi_5$.

So, $n_{\pi_k}$ appears in $R_k, R_{k-1}, \dots, R_1$.
Total occurrences of $n_{\pi_k}$ in the sum $W$ is $k$.

Thus:
$$ W = \sum_{k=1}^{5} k \cdot n_{\pi_k} $$

To **minimize** $W = 1 \cdot n_{\pi_1} + 2 \cdot n_{\pi_2} + 3 \cdot n_{\pi_3} + 4 \cdot n_{\pi_4} + 5 \cdot n_{\pi_5}$:

We must assign the **largest** $n_i$ values to the **smallest** coefficients $k$.
This is an application of the **Rearrangement Inequality** (or simply sorting in descending order of quantity to minimize the weighted sum where weights increase with position).

*   Smallest weight ($k=1$) $\rightarrow$ Largest $n_i$
*   Second smallest weight ($k=2$) $\rightarrow$ Second largest $n_i$
*   ...
*   Largest weight ($k=5$) $\rightarrow$ Smallest $n_i$

Therefore, the optimal strategy is to sort the grades in **descending order of their frequency (quantity)**.

### 3. Calculation

1.  **Calculate Quantities ($n_i$):**
    *   $n_A = 50,000 \times 0.10 = 5,000$
    *   $n_B = 50,000 \times 0.25 = 12,500$
    *   $n_C = 50,000 \times 0.30 = 15,000$
    *   $n_D = 50,000 \times 0.20 = 10,000$
    *   $n_E = 50,000 \times 0.15 = 7,500$

2.  **Rank by Quantity (Descending):**
    1.  $C$ (15,000)
    2.  $B$ (12,500)
    3.  $D$ (10,000)
    4.  $E$ (7,500)
    5.  $A$ (5,000)

3.  **Determine Order:**
    The order should be $C, B, D, E, A$.

### 4. Formal Optimization Model

Although the solution is derived via greedy logic (Rearrangement Inequality), we can formalize it as a Linear Assignment Problem (LAP) or Quadratic Assignment Problem (QAP) if we were to solve it computationally for a general case. Here, the structure is simple enough for direct derivation, but we define the variables for clarity.

**Index Sets:**
*   $G = \{A, B, C, D, E\}$: Set of grades.
*   $K = \{1, 2, 3, 4, 5\}$: Set of sorting steps (positions in the sequence).

**Parameters:**
*   $N = 50,000$: Total number of sheets.
*   $p_g$: Proportion of grade $g$.
    *   $p_A=0.10, p_B=0.25, p_C=0.30, p_D=0.20, p_E=0.15$.
*   $n_g = N \cdot p_g$: Number of sheets for grade $g$.
    *   $n_C=15,000, n_B=12,500, n_D=10,000, n_E=7,500, n_A=5,000$.

**Decision Variables:**
*   $x_{g,k} \in \{0, 1\}$: Equals 1 if grade $g$ is sorted at step $k$, 0 otherwise.

**Objective Function:**
Minimize Total Workload $W$:
$$ \text{Minimize } W = \sum_{g \in G} \sum_{k \in K} k \cdot n_g \cdot x_{g,k} $$

**Constraints:**
1.  Each grade is assigned to exactly one step:
    $$ \sum_{k \in K} x_{g,k} = 1, \quad \forall g \in G $$
2.  Each step is assigned exactly one grade:
    $$ \sum_{g \in G} x_{g,k} = 1, \quad \forall k \in K $$
3.  Binary constraints:
    $$ x_{g,k} \in \{0, 1\}, \quad \forall g \in G, k \in K $$

**Solution Logic:**
To minimize $\sum k \cdot n_g \cdot x_{g,k}$, we pair the largest $n_g$ with the smallest $k$.
*   $k=1$ gets largest $n$ ($C$).
*   $k=2$ gets next largest $n$ ($B$).
*   $k=3$ gets next ($D$).
*   $k=4$ gets next ($E$).
*   $k=5$ gets smallest $n$ ($A$).

### Conclusion

The optimal order of sorting to minimize the total workload is:

**C, B, D, E, A**