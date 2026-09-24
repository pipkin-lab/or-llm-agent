## Mathematical Optimization Model

### Model Type: MILP (Mixed-Integer Linear Programming)

This is a **Steiner Tree Problem** (specifically, a minimum spanning tree with a fixed root node and optional Steiner points). Since the problem states "pipelines are only allowed to branch at the well locations," this simplifies to a **Minimum Spanning Tree (MST)** problem on the complete graph of 8 well-nodes plus the coast node. The coast is a fixed starting point, and we need to connect all 8 wells to the coast via a tree structure.

Let me re-examine: the distance from coast to Well 1 is 5 miles. The distances between wells are given in the table. We need to build a tree connecting the coast (node 0) to all 8 wells (nodes 1–8) using edges with the given distances, minimizing total length. Since branching is only allowed at well locations (and the coast), this is a **Minimum Spanning Tree** on 9 nodes (coast + 8 wells).

Wait — let me reconsider. The problem says "Starting from the coast through Well 1," which means the pipeline starts at the coast, goes to Well 1 (distance = 5 miles), and then connects all other wells. The constraint "pipelines are only allowed to branch at the well locations" means we cannot create intermediate junctions — all connections must be between well locations (or between coast and a well). This is indeed a **Minimum Spanning Tree** problem on the graph with nodes {Coast, 1, 2, 3, 4, 5, 6, 7, 8}.

The only edge from the coast is to Well 1 (distance = 5). All other edges are between wells with distances from the table. Since the coast only connects to Well 1, the MST must include the edge (Coast, 1). The remaining problem is to find the MST of the 8 wells (nodes 1–8) using the distances in Table 8-4, and add the 5-mile coast-to-Well-1 edge.

### Index Sets & Parameters

**Index Sets:**
- $V = \{0, 1, 2, 3, 4, 5, 6, 7, 8\}$: Set of nodes, where node 0 = Coast, nodes 1–8 = oil wells.
- $E = \{(i,j) : i < j,\ i \in V,\ j \in V\}$: Set of candidate edges.

**Parameters:**
- $c_{0,1} = 5.0$ miles: Distance from Coast to Well 1.
- $c_{i,j}$: Distance between Well $i$ and Well $j$ (for $i \neq j$), from Table 8-4:

| From \ To | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|-----------|-----|-----|-----|-----|-----|-----|-----|
| 1 | 1.3 | 2.1 | 0.9 | 0.7 | 1.8 | 2.0 | 1.5 |
| 2 | — | 0.9 | 1.8 | 1.2 | 2.6 | 2.3 | 1.1 |
| 3 | — | — | 2.6 | 1.7 | 2.5 | 1.9 | 1.0 |
| 4 | — | — | — | 0.7 | 1.6 | 1.5 | 0.9 |
| 5 | — | — | — | — | 0.9 | 1.1 | 0.8 |
| 6 | — | — | — | — | — | 0.6 | 1.0 |
| 7 | — | — | — | — | — | — | 0.5 |

All distances are symmetric: $c_{i,j} = c_{j,i}$.

### Decision Variables

- $x_{i,j} \in \{0, 1\}$ for all $(i,j) \in E$: Binary variable where $x_{i,j} = 1$ if the pipeline segment between node $i$ and node $j$ is included in the solution, and $x_{i,j} = 0$ otherwise.

### Objective Function

$$\text{Minimize} \quad Z = \sum_{(i,j) \in E} c_{i,j} \cdot x_{i,j}$$

### Operational Constraints

**1. Connectivity / Tree Structure (Subtour Elimination Constraints):**

To ensure the selected edges form a single tree connecting all 9 nodes (no cycles, all nodes connected), we use the standard subtour elimination constraints. For every subset $S \subseteq V$ with $|S| \geq 2$:

$$\sum_{i \in S,\ j \in V \setminus S} x_{i,j} \geq 1 \quad \forall S \subset V, \ |S| \geq 2$$

This is the cut-based formulation for the MST. However, this involves exponentially many constraints. An equivalent and more compact formulation uses **flow-based (rooted tree)** constraints.

**Alternative: Rooted Tree Formulation (using node 0 = Coast as root):**

Introduce auxiliary variables:
- $y_{i} \in \mathbb{R}_+$: Flow variable representing the number of nodes in the subtree rooted at node $i$ (excluding the root side).

Actually, the cleanest MILP formulation for MST uses the **Miller-Tucker-Zemlin (MTZ)** style or **cutset** formulation. Given the small size (9 nodes), the cutset formulation is appropriate.

**Compact MILP Formulation using Cutset Constraints:**

For every non-empty proper subset $S \subset V$:
$$\sum_{i \in S,\ j \notin S} x_{i,j} \geq 1$$

Since the problem is small (9 nodes, 36 possible edges), this is solvable.

**Simpler Equivalent Formulation (using degree and cycle constraints):**

Given the structure (Coast only connects to Well 1), the edge $(0,1)$ must be in the solution. We can fix $x_{0,1} = 1$ and solve the MST on the 8 well-nodes.

**Final Simplified Model:**

**Fixed:** $x_{0,1} = 1$ (Coast to Well 1 is mandatory and the only coast connection).

For the 8 wells (nodes 1–8), find the MST using the distances in Table 8-4.

**Decision Variables:** $x_{i,j} \in \{0,1\}$ for all $1 \leq i < j \leq 8$.

**Objective:**
$$\text{Minimize} \quad Z = 5.0 + \sum_{1 \leq i < j \leq 8} c_{i,j} \cdot x_{i,j}$$

**Constraints:**

**(a) Spanning Tree on 8 nodes (MST):**

The selected edges among the 8 wells must form a tree (connected, acyclic, spanning all 8 nodes).

Using the **subtour elimination** constraints: For every subset $S \subseteq \{1, 2, \ldots, 8\}$ with $2 \leq |S| \leq 7$:
$$\sum_{i \in S,\ j \in \{1,\ldots,8\} \setminus S} x_{i,j} \geq 1$$

**(b) Number of edges in tree:** A tree on 8 nodes has exactly 7 edges:
$$\sum_{1 \leq i < j \leq 8} x_{i,j} = 7$$

**(c) Non-negativity and integrality:**
$$x_{i,j} \in \{0, 1\} \quad \forall 1 \leq i < j \leq 8$$

### Feasibility Sanity Check

- Total nodes in the full problem: 9 (Coast + 8 wells). A spanning tree on 9 nodes requires 8 edges.
- Edge (Coast, Well 1) is fixed: 1 edge.
- Remaining: 7 edges among the 8 wells to form a tree. ✓
- All distances are positive and finite. ✓
- The graph of wells (nodes 1–8) with the given distances is connected (every pair has a finite distance). ✓

### Parameter Completeness Verification

**Cost Inventory (MANDATORY):**
| Parameter | Value | Source |
|-----------|-------|--------|
| $c_{0,1}$ (Coast to Well 1) | 5.0 miles | Problem text: "Well 1 is the closest to the coast, at a distance of 5 miles" |
| $c_{1,2}$ | 1.3 | Table 8-4 |
| $c_{1,3}$ | 2.1 | Table 8-4 |
| $c_{1,4}$ | 0.9 | Table 8-4 |
| $c_{1,5}$ | 0.7 | Table 8-4 |
| $c_{1,6}$ | 1.8 | Table 8-4 |
| $c_{1,7}$ | 2.0 | Table 8-4 |
| $c_{1,8}$ | 1.5 | Table 8-4 |
| $c_{2,3}$ | 0.9 | Table 8-4 |
| $c_{2,4}$ | 1.8 | Table 8-4 |
| $c_{2,5}$ | 1.2 | Table 8-4 |
| $c_{2,6}$ | 2.6 | Table 8-4 |
| $c_{2,7}$ | 2.3 | Table 8-4 |
| $c_{2,8}$ | 1.1 | Table 8-4 |
| $c_{3,4}$ | 2.6 | Table 8-4 |
| $c_{3,5}$ | 1.7 | Table 8-4 |
| $c_{3,6}$ | 2.5 | Table 8-4 |
| $c_{3,7}$ | 1.9 | Table 8-4 |
| $c_{3,8}$ | 1.0 | Table 8-4 |
| $c_{4,5}$ | 0.7 | Table 8-4 |
| $c_{4,6}$ | 1.6 | Table 8-4 |
| $c_{4,7}$ | 1.5 | Table 8-4 |
| $c_{4,8}$ | 0.9 | Table 8-4 |
| $c_{5,6}$ | 0.9 | Table 8-4 |
| $c_{5,7}$ | 1.1 | Table 8-4 |
| $c_{5,8}$ | 0.8 | Table 8-4 |
| $c_{6,7}$ | 0.6 | Table 8-4 |
| $c_{6,8}$ | 1.0 | Table 8-4 |
| $c_{7,8}$ | 0.5 | Table 8-4 |

All 28 pairwise distances among the 8 wells are provided. The coast-to-Well-1 distance is provided. **No parameters are missing.**

**Objective Parameter Cross-Reference:** Every $c_{i,j}$ in the objective has a numeric value from the table or problem text. ✓

**Objective Unit Check:** The objective is in miles, which is the natural unit for "total pipeline length." The final answer should be a total length in miles. A greedy/Kruskal solution would yield a value on the order of 10–15 miles, which is reasonable for 8 edges with average length ~1 mile. ✓