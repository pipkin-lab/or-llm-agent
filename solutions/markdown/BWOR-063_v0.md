Model Type: MILP (Mixed-Integer Linear Programming)

### Index Sets & Parameters

**Index Sets:**
*   $I = \{1, 2, 3\}$: Set of departments.
*   $X = \{0, 1, 2, 3\}$: Possible integer allocations of Resource 1.
*   $Y = \{0, 1, 2, 3\}$: Possible integer allocations of Resource 2.

**Parameters:**
*   $X_{total} = 3$: Total units of Resource 1.
*   $Y_{total} = 3$: Total units of Resource 2.
*   $P_{i}(x, y)$: Profit for department $i$ given $x$ units of Resource 1 and $y$ units of Resource 2.
    *   **Department 1 ($P_1$):**
        *   $P_1(0,0)=0, P_1(0,1)=1, P_1(0,2)=3, P_1(0,3)=6$
        *   $P_1(1,0)=4, P_1(1,1)=5, P_1(1,2)=6, P_1(1,3)=7$
        *   $P_1(2,0)=5, P_1(2,1)=6, P_1(2,2)=7, P_1(2,3)=8$
        *   $P_1(3,0)=6, P_1(3,1)=7, P_1(3,2)=8, P_1(3,3)=9$
    *   **Department 2 ($P_2$):**
        *   $P_2(0,0)=0, P_2(0,1)=2, P_2(0,2)=4, P_2(0,3)=6$
        *   $P_2(1,0)=1, P_2(1,1)=4, P_2(1,2)=6, P_2(1,3)=7$
        *   $P_2(2,0)=4, P_2(2,1)=6, P_2(2,2)=8, P_2(2,3)=9$
        *   $P_2(3,0)=6, P_2(3,1)=8, P_2(3,2)=10, P_2(3,3)=11$
    *   **Department 3 ($P_3$):**
        *   $P_3(0,0)=0, P_3(0,1)=3, P_3(0,2)=5, P_3(0,3)=8$
        *   $P_3(1,0)=2, P_3(1,1)=5, P_3(1,2)=7, P_3(1,3)=9$
        *   $P_3(2,0)=4, P_3(2,1)=7, P_3(2,2)=9, P_3(2,3)=11$
        *   $P_3(3,0)=6, P_3(3,1)=9, P_3(3,2)=11, P_3(3,3)=13$

### Decision Variables

*   $z_{i,x,y} \in \{0, 1\}$: Binary variable for each department $i \in I$, resource 1 allocation $x \in X$, and resource 2 allocation $y \in Y$.
    *   $z_{i,x,y} = 1$ if department $i$ receives exactly $x$ units of Resource 1 and $y$ units of Resource 2.
    *   $z_{i,x,y} = 0$ otherwise.

### Objective Function

Maximize Total Profit:
$$ \text{Maximize } Z = \sum_{i \in I} \sum_{x \in X} \sum_{y \in Y} P_i(x, y) \cdot z_{i,x,y} $$

### Operational Constraints

1.  **Exclusive Allocation per Department:**
    Each department must receive exactly one specific combination of $(x, y)$ allocations.
    $$ \sum_{x \in X} \sum_{y \in Y} z_{i,x,y} = 1 \quad \forall i \in I $$

2.  **Resource 1 Conservation:**
    The total units of Resource 1 allocated across all departments must equal the total available supply ($3$).
    $$ \sum_{i \in I} \sum_{y \in Y} \sum_{x \in X} x \cdot z_{i,x,y} = 3 $$

3.  **Resource 2 Conservation:**
    The total units of Resource 2 allocated across all departments must equal the total available supply ($3$).
    $$ \sum_{i \in I} \sum_{x \in X} \sum_{y \in Y} y \cdot z_{i,x,y} = 3 $$

4.  **Variable Bounds:**
    $$ z_{i,x,y} \in \{0, 1\} \quad \forall i \in I, x \in X, y \in Y $$