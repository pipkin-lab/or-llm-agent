# Operations Research Model: Production Planning for Hongsheng Factory

## Model Type: LP (Linear Programming)

---

## Index Sets & Parameters

### Index Sets
- $P = \{1, 2, 3\}$: Set of products (I, II, III)
- $M_A = \{A_1, A_2\}$: Set of Stage A machines
- $M_B = \{B_1, B_2, B_3\}$: Set of Stage B machines
- $M = M_A \cup M_B$: Set of all machines

### Parameters

**Processing times per unit (minutes):**

| Machine | Product I | Product II | Product III |
|---------|-----------|------------|-------------|
| $A_1$ | 5 | 10 | — |
| $A_2$ | 7 | 9 | 12 |
| $B_1$ | 6 | 8 | — |
| $B_2$ | 4 | — | 11 |
| $B_3$ | 7 | — | — |

*(Blank cells indicate the product cannot be processed on that machine.)*

**Machine availability (hours):**
- $\text{Cap}_{A_1} = 6000$
- $\text{Cap}_{A_2} = 10000$
- $\text{Cap}_{B_1} = 4000$
- $\text{Cap}_{B_2} = 7000$
- $\text{Cap}_{B_3} = 4000$

**Processing cost (yuan/hour):**
- $c_{A_1} = 0.05$, $c_{A_2} = 0.03$
- $c_{B_1} = 0.06$, $c_{B_2} = 0.11$, $c_{B_3} = 0.05$

**Raw material cost (yuan/unit):**
- $r_1 = 0.25$ (Product I)
- $r_2 = 0.35$ (Product II)
- $r_3 = 0.50$ (Product III)

**Selling price (yuan/unit):**
- $p_1 = 1.25$ (Product I)
- $p_2 = 2.00$ (Product II)
- $p_3 = 2.80$ (Product III)

### Cost Inventory (Mandatory Pre-Modeling Step)
| Numeric Value | Entity / Role |
|---|---|
| 5, 10, 7, 9, 12, 6, 8, 4, 11, 7 (min) | Processing times per unit |
| 6000, 10000, 4000, 7000, 4000 (hours) | Machine capacities |
| 0.05, 0.03, 0.06, 0.11, 0.05 (yuan/h) | Processing costs |
| 0.25, 0.35, 0.50 (yuan/unit) | Raw material costs |
| 1.25, 2.00, 2.80 (yuan/unit) | Selling prices |

All parameters are explicitly provided. No [NOT_PROVIDED] values.

---

## Decision Variables

Let $x_{ij}$ denote the **number of units** of product $j$ processed on machine $i$ in the respective stage. Since each product must go through exactly one Stage A machine and exactly one Stage B machine, we define:

**Stage A variables (continuous, $\geq 0$):**
- $x_{A_1,1}$: units of Product I on $A_1$
- $x_{A_1,2}$: units of Product II on $A_1$
- $x_{A_2,1}$: units of Product I on $A_2$
- $x_{A_2,2}$: units of Product II on $A_2$
- $x_{A_2,3}$: units of Product III on $A_2$

**Stage B variables (continuous, $\geq 0$):**
- $x_{B_1,1}$: units of Product I on $B_1$
- $x_{B_1,2}$: units of Product II on $B_1$
- $x_{B_2,1}$: units of Product I on $B_2$
- $x_{B_2,3}$: units of Product III on $B_2$
- $x_{B_3,1}$: units of Product I on $B_3$

**Total production variables (continuous, $\geq 0$):**
- $Q_j = \sum_{i \in M_A} x_{i,j}$ for $j=1,2,3$ (Stage A total)
- $Q_j = \sum_{i \in M_B} x_{i,j}$ for $j=1,2,3$ (Stage B total)

> **Note on integrality:** The problem asks for a "production plan" to maximize profit. Since products are physical units, integer restrictions would be natural. However, given the large scale of machine capacities (thousands of hours) and small processing times, the LP relaxation will yield near-integer solutions. We declare these as **continuous** variables for standard LP formulation. If strict integrality is required, all $x_{ij}$ and $Q_j$ should be INTEGER.

**Domain:**
$$x_{ij} \geq 0, \quad \forall i, j$$

---

## Objective Function

**Maximize total profit = Total Revenue − Total Raw Material Cost − Total Processing Cost**

### Revenue (yuan):
$$\text{Revenue} = 1.25 \, Q_1 + 2.00 \, Q_2 + 2.80 \, Q_3$$

### Raw Material Cost (yuan):
$$\text{RawCost} = 0.25 \, Q_1 + 0.35 \, Q_2 + 0.50 \, Q_3$$

### Processing Cost (yuan):
$$\text{ProcCost} = \sum_{i \in M} c_i \cdot t_{ij} \cdot x_{ij}$$

Expanding explicitly:

$$\text{ProcCost} = 0.05(5x_{A_1,1} + 10x_{A_1,2}) + 0.03(7x_{A_2,1} + 9x_{A_2,2} + 12x_{A_2,3}) + 0.06(6x_{B_1,1} + 8x_{B_1,2}) + 0.11(4x_{B_2,1} + 11x_{B_2,3}) + 0.05(7x_{B_3,1})$$

### Net Profit Objective:

$$\max \; Z = \underbrace{(1.25 - 0.25)Q_1 + (2.00 - 0.35)Q_2 + (2.80 - 0.50)Q_3}_{\text{Gross margin}} - \underbrace{\sum_{i \in M} c_i \sum_{j} t_{ij} \, x_{ij}}_{\text{Processing cost}}$$

Substituting $Q_j$ in terms of Stage A variables (using Stage A for quantity definition; Stage B constraint ensures consistency):

$$\boxed{\max \; Z = 1.00\,Q_1 + 1.65\,Q_2 + 2.30\,Q_3 - \Big[ 0.25x_{A_1,1} + 0.50x_{A_1,2} + 0.21x_{A_2,1} + 0.27x_{A_2,2} + 0.36x_{A_2,3} + 0.36x_{B_1,1} + 0.48x_{B_1,2} + 0.44x_{B_2,1} + 1.21x_{B_2,3} + 0.35x_{B_3,1} \Big]}$$

Where the processing cost coefficients are computed as $c_i \times t_{ij}$ (yuan/unit):

| Term | Calculation | Coefficient |
|---|---|---|
| $x_{A_1,1}$ | $0.05 \times 5$ | 0.25 |
| $x_{A_1,2}$ | $0.05 \times 10$ | 0.50 |
| $x_{A_2,1}$ | $0.03 \times 7$ | 0.21 |
| $x_{A_2,2}$ | $0.03 \times 9$ | 0.27 |
| $x_{A_2,3}$ | $0.03 \times 12$ | 0.36 |
| $x_{B_1,1}$ | $0.06 \times 6$ | 0.36 |
| $x_{B_1,2}$ | $0.06 \times 8$ | 0.48 |
| $x_{B_2,1}$ | $0.11 \times 4$ | 0.44 |
| $x_{B_2,3}$ | $0.11 \times 11$ | 1.21 |
| $x_{B_3,1}$ | $0.05 \times 7$ | 0.35 |

---

## Operational Constraints

### 1. Stage A Machine Capacity Constraints (minutes)

Converting available hours to minutes (×60):
- $A_1$: $6000 \times 60 = 360{,}000$ min
- $A_2$: $10{,}000 \times 60 = 600{,}000$ min

$$5x_{A_1,1} + 10x_{A_1,2} \leq 360{,}000 \tag{A1}$$

$$7x_{A_2,1} + 9x_{A_2,2} + 12x_{A_2,3} \leq 600{,}000 \tag{A2}$$

### 2. Stage B Machine Capacity Constraints (minutes)

- $B_1$: $4000 \times 60 = 240{,}000$ min
- $B_2$: $7000 \times 60 = 420{,}000$ min
- $B_3$: $4000 \times 60 = 240{,}000$ min

$$6x_{B_1,1} + 8x_{B_1,2} \leq 240{,}000 \tag{B1}$$

$$4x_{B_2,1} + 11x_{B_2,3} \leq 420{,}000 \tag{B2}$$

$$7x_{B_3,1} \leq 240{,}000 \tag{B3}$$

### 3. Flow Balance Constraints (Stage A output = Stage B input for each product)

Every unit of product that goes through Stage A must also go through Stage B (and vice versa). For each product $j$:

**Product I:**
$$x_{A_1,1} + x_{A_2,1} = x_{B_1,1} + x_{B_2,1} + x_{B_3,1} \tag{F1}$$

**Product II:**
$$x_{A_1,2} + x_{A_2,2} = x_{B_1,2} \tag{F2}$$
*(Product II can only use $B_1$ in Stage B)*

**Product III:**
$$x_{A_2,3} = x_{B_2,3} \tag{F3}$$
*(Product III can only use $A_2$ in Stage A and $B_2$ in Stage B)*

### 4. Non-Negativity Constraints

$$x_{A_1,1},\; x_{A_1,2},\; x_{A_2,1},\; x_{A_2,2},\; x_{A_2,3} \geq 0$$
$$x_{B_1,1},\; x_{B_1,2},\; x_{B_2,1},\; x_{B_2,3},\; x_{B_3,1} \geq 0$$

---

## Feasibility Sanity Check

**Aggregate capacity check (worst case, all machines dedicated to one product):**

- Total Stage A minutes: $360{,}000 + 600{,}000 = 960{,}000$ min
- Total Stage B minutes: $240{,}000 + 420{,}000 + 240{,}000 = 900{,}000$ min

- Product I: min 4 min (B2) + min 5 min (A1) = 9 min/unit → max ~100,000 units
- Product II: min 8 min (B1) + min 9 min (A2) = 17 min/unit → max ~52,941 units
- Product III: 11 min (B2) + 12 min (A2) = 23 min/unit → max ~39,130 units

All individual products can be produced in positive quantities. The feasible region is non-empty.

**Objective parameter cross-reference:**
| Parameter in Objective | Value | Source |
|---|---|---|
| $1.00$ (net margin I) | $1.25 - 0.25$ | Selling price − raw material |
| $1.65$ (net margin II) | $2.00 - 0.35$ | Selling price − raw material |
| $2.30$ (net margin III) | $2.80 - 0.50$ | Selling price − raw material |
| All processing cost coefficients | $c_i \times t_{ij}$ | From table |

All objective parameters are fully specified. No [NOT_PROVIDED] values remain.

**Magnitude sanity check:** A greedy solution producing ~50,000 units of Product II would yield profit on the order of $50{,}000 \times 1.65 \approx 82{,}500$ yuan minus processing costs, which is a reasonable magnitude for a factory-scale production problem. The objective units are **yuan**, matching the problem's cost/price units.