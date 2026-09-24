## Model Type Declaration
**MILP (Mixed Integer Linear Program)**
*Note: Since the supplies and demands are integers, the optimal solution will naturally have integer values for a standard transportation problem structure, but formally, decision variables representing discrete units of goods are defined as integers to ensure physical validity.*

## Index Sets & Parameters

**Sets:**
- $I = \{1, 2, 3\}$: Set of origins (supply nodes)
- $J = \{A, B, C\}$: Set of destinations (demand nodes)

**Parameters (from Table 3-17 and problem statement):**

**Transportation Costs ($c_{ij}$):**
| $i \setminus j$ | A | B | C |
| :--- | :---: | :---: | :---: |
| **1** | 1 | 2 | 2 |
| **2** | 1 | 4 | 5 |
| **3** | 2 | 3 | 3 |

**Supply Capacities ($S_i$):**
- $S_1 = 20$
- $S_2 = 40$
- $S_3 = 30$
- Total Supply = $90$

**Demands ($D_j$):**
- $D_A = 30$
- $D_B = 20$
- $D_C = 20$
- Total Demand = $70$

**Unit Storage Costs ($s_i$) for unshipped goods:**
- $s_1 = 5$
- $s_2 = 4$
- $s_3 = 3$

**Minimum Shipping Requirements:**
- Min shipped from Origin 2: $M_2 = 38$
- Min shipped from Origin 3: $M_3 = 27$
- Min shipped from Origin 1: $M_1 = 0$ (No specific minimum stated, implied 0)

## Decision Variables

Let $x_{ij}$ be the number of units shipped from origin $i$ to destination $j$.
- **Domain:** $x_{ij} \in \mathbb{Z}^{\ge 0}$ for all $i \in I, j \in J$.

Let $y_i$ be the number of units stored (not shipped) at origin $i$.
- **Domain:** $y_i \in \mathbb{Z}^{\ge 0}$ for all $i \in I$.

## Objective Function

Minimize the total cost, which includes transportation costs for shipped units and storage costs for unshipped units.

$$
\text{Minimize } Z = \sum_{i \in I} \sum_{j \in J} c_{ij} x_{ij} + \sum_{i \in I} s_i y_i
$$

Expanding with specific parameters:

$$
Z = (1x_{1A} + 2x_{1B} + 2x_{1C}) + (1x_{2A} + 4x_{2B} + 5x_{2C}) + (2x_{3A} + 3x_{3B} + 3x_{3C}) + (5y_1 + 4y_2 + 3y_3)
$$

## Operational Constraints

**1. Supply Balance Constraints:**
The amount shipped from an origin plus the amount stored cannot exceed the total supply available at that origin.
$$
\sum_{j \in J} x_{ij} + y_i \le S_i \quad \forall i \in I
$$
- $x_{1A} + x_{1B} + x_{1C} + y_1 \le 20$
- $x_{2A} + x_{2B} + x_{2C} + y_2 \le 40$
- $x_{3A} + x_{3B} + x_{3C} + y_3 \le 30$

**2. Demand Satisfaction Constraints:**
The total amount received at each destination must exactly meet the demand.
$$
\sum_{i \in I} x_{ij} = D_j \quad \forall j \in J
$$
- $x_{1A} + x_{2A} + x_{3A} = 30$
- $x_{1B} + x_{2B} + x_{3B} = 20$
- $x_{1C} + x_{2C} + x_{3C} = 20$

**3. Minimum Shipping Constraints:**
The total amount shipped from specific origins must meet the minimum requirements.
$$
\sum_{j \in J} x_{ij} \ge M_i \quad \forall i \in I
$$
- $x_{1A} + x_{1B} + x_{1C} \ge 0$
- $x_{2A} + x_{2B} + x_{2C} \ge 38$
- $x_{3A} + x_{3B} + x_{3C} \ge 27$

**4. Non-negativity and Integrality:**
- $x_{ij} \in \mathbb{Z}^{\ge 0}$ for all $i, j$
- $y_i \in \mathbb{Z}^{\ge 0}$ for all $i$

## Feasibility Sanity Check

**Total Supply vs. Total Demand + Minimums:**
- Total Demand = 70.
- Total Supply = 90.
- Excess Supply = 20 (this will be stored).
- Minimum Shipments required:
  - Origin 2: at least 38.
  - Origin 3: at least 27.
  - Sum of min shipments for 2 & 3 = 65.
  - Remaining demand to be met by Origin 1 = $70 - 65 = 5$ (minimum).
  - Max possible shipment from Origin 1 is 20.
  - Let's check if we can satisfy demands with these minimums.
    - If $Shipped_2 = 38$ and $Shipped_3 = 27$, total shipped so far = 65.
    - Remaining demand = 5. This must come from Origin 1.
    - $Shipped_1 \ge 5$.
    - Is $Shipped_1 \le 20$? Yes.
    - Is $Shipped_2 \le 40$? Yes ($38 \le 40$).
    - Is $Shipped_3 \le 30$? **Wait.** The supply at Origin 3 is 30. The minimum shipment from Origin 3 is 27. This is feasible ($27 \le 30$).
    - However, we must check if the *combination* of minimums allows satisfying the specific destination demands.
    - Demand A=30, B=20, C=20.
    - Let's verify if a feasible flow exists.
      - Try min constraints: Ship 38 from 2, 27 from 3.
      - Origin 3 supply is 30, so it can ship max 30. Min is 27.
      - Origin 2 supply is 40, min 38.
      - Origin 1 supply is 20.
      - Total shipped must be 70.
      - $Shipped_1 + Shipped_2 + Shipped_3 = 70$.
      - We know $Shipped_2 \ge 38$ and $Shipped_3 \ge 27$.
      - Min sum of $Shipped_2 + Shipped_3 = 65$.
      - Therefore $Shipped_1 \le 70 - 65 = 5$.
      - Also $Shipped_1 \le 20$.
      - So $Shipped_1 \in [0, 5]$? No, $Shipped_1$ is determined by the others.
      - Actually, $Shipped_1 = 70 - Shipped_2 - Shipped_3$.
      - Since $Shipped_2 \le 40$ and $Shipped_3 \le 30$, max $Shipped_2+Shipped_3 = 70$.
      - If $Shipped_2=40, Shipped_3=30$, then $Shipped_1=0$.
      - If $Shipped_2=38, Shipped_3=27$, then $Shipped_1=5$.
      - So feasible range for shipments is tight but exists.
      - Specifically, check Origin 3 constraint: $Shipped_3 \le 30$ (Supply) AND $Shipped_3 \ge 27$ (Min). Feasible.
      - Check Origin 2 constraint: $Shipped_2 \le 40$ (Supply) AND $Shipped_2 \ge 38$ (Min). Feasible.
      - Check Origin 1 constraint: $Shipped_1 \le 20$ (Supply).
      - Since $Shipped_1 = 70 - Shipped_2 - Shipped_3$, and min $Shipped_2+Shipped_3 = 65$, max $Shipped_1 = 5$.
      - Since max $Shipped_2+Shipped_3 = 70$, min $Shipped_1 = 0$.
      - So $Shipped_1$ will be between 0 and 5. This is within its supply limit of 20.
      - The model is feasible.