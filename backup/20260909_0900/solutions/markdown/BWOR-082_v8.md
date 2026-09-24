# Relocation Planning Optimization Model

## 1. Index Sets & Parameters

**Index Sets:**
*   $W = \{A, B, C, D, E\}$: Set of workshops.
*   $L = \{U, \alpha, \beta\}$: Set of locations, where $U$ is the Urban area, $\alpha$ is Town $\alpha$, and $\beta$ is Town $\beta$.

**Parameters:**

**A. Relocation Savings ($S_{i,l}$):**
Annual cost savings (in 10,000 yuan) if workshop $i$ is moved from Urban to location $l$.
*   Note: Savings are only applicable if the workshop moves from Urban. If a workshop stays in Urban, savings are 0.
    *   $S_{i, U} = 0$ for all $i \in W$.
    *   $S_{A, \alpha} = 100$, $S_{B, \alpha} = 150$, $S_{C, \alpha} = 100$, $S_{D, \alpha} = 200$, $S_{E, \alpha} = 50$
    *   $S_{A, \beta} = 100$, $S_{B, \beta} = 200$, $S_{C, \beta} = 150$, $S_{D, \beta} = 150$, $S_{E, \beta} = 150$

**B. Transport Volumes ($C_{ik}$):**
Annual transport volume (tons/year) between workshop $i$ and workshop $k$. Based on Table C-19:
*   $C_{A,B} = C_{B,A} = 0$ (Implicit, not listed, assume 0 if not specified or symmetric. Table shows A-B is 0? Wait, Table C-19 Row A, Col B is 0. Row B, Col C is 1400. Let's list non-zeros explicitly from the table structure):
    *   $C_{A,C} = 1000$
    *   $C_{A,D} = 1500$
    *   $C_{B,C} = 1400$
    *   $C_{B,D} = 1200$
    *   $C_{C,E} = 2000$
    *   $C_{D,E} = 700$
    *   All other $C_{ik} = 0$.
*   Note: The table is upper triangular. We assume traffic is bidirectional or the cost is calculated per unit flow $C_{ik}$ from $i$ to $k$. Usually, in these facility location problems, $C_{ik}$ represents the total flow between $i$ and $k$. The cost incurred is $C_{ik} \times D_{loc(i), loc(k)}$.

**C. Transportation Costs ($D_{jl}$):**
Cost per ton (yuan/t) to transport from location $j$ to location $l$. Based on Table C-20:
*   $D_{\alpha, \alpha} = 500$, $D_{\alpha, \beta} = 1400$, $D_{\alpha, U} = 1300$
*   $D_{\beta, \alpha} = 1400$ (Implied symmetric or read from table? Table shows $\beta$ row, $\alpha$ col is blank? No, Table C-20:
    *   Row $\alpha$: 500, 1400, 1300
    *   Row $\beta$: (blank), 500, 900 -> Implies $D_{\beta, \alpha} = 1400$ by symmetry or missing data? Standard assumption in such tables is symmetry if blank, or check row/col. Let's look at Row $\alpha$ Col $\beta$ is 1400. Row $\beta$ Col $\alpha$ is blank. Row $U$ Col $\alpha$ is blank, Col $\beta$ is blank?
    *   Let's re-read Table C-20 carefully:
        *   Row $\alpha$: $\alpha=500$, $\beta=1400$, $U=1300$
        *   Row $\beta$: $\alpha=$ (blank), $\beta=500$, $U=900$
        *   Row $U$: $\alpha=$ (blank), $\beta=$ (blank), $U=1000$
    *   Assumption: Transportation costs are symmetric. Thus $D_{j,l} = D_{l,j}$.
    *   $D_{\beta, \alpha} = 1400$
    *   $D_{U, \alpha} = 1300$
    *   $D_{U, \beta} = 900$
    *   $D_{U, U} = 1000$
    *   $D_{\alpha, \alpha} = 500$, $D_{\beta, \beta} = 500$

**D. Capacity Constraint:**
*   Max workshops per location: $M = 3$.

## 2. Decision Variables

Since the number of workshops is small (5) and the problem asks for a specific location plan, this is a discrete assignment problem.

Let $x_{i,l}$ be a binary variable:
$$
x_{i,l} = \begin{cases} 
1 & \text{if workshop } i \text{ is located in } l \\
0 & \text{otherwise}
\end{cases}
$$
for all $i \in W, l \in L$.

## 3. Objective Function

The objective is to **Minimize** the Total Annual Net Cost.
Total Cost = (Total Transportation Costs) - (Total Relocation Savings).

Note on Units:
*   Savings are in **10,000 yuan**.
*   Transportation costs are in **yuan** (since Volume is tons, Cost is yuan/ton).
*   We must convert units to be consistent. Let's convert Savings to **yuan** or Transportation to **10,000 yuan**.
    *   Savings: $S_{i,l} \times 10,000$ yuan.
    *   Transport: $C_{ik} \times D_{jl}$ yuan.
    *   Let's keep the objective in **10,000 yuan** for easier scaling, or just **yuan**. Let's use **yuan** to avoid decimal errors in the model description, but note that $S_{i,l}$ in the table is 100, 150, etc. So $S_{i,l}^{yuan} = S_{i,l}^{table} \times 10,000$.

$$
\text{Minimize } Z = \underbrace{\sum_{i \in W} \sum_{k \in W} C_{ik} \sum_{j \in L} \sum_{l \in L} x_{i,j} D_{j,l} x_{k,l}}_{\text{Total Transportation Cost}} - \underbrace{\sum_{i \in W} \sum_{l \in L} S_{i,l}^{yuan} x_{i,l}}_{\text{Total Relocation Savings}}
$$

*Note on Transportation Term:*
The term $\sum_{j} \sum_{l} x_{i,j} D_{j,l} x_{k,l}$ calculates the unit cost between workshop $i$ and $k$ based on their assigned locations. Since $x$ are binary, this product is 1 only if $i$ is at $j$ and $k$ is at $l$.
This is a quadratic objective function. To linearize it for an LP/MILP solver, we can introduce auxiliary variables or use a different formulation. However, given the small size (5 workshops, 3 locations), we can also formulate this as a MILP with linear objective by expanding the cost structure or using a standard facility location formulation with linearization if necessary. But actually, the product of two binary variables $x_{i,j} x_{k,l}$ is non-linear.

**Linearization Strategy:**
Let $y_{i,k,j,l}$ be a binary variable equal to 1 if workshop $i$ is at $j$ and workshop $k$ is at $l$.
Constraints:
$y_{i,k,j,l} \le x_{i,j}$
$y_{i,k,j,l} \le x_{k,l}$
$y_{i,k,j,l} \ge x_{i,j} + x_{k,l} - 1$
$y_{i,k,j,l} \in \{0,1\}$

Then the transportation cost term becomes:
$\sum_{i} \sum_{k} C_{ik} \sum_{j} \sum_{l} D_{j,l} y_{i,k,j,l}$

However, a simpler approach for small problems or if the solver supports it is to keep the quadratic form if the solver is MILP and allows non-linear objectives, OR we can observe that $C_{ik}$ is 0 for many pairs.
Actually, there is a standard linear formulation for this specific "Quadratic Assignment-like" problem if we fix the locations, but here locations are variables.
Given the constraints (5 workshops), an exhaustive search is possible, but we need a mathematical model.
Let's stick to the **MILP with linearization** for the transportation cost to ensure it is solvable by standard LP/MILP solvers like GLOP/SCIP.

**Revised Objective (Linearized):**
$$
\text{Minimize } Z = \sum_{i \in W} \sum_{k \in W} C_{ik} \sum_{j \in L} \sum_{l \in L} D_{j,l} y_{i,k,j,l} - \sum_{i \in W} \sum_{l \in L} S_{i,l}^{yuan} x_{i,l}
$$

Where $S_{i,l}^{yuan} = S_{i,l}^{\text{table}} \times 10,000$.

## 4. Operational Constraints

**1. Assignment Constraints:**
Each workshop must be located in exactly one location.
$$
\sum_{l \in L} x_{i,l} = 1, \quad \forall i \in W
$$

**2. Capacity Constraints:**
No more than 3 workshops in any single area.
$$
\sum_{i \in W} x_{i,l} \le 3, \quad \forall l \in L
$$

**3. Linking Constraints for Auxiliary Variables ($y_{i,k,j,l}$):**
These ensure the transportation cost is only incurred if both workshops are assigned to the respective locations.
For all $i, k \in W, j, l \in L$:
$$
y_{i,k,j,l} \le x_{i,j}
$$
$$
y_{i,k,j,l} \le x_{k,l}
$$
$$
y_{i,k,j,l} \ge x_{i,j} + x_{k,l} - 1
$$
$$
y_{i,k,j,l} \in \{0, 1\}
$$

*Optimization Note:* Since $C_{ik} = C_{ki}$ and $D_{j,l} = D_{l,j}$, and we sum over all $i,k$, we might be double-counting if we don't restrict $i < k$.
In the objective sum $\sum_{i} \sum_{k}$, the pair $(A,C)$ and $(C,A)$ are both included.
The cost of transport between A and C is $C_{AC} \times D_{loc(A), loc(C)}$.
If we sum over all $i \neq k$, we count the flow $A \to C$ and $C \to A$.
If $C_{ik}$ represents the *total* traffic volume between i and k (bidirectional), then the cost is just $C_{ik} \times D$.
If the sum is over all $i \neq k$, then for pair $\{i,k\}$, we have terms for $(i,k)$ and $(k,i)$.
If $C_{ik}$ is the volume from $i$ to $k$, and traffic is symmetric ($C_{ik}=C_{ki}$), then the total cost for the pair is $2 \times C_{ik} \times D$?
Usually, in such tables, $C_{ik}$ is the total flow between $i$ and $k$.
Let's assume the table provides the total flow between $i$ and $k$.
If we define the objective as $\sum_{i < k} C_{ik} \times \text{Cost}(loc(i), loc(k))$, we avoid double counting.
Let's refine the objective to sum over unique pairs $i < k$.

**Refined Objective:**
$$
\text{Minimize } Z = \sum_{\{i,k\} \subseteq W, i < k} C_{ik} \left( \sum_{j \in L} \sum_{l \in L} D_{j,l} y_{i,k,j,l} \right) - \sum_{i \in W} \sum_{l \in L} S_{i,l}^{yuan} x_{i,l}
$$

**4. Variable Domains:**
$$
x_{i,l} \in \{0, 1\}, \quad \forall i \in W, l \in L
$$
$$
y_{i,k,j,l} \in \{0, 1\}, \quad \forall i, k \in W, i \neq k, j, l \in L
$$

---

### Summary of Data for Implementation

**Savings (converted to Yuan):**
*   A: $\alpha=1,000,000$, $\beta=1,000,000$
*   B: $\alpha=1,500,000$, $\beta=2,000,000$
*   C: $\alpha=1,000,000$, $\beta=1,500,000$
*   D: $\alpha=2,000,000$, $\beta=1,500,000$
*   E: $\alpha=500,000$, $\beta=1,500,000$
*   (Savings for Urban = 0)

**Transport Volumes $C_{ik}$ (Tons):**
*   $C_{A,C} = 1000$
*   $C_{A,D} = 1500$
*   $C_{B,C} = 1400$
*   $C_{B,D} = 1200$
*   $C_{C,E} = 2000$
*   $C_{D,E} = 700$
*   All others 0.

**Transport Costs $D_{jl}$ (Yuan/Ton):**
*   $D_{U,U} = 1000$
*   $D_{U,\alpha} = D_{\alpha,U} = 1300$
*   $D_{U,\beta} = D_{\beta,U} = 900$
*   $D_{\alpha,\alpha} = 500$
*   $D_{\alpha,\beta} = D_{\beta,\alpha} = 1400$
*   $D_{\beta,\beta} = 500$