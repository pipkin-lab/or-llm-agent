### 1. Index Sets & Parameters

**Index Sets:**
*   $V$: Set of all nodes in the network.
    *   $V = \{0, 1, 2, 3, 4, 5, 6, 7, 8\}$
    *   Node 0 represents the **Coast**.
    *   Nodes $1, \dots, 8$ represent the **Oil Wells**.
*   $E$: Set of all potential edges (pipeline segments) between nodes.
    *   $E = \{(i, j) \mid i, j \in V, i < j\}$
    *   The edges include connections between the Coast (0) and Well 1, and all pairs of wells.

**Parameters:**
*   $c_{ij}$: Distance (length) of the pipeline segment connecting node $i$ and node $j$ (in miles).
    *   $c_{0,1} = 5$ (Coast to Well 1)
    *   $c_{ij}$ for wells $i, j$ are taken from Table 8-4.
    *   $c_{ij} = c_{ji}$ (Symmetric distances).
    *   $c_{ij} = \infty$ (or a large number $M$) if no direct pipeline is feasible (though in this specific problem, all well-to-well connections are provided, and only Coast-to-Well-1 is the external link).
    *   Specifically:
        *   $c_{1,2}=1.3, c_{1,3}=2.1, c_{1,4}=0.9, c_{1,5}=0.7, c_{1,6}=1.8, c_{1,7}=2.0, c_{1,8}=1.5$
        *   $c_{2,3}=0.9, c_{2,4}=1.8, c_{2,5}=1.2, c_{2,6}=2.6, c_{2,7}=2.3, c_{2,8}=1.1$
        *   $c_{3,4}=2.6, c_{3,5}=1.7, c_{3,6}=2.5, c_{3,7}=1.9, c_{3,8}=1.0$
        *   $c_{4,5}=0.7, c_{4,6}=1.6, c_{4,7}=1.5, c_{4,8}=0.9$
        *   $c_{5,6}=0.9, c_{5,7}=1.1, c_{5,8}=0.8$
        *   $c_{6,7}=0.6, c_{6,8}=1.0$
        *   $c_{7,8}=0.5$
    *   All other $c_{ij}$ (e.g., Coast to Well 2) are effectively $\infty$ as pipelines must start via Well 1.

### 2. Decision Variables

*   $x_{ij} \in \{0, 1\}$: Binary variable for each potential edge $(i, j) \in E$.
    *   $x_{ij} = 1$ if a pipeline is laid between node $i$ and node $j$.
    *   $x_{ij} = 0$ otherwise.

### 3. Objective Function

**Minimize Total Pipeline Length:**

$$
\text{Minimize } Z = \sum_{(i,j) \in E} c_{ij} x_{ij}
$$

### 4. Operational Constraints

**1. Flow Conservation / Connectivity (Steiner Tree / Minimum Spanning Tree Formulation)**

Since the problem requires connecting the Coast to all wells via a tree structure (no cycles, as cycles would add unnecessary length in a minimum spanning tree context), we can model this as a **Minimum Spanning Tree (MST)** problem on the graph $G=(V, E)$, or more rigorously, as a **Steiner Tree** problem where the Coast is the root.

However, since the Coast is only connected to Well 1, and we must connect all wells, this is equivalent to finding the **Minimum Spanning Tree** of the graph containing nodes $\{0, 1, ..., 8\}$ with the constraint that the tree must connect all nodes.

To ensure the selected edges form a tree connecting all $N=9$ nodes (Coast + 8 wells) without cycles and ensuring full connectivity, we use the **Subtour Elimination Constraints** (also known as connectivity constraints for MST).

Let $N = |V| = 9$.
Let $S$ be any proper subset of $V$ such that $S \neq \emptyset$ and $S \neq V$.

**Connectivity Constraints (Cutset Inequalities):**

For every subset $S \subset V$ where $S \neq \emptyset$ and $S \neq V$:

$$
\sum_{i \in S, j \in V \setminus S, i < j} x_{ij} \ge 1
$$

*Note: In practice, for an MST of a small graph (9 nodes), one can also use the **Degree Constraints** combined with **Subtour Elimination** for a specific root, or simply rely on the standard MST property. Since the graph is small, the cutset formulation is robust.*

Alternatively, a more standard integer programming formulation for MST uses **Degree Constraints** and **Subtour Elimination** (similar to TSP but for trees):

1.  **Degree Constraints:**
    For every node $i \in V$:
    $$
    \sum_{j \in V, j \neq i} x_{ij} \le 2 \quad \text{(This is for Hamiltonian Cycle, not MST. For MST, we need a different approach.)}
    $$

    **Correct MST Formulation:**
    To ensure the subgraph is a tree connecting all nodes:
    1.  **Connectivity:** For all $S \subset V, S \neq \emptyset, S \neq V$:
        $$
        \sum_{i \in S, j \in V \setminus S} x_{ij} \ge 1
        $$
    2.  **Acyclicity (Implied by Connectivity + Edge Count):**
        A connected graph with $N$ nodes has exactly $N-1$ edges.
        $$
        \sum_{(i,j) \in E} x_{ij} = |V| - 1 = 8
        $$
        *If the graph is connected and has $N-1$ edges, it is automatically a tree (acyclic).*

**Verification of the Model Logic:**
- We have 9 nodes (Coast + 8 Wells).
- We need to select exactly 8 edges to connect all 9 nodes.
- The cutset constraints ensure that no node or group of nodes is isolated from the rest of the network.
- The edge count constraint ensures no cycles (since a connected graph with $V$ nodes and $V-1$ edges is a tree).

**Simplified Constraints for Implementation:**

1.  **Edge Count Constraint:**
    $$
    \sum_{(i,j) \in E} x_{ij} = 8
    $$

2.  **Cutset Constraints (Subtour Elimination):**
    For all non-empty subsets $S \subset V$ with $S \neq V$:
    $$
    \sum_{i \in S, j \in V \setminus S} x_{ij} \ge 1
    $$
    *(Note: Due to symmetry, we sum over pairs where $i \in S$ and $j \in V \setminus S$. The variable $x_{ij}$ is defined for $i<j$, so in implementation, one must carefully map the pair indices.)*

3.  **Binary Constraints:**
    $$
    x_{ij} \in \{0, 1\} \quad \forall (i,j) \in E
    $$

### Summary of the Model

*   **Type:** Integer Linear Programming (ILP) / Binary Linear Programming (BLP).
*   **Variables:** 36 binary variables (edges among 9 nodes: $9 \times 8 / 2 = 36$).
*   **Objective:** Minimize weighted sum of selected edges.
*   **Constraints:**
    1.  Exactly 8 edges are selected.
    2.  The selected edges form a connected graph (enforced by cutset inequalities).
    3.  Binary nature of decision variables.

This formulation will yield the Minimum Spanning Tree starting from the Coast (via Well 1) that connects all 8 oil wells with minimum total pipeline length.