To minimize the total sorting workload when sorting items by recognizing one grade at a time, we must determine the optimal sequence in which to extract each grade.

### Problem Analysis

1.  **Process Definition**:
    *   We have a set of answer sheets categorized into 5 grades: $A, B, C, D, E$.
    *   The sorting process involves scanning the remaining unsorted sheets one grade at a time.
    *   If we choose to sort for grade $g$ at step $k$, the computer must scan **all** sheets currently in the "unsorted" pile to identify and remove those belonging to grade $g$.
    *   The "workload" for a step is the number of sheets scanned.
    *   The total workload is the sum of the number of sheets scanned in each step.

2.  **Workload Calculation**:
    *   Let $N_g$ be the number of sheets with grade $g$.
    *   Let the sorting order be a permutation $\pi = (g_1, g_2, g_3, g_4, g_5)$.
    *   **Step 1**: Sort for $g_1$. We scan all $N_{total}$ sheets. Workload $W_1 = N_{total}$.
    *   **Step 2**: Sort for $g_2$. The sheets for $g_1$ have been removed. We scan the remaining $N_{total} - N_{g_1}$ sheets. Workload $W_2 = N_{total} - N_{g_1}$.
    *   **Step 3**: Sort for $g_3$. We scan the remaining $N_{total} - N_{g_1} - N_{g_2}$ sheets. Workload $W_3 = N_{total} - N_{g_1} - N_{g_2}$.
    *   ...
    *   **Step $k$**: Workload $W_k = N_{total} - \sum_{j=1}^{k-1} N_{g_j}$.

    Total Workload $W_{total} = \sum_{k=1}^{5} W_k$.
    
    Substituting the expressions:
    $$ W_{total} = N_{total} + (N_{total} - N_{g_1}) + (N_{total} - N_{g_1} - N_{g_2}) + \dots $$
    
    Rearranging the terms to see which grade appears how many times:
    *   $N_{g_1}$ is subtracted in steps 2, 3, 4, 5 (4 times).
    *   $N_{g_2}$ is subtracted in steps 3, 4, 5 (3 times).
    *   $N_{g_3}$ is subtracted in steps 4, 5 (2 times).
    *   $N_{g_4}$ is subtracted in step 5 (1 time).
    *   $N_{g_5}$ is never subtracted (0 times).
    
    Alternatively, we can view the contribution of each grade to the total workload. A sheet of grade $g_i$ is scanned in step 1, step 2, ..., up to the step *before* it is sorted.
    *   If a grade is sorted **first** ($g_1$), its sheets are scanned in steps 2, 3, 4, 5. (Wait, let's re-evaluate the scan count per item).
    
    Let's trace a single sheet of grade $g_k$ (sorted at position $k$):
    *   It is present in the pile during Step 1 (scanned).
    *   It is present in the pile during Step 2 (scanned).
    *   ...
    *   It is present in the pile during Step $k-1$ (scanned).
    *   In Step $k$, it is identified and removed.
    
    So, a sheet sorted at position $k$ contributes to the workload exactly $k$ times? No, the workload is the *number of sheets scanned*.
    Let's sum the workloads directly:
    $$ W_{total} = \sum_{k=1}^{5} (\text{Total Sheets Remaining before Step } k) $$
    
    Let's expand $W_{total}$:
    $$ W_{total} = N_{total} + (N_{total} - N_{g_1}) + (N_{total} - N_{g_1} - N_{g_2}) + (N_{total} - N_{g_1} - N_{g_2} - N_{g_3}) + (N_{total} - N_{g_1} - N_{g_2} - N_{g_3} - N_{g_4}) $$
    
    Grouping by grade counts $N_{g_i}$:
    *   $N_{total}$ appears 5 times.
    *   $N_{g_1}$ is subtracted 4 times.
    *   $N_{g_2}$ is subtracted 3 times.
    *   $N_{g_3}$ is subtracted 2 times.
    *   $N_{g_4}$ is subtracted 1 time.
    *   $N_{g_5}$ is subtracted 0 times.
    
    So, $W_{total} = 5 N_{total} - (4 N_{g_1} + 3 N_{g_2} + 2 N_{g_3} + 1 N_{g_4})$.
    
    To **minimize** $W_{total}$, we must **maximize** the term $S = 4 N_{g_1} + 3 N_{g_2} + 2 N_{g_3} + 1 N_{g_4}$.
    
    Since the coefficients $4, 3, 2, 1$ are decreasing, to maximize the sum, we should assign the **largest** $N_g$ to the **largest** coefficient.
    
    Therefore, the grade with the highest count should be sorted **first**, the second highest **second**, and so on.
    
    Let's verify this logic intuitively:
    *   If we sort a large group first, we remove many items early, reducing the pile size for all subsequent steps.
    *   If we sort a small group first, we remove few items, leaving a large pile for subsequent steps, which is inefficient.
    *   Thus, **Descending Order of Frequency** minimizes the total workload.

3.  **Data Extraction**:
    *   Total Participants $N = 50,000$.
    *   Grade A: 10% $\rightarrow N_A = 5,000$
    *   Grade B: 25% $\rightarrow N_B = 12,500$
    *   Grade C: 30% $\rightarrow N_C = 15,000$
    *   Grade D: 20% $\rightarrow N_D = 10,000$
    *   Grade E: 15% $\rightarrow N_E = 7,500$

4.  **Determining the Order**:
    Sort the grades by their counts in descending order:
    1.  **C** (15,000) - Largest
    2.  **B** (12,500)
    3.  **D** (10,000)
    4.  **E** (7,500)
    5.  **A** (5,000) - Smallest

    The optimal sorting order is **C, B, D, E, A**.

5.  **Mathematical Formulation**:
    Although this specific problem has a greedy solution (sort by descending frequency), it can be formally modeled as an Assignment/Permutation problem.

### Formal Mathematical Model

#### 1. Index Sets & Parameters
*   **Set of Grades**: $G = \{A, B, C, D, E\}$, with $|G| = 5$.
*   **Set of Positions**: $P = \{1, 2, 3, 4, 5\}$, where position $p$ indicates the $p$-th step in the sorting sequence.
*   **Parameter $N_g$**: The number of answer sheets for grade $g \in G$.
    *   $N_A = 5,000$
    *   $N_B = 12,500$
    *   $N_C = 15,000$
    *   $N_D = 10,000$
    *   $N_E = 7,500$
*   **Parameter $N_{total}$**: Total number of sheets, $\sum_{g \in G} N_g = 50,000$.
*   **Parameter $w_p$**: The weight (number of times a sheet sorted at position $p$ contributes to the workload).
    *   A sheet sorted at position $p$ is scanned in steps $1, 2, \dots, p$.
    *   Wait, let's re-verify the contribution.
        *   Step 1 scans all.
        *   Step 2 scans all except those removed in Step 1.
        *   ...
        *   A sheet removed in Step $p$ is present in steps $1, \dots, p$.
        *   So it is scanned $p$ times.
    *   Therefore, if grade $g$ is assigned to position $p$, its contribution to total workload is $p \cdot N_g$.
    *   Total Workload $W = \sum_{p=1}^{5} \sum_{g \in G} x_{g,p} \cdot p \cdot N_g$.
    *   To minimize $W$, we must minimize $\sum_{g \in G} p_g N_g$, where $p_g$ is the position assigned to grade $g$.
    *   This is equivalent to minimizing the dot product of the sorted counts and sorted positions. By the Rearrangement Inequality, the minimum is achieved when the sequence of $N_g$ is sorted in **descending** order and the sequence of positions $p$ is sorted in **ascending** order (1, 2, 3, 4, 5).
    *   Wait, let's double check the previous derivation.
        *   Previous derivation: $W_{total} = 5 N_{total} - (4 N_{g_1} + 3 N_{g_2} + 2 N_{g_3} + 1 N_{g_4})$.
        *   This implies minimizing $W_{total}$ is equivalent to maximizing $4 N_{g_1} + 3 N_{g_2} + 2 N_{g_3} + 1 N_{g_4}$.
        *   This means the grade at position 1 ($g_1$) gets coefficient 4 in the "maximization" part, or effectively, it is "removed" from the count of items scanned in subsequent steps.
        *   Let's check the contribution method: $W = \sum p_g N_g$.
            *   If $g_1$ is at pos 1, it contributes $1 \cdot N_{g_1}$.
            *   If $g_2$ is at pos 2, it contributes $2 \cdot N_{g_2}$.
            *   ...
            *   If $g_5$ is at pos 5, it contributes $5 \cdot N_{g_5}$.
            *   Total $W = 1 N_{g_1} + 2 N_{g_2} + 3 N_{g_3} + 4 N_{g_4} + 5 N_{g_5}$.
        *   Let's check consistency with the subtraction method.
            *   $W_{total} = 5 N_{total} - (4 N_{g_1} + 3 N_{g_2} + 2 N_{g_3} + 1 N_{g_4})$.
            *   $5 N_{total} = 5(N_{g_1} + N_{g_2} + N_{g_3} + N_{g_4} + N_{g_5}) = 5 N_{g_1} + 5 N_{g_2} + 5 N_{g_3} + 5 N_{g_4} + 5 N_{g_5}$.
            *   Subtracting the term:
                *   $N_{g_1}: 5 - 4 = 1$.
                *   $N_{g_2}: 5 - 3 = 2$.
                *   $N_{g_3}: 5 - 2 = 3$.
                *   $N_{g_4}: 5 - 1 = 4$.
                *   $N_{g_5}: 5 - 0 = 5$.
            *   Result: $1 N_{g_1} + 2 N_{g_2} + 3 N_{g_3} + 4 N_{g_4} + 5 N_{g_5}$.
            *   Both methods yield the same objective function.

    *   **Objective**: Minimize $Z = \sum_{p=1}^{5} p \cdot N_{g_p}$, where $g_p$ is the grade assigned to position $p$.
    *   To minimize this sum, we must assign the **smallest** position index $p$ to the **largest** $N_g$.
        *   Position 1 (lowest multiplier 1) $\leftarrow$ Largest $N_g$ (Grade C).
        *   Position 2 (multiplier 2) $\leftarrow$ 2nd Largest $N_g$ (Grade B).
        *   Position 3 (multiplier 3) $\leftarrow$ 3rd Largest $N_g$ (Grade D).
        *   Position 4 (multiplier 4) $\leftarrow$ 4th Largest $N_g$ (Grade E).
        *   Position 5 (multiplier 5) $\leftarrow$ Smallest $N_g$ (Grade A).

#### 2. Decision Variables
Let $x_{g,p}$ be a binary variable:
$$ x_{g,p} = \begin{cases} 1 & \text{if grade } g \text{ is sorted at position } p \\ 0 & \text{otherwise} \end{cases} $$
for all $g \in G, p \in P$.

#### 3. Objective Function
Minimize the total workload $Z$:
$$ \text{Minimize } Z = \sum_{g \in G} \sum_{p \in P} x_{g,p} \cdot p \cdot N_g $$

#### 4. Operational Constraints
1.  **Each grade is assigned to exactly one position**:
    $$ \sum_{p \in P} x_{g,p} = 1 \quad \forall g \in G $$
2.  **Each position is assigned exactly one grade**:
    $$ \sum_{g \in G} x_{g,p} = 1 \quad \forall p \in P $$
3.  **Binary constraints**:
    $$ x_{g,p} \in \{0, 1\} \quad \forall g \in G, p \in P $$

### Solution Calculation

Based on the model, we assign grades to positions to minimize $Z$.
Counts:
$N_C = 15,000$
$N_B = 12,500$
$N_D = 10,000$
$N_E = 7,500$
$N_A = 5,000$

Optimal Assignment:
*   Pos 1: Grade C ($N_C$)
*   Pos 2: Grade B ($N_B$)
*   Pos 3: Grade D ($N_D$)
*   Pos 4: Grade E ($N_E$)
*   Pos 5: Grade A ($N_A$)

The order is **C, B, D, E, A**.

Let's calculate the minimum workload for verification:
$Z = 1(15,000) + 2(12,500) + 3(10,000) + 4(7,500) + 5(5,000)$
$Z = 15,000 + 25,000 + 30,000 + 30,000 + 25,000$
$Z = 125,000$

If we used the reverse order (A, E, D, B, C):
$Z' = 1(5,000) + 2(7,500) + 3(10,000) + 4(12,500) + 5(15,000)$
$Z' = 5,000 + 15,000 + 30,000 + 50,000 + 75,000 = 175,000$
$175,000 > 125,000$, confirming the descending frequency order is optimal.

### Final Answer

**Index Sets & Parameters**
*   $G = \{A, B, C, D, E\}$: Set of grades.
*   $P = \{1, 2, 3, 4, 5\}$: Set of sorting positions (steps).
*   $N_g$: Number of sheets for grade $g$.
    *   $N_A = 5,000$
    *   $N_B = 12,500$
    *   $N_C = 15,000$
    *   $N_D = 10,000$
    *   $N_E = 7,500$

**Decision Variables**
*   $x_{g,p} \in \{0, 1\}$: Equals 1 if grade $g$ is sorted at position $p$, 0 otherwise.

**Objective Function**
$$ \text{Minimize } Z = \sum_{g \in G} \sum_{p \in P} p \cdot N_g \cdot x_{g,p} $$

**Operational Constraints**
1.  $\sum_{p=1}^{5} x_{g,p} = 1 \quad \forall g \in G$
2.  $\sum_{g \in G} x_{g,p} = 1 \quad \forall p \in P$
3.  $x_{g,p} \in \{0, 1\} \quad \forall g \in G, p \in P$

**Optimal Sorting Order**
To minimize the workload, grades should be sorted in **descending order of their frequency**:
1.  **C** (15,000 sheets)
2.  **B** (12,500 sheets)
3.  **D** (10,000 sheets)
4.  **E** (7,500 sheets)
5.  **A** (5,000 sheets)

**Order: C, B, D, E, A**