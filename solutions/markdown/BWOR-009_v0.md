## MANDATORY COST INVENTORY (PRE-MODELING STEP)

Let me extract every numeric value representing a cost, fee, price, rate, or charge:

1. **Storage and maintenance fee**: 0.1 thousand yuan per unit per quarter (applies to units held in inventory between quarters)
2. **Production cost per unit, Quarter 1**: 12.0 thousand yuan
3. **Production cost per unit, Quarter 2**: 11.0 thousand yuan
4. **Production cost per unit, Quarter 3**: 11.5 thousand yuan
5. **Production cost per unit, Quarter 4**: 12.5 thousand yuan

Total distinct cost figures: 5 (4 production costs + 1 storage fee). These map to:
- 4 production cost parameters (one per quarter) → objective coefficients for production variables
- 1 storage rate parameter → objective coefficients for inventory holding variables

All objective parameters are present. No [NOT_PROVIDED] needed.

## MODEL TYPE DECLARATION

**LP** (Linear Program). All variables are continuous (production quantities and inventory levels are in units, which can be fractional in the LP relaxation; however, since all data are integers and the constraint matrix is totally unimodular for this network flow structure, the LP will yield integer solutions automatically).

## Index Sets & Parameters

**Index Sets:**
- $T = \{1, 2, 3, 4\}$: set of quarters
- $I(i)$: set of production quarters $\{p\}$ that can satisfy demand in quarter $i$, where $p \leq i$ (production in quarter $p$ can be delivered in quarter $i$ if $p \leq i$)

**Parameters (all in thousand yuan):**

| Parameter | Description | Values |
|-----------|-------------|--------|
| $C_p$ | Production capacity in quarter $p$ (units) | $C_1=25,\; C_2=35,\; C_3=30,\; C_4=20$ |
| $D_i$ | Delivery quantity required in quarter $i$ (units) | $D_1=15,\; D_2=20,\; D_3=25,\; D_4=20$ |
| $c_p$ | Production cost per unit in quarter $p$ (thousand yuan/unit) | $c_1=12.0,\; c_2=11.0,\; c_3=11.5,\; c_4=12.5$ |
| $h$ | Storage and maintenance fee per unit per quarter (thousand yuan/unit/quarter) | $h = 0.1$ |
| $H_{p,i}$ | Holding cost for a unit produced in quarter $p$ and delivered in quarter $i$ ($p < i$) | $H_{p,i} = h \times (i - p)$ |

Explicit holding costs:
- $H_{1,2} = 0.1 \times 1 = 0.1$
- $H_{1,3} = 0.1 \times 2 = 0.2$
- $H_{1,4} = 0.1 \times 3 = 0.3$
- $H_{2,3} = 0.1 \times 1 = 0.1$
- $H_{2,4} = 0.1 \times 2 = 0.2$
- $H_{3,4} = 0.1 \times 1 = 0.1$

**Objective Parameter Cross-Reference:**
- $c_p$ for $p=1..4$: all values located in Table 3-30. ✓
- $H_{p,i}$: derived from $h=0.1$ (stated in problem text) and time lag $(i-p)$. ✓
- All parameters fully specified.

## Decision Variables

$x_{p,i}$: Number of units produced in quarter $p$ and delivered in quarter $i$ (units), for all $p \in T,\; i \in T,\; p \leq i$.

Domain: $x_{p,i} \geq 0$ for all valid $(p, i)$ pairs.

There are $\binom{4+1}{2} = 10$ decision variables:
- Quarter 1 production: $x_{1,1},\; x_{1,2},\; x_{1,3},\; x_{1,4}$
- Quarter 2 production: $x_{2,2},\; x_{2,3},\; x_{2,4}$
- Quarter 3 production: $x_{3,3},\; x_{3,4}$
- Quarter 4 production: $x_{4,4}$

## Objective Function

$$\min \; Z = \sum_{p=1}^{4} \sum_{i=p}^{4} \left( c_p + H_{p,i} \right) x_{p,i}$$

Expanded:

$$Z = 12.0\,x_{1,1} + 12.1\,x_{1,2} + 12.2\,x_{1,3} + 12.3\,x_{1,4} + 11.0\,x_{2,2} + 11.1\,x_{2,3} + 11.2\,x_{2,4} + 11.5\,x_{3,3} + 11.6\,x_{3,4} + 12.5\,x_{4,4}$$

**Objective Unit Verification:** The objective is in thousand yuan (matching the problem's request for "total annual cost in thousand yuan"). Each term is (cost per unit in thousand yuan) × (number of units) = thousand yuan. ✓

## Operational Constraints

### 1. Production Capacity Constraints (one per quarter)

For each production quarter $p \in T$, the total units produced in quarter $p$ (for delivery in any quarter $i \geq p$) cannot exceed the production capacity:

$$\sum_{i=p}^{4} x_{p,i} \leq C_p, \quad \forall\; p \in T$$

Explicitly:
- $x_{1,1} + x_{1,2} + x_{1,3} + x_{1,4} \leq 25$
- $x_{2,2} + x_{2,3} + x_{2,4} \leq 35$
- $x_{3,3} + x_{3,4} \leq 30$
- $x_{4,4} \leq 20$

### 2. Delivery Demand Constraints (one per quarter)

For each delivery quarter $i \in T$, the total units delivered in quarter $i$ (from production in any quarter $p \leq i$) must exactly meet the contractual delivery quantity:

$$\sum_{p=1}^{i} x_{p,i} = D_i, \quad \forall\; i \in T$$

Explicitly:
- $x_{1,1} = 15$
- $x_{1,2} + x_{2,2} = 20$
- $x_{1,3} + x_{2,3} + x_{3,3} = 25$
- $x_{1,4} + x_{2,4} + x_{3,4} + x_{4,4} = 20$

### 3. Non-negativity Constraints

$$x_{p,i} \geq 0, \quad \forall\; p \in T,\; i \in T,\; p \leq i$$

## FEASIBILITY SANITY CHECK

- **Total production capacity**: $25 + 35 + 30 + 20 = 110$ units
- **Total delivery demand**: $15 + 20 + 25 + 20 = 80$ units
- Since total supply (110) > total demand (80), the capacity constraints are inequalities ($\leq$), allowing unused capacity. The demand constraints are equalities because the contract must be fully met.
- No individual quarter's capacity is less than its own demand: $25 \geq 15$ ✓, $35 \geq 20$ ✓, $30 \geq 25$ ✓, $20 \geq 20$ ✓. So even with no carry-over, each quarter could independently meet its own demand. The problem is feasible.
- The structure is a classic transportation/lot-sizing network flow problem with a totally unimodular constraint matrix (each variable appears in exactly one capacity constraint and one demand constraint), guaranteeing integer optimal solutions.

## FINAL MAGNITUDE SANITY CHECK (Greedy Solution Estimate)

A natural heuristic: produce as much as possible in the cheapest quarter (Q2, cost 11.0) and use others as needed.

- Q1 demand (15): must be met by Q1 production (earliest). Cost: $15 \times 12.0 = 180$.
- Q2 demand (20): Q2 is cheapest (11.0). Produce 20 in Q2. Cost: $20 \times 11.0 = 220$.
- Q3 demand (25): Q2 is still cheapest, but Q2 capacity is 35 and 20 are already used for Q2 demand. Remaining Q2 capacity: 15. Use 15 from Q2 (cost $15 \times (11.0 + 0.1) = 15 \times 11.1 = 166.5$) and 10 from Q3 (cost $10 \times 11.5 = 115$). Q3 total produced: 10 (for Q3) + remaining for Q4.
- Q4 demand (20): Remaining Q2 capacity: 0. Q3 remaining capacity: $30 - 10 = 20$. Use 20 from Q3 (cost $20 \times (11.5 + 0.1) = 20 \times 11.6 = 232$).

Total ≈ $180 + 220 + 166.5 + 115 + 232 = 913.5$ thousand yuan.

This is a reasonable magnitude for the problem context. The objective is in thousand yuan, and the answer is expected to be in the hundreds of thousand yuan range. ✓