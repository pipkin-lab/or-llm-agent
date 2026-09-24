# Transshipment Problem Formulation

## 1. Index Sets & Parameters

**Index Sets:**
- $S = \{X, Y\}$: Set of supply locations (sources)
- $D = \{A, B, C\}$: Set of demand locations (destinations)
- $N = S \cup D = \{X, Y, A, B, C\}$: Set of all nodes in the network

**Parameters:**

*Supply Capacities (tons):*
- $S_X = 70$
- $S_Y = 55$
- Total Supply $= 125$ tons

*Demand Requirements (tons):*
- $D_A = 35$
- $D_B = 40$
- $D_C = 50$
- Total Demand $= 125$ tons
*(Note: Supply equals Demand, so the problem is balanced.)*

*Distance Matrix (km):*
Let $c_{ij}$ denote the distance from node $i$ to node $j$. Based on the provided tables:

| From \ To | X | Y | A | B | C |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **X** | 0 | 12 | 10 | 14 | 12 |
| **Y** | 10 | 0 | 15 | 12 | 18 |
| **A** | [NOT_PROVIDED] | [NOT_PROVIDED] | 0 | 14 | 11 |
| **B** | [NOT_PROVIDED] | [NOT_PROVIDED] | 10 | 0 | 4 |
| **C** | [NOT_PROVIDED] | [NOT_PROVIDED] | 8 | 12 | 0 |

*Clarification on Distances:*
The problem states goods can be shipped directly or transshipped via certain points. The tables provide:
1.  Distances between Sources ($X, Y$).
2.  Distances from Sources to Destinations ($X,Y \to A,B,C$).
3.  Distances between Destinations ($A,B,C$).

In standard transshipment problems where destinations can act as transshipment hubs, flows can move between any nodes in $N$. However, the distance from Destinations back to Sources ($A,B,C \to X,Y$) is not explicitly provided in the tables. Typically, in such textbook problems, if the return distance is not given, it is either assumed to be the same as the forward distance (symmetric) or, more commonly, transshipment is only allowed *through* the destination nodes in a forward direction or the network is directed.

However, looking at Table 3-25, it only lists distances *among* A, B, and C. It does not list distances from A, B, or C to X or Y.
*Interpretation:* The problem implies a network where goods originate at X and Y, must end at A, B, or C, and can potentially move between A, B, and C (transshipment via destination nodes). It does *not* imply shipping from A back to X. Therefore, the arc set $E$ consists of:
- $X \to Y$
- $Y \to X$
- $X \to A, X \to B, X \to C$
- $Y \to A, Y \to B, Y \to C$
- $A \to B, A \to C$
- $B \to A, B \to C$
- $C \to A, C \to B$

The costs $c_{ij}$ for these specific arcs are:
- $c_{XY} = 12, c_{YX} = 10$
- $c_{XA} = 10, c_{XB} = 14, c_{XC} = 12$
- $c_{YA} = 15, c_{YB} = 12, c_{YC} = 18$
- $c_{AB} = 14, c_{AC} = 11$
- $c_{BA} = 10, c_{BC} = 4$
- $c_{CA} = 8, c_{CB} = 12$
- $c_{ii} = 0$ for all $i \in N$

## 2. Decision Variables

Let $x_{ij}$ be the amount of goods (in tons) shipped from node $i$ to node $j$.

**Domain:**
- $x_{ij} \ge 0$ for all arcs $(i, j)$ in the defined network.
- Since the problem involves tons of goods, which can be continuous (bulk goods), we define $x_{ij}$ as **continuous** variables.

Specific variables:
- $x_{XY}, x_{YX}$
- $x_{XA}, x_{XB}, x_{XC}$
- $x_{YA}, x_{YB}, x_{YC}$
- $x_{AB}, x_{AC}$
- $x_{BA}, x_{BC}$
- $x_{CA}, x_{CB}$

## 3. Objective Function

Minimize the total transportation distance:

$$
\text{Minimize } Z = 12x_{XY} + 10x_{YX} + 10x_{XA} + 14x_{XB} + 12x_{XC} + 15x_{YA} + 12x_{YB} + 18x_{YC} + 14x_{AB} + 11x_{AC} + 10x_{BA} + 4x_{BC} + 8x_{CA} + 12x_{CB}
$$

## 4. Operational Constraints

The problem is a balanced transshipment problem. We apply flow conservation constraints for each node in $N = \{X, Y, A, B, C\}$.

**Node Balance Constraints:**

For each node $k \in N$, the total flow into the node plus any supply (if $k$ is a source) must equal the total flow out of the node plus any demand (if $k$ is a destination).

Alternatively, using the standard net flow formulation:
$$ \sum_{j \in N} x_{kj} - \sum_{i \in N} x_{ik} = b_k $$
Where $b_k$ is the net supply at node $k$:
- $b_k > 0$ for pure sources
- $b_k < 0$ for pure sinks
- $b_k = 0$ for transshipment nodes

In this problem:
- Nodes X and Y are sources but can also be transshipment points (since $x_{XY}$ and $x_{YX}$ exist).
- Nodes A, B, and C are destinations but can also be transshipment points (since $x_{AB}$, etc., exist).
- Therefore, **all nodes** act as transshipment nodes in the flow conservation sense, with net supply/demand values determined by their initial supply or final demand.

Let's define $b_k$ (Net Outflow) for each node:
- **Node X**: Has 70 tons of supply. Net outflow = $+70$.
- **Node Y**: Has 55 tons of supply. Net outflow = $+55$.
- **Node A**: Has 35 tons of demand. Net outflow = $-35$.
- **Node B**: Has 40 tons of demand. Net outflow = $-40$.
- **Node C**: Has 50 tons of demand. Net outflow = $-50$.

Check: $70 + 55 - 35 - 40 - 50 = 125 - 125 = 0$. The system is balanced.

**Constraints:**

1.  **Node X (Net Supply = 70):**
    $$ x_{XY} + x_{XA} + x_{XB} + x_{XC} - x_{YX} = 70 $$
    *(Note: Flows into X are subtracted, flows out are added. Here, $x_{YX}$ is the only inflow.)*

2.  **Node Y (Net Supply = 55):**
    $$ x_{YX} + x_{YA} + x_{YB} + x_{YC} - x_{XY} = 55 $$
    *(Note: Flows into Y are subtracted, flows out are added. Here, $x_{XY}$ is the only inflow.)*

3.  **Node A (Net Demand = -35):**
    $$ x_{AB} + x_{AC} - (x_{XA} + x_{YA} + x_{BA} + x_{CA}) = -35 $$
    Or rearranged for clarity (Inflow - Outflow = Demand):
    $$ (x_{XA} + x_{YA} + x_{BA} + x_{CA}) - (x_{AB} + x_{AC}) = 35 $$

4.  **Node B (Net Demand = -40):**
    $$ (x_{XB} + x_{YB} + x_{AB} + x_{CB}) - (x_{BA} + x_{BC}) = 40 $$

5.  **Node C (Net Demand = -50):**
    $$ (x_{XC} + x_{YC} + x_{AC} + x_{BC}) - (x_{CA} + x_{CB}) = 50 $$

**Non-negativity Constraints:**
$$ x_{ij} \ge 0 \quad \forall (i,j) \in E $$
Where $E = \{(X,Y), (Y,X), (X,A), (X,B), (X,C), (Y,A), (Y,B), (Y,C), (A,B), (A,C), (B,A), (B,C), (C,A), (C,B)\}$