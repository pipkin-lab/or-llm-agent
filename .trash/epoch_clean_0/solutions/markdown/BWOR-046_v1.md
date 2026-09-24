# Transportation Problem: Sugar Factory to Regions via Warehouses

## 1. Index Sets & Parameters

**Sets:**
- $I = \{1, 2, 3\}$: Set of warehouses (A1, A2, A3).
- $J = \{1, 2, 3, 4, 5\}$: Set of demand regions (B1, B2, B3, B4, B5).

**Parameters:**
- $S$: Total supply from the sugar factory = $270$ tons.
- $W_i$: Maximum storage capacity of warehouse $i$ (tons).
  - $W_1 = 50$
  - $W_2 = 100$
  - $W_3 = 150$
- $D_j$: Demand of region $j$ (tons).
  - $D_1 = 25$
  - $D_2 = 105$
  - $D_3 = 60$
  - $D_4 = 30$
  - $D_5 = 70$
- $C_{ij}$: Transportation and storage cost (cost units) to transport 1 ton from warehouse $i$ to region $j$.
  - Row A1: $[10, 15, 20, 20, 40]$
  - Row A2: $[20, 40, 15, 30, 30]$
  - Row A3: $[30, 35, 40, 55, 25]$

**Derived Check:**
- Total Supply $S = 270$.
- Total Demand $\sum D_j = 25 + 105 + 60 + 30 + 70 = 290$.
- Total Warehouse Capacity $\sum W_i = 50 + 100 + 150 = 300$.
- Note: Total Demand (290) > Total Supply (270). The problem is supply-constrained. Since the factory produces "up to" 270 tons, we assume all 270 tons must be shipped to meet as much demand as possible, or that unmet demand is penalized. However, standard transportation problems usually assume supply = demand or allow surplus/deficit. Given the specific phrasing "Determine a transportation plan... minimizes total cost" and the fact that supply < demand, we must model **unmet demand** or assume the factory ships exactly its capacity and some demand is not met.
- *Correction/Refinement*: In many textbook formulations of this type where Supply < Demand, if no penalty for unmet demand is given, it is often implied that the supply is the limiting factor and we maximize satisfied demand or minimize cost for the shipped amount. However, a more standard interpretation for "minimize cost" with Supply < Demand and no explicit penalty is that we cannot satisfy all demand. Usually, this implies we ship all available supply (270) to minimize the cost of the *shipped* goods, but this leaves 20 tons of demand unmet.
- *Alternative Interpretation*: Does "production up to 270" mean we can produce less? If we produce less, we save production cost? No production cost is given, only transportation/storage cost. Usually, in such problems, if no production cost is given, we assume we utilize the full capacity to serve demand because "not producing" doesn't save a stated cost, but "not shipping" saves shipping cost. However, failing to meet demand is usually a violation.
- Let's look at the constraints again. Warehouse capacities sum to 300. Factory supply is 270. Demand is 290.
- If we must satisfy all demand, it's infeasible ($290 > 270$).
- Therefore, the model **must** allow for unmet demand or assume the factory can produce *at most* 270 and we choose how much to produce/ship.
- Since no production cost is listed, but there is a "transportation and storage cost", it is rational to ship as much as possible if the marginal cost of shipping is positive? No, if we don't have to ship, we don't pay the cost. But we have "Demand".
- Standard OR convention for "Minimize Cost" with Supply < Demand:
  1. Either the problem implies Demand is a *maximum* (unlikely given the word "demand").
  2. Or there is a penalty for unmet demand (not given).
  3. Or, most likely in this specific textbook context, the "Supply" is the hard constraint on outflow from the source, and we are distributing the 270 tons to the 5 regions. The "Demand" figures represent the *maximum* acceptable amount or the *required* amount? If required, the problem is infeasible.
  4. Let's re-read carefully: "The demand in each region is...". This usually implies a lower bound. If infeasible, did I sum wrong? $25+105+60+30+70 = 290$. Supply 270.
  5. Is it possible that the warehouse capacities are the supply? No, "sugar is first transported to three warehouses... storage capacities...". The factory produces 270.
  6. Let's assume the standard **Balanced Transportation Problem** structure is expected, but since it's unbalanced, we typically add a "Dummy" destination or source. Here, Source (Factory) < Demand. So we have a **Deficit** at the destination.
  7. If no penalty is given for unmet demand, the objective function would simply minimize the cost of the units *actually shipped*. The constraints would be:
     - Outflow from Factory = Sum of inflows to Warehouses <= 270.
     - Inflow to Region $j$ <= $D_j$ (Demand is a cap).
     - This models "Meet demand up to the requested amount, minimizing shipping cost". This is a standard interpretation when Supply < Demand and no penalty is specified: you serve the cheapest demands first up to the supply limit.
     - *However*, "Demand" usually means a requirement. If it's a requirement, the problem is infeasible.
     - Let's check if "Demand" implies "Maximum Demand" (i.e., potential market size). In many logistics problems, "Demand" is the upper limit of what *can* be sold, and you want to ship to minimize cost while maximizing profit? No, objective is just minimize cost.
     - Let's assume the standard LP interpretation: **Supply Constraint** is binding. **Demand Constraints** are upper bounds (you can't ship more than the market wants). We ship all 270 tons (since shipping has a cost, but presumably the "product" is already made or the "cost" includes the variable production cost which is linear? No, "transportation and storage costs" are given. If production cost is fixed, we produce 270. If production cost is variable, we might produce less. Without production cost, the cost of "not shipping" is 0. The cost of shipping is $C_{ij}$. Minimizing cost would lead to shipping 0 tons if demand is an upper bound. This contradicts the goal of a "transportation plan".
     - *Most Likely Intent*: The problem assumes **Demand is a lower bound** (must be met) and there is a typo in the numbers, OR **Supply is >= Demand**. Let's re-add. 25+105=130. 130+60=190. 190+30=220. 220+70=290. Supply 270.
     - Given the strict instruction to model the problem as described, and the infeasibility of meeting all demand with the given supply, I will model it as a **Min-Cost Flow** where:
       - The factory supplies $S=270$.
       - The regions have demand $D_j$.
       - Since $S < \sum D_j$, we cannot satisfy all demand.
       - In the absence of a penalty for unmet demand, the standard mathematical formulation for "Minimize Transportation Cost" subject to Supply and Demand usually requires balancing.
       - **Assumption**: The "Demand" values are the **maximum** amounts that can be accepted by each region (market size). We must allocate the 270 tons of supply to these regions to minimize cost. Since we are minimizing cost, and all costs are positive, we would prefer to ship 0. This implies there is an implicit constraint that we **must ship all available supply** (e.g., production is already committed or sunk).
       - Therefore:
         - $\sum_{j} x_{ij} \le W_i$ (Warehouse capacity)
         - $\sum_{i} x_{ij} \le D_j$ (Region demand cap)
         - $\sum_{i} \sum_{j} x_{ij} = 270$ (All produced sugar must be distributed)
         - Minimize $\sum C_{ij} x_{ij}$

## 2. Decision Variables

Let $x_{ij}$ be the amount of sugar (in tons) transported from warehouse $i$ to region $j$.

**Domain:**
$x_{ij} \ge 0$ for all $i \in I, j \in J$.
(Continuous variables are appropriate for tons of sugar).

## 3. Objective Function

Minimize the total transportation and storage cost:

$$ \text{Minimize } Z = \sum_{i \in I} \sum_{j \in J} C_{ij} x_{ij} $$

Expanding the coefficients:
$$ Z = 10x_{11} + 15x_{12} + 20x_{13} + 20x_{14} + 40x_{15} + 20x_{21} + 40x_{22} + 15x_{23} + 30x_{24} + 30x_{25} + 30x_{31} + 35x_{32} + 40x_{33} + 55x_{34} + 25x_{35} $$

## 4. Operational Constraints

**1. Warehouse Capacity Constraints:**
The total amount of sugar sent from each warehouse cannot exceed its storage capacity. Note: The sugar passes *through* the warehouses. The capacity limits the throughput/storage at that node.
$$ \sum_{j=1}^{5} x_{1j} \le 50 \quad (\text{Warehouse A}_1) $$
$$ \sum_{j=1}^{5} x_{2j} \le 100 \quad (\text{Warehouse A}_2) $$
$$ \sum_{j=1}^{5} x_{3j} \le 150 \quad (\text{Warehouse A}_3) $$

**2. Region Demand Constraints:**
The total amount of sugar received by each region cannot exceed its stated demand (interpreted as market capacity/maximum acceptable volume).
$$ \sum_{i=1}^{3} x_{i1} \le 25 \quad (\text{Region B}_1) $$
$$ \sum_{i=1}^{3} x_{i2} \le 105 \quad (\text{Region B}_2) $$
$$ \sum_{i=1}^{3} x_{i3} \le 60 \quad (\text{Region B}_3) $$
$$ \sum_{i=1}^{3} x_{i4} \le 30 \quad (\text{Region B}_4) $$
$$ \sum_{i=1}^{3} x_{i5} \le 70 \quad (\text{Region B}_5) $$

**3. Supply Constraint (Factory Production):**
The total amount of sugar distributed from the system must equal the factory's production output. Since the factory produces "up to 270" and we assume all produced sugar is shipped (to avoid the trivial solution of shipping nothing, and assuming production is committed or the "cost" of production is fixed/sunk), the sum of all flows equals the supply.
$$ \sum_{i=1}^{3} \sum_{j=1}^{5} x_{ij} = 270 $$

**4. Non-negativity:**
$$ x_{ij} \ge 0 \quad \forall i \in \{1,2,3\}, j \in \{1,2,3,4,5\} $$

***

**Note on Feasibility and Interpretation:**
Total Demand ($290$) exceeds Total Supply ($270$). The formulation above treats "Demand" as an upper bound (maximum sellable amount) and enforces that all 270 tons of supply are shipped. The solver will determine which 270 tons of the 290 potential demand to fulfill in the most cost-effective manner. If the problem intended "Demand" to be a strict lower bound, the problem would be infeasible. Given the context of minimization without unmet-demand penalties, the "maximum demand" interpretation is the standard viable model.