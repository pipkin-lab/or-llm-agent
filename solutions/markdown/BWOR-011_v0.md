**Model Type:** LP (Linear Programming)

### Index Sets & Parameters

**Index Sets:**
- $S = \{I, II\}$: Set of power stations.
- $C = \{1, 2, 3\}$: Set of cities.

**Parameters:**
- $cap_s$: Maximum supply capacity of station $s$ (units).
  - $cap_I = 400$
  - $cap_{II} = 450$
- $d^{min}_j$: Minimum required supply for city $j$ (units).
  - $d^{min}_1 = 290$ (320 - 30)
  - $d^{min}_2 = 250$
  - $d^{min}_3 = 270$
- $d^{max}_j$: Maximum required supply for city $j$ (units).
  - $d^{max}_1 = 320$
  - $d^{max}_2 = 250$
  - $d^{max}_3 = 350$
- $c_{s,j}$: Unit cost of supplying electricity from station $s$ to city $j$ (Yuan/unit).
  - $c_{I,1} = 15, c_{I,2} = 18, c_{I,3} = 22$
  - $c_{II,1} = 21, c_{II,2} = 25, c_{II,3} = 16$

**Cost Inventory:**
- Cost from Station I to City 1: 15
- Cost from Station I to City 2: 18
- Cost from Station I to City 3: 22
- Cost from Station II to City 1: 21
- Cost from Station II to City 2: 25
- Cost from Station II to City 3: 16
All objective parameters are explicitly provided in Table 3-33.

### Decision Variables

Let $x_{s,j}$ be the amount of electricity (in units) supplied from station $s \in S$ to city $j \in C$.
- Domain: $x_{s,j} \ge 0$ for all $s \in S, j \in C$.
- Note: Since electricity is a continuous resource, these variables are continuous.

### Objective Function

Minimize the total cost of electricity supply.

$$
\text{Minimize } Z = \sum_{s \in S} \sum_{j \in C} c_{s,j} x_{s,j}
$$

Expanding the objective function with specific coefficients:
$$
Z = 15x_{I,1} + 18x_{I,2} + 22x_{I,3} + 21x_{II,1} + 25x_{II,2} + 16x_{II,3}
$$

### Operational Constraints

**1. Supply Capacity Constraints (Station Side)**
The total electricity supplied by each station cannot exceed its maximum capacity. Since the problem states that the plan must "use up all available electricity from both stations" and total supply ($400+450=850$) is less than or equal to the maximum possible demand ($320+250+350=920$) but greater than the minimum demand ($290+250+270=810$), we must ensure all supply is allocated. Thus, the supply constraints are equalities.

$$
\sum_{j \in C} x_{I,j} = 400
$$
$$
\sum_{j \in C} x_{II,j} = 450
$$

**2. Demand Constraints (City Side)**
The total electricity received by each city must satisfy its specific minimum and maximum requirements.

*City 1:*
$$
d^{min}_1 \le \sum_{s \in S} x_{s,1} \le d^{max}_1
$$
$$
290 \le x_{I,1} + x_{II,1} \le 320
$$

*City 2:*
$$
d^{min}_2 \le \sum_{s \in S} x_{s,2} \le d^{max}_2
$$
$$
250 \le x_{I,2} + x_{II,2} \le 250 \implies x_{I,2} + x_{II,2} = 250
$$

*City 3:*
$$
d^{min}_3 \le \sum_{s \in S} x_{s,3} \le d^{max}_3
$$
$$
270 \le x_{I,3} + x_{II,3} \le 350
$$

**3. Non-negativity**
$$
x_{s,j} \ge 0 \quad \forall s \in S, j \in C
$$

### Feasibility Sanity Check

Total Supply = $400 + 450 = 850$.
Total Minimum Demand = $290 + 250 + 270 = 810$.
Total Maximum Demand = $320 + 250 + 350 = 920$.
Since $810 \le 850 \le 920$, a feasible solution exists where all supply is used and all city minimums are met. The equality constraints on the supply side ensure that the total outflow is exactly 850, which is distributed among the cities within their respective bounds.

### Final Model Summary

**Model Type:** LP

**Minimize**
$$ Z = 15x_{I,1} + 18x_{I,2} + 22x_{I,3} + 21x_{II,1} + 25x_{II,2} + 16x_{II,3} $$

**Subject to:**

1.  **Station I Capacity:**
    $$ x_{I,1} + x_{I,2} + x_{I,3} = 400 $$
2.  **Station II Capacity:**
    $$ x_{II,1} + x_{II,2} + x_{II,3} = 450 $$
3.  **City 1 Demand:**
    $$ 290 \le x_{I,1} + x_{II,1} \le 320 $$
4.  **City 2 Demand:**
    $$ x_{I,2} + x_{II,2} = 250 $$
5.  **City 3 Demand:**
    $$ 270 \le x_{I,3} + x_{II,3} \le 350 $$
6.  **Non-negativity:**
    $$ x_{I,1}, x_{I,2}, x_{I,3}, x_{II,1}, x_{II,2}, x_{II,3} \ge 0 $$