# Transportation Problem Formulation

## 1. Index Sets & Parameters

### Index Sets
- $I = \{1, 2, 3\}$: Set of warehouses (indexed by $i$).
- $J = \{1, 2, 3, 4, 5\}$: Set of regions (indexed by $j$).

### Parameters
- **Production Capacity**:
  - $S_{max} = 270$ tons/month (Total maximum output from the sugar factory).
- **Warehouse Capacities** ($C_i$ for $i \in I$):
  - $C_1 = 50$ tons
  - $C_2 = 100$ tons
  - $C_3 = 150$ tons
- **Regional Demands** ($D_j$ for $j \in J$):
  - $D_1 = 25$ tons
  - $D_2 = 105$ tons
  - $D_3 = 60$ tons
  - $D_4 = 30$ tons
  - $D_5 = 70$ tons
- **Unit Transportation Costs** ($c_{ij}$ for $i \in I, j \in J$):
  - From Warehouse $A_1$: $c_{1,1}=10, c_{1,2}=15, c_{1,3}=20, c_{1,4}=20, c_{1,5}=40$
  - From Warehouse $A_2$: $c_{2,1}=20, c_{2,2}=40, c_{2,3}=15, c_{2,4}=30, c_{2,5}=30$
  - From Warehouse $A_3$: $c_{3,1}=30, c_{3,2}=35, c_{3,3}=40, c_{3,4}=55, c_{3,5}=25$

### Feasibility Check
- Total Warehouse Capacity: $50 + 100 + 150 = 300$ tons.
- Total Regional Demand: $25 + 105 + 60 + 30 + 70 = 290$ tons.
- Factory Capacity: $270$ tons.
- Since Total Demand ($290$) > Factory Capacity ($270$), the problem is **infeasible** under strict demand satisfaction constraints. However, in standard transportation problem formulations, we typically assume the system is balanced or that "demand" represents maximum allowable supply if capacity is the bottleneck, or more commonly, we check if Total Supply $\ge$ Total Demand.
  - Here, Max Supply from Factory = 270.
  - Total Demand = 290.
  - **Note**: The problem states the factory produces *up to* 270 tons. If demand must be fully met, it is impossible. In many textbook contexts, if Supply < Demand, it implies a shortage or the problem expects us to minimize cost for the *available* supply, or potentially there is a typo in the problem statement (e.g., factory capacity is actually 300, or demand is lower).
  - **Assumption for Modeling**: Given the explicit instruction to "Determine a transportation plan that minimizes the total cost" and standard OR problem structures, we will model the flow from the **Factory** to **Warehouses** and **Warehouses** to **Regions**.
  - Let's re-read carefully: "A sugar factory can produce up to 270 tons... transported to three warehouses... supplied to five regions."
  - Usually, these are transshipment or two-stage transportation problems.
  - Let $x_{0i}$ be flow from Factory to Warehouse $i$.
  - Let $x_{ij}$ be flow from Warehouse $i$ to Region $j$.
  - Constraint: $\sum x_{0i} \le 270$.
  - Constraint: $\sum x_{ij} \le C_i$ (Warehouse capacity).
  - Constraint: $\sum x_{ij} = D_j$ (Demand satisfaction).
  - If $\sum D_j > 270$, the model is infeasible.
  - **Alternative Interpretation**: Often in such problems, if Supply < Demand, the problem might be asking to allocate the *available* supply to meet demand as much as possible, or the "Demand" figures are actually capacities, or the Factory Capacity is the binding constraint and we simply cannot meet all demand.
  - However, looking at the numbers: $25+105+60+30+70 = 290$. $50+100+150=300$.
  - If the factory only produces 270, we cannot satisfy 290.
  - **Standard Textbook Context**: It is highly likely that this is a standard **Balanced Transportation Problem** where the "Supply" node is the Factory and the "Demand" nodes are the Regions, with Warehouses as intermediate nodes. But wait, the costs are given from **Warehouses** to **Regions**. The cost from Factory to Warehouses is **not provided**.
  - **Critical Observation**: The cost table only provides costs from **Warehouses** ($A_1, A_2, A_3$) to **Regions** ($B_1..B_5$). There is **no cost** given from the Factory to the Warehouses.
  - This implies one of two things:
    1. The Factory is the **Source** with supply 270, and the Warehouses are just storage buffers. But we need costs to send from Factory to Warehouse. Since they are missing, perhaps the problem assumes the Factory *is* the source of the costed flow, i.e., the "cost" is incurred from Warehouse to Region, and the Factory simply feeds the warehouses. But how do we know which warehouse gets the sugar?
    2. More likely: This is a **single-source, single-sink with intermediate nodes** problem where the "supply" is effectively the warehouse capacities, but constrained by the factory. OR, the problem is actually a standard transportation problem where the **Supplies** are the Warehouse Capacities (limited by Factory) and **Demands** are the Regions.
    3. Let's look at the structure again. If there is no cost from Factory to Warehouse, the cost is independent of *which* warehouse the sugar comes from, *unless* the warehouse itself has a storage cost or the "transportation" includes the factory leg. But the table is explicitly $A_i \to B_j$.
    4. **Most Logical Interpretation for Solvability**: The problem is likely a standard transportation problem where the **Supply** at each warehouse is limited by its capacity, and the total supply is limited by the factory. Since no factory-to-warehouse costs are given, we assume the cost is only incurred in the second leg (Warehouse to Region). To minimize cost, we need to decide how much sugar to allocate to each warehouse (up to its capacity and total 270 limit) and then route it to regions.
    5. However, if the cost from Factory to Warehouse is zero or irrelevant, the only decision affecting cost is the $A_i \to B_j$ flow. But the amount of flow leaving $A_i$ cannot exceed its capacity $C_i$, and the total flow from all warehouses cannot exceed 270.
    6. Since Total Demand (290) > Max Supply (270), we **cannot** satisfy all demands. The problem asks to "minimize the total cost". This usually implies satisfying demand. If infeasible, standard practice in some contexts is to introduce a dummy region or minimize unmet demand. But without a penalty for unmet demand, the problem is ill-posed.
    7. **Re-evaluating the numbers**: Is it possible the factory capacity is 300? Or Demand is different?
       - $25+105+60+30+70 = 290$.
       - $50+100+150 = 300$.
       - If Factory = 270, it's infeasible for full satisfaction.
       - **Hypothesis**: Maybe the "Demand" is not a hard constraint but a maximum? No, "demand" usually means required.
       - **Hypothesis**: Maybe the Factory produces 300? If Factory = 300, then Supply = 300, Demand = 290. This is a standard **unbalanced** problem (Supply > Demand), which is feasible. We would satisfy all demands and leave 10 tons unshipped.
       - Given the specific number "270" in the prompt, I must use it.
       - **Decision**: I will model the problem as a **Min-Cost Flow** problem.
         - Source: Factory (Supply 270).
         - Intermediate: Warehouses (Capacities 50, 100, 150).
         - Sink: Regions (Demands 25, 105, 60, 30, 70).
         - Since $\sum D > \text{Supply}$, the model as stated is infeasible if demands are equalities.
         - To provide a valid mathematical model that a solver can process, I will assume that **Demand must be met as much as possible** or, more standardly, that there is a **shortage**. However, without a penalty cost for shortage, the objective is undefined for the unmet portion.
         - **Alternative Standard Interpretation**: In many textbook problems, if Supply < Demand, it's a "shortage" problem. But often, these typos occur. Let's look at the sum of costs.
         - Let's assume the standard interpretation: **The factory supplies the warehouses, and warehouses supply the regions.**
         - Since no cost is given for Factory $\to$ Warehouse, we assume the cost is only for Warehouse $\to$ Region.
         - The decision variables will be $x_{ij}$ (amount shipped from Warehouse $i$ to Region $j$).
         - We must also decide how much capacity is *utilized* at each warehouse, which is implicitly determined by $\sum_j x_{ij}$.
         - Constraints:
           1. $\sum_j x_{ij} \le C_i$ for all $i$ (Warehouse Capacity).
           2. $\sum_i \sum_j x_{ij} \le 270$ (Factory Capacity).
           3. $\sum_i x_{ij} \ge D_j$? No, if infeasible, it should be $\sum_i x_{ij} = D_j$ if feasible, or $\le D_j$ if we can't meet demand?
           - If we use $\sum_i x_{ij} = D_j$, the solver will return "Infeasible".
           - If the problem implies that the factory *can* produce up to 270, but the warehouses can store more? No, "storage capacities... are 50, 100, 150".
           - **Let's assume the problem intends for Demand to be met, and the "270" might be a typo for 300, OR the Demand sum is a typo.**
           - However, as an AI, I must model what is given.
           - **Refined Approach**: I will define the model with **Demand Satisfaction** constraints as equalities, but note the infeasibility. **BUT**, to be helpful, I will check if "Demand" means "Maximum Demand" (i.e., we ship *up to* the demand). If so, the problem becomes: Maximize shipped amount? No, "Minimize total cost". If we can ship less, we ship 0 and cost is 0. That's trivial.
           - Therefore, Demand **must** be a hard requirement.
           - **Conclusion on Data Conflict**: The problem data is inconsistent (Supply 270 < Demand 290).
           - **Standard Fix in Modeling Tasks**: Often, "up to 270" might mean the factory *capacity*, but maybe we buy from elsewhere? No.
           - I will construct the model assuming **Demand must be met** and **Factory Supply is 270**. This will result in an infeasible model.
           - **Wait**, let's look at the table again. Is it possible the costs are for Factory $\to$ Warehouse? No, rows are $A_1, A_2, A_3$.
           - Is it possible the warehouses are the **Sources** with supplies 50, 100, 150 and the Factory constraint is just context? If we ignore the 270 and use Warehouse Capacities as Supplies: Total Supply = 300. Total Demand = 290. This is a feasible, standard transportation problem. The "Factory produces up to 270" might be a red herring or a constraint that makes it infeasible, OR it implies that the *effective* supply at the warehouses is capped by the factory.
           - If I treat it as a standard transportation problem with **Supplies** = Warehouse Capacities (50, 100, 150) and **Demands** = Regional Demands (25, 105, 60, 30, 70), it is feasible (Supply 300 > Demand 290). The factory constraint $\sum \text{outflow} \le 270$ would then cut off 20 units of potential supply, making it infeasible for full demand.
           - **Most Likely Intended Problem**: The factory capacity is likely **300** or the demands are lower. Given I cannot change the numbers, I will model the **general structure** and include the factory constraint. To make the model solvable/meaningful in a real-world sense, I will interpret "Demand" as the **required** amount. If the model is infeasible, it is infeasible.
           - **HOWEVER**, for the purpose of providing a correct *mathematical formulation*, I will define the variables for the flow from Warehouses to Regions. I will include the Factory constraint. I will set the Demand constraints as **Equalities**.

## 2. Decision Variables

Let $x_{ij}$ be the amount of sugar (in tons) shipped from Warehouse $i$ to Region $j$.

- $x_{ij} \ge 0$ for all $i \in I, j \in J$.
- Domain: **Continuous** (Sugar is a divisible bulk commodity).

*(Note: We do not need explicit variables for Factory $\to$ Warehouse flow because the cost is zero/unspecified for that leg, and the flow is entirely determined by the conservation of flow at the warehouses, bounded by warehouse capacities and total factory output.)*

## 3. Objective Function

Minimize the total transportation cost from warehouses to regions.

$$
\text{Minimize } Z = \sum_{i \in I} \sum_{j \in J} c_{ij} x_{ij}
$$

Expanded:
$$
Z = 10x_{11} + 15x_{12} + 20x_{13} + 20x_{14} + 40x_{15} \\
+ 20x_{21} + 40x_{22} + 15x_{23} + 30x_{24} + 30x_{25} \\
+ 30x_{31} + 35x_{32} + 40x_{33} + 55x_{34} + 25x_{35}
$$

## 4. Operational Constraints

### 1. Warehouse Capacity Constraints
The total amount of sugar shipped from each warehouse cannot exceed its storage capacity.

- For $A_1$:
  $$
  x_{11} + x_{12} + x_{13} + x_{14} + x_{15} \le 50
  $$
- For $A_2$:
  $$
  x_{21} + x_{22} + x_{23} + x_{24} + x_{25} \le 100
  $$
- For $A_3$:
  $$
  x_{31} + x_{32} + x_{33} + x_{34} + x_{35} \le 150
  $$

### 2. Factory Production Constraint
The total amount of sugar distributed to all regions (which equals the total shipped from all warehouses) cannot exceed the factory's monthly production capacity.

$$
\sum_{i \in I} \sum_{j \in J} x_{ij} \le 270
$$

### 3. Regional Demand Constraints
The total amount of sugar received by each region must satisfy its demand.
*(Note: As analyzed, $\sum D_j = 290 > 270$, so this system is infeasible. In a real scenario, these would be $\ge D_j$ with a shortage variable, or the problem data contains an error. Based on strict "demand" language, we use equality.)*

- For $B_1$:
  $$
  x_{11} + x_{21} + x_{31} = 25
  $$
- For $B_2$:
  $$
  x_{12} + x_{22} + x_{32} = 105
  $$
- For $B_3$:
  $$
  x_{13} + x_{23} + x_{33} = 60
  $$
- For $B_4$:
  $$
  x_{14} + x_{24} + x_{34} = 30
  $$
- For $B_5$:
  $$
  x_{15} + x_{25} + x_{35} = 70
  $$

### 4. Non-negativity Constraints

$$
x_{ij} \ge 0 \quad \forall i \in \{1,2,3\}, j \in \{1,2,3,4,5\}
$$

---

### **Feasibility Note for the User/Code Agent**
The sum of regional demands is $25 + 105 + 60 + 30 + 70 = 290$ tons.
The factory production capacity is $270$ tons.
Since $290 > 270$, **no feasible solution exists** that satisfies all demand equalities and the factory capacity constraint simultaneously.

If the intention is to **maximize the amount of demand satisfied** within the 270 ton limit, the Demand Constraints (Section 4.3) should be changed to inequalities:
$$
x_{1j} + x_{2j} + x_{3j} \le D_j
$$
And the Objective should likely be changed to **Maximize Total Shipped** or **Minimize Shortage**. However, based on the prompt "Minimize the total cost" and "Demand... is...", the standard interpretation is the equality constraints above, which implies the problem statement likely contains a typo (e.g., Factory capacity should be $\ge 290$, or Demand sums to $\le 270$).

If forced to provide a solvable model assuming the "Demand" is a **maximum** (i.e., we can ship *up to* the demand), the constraints 4.3 become $\le D_j$, and the objective is Min Cost. In that case, the optimal solution would likely ship 0 to all regions (Cost = 0) unless there is a constraint forcing shipment. Thus, the equality interpretation is the only one that makes "Minimize Cost" non-trivial, despite the infeasibility.

**Recommendation for Code Agent**:
1. Check if the Factory Capacity should be **300** (matching total warehouse capacity) or if Demand values are different.
2. If the data is immutable, the model is **Infeasible**.
3. If the goal is to allocate the **available 270 tons** to meet demand as much as possible in the most cost-effective manner, you must introduce **shortage variables** $s_j \ge 0$ for each region:
   - Change Demand Constraints to: $\sum_i x_{ij} + s_j = D_j$
   - Change Objective to: Minimize $\sum c_{ij}x_{ij} + M \sum s_j$ (where $M$ is a large penalty for unmet demand) OR Maximize $\sum (D_j - s_j)$ subject to cost limits?
   - Given the prompt doesn't specify shortage penalties, the strict equality model is the formal translation of the text.