## Model Type Declaration
**MILP** (Mixed Integer Linear Programming)

The problem involves allocating discrete physical units (sales outlets) to regions to maximize profit. Since the number of outlets must be integers, this is an integer programming problem. The objective function and constraints are linear with respect to the decision variables.

---

## Index Sets & Parameters

**Index Sets:**
- $R = \{1, 2, 3\}$: Set of regions.
- $K = \{0, 1, 2, 3, 4\}$: Set of possible numbers of sales outlets per region.

**Parameters:**
- $N = 4$: Total number of sales outlets to be allocated.
- $P_{r,k}$: Monthly profit (in consistent monetary units) from allocating $k$ sales outlets to region $r$.

The profit parameters $P_{r,k}$ are extracted from Table 7-2:

| Region $r$ | $k=0$ | $k=1$ | $k=2$ | $k=3$ | $k=4$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| 1 | 0 | 16 | 25 | 30 | 32 |
| 2 | 0 | 12 | 17 | 21 | 22 |
| 3 | 0 | 10 | 14 | 16 | 17 |

---

## Decision Variables

We use binary variables to represent the allocation choices. For each region $r \in R$ and each possible number of outlets $k \in K$, define:

$$
x_{r,k} = 
\begin{cases} 
1 & \text{if exactly } k \text{ sales outlets are allocated to region } r \\
0 & \text{otherwise}
\end{cases}
$$

**Domain:**
$$
x_{r,k} \in \{0, 1\} \quad \forall r \in R, \forall k \in K
$$

---

## Objective Function

Maximize the total monthly profit:

$$
\text{Maximize } Z = \sum_{r \in R} \sum_{k \in K} P_{r,k} \cdot x_{r,k}
$$

Substituting the parameter values:

$$
Z = 0x_{1,0} + 16x_{1,1} + 25x_{1,2} + 30x_{1,3} + 32x_{1,4} + 0x_{2,0} + 12x_{2,1} + 17x_{2,2} + 21x_{2,3} + 22x_{2,4} + 0x_{3,0} + 10x_{3,1} + 14x_{3,2} + 16x_{3,3} + 17x_{3,4}
$$

---

## Operational Constraints

### 1. Exactly one allocation level per region
Each region must have exactly one number of sales outlets allocated (from 0 to 4):

$$
\sum_{k \in K} x_{r,k} = 1 \quad \forall r \in R
$$

Explicitly:
$$
x_{1,0} + x_{1,1} + x_{1,2} + x_{1,3} + x_{1,4} = 1
$$
$$
x_{2,0} + x_{2,1} + x_{2,2} + x_{2,3} + x_{2,4} = 1
$$
$$
x_{3,0} + x_{3,1} + x_{3,2} + x_{3,3} + x_{3,4} = 1
$$

### 2. Total number of outlets constraint
The sum of outlets allocated across all regions must equal exactly $N = 4$:

$$
\sum_{r \in R} \sum_{k \in K} k \cdot x_{r,k} = 4
$$

Explicitly:
$$
0x_{1,0} + 1x_{1,1} + 2x_{1,2} + 3x_{1,3} + 4x_{1,4} + 0x_{2,0} + 1x_{2,1} + 2x_{2,2} + 3x_{2,3} + 4x_{2,4} + 0x_{3,0} + 1x_{3,1} + 2x_{3,2} + 3x_{3,3} + 4x_{3,4} = 4
$$

### 3. Non-negativity and integrality
Already specified in the variable domains:
$$
x_{r,k} \in \{0, 1\} \quad \forall r \in R, \forall k \in K
$$

---

## Feasibility Sanity Check

- **Total supply of outlets:** 4
- **Total capacity:** Each region can take up to 4 outlets, so total capacity is $4+4+4=12 \geq 4$. Feasible.
- **Minimum allocation:** Each region can take 0 outlets, so minimum total is 0. Since we need to allocate exactly 4, and $4 \leq 12$, the constraint is satisfiable.
- **Example feasible solution:** Allocate 2 to Region 1, 1 to Region 2, 1 to Region 3 → total = 4. Profit = $25 + 12 + 10 = 47$.
- **Example optimal candidate:** Let's check a few combinations summing to 4:
  - (4,0,0): $32+0+0=32$
  - (3,1,0): $30+12+0=42$
  - (3,0,1): $30+0+10=40$
  - (2,2,0): $25+17+0=42$
  - (2,1,1): $25+12+10=47$
  - (1,3,0): $16+21+0=37$
  - (1,2,1): $16+17+10=43$
  - (1,1,2): $16+12+14=42$
  - (0,4,0): $0+22+0=22$
  - (0,3,1): $0+21+10=31$
  - (0,2,2): $0+17+14=31$
  - (0,1,3): $0+12+16=28$
  - (0,0,4): $0+0+17=17$
  - (2,0,2): $25+0+14=39$
  - (1,0,3): $16+0+16=32$
  - (0,3,1) already checked
  - (3,1,0) already checked
  - (1,3,0) already checked
  - (4,0,0) already checked
  
  The maximum among these is **47** for allocation (2,1,1).

The model is feasible and the expected optimal solution is to allocate 2 outlets to Region 1, 1 outlet to Region 2, and 1 outlet to Region 3, yielding a maximum monthly profit of **47**.