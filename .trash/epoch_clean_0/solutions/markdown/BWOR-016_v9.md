### 1. Index Sets & Parameters

**Index Sets:**
*   $I = \{A_1, A_2, A_3, A_4\}$: Set of all potential factories (sources).
*   $J = \{B_1, B_2, B_3, B_4\}$: Set of demand locations (destinations).
*   $K = \{A_3, A_4\}$: Set of candidate new factories that may be built.

**Parameters:**
*   $S_i$: Annual production capacity of factory $i$ (kt/year).
    *   $S_{A_1} = 400$, $S_{A_2} = 600$, $S_{A_3} = 200$, $S_{A_4} = 200$.
*   $D_j$: Annual demand at location $j$ (kt/year).
    *   $D_{B_1} = 350$, $D_{B_2} = 400$, $D_{B_3} = 300$, $D_{B_4} = 150$.
    *   Total Demand = 1200 kt.
    *   Total Existing Capacity ($A_1 + A_2$) = 1000 kt.
    *   Total Potential Capacity (if one new factory is built) = 1200 kt.
    *   Note: Total Supply equals Total Demand exactly when one new factory is built.
*   $c_{ij}$: Unit transportation cost from factory $i$ to location $j$ (thousand yuan/kt).
    *   $c_{A_1, B_1}=2, c_{A_1, B_2}=9, c_{A_1, B_3}=3, c_{A_1, B_4}=4$
    *   $c_{A_2, B_1}=8, c_{A_2, B_2}=3, c_{A_2, B_3}=5, c_{A_2, B_4}=7$
    *   $c_{A_3, B_1}=7, c_{A_3, B_2}=6, c_{A_3, B_3}=1, c_{A_3, B_4}=2$
    *   $c_{A_4, B_1}=4, c_{A_4, B_2}=5, c_{A_4, B_3}=2, c_{A_4, B_4}=5$
*   $F_k$: Annual fixed production cost of building factory $k$ (thousand yuan).
    *   $F_{A_3} = 1200$
    *   $F_{A_4} = 1500$
*   $M$: A sufficiently large constant (Big-M). We can set $M = \max(S_i) = 600$ for the capacity constraints.

### 2. Decision Variables

**Binary Variables:**
*   $y_k \in \{0, 1\}$ for each $k \in K$:
    *   $y_k = 1$ if factory $k$ is built.
    *   $y_k = 0$ otherwise.

**Continuous Variables:**
*   $x_{ij} \geq 0$ for all $i \in I, j \in J$:
    *   Amount of material (in kt) shipped from factory $i$ to location $j$.

### 3. Objective Function

Minimize the total annual cost, which consists of transportation costs for all active factories and the fixed production cost of the new factory that is built.

$$
\text{Minimize } Z = \sum_{i \in I} \sum_{j \in J} c_{ij} x_{ij} + \sum_{k \in K} F_k y_k
$$

### 4. Operational Constraints

**1. Demand Satisfaction Constraints:**
The total amount of material received by each demand location $j$ must meet the demand $D_j$.

$$
\sum_{i \in I} x_{ij} = D_j \quad \forall j \in J
$$

**2. Production Capacity Constraints:**
The total amount of material shipped from a factory $i$ cannot exceed its capacity $S_i$.
For existing factories $A_1$ and $A_2$, they are always available. For new factories $A_3$ and $A_4$, they can only ship if they are built. We use a Big-M constraint to link the flow to the binary decision variable.

For $i \in \{A_1, A_2\}$:
$$
\sum_{j \in J} x_{ij} \leq S_i
$$

For $k \in \{A_3, A_4\}$:
$$
\sum_{j \in J} x_{kj} \leq S_k y_k
$$
*(Note: Since $S_k$ is the capacity, if $y_k=0$, the RHS is 0, forcing all $x_{kj}=0$. If $y_k=1$, the RHS is $S_k$, allowing up to full capacity.)*

**3. Factory Selection Constraint:**
Exactly one new factory must be built.

$$
y_{A_3} + y_{A_4} = 1
$$

**4. Non-negativity and Integrality Constraints:**
$$
x_{ij} \geq 0 \quad \forall i \in I, j \in J
$$
$$
y_k \in \{0, 1\} \quad \forall k \in K
$$