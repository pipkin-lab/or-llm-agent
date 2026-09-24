# Mathematical Optimization Model for Shipyard Production Planning

## 1. Index Sets & Parameters

**Index Sets:**
- $t \in \{1, 2, 3\}$: Time periods (Years).
- $p \in \{N, O\}$: Production modes, where $N$ is Normal production and $O$ is Overtime production.

**Parameters (in thousand yuan and ships):**

**Demand:**
- $D_t = 3$: Ships required for delivery at the end of year $t$ for all $t \in \{1, 2, 3\}$.
- $S_{end} = 1$: Required ending inventory at the end of year 3 (spare ship).
- $I_0 = 2$: Initial inventory of undelivered ships at the start of year 1.

**Production Capacities (ships/year):**
- $Cap_{t, N}$: Maximum ships producible under normal mode in year $t$.
- $Cap_{t, O}$: Maximum ships producible under overtime mode in year $t$.

| Year ($t$) | $Cap_{t, N}$ | $Cap_{t, O}$ |
| :--- | :---: | :---: |
| 1 | 2 | 3 |
| 2 | 4 | 2 |
| 3 | 1 | 3 |

**Costs (thousand yuan/ship):**
- $C_{t, N}$: Production cost per ship under normal mode in year $t$.
- $C_{t, O}$: Production cost per ship under overtime mode in year $t$.
- $h$: Holding/storage cost per ship per year delay.

| Year ($t$) | $C_{t, N}$ | $C_{t, O}$ | Calculation Note |
| :--- | :---: | :---: | :--- |
| 1 | 500 | 570 | $500 + 70$ |
| 2 | 600 | 670 | $600 + 70$ |
| 3 | 550 | 620 | $550 + 70$ |

- $h = 40$

## 2. Decision Variables

Let $x_{t, p}$ be the number of ships produced in year $t$ using mode $p$.
Let $I_t$ be the inventory of ships at the **end** of year $t$.

**Variable Definitions & Domains:**
- $x_{t, p} \ge 0$ and integer, for all $t \in \{1, 2, 3\}$, $p \in \{N, O\}$.
  *(Note: Since ship units are discrete, these are integer variables. Given the small scale, this is a Mixed Integer Linear Program (MILP), though LP relaxation would likely yield integer solutions due to the network flow structure.)*
- $I_t \ge 0$ and integer, for all $t \in \{1, 2, 3\}$.

## 3. Objective Function

Minimize the total cost, which includes production costs and inventory holding costs.

$$
\text{Minimize } Z = \sum_{t=1}^{3} \left[ \sum_{p \in \{N, O\}} C_{t, p} x_{t, p} + h \cdot I_t \right]
$$

Substituting the specific cost values:
$$
Z = 500x_{1,N} + 570x_{1,O} + 600x_{2,N} + 670x_{2,O} + 550x_{3,N} + 620x_{3,O} + 40(I_1 + I_2 + I_3)
$$

## 4. Operational Constraints

### A. Inventory Balance Constraints
The inventory at the end of year $t$ equals the inventory at the start of year $t$, plus total production in year $t$, minus deliveries made in year $t$.

$$
I_t = I_{t-1} + \sum_{p \in \{N, O\}} x_{t, p} - D_t, \quad \forall t \in \{1, 2, 3\}
$$

Where:
- $I_0 = 2$ (Initial stock)
- $D_t = 3$ (Demand/Delivery requirement)

Explicitly written out:
1.  **Year 1:** $I_1 = 2 + x_{1,N} + x_{1,O} - 3$
2.  **Year 2:** $I_2 = I_1 + x_{2,N} + x_{2,O} - 3$
3.  **Year 3:** $I_3 = I_2 + x_{3,N} + x_{3,O} - 3$

### B. Ending Inventory Requirement
The shipyard must have exactly one spare ship in storage at the end of year 3.

$$
I_3 = 1
$$

### C. Production Capacity Constraints
Production cannot exceed the available capacity for each mode and year.

$$
x_{t, N} \le Cap_{t, N}, \quad \forall t \in \{1, 2, 3\}
$$
$$
x_{t, O} \le Cap_{t, O}, \quad \forall t \in \{1, 2, 3\}
$$

Explicitly:
- $x_{1,N} \le 2$
- $x_{1,O} \le 3$
- $x_{2,N} \le 4$
- $x_{2,O} \le 2$
- $x_{3,N} \le 1$
- $x_{3,O} \le 3$

### D. Non-negativity and Integrality
$$
x_{t, p} \in \mathbb{Z}^+, \quad \forall t, p
$$
$$
I_t \in \mathbb{Z}^+, \quad \forall t
$$

*(Note: While $I_t$ is defined as non-negative, the balance equations and the final requirement $I_3=1$ along with the initial stock ensure feasibility. The constraint $I_t \ge 0$ is standard to prevent backlogging, though the problem implies immediate delivery of produced items or existing stock, so inventory cannot go negative.)*

### Summary of Data Completeness Check
- **Demand:** 3 ships/year for 3 years + 1 ending stock. Total required = $3+3+3+1 = 10$ ships.
- **Initial Stock:** 2 ships.
- **Net Production Required:** $10 - 2 = 8$ ships total over 3 years.
- **Max Capacity:**
    - Year 1: $2+3=5$
    - Year 2: $4+2=6$
    - Year 3: $1+3=4$
    - Total Max Capacity = $15$ ships.
    - Since $8 < 15$, the problem is feasible.
- **Costs:** All normal costs, overtime premium, and holding costs are explicitly provided. No missing data.