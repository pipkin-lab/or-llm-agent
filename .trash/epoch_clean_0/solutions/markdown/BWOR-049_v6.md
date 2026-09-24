## Model Type: LP (Linear Programming)

This is a **transshipment problem** (a generalized transportation problem). Since goods can be shipped directly from sources to destinations or transshipped via intermediate nodes (including other destinations acting as transshipment points), we model this as a network flow problem on a directed graph where all nodes can both receive and send flow.

### Index Sets & Parameters

**Node Set:** $N = \{X, Y, A, B, C\}$

**Supply/Demand Parameters** (in tons):
- $s_X = 70$ (supply at X)
- $s_Y = 55$ (supply at Y)
- $d_A = 35$ (demand at A)
- $d_B = 40$ (demand at B)
- $d_C = 50$ (demand at C)

**Net Balance** $b_i$ for each node $i \in N$ (positive = supply, negative = demand):
- $b_X = 70$
- $b_Y = 55$
- $b_A = -35$
- $b_B = -40$
- $b_C = -50$

**Arc Set:** All ordered pairs $(i, j)$ where $i \neq j$ and a distance is defined. Based on the tables, all inter-node distances are provided:
- From Table 3-23 (X, Y interconnections):
  - $c_{XY} = 12$, $c_{YX} = 10$
- From Table 3-24 (X, Y to A, B, C):
  - $c_{XA} = 10$, $c_{XB} = 14$, $c_{XC} = 12$
  - $c_{YA} = 15$, $c_{YB} = 12$, $c_{YC} = 18$
- From Table 3-25 (A, B, C interconnections):
  - $c_{AB} = 14$, $c_{AC} = 11$
  - $c_{BA} = 10$, $c_{BC} = 4$
  - $c_{CA} = 8$, $c_{CB} = 12$

Total supply = $70 + 55 = 125$ tons. Total demand = $35 + 40 + 50 = 125$ tons. **Balanced problem.**

### Decision Variables

For every directed arc $(i, j)$ with $i \neq j$:
$$x_{ij} \geq 0, \quad \forall (i,j) \in \mathcal{A}$$
where $\mathcal{A} = \{(i,j) : i, j \in N, i \neq j\}$

There are $5 \times 4 = 20$ decision variables:
$x_{XY}, x_{YX}, x_{XA}, x_{XB}, x_{XC}, x_{YA}, x_{YB}, x_{YC}, x_{AB}, x_{AC}, x_{BA}, x_{BC}, x_{CA}, x_{CB}, x_{AX}, x_{AY}, x_{BX}, x_{BY}, x_{CX}, x_{CY}$

**Domain:** All $x_{ij} \in \mathbb{R}_{\geq 0}$ (continuous, since goods are measured in tons and can be fractionally allocated).

### Objective Function

Minimize total transport distance (in ton-km):

$$\min \sum_{(i,j) \in \mathcal{A}} c_{ij} \, x_{ij}$$

Expanded:
$$\min \; 12x_{XY} + 10x_{YX} + 10x_{XA} + 14x_{XB} + 12x_{XC} + 15x_{YA} + 12x_{YB} + 18x_{YC} + 14x_{AB} + 11x_{AC} + 10x_{BA} + 4x_{BC} + 8x_{CA} + 12x_{CB} + 0 \cdot x_{AX} + 0 \cdot x_{AY} + 0 \cdot x_{BX} + 0 \cdot x_{BY} + 0 \cdot x_{CX} + 0 \cdot x_{CY}$$

**Note:** The distances from destinations back to sources (e.g., $A \to X$, $B \to Y$, etc.) are **not provided** in any table. Since transshipment from destinations back to sources would be physically nonsensical in a distribution context, and no cost is given, we set these arcs' costs to 0 but they will naturally not be used in an optimal solution (or we can exclude them from the model entirely). For completeness of the formulation, I will **exclude** arcs from $\{A,B,C\}$ back to $\{X,Y\}$ since no distance/cost is provided and they are operationally irrelevant. The effective arc set is:

$\mathcal{A} = \{(X,Y), (Y,X), (X,A), (X,B), (X,C), (Y,A), (Y,B), (Y,C), (A,B), (A,C), (B,A), (B,C), (C,A), (C,B)\}$

Revised objective (14 terms):
$$\min \; 12x_{XY} + 10x_{YX} + 10x_{XA} + 14x_{XB} + 12x_{XC} + 15x_{YA} + 12x_{YB} + 18x_{YC} + 14x_{AB} + 11x_{AC} + 10x_{BA} + 4x_{BC} + 8x_{CA} + 12x_{CB}$$

### Operational Constraints

**Flow Conservation Constraints** for each node $i \in N$:

$$\sum_{j: (i,j)\in\mathcal{A}} x_{ij} - \sum_{j: (j,i)\in\mathcal{A}} x_{ji} = b_i$$

Expanded for each node:

**Node X** (supply = 70):
$$x_{XY} + x_{XA} + x_{XB} + x_{XC} - x_{YX} = 70$$

**Node Y** (supply = 55):
$$x_{YX} + x_{YA} + x_{YB} + x_{YC} - x_{XY} = 55$$

**Node A** (demand = 35):
$$x_{AB} + x_{AC} - x_{XA} - x_{YA} - x_{BA} - x_{CA} = -35$$

**Node B** (demand = 40):
$$x_{BA} + x_{BC} - x_{XB} - x_{YB} - x_{AB} - x_{CB} = -40$$

**Node C** (demand = 50):
$$x_{CA} + x_{CB} - x_{XC} - x_{YC} - x_{AC} - x_{BC} = -50$$

**Non-negativity:**
$$x_{ij} \geq 0 \quad \forall (i,j) \in \mathcal{A}$$

### Feasibility Sanity Check

- Total supply: $70 + 55 = 125$ tons
- Total demand: $35 + 40 + 50 = 125$ tons
- The problem is balanced. A feasible solution exists (e.g., direct shipments only can satisfy all demands since $70 \geq 35+40$ is false, but with transshipment and the full network, feasibility is guaranteed by the balanced nature and connectivity of the network).

### Parameter Completeness Verification

| Parameter | Value | Source |
|-----------|-------|--------|
| $s_X$ | 70 | Problem text |
| $s_Y$ | 55 | Problem text |
| $d_A$ | 35 | Problem text |
| $d_B$ | 40 | Problem text |
| $d_C$ | 50 | Problem text |
| $c_{XY}$ | 12 | Table 3-23 |
| $c_{YX}$ | 10 | Table 3-23 |
| $c_{XA}$ | 10 | Table 3-24 |
| $c_{XB}$ | 14 | Table 3-24 |
| $c_{XC}$ | 12 | Table 3-24 |
| $c_{YA}$ | 15 | Table 3-24 |
| $c_{YB}$ | 12 | Table 3-24 |
| $c_{YC}$ | 18 | Table 3-24 |
| $c_{AB}$ | 14 | Table 3-25 |
| $c_{AC}$ | 11 | Table 3-25 |
| $c_{BA}$ | 10 | Table 3-25 |
| $c_{BC}$ | 4 | Table 3-25 |
| $c_{CA}$ | 8 | Table 3-25 |
| $c_{CB}$ | 12 | Table 3-25 |

All parameters are fully specified. No `[NOT_PROVIDED]` values.