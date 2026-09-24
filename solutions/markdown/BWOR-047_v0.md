# Mathematical Model for Shipyard Production Planning

## Model Type Declaration
**Model Type:** MILP (Mixed-Integer Linear Programming)
**Reason:** Ships are discrete units (integer variables), and all objective/constraint terms are linear.

## Index Sets & Parameters

### Index Sets
- $T = \{1, 2, 3\}$: Set of years (planning horizon).

### Parameters
| Parameter | Symbol | Value | Unit | Source |
| :--- | :--- | :--- | :--- | :--- |
| Demand per year | $D_t$ | 3 | ships/year | "deliver three identical large cargo ships at the end of each of the next three years" |
| Normal production capacity | $N_t$ | $[2, 4, 1]$ | ships/year | Table 3-20, "Ships under normal production" |
| Overtime production capacity | $O_t$ | $[3, 2, 3]$ | ships/year | Table 3-20, "Ships under overtime production" |
| Normal production cost | $c_t^N$ | $[500, 600, 550]$ | thousand yuan/ship | Table 3-20, "Cost per ship (normal)" |
| Overtime cost premium | $\Delta c$ | 70 | thousand yuan/ship | "cost per ship is 70 thousand yuan higher than under normal production" |
| Overtime production cost | $c_t^O$ | $[570, 670, 620]$ | thousand yuan/ship | $c_t^N + \Delta c$ |
| Storage cost | $h$ | 40 | thousand yuan/ship-year | "each year of delay results in an additional maintenance and storage loss of 40 thousand yuan per ship" |
| Initial inventory | $I_0$ | 2 | ships | "shipyard already has two undelivered ships in stock" |
| Final inventory requirement | $I_{final}$ | 1 | ship | "wishes to have one spare ship in storage at the end of the third year" |

**Cost Inventory (Mandatory Pre-Modeling Step):**
1.  Normal costs: Year 1 = 500, Year 2 = 600, Year 3 = 550.
2.  Overtime premium: 70 (applies to all years).
3.  Storage cost: 40 per ship-year.
4.  All objective parameters are explicitly defined in the text/table. No `[NOT_PROVIDED]` values.

## Decision Variables

Let the following be the decision variables for each year $t \in T$:

- $x_t^N$: Number of ships produced in year $t$ under **normal** production.
- $x_t^O$: Number of ships produced in year $t$ under **overtime** production.
- $I_t$: Number of ships in inventory (storage) at the **end** of year $t$.

**Domains:**
- $x_t^N \in \mathbb{Z}_{\ge 0}$ for all $t \in T$
- $x_t^O \in \mathbb{Z}_{\ge 0}$ for all $t \in T$
- $I_t \in \mathbb{Z}_{\ge 0}$ for all $t \in T$

*(Note: Variables are integer because ships are discrete physical units.)*

## Objective Function

Minimize the total cost, which includes production costs (normal + overtime) and storage holding costs for ships carried over from previous years.

$$
\text{Minimize } Z = \sum_{t=1}^{3} \left( c_t^N x_t^N + c_t^O x_t^O + h I_{t-1} \right)
$$

Substituting the numeric values:
$$
\text{Minimize } Z = (500 x_1^N + 570 x_1^O) + (600 x_2^N + 670 x_2^O) + (550 x_3^N + 620 x_3^O) + 40(I_0 + I_1 + I_2)
$$

*Clarification on Storage Cost Timing:*
The problem states "each year of delay results in an additional... loss". A ship produced in year $t$ and stored for delivery in year $t+1$ incurs 1 year of storage cost. This cost is associated with the inventory level $I_t$ (end of period $t$) being held during the next period. Alternatively, we can model it as the cost of holding inventory $I_{t-1}$ during year $t$.
Let's refine the storage term.
- Ships in $I_0$ (start of Year 1) are held during Year 1. If delivered in Year 1, they incur 0 delay? No, "delay" implies they were produced before the delivery year.
- Let's look at the standard interpretation: "produced but not delivered in the same year... each year of delay... 40".
    - A ship produced in Year 1 and delivered in Year 2 has 1 year of delay.
    - A ship in $I_0$ (existing stock) delivered in Year 1: Was it "produced but not delivered in the same year" in Year 0? Yes. Does it incur storage cost in Year 1? The problem says "At the time of contract signing... already has two undelivered ships". Usually, existing inventory incurs holding costs if held, but the specific clause "produced but not delivered in the same year" applies to *new* production. However, standard inventory models charge holding cost on the average or ending inventory.
    - Let's stick to the most robust interpretation: Holding cost $h$ is incurred for each ship in the inventory $I_t$ at the end of year $t$. Why? Because $I_t$ represents ships that were NOT delivered in year $t$ (or earlier) and must be held for future years.
    - Actually, let's trace a specific ship.
        - Produced Year 1, Delivered Year 1: Cost $c_1$. Storage: 0.
        - Produced Year 1, Delivered Year 2: Cost $c_1$. It was in $I_1$. It incurred 1 year of storage.
        - Produced Year 1, Delivered Year 3: Cost $c_1$. It was in $I_1$ and $I_2$. It incurred 2 years of storage.
    - Therefore, the total storage cost is $h \times \sum_{t=1}^{3} I_t$.
    - What about $I_0$? The 2 ships in stock are "undelivered". If delivered in Year 1, do they incur storage cost? The text says "if a ship is produced but not delivered in the same year". The $I_0$ ships were produced in Year 0 (or earlier). They were not delivered in Year 0 (presumably). So they have already accumulated delay. However, usually, in such problems, the holding cost is for the *future* storage. Let's assume the 40k is charged for each year a ship sits in the yard *after* production.
    - If a ship from $I_0$ is delivered in Year 1, it has been sitting there. Does it cost 40? The prompt says "each year of delay results in... 40".
    - Let's assume the standard inventory balance cost: $h \sum_{t=1}^{3} I_t$. This charges 40 for each ship in $I_1$ (held from end of Y1 to start of Y2), and 40 for each ship in $I_2$ (held from end of Y2 to start of Y3).
    - Does $I_0$ incur a cost in Year 1? If we charge $h I_0$, it means we pay 40 for the ships already there. Given the ambiguity, the most standard formulation for "storage loss" in production planning is $h \sum I_t$ where $I_t$ is the end-of-period inventory. Let's verify with the "delay" wording. "Produced... not delivered in same year".
        - Ship produced Y1, delivered Y2: 1 delay year. In $I_1$. Cost 40.
        - Ship produced Y1, delivered Y3: 2 delay years. In $I_1, I_2$. Cost 80.
        - Ship in $I_0$ delivered Y1: Produced Y0? Not delivered Y0? 1 delay year? If so, it should incur cost. But $I_0$ is a parameter, not a decision. Usually, costs associated with initial inventory are either sunk or included in the holding cost of the first period. Let's look at the wording again: "if a ship is produced but not delivered in the same year... 40... per ship". This implies the cost is triggered by the *act* of producing early.
        - If I produce in Year 1 and deliver in Year 2, I pay 40.
        - If I take an existing ship (Year 0) and deliver in Year 1, did I produce it in Year 0? Yes. Was it not delivered in Year 0? Yes. So it has 1 year of delay. Should I pay 40?
        - Often, initial inventory costs are not penalized in the objective function of the *planning* period unless specified as "holding cost for initial inventory". However, "storage loss" suggests an ongoing cost.
        - Let's assume the cost is $h \sum_{t=1}^{3} I_t$. This is the standard interpretation for "end-of-period inventory holding cost". If the problem meant to charge for $I_0$, it would typically say "holding cost of 40 per ship per year". The phrase "produced but not delivered in the same year" links the cost to the production decision.
        - *Decision:* I will include storage costs for $I_1, I_2, I_3$. $I_3$ is the final inventory (1 ship). Does it incur storage cost? It is stored "at the end of the third year". It will be stored for Year 4. The contract ends. The requirement is to *have* it. The cost of storing it *during* Year 3 (if produced in Year 3) is 0 delay. If produced in Year 2, it's in $I_2$ (1 delay). If produced in Year 1, it's in $I_1, I_2$ (2 delays).
        - So, Storage Cost = $40 (I_1 + I_2 + I_3)$?
        - Let's check $I_3$. If a ship is produced in Year 3 and kept as spare, it was produced and not delivered (delivered to contract) in Year 3. It is held for the future. Does it incur 1 year of storage cost immediately? "each year of delay". If it's produced in Y3 and held for Y4, that is 1 year of delay relative to production. So yes, $I_3$ should likely incur cost.
        - So Objective Storage Term: $40 (I_1 + I_2 + I_3)$.
        - What about $I_0$? The 2 ships are already there. They are "undelivered". If delivered in Y1, they have been delayed from Y0. Do we pay 40? The problem asks to minimize cost *of the plan*. The 40k is a "loss". If it has already happened, it's sunk. If it happens during the planning horizon, it's a cost. The 2 ships are in stock *now*. If we use them in Year 1, we avoid producing them. If we don't use them, we store them.
        - Let's assume the 40k is charged for each year a ship is in the *planning horizon's* inventory $I_t$ ($t=1..3$). This is the safest standard assumption.

**Revised Objective Function:**
$$
\text{Minimize } Z = \sum_{t=1}^{3} (500 x_t^N + c_t^O x_t^O) + 40 \sum_{t=1}^{3} I_t
$$
Where:
- $c_1^O = 570, c_2^O = 670, c_3^O = 620$.

## Operational Constraints

1.  **Capacity Constraints:**
    Production cannot exceed available capacity.
    -   $x_1^N \le 2$
    -   $x_2^N \le 4$
    -   $x_3^N \le 1$
    -   $x_1^O \le 3$
    -   $x_2^O \le 2$
    -   $x_3^O \le 3$

2.  **Inventory Balance Constraints:**
    For each year $t \in \{1, 2, 3\}$:
    $$ I_{t-1} + x_t^N + x_t^O - I_t = D_t $$
    Where $D_t = 3$ for all $t$.
    
    Expanded:
    -   **Year 1:** $I_0 + x_1^N + x_1^O - I_1 = 3 \implies 2 + x_1^N + x_1^O - I_1 = 3$
    -   **Year 2:** $I_1 + x_2^N + x_2^O - I_2 = 3$
    -   **Year 3:** $I_2 + x_3^N + x_3^O - I_3 = 3$

3.  **Final Inventory Requirement:**
    The shipyard wishes to have one spare ship in storage at the end of the third year.
    $$ I_3 = 1 $$

4.  **Non-negativity and Integrality:**
    $$ x_t^N, x_t^O, I_t \in \mathbb{Z}_{\ge 0} \quad \forall t \in \{1, 2, 3\} $$

## Feasibility Sanity Check

-   **Total Demand:** $3 \text{ years} \times 3 \text{ ships/year} = 9$ ships for delivery.
-   **Final Inventory Requirement:** 1 ship.
-   **Total Ships Needed (Delivered + Final Stock):** $9 + 1 = 10$ ships.
-   **Initial Inventory:** 2 ships.
-   **Total Production Required:** $10 - 2 = 8$ ships.
-   **Total Available Production Capacity:**
    -   Year 1: $2 + 3 = 5$
    -   Year 2: $4 + 2 = 6$
    -   Year 3: $1 + 3 = 4$
    -   Total Capacity = $5 + 6 + 4 = 15$ ships.
-   Since Total Capacity (15) > Total Production Required (8), the problem is feasible.

## Summary of Model

**Model Type:** MILP

**Sets:** $T = \{1, 2, 3\}$

**Parameters:**
-   $D = [3, 3, 3]$
-   $Cap^N = [2, 4, 1]$
-   $Cap^O = [3, 2, 3]$
-   $Cost^N = [500, 600, 550]$
-   $Cost^O = [570, 670, 620]$
-   $H = 40$
-   $I_0 = 2$
-   $I_{final} = 1$

**Variables:**
-   $x_t^N \in \mathbb{Z}_{\ge 0}$
-   $x_t^O \in \mathbb{Z}_{\ge 0}$
-   $I_t \in \mathbb{Z}_{\ge 0}$

**Objective:**
$$ \min Z = \sum_{t=1}^3 (Cost^N_t x_t^N + Cost^O_t x_t^O) + 40 \sum_{t=1}^3 I_t $$

**Constraints:**
1.  $x_t^N \le Cap^N_t, \quad x_t^O \le Cap^O_t \quad \forall t$
2.  $I_{t-1} + x_t^N + x_t^O - I_t = 3 \quad \forall t$ (with $I_0=2$)
3.  $I_3 = 1$
4.  $x, I \ge 0$ integers