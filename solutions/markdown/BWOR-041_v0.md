# Operations Research Model: Toy Distribution Problem

## Model Type Declaration
**LP (Linear Program)** — All variables are continuous (units of toys are treated as divisible for the purpose of this LP formulation, though in practice they would be integer; the problem structure and scale suggest an LP is the intended formulation).

## Index Sets & Parameters

**Index Sets:**
- $I = \{A, B, C\}$: set of toy types (supplies)
- $J = \{X, Y, Z\}$: set of department stores (destinations)

**Parameters:**

| Parameter | Description | Values |
|-----------|-------------|--------|
| $S_i$ | Monthly supply limit for toy $i$ | $S_A = 1000$, $S_B = 2000$, $S_C = 2000$ |
| $D_j$ | Expected monthly sales volume per toy type at store $j$ | $D_X = D_Y = D_Z = 1500$ (per toy type) |
| $c_{ij}$ | Profit margin per unit of toy $i$ sold at store $j$ | See matrix below |
| $L_{ij}$ | Lower bound on $x_{ij}$ | $L_{CZ} = 1000$; all others $= 0$ |
| $U_{ij}$ | Upper bound on $x_{ij}$ (effectively 0 if forbidden) | $U_{AZ} = 0$; all others $= +\infty$ (subject to supply/demand) |

**Profit Margin Matrix $c_{ij}$ (from Table 3-6):**

|       | X   | Y   | Z   |
|-------|-----|-----|-----|
| A     | 5   | 4   | —   |
| B     | 16  | 8   | 6   |
| C     | 12  | 10  | 11  |

**Cost Inventory (Mandatory Pre-Modeling Step):**
The only numeric values that serve as objective coefficients are the profit margins in Table 3-6:
- $c_{AX} = 5$, $c_{AY} = 4$, $c_{AZ}$ = forbidden (no value)
- $c_{BX} = 16$, $c_{BY} = 8$, $c_{BZ} = 6$
- $c_{CX} = 12$, $c_{CY} = 10$, $c_{CZ} = 11$

All 8 permissible flow arcs have explicit profit margins. No cost is missing.

**Supply-Demand Balance Check:**
- Total supply: $1000 + 2000 + 2000 = 5000$ units
- Total demand: $3 \text{ stores} \times 3 \text{ toys} \times 1500 = 13500$ units? 

Wait — re-reading: "Each department store has an expected monthly sales volume of 1,500 units for each type of toy." This means each store can sell up to 1,500 units of Toy A, up to 1,500 units of Toy B, and up to 1,500 units of Toy C. So the **demand per toy type** is:
- Demand for Toy A: $1500 \times 3 = 4500$ (but supply is only 1000)
- Demand for Toy B: $1500 \times 3 = 4500$ (but supply is only 2000)
- Demand for Toy C: $1500 \times 3 = 4500$ (but supply is only 2000)

Total demand (13,500) **exceeds** total supply (5,000). Therefore, this is a **supply-constrained** problem: all supply must be shipped (equality on supply side), and demand is an upper bound (inequality).

## Decision Variables

$$x_{ij} = \text{number of units of toy } i \text{ shipped to store } j, \quad \forall i \in I, \; j \in J$$

**Domain:**
$$x_{ij} \geq 0, \quad \forall i \in I, \; j \in J$$

Specifically:
- $x_{AZ} = 0$ (Store Z refuses Toy A — actually "Store C refuses to accept Toy A" — see clarification below)

**Clarification on the constraint "Store C refuses to accept Toy A":** The problem states stores are labeled X, Y, Z, but the constraint says "Store C." Given the table uses X, Y, Z and the toys are A, B, C, this is almost certainly a typo and should read **"Store Z refuses to accept Toy A"** (consistent with the blank/missing entry in Table 3-6 for cell (A, Z)). The table confirms: the (A, Z) cell is empty, indicating no profit margin / not permitted. We set $x_{AZ} = 0$.

## Objective Function

**MAXIMIZE** total profit:

$$\max \; Z = 5\,x_{AX} + 4\,x_{AY} + 16\,x_{BX} + 8\,x_{BY} + 6\,x_{BZ} + 12\,x_{CX} + 10\,x_{CY} + 11\,x_{CZ}$$

Note: $x_{AZ}$ is excluded (set to 0).

**Objective Parameter Cross-Reference:**
| Parameter | Value | Source |
|-----------|-------|--------|
| $c_{AX}$ | 5 | Table 3-6, row A, col X |
| $c_{AY}$ | 4 | Table 3-6, row A, col Y |
| $c_{BX}$ | 16 | Table 3-6, row B, col X |
| $c_{BY}$ | 8 | Table 3-6, row B, col Y |
| $c_{BZ}$ | 6 | Table 3-6, row B, col Z |
| $c_{CX}$ | 12 | Table 3-6, row C, col X |
| $c_{CY}$ | 10 | Table 3-6, row C, col Y |
| $c_{CZ}$ | 11 | Table 3-6, row C, col Z |

All 8 objective parameters confirmed present in the source text.

## Operational Constraints

### 1. Supply Constraints (Equality — Supply < Demand, Rule 18)

Since total supply (5,000) < total potential demand (13,500), **all supply must be fully allocated**:

$$x_{AX} + x_{AY} = 1000 \quad \text{(Toy A supply; } x_{AZ}=0 \text{)}$$

$$x_{BX} + x_{BY} + x_{BZ} = 2000 \quad \text{(Toy B supply)}$$

$$x_{CX} + x_{CY} + x_{CZ} = 2000 \quad \text{(Toy C supply)}$$

### 2. Demand Constraints (Inequality — Store Capacity per Toy Type)

Each store can sell at most 1,500 units of **each** toy type:

For Store X:
$$x_{AX} \leq 1500$$
$$x_{BX} \leq 1500$$
$$x_{CX} \leq 1500$$

For Store Y:
$$x_{AY} \leq 1500$$
$$x_{BY} \leq 1500$$
$$x_{CY} \leq 1500$$

For Store Z:
$$x_{BZ} \leq 1500$$
$$x_{CZ} \leq 1500$$
($x_{AZ} = 0$, so no constraint needed for Toy A at Z)

### 3. Specific Operational Constraints

- **Store Z (referred to as "Store C" in text, typo) refuses Toy A:**
$$x_{AZ} = 0$$

- **Store Z requires at least 1,000 units of Toy C** ("Store C requires at least 1,000 units of Toy C" — again, "Store C" refers to Store Z based on context, since the constraint is about a store's minimum requirement and the only store-specific minimum mentioned alongside the refusal is for the store that doesn't get Toy A):
$$x_{CZ} \geq 1000$$

> **Note on "Store C" ambiguity:** The problem uses X, Y, Z for stores and A, B, C for toys. The phrase "Store C requires at least 1,000 units of Toy C" and "Store C refuses to accept Toy A" most logically refer to **Store Z**, because:
> 1. The table shows a blank for (A, Z), confirming Z does not receive Toy A.
> 2. The minimum requirement of 1,000 for Toy C at a specific store is only operationally meaningful if that store is one of the three (X, Y, Z).
> 3. If it referred to a non-existent "Store C," the constraint would be meaningless.
> 
> We interpret both constraints as applying to **Store Z**.

### 4. Non-Negativity and Prohibition

$$x_{ij} \geq 0, \quad \forall i \in I, \; j \in J$$
$$x_{AZ} = 0$$

## Feasibility Sanity Check

- Supply of A = 1,000, distributed to X and Y (Z forbidden). Max each can take: 1,500. Feasible.
- Supply of B = 2,000, distributed to X, Y, Z. Max each: 1,500. Feasible.
- Supply of C = 2,000, distributed to X, Y, Z. Z needs at least 1,000. Remaining 1,000 split between X and Y (each max 1,500). Feasible.
- No conflict: $x_{CZ} \geq 1000$ and $x_{CZ} \leq 1500$ (demand) and $x_{CZ} \leq 2000$ (supply) are mutually consistent.

The model is **feasible**.

## Summary of the Complete LP

$$\boxed{
\begin{aligned}
\max \quad & 5x_{AX} + 4x_{AY} + 16x_{BX} + 8x_{BY} + 6x_{BZ} + 12x_{CX} + 10x_{CY} + 11x_{CZ} \\[6pt]
\text{s.t.} \quad 
& x_{AX} + x_{AY} = 1000 && \text{(Supply of Toy A)}\\
& x_{BX} + x_{BY} + x_{BZ} = 2000 && \text{(Supply of Toy B)}\\
& x_{CX} + x_{CY} + x_{CZ} = 2000 && \text{(Supply of Toy C)}\\[4pt]
& x_{AX} \leq 1500, \quad x_{BX} \leq 1500, \quad x_{CX} \leq 1500 && \text{(Store X capacity per toy)}\\
& x_{AY} \leq 1500, \quad x_{BY} \leq 1500, \quad x_{CY} \leq 1500 && \text{(Store Y capacity per toy)}\\
& x_{BZ} \leq 1500, \quad x_{CZ} \leq 1500 && \text{(Store Z capacity per toy)}\\[4pt]
& x_{CZ} \geq 1000 && \text{(Store Z minimum for Toy C)}\\
& x_{AZ} = 0 && \text{(Toy A not shipped to Store Z)}\\[4pt]
& x_{ij} \geq 0, \quad \forall i,j
\end{aligned}
}
$$