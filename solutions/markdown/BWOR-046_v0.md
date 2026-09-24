# Transportation Problem Formulation

## MANDATORY COST INVENTORY (PRE-MODELING STEP)

**Objective cost parameters (transportation + storage costs from factory → warehouse → region):**

| Source (Warehouse) | B1 | B2 | B3 | B4 | B5 |
|---|---|---|---|---|---|
| A1 | 10 | 15 | 20 | 20 | 40 |
| A2 | 20 | 40 | 15 | 30 | 30 |
| A3 | 30 | 35 | 40 | 55 | 25 |

All 15 cost figures are present in Table 3-19. These are per-ton costs (factory-to-warehouse-to-region combined).

**Other numeric parameters:**
- Factory capacity: 270 tons/month
- Warehouse capacities: A1 = 50, A2 = 100, A3 = 150 tons
- Regional demands: B1 = 25, B2 = 105, B3 = 60, B4 = 30, B5 = 70 tons

**Feasibility check:**
- Total demand = 25 + 105 + 60 + 30 + 70 = **300 tons**
- Total supply = **270 tons**
- Total warehouse capacity = 50 + 100 + 150 = **300 tons**
- Since supply (270) < demand (300), not all demand can be met. The model must allow unmet demand.

Per **Rule 18** (Supply < Demand): the supply-side constraint must be an **equality** (all 270 tons are produced and shipped), while demand-side constraints are **inequalities** (≤) to permit unmet demand.

---

## MODEL TYPE DECLARATION

**LP** (Linear Programming). All variables are continuous (tons of sugar are treated as continuous quantities). No integer restrictions are needed.

---

## Index Sets & Parameters

### Index Sets
- $I = \{1, 2, 3\}$: set of warehouses, indexed by $i$ (A1, A2, A3)
- $J = \{1, 2, 3, 4, 5\}$: set of regions, indexed by $j$ (B1, B2, B3, B4, B5)

### Parameters

| Symbol | Description | Value |
|---|---|---|
| $S$ | Total factory supply capacity (tons) | 270 |
| $c_{ij}$ | Unit cost (per ton) from warehouse $i$ to region $j$ | See Table 3-19 below |
| $C_i$ | Storage capacity of warehouse $i$ (tons) | $C_1=50,\; C_2=100,\; C_3=150$ |
| $D_j$ | Demand in region $j$ (tons) | $D_1=25,\; D_2=105,\; D_3=60,\; D_4=30,\; D_5=70$ |

**Cost matrix $c_{ij}$:**

| $c_{ij}$ | $j$=B1 | $j$=B2 | $j$=B3 | $j$=B4 | $j$=B5 |
|---|---|---|---|---|---|
| $i$=A1 | 10 | 15 | 20 | 20 | 40 |
| $i$=A2 | 20 | 40 | 15 | 30 | 30 |
| $i$=A3 | 30 | 35 | 40 | 55 | 25 |

---

## Decision Variables

$$x_{ij} = \text{tons of sugar shipped from warehouse } i \text{ to region } j, \quad \forall i \in I, \; j \in J$$

**Domain:**
$$x_{ij} \geq 0, \quad \forall i \in I, \; j \in J \quad \text{(continuous, non-negative)}$$

---

## Objective Function

**MINIMIZE** total transportation and storage cost:

$$\min \; Z = \sum_{i=1}^{3} \sum_{j=1}^{5} c_{ij} \, x_{ij}$$

Expanded:

$$Z = 10x_{11} + 15x_{12} + 20x_{13} + 20x_{14} + 40x_{15} + 20x_{21} + 40x_{22} + 15x_{23} + 30x_{24} + 30x_{25} + 30x_{31} + 35x_{32} + 40x_{33} + 55x_{34} + 25x_{35}$$

**Objective Parameter Cross-Reference:** All 15 coefficients $(10, 15, 20, 20, 40, 20, 40, 15, 30, 30, 30, 35, 40, 55, 25)$ are extracted directly from Table 3-19. ✓

---

## Operational Constraints

### 1. Supply Constraint (Factory Capacity)

All 270 tons produced must be allocated (Rule 18: supply < demand → equality):

$$\sum_{i=1}^{3} \sum_{j=1}^{5} x_{ij} = 270$$

### 2. Warehouse Capacity Constraints

The total flow through each warehouse cannot exceed its storage capacity:

$$\sum_{j=1}^{5} x_{1j} \leq 50 \quad \text{(A1)}$$

$$\sum_{j=1}^{5} x_{2j} \leq 100 \quad \text{(A2)}$$

$$\sum_{j=1}^{5} x_{3j} \leq 150 \quad \text{(A3)}$$

Or in indexed form:
$$\sum_{j=1}^{5} x_{ij} \leq C_i, \quad \forall i \in I$$

### 3. Regional Demand Constraints

Since total supply (270) < total demand (300), not all demand can be satisfied. Each region can receive at most its demand (Rule 18):

$$\sum_{i=1}^{3} x_{i1} \leq 25 \quad \text{(B1)}$$

$$\sum_{i=1}^{3} x_{i2} \leq 105 \quad \text{(B2)}$$

$$\sum_{i=1}^{3} x_{i3} \leq 60 \quad \text{(B3)}$$

$$\sum_{i=1}^{3} x_{i4} \leq 30 \quad \text{(B4)}$$

$$\sum_{i=1}^{3} x_{i5} \leq 70 \quad \text{(B5)}$$

Or in indexed form:
$$\sum_{i=1}^{3} x_{ij} \leq D_j, \quad \forall j \in J$$

### 4. Non-negativity

$$x_{ij} \geq 0, \quad \forall i \in I, \; j \in J$$

---

## Feasibility Sanity Check

- **Total supply:** 270 tons (equality constraint forces all to be shipped)
- **Total demand:** 300 tons (only ≤ constraints, so 30 tons of demand will go unmet)
- **Total warehouse capacity:** 300 tons ≥ 270 tons (feasible)
- **Individual warehouse capacities:** 50 + 100 + 150 = 300 ≥ 270 (feasible)
- **Individual region demands:** Each $D_j$ is individually satisfiable given the warehouse capacities.
- The model is **feasible**. The solver will find the minimum-cost allocation of 270 tons across the 5 regions, leaving 30 tons of demand unmet (preferentially the most expensive-to-serve region).