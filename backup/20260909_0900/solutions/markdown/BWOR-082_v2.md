### 1. Index Sets & Parameters

**Index Sets:**
*   $W = \{A, B, C, D, E\}$: Set of workshops, indexed by $i \in W$.
*   $L = \{\alpha, \beta, U\}$: Set of locations (Town $\alpha$, Town $\beta$, Urban Area), indexed by $j \in L$.
    *   Note: We use $U$ to denote the Urban area to distinguish it from towns.

**Parameters:**

**1. Relocation Savings ($S_{ij}$):**
Annual cost savings (10,000 yuan/year) if workshop $i$ is moved from Urban to location $j$.
*   If $j = U$ (Urban), $S_{iU} = 0$ (no savings).
*   From Table C-18:
    *   $S_{A,\alpha}=100, S_{A,\beta}=100$
    *   $S_{B,\alpha}=150, S_{B,\beta}=200$
    *   $S_{C,\alpha}=100, S_{C,\beta}=150$
    *   $S_{D,\alpha}=200, S_{D,\beta}=150$
    *   $S_{E,\alpha}=50, S_{E,\beta}=150$

**2. Transportation Volume ($C_{ik}$):**
Annual transport volume (tons/year) between workshop $i$ and workshop $k$.
*   From Table C-19 (Symmetric, $C_{ik} = C_{ki}$):
    *   $C_{AB}=0, C_{AC}=1000, C_{AD}=1500, C_{AE}=0$
    *   $C_{BC}=1400, C_{BD}=1200, C_{BE}=0$
    *   $C_{CD}=0, C_{CE}=2000$
    *   $C_{DE}=700$
    *   All other pairs are 0.

**3. Transportation Cost ($D_{jl}$):**
Cost (yuan/ton) to transport goods from location $j$ to location $l$.
*   From Table C-20:
    *   $D_{\alpha,\alpha}=500, D_{\alpha,\beta}=1400, D_{\alpha,U}=1300$
    *   $D_{\beta,\beta}=500, D_{\beta,U}=900$
    *   $D_{U,U}=1000$
    *   Note: The diagonal elements ($D_{jj}$) represent the cost of transporting goods *within* the same location. The table provides specific values for these (500 for towns, 1000 for Urban). We must use these values as given.
    *   Symmetry: $D_{jl} = D_{lj}$.

**Unit Conversion Note:**
*   Savings are in **10,000 yuan/year**.
*   Transport costs are in **yuan/ton**.
*   Volumes are in **tons/year**.
*   To minimize total cost, we must unify units. Let's convert everything to **10,000 yuan/year**.
    *   Savings term: $S_{ij}$ is already in 10,000 yuan.
    *   Transport term: $C_{ik} \times D_{jl}$ is in (tons) $\times$ (yuan/ton) = yuan.
    *   To convert yuan to 10,000 yuan, divide by 10,000.
    *   Therefore, the effective transport cost coefficient in the objective function will be $\frac{C_{ik} D_{jl}}{10000}$.

### 2. Decision Variables

Let $x_{ij}$ be a binary variable:
$$
x_{ij} = \begin{cases} 
1 & \text{if workshop } i \text{ is located at location } j \\
0 & \text{otherwise}
\end{cases}
$$
for all $i \in W, j \in L$.

### 3. Objective Function

We want to **minimize** the total annual cost.
Total Cost = (Total Transportation Costs) - (Total Relocation Savings).
*Note: Since savings reduce cost, we subtract them. Alternatively, we can view it as minimizing Net Cost = Transport Cost - Savings.*

Let $Z$ be the objective function value (in 10,000 yuan/year).

$$
\min Z = \sum_{i \in W} \sum_{k \in W, i \neq k} \sum_{j \in L} \sum_{l \in L} \left( \frac{C_{ik} D_{jl}}{10000} \right) x_{ij} x_{kl} - \sum_{i \in W} \sum_{j \in L} S_{ij} x_{ij}
$$

**Linearity Handling:**
The term $x_{ij} x_{kl}$ is non-linear (product of binaries). To make this a Mixed Integer Linear Program (MILP), we introduce auxiliary binary variables $y_{ijkl}$.

Let $y_{ijkl}$ be a binary variable:
$$
y_{ijkl} = \begin{cases} 
1 & \text{if workshop } i \text{ is at } j \text{ AND workshop } k \text{ is at } l \\
0 & \text{otherwise}
\end{cases}
$$
for all $i, k \in W$ where $i \neq k$, and $j, l \in L$.

**Reformulated Objective Function:**
$$
\min Z = \sum_{i \in W} \sum_{k \in W, i \neq k} \sum_{j \in L} \sum_{l \in L} \left( \frac{C_{ik} D_{jl}}{10000} \right) y_{ijkl} - \sum_{i \in W} \sum_{j \in L} S_{ij} x_{ij}
$$

*Optimization Note:* Since $C_{ik} = C_{ki}$ and $D_{jl} = D_{lj}$, and the cost of transport between $i$ and $k$ is incurred regardless of direction, we can sum over $i < k$ to avoid double counting if we define the cost flow carefully. However, the standard formulation above sums over all ordered pairs $i \neq k$. If we sum $i \neq k$, the cost $C_{ik}D_{jl}$ is added for pair $(i,k)$ and also for pair $(k,i)$ with locations $(l,j)$.
Let's check the cost symmetry.
Cost for $i \to k$ via $j \to l$ is $C_{ik} D_{jl}$.
Cost for $k \to i$ via $l \to j$ is $C_{ki} D_{lj} = C_{ik} D_{jl}$.
So summing over all $i \neq k$ counts the total traffic between $i$ and $k$ correctly?
Actually, $C_{ik}$ is the total volume between $i$ and $k$. Usually, in facility location, $C_{ik}$ represents the total flow between the two facilities. The cost is $C_{ik} \times D_{dist(loc_i, loc_k)}$.
The term $x_{ij}x_{kl}$ is 1 only if $i$ is at $j$ AND $k$ is at $l$.
If we sum over all $i \neq k$, we count the flow $C_{ik}$ once for the direction $i \to k$ and once for $k \to i$?
No, $C_{ik}$ is a single parameter "volume between i and k".
Standard formulation:
$\text{Transport Cost} = \sum_{i < k} C_{ik} D_{dist(i,k)}$.
Using variables:
$\sum_{i < k} \sum_{j} \sum_{l} C_{ik} D_{jl} y_{ijkl}$.
This avoids double counting the volume $C_{ik}$.

**Corrected Objective Function:**
$$
\min Z = \sum_{\{i,k\} \subset W, i<k} \sum_{j \in L} \sum_{l \in L} \left( \frac{C_{ik} D_{jl}}{10000} \right) y_{ijkl} - \sum_{i \in W} \sum_{j \in L} S_{ij} x_{ij}
$$

### 4. Operational Constraints

**1. Assignment Constraints:**
Each workshop must be located in exactly one location.
$$
\sum_{j \in L} x_{ij} = 1 \quad \forall i \in W
$$

**2. Capacity/Location Constraints:**
No more than 3 workshops can be located in any single area (Urban, $\alpha$, or $\beta$).
$$
\sum_{i \in W} x_{ij} \le 3 \quad \forall j \in L
$$

**3. Linking Constraints for Auxiliary Variables:**
We need to enforce $y_{ijkl} = 1 \iff x_{ij}=1 \text{ and } x_{kl}=1$.
For all $i, k \in W$ with $i < k$, and $j, l \in L$:

*   $y_{ijkl} \le x_{ij}$
*   $y_{ijkl} \le x_{kl}$
*   $y_{ijkl} \ge x_{ij} + x_{kl} - 1$

**4. Variable Domains:**
$$
x_{ij} \in \{0, 1\} \quad \forall i \in W, j \in L
$$
$$
y_{ijkl} \in \{0, 1\} \quad \forall i, k \in W, i < k, j, l \in L
$$

---

### Final Model Summary

**Sets:**
*   $W = \{A, B, C, D, E\}$
*   $L = \{\alpha, \beta, U\}$
*   $P = \{\{i,k\} | i, k \in W, i < k\}$ (Pairs of distinct workshops)

**Parameters:**
*   $S_{ij}$: Savings (10k yuan)
*   $C_{ik}$: Volume (tons)
*   $D_{jl}$: Unit cost (yuan/ton)
*   $\alpha_{ikjl} = \frac{C_{ik} D_{jl}}{10000}$: Converted transport cost coefficient (10k yuan)

**Variables:**
*   $x_{ij} \in \{0,1\}$ for $i \in W, j \in L$
*   $y_{ijkl} \in \{0,1\}$ for $\{i,k\} \in P, j, l \in L$

**Objective:**
$$
\min \sum_{\{i,k\} \in P} \sum_{j \in L} \sum_{l \in L} \alpha_{ikjl} y_{ijkl} - \sum_{i \in W} \sum_{j \in L} S_{ij} x_{ij}
$$

**Constraints:**
1.  $\sum_{j \in L} x_{ij} = 1, \forall i \in W$
2.  $\sum_{i \in W} x_{ij} \le 3, \forall j \in L$
3.  $y_{ijkl} \le x_{ij}, \forall \{i,k\} \in P, j, l \in L$
4.  $y_{ijkl} \le x_{kl}, \forall \{i,k\} \in P, j, l \in L$
5.  $y_{ijkl} \ge x_{ij} + x_{kl} - 1, \forall \{i,k\} \in P, j, l \in L$