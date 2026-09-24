## MANDATORY COST INVENTORY (PRE-MODELING STEP)

| # | Numeric Value | Entity / Description | Role in Model |
|---|---|---|---|
| 1 | 50,000 | Total number of participants (answer sheets) | Total item count $N$ |
| 2 | 10% | Percentage of grade A | Proportion $p_A$ |
| 3 | 25% | Percentage of grade B | Proportion $p_B$ |
| 4 | 30% | Percentage of grade C | Proportion $p_C$ |
| 5 | 20% | Percentage of grade D | Proportion $p_D$ |
| 6 | 15% | Percentage of grade E | Proportion $p_E$ |

**Derived absolute counts:**
- $n_A = 0.10 \times 50000 = 5{,}000$
- $n_B = 0.25 \times 50000 = 12{,}500$
- $n_C = 0.30 \times 50000 = 15{,}000$
- $n_D = 0.20 \times 50000 = 10{,}000$
- $n_E = 0.15 \times 50000 = 7{,}500$

**Cost Interpretation:** Each "scan" detects exactly one specific grade across the entire remaining pile. The cost of one scan is proportional to the number of sheets still in the pile (each sheet must be individually inspected). When sorting grade $g$ at position $k$ in the sequence, the number of sheets examined is the total remaining sheets at that point. The objective is to minimize the **total number of sheet-inspections** (total sorting workload).

---

## Model Type Declaration

**MILP** (Mixed Integer Linear Program) — The decision is a permutation (ordering) of 5 distinct grades, which is naturally modeled with binary assignment variables. The objective is linear in these variables once expanded.

---

## Index Sets & Parameters

### Index Sets
- $G = \{A, B, C, D, E\}$: Set of grades, $|G| = 5$
- $K = \{1, 2, 3, 4, 5\}$: Set of position indices (1 = first to sort, 5 = last to sort)

### Parameters
| Symbol | Value | Description |
|---|---|---|
| $N$ | 50,000 | Total number of answer sheets |
| $n_g$ | $n_A=5000,\; n_B=12500,\; n_C=15000,\; n_D=10000,\; n_E=7500$ | Number of sheets of grade $g$ |
| $p_g$ | $p_A=0.10,\; p_B=0.25,\; p_C=0.30,\; p_D=0.20,\; p_E=0.15$ | Proportion of grade $g$ |

### Derived Parameter
For a grade $g$ placed at position $k$, the number of sheets still present when grade $g$ is scanned equals:
$$R(k) = N - \sum_{j=1}^{k-1} n_{g_j}$$
where $g_j$ is the grade assigned to position $j$. This is the "remaining pile size" before extracting grade at position $k$.

---

## Decision Variables

$$x_{g,k} \in \{0, 1\} \quad \forall\, g \in G,\; k \in K$$

$x_{g,k} = 1$ if and only if grade $g$ is sorted at position $k$ (i.e., it is the $k$-th grade to be scanned/extracted).

---

## Objective Function

**MINIMIZE** total sorting workload $W$, where the workload is the total number of individual sheet-inspections across all scan operations.

When grade $g$ is placed at position $k$, the scan inspects every sheet still in the pile. The pile size at position $k$ is:
$$\text{PileSize}(k) = N - \sum_{j=1}^{k-1} \sum_{g' \in G} n_{g'} \, x_{g',j}$$

The total workload is:
$$\min \quad W = \sum_{k \in K} \sum_{g \in G} x_{g,k} \cdot \left( N - \sum_{j=1}^{k-1} \sum_{g' \in G} n_{g'} \, x_{g',j} \right)$$

This is **quadratic** in the binary variables. However, it can be linearized. Define auxiliary variables:

$$z_{g,k} \in \{0,1\} \quad \forall\, g \in G,\; k \in K$$

with $z_{g,k} = 1$ if grade $g$ is sorted at position $k$ AND we track the cumulative count of sheets already removed before position $k$.

**Linearized Formulation:**

Introduce continuous variables $s_k \geq 0$ for $k \in K$, representing the cumulative number of sheets removed **before** position $k$:
$$s_k = \sum_{j=1}^{k-1} \sum_{g' \in G} n_{g'} \, x_{g',j}$$

Then the pile size at position $k$ is $N - s_k$, and the objective becomes:

$$\min \quad W = \sum_{k=1}^{5} \sum_{g \in G} n_{\text{remaining at } k} \cdot x_{g,k}$$

More precisely, the cost of scanning at position $k$ is $(N - s_k) \times 1$ (one full pass over the remaining pile). But since each scan removes only the sheets of the target grade, the **workload** (total inspections) for a scan at position $k$ equals the pile size at that moment:

$$\min \quad W = \sum_{k=1}^{5} (N - s_k) \cdot \underbrace{\sum_{g \in G} x_{g,k}}_{=1} = \sum_{k=1}^{5} (N - s_k)$$

Wait — this formulation needs care. Let me re-derive.

**Correct Workload Model:**

- At position $k$, the computer scans the pile to find all sheets of the target grade $g$. It must inspect each sheet in the pile until it has found all $n_g$ sheets of grade $g$. In the **worst case / standard model**, it inspects the **entire remaining pile** of size $(N - s_k)$.
- Total workload = sum over all positions of (pile size at that position).

$$\min \quad W = \sum_{k=1}^{5} (N - s_k)$$

where $s_k = \sum_{j=1}^{k-1} \sum_{g' \in G} n_{g'} \, x_{g',j}$ is the number of sheets already extracted before position $k$.

Since $\sum_{g \in G} x_{g,k} = 1$ for each $k$, this is well-defined.

**Fully Linear Objective:**

$$\min \quad W = \sum_{k=1}^{5} N - \sum_{k=1}^{5} s_k = 5N - \sum_{k=1}^{5} \sum_{j=1}^{k-1} \sum_{g' \in G} n_{g'} \, x_{g',j}$$

Re-indexing the double sum (for each grade $g'$ sorted at position $j$, it contributes $n_{g'}$ to $s_k$ for every $k > j$, i.e., for $(5 - j)$ subsequent positions):

$$W = 5N - \sum_{j=1}^{5} \sum_{g' \in G} n_{g'} \, x_{g',j} \cdot (5 - j)$$

$$\boxed{\min \quad W = 5N - \sum_{j=1}^{5} \sum_{g \in G} n_g \, (5 - j) \, x_{g,j}}$$

Equivalently, since $5N$ is constant, this is equivalent to:

$$\max \quad \sum_{j=1}^{5} \sum_{g \in G} n_g \, (5 - j) \, x_{g,j}$$

**Interpretation:** To minimize total workload, we want grades with **large** $n_g$ to be sorted at **early** positions (small $j$), so that their contribution $n_g(5-j)$ is large (maximizing the subtracted term). This means: **sort the most frequent grades first.**

---

## Operational Constraints

### 1. Each grade is assigned to exactly one position:
$$\sum_{k=1}^{5} x_{g,k} = 1 \quad \forall\, g \in G$$

### 2. Each position is assigned exactly one grade:
$$\sum_{g \in G} x_{g,k} = 1 \quad \forall\, k \in K$$

### 3. Binary domain:
$$x_{g,k} \in \{0, 1\} \quad \forall\, g \in G,\; k \in K$$

### 4. Non-negativity (implied by binary domain, stated explicitly per rules):
$$x_{g,k} \geq 0 \quad \forall\, g \in G,\; k \in K$$

---

## Feasibility Sanity Check

- 5 grades, 5 positions → assignment is always feasible (any permutation is valid).
- Total supply (50,000) equals total "demand" (50,000 sheets to be sorted). No infeasibility.

---

## Final Magnitude Sanity Check

**Greedy solution (sort by descending frequency):**

| Position $j$ | Grade | $n_g$ | $5-j$ | Contribution $n_g(5-j)$ |
|---|---|---|---|---|
| 1 | C | 15,000 | 4 | 60,000 |
| 2 | B | 12,500 | 3 | 37,500 |
| 3 | D | 10,000 | 2 | 20,000 |
| 4 | E | 7,500 | 1 | 7,500 |
| 5 | A | 5,000 | 0 | 0 |

Sum of contributions = 60,000 + 37,500 + 20,000 + 7,500 + 0 = **125,000**

$W = 5N - 125{,}000 = 250{,}000 - 125{,}000 = 125{,}000$

**Verification by direct computation:**
- Position 1 (C): pile = 50,000 → cost 50,000
- Position 2 (B): pile = 50,000 − 15,000 = 35,000 → cost 35,000
- Position 3 (D): pile = 35,000 − 12,500 = 22,500 → cost 22,500
- Position 4 (E): pile = 22,500 − 10,000 = 12,500 → cost 12,500
- Position 5 (A): pile = 12,500 − 7,500 = 5,000 → cost 5,000

Total = 50,000 + 35,000 + 22,500 + 12,500 + 5,000 = **125,000** ✓

The objective value is in "sheet-inspections" (raw unit count), which matches the problem's question about "total sorting workload." The magnitude (125,000) is reasonable for 50,000 items sorted in 5 passes.

---

## Optimal Ordering (Solution)

The optimal sorting order is by **descending frequency**:

$$\boxed{C \;\to\; B \;\to\; D \;\to\; E \;\to\; A}$$

Minimum total sorting workload: **125,000 sheet-inspections**.