# Optimization Model: Multi-Period Production Planning

## 1. Index Sets & Parameters

**Index Sets:**
*   $P = \{1, \dots, 7\}$: Set of products (I to VII).
*   $T = \{1, \dots, 6\}$: Set of time periods (Months 1 to 6, corresponding to Jan to Jun).
*   $M = \{1, \dots, 5\}$: Set of machine types.
    *   $m=1$: Grinding
    *   $m=2$: Upright Drill
    *   $m=3$: Horizontal Drill
    *   $m=4$: Boring Machine
    *   $m=5$: Planer

**Parameters:**

*   **Machine Capacity Availability:**
    *   The factory operates 24 days/month $\times$ 2 shifts/day $\times$ 8 hours/shift = **384 hours/month**.
    *   $M_{total}(m)$: Total number of machines of type $m$.
        *   $M_{total}(1) = 4$ (Grinding)
        *   $M_{total}(2) = 2$ (Upright Drill)
        *   $M_{total}(3) = 3$ (Horizontal Drill)
        *   $M_{total}(4) = 1$ (Boring)
        *   $M_{total}(5) = 1$ (Planer)
    *   $Maint(m, t)$: Number of machines of type $m$ under maintenance in month $t$.
        *   $t=1$ (Jan): $Maint(1,1)=1$, others 0.
        *   $t=2$ (Feb): $Maint(3,2)=2$, others 0.
        *   $t=3$ (Mar): $Maint(4,3)=1$, others 0.
        *   $t=4$ (Apr): $Maint(2,4)=1$, others 0.
        *   $t=5$ (May): $Maint(1,5)=1, Maint(2,5)=1$, others 0.
        *   $t=6$ (Jun): $Maint(5,6)=1, Maint(3,6)=1$, others 0.
    *   $Cap(m, t)$: Available machine-hours for machine type $m$ in month $t$.
        $$Cap(m, t) = 384 \times \max(0, M_{total}(m) - Maint(m, t))$$

*   **Processing Times:**
    *   $a_{m,p}$: Machine-hours required on machine $m$ for one unit of product $p$. Derived from Table C-3. Note: "--" implies 0.

    | Machine $m$ \ Product $p$ | 1 (I) | 2 (II) | 3 (III) | 4 (IV) | 5 (V) | 6 (VI) | 7 (VII) |
    | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
    | 1 (Grind) | 0.5 | 0.7 | 0 | 0 | 0.3 | 0.2 | 0.5 |
    | 2 (Upright) | 0.1 | 0.2 | 0 | 0.3 | 0 | 0.6 | 0 |
    | 3 (Horiz) | 0.2 | 0 | 0.8 | 0 | 0 | 0 | 0.6 |
    | 4 (Boring) | 0.05 | 0.03 | 0 | 0.07 | 0.1 | 0 | 0.08 |
    | 5 (Planer) | 0 | 0 | 0.01 | 0 | 0.05 | 0 | 0.05 |

*   **Profit & Costs:**
    *   $Profit_p$: Profit per unit of product $p$ (yuan).
        *   $Profit = [100, 60, 80, 40, 110, 90, 30]$ for $p=1 \dots 7$.
    *   $H_p$: Holding cost per unit per month = 5 yuan. (Same for all products).

*   **Demand & Inventory:**
    *   $D_{p,t}$: Maximum market demand for product $p$ in month $t$ (Table C-4).
    *   $Inv_{p,0}$: Initial inventory for product $p$ at $t=0$ (Jan 1st) = 0.
    *   $Inv_{p,T}^{req}$: Required final inventory for product $p$ at end of $T=6$ = 50.
    *   $Inv_{max}$: Maximum inventory allowed per product at any time = 100.

## 2. Decision Variables

*   $x_{p,t}$: Continuous variable representing the number of units of product $p$ produced in month $t$.
    *   Domain: $x_{p,t} \ge 0, \quad \forall p \in P, t \in T$.
    *   *Note: While production is physical, given the large scale (hundreds of units) and standard LP practice for such linear production planning problems, continuous variables are appropriate. If integer constraints were strictly required, $x_{p,t} \in \mathbb{Z}^+$, but LP relaxation is typically expected for this scale unless specified otherwise. However, given "units" are discrete, let's check magnitude. 500 units is not tiny. Standard OR textbooks often accept LP here. But to be safe with "units", let's define them as continuous as fractional production planning is common in aggregate models. If strict integrality is needed, change to INTEGER. Given the prompt's instruction "If the problem involves small counts (<100)... ALWAYS use integer", but here counts are 100-1100. 1.5 units of product is physically impossible. However, usually, these aggregate models assume divisibility or the numbers are large enough that integrality is negligible. Let's look at the "Integrality & Continuity" rule again: "If the problem involves 'units' of a product where fractional units are physically impossible... use integer variables." I will define them as **INTEGER** to be strictly correct physically, although the solver might handle the LP relaxation well. Actually, for a 6-period, 7-product model, MILP is very fast. I will specify **INTEGER**.*
    *   **Correction**: The prompt says "If the problem involves small counts (< 100 units... ALWAYS use integer". Here counts are > 100. "If the problem involves 'units' of a product where fractional units are physically impossible (e.g., 1.5 ships), use integer variables." Products are discrete. I will use **INTEGER** variables to be safe, but note that LP relaxation is often the textbook answer for such large numbers. Let's stick to **INTEGER** for $x_{p,t}$ and $y_{p,t}$ to ensure physical validity, as per the strict rule "fractional units are physically impossible".

*   $y_{p,t}$: Continuous variable representing the number of units of product $p$ sold (shipped to market) in month $t$.
    *   Domain: $y_{p,t} \in \mathbb{Z}^+$ (or $\mathbb{R}^+$ if we assume aggregate flow). Let's keep consistency: **INTEGER**.
    *   *Self-Correction*: If $x$ is integer, $y$ should likely be integer. Inventory $I$ will also be integer.

*   $I_{p,t}$: Continuous/Integer variable representing the inventory level of product $p$ at the **end** of month $t$.
    *   Domain: $I_{p,t} \in \mathbb{Z}^+$.

## 3. Objective Function

Maximize Total Profit:
$$ \text{Maximize } Z = \sum_{t=1}^{6} \sum_{p=1}^{7} (Profit_p \cdot x_{p,t} - H_p \cdot I_{p,t}) $$

*Note: The problem asks to maximize total profit. Usually, profit is calculated on sales. However, "Profit per unit" is given for production. In standard production-inventory problems, the objective is often:
$\sum (\text{Sales Revenue} - \text{Production Cost} - \text{Holding Cost})$.
Here, "Profit per unit" likely means the net contribution margin (Revenue - Variable Production Cost).
Does the profit apply to units *produced* or *sold*?
Standard interpretation: You earn the profit when you sell. You pay holding cost on what you store.
However, sometimes "Profit per unit" is treated as a benefit of production that is realized regardless of when it is sold, minus holding costs.
Let's look at the phrasing: "profit per unit... is given... maximize total profit".
If I produce 1 unit and store it, have I made the profit? No, I've incurred the variable cost. The profit is realized upon sale.
BUT, in many simplified LP formulations, the objective is $\sum (c_p x_{p,t}) - \sum (h_p I_{p,t})$, where $c_p$ is the unit profit. This assumes the "profit" is the contribution margin generated by the production activity, and holding is a penalty.
Alternatively, if "Profit" is the final margin, it should be linked to sales $y_{p,t}$.
Let's analyze the data. $Profit_p$ is listed alongside machine hours. This usually implies the contribution margin per unit produced.
If I use $\sum Profit_p x_{p,t}$, I am assuming I get paid for production.
If I use $\sum Profit_p y_{p,t}$, I am assuming I get paid for sales.
Given the constraint "Unsold units can be stored... storage cost 5 yuan", the most robust economic model is:
Objective = (Total Contribution Margin from Sales) - (Total Holding Costs).
However, if "Profit per unit" is the *unit profit* (i.e., Price - Cost), and we assume we only count profit when sold, the term is $Profit_p \cdot y_{p,t}$.
Let's check the constraint "Final inventory requirement... 50 units". These 50 units are produced but not sold in the 6 months (or sold later, but outside the horizon). If we only count profit on sales $y$, the 50 final units generate 0 profit in the objective. This is standard for a finite horizon problem (terminal inventory has no immediate profit realization, only its residual value, which is not given).
However, often in these textbook problems, "Maximize Profit" with "Unit Profit" given implies:
$Z = \sum_{t,p} Profit_p x_{p,t} - \sum_{t,p} HoldingCost_p I_{p,t}$.
Why? Because the "Unit Profit" is the economic benefit of the *production plan*. The holding cost is the penalty for delaying the sale. This formulation effectively treats the "Profit" as the cash flow generated by production, offset by the cost of storage.
Let's consider the alternative: $Z = \sum_{t,p} Profit_p y_{p,t} - \sum_{t,p} HoldingCost_p I_{p,t}$.
If I produce 100, sell 50, store 50.
Case A (Profit on Production): Gain 100*P, Cost 50*H.
Case B (Profit on Sales): Gain 50*P, Cost 50*H.
Which is standard?
Usually, "Profit per unit" in such tables is the *contribution margin*. In a multi-period model, you maximize the sum of contribution margins from *sales* minus holding costs.
However, if the problem doesn't distinguish between "Revenue" and "Cost" but gives a single "Profit" number, it's ambiguous.
Let's look at similar problems. Often, if "Profit" is given per unit, the objective is $\sum Profit \cdot x - \sum Holding \cdot I$. This assumes the "profit" is realized upon production (perhaps the cost is sunk or the profit is defined as the net benefit of the activity).
Actually, a more precise interpretation: The factory's goal is to maximize the net financial outcome.
Outcome = (Value of Goods Sold) - (Cost of Goods Produced) - (Holding Costs).
We are given "Profit per unit" = (Value of Goods Sold - Cost of Goods Produced) / Unit.
So, Value - Cost = $Profit_p \times (\text{Units Sold})$.
Therefore, the objective should be based on **Sales** $y_{p,t}$.
$Z = \sum_{t=1}^6 \sum_{p=1}^7 (Profit_p \cdot y_{p,t} - 5 \cdot I_{p,t})$.
*Wait*, if I produce units that remain in final inventory, they are not sold, so they don't generate the "Profit" term in this formulation. This is correct for a cash-flow based maximization over the horizon. The 50 final units are a liability/asset with no cash inflow in the period.
However, there is a risk that the problem intends "Profit" to be the benefit of production.
Let's check the magnitude. If I use $x$, I am rewarded for producing the final 50 units. If I use $y$, I am not.
Given "Final inventory requirement: 50 units", these units are *forced* to be produced. If the objective rewards production, the solver will produce exactly what is needed to meet demand + final inventory. If it rewards sales, it will produce what is needed to meet demand + final inventory. The constraint links them.
Let's assume the standard **Sales-based Profit** interpretation, as it is financially rigorous.
*Re-evaluation*: Many OR textbooks define the objective as $\sum c_p x_{p,t} - \sum h_p I_{p,t}$ where $c_p$ is the profit per unit produced. Why? Because the "Profit" is often modeled as the net gain from the production decision itself, and the holding cost is the penalty. If we use sales, we must ensure we don't sell more than we produce (which is handled by inventory balance).
Let's look at the "Data Completeness" and "Objective Direction".
If I use $y_{p,t}$, the objective is $\sum (100 y_{1,t} + \dots) - 5 \sum I_{p,t}$.
If I use $x_{p,t}$, the objective is $\sum (100 x_{1,t} + \dots) - 5 \sum I_{p,t}$.
Difference: $\sum (Profit_p \cdot x_{p,t} - Profit_p \cdot y_{p,t}) = \sum Profit_p \cdot (x_{p,t} - y_{p,t})$.
From inventory balance: $I_{p,t} - I_{p,t-1} = x_{p,t} - y_{p,t}$.
So $x_{p,t} - y_{p,t} = I_{p,t} - I_{p,t-1}$.
Summing over $t$: $\sum (x_{p,t} - y_{p,t}) = I_{p,T} - I_{p,0}$.
So, $\sum_{t} (Profit_p \cdot x_{p,t}) - \sum_{t} (Profit_p \cdot y_{p,t}) = Profit_p \cdot (I_{p,6} - I_{p,0})$.
Since $I_{p,6} = 50$ and $I_{p,0} = 0$, the difference is a constant: $\sum_p 50 \cdot Profit_p$.
**Conclusion**: Mathematically, maximizing $\sum Profit_p x_{p,t} - \sum 5 I_{p,t}$ is **equivalent** to maximizing $\sum Profit_p y_{p,t} - \sum 5 I_{p,t}$, because the difference between the two objectives is a constant ($\sum_p 50 Profit_p$).
Therefore, either formulation yields the same optimal production/sales plan. I will use the **Production-based** formulation ($x_{p,t}$) as it is often more direct in LPs where production is the primary control variable, but I will note the equivalence. Actually, using $y_{p,t}$ is safer if "Profit" is strictly a sales metric. But since they are equivalent, I will write the objective using $x_{p,t}$ for simplicity of indexing in the production context, or $y_{p,t}$ for financial accuracy. Let's use **$y_{p,t}$** (Sales) to be semantically precise: "Profit is earned when sold".
Wait, if I use $y$, the term is $Profit_p \cdot y_{p,t}$.
Let's stick to:
$$ \text{Maximize } Z = \sum_{t=1}^{6} \sum_{p=1}^{7} (Profit_p \cdot y_{p,t}) - \sum_{t=1}^{6} \sum_{p=1}^{7} (5 \cdot I_{p,t}) $$
This is robust.

## 4. Operational Constraints

### A. Inventory Balance Constraints
For each product $p$ and month $t$:
$$ I_{p,t} = I_{p,t-1} + x_{p,t} - y_{p,t} $$
Where:
*   $I_{p,0} = 0$ (Given)
*   $I_{p,6} = 50$ (Given final requirement)
*   $I_{p,t} \le 100$ (Storage limit)
*   $I_{p,t} \ge 0$

### B. Demand Satisfaction Constraints
The problem states "Maximum market demand". This implies we can sell *up to* the demand. We are not forced to sell all demand if we choose not to (though profit maximization will likely push us to sell as much as possible if capacity allows, or produce less if capacity is tight).
$$ y_{p,t} \le D_{p,t} \quad \forall p \in P, t \in T $$

### C. Machine Capacity Constraints
For each machine type $m$ and month $t$:
$$ \sum_{p=1}^{7} a_{m,p} \cdot x_{p,t} \le Cap(m, t) $$

Where $Cap(m, t)$ is calculated as:
$$ Cap(m, t) = 384 \times \max(0, M_{total}(m) - Maint(m, t)) $$

Let's pre-calculate the capacities for clarity in the model definition (though the solver will use the formula):
*   **Grinding ($m=1$)**: Total 4.
    *   Jan: $4-1=3 \rightarrow 3 \times 384 = 1152$
    *   Feb: $4-0=4 \rightarrow 4 \times 384 = 1536$
    *   Mar: $4-0=4 \rightarrow 1536$
    *   Apr: $4-0=4 \rightarrow 1536$
    *   May: $4-1=3 \rightarrow 1152$
    *   Jun: $4-0=4 \rightarrow 1536$
*   **Upright Drill ($m=2$)**: Total 2.
    *   Jan: $2-0=2 \rightarrow 768$
    *   Feb: $2-0=2 \rightarrow 768$
    *   Mar: $2-0=2 \rightarrow 768$
    *   Apr: $2-1=1 \rightarrow 384$
    *   May: $2-1=1 \rightarrow 384$
    *   Jun: $2-0=2 \rightarrow 768$
*   **Horizontal Drill ($m=3$)**: Total 3.
    *   Jan: $3-0=3 \rightarrow 1152$
    *   Feb: $3-2=1 \rightarrow 384$
    *   Mar: $3-0=3 \rightarrow 1152$
    *   Apr: $3-0=3 \rightarrow 1152$
    *   May: $3-0=3 \rightarrow 1152$
    *   Jun: $3-1=2 \rightarrow 768$
*   **Boring ($m=4$)**: Total 1.
    *   Jan: $1-0=1 \rightarrow 384$
    *   Feb: $1-0=1 \rightarrow 384$
    *   Mar: $1-1=0 \rightarrow 0$
    *   Apr: $1-0=1 \rightarrow 384$
    *   May: $1-0=1 \rightarrow 384$
    *   Jun: $1-0=1 \rightarrow 384$
*   **Planer ($m=5$)**: Total 1.
    *   Jan: $1-0=1 \rightarrow 384$
    *   Feb: $1-0=1 \rightarrow 384$
    *   Mar: $1-0=1 \rightarrow 384$
    *   Apr: $1-0=1 \rightarrow 384$
    *   May: $1-0=1 \rightarrow 384$
    *   Jun: $1-1=0 \rightarrow 0$

### D. Non-negativity and Integrality
$$ x_{p,t} \ge 0, \quad y_{p,t} \ge 0, \quad I_{p,t} \ge 0 $$
$$ x_{p,t}, y_{p,t}, I_{p,t} \in \mathbb{Z} \quad \text{(Integer constraints)} $$

*(Note: As discussed, if the problem expects an LP solution, relax integrality to $\mathbb{R}^+$. Given the scale, the difference might be negligible, but integer is physically correct.)*

## Final Model Summary

**Sets:**
*   $P = \{1,\dots,7\}$
*   $T = \{1,\dots,6\}$
*   $M = \{1,\dots,5\}$

**Parameters:**
*   $a_{m,p}$: Processing time (Table C-3)
*   $Profit_p$: Unit profit (Table C-3)
*   $D_{p,t}$: Demand (Table C-4)
*   $Cap_{m,t}$: Available machine hours (Calculated above)
*   $H_p = 5$: Holding cost
*   $I_{p,0} = 0$
*   $I_{p,6} = 50$
*   $I_{max} = 100$

**Variables:**
*   $x_{p,t} \in \mathbb{Z}^+$: Production of $p$ in $t$
*   $y_{p,t} \in \mathbb{Z}^+$: Sales of $p$ in $t$
*   $I_{p,t} \in \mathbb{Z}^+$: End-of-month inventory of $p$ in $t$

**Objective:**
$$ \text{Maximize } Z = \sum_{t \in T} \sum_{p \in P} Profit_p y_{p,t} - \sum_{t \in T} \sum_{p \in P} 5 I_{p,t} $$

**Constraints:**
1.  **Inventory Balance:**
    $$ I_{p,t} = I_{p,t-1} + x_{p,t} - y_{p,t} \quad \forall p \in P, t \in T $$
    *(With $I_{p,0}=0$ and $I_{p,6}=50$ fixed)*

2.  **Demand Limit:**
    $$ y_{p,t} \le D_{p,t} \quad \forall p \in P, t \in T $$

3.  **Inventory Limit:**
    $$ I_{p,t} \le 100 \quad \forall p \in P, t \in T $$

4.  **Machine Capacity:**
    $$ \sum_{p \in P} a_{m,p} x_{p,t} \le Cap_{m,t} \quad \forall m \in M, t \in T $$

5.  **Non-negativity/Integrality:**
    $$ x_{p,t}, y_{p,t}, I_{p,t} \ge 0, \quad \text{integer} $$