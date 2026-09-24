## Model Type: MILP (Mixed-Integer Linear Program)

**MANDATORY COST INVENTORY (PRE-MODELING STEP):**
1. **Relocation Savings (Table C-18, 10,000 yuan/year):**
   - Workshop A to α: 100; A to β: 100
   - Workshop B to α: 150; B to β: 200
   - Workshop C to α: 100; C to β: 150
   - Workshop D to α: 200; D to β: 150
   - Workshop E to α: 50; E to β: 150
   *Note: These are SAVINGS (negative costs). Keeping a workshop in Urban yields 0 savings.*

2. **Transportation Costs (Table C-20, yuan/ton):**
   - $D_{\alpha, \alpha} = 500$, $D_{\alpha, \beta} = 1400$, $D_{\alpha, Urban} = 1300$
   - $D_{\beta, \alpha} = 1400$ (symmetric implied or explicit? Table shows row $\beta$, col $\alpha$ is blank but row $\alpha$, col $\beta$ is 1400. Usually symmetric. Let's look at Table C-20 structure: Row $\alpha$: 500, 1400, 1300. Row $\beta$: [blank], 500, 900. Row Urban: [blank], [blank], 1000.
   - Standard interpretation for such matrices: $D_{jl}$ is cost from $j$ to $l$.
     - $D_{\alpha, \alpha} = 500$
     - $D_{\alpha, \beta} = 1400$
     - $D_{\alpha, U} = 1300$
     - $D_{\beta, \beta} = 500$
     - $D_{\beta, U} = 900$
     - $D_{U, U} = 1000$
     - Missing entries ($D_{\beta, \alpha}, D_{U, \alpha}, D_{U, \beta}$) are typically symmetric in transport cost matrices unless specified otherwise. Given $D_{\alpha, \beta}=1400$, assume $D_{\beta, \alpha}=1400$. Given $D_{\alpha, U}=1300$, assume $D_{U, \alpha}=1300$. Given $D_{\beta, U}=900$, assume $D_{U, \beta}=900$.
     - *Self-Correction/Verification*: In many textbook problems, the matrix is lower/upper triangular because $D_{jl}=D_{lj}$. I will assume symmetry for missing off-diagonal terms.

3. **Volumes (Table C-19, tons/year):**
   - $C_{AB} = 0$ (Wait, table says A row, B col is 0? No, looking at C-19:
     - Row A: B=0, C=1000, D=1500, E=0.
     - Row B: C=1400, D=1200, E=0.
     - Row C: D=0, E=2000.
     - Row D: E=700.
   - Note: $C_{ik}$ is given for $i < k$ mostly. Let's list non-zero volumes:
     - $C_{AC} = 1000$
     - $C_{AD} = 1500$
     - $C_{BC} = 1400$
     - $C_{BD} = 1200$
     - $C_{CE} = 2000$ (Wait, Row C, Col E is 2000. Row C, Col D is 0.)
     - $C_{DE} = 700$
   - Let's re-read Table C-19 carefully.
     - Header: & B & C & D & E
     - Row A: 0, 1000, 1500, 0  -> $C_{AB}=0, C_{AC}=1000, C_{AD}=1500, C_{AE}=0$
     - Row B: (blank), 1400, 1200, 0 -> $C_{BC}=1400, C_{BD}=1200, C_{BE}=0$
     - Row C: (blank), (blank), 0, 2000 -> $C_{CD}=0, C_{CE}=2000$
     - Row D: (blank), (blank), (blank), 700 -> $C_{DE}=700$
   - Total pairs with volume: (A,C), (A,D), (B,C), (B,D), (C,E), (D,E).

**Objective Parameter Cross-Reference:**
- Savings $S_{i,t}$: All values provided in Table C-18.
- Volumes $C_{ik}$: All values provided in Table C-19.
- Rates $D_{jl}$: All values provided in Table C-20 (with symmetry assumption for missing cells).

---

## Index Sets & Parameters

**Sets:**
- $I = \{A, B, C, D, E\}$: Set of workshops.
- $L = \{U, \alpha, \beta\}$: Set of locations (Urban, Town $\alpha$, Town $\beta$).
- $P = \{(i,k) \in I \times I \mid i < k, C_{ik} > 0\}$: Set of workshop pairs with non-zero transport volume.
  - $P = \{(A,C), (A,D), (B,C), (B,D), (C,E), (D,E)\}$

**Parameters:**
- $S_{i,t}$: Annual cost **savings** (10,000 yuan/year) if workshop $i$ is moved to town $t \in \{\alpha, \beta\}$. If $t=U$ (Urban), $S_{i,U} = 0$.
  - Values (10,000 yuan/year):
    - $S_{A,\alpha}=100, S_{A,\beta}=100$
    - $S_{B,\alpha}=150, S_{B,\beta}=200$
    - $S_{C,\alpha}=100, S_{C,\beta}=150$
    - $S_{D,\alpha}=200, S_{D,\beta}=150$
    - $S_{E,\alpha}=50, S_{E,\beta}=150$
- $C_{ik}$: Annual transport volume (tons/year) between workshop $i$ and $k$ for $(i,k) \in P$.
  - $C_{AC}=1000, C_{AD}=1500, C_{BC}=1400, C_{BD}=1200, C_{CE}=2000, C_{DE}=700$.
- $D_{jl}$: Transportation cost (yuan/ton) from location $j$ to location $l$.
  - $D_{UU}=1000, D_{\alpha\alpha}=500, D_{\beta\beta}=500$
  - $D_{U\alpha}=1300, D_{\alpha U}=1300$
  - $D_{U\beta}=900, D_{\beta U}=900$
  - $D_{\alpha\beta}=1400, D_{\beta\alpha}=1400$
  - *Unit Note:* Savings are in **10,000 yuan**. Transport costs are in **yuan**.
  - Conversion: $1 \text{ unit of Savings} = 10,000 \text{ yuan}$.
  - To combine into one objective, convert Savings to Yuan: $S'_{i,t} = 10,000 \times S_{i,t}$.
  - OR convert Transport Cost to 10,000 Yuan: $D'_{jl} = D_{jl} / 10,000$.
  - Let's work in **Yuan** for precision, or **10,000 Yuan** for simplicity. Let's use **10,000 Yuan** as the base unit for the objective function to keep numbers manageable, but be careful with transport costs.
  - Actually, it is safer to define the objective in **Yuan** to avoid fractional coefficients for transport if needed, but 10,000s are also fine. Let's stick to **10,000 Yuan** as the reporting unit, so we divide transport costs by 10,000.
  - $D'_{jl} = D_{jl} / 10,000$ (10,000 yuan/ton).
    - $D'_{UU} = 0.1$
    - $D'_{\alpha\alpha} = 0.05, D'_{\beta\beta} = 0.05$
    - $D'_{U\alpha} = D'_{\alpha U} = 0.13$
    - $D'_{U\beta} = D'_{\beta U} = 0.09$
    - $D'_{\alpha\beta} = D'_{\beta\alpha} = 0.14$

## Decision Variables

1. $x_{i,t}$: Binary variable, $x_{i,t} = 1$ if workshop $i$ is located at location $t$, 0 otherwise.
   - Domain: $x_{i,t} \in \{0, 1\}$ for all $i \in I, t \in L$.

2. $y_{ik, jl}$: Binary variable, $y_{ik, jl} = 1$ if workshop $i$ is at location $j$ AND workshop $k$ is at location $l$.
   - Domain: $y_{ik, jl} \in \{0, 1\}$ for all $(i,k) \in P, j,l \in L$.
   - *Note:* This linearizes the product $x_{i,j} x_{k,l}$.

## Objective Function

Minimize Total Annual Cost = (Total Transport Cost) - (Total Relocation Savings)

$$ \text{Minimize } Z = \sum_{(i,k) \in P} \sum_{j \in L} \sum_{l \in L} C_{ik} D'_{jl} y_{ik, jl} - \sum_{i \in I} \sum_{t \in \{\alpha, \beta\}} S_{i,t} x_{i,t} $$

*Where:*
- $C_{ik} D'_{jl}$ is the annual transport cost (10,000 yuan) for the flow between $i$ and $k$ when $i$ is at $j$ and $k$ is at $l$.
- $S_{i,t}$ is the annual savings (10,000 yuan) for moving $i$ to $t$.

## Operational Constraints

**1. Assignment Constraints:**
Each workshop must be assigned to exactly one location.
$$ \sum_{t \in L} x_{i,t} = 1 \quad \forall i \in I $$

**2. Capacity/Location Constraints:**
No more than 3 workshops in any location.
$$ \sum_{i \in I} x_{i,t} \le 3 \quad \forall t \in L $$

**3. Linking Constraints (Linearization):**
Ensure $y_{ik, jl}$ is 1 if and only if $x_{i,j}=1$ and $x_{k,l}=1$.
For all $(i,k) \in P, j,l \in L$:
$$ y_{ik, jl} \le x_{i,j} $$
$$ y_{ik, jl} \le x_{k,l} $$
$$ y_{ik, jl} \ge x_{i,j} + x_{k,l} - 1 $$

**4. Non-negativity and Integrality:**
$$ x_{i,t} \in \{0, 1\} \quad \forall i \in I, t \in L $$
$$ y_{ik, jl} \in \{0, 1\} \quad \forall (i,k) \in P, j,l \in L $$

---

### Feasibility Sanity Check
- Total workshops = 5.
- Max per location = 3.
- Locations = 3 (Urban, $\alpha$, $\beta$).
- Can we distribute 5 workshops into 3 bins of size 3? Yes (e.g., 2, 2, 1 or 3, 1, 1). The constraints are not mutually exclusive.

### Parameter Completeness Check
- All $S_{i,t}$ values are present.
- All $C_{ik}$ values for non-zero flows are present.
- All $D_{jl}$ values are present (with symmetry assumption for missing off-diagonals, which is standard for cost matrices in this context).

### Final Magnitude Sanity Check
- If all workshops stay in Urban:
  - Savings = 0.
  - Transport Cost: All pairs are at $U-U$. Rate $D'_{UU} = 0.1$.
  - Total Volume = $1000+1500+1400+1200+2000+700 = 7800$ tons.
  - Cost = $7800 \times 0.1 = 780,000$ yuan = 78 (10,000 yuan).
- If we move some workshops, we gain savings (up to ~100+150+... ~ 850,000 yuan max) but pay higher transport rates (e.g., 0.13, 0.14).
- The objective value should be in the range of tens of "10,000 yuan".
- The question asks to "minimize the total cost". It does not ask for a normalized rate. The base unit of the problem's cost data is mixed (10,000 yuan and yuan). I have normalized to 10,000 yuan. The final answer will be in 10,000 yuan. If the code agent outputs the raw number, it will be in 10,000 yuan. This is consistent.

### Model Summary for Code Agent
- **Type:** MILP
- **Variables:**
  - `x[i][t]` (Binary): Workshop $i$ at location $t$.
  - `y[i][k][j][l]` (Binary): Workshop $i$ at $j$ AND workshop $k$ at $l$. (Only for pairs $(i,k)$ in $P$).
- **Objective:** Minimize $\sum C_{ik} D'_{jl} y_{ik,jl} - \sum S_{it} x_{it}$.
- **Constraints:**
  1. $\sum_t x_{it} = 1$
  2. $\sum_i x_{it} \le 3$
  3. $y_{ikjl} \le x_{ij}$
  4. $y_{ikjl} \le x_{kl}$
  5. $y_{ikjl} \ge x_{ij} + x_{kl} - 1$