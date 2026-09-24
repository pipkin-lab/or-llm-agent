# Mathematical Optimization Model

## Model Type Declaration
**MILP (Mixed-Integer Linear Programming)**
*Note: While the underlying problem is a transshipment problem (a linear network flow problem), if physical goods are indivisible units requiring integer tonnage, binary or integer variables may be needed. However, in standard transportation problems, tonnage is treated as a continuous divisible commodity. Therefore, the most appropriate and standard classification is **LP (Linear Programming)**. If strict integer tonnage is required, it becomes an ILP. Given the context of "tons" as a bulk commodity, we treat variables as continuous.*

**Final Declaration: LP (Linear Programming)**

---

## 1. Index Sets & Parameters

### Index Sets
- $O = \{X, Y\}$ : Set of Origin nodes (Supply points)
- $D = \{A, B, C\}$ : Set of Destination nodes (Demand points)
- $N = O \cup D = \{X, Y, A, B, C\}$ : Set of all nodes in the network
- $A_{od}$ : Set of possible shipment arcs from origin $o \in O$ to destination $d \in D$
- $A_{dd'}$ : Set of possible transshipment arcs between destinations $d, d' \in D$ (where $d \neq d'$)
- $A_{od'}$ : Set of possible shipment arcs from origin $o \in O$ to destination $d' \in D$ (Direct shipment)
- $A_{od}$ : Set of all possible arcs in the network.

*Explicit Arc List based on Tables:*
1.  **Supply to Demand (Direct):**
    -   $X \to A$, $X \to B$, $X \to C$
    -   $Y \to A$, $Y \to B$, $Y \to C$
2.  **Transshipment (Between Destinations):**
    -   $A \to B$, $A \to C$
    -   $B \to A$, $B \to C$
    -   $C \to A$, $C \to B$
    *(Note: Self-loops like $A \to A$ have distance 0 and are redundant for flow conservation, so they are excluded from decision variables to simplify the model.)*

### Parameters
**Supply ($S_i$) in tons:**
-   $S_X = 70$
-   $S_Y = 55$
-   Total Supply = $70 + 55 = 125$ tons

**Demand ($D_j$) in tons:**
-   $D_A = 35$
-   $D_B = 40$
-   $D_C = 50$
-   Total Demand = $35 + 40 + 50 = 125$ tons
*(Balance Check: Total Supply = Total Demand. The problem is balanced.)*

**Distances ($c_{ij}$) in km:**
*From Table 3-24 (Origin to Destination):*
-   $c_{XA} = 10$
-   $c_{XB} = 14$
-   $c_{XC} = 12$
-   $c_{YA} = 15$
-   $c_{YB} = 12$
-   $c_{YC} = 18$

*From Table 3-25 (Destination to Destination Transshipment):*
-   $c_{AB} = 14$
-   $c_{AC} = 11$
-   $c_{BA} = 10$
-   $c_{BC} = 4$
-   $c_{CA} = 8$
-   $c_{CB} = 12$

*(Note: Distances in Table 3-23 between X and Y are provided but not used in the objective function because goods originate at X or Y and do not need to be moved between X and Y before shipment, as they are distinct supply sources. The problem states goods are shipped *from* X and Y. There is no indication that goods can be pooled at X/Y before distribution in a way that incurs X-Y transport costs in the standard transshipment model unless specified. Standard interpretation: X and Y are independent sources. The distances in Table 3-23 are likely distractors or for context, but since we minimize total distance of goods *flow*, and flow starts at X or Y, we only sum costs for arcs traversed by the goods. Goods do not start at X, go to Y, then to A. They start at X, go to A. Or start at X, go to B, then B to A. The cost is the sum of segment distances.)*

---

## 2. Decision Variables

Let $x_{ij}$ be the amount of goods (in tons) shipped from node $i$ to node $j$.

**Variables:**
1.  **Direct Shipment Variables (Origin to Destination):**
    -   $x_{XA}, x_{XB}, x_{XC}$
    -   $x_{YA}, x_{YB}, x_{YC}$
2.  **Transshipment Variables (Destination to Destination):**
    -   $x_{AB}, x_{AC}$
    -   $x_{BA}, x_{BC}$
    -   $x_{CA}, x_{CB}$

**Domain:**
$$x_{ij} \geq 0 \quad \forall (i,j) \in \text{Arcs}$$
*(Continuous, non-negative real numbers)*

---

## 3. Objective Function

**Minimize Total Transport Distance:**

$$
\text{Minimize } Z = 
\underbrace{10x_{XA} + 14x_{XB} + 12x_{XC} + 15x_{YA} + 12x_{YB} + 18x_{YC}}_{\text{Direct Origin-to-Destination Costs}} + 
\underbrace{14x_{AB} + 11x_{AC} + 10x_{BA} + 4x_{BC} + 8x_{CA} + 12x_{CB}}_{\text{Transshipment Costs}}
$$

---

## 4. Operational Constraints

### A. Supply Constraints (Outflow from Origins)
The total amount shipped out of an origin cannot exceed its available supply. Since the problem is balanced (Supply = Demand), these are equalities.

1.  **Node X:**
    $$x_{XA} + x_{XB} + x_{XC} = 70$$
2.  **Node Y:**
    $$x_{YA} + x_{YB} + x_{YC} = 55$$

### B. Demand/Flow Conservation Constraints (At Destinations)
For each destination node $j \in \{A, B, C\}$, the total inflow (from origins + from other destinations) must equal the demand at that node.
*Note: In a transshipment model, the node acts as a demand point. The final net inflow must satisfy the demand. Inflow includes direct shipments and transshipments. Outflow from a demand node is only via transshipment to other demand nodes.*

**Conservation Equation General Form for Node $j$:**
$$ \sum_{i \in \{X,Y\}} x_{ij} + \sum_{k \in D, k \neq j} x_{kj} - \sum_{k \in D, k \neq j} x_{jk} = D_j $$

3.  **Node A (Demand = 35):**
    $$ (x_{XA} + x_{YA}) + (x_{BA} + x_{CA}) - (x_{AB} + x_{AC}) = 35 $$
    *Rearranged:*
    $$ x_{XA} + x_{YA} + x_{BA} + x_{CA} - x_{AB} - x_{AC} = 35 $$

4.  **Node B (Demand = 40):**
    $$ (x_{XB} + x_{YB}) + (x_{AB} + x_{CB}) - (x_{BA} + x_{BC}) = 40 $$
    *Rearranged:*
    $$ x_{XB} + x_{YB} + x_{AB} + x_{CB} - x_{BA} - x_{BC} = 40 $$

5.  **Node C (Demand = 50):**
    $$ (x_{XC} + x_{YC}) + (x_{AC} + x_{BC}) - (x_{CA} + x_{CB}) = 50 $$
    *Rearranged:*
    $$ x_{XC} + x_{YC} + x_{AC} + x_{BC} - x_{CA} - x_{CB} = 50 $$

### C. Non-Negativity Constraints
$$x_{ij} \geq 0 \quad \forall i \in \{X,Y\}, j \in \{A,B,C\}$$
$$x_{ij} \geq 0 \quad \forall i,j \in \{A,B,C\}, i \neq j$$

---

## Feasibility Sanity Check

1.  **Balance:** Total Supply (125) = Total Demand (125). The system is balanced.
2.  **Connectivity:** The network is fully connected via direct and transshipment links.
3.  **Non-negativity:** All flows are constrained to be non-negative.
4.  **Redundancy Check:** The sum of all demand constraints (A+B+C) is:
    $$(\text{Total Direct Inflow}) + (\text{Total Trans Inflow}) - (\text{Total Trans Outflow}) = 125$$
    Since $\text{Total Trans Inflow} = \text{Total Trans Outflow}$ (every unit shipped from one dest to another is an outflow from one and inflow to the other), this simplifies to:
    $$\text{Total Direct Inflow} = 125$$
    Which is consistent with the sum of Supply constraints ($70+55=125$). The system is linearly dependent in the standard network flow sense, which is expected and does not affect solvability.

## Final Model Summary

**Model Type:** LP

**Variables:**
$x_{XA}, x_{XB}, x_{XC}, x_{YA}, x_{YB}, x_{YC}, x_{AB}, x_{AC}, x_{BA}, x_{BC}, x_{CA}, x_{CB} \in \mathbb{R}^+$

**Objective:**
$\text{Min } Z = 10x_{XA} + 14x_{XB} + 12x_{XC} + 15x_{YA} + 12x_{YB} + 18x_{YC} + 14x_{AB} + 11x_{AC} + 10x_{BA} + 4x_{BC} + 8x_{CA} + 12x_{CB}$

**Subject to:**
1.  $x_{XA} + x_{XB} + x_{XC} = 70$
2.  $x_{YA} + x_{YB} + x_{YC} = 55$
3.  $x_{XA} + x_{YA} + x_{BA} + x_{CA} - x_{AB} - x_{AC} = 35$
4.  $x_{XB} + x_{YB} + x_{AB} + x_{CB} - x_{BA} - x_{BC} = 40$
5.  $x_{XC} + x_{YC} + x_{AC} + x_{BC} - x_{CA} - x_{CB} = 50$
6.  $x_{ij} \geq 0$ for all defined $x_{ij}$