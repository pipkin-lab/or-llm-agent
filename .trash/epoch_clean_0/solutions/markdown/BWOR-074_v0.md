To minimize the total sorting workload, we must determine the optimal sequence in which to scan for the five grades (A, B, C, D, E).

### 1. Index Sets & Parameters

**Index Sets:**
*   $G = \{A, B, C, D, E\}$: The set of 5 possible grades.
*   $P = \{1, 2, 3, 4, 5\}$: The set of positions (steps) in the sorting sequence. $P$ represents the order in which grades are scanned.

**Parameters:**
*   $N = 50,000$: Total number of participants (answer sheets).
*   $p_g$: The proportion of sheets with grade $g$.
    *   $p_A = 0.10$
    *   $p_B = 0.25$
    *   $p_C = 0.30$
    *   $p_D = 0.20$
    *   $p_E = 0.15$
*   $C_g = N \times p_g$: The absolute count of sheets with grade $g$.
    *   $C_A = 5,000$
    *   $C_B = 12,500$
    *   $C_C = 15,000$
    *   $C_D = 10,000$
    *   $C_E = 7,500$

**Workload Definition:**
The problem states that each scan detects **one specific grade**. When we perform the scan for a specific grade at position $k$ in the sequence, we examine every remaining sheet in the pile.
*   If a sheet matches the target grade, it is removed from the pile (sorted).
*   If a sheet does not match, it remains in the pile for subsequent scans.

Let $x_{g,k}$ be a binary variable indicating if grade $g$ is scanned at position $k$.
Let $W$ be the total workload (total number of individual sheet-inspections performed by the computer).

Consider a sheet with grade $g$.
*   It is inspected during the scan for the first grade in the sequence.
*   It is inspected during the scan for the second grade in the sequence.
*   ...
*   It is inspected during the scan for its own grade $g$. At this point, it is identified and removed.
*   It is **not** inspected in subsequent scans.

Therefore, the number of times a sheet with grade $g$ is inspected is equal to the position $k$ where grade $g$ is scanned.
Total Workload $W = \sum_{g \in G} C_g \times (\text{position of } g)$.

To minimize the total workload $W$, we must assign the grades to positions such that the grades with the **largest counts** ($C_g$) are assigned to the **smallest positions** (scanned first). This is an application of the **Rearrangement Inequality** (or simply the logic that high frequency items should be prioritized to reduce the cumulative count of remaining items in later steps).

### 2. Decision Variables

*   $x_{g,k} \in \{0, 1\}$ for all $g \in G, k \in P$:
    *   $x_{g,k} = 1$ if grade $g$ is scanned at position $k$.
    *   $x_{g,k} = 0$ otherwise.

### 3. Objective Function

Minimize the total number of sheet inspections (workload):

$$
\text{Minimize } Z = \sum_{g \in G} \sum_{k \in P} C_g \cdot k \cdot x_{g,k}
$$

Where:
*   $C_g$ is the count of sheets for grade $g$.
*   $k$ is the position index (1st scan, 2nd scan, etc.).
*   The term $C_g \cdot k$ represents the total inspections contributed by grade $g$ if it is scanned at step $k$.

### 4. Operational Constraints

**1. Each grade is assigned to exactly one position:**
$$
\sum_{k \in P} x_{g,k} = 1 \quad \forall g \in G
$$

**2. Each position is assigned exactly one grade:**
$$
\sum_{g \in G} x_{g,k} = 1 \quad \forall k \in P
$$

**3. Binary Constraints:**
$$
x_{g,k} \in \{0, 1\} \quad \forall g \in G, k \in P
$$

### Solution Derivation (Analytical)

Since this is a linear assignment problem with a specific cost structure (cost is proportional to position index), the optimal solution is obtained by sorting the counts $C_g$ in **descending order** and assigning them to positions $k=1, 2, 3, 4, 5$ in **ascending order**.

**Counts in Descending Order:**
1.  $C_C = 15,000$ (Grade C)
2.  $C_B = 12,500$ (Grade B)
3.  $C_D = 10,000$ (Grade D)
4.  $C_E = 7,500$ (Grade E)
5.  $C_A = 5,000$ (Grade A)

**Optimal Sequence:**
*   Position 1: Grade C
*   Position 2: Grade B
*   Position 3: Grade D
*   Position 4: Grade E
*   Position 5: Grade A

**Order:** **C $\rightarrow$ B $\rightarrow$ D $\rightarrow$ E $\rightarrow$ A**

**Verification of Workload:**
*   Scan 1 (C): Inspect 50,000 sheets. Remove 15,000. Remaining: 35,000.
*   Scan 2 (B): Inspect 35,000 sheets. Remove 12,500. Remaining: 22,500.
*   Scan 3 (D): Inspect 22,500 sheets. Remove 10,000. Remaining: 12,500.
*   Scan 4 (E): Inspect 12,500 sheets. Remove 7,500. Remaining: 5,000.
*   Scan 5 (A): Inspect 5,000 sheets. Remove 5,000. Remaining: 0.

Total Workload = $50,000 + 35,000 + 22,500 + 12,500 + 5,000 = 125,000$ inspections.

If we used the order A, B, C, D, E:
*   Scan 1 (A): 50,000. Rem: 45,000.
*   Scan 2 (B): 45,000. Rem: 32,500.
*   Scan 3 (C): 32,500. Rem: 17,500.
*   Scan 4 (D): 17,500. Rem: 7,500.
*   Scan 5 (E): 7,500. Rem: 0.
Total = $50,000 + 45,000 + 32,500 + 17,500 + 7,500 = 152,500$.

$125,000 < 152,500$, confirming the derived order is optimal.

### Final Answer

The optimal order of sorting to minimize the total sorting workload is:
**C, B, D, E, A**