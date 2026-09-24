# Transportation Problem Formulation

## 1. Index Sets & Parameters

**Sets:**
- $I = \{1, 2, 3\}$: Set of warehouses (corresponding to $A_1, A_2, A_3$)
- $J = \{1, 2, 3, 4, 5\}$: Set of regions (corresponding to $B_1, B_2, B_3, B_4, B_5$)

**Parameters:**
- $C_{ij}$: Total transportation and storage cost per ton from warehouse $i$ to region $j$ (given in Table 3-19).
  - $C_{11}=10, C_{12}=15, C_{13}=20, C_{14}=20, C_{15}=40$
  - $C_{21}=20, C_{22}=40, C_{23}=15, C_{24}=30, C_{25}=30$
  - $C_{31}=30, C_{32}=35, C_{33}=40, C_{34}=55, C_{35}=25$
- $S_i$: Storage capacity of warehouse $i$ (tons).
  - $S_1 = 50, S_2 = 100, S_3 = 150$
- $D_j$: Demand of region $j$ (tons).
  - $D_1 = 25, D_2 = 105, D_3 = 60, D_4 = 30, D_5 = 70$
- $P$: Maximum production capacity of the sugar factory (tons/month).
  - $P = 270$

**Data Verification:**
- Total Supply Capacity: $\sum_{i \in I} S_i = 50 + 100 + 150 = 300$ tons.
- Factory Production Limit: $270$ tons.
- Total Demand: $\sum_{j \in J} D_j = 25 + 105 + 60 + 30 + 70 = 290$ tons.

*Note on Balance:* The factory produces at most 270 tons, but total demand is 290 tons. Since the problem asks to minimize cost for a "transportation plan" and does not specify penalties for unmet demand or allow for backorders, we must check if the problem implies full satisfaction.
- If we must satisfy all demand (290), it is infeasible because max supply is 270.
- If we can only supply up to 270, we must leave 20 tons of demand unmet. However, standard textbook transportation problems of this type usually imply that the supply side is the limiting factor and we allocate the available supply to meet demand as much as possible, OR there is a typo in the problem statement regarding the production limit vs demand.
- *Re-reading carefully:* "Determine a transportation plan that minimizes the total cost." In many such problems, if Supply < Demand, the model is a "unbalanced" transportation problem where we minimize cost for the supplied amount, or we assume unmet demand has zero cost (which is non-standard) or we prioritize demand.
- *Alternative Interpretation:* Often in these specific textbook examples (likely from a Chinese OR textbook given the table format), if Production < Demand, the factory produces its maximum (270) and we distribute it. The constraint is that the total shipped cannot exceed 270. The regions will not receive their full demand. The objective is to minimize the cost of the 270 tons shipped.
- *Correction/Refinement:* Actually, looking at the numbers: Supply (Factory) = 270. Warehouse Capacity Sum = 300. Demand Sum = 290.
  The factory is the bottleneck. We can only move 270 tons total.
  Therefore, the sum of flows $x_{ij}$ will be $\le 270$.
  Since costs are positive, we will only ship if it makes sense, but typically in these problems, we assume we *want* to satisfy as much demand as possible up to the supply limit, or simply that the supply is fixed at the maximum production because there is no cost for "not producing" other than the opportunity cost which isn't modeled, or more likely, the problem implies that the 270 tons produced *must* be distributed.
  
  Let's assume the standard interpretation: The factory produces exactly 270 tons (or up to 270, but since costs are positive, we only ship what is beneficial? No, usually "produce and transport" implies the cost is incurred on the shipped amount. If we don't ship, we don't pay cost. But usually, these problems assume the supply is available and we must allocate it. Given $Supply < Demand$, we cannot satisfy everyone. We will formulate it as shipping exactly 270 tons to minimize the cost of those shipments, effectively choosing which 270 tons of the 290 tons of demand to satisfy. Since all costs are positive, we don't "throw away" sugar, we just don't produce it. Wait, if we don't produce it, we don't pay the transport cost. So the objective is simply to minimize the cost of the goods shipped. We are free to ship any amount $\le 270$. However, usually, "sugar factory... can produce up to..." combined with specific demands implies we should satisfy demand if possible. Here it is not possible.
  
  *Standard Model Approach for Supply < Demand:*
  We define $x_{ij}$ as the amount shipped from $i$ to $j$.
  Constraints:
  1. Warehouse capacity: $\sum_j x_{ij} \le S_i$
  2. Factory capacity: $\sum_{i,j} x_{ij} \le P$
  3. Demand: $\sum_i x_{ij} \le D_j$ (We cannot exceed demand, and we cannot exceed supply).
  
  Since all $C_{ij} > 0$, the optimal solution will maximize the amount shipped if there is a "revenue" not modeled, OR simply minimize cost for a *required* amount. However, without a revenue term, minimizing cost would result in shipping 0 tons (Cost = 0). This is trivial and incorrect.
  
  Therefore, the implicit assumption in such problems is that **all produced sugar must be sold/shipped**, or **we must satisfy the maximum possible demand**. Given the context of "Determine a transportation plan", it implies a full allocation of the available supply (270 tons) to the regions. We assume the factory produces 270 tons and all 270 tons must be distributed.

## 2. Decision Variables

Let $x_{ij}$ be the amount of sugar (tons) transported from warehouse $i \in I$ to region $j \in J$.
Domain: $x_{ij} \ge 0$ (Continuous, as tons of sugar are divisible).

## 3. Objective Function

Minimize the total transportation cost $Z$:

$$
\min Z = \sum_{i \in I} \sum_{j \in J} C_{ij} x_{ij}
$$

Subject to the data:
$$
Z = 10x_{11} + 15x_{12} + 20x_{13} + 20x_{14} + 40x_{15} \\
+ 20x_{21} + 40x_{22} + 15x_{23} + 30x_{24} + 30x_{25} \\
+ 30x_{31} + 35x_{32} + 40x_{33} + 55x_{34} + 25x_{35}
$$

## 4. Operational Constraints

**1. Warehouse Capacity Constraints (Supply Side):**
The total amount shipped from each warehouse cannot exceed its storage capacity.
$$
\sum_{j \in J} x_{ij} \le S_i, \quad \forall i \in I
$$
Expanded:
1. $x_{11} + x_{12} + x_{13} + x_{14} + x_{15} \le 50$
2. $x_{21} + x_{22} + x_{23} + x_{24} + x_{25} \le 100$
3. $x_{31} + x_{32} + x_{33} + x_{34} + x_{35} \le 150$

**2. Factory Production Constraint (Global Supply Limit):**
The total amount shipped from all warehouses cannot exceed the factory's production capacity.
$$
\sum_{i \in I} \sum_{j \in J} x_{ij} \le P
$$
$$
\sum_{i \in I} \sum_{j \in J} x_{ij} \le 270
$$
*(Note: Since the sum of warehouse capacities is 300 > 270, this constraint is tighter than the individual warehouse sums combined. It ensures we don't pull more than the factory can make.)*

**3. Regional Demand Constraints (Demand Side):**
The total amount received by each region cannot exceed its demand.
$$
\sum_{i \in I} x_{ij} \le D_j, \quad \forall j \in J
$$
Expanded:
1. $x_{11} + x_{21} + x_{31} \le 25$
2. $x_{12} + x_{22} + x_{32} \le 105$
3. $x_{13} + x_{23} + x_{33} \le 60$
4. $x_{14} + x_{24} + x_{34} \le 30$
5. $x_{15} + x_{25} + x_{35} \le 70$

**4. Non-negativity Constraints:**
$$
x_{ij} \ge 0, \quad \forall i \in I, j \in J
$$

---

### Analysis of Balance & Objective Implicitness
As noted, Total Demand (290) > Total Supply (270).
In a pure minimization problem with $\le$ constraints on supply and demand, the trivial solution is $x_{ij}=0$ for all $i,j$ with $Z=0$.
To make this a meaningful transportation problem where we "determine a plan", we must assume that **the factory produces 270 tons and all of it must be shipped**. Therefore, the factory constraint becomes an equality:
$$
\sum_{i \in I} \sum_{j \in J} x_{ij} = 270
$$
Alternatively, this can be modeled by adding a dummy region $B_6$ with demand $290 - 270 = 20$ tons and zero cost from all warehouses to it, effectively "discarding" the 20 tons of unmet demand at no cost. However, since the costs are "transportation and storage", discarding might not be free. But usually, "unmet demand" is just not served.
Given the prompt asks to minimize cost, and usually these problems imply satisfying the supply, we will stick to the interpretation: **Ship exactly 270 tons.**

If we assume we *must* satisfy as much demand as possible (which is 270), the constraint is $\sum x = 270$.

**Final Model Summary:**

**Objective:**
$$ \min Z = \sum_{i=1}^3 \sum_{j=1}^5 c_{ij} x_{ij} $$

**Subject to:**
1. $\sum_{j=1}^5 x_{1j} \le 50$
2. $\sum_{j=1}^5 x_{2j} \le 100$
3. $\sum_{j=1}^5 x_{3j} \le 150$
4. $\sum_{i=1}^3 x_{i1} \le 25$
5. $\sum_{i=1}^3 x_{i2} \le 105$
6. $\sum_{i=1}^3 x_{i3} \le 60$
7. $\sum_{i=1}^3 x_{i4} \le 30$
8. $\sum_{i=1}^3 x_{i5} \le 70$
9. $\sum_{i=1}^3 \sum_{j=1}^5 x_{ij} = 270$  *(Assuming full production is shipped)*
10. $x_{ij} \ge 0$