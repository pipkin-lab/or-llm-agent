**Model Type:** MILP (Mixed Integer Linear Programming)

### 1. Index Sets & Parameters

**Index Sets:**
*   $P = \{A, B, C\}$: The set of projects.
*   $K = \{0, 1, 2, 3, 4\}$: The set of discrete investment levels (in thousand yuan).

**Parameters:**
*   $M = 4$: Total available capital (in thousand yuan).
*   $R_{p,k}$: The benefit (in thousand yuan) obtained from investing amount $k$ in project $p$. Values extracted from Table 7-18:

| Project ($p$) | $k=0$ | $k=1$ | $k=2$ | $k=3$ | $k=4$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **A** | 0 | 41 | 48 | 60 | 66 |
| **B** | 0 | 42 | 50 | 60 | 66 |
| **C** | 0 | 64 | 68 | 78 | 76 |

### 2. Decision Variables

Let $x_{p,k}$ be a binary decision variable defined for each project $p \in P$ and investment level $k \in K$:

$$
x_{p,k} = 
\begin{cases} 
1 & \text{if project } p \text{ is invested with amount } k \\
0 & \text{otherwise}
\end{cases}
$$

**Domain:**
$$ x_{p,k} \in \{0, 1\} \quad \forall p \in P, \forall k \in K $$

### 3. Objective Function

Maximize the total benefit from all projects:

$$
\text{Maximize } Z = \sum_{p \in P} \sum_{k \in K} R_{p,k} x_{p,k}
$$

Substituting the parameter values:

$$
\text{Maximize } Z = 41x_{A,1} + 48x_{A,2} + 60x_{A,3} + 66x_{A,4} + 42x_{B,1} + 50x_{B,2} + 60x_{B,3} + 66x_{B,4} + 64x_{C,1} + 68x_{C,2} + 78x_{C,3} + 76x_{C,4}
$$
*(Note: Terms with $k=0$ have coefficient 0 and are omitted for brevity, but are included in the summation definition.)*

### 4. Operational Constraints

**Constraint 1: Single Investment Level per Project**
Each project must be assigned exactly one investment level from the set $K$. This ensures that for each project $p$, the sum of binary variables across all possible amounts $k$ equals 1.

$$
\sum_{k \in K} x_{p,k} = 1 \quad \forall p \in P
$$

Explicitly:
1.  $x_{A,0} + x_{A,1} + x_{A,2} + x_{A,3} + x_{A,4} = 1$
2.  $x_{B,0} + x_{B,1} + x_{B,2} + x_{B,3} + x_{B,4} = 1$
3.  $x_{C,0} + x_{C,1} + x_{C,2} + x_{C,3} + x_{C,4} = 1$

**Constraint 2: Capital Budget Constraint**
The total amount invested across all projects cannot exceed the available capital $M$.

$$
\sum_{p \in P} \sum_{k \in K} k \cdot x_{p,k} \leq M
$$

Substituting $M=4$:
$$
0(x_{A,0} + x_{B,0} + x_{C,0}) + 1(x_{A,1} + x_{B,1} + x_{C,1}) + 2(x_{A,2} + x_{B,2} + x_{C,2}) + 3(x_{A,3} + x_{B,3} + x_{C,3}) + 4(x_{A,4} + x_{B,4} + x_{C,4}) \leq 4
$$

Simplified:
$$
\sum_{p \in P} (x_{p,1} + 2x_{p,2} + 3x_{p,3} + 4x_{p,4}) \leq 4
$$