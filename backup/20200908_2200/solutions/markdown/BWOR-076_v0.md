### 1. Index Sets & Parameters

**Index Sets:**
*   $T = \{1, 2, 3, 4\}$: The set of years in the planning horizon.
*   $A = \{0, 1, 2, 3, 4\}$: The set of possible ages of the machine (years in service).

**Parameters:**
*   $C_{buy}(t)$: Purchase price of a new machine at the beginning of year $t$ (thousand yuan).
    *   $C_{buy}(1) = 2.5$
    *   $C_{buy}(2) = 2.6$
    *   $C_{buy}(3) = 2.8$
    *   $C_{buy}(4) = 3.1$
*   $S(a)$: Salvage value of a machine after it has been used for $a$ years (thousand yuan).
    *   $S(1) = 2.0$
    *   $S(2) = 1.6$
    *   $S(3) = 1.3$
    *   $S(4) = 1.1$
*   $M(a)$: Annual operating and maintenance cost for a machine of age $a$ (thousand yuan).
    *   $M(1) = 0.3$
    *   $M(2) = 0.8$
    *   $M(3) = 1.5$
    *   $M(4) = 2.0$

### 2. Decision Variables

Let $x_{i,j}$ be a binary decision variable:
$$
x_{i,j} = 
\begin{cases} 
1 & \text{if a new machine is purchased at the beginning of year } i \text{ and sold/replaced at the end of year } j \\
0 & \text{otherwise}
\end{cases}
$$
**Domain:**
*   $x_{i,j} \in \{0, 1\}$ for all $i, j \in T$ such that $1 \le i \le j \le 4$.

*Note: The condition $i \le j$ ensures that a machine is used for at least 1 year ($j-i+1 \ge 1$) and not more than the remaining horizon.*

### 3. Objective Function

The objective is to minimize the total cost, which consists of the purchase price, operating costs, minus the salvage value for each replacement cycle.

For a specific decision $x_{i,j}=1$:
*   Purchase Cost: $C_{buy}(i)$
*   Operating Cost: The machine is used for years $i, i+1, \dots, j$. The age during year $k$ (where $i \le k \le j$) is $k - i + 1$.
    *   Total Operating Cost: $\sum_{k=i}^{j} M(k - i + 1)$
*   Salvage Value: The machine has been used for $j - i + 1$ years.
    *   Salvage Credit: $-S(j - i + 1)$

The total cost for purchasing at $i$ and selling at $j$ is:
$$ \text{Cost}(i, j) = C_{buy}(i) + \sum_{k=i}^{j} M(k - i + 1) - S(j - i + 1) $$

**Minimize:**
$$ Z = \sum_{i=1}^{4} \sum_{j=i}^{4} \text{Cost}(i, j) \cdot x_{i,j} $$

### 4. Operational Constraints

The constraints ensure that the machine schedule is continuous and covers the entire 4-year period without gaps or overlaps.

1.  **Start Constraint:** A machine must be purchased at the beginning of Year 1.
    $$ \sum_{j=1}^{4} x_{1,j} = 1 $$

2.  **Continuity/Linkage Constraints:** For any year $t$ (where $t = 1, 2, 3$), if a machine is sold at the end of year $t$ (meaning it was bought at some $i \le t$ and sold at $j=t$), a new machine must be purchased at the beginning of the next year, $t+1$.
    
    More formally, the set of machines sold at the end of year $t$ must equal the set of machines purchased at the start of year $t+1$.
    
    For $t = 1$:
    $$ \sum_{i=1}^{1} x_{i,1} = \sum_{j=2}^{4} x_{2,j} $$
    *(Machines sold end of Year 1 = Machines bought start of Year 2)*

    For $t = 2$:
    $$ \sum_{i=1}^{2} x_{i,2} = \sum_{j=3}^{4} x_{3,j} $$
    *(Machines sold end of Year 2 = Machines bought start of Year 3)*

    For $t = 3$:
    $$ \sum_{i=1}^{3} x_{i,3} = \sum_{j=4}^{4} x_{4,j} $$
    *(Machines sold end of Year 3 = Machines bought start of Year 4)*

3.  **End Constraint:** A machine must be sold (or its value realized) at the end of the planning horizon (Year 4).
    $$ \sum_{i=1}^{4} x_{i,4} = 1 $$

*(Note: The continuity constraints combined with the start/end constraints ensure a valid partition of the time interval [1,4] into contiguous segments, each corresponding to the lifespan of a single machine.)*