### Index Sets & Parameters

**Index Sets:**
*   $W = \{A, B, C, D, E\}$: Set of workshops.
*   $L = \{U, \alpha, \beta\}$: Set of locations (Urban area, Town $\alpha$, Town $\beta$).
*   $W_{pair}$: Set of workshop pairs $\{i, k\}$ where $i < k$ and $C_{ik} > 0$. Based on Table C-19, the active pairs are:
    *   $(A, C)$ with volume 1000
    *   $(A, D)$ with volume 1500
    *   $(B, C)$ with volume 1400
    *   $(B, D)$ with volume 1200
    *   $(C, E)$ with volume 2000
    *   $(D, E)$ with volume 700

**Parameters:**
*   $S_{i, l}$: Annual cost savings (10,000 yuan/year) if workshop $i$ is moved to location $l$.
    *   $S_{A, \alpha}=100, S_{B, \alpha}=150, S_{C, \alpha}=100, S_{D, \alpha}=200, S_{E, \alpha}=50$
    *   $S_{A, \beta}=100, S_{B, \beta}=200, S_{C, \beta}=150, S_{D, \beta}=150, S_{E, \beta}=150$
    *   $S_{i, U} = 0$ for all $i$ (Baseline, no savings).
    *   *Note: Units converted to yuan/year by multiplying by 10,000 for consistency with transport costs.*
*   $C_{ik}$: Annual transport volume (tons/year) between workshops $i$ and $k$.
    *   $C_{A,C}=1000, C_{A,D}=1500, C_{B,C}=1400, C_{B,D}=1200, C_{C,E}=2000, C_{D,E}=700$.
*   $D_{j, l}$: Transportation cost per ton (yuan/t) from location $j$ to location $l$.
    *   $D_{U, \alpha}=1300, D_{U, \beta}=900, D_{U, U}=1000$
    *   $D_{\alpha, \beta}=1400, D_{\alpha, U}=1300, D_{\alpha, \alpha}=500$
    *   $D_{\beta, U}=900, D_{\beta, \alpha}=1400, D_{\beta, \beta}=500$
    *   *Note: Symmetric, so $D_{j,l} = D_{l,j}$.*

### Decision Variables

1.  **$x_{i, l}$**: Binary variable.
    *   $x_{i, l} = 1$ if workshop $i$ is located in location $l$.
    *   $x_{i, l} = 0$ otherwise.
    *   Domain: $x_{i, l} \in \{0, 1\}$ for all $i \in W, l \in L$.

2.  **$y_{i, k, j, l}$**: Binary variable (Auxiliary variable for linearization).
    *   $y_{i, k, j, l} = 1$ if workshop $i$ is in location $j$ AND workshop $k$ is in location $l$.
    *   Domain: $y_{i, k, j, l} \in \{0, 1\}$ for all distinct $i, k \in W$, $j, l \in L$.
    *   *Note: We only need these variables for pairs $(i,k) \in W_{pair}$.*

### Objective Function

Minimize the total net cost, which is the total increased transportation cost minus the total relocation savings.

$$
\text{Minimize } Z = \sum_{(i,k) \in W_{pair}} C_{ik} \sum_{j \in L} \sum_{l \in L} D_{j,l} y_{i,k,j,l} - \sum_{i \in W} \sum_{l \in L} S_{i,l}^{(yuan)} x_{i,l}
$$

Where $S_{i,l}^{(yuan)} = S_{i,l} \times 10,000$.

### Operational Constraints

1.  **Assignment Constraint**: Each workshop must be assigned to exactly one location.
    $$
    \sum_{l \in L} x_{i, l} = 1 \quad \forall i \in W
    $$

2.  **Capacity Constraint**: No more than 3 workshops in any location.
    $$
    \sum_{i \in W} x_{i, l} \leq 3 \quad \forall l \in L
    $$

3.  **Linking Constraints (Linearization of Product)**: Ensure $y_{i,k,j,l}$ correctly represents the conjunction of $x_{i,j}=1$ and $x_{k,l}=1$.
    For all distinct $i, k \in W$ and $j, l \in L$:
    
    $$
    y_{i,k,j,l} \leq x_{i,j}
    $$
    $$
    y_{i,k,j,l} \leq x_{k,l}
    $$
    $$
    y_{i,k,j,l} \geq x_{i,j} + x_{k,l} - 1
    $$
    $$
    y_{i,k,j,l} \geq 0
    $$

    *Optimization Note*: Since we only calculate costs for pairs where $C_{ik} > 0$, we only need to define and constrain $y$ variables for $(i,k) \in W_{pair}$. For symmetry in transport cost (distance from $j$ to $l$ is same as $l$ to $j$ in terms of total flow cost if we sum over all ordered pairs, but here we treat flow as undirected volume $C_{ik}$ moving between the two locations), we must be careful.
    
    Actually, the transport cost for pair $(i,k)$ is $C_{ik} \times D_{loc(i), loc(k)}$.
    If we define $y_{i,k,j,l}$ as "i in j AND k in l", then the cost term is $C_{ik} D_{j,l} y_{i,k,j,l}$.
    Since $i \neq k$, the case $j=l$ is possible (if both are in same location).
    
    To reduce variables, we can exploit symmetry if we assume $D_{j,l}=D_{l,j}$, but the standard linearization above is robust.
    
    Let's refine the linking constraints to be strictly necessary.
    For each pair $(i,k) \in W_{pair}$:
    For all $j, l \in L$:
    $$
    y_{i,k,j,l} \leq x_{i,j}
    $$
    $$
    y_{i,k,j,l} \leq x_{k,l}
    $$
    $$
    y_{i,k,j,l} \geq x_{i,j} + x_{k,l} - 1
    $$
    $$
    y_{i,k,j,l} \in \{0, 1\}
    $$