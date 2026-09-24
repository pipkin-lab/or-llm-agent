# Mathematical Optimization Model

## 1. Index Sets & Parameters

**Sets:**
- $P = \{1, 2, 3\}$: Set of products (1: Manuscript paper, 2: Diaries, 3: Exercise books).

**Parameters:**
- $W_{regular} = 100$: Number of regular workers.
- $S_{paper} = 30,000$: Monthly supply of white base paper (kg).
- $r_p$: Labor productivity (units per worker per month) for product $p$.
  - $r_1 = 30$ (bundles/worker)
  - $r_2 = 30$ (dozens/worker)
  - $r_3 = 30$ (boxes/worker)
- $c_p$: Raw material consumption (kg per unit) for product $p$.
  - $c_1 = 3\frac{1}{3} = \frac{10}{3}$ kg/bundle
  - $c_2 = 13\frac{1}{3} = \frac{40}{3}$ kg/dozen
  - $c_3 = 26\frac{2}{3} = \frac{80}{3}$ kg/box
- $\pi_p$: Profit per unit for product $p$ (yuan).
  - $\pi_1 = 2$ yuan/bundle
  - $\pi_2 = 3$ yuan/dozen
  - $\pi_3 = 1$ yuan/box
- $W_{cost} = 40$: Wage cost per temporary worker per month (yuan).

## 2. Decision Variables

- $x_p$: Quantity of product $p$ produced in the month (continuous, $x_p \ge 0$).
  - $x_1$: Bundles of manuscript paper.
  - $x_2$: Dozens of diaries.
  - $x_3$: Boxes of exercise books.
- $T$: Number of temporary workers hired (continuous, $T \ge 0$).
  - *Note: While workers are discrete, in large-scale aggregate planning with high production volumes, temporary workers are typically modeled as continuous variables to allow for fractional allocation or because the optimal solution often falls on integer boundaries or the LP relaxation provides the standard expected answer for this type of linear programming problem. Given the scale (30,000 kg paper), fractional workers in the LP sense represent average staffing levels or the problem expects the LP solution.*

## 3. Objective Function

**Maximize Net Profit** ($Z$):

$$
\text{Maximize } Z = 2x_1 + 3x_2 + 1x_3 - 40T
$$

*Explanation:* Total profit from sales minus the cost of hiring temporary workers.

## 4. Operational Constraints

### A. Labor Capacity Constraint
The total labor required to produce the products cannot exceed the total labor hours supplied by regular and temporary workers. Since productivity is given in units per worker, we convert production units to "worker-equivalents".

Labor required for product $p$ = $\frac{x_p}{r_p}$.

$$
\frac{x_1}{30} + \frac{x_2}{30} + \frac{x_3}{30} \le W_{regular} + T
$$

Substituting values:
$$
\frac{x_1}{30} + \frac{x_2}{30} + \frac{x_3}{30} \le 100 + T
$$

Rearranging to isolate variables:
$$
\frac{x_1}{30} + \frac{x_2}{30} + \frac{x_3}{30} - T \le 100
$$

### B. Raw Material (Paper) Constraint
The total paper consumed cannot exceed the monthly supply.

$$
\frac{10}{3}x_1 + \frac{40}{3}x_2 + \frac{80}{3}x_3 \le 30,000
$$

Simplifying (multiplying by 3/10 for clarity, though not necessary for the solver):
$$
x_1 + 4x_2 + 8x_3 \le 9,000
$$

### C. Non-negativity Constraints
$$
x_1, x_2, x_3, T \ge 0
$$

---

## Model Analysis & Solution Logic

To determine if temporary workers should be hired, we analyze the marginal profit versus the marginal cost of labor.

1.  **Check Binding Constraints at Base Case ($T=0$):**
    *   **Labor Capacity with 100 workers:**
        Max units if only producing Product 1 (most labor-efficient per unit? No, let's look at profit per labor unit).
        Let's calculate **Profit per unit of Labor** (yuan/worker-month) for each product:
        *   Product 1: $\frac{2 \text{ yuan}}{1/30 \text{ worker}} = 60$ yuan/worker.
        *   Product 2: $\frac{3 \text{ yuan}}{1/30 \text{ worker}} = 90$ yuan/worker.
        *   Product 3: $\frac{1 \text{ yuan}}{1/30 \text{ worker}} = 30$ yuan/worker.
        
        Product 2 yields the highest profit per worker. However, we must check the **Paper Constraint**.

    *   **Paper Limitations:**
        Let's see how much of each product can be made with 100 workers if we prioritize by profit/labor.
        
        *Scenario 1: Produce only Product 2 (Diaries).*
        Labor constraint: $\frac{x_2}{30} \le 100 \Rightarrow x_2 \le 3000$.
        Paper constraint: $\frac{40}{3}x_2 \le 30,000 \Rightarrow x_2 \le 30,000 \times \frac{3}{40} = 2,250$.
        Since $2,250 < 3,000$, the **Paper Constraint is binding** for Product 2.
        Max $x_2 = 2,250$.
        Labor used: $2,250 / 30 = 75$ workers.
        Remaining Labor: $100 - 75 = 25$ workers.
        Remaining Paper: 0.
        
        Can we use the remaining 25 workers to produce other products?
        No, because Paper is exhausted.
        
        *Wait, let's check if mixing yields better results.*
        
        Let's define the variables in terms of worker allocation or just solve the LP.
        
        **Corner Point Analysis:**
        
        The constraints are:
        1) $x_1 + 4x_2 + 8x_3 \le 9,000$ (Paper)
        2) $x_1 + x_2 + x_3 \le 3,000$ (Labor, with $T=0$, since $100 \times 30 = 3000$ total unit-capacity)
           *Note: The labor constraint in terms of units is simply $x_1/30 + x_2/30 + x_3/30 \le 100 \Rightarrow x_1 + x_2 + x_3 \le 3000$.*
        
        Objective: Max $Z = 2x_1 + 3x_2 + x_3$ (ignoring T cost for now to see if T>0 is beneficial).
        
        Let's evaluate the vertices of the feasible region defined by $x_i \ge 0$.
        
        **Vertex A: Maximize $x_2$ (highest profit/unit paper? No, profit/unit labor is higher for x2).**
        Let's check Profit per kg of Paper:
        *   Product 1: $2 / (10/3) = 0.6$ yuan/kg.
        *   Product 2: $3 / (40/3) = 0.225$ yuan/kg.
        *   Product 3: $1 / (80/3) = 0.0375$ yuan/kg.
        
        Product 1 is the most profitable per kg of paper.
        Product 2 is the most profitable per worker.
        
        This suggests a trade-off. We should likely produce a mix.
        
        Let's solve the LP with $T=0$ first.
        Constraints:
        (C1) $x_1 + 4x_2 + 8x_3 \le 9,000$
        (C2) $x_1 + x_2 + x_3 \le 3,000$
        
        Intersect C1 and C2 (assuming $x_3=0$ as it has lowest profit in both metrics):
        Subtract C2 from C1:
        $3x_2 + 7x_3 \le 6,000$.
        
        Let's test corners:
        1. **All Paper on $x_1$**:
           $x_1 = 9,000$.
           Labor required: $9,000 / 30 = 300$ workers.
           Available: 100.
           Infeasible without temp workers.
           
        2. **All Labor on $x_1$**:
           $x_1 = 3,000$.
           Paper required: $3,000 \times (10/3) = 10,000$ kg.
           Available: 30,000 kg.
           Feasible.
           Profit: $3,000 \times 2 = 6,000$ yuan.
           
        3. **All Labor on $x_2$**:
           $x_2 = 3,000$.
           Paper required: $3,000 \times (40/3) = 40,000$ kg.
           Available: 30,000 kg.
           Infeasible.
           
        4. **All Labor on $x_3$**:
           $x_3 = 3,000$.
           Paper required: $3,000 \times (80/3) = 80,000$ kg.
           Infeasible.
           
        5. **Intersection of C1 and C2 with $x_3=0$**:
           $x_1 + 4x_2 = 9,000$
           $x_1 + x_2 = 3,000$
           Subtracting: $3x_2 = 6,000 \Rightarrow x_2 = 2,000$.
           $x_1 = 1,000$.
           Check $x_3=0$.
           Feasibility: $x_1, x_2 \ge 0$. Yes.
           Profit: $2(1,000) + 3(2,000) + 1(0) = 10,000$ yuan.
           
        6. **Intersection of C1 and Axis $x_1=0$**:
           $4x_2 + 8x_3 = 9,000$
           $x_2 + x_3 = 3,000 \Rightarrow x_2 = 3,000 - x_3$
           $4(3,000 - x_3) + 8x_3 = 9,000$
           $12,000 + 4x_3 = 9,000 \Rightarrow 4x_3 = -3,000$. Infeasible.
           
        7. **Intersection of C2 and Axis $x_1=0$ (Labor bound)**:
           $x_2 + x_3 = 3,000$.
           To maximize profit, maximize $x_2$ (coeff 3 vs 1).
           Set $x_3=0, x_2=3,000$.
           Check Paper: $4(3,000) = 12,000 \le 9,000$? No, $12,000 > 9,000$.
           So this point is cut off by Paper constraint.
           
        So, with $T=0$, the optimal production is **$x_1=1,000, x_2=2,000, x_3=0$**.
        Profit = 10,000 yuan.
        Labor used: $(1000+2000)/30 = 100$ workers. (Fully utilized).
        Paper used: $1000(10/3) + 2000(40/3) = 3333.33 + 26666.67 = 30,000$ kg. (Fully utilized).
        
        Both constraints are binding.
        
    **Should we hire temporary workers?**
    
    If we hire 1 temporary worker ($T=1$):
    Cost = 40 yuan.
    Labor capacity increases by 30 units (1 worker * 30).
    New Labor Constraint: $x_1 + x_2 + x_3 \le 3,030$.
    Paper Constraint remains: $x_1 + 4x_2 + 8x_3 \le 9,000$.
    
    We need to find the new optimal mix.
    Since both constraints were binding, we shift along the edge defined by the intersection of the two planes, or potentially hit a new axis.
    
    Let's look at the **Marginal Profit** of adding 1 unit of labor capacity.
    At the current vertex ($x_1=1000, x_2=2000$), we are at the intersection of Labor and Paper constraints.
    The "bottleneck" is both.
    
    Let's use the dual prices (shadow prices) or simply re-solve the small LP.
    
    Objective: Max $2x_1 + 3x_2 + x_3$
    Subject to:
    1) $x_1 + 4x_2 + 8x_3 \le 9,000$
    2) $x_1 + x_2 + x_3 \le 3,000 + 30T$
    
    Let's assume $x_3=0$ still holds (lowest profit).
    System:
    $x_1 + 4x_2 = 9,000$  (Paper binding? Let's check)
    $x_1 + x_2 = 3,000 + 30T$ (Labor binding?)
    
    If both are binding:
    Subtracting: $3x_2 = 6,000 - 30T \Rightarrow x_2 = 2,000 - 10T$.
    $x_1 = 3,000 + 30T - (2,000 - 10T) = 1,000 + 40T$.
    
    Check non-negativity:
    $x_2 \ge 0 \Rightarrow 2,000 - 10T \ge 0 \Rightarrow T \le 200$.
    $x_1 \ge 0 \Rightarrow 1,000 + 40T \ge 0$ (Always true for $T \ge 0$).
    
    So, for $0 \le T \le 200$, the optimal solution is:
    $x_1 = 1,000 + 40T$
    $x_2 = 2,000 - 10T$
    $x_3 = 0$
    
    Total Profit Function $Z(T)$:
    $Z(T) = 2(1,000 + 40T) + 3(2,000 - 10T) + 0 - 40T$
    $Z(T) = 2,000 + 80T + 6,000 - 30T - 40T$
    $Z(T) = 8,000 + 10T$
    
    Since the coefficient of $T$ is **positive (+10)**, the profit increases as we hire more temporary workers.
    
    **How many is optimal?**
    The formula is valid as long as $x_2 \ge 0$, i.e., $T \le 200$.
    If $T > 200$, $x_2$ becomes 0.
    Let's check what happens if $T > 200$.
    If $x_2=0$, constraints become:
    1) $x_1 + 8x_3 \le 9,000$
    2) $x_1 + x_3 \le 3,000 + 30T$
    
    Since $x_1$ has higher profit (2) than $x_3$ (1), and $x_1$ uses less paper per unit than $x_3$ (10/3 vs 80/3), we should prioritize $x_1$.
    Max $x_1$ is limited by Paper: $x_1 \le 9,000$.
    Labor required for $x_1=9,000$ is $9,000/30 = 300$ workers.
    So if $3,000 + 30T \ge 9,000 \Rightarrow 30T \ge 6,000 \Rightarrow T \ge 200$, the labor constraint is no longer binding for producing max $x_1$.
    
    For $T \ge 200$:
    We can produce $x_1 = 9,000$ (using all paper).
    Labor used: 300 workers.
    Labor available: $100 + T$.
    Since $T \ge 200$, available labor $\ge 300$. So labor is sufficient.
    $x_3$ will be 0 (no profit incentive to use remaining labor if paper is exhausted).
    
    Profit for $T \ge 200$:
    $Z(T) = 2(9,000) - 40T = 18,000 - 40T$.
    
    Let's check the value at the boundary $T=200$:
    From first case ($Z = 8,000 + 10T$): $Z(200) = 8,000 + 2,000 = 10,000$.
    From second case ($Z = 18,000 - 40T$): $Z(200) = 18,000 - 8,000 = 10,000$.
    Matches.
    
    For $T > 200$, $Z(T) = 18,000 - 40T$.
    This is a decreasing function.
    Therefore, the maximum profit is achieved at the smallest $T$ in this region, which is $T=200$.
    
    **Conclusion:**
    The profit increases by 10 yuan for every temporary worker hired, up to 200 workers.
    After 200 workers, the profit decreases by 40 yuan for every additional worker (because you are paying 40 yuan for a worker who cannot utilize any more paper, as the paper supply is the ultimate bottleneck).
    
    Thus, the optimal number of temporary workers is **200**.
    
    **Verification of T=200:**
    - Workers: $100 + 200 = 300$.
    - Labor Capacity: $300 \times 30 = 9,000$ units.
    - Paper Supply: 30,000 kg.
    - Max $x_1$ (Manuscript) possible with Paper: $30,000 / (10/3) = 9,000$ units.
    - Labor required for 9,000 units of $x_1$: $9,000 / 30 = 300$ workers.
    - This exactly matches the available workforce.
    - Production: $x_1 = 9,000, x_2 = 0, x_3 = 0$.
    - Revenue: $9,000 \times 2 = 18,000$ yuan.
    - Cost: $200 \times 40 = 8,000$ yuan.
    - Net Profit: $18,000 - 8,000 = 10,000$ yuan.
    
    Compare with $T=0$:
    - Production: $x_1=1,000, x_2=2,000$.
    - Revenue: $1,000(2) + 2,000(3) = 10,000$.
    - Cost: 0.
    - Net Profit: 10,000 yuan.
    
    Compare with $T=100$:
    - $x_1 = 1,000 + 40(100) = 5,000$.
    - $x_2 = 2,000 - 10(100) = 1,000$.
    - Revenue: $5,000(2) + 1,000(3) = 13,000$.
    - Cost: $100(40) = 4,000$.
    - Net Profit: $13,000 - 4,000 = 9,000$.
    Wait, my previous formula $Z(T) = 8,000 + 10T$ gave $8,000 + 1,000 = 9,000$. Correct.
    
    Compare with $T=200$:
    - Net Profit: 10,000.
    
    Compare with $T=201$:
    - $Z = 18,000 - 40(201) = 18,000 - 8,040 = 9,960$.
    
    So the profit is **10,000** at $T=0$ and **10,000** at $T=200$.
    Is it strictly increasing in between?
    $Z(T) = 8,000 + 10T$.
    At $T=0, Z=8,000$?
    Wait, let's re-evaluate $Z(0)$ with the formula.
    $Z(0) = 8,000 + 0 = 8,000$.
    But we calculated $Z(0) = 10,000$ manually earlier.
    
    **ERROR DETECTION:**
    Let's re-calculate $Z(0)$ from the manual corner point.
    $x_1=1,000, x_2=2,000$.
    Profit = $2(1,000) + 3(2,000) = 10,000$.
    
    Let's re-calculate $Z(T)$ formula derivation.
    $Z(T) = 2(1,000 + 40T) + 3(2,000 - 10T) - 40T$
    $= 2,000 + 80T + 6,000 - 30T - 40T$
    $= 8,000 + 10T$.
    
    At $T=0$, formula gives 8,000. Manual calc gives 10,000.
    Why the discrepancy?
    
    Let's check the manual calc for $T=0$ again.
    $x_1 + 4x_2 = 9,000$
    $x_1 + x_2 = 3,000$
    $3x_2 = 6,000 \rightarrow x_2 = 2,000$.
    $x_1 = 1,000$.
    Profit = $2(1,000) + 3(2,000) = 10,000$.
    
    Let's check the formula inputs.
    $x_1(T) = 1,000 + 40T$. At $T=0, x_1=1,000$.
    $x_2(T) = 2,000 - 10T$. At $T=0, x_2=2,000$.
    Revenue = $2(1,000) + 3(2,000) = 10,000$.
    Cost = 0.
    Net = 10,000.
    
    Where did I get $8,000$ in the formula expansion?
    $2(1,000) = 2,000$.
    $3(2,000) = 6,000$.
    Sum = 8,000.
    Ah, $2,000 + 6,000 = 8,000$? No, $2,000 + 6,000 = 8,000$ is WRONG.
    $2,000 + 6,000 = 8,000$ is incorrect arithmetic.
    $2,000 + 6,000 = 8,000$... wait.
    $2 \times 1000 = 2000$.
    $3 \times 2000 = 6000$.
    $2000 + 6000 = 8000$.
    
    Wait. $2(1,000) + 3(2,000) = 2,000 + 6,000 = 8,000$.
    
    Let me re-read the profit parameters.
    "profit for producing: one bundle of manuscript paper is 2 yuan, one dozen of diaries is 3 yuan".
    
    My manual calc:
    $x_1 = 1,000$ bundles. Profit = $1,000 \times 2 = 2,000$.
    $x_2 = 2,000$ dozens. Profit = $2,000 \times 3 = 6,000$.
    Total Profit = 8,000.
    
    Why did I write 10,000 before?
    "Profit: $2(1,000) + 3(2,000) = 10,000$".
    $2,000 + 6,000 = 8,000$.
    I made an arithmetic error in the previous thought block.
    
    So, $Z(0) = 8,000$.
    $Z(200) = 10,000$.
    $Z(100) = 8,000 + 1,000 = 9,000$.
    
    So, hiring temporary workers **increases** profit from 8,000 to 10,000.
    
    **Final Answer Formulation:**
    1.  **Should the factory hire temporary workers?** Yes.
    2.  **How many is optimal?** 200.
    
    **Double Check:**
    If $T=200$:
    Workers = 300.
    Paper = 30,000 kg.
    Produce $x_1$ (Manuscript) only?
    Max $x_1$ by paper = $30,000 / (10/3) = 9,000$ bundles.
    Labor needed = $9,000 / 30 = 300$ workers.
    Matches exactly.
    Profit = $9,000 \times 2 = 18,000$.
    Cost = $200 \times 40 = 8,000$.
    Net = 10,000.
    
    If $T=0$:
    Net = 8,000.
    
    If $T=201$:
    Workers = 301.
    Max $x_1$ by paper = 9,000.
    Labor needed = 300.
    1 worker idle.
    Profit = 18,000.
    Cost = $201 \times 40 = 8,040$.
    Net = 9,960.
    
    So 200 is indeed the optimal integer count (and continuous optimum).