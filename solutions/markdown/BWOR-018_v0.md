# Operations Research Model: Construction Task Assignment

## Model Type: MILP (Mixed-Integer Linear Program)

> **Note:** This is a classic **Assignment Problem**, which is a special case of a linear assignment problem. Since each store must be assigned to exactly one company and each company can build at most one store, the decision variables are binary (0/1). The model is a **MILP** (specifically, a linear assignment problem that can also be solved as an LP due to the total unimodularity of the constraint matrix, but we declare it as MILP for correctness of variable domains).

---

## Index Sets & Parameters

### Index Sets
- $I = \{1, 2, 3, 4, 5\}$: Set of construction companies $A_i$
- $J = \{1, 2, 3, 4, 5\}$: Set of stores $B_j$

### Parameters
The cost parameter $c_{ij}$ represents the construction cost (in thousand yuan) for company $A_i$ to build store $B_j$. All values are extracted from Table 5-10:

| $c_{ij}$ | $B_1$ | $B_2$ | $B_3$ | $B_4$ | $B_5$ |
|----------|-------|-------|-------|-------|-------|
| **$A_1$** | 4     | 8     | 7     | 15    | 12    |
| **$A_2$** | 7     | 9     | 17    | 14    | 10    |
| **$A_3$** | 6     | 9     | 12    | 8     | 7     |
| **$A_4$** | 6     | 7     | 14    | 6     | 10    |
| **$A_5$** | 6     | 9     | 12    | 10    | 6     |

All 25 cost values are explicitly provided in the problem statement. No parameter is missing.

---

## Decision Variables

$$x_{ij} = \begin{cases} 1 & \text{if construction company } A_i \text{ is assigned to build store } B_j \\ 0 & \text{otherwise} \end{cases}$$

**Domain:** $x_{ij} \in \{0, 1\}$ for all $i \in I, j \in J$

---

## Objective Function

**Minimize** the total construction cost (in thousand yuan):

$$\min \sum_{i=1}^{5} \sum_{j=1}^{5} c_{ij} \, x_{ij}$$

Expanding with the given cost values:

$$\min \; 4x_{11} + 8x_{12} + 7x_{13} + 15x_{14} + 12x_{15} + 7x_{21} + 9x_{22} + 17x_{23} + 14x_{24} + 10x_{25} + 6x_{31} + 9x_{32} + 12x_{33} + 8x_{34} + 7x_{35} + 6x_{41} + 7x_{42} + 14x_{43} + 6x_{44} + 10x_{45} + 6x_{51} + 9x_{52} + 12x_{53} + 10x_{54} + 6x_{55}$$

---

## Operational Constraints

### 1. Each store is assigned to exactly one construction company (demand-side balance):

$$\sum_{i=1}^{5} x_{ij} = 1 \quad \forall \, j \in J$$

Explicitly:
- Store $B_1$: $x_{11} + x_{21} + x_{31} + x_{41} + x_{51} = 1$
- Store $B_2$: $x_{12} + x_{22} + x_{32} + x_{42} + x_{52} = 1$
- Store $B_3$: $x_{13} + x_{23} + x_{33} + x_{43} + x_{53} = 1$
- Store $B_4$: $x_{14} + x_{24} + x_{34} + x_{44} + x_{54} = 1$
- Store $B_5$: $x_{15} + x_{25} + x_{35} + x_{45} + x_{55} = 1$

### 2. Each construction company is assigned to at most one store (supply-side capacity):

$$\sum_{j=1}^{5} x_{ij} \leq 1 \quad \forall \, i \in I$$

Since there are exactly 5 companies and 5 stores, and each store must be assigned to exactly one company, these constraints effectively become equalities ($= 1$) in any feasible solution. However, we write them as $\leq 1$ to reflect the logical "at most one" constraint explicitly.

Explicitly:
- Company $A_1$: $x_{11} + x_{12} + x_{13} + x_{14} + x_{15} \leq 1$
- Company $A_2$: $x_{21} + x_{22} + x_{23} + x_{24} + x_{25} \leq 1$
- Company $A_3$: $x_{31} + x_{32} + x_{33} + x_{34} + x_{35} \leq 1$
- Company $A_4$: $x_{41} + x_{42} + x_{43} + x_{44} + x_{45} \leq 1$
- Company $A_5$: $x_{51} + x_{52} + x_{53} + x_{54} + x_{55} \leq 1$

### 3. Variable Bounds:

$$x_{ij} \in \{0, 1\} \quad \forall \, i \in I, \, j \in J$$

---

## Feasibility Sanity Check

- **Total supply** = 5 companies, each can build at most 1 store → max 5 stores can be built.
- **Total demand** = 5 stores, each requires exactly 1 company → need exactly 5 assignments.
- Supply = Demand = 5, so the system is balanced. A feasible solution exists (e.g., the identity assignment). The model is **feasible**.

## Objective Parameter Cross-Reference

All 25 objective coefficients $c_{ij}$ are verified against Table 5-10:

| Index | $c_{ij}$ value | Source |
|-------|---------------|--------|
| $c_{11}$ | 4 | Row $A_1$, Col $B_1$ ✓ |
| $c_{12}$ | 8 | Row $A_1$, Col $B_2$ ✓ |
| $c_{13}$ | 7 | Row $A_1$, Col $B_3$ ✓ |
| $c_{14}$ | 15 | Row $A_1$, Col $B_4$ ✓ |
| $c_{15}$ | 12 | Row $A_1$, Col $B_5$ ✓ |
| $c_{21}$ | 7 | Row $A_2$, Col $B_1$ ✓ |
| $c_{22}$ | 9 | Row $A_2$, Col $B_2$ ✓ |
| $c_{23}$ | 17 | Row $A_2$, Col $B_3$ ✓ |
| $c_{24}$ | 14 | Row $A_2$, Col $B_4$ ✓ |
| $c_{25}$ | 10 | Row $A_2$, Col $B_5$ ✓ |
| $c_{31}$ | 6 | Row $A_3$, Col $B_1$ ✓ |
| $c_{32}$ | 9 | Row $A_3$, Col $B_2$ ✓ |
| $c_{33}$ | 12 | Row $A_3$, Col $B_3$ ✓ |
| $c_{34}$ | 8 | Row $A_3$, Col $B_4$ ✓ |
| $c_{35}$ | 7 | Row $A_3$, Col $B_5$ ✓ |
| $c_{41}$ | 6 | Row $A_4$, Col $B_1$ ✓ |
| $c_{42}$ | 7 | Row $A_4$, Col $B_2$ ✓ |
| $c_{43}$ | 14 | Row $A_4$, Col $B_3$ ✓ |
| $c_{44}$ | 6 | Row $A_4$, Col $B_4$ ✓ |
| $c_{45}$ | 10 | Row $A_4$, Col $B_5$ ✓ |
| $c_{51}$ | 6 | Row $A_5$, Col $B_1$ ✓ |
| $c_{52}$ | 9 | Row $A_5$, Col $B_2$ ✓ |
| $c_{53}$ | 12 | Row $A_5$, Col $B_3$ ✓ |
| $c_{54}$ | 10 | Row $A_5$, Col $B_4$ ✓ |
| $c_{55}$ | 6 | Row $A_5$, Col $B_5$ ✓ |

All objective parameters are confirmed present in the source text. No [NOT_PROVIDED] annotations needed.

## Magnitude Sanity Check

The objective is the sum of exactly 5 cost values (one per assignment), each in the range [4, 17] thousand yuan. A greedy lower-bound estimate: sum of the 5 smallest values in the matrix that form a valid assignment. The minimum possible total is at least $4+6+6+6+6 = 28$ thousand yuan, and the maximum is at most $15+14+17+12+10 = 68$ thousand yuan. The expected optimal answer is a value in the range of roughly 30–50 thousand yuan, which matches the problem's scale (single to double-digit thousand yuan values per assignment). No normalization is needed — the objective is already in the problem's native units (thousand yuan).