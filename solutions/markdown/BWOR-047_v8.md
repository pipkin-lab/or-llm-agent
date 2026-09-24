## MANDATORY COST INVENTORY

Before modeling, I extract every cost/parameter figure from the problem:

| # | Value | Entity Modified | Role |
|---|-------|----------------|------|
| 1 | 500 | Normal production cost per ship, Year 1 | Objective coefficient |
| 2 | 600 | Normal production cost per ship, Year 2 | Objective coefficient |
| 3 | 550 | Normal production cost per ship, Year 3 | Objective coefficient |
| 4 | +70 | Overtime premium over normal cost (all years) | Objective coefficient modifier |
| 5 | 40 | Storage/maintenance cost per ship-year of delay | Objective coefficient |
| 6 | 2 | Ships under normal production, Year 1 | Capacity bound |
| 7 | 3 | Ships under overtime production, Year 1 | Capacity bound |
| 8 | 4 | Ships under normal production, Year 2 | Capacity bound |
| 9 | 2 | Ships under overtime production, Year 2 | Capacity bound |
| 10 | 1 | Ships under normal production, Year 3 | Capacity bound |
| 11 | 3 | Ships under overtime production, Year 3 | Capacity bound |
| 12 | 3 | Ships to deliver at end of each year (Years 1, 2, 3) | Demand |
| 13 | 2 | Initial undelivered ships in stock at contract signing | Initial inventory |
| 14 | 1 | Spare ship required in storage at end of Year 3 | Final inventory requirement |

**Overtime costs derived:**
- Year 1: 500 + 70 = 570
- Year 2: 600 + 70 = 670
- Year 3: 550 + 70 = 620

All objective parameters are matched to explicit values. No [NOT_PROVIDED] needed.

---

## MODEL FORMULATION

**Model Type:** MILP (Mixed-Integer Linear Program)

### Index Sets & Parameters

**Index Set:**
- $t \in \{1, 2, 3\}$: Years (production and delivery periods)

**Parameters:**

| Symbol | Description | Value |
|--------|-------------|-------|
| $d_t$ | Ships to deliver at end of year $t$ | $d_1 = 3,\; d_2 = 3,\; d_3 = 3$ |
| $N_t$ | Max ships under normal production in year $t$ | $N_1=2,\; N_2=4,\; N_3=1$ |
| $O_t$ | Max ships under overtime production in year $t$ | $O_1=3,\; O_2=2,\; O_3=3$ |
| $c_t$ | Normal production cost per ship in year $t$ (thousand yuan) | $c_1=500,\; c_2=600,\; c_3=550$ |
| $p$ | Overtime premium per ship (thousand yuan) | $70$ |
| $h$ | Storage/maintenance cost per ship-year (thousand yuan) | $40$ |
| $I_0$ | Initial inventory of undelivered ships | $2$ |
| $I_{\text{end}}$ | Required inventory at end of year 3 | $1$ |

**Derived Parameters (overtime cost per ship in year $t$):**
- $c_t^{OT} = c_t + p$: $c_1^{OT}=570,\; c_2^{OT}=670,\; c_3^{OT}=620$

### Decision Variables

| Variable | Domain | Description |
|----------|--------|-------------|
| $x_t$ | Integer, $0 \leq x_t \leq N_t$ | Number of ships produced under **normal** production in year $t$ |
| $y_t$ | Integer, $0 \leq y_t \leq O_t$ | Number of ships produced under **overtime** production in year $t$ |
| $I_t$ | Integer, $I_t \geq 0$ | Number of ships in inventory (storage) at **end of year** $t$ |

### Objective Function

**MINIMIZE** total cost (in thousand yuan):

$$\min \sum_{t=1}^{3} \left( c_t \cdot x_t + (c_t + p) \cdot y_t + h \cdot I_t \right)$$

Expanded:

$$\min \; 500\,x_1 + 570\,y_1 + 40\,I_1 + 600\,x_2 + 670\,y_2 + 40\,I_2 + 550\,x_3 + 620\,y_3 + 40\,I_3$$

**Unit verification:** All costs are in thousand yuan per ship; storage cost is 40 thousand yuan per ship per year. The objective is in thousand yuan, matching the problem's requested unit.

### Operational Constraints

**1. Inventory Balance (Flow Conservation):**

For each year $t = 1, 2, 3$:

$$I_t = I_{t-1} + x_t + y_t - d_t$$

where $I_0 = 2$ (initial stock).

Explicitly:
- **Year 1:** $I_1 = 2 + x_1 + y_1 - 3$
- **Year 2:** $I_2 = I_1 + x_2 + y_2 - 3$
- **Year 3:** $I_3 = I_2 + x_3 + y_3 - 3$

**2. Final Inventory Requirement:**

$$I_3 = 1$$

(The shipyard must have exactly one spare ship in storage at the end of year 3.)

**3. Production Capacity Bounds:**

$$0 \leq x_t \leq N_t \quad \forall\, t \in \{1,2,3\}$$
$$0 \leq y_t \leq O_t \quad \forall\, t \in \{1,2,3\}$$

Explicitly:
- $0 \leq x_1 \leq 2,\quad 0 \leq y_1 \leq 3$
- $0 \leq x_2 \leq 4,\quad 0 \leq y_2 \leq 2$
- $0 \leq x_3 \leq 1,\quad 0 \leq y_3 \leq 3$

**4. Non-negativity of Inventory:**

$$I_t \geq 0 \quad \forall\, t \in \{1,2,3\}$$

**5. Integrality:**

$$x_t, \, y_t, \, I_t \in \mathbb{Z}_{\geq 0} \quad \forall\, t \in \{1,2,3\}$$

---

### Feasibility Sanity Check

- **Total ships required:** 3 deliveries/year × 3 years = 9 delivered + 1 spare = 10 ships needed in total (including the 2 already in stock).
- **Net new production needed:** 10 − 2 (initial stock) = 8 ships.
- **Maximum total production capacity:** $(2+3) + (4+2) + (1+3) = 5 + 6 + 4 = 15$ ships.
- Since 8 ≤ 15, the problem is **feasible**.

### Storage Interpretation Verification

The storage cost $h \cdot I_t$ is charged on the **end-of-year** inventory. A ship produced in year $s$ and delivered in year $t > s$ incurs $(t - s)$ years of storage cost, which is correctly captured because it sits in $I_s, I_{s+1}, \ldots, I_{t-1}$ (each contributing 40 thousand yuan). A ship in the final spare ($I_3$) incurs storage cost for year 3 only if it was produced before year 3, or zero additional storage if produced in year 3 (it enters $I_3$ at the end of year 3). This matches the problem statement: "each year of delay results in an additional maintenance and storage loss of 40 thousand yuan per ship."