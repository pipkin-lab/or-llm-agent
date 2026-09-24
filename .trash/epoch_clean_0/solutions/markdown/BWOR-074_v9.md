## Model Type Declaration
**Model Type:** MILP (Mixed Integer Linear Programming)
*Note: While the core logic is a deterministic sequencing problem, it is formulated as a MILP to explicitly handle the discrete decision of grade ordering and the cumulative workload calculation. Given the small number of grades (5), this could also be solved via exhaustive enumeration, but the formal OR model below uses binary variables for sequence positions.*

## Index Sets & Parameters

**Index Sets:**
- $G = \{A, B, C, D, E\}$: Set of grades.
- $K = \{1, 2, 3, 4, 5\}$: Set of sorting steps (positions in the sequence), where $k=1$ is the first grade to be scanned/sorted, and $k=5$ is the last.

**Parameters:**
- $N = 50,000$: Total number of answer sheets.
- $p_g$: Percentage distribution of grade $g$.
  - $p_A = 0.10$
  - $p_B = 0.25$
  - $p_C = 0.30$
  - $p_D = 0.20$
  - $p_E = 0.15$
- $n_g$: Absolute count of answer sheets for grade $g$, calculated as $n_g = N \times p_g$.
  - $n_A = 5,000$
  - $n_B = 12,500$
  - $n_C = 15,000$
  - $n_D = 10,000$
  - $n_E = 7,500$

**Derived Parameters:**
- Let $S_k$ be the set of grades remaining to be sorted *before* step $k$. Alternatively, we can define the workload directly based on the cumulative number of sheets processed.
- *Workload Definition*: The problem states the computer sorts by "recognizing one grade at a time". A standard interpretation in such sorting problems (like the "postman problem" or sequential extraction) is that in step $k$, the machine scans the *entire current pool* of unsorted sheets to identify and remove those of the specific grade assigned to step $k$.
  - Workload in step $k$ = Number of sheets present in the pool at the start of step $k$.
  - The pool size decreases as grades are removed.

## Decision Variables

- $x_{g,k} \in \{0, 1\}$: Binary variable, where $x_{g,k} = 1$ if grade $g$ is assigned to sorting step $k$, and $0$ otherwise.
- $W_k \in \mathbb{R}^+$: Continuous variable representing the workload (number of sheets scanned) in step $k$.

## Objective Function

Minimize the total sorting workload:
$$ \text{Minimize } Z = \sum_{k=1}^{5} W_k $$

## Operational Constraints

**1. Assignment Constraints:**
Each grade must be assigned to exactly one step:
$$ \sum_{k=1}^{5} x_{g,k} = 1 \quad \forall g \in G $$

Each step must be assigned exactly one grade:
$$ \sum_{g \in G} x_{g,k} = 1 \quad \forall k \in K $$

**2. Workload Calculation Constraints:**
The workload $W_k$ at step $k$ is the total number of sheets that have *not* been removed in any previous step $j < k$.
Let $R_k$ be the set of grades assigned to steps $j$ such that $j < k$.
The number of sheets remaining at step $k$ is $N - \sum_{g \in R_k} n_g$.

To linearize this, we can express $W_k$ in terms of the binary variables.
$W_k = N - \sum_{j=1}^{k-1} \sum_{g \in G} n_g x_{g,j}$

Let's expand this for clarity in the model:
For $k=1$: $W_1 = N$ (All sheets are present initially)
For $k=2$: $W_2 = N - \sum_{g \in G} n_g x_{g,1}$
For $k=3$: $W_3 = N - \sum_{g \in G} n_g x_{g,1} - \sum_{g \in G} n_g x_{g,2}$
...
For $k=5$: $W_5 = N - \sum_{j=1}^{4} \sum_{g \in G} n_g x_{g,j}$

Substituting $W_k$ into the objective function:
$$ \text{Minimize } Z = W_1 + W_2 + W_3 + W_4 + W_5 $$
$$ Z = 5N - 4\sum_{g} n_g x_{g,1} - 3\sum_{g} n_g x_{g,2} - 2\sum_{g} n_g x_{g,3} - 1\sum_{g} n_g x_{g,4} - 0\sum_{g} n_g x_{g,5} $$

Since $5N$ is a constant, minimizing $Z$ is equivalent to minimizing:
$$ \sum_{k=1}^{4} (5-k) \sum_{g \in G} n_g x_{g,k} $$
Or more intuitively, this formulation implies that grades assigned to earlier steps (smaller $k$) contribute more to the total workload of *subsequent* steps. To minimize total workload, we should remove the *largest* groups first? Or smallest?

Let's verify the logic:
If we remove Grade A ($n_A=5,000$) first:
$W_1 = 50,000$
$W_2 = 45,000$
...
If we remove Grade C ($n_C=15,000$) first:
$W_1 = 50,000$
$W_2 = 35,000$
...
Clearly, removing larger groups *early* reduces the workload for all subsequent steps more significantly. Therefore, the optimal strategy is to sort grades in **descending order of their counts** (Largest First).

Let's double check the objective function derivation:
$Z = \sum_{k=1}^5 W_k$.
$W_k$ is the size of the pile at step $k$.
Total Work = Sum of pile sizes.
To minimize the sum of pile sizes, we want the pile to shrink as fast as possible. This means we must remove the largest quantities first.

The linear objective function to minimize is:
$$ \text{Minimize } \sum_{k=1}^{5} \sum_{j=k}^{5} \left( N - \sum_{m=1}^{k-1} \sum_{g \in G} n_g x_{g,m} \right) $$
Simplifying the coefficients for $x_{g,k}$ in the final objective:
The term $x_{g,k}$ (removing grade $g$ at step $k$) reduces the workload for steps $k+1, k+2, \dots, 5$.
Specifically, if grade $g$ is removed at step $k$, it is present in steps $1, \dots, k$. It is *absent* from steps $k+1, \dots, 5$.
Wait, let's look at the contribution of a specific grade $g$ to the total workload $Z$.
If grade $g$ is placed at step $k$:
- In steps $1, \dots, k$, the sheets of grade $g$ are in the pile. So they contribute $n_g$ to $W_1, W_2, \dots, W_k$.
- In steps $k+1, \dots, 5$, the sheets of grade $g$ are removed. They contribute 0 to $W_{k+1}, \dots, W_5$.
So, if $x_{g,k}=1$, the contribution of grade $g$ to the total sum $Z$ is $k \cdot n_g$.

Therefore, the objective function simplifies to:
$$ \text{Minimize } Z = \sum_{g \in G} \sum_{k=1}^{5} k \cdot n_g x_{g,k} + C_0 $$
Where $C_0$ is a constant (actually, the base workload without any removals would be $5N$, but since every grade is removed exactly once, the "base" isn't quite $5N$ in a simple additive sense unless we view it as "time spent in the queue").
Let's re-verify:
$Z = \sum_{k=1}^5 W_k$.
$W_k = \sum_{h=k}^5 (\text{Sheets removed at step } h) + (\text{Sheets removed at steps } < k \text{? No, those are gone})$.
Actually, $W_k = \sum_{j=k}^5 \sum_{g \in G} n_g x_{g,j}$.
(The pile at step $k$ consists of all grades assigned to step $k, k+1, \dots, 5$).

Substitute this into $Z$:
$$ Z = \sum_{k=1}^5 \sum_{j=k}^5 \sum_{g \in G} n_g x_{g,j} $$
Swap summations. For a fixed $g$ and $j$ (grade $g$ at step $j$), how many times does the term $n_g x_{g,j}$ appear in the sum?
It appears for all $k$ such that $k \le j$.
Since $k$ runs from $1$ to $5$, and the inner sum is over $j$ from $k$ to $5$, the term for a specific $j$ is included in the outer sum for $k=1, 2, \dots, j$.
So it appears $j$ times.

Thus:
$$ Z = \sum_{g \in G} \sum_{j=1}^{5} j \cdot n_g x_{g,j} $$

**Final Objective Function:**
$$ \text{Minimize } \sum_{g \in G} \sum_{k=1}^{5} k \cdot n_g \cdot x_{g,k} $$

**3. Domain Constraints:**
$$ x_{g,k} \in \{0, 1\} \quad \forall g \in G, k \in K $$

## Feasibility Sanity Check

- **Total Supply/Demand:** The assignment constraints ensure a permutation of the 5 grades is selected.
- **Bounds:** $x_{g,k}$ are binary.
- **Logic:** The objective function $\sum k \cdot n_g x_{g,k}$ assigns a "cost" of $k \cdot n_g$ to placing grade $g$ at position $k$. Since $n_g$ is fixed for each grade, to minimize the sum, we must assign the smallest $k$ (earliest position) to the largest $n_g$, and the largest $k$ (latest position) to the smallest $n_g$.
  - $n_C = 15,000$ (Largest) $\rightarrow$ Assign to $k=1$. Cost: $1 \times 15,000 = 15,000$.
  - $n_B = 12,500$ $\rightarrow$ Assign to $k=2$. Cost: $2 \times 12,500 = 25,000$.
  - $n_D = 10,000$ $\rightarrow$ Assign to $k=3$. Cost: $3 \times 10,000 = 30,000$.
  - $n_E = 7,500$ $\rightarrow$ Assign to $k=4$. Cost: $4 \times 7,500 = 30,000$.
  - $n_A = 5,000$ (Smallest) $\rightarrow$ Assign to $k=5$. Cost: $5 \times 5,000 = 25,000$.
  
  Total Objective Value (proportional to workload): $15,000 + 25,000 + 30,000 + 30,000 + 25,000 = 125,000$.
  
  Let's check the actual workload sum for this order (C, B, D, E, A):
  - Step 1 (C): Pile = 50,000. Workload = 50,000.
  - Step 2 (B): Pile = 50,000 - 15,000 = 35,000. Workload = 35,000.
  - Step 3 (D): Pile = 35,000 - 12,500 = 22,500. Workload = 22,500.
  - Step 4 (E): Pile = 22,500 - 10,000 = 12,500. Workload = 12,500.
  - Step 5 (A): Pile = 12,500 - 7,500 = 5,000. Workload = 5,000.
  - Total Workload = $50,000 + 35,000 + 22,500 + 12,500 + 5,000 = 125,000$.
  
  The math holds. The model is feasible and consistent.

## Final Model Summary

**Model Type:** MILP

**Parameters:**
- $n_A=5000, n_B=12500, n_C=15000, n_D=10000, n_E=7500$.

**Variables:**
- $x_{g,k} \in \{0,1\}$ for $g \in \{A,B,C,D,E\}, k \in \{1,2,3,4,5\}$.

**Objective:**
$$ \text{Minimize } 1 \cdot n_A x_{A,1} + 1 \cdot n_B x_{B,1} + 1 \cdot n_C x_{C,1} + 1 \cdot n_D x_{D,1} + 1 \cdot n_E x_{E,1} + \dots + 5 \cdot n_A x_{A,5} + \dots + 5 \cdot n_E x_{E,5} $$
*(Expanded form: Minimize $\sum_{k=1}^5 k \sum_{g \in G} n_g x_{g,k}$)*

**Constraints:**
1. $\sum_{k=1}^5 x_{g,k} = 1 \quad \forall g \in \{A,B,C,D,E\}$
2. $\sum_{g \in \{A,B,C,D,E\}} x_{g,k} = 1 \quad \forall k \in \{1,2,3,4,5\}$
3. $x_{g,k} \in \{0,1\} \quad \forall g, k$