To solve this problem, we must model it as a **Minimum Spanning Tree (MST)** problem. The goal is to connect all 8 offshore oil wells to the coast (via Well 1) using the minimum total pipeline length. Since pipelines can only branch at well locations, we are finding a tree structure that connects all nodes (the wells) to the root (the coast, connected via Well 1).

### **1. Index Sets & Parameters**

**Index Sets:**
*   $N = \{1, 2, 3, 4, 5, 6, 7, 8\}$: The set of oil wells.
*   $V = \{0, 1, 2, 3, 4, 5, 6, 7, 8\}$: The set of all nodes, where node $0$ represents the Coast.
*   $E = \{(i, j) \mid i, j \in V, i < j\}$: The set of all possible edges (potential pipeline segments).

**Parameters:**
*   $d_{01} = 5$: Distance from the Coast (node 0) to Well 1 (node 1).
*   $c_{ij}$: The distance (length of pipeline) between node $i$ and node $j$.
    *   For $i, j \in N$, $c_{ij}$ is given in Table 8-4.
    *   $c_{01} = 5$.
    *   $c_{0j} = \infty$ for $j \in N, j \neq 1$ (Only Well 1 is connected to the coast directly).
    *   $c_{ij} = c_{ji}$ (Undirected graph).

**Distance Matrix Values ($c_{ij}$ in miles):**
*   $c_{12}=1.3, c_{13}=2.1, c_{14}=0.9, c_{15}=0.7, c_{16}=1.8, c_{17}=2.0, c_{18}=1.5$
*   $c_{23}=0.9, c_{24}=1.8, c_{25}=1.2, c_{26}=2.6, c_{27}=2.3, c_{28}=1.1$
*   $c_{34}=2.6, c_{35}=1.7, c_{36}=2.5, c_{37}=1.9, c_{38}=1.0$
*   $c_{45}=0.7, c_{46}=1.6, c_{47}=1.5, c_{48}=0.9$
*   $c_{56}=0.9, c_{57}=1.1, c_{58}=0.8$
*   $c_{67}=0.6, c_{68}=1.0$
*   $c_{78}=0.5$
*   $c_{01}=5$

### **2. Decision Variables**

*   $x_{ij} \in \{0, 1\}$: Binary variable for each edge $(i, j) \in E$.
    *   $x_{ij} = 1$ if a pipeline is laid between node $i$ and node $j$.
    *   $x_{ij} = 0$ otherwise.

### **3. Objective Function**

**Minimize** the total pipeline length:

$$
\text{Minimize } Z = \sum_{(i,j) \in E, i < j} c_{ij} x_{ij}
$$

### **4. Operational Constraints**

To ensure the solution forms a valid tree connecting the Coast (node 0) to all wells (nodes 1-8) without cycles, we use the **Miller-Tucker-Zemlin (MTZ)** formulation or a **Subtour Elimination** constraint. Given the small size ($N=9$), MTZ is efficient and standard for MST.

Let $u_i$ be an auxiliary continuous variable for each node $i \in N$ (well nodes), representing the "rank" or position of the node in the tree rooted at the Coast.
*   $u_0 = 0$ (Root at Coast).
*   $u_i \in [1, N]$ for $i \in N$.

**Constraints:**

1.  **Flow/Tree Connectivity (MTZ Constraints):**
    To prevent subtours (cycles) and ensure connectivity to the root, we enforce a potential difference across edges. For a tree with $N$ nodes, the rank difference between connected nodes must be bounded.
    
    For all $i, j \in V$ where $i \neq j$ and $x_{ij}$ is a decision variable:
    $$
    u_i - u_j + N \cdot x_{ij} \leq N - 1
    $$
    *Wait, standard MTZ for MST directed from root:*
    It is often clearer to define the constraint as: if $x_{ij}=1$ (edge exists), the "level" must increase by at least 1.
    Let's use the standard subtour elimination for a rooted tree:
    For all subsets $S \subset N$ (the well nodes), $\sum_{i \in S, j \notin S} x_{ij} \geq 1$. This ensures no isolated subtours of wells. However, enumerating all subsets is exponential.
    
    A more compact LP relaxation formulation using node potentials $u_i$ for $i \in \{1, ..., 8\}$:
    $$
    u_i - u_j + 9 \cdot x_{ij} \leq 8 \quad \forall i, j \in \{0, ..., 8\}, i \neq j
    $$
    Where we fix $u_0 = 0$ and $1 \leq u_i \leq 8$ for $i \in \{1, ..., 8\}$.
    *Note:* In practice, for a small graph like this, the **Subtour Elimination Constraint** (SEC) is the most rigorous integer programming constraint.
    
    **SEC Formulation:**
    For every non-empty proper subset $S$ of the well nodes $N$ (i.e., $S \subset N, S \neq \emptyset$):
    $$
    \sum_{i \in S, j \in V \setminus S} x_{ij} \geq 1
    $$
    This ensures that every group of wells is connected to the rest of the network (and ultimately to the Coast).
    
    *Alternative Simple Constraint for Small N:*
    Since we just need to connect 8 wells to the root, and the graph is complete (plus the coast link), we can also simply state that the number of selected edges must be exactly $|V| - 1 = 8$ to form a tree, combined with the SECs.
    
    $$
    \sum_{(i,j) \in E} x_{ij} = 8
    $$
    
    And for every subset $S \subset \{1,2,3,4,5,6,7,8\}$ such that $S \neq \emptyset$:
    $$
    \sum_{i \in S, j \notin S} x_{ij} \geq 1
    $$
    *(Note: In implementation, these SECs are added iteratively or all subsets are generated for such a small N).*

2.  **Domain Constraints:**
    $$
    x_{ij} \in \{0, 1\} \quad \forall (i,j) \in E
    $$

---

### **Solution Derivation (Step-by-Step)**

Since the problem asks "how should pipelines be laid," providing the specific edges is part of the analysis. We can solve this manually using **Prim's Algorithm** starting from the Coast (Node 0) or Well 1 (since only Well 1 connects to Coast, the MST must include edge (0,1)).

**Step 1:** Start with Node 0 (Coast).
*   Connect to Well 1. Cost: $c_{01} = 5$.
*   **Selected Edges:** $\{(0, 1)\}$
*   **Tree Nodes:** $\{0, 1\}$

**Step 2:** Find the cheapest edge connecting $\{0, 1\}$ to $\{2, 3, 4, 5, 6, 7, 8\}$.
*   Edges from 1:
    *   $c_{12} = 1.3$
    *   $c_{13} = 2.1$
    *   $c_{14} = 0.9$
    *   $c_{15} = 0.7$  <-- Minimum
    *   $c_{16} = 1.8$
    *   $c_{17} = 2.0$
    *   $c_{18} = 1.5$
*   Select edge **(1, 5)**. Cost: $0.7$.
*   **Selected Edges:** $\{(0, 1), (1, 5)\}$
*   **Tree Nodes:** $\{0, 1, 5\}$

**Step 3:** Find the cheapest edge connecting $\{0, 1, 5\}$ to the rest.
*   Edges from 1: (1,2)=1.3, (1,3)=2.1, (1,4)=0.9, (1,6)=1.8, (1,7)=2.0, (1,8)=1.5
*   Edges from 5:
    *   $c_{52} = 1.2$
    *   $c_{53} = 1.7$
    *   $c_{54} = 0.7$
    *   $c_{56} = 0.9$
    *   $c_{57} = 1.1$
    *   $c_{58} = 0.8$
*   Candidates: 1.3, 2.1, 0.9, 1.8, 2.0, 1.5, 1.2, 1.7, **0.7** (1,4), 0.9, 1.1, 0.8.
*   Minimum is $c_{14} = 0.9$ and $c_{54} = 0.7$.
*   Select edge **(5, 4)**. Cost: $0.7$.
*   **Selected Edges:** $\{(0, 1), (1, 5), (5, 4)\}$
*   **Tree Nodes:** $\{0, 1, 4, 5\}$

**Step 4:** Find the cheapest edge connecting $\{0, 1, 4, 5\}$ to the rest $\{2, 3, 6, 7, 8\}$.
*   Edges from 1: (1,2)=1.3, (1,3)=2.1, (1,6)=1.8, (1,7)=2.0, (1,8)=1.5
*   Edges from 5: (5,2)=1.2, (5,3)=1.7, (5,6)=0.9, (5,7)=1.1, (5,8)=0.8
*   Edges from 4:
    *   $c_{42} = 1.8$
    *   $c_{43} = 2.6$
    *   $c_{46} = 1.6$
    *   $c_{47} = 1.5$
    *   $c_{48} = 0.9$
*   Candidates: 1.3, 2.1, 1.8, 2.0, 1.5, 1.2, 1.7, 0.9, 1.1, 0.8, 1.8, 2.6, 1.6, 1.5, 0.9.
*   Minimum is $c_{58} = 0.8$.
*   Select edge **(5, 8)**. Cost: $0.8$.
*   **Selected Edges:** $\{(0, 1), (1, 5), (5, 4), (5, 8)\}$
*   **Tree Nodes:** $\{0, 1, 4, 5, 8\}$

**Step 5:** Find the cheapest edge connecting $\{0, 1, 4, 5, 8\}$ to the rest $\{2, 3, 6, 7\}$.
*   Edges from 1: (1,2)=1.3, (1,3)=2.1, (1,6)=1.8, (1,7)=2.0
*   Edges from 5: (5,2)=1.2, (5,3)=1.7, (5,6)=0.9, (5,7)=1.1
*   Edges from 4: (4,2)=1.8, (4,3)=2.6, (4,6)=1.6, (4,7)=1.5
*   Edges from 8:
    *   $c_{82} = 1.1$
    *   $c_{83} = 1.0$
    *   $c_{86} = 1.0$
    *   $c_{87} = 0.5$  <-- Minimum
*   Candidates: 1.3, 2.1, 1.8, 2.0, 1.2, 1.7, 0.9, 1.1, 1.8, 2.6, 1.6, 1.5, 1.1, 1.0, 1.0, **0.5**.
*   Select edge **(8, 7)**. Cost: $0.5$.
*   **Selected Edges:** $\{(0, 1), (1, 5), (5, 4), (5, 8), (8, 7)\}$
*   **Tree Nodes:** $\{0, 1, 4, 5, 7, 8\}$

**Step 6:** Find the cheapest edge connecting $\{0, 1, 4, 5, 7, 8\}$ to the rest $\{2, 3, 6\}$.
*   Edges from 1: (1,2)=1.3, (1,3)=2.1, (1,6)=1.8
*   Edges from 5: (5,2)=1.2, (5,3)=1.7, (5,6)=0.9
*   Edges from 4: (4,2)=1.8, (4,3)=2.6, (4,6)=1.6
*   Edges from 8: (8,2)=1.1, (8,3)=1.0, (8,6)=1.0
*   Edges from 7:
    *   $c_{72} = 2.3$
    *   $c_{73} = 1.9$
    *   $c_{76} = 0.6$  <-- Minimum
*   Candidates: 1.3, 2.1, 1.8, 1.2, 1.7, 0.9, 1.8, 2.6, 1.6, 1.1, 1.0, 1.0, 2.3, 1.9, **0.6**.
*   Select edge **(7, 6)**. Cost: $0.6$.
*   **Selected Edges:** $\{(0, 1), (1, 5), (5, 4), (5, 8), (8, 7), (7, 6)\}$
*   **Tree Nodes:** $\{0, 1, 4, 5, 6, 7, 8\}$

**Step 7:** Find the cheapest edge connecting $\{0, 1, 4, 5, 6, 7, 8\}$ to the last node $\{2, 3\}$.
*   Edges to 2 from existing nodes:
    *   $c_{12} = 1.3$
    *   $c_{52} = 1.2$
    *   $c_{42} = 1.8$
    *   $c_{82} = 1.1$  <-- Min for 2
    *   $c_{72} = 2.3$
    *   $c_{62} = 2.6$
*   Edges to 3 from existing nodes:
    *   $c_{13} = 2.1$
    *   $c_{53} = 1.7$
    *   $c_{43} = 2.6$
    *   $c_{83} = 1.0$  <-- Min for 3
    *   $c_{73} = 1.9$
    *   $c_{63} = 2.5$
*   Global minimum among all candidates is $c_{83} = 1.0$ (connects 3) or $c_{82} = 1.1$ (connects 2).
*   Select edge **(8, 3)**. Cost: $1.0$.
*   **Selected Edges:** $\{(0, 1), (1, 5), (5, 4), (5, 8), (8, 7), (7, 6), (8, 3)\}$
*   **Tree Nodes:** $\{0, 1, 3, 4, 5, 6, 7, 8\}$

**Step 8:** Connect the final node $\{2\}$.
*   Cheapest edge to 2 from existing nodes:
    *   $c_{82} = 1.1$ (Current min from Step 7)
    *   $c_{52} = 1.2$
    *   $c_{12} = 1.3$
*   Select edge **(8, 2)**. Cost: $1.1$.
*   **Selected Edges:** $\{(0, 1), (1, 5), (5, 4), (5, 8), (8, 7), (7, 6), (8, 3), (8, 2)\}$

**Total Length Calculation:**
1.  Coast to 1: 5.0
2.  1 to 5: 0.7
3.  5 to 4: 0.7
4.  5 to 8: 0.8
5.  8 to 7: 0.5
6.  7 to 6: 0.6
7.  8 to 3: 1.0
8.  8 to 2: 1.1

Sum = $5.0 + 0.7 + 0.7 + 0.8 + 0.5 + 0.6 + 1.0 + 1.1 = 11.4$ miles.

### **Final Answer**

**Model Type:** MILP (Minimum Spanning Tree)

**Optimal Pipeline Layout:**
The pipelines should be laid along the following segments:
1.  Coast to Well 1
2.  Well 1 to Well 5
3.  Well 5 to Well 4
4.  Well 5 to Well 8
5.  Well 8 to Well 7
6.  Well 7 to Well 6
7.  Well 8 to Well 3
8.  Well 8 to Well 2

**Minimum Total Pipeline Length:**
$$ 11.4 \text{ miles} $$