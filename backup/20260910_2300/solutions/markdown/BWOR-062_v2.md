# Operations Research Model: Sales Outlet Allocation

## 1. Index Sets & Parameters

**Index Sets:**
- $R = \{1, 2, 3\}$: Set of regions.
- $K = \{0, 1, 2, 3, 4\}$: Set of possible numbers of sales outlets to allocate to a single region.

**Parameters:**
- $M = 4$: Total number of sales outlets to be allocated.
- $p_{r,k}$: Monthly profit (in consistent currency units) from allocating $k$ sales outlets to region $r$.

**Profit Data Matrix ($p_{r,k}$):**

| Region ($r$) | $k=0$ | $k=1$ | $k=2$ | $k=3$ | $k=4$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| 1 | 0 | 16 | 25 | 30 | 32 |
| 2 | 0 | 12 | 17 | 21 | 22 |
| 3 | 0 | 10 | 14 | 16 | 17 |

## 2. Decision Variables

We use a **multiple-choice** or **assignment** formulation. Since each region must receive a specific number of outlets, we define binary variables to select the number of outlets assigned to each region.

Let $x_{r,k}$ be a binary decision variable defined as:
$$
x_{r,k} = 
\begin{cases} 
1 & \text{if } k \text{ sales outlets are allocated to region } r \\
0 & \text{otherwise}
\end{cases}
$$
**Domain:**
$$
x_{r,k} \in \{0, 1\} \quad \forall r \in R, \forall k \in K
$$

*Note: This formulation ensures that for each region $r$, exactly one $k$ is selected, satisfying the discrete nature of the problem without requiring linearization of a concave/convex function directly, though the profit table is concave, the binary selection is the most robust standard form for small discrete choices.*

## 3. Objective Function

**Goal:** Maximize the total monthly profit.

$$
\text{Maximize } Z = \sum_{r \in R} \sum_{k \in K} p_{r,k} x_{r,k}
$$

Expanding with the given data:
$$
\text{Maximize } Z = 0x_{1,0} + 16x_{1,1} + 25x_{1,2} + 30x_{1,3} + 32x_{1,4} + 0x_{2,0} + 12x_{2,1} + 17x_{2,2} + 21x_{2,3} + 22x_{2,4} + 0x_{3,0} + 10x_{3,1} + 14x_{3,2} + 16x_{3,3} + 17x_{3,4}
$$

## 4. Operational Constraints

### A. Selection Constraint (One Option Per Region)
Each region must be assigned exactly one number of outlets from the possible choices $\{0, 1, 2, 3, 4\}$.

$$
\sum_{k \in K} x_{r,k} = 1 \quad \forall r \in R
$$

Explicitly:
1.  $x_{1,0} + x_{1,1} + x_{1,2} + x_{1,3} + x_{1,4} = 1$
2.  $x_{2,0} + x_{2,1} + x_{2,2} + x_{2,3} + x_{2,4} = 1$
3.  $x_{3,0} + x_{3,1} + x_{3,2} + x_{3,3} + x_{3,4} = 1$

### B. Resource Constraint (Total Outlets)
The total number of sales outlets allocated across all regions must equal the total available outlets ($M=4$).

$$
\sum_{r \in R} \sum_{k \in K} k \cdot x_{r,k} = 4
$$

Explicitly:
$$
0(x_{1,0} + x_{2,0} + x_{3,0}) + 1(x_{1,1} + x_{2,1} + x_{3,1}) + 2(x_{1,2} + x_{2,2} + x_{3,2}) + 3(x_{1,3} + x_{2,3} + x_{3,3}) + 4(x_{1,4} + x_{2,4} + x_{3,4}) = 4
$$

### C. Integrality Constraints
$$
x_{r,k} \in \{0, 1\} \quad \forall r \in R, \forall k \in K
$$

---

### Solution Analysis (Verification)

To find the maximum profit, we look for combinations of $(k_1, k_2, k_3)$ such that $k_1 + k_2 + k_3 = 4$ and $k_i \in \{0,1,2,3,4\}$ that maximize $p_{1,k_1} + p_{2,k_2} + p_{3,k_3}$.

Let's evaluate the marginal profits (increments) to guide the logic, or simply check high-yield combinations.

Marginal Profits:
-   Region 1: +16, +9, +5, +2
-   Region 2: +12, +5, +4, +1
-   Region 3: +10, +4, +2, +1

We need to pick 4 "units" of allocation.
1.  1st unit to R1: Profit 16 (Total 16)
2.  2nd unit to R1: Profit +9 (Total 25)
3.  3rd unit to R1: Profit +5 (Total 30)
    *Current Allocation: R1=3, R2=0, R3=0. Total outlets=3. Profit=30.*
    *Remaining outlet: 1.*
    *Options for 4th outlet:*
    -   Add to R1 (4th): +2 $\rightarrow$ Total Profit 32. (Alloc: 4,0,0)
    -   Add to R2 (1st): +12 $\rightarrow$ Total Profit 42. (Alloc: 3,1,0)
    -   Add to R3 (1st): +10 $\rightarrow$ Total Profit 40. (Alloc: 3,0,1)

    Let's restart the greedy-like check with all possibilities for sum=4:

    Possible integer partitions of 4 into 3 parts:
    -   (4,0,0): $32 + 0 + 0 = 32$
    -   (3,1,0): $30 + 12 + 0 = 42$
    -   (3,0,1): $30 + 0 + 10 = 40$
    -   (2,2,0): $25 + 17 + 0 = 42$
    -   (2,1,1): $25 + 12 + 10 = 47$
    -   (2,0,2): $25 + 0 + 14 = 39$
    -   (1,3,0): $16 + 21 + 0 = 37$
    -   (1,2,1): $16 + 17 + 10 = 43$
    -   (1,1,2): $16 + 12 + 14 = 42$
    -   (0,4,0): $0 + 22 + 0 = 22$
    -   (0,3,1): $0 + 21 + 10 = 31$
    -   (0,2,2): $0 + 17 + 14 = 31$
    -   (1,0,3): $16 + 0 + 16 = 32$
    -   (0,1,3): $0 + 12 + 16 = 28$
    -   (0,0,4): $0 + 0 + 17 = 17$

    The maximum value found is **47**, corresponding to the allocation:
    -   Region 1: 2 outlets
    -   Region 2: 1 outlet
    -   Region 3: 1 outlet

    Check: $2 + 1 + 1 = 4$ outlets.
    Profit: $25 (R1) + 12 (R2) + 10 (R3) = 47$.

**Final Answer:**
The company should allocate **2 outlets to Region 1**, **1 outlet to Region 2**, and **1 outlet to Region 3**.
The maximum total monthly profit is **47**.