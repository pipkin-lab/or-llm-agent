# Mathematical Optimization Model

## 1. Index Sets & Parameters

**Index Sets:**
- $I = \{1, \dots, 7\}$: Set of products (I to VII).
- $T = \{1, \dots, 6\}$: Set of months (January to June).
- $M = \{1, \dots, 5\}$: Set of machine types (Grinding, Upright Drill, Horizontal Drill, Boring Machine, Planer).

**Parameters:**
- $p_{i}$: Profit per unit of product $i$ (yuan).
  - $p = [100, 60, 80, 40, 110, 90, 30]$
- $a_{m,i}$: Machine-hours required per unit of product $i$ on machine type $m$.
  - Matrix $A$ (rows are machines, columns are products). Entries are 0 if the product does not use that machine.
  - $a_{1,1}=0.5, a_{1,2}=0.7, a_{1,5}=0.3, a_{1,6}=0.2, a_{1,7}=0.5$
  - $a_{2,1}=0.1, a_{2,2}=0.2, a_{2,4}=0.3, a_{2,6}=0.6$
  - $a_{3,1}=0.2, a_{3,3}=0.8, a_{3,7}=0.6$
  - $a_{4,1}=0.05, a_{4,2}=0.03, a_{4,4}=0.07, a_{4,5}=0.1, a_{4,7}=0.08$
  - $a_{5,3}=0.01, a_{5,5}=0.05, a_{5,7}=0.05$
- $N_{m}$: Total number of machines of type $m$.
  - $N_1=4$ (Grinding), $N_2=2$ (Upright Drill), $N_3=3$ (Horizontal Drill), $N_4=1$ (Boring), $N_5=1$ (Planer).
- $D_{t,i}$: Market demand for product $i$ in month $t$.
  - (Values from Table C-4)
- $h$: Storage cost per unit per month. $h = 5$.
- $Inv_{max}$: Maximum storage limit per product. $Inv_{max} = 100$.
- $F_{i}$: Final inventory requirement for product $i$ at end of June. $F_i = 50$ for all $i$.
- $Inv_{0,i}$: Initial inventory. $Inv_{0,i} = 0$ for all $i$.
- $H_{total}$: Total available hours per machine per month.
  - $24 \text{ days} \times 2 \text{ shifts} \times 8 \text{ hours} = 384$ hours.
- $M_{maint}(t, m)$: Number of machines of type $m$ under maintenance in month $t$.
  - $t=1$ (Jan): $M_{maint}(1,1)=1$, others 0.
  - $t=2$ (Feb): $M_{maint}(2,3)=2$, others 0.
  - $t=3$ (Mar): $M_{maint}(3,4)=1$, others 0.
  - $t=4$ (Apr): $M_{maint}(4,2)=1$, others 0.
  - $t=5$ (May): $M_{maint}(5,1)=1, M_{maint}(5,2)=1$, others 0.
  - $t=6$ (Jun): $M_{maint}(6,5)=1, M_{maint}(6,3)=1$, others 0.
- $C_{t,m}$: Available capacity (hours) for machine type $m$ in month $t$.
  - $C_{t,m} = (N_m - M_{maint}(t, m)) \times 384$.

## 2. Decision Variables

- $x_{t,i}$: Quantity of product $i$ produced in month $t$.
  - Domain: $x_{t,i} \ge 0$ (Continuous, as this is an aggregate planning problem with large volumes).
- $Inv_{t,i}$: Inventory level of product $i$ at the **end** of month $t$.
  - Domain: $Inv_{t,i} \ge 0$ (Continuous).

## 3. Objective Function

Maximize total profit (Revenue from sales - Storage Costs).
Note: Production costs are not given, only "profit per unit". Usually, "profit per unit" implies revenue minus variable production costs. Storage cost is a separate holding cost.

$$
\text{Maximize } Z = \sum_{t=1}^{6} \sum_{i=1}^{7} (p_i \cdot x_{t,i}) - \sum_{t=1}^{6} \sum_{i=1}^{7} (h \cdot Inv_{t,i})
$$

*Clarification on Sales vs Production*: In standard production-inventory LPs, we assume all produced units are either sold or stored. The revenue is typically associated with sales. However, since demand is a *maximum* (upper bound), we can choose to produce less than demand. If we produce $x_{t,i}$, and have inventory $Inv_{t-1,i}$, the total available is $Inv_{t-1,i} + x_{t,i}$. The amount sold is $S_{t,i} = Inv_{t-1,i} + x_{t,i} - Inv_{t,i}$.
The objective should technically be $\sum (p_i S_{t,i}) - \sum (h Inv_{t,i})$.
Substituting $S_{t,i}$:
$$
Z = \sum_{t=1}^{6} \sum_{i=1}^{7} p_i (Inv_{t-1,i} + x_{t,i} - Inv_{t,i}) - \sum_{t=1}^{6} \sum_{i=1}^{7} h Inv_{t,i}
$$
This can be simplified, but the expanded form is safer for implementation. Alternatively, since $\sum Inv_{t-1,i} - \sum Inv_{t,i}$ telescopes to $Inv_{0} - Inv_{6}$, which are constants ($0 - 50$), the objective is equivalent to:
$$
\text{Maximize } Z = \sum_{t=1}^{6} \sum_{i=1}^{7} (p_i \cdot x_{t,i}) - \sum_{t=1}^{6} \sum_{i=1}^{7} (h \cdot Inv_{t,i}) + \text{Constant}
$$
We will use the direct sales formulation for clarity in constraints:
Let $S_{t,i}$ be sales.
Maximize $\sum_{t,i} p_i S_{t,i} - \sum_{t,i} h Inv_{t,i}$
Subject to $S_{t,i} = Inv_{t-1,i} + x_{t,i} - Inv_{t,i}$ and $0 \le S_{t,i} \le D_{t,i}$.

To keep the model compact with only $x$ and $Inv$ variables, we substitute $S_{t,i}$ back into the objective:
$$
\text{Maximize } Z = \sum_{t=1}^{6} \sum_{i=1}^{7} p_i (x_{t,i} + Inv_{t-1,i} - Inv_{t,i}) - \sum_{t=1}^{6} \sum_{i=1}^{7} 5 \cdot Inv_{t,i}
$$
Since $Inv_{0,i}=0$ and $Inv_{6,i}=50$ are fixed, the terms $-p_i Inv_{6,i}$ and $+p_i Inv_{0,i}$ are constants. The solver can handle the variable terms.
Simplified Objective for Solver:
$$
\text{Maximize } \sum_{t=1}^{6} \sum_{i=1}^{7} p_i x_{t,i} - \sum_{t=1}^{6} \sum_{i=1}^{7} (p_i + h) Inv_{t,i}
$$
*(Note: The coefficient for $Inv_{t,i}$ becomes $-(p_i + 5)$ because holding inventory reduces current sales potential or incurs cost, effectively reducing the net benefit of previous production compared to current production. Specifically, $Inv_{t,i}$ appears with $-p_i$ in the sales term and $-h$ in the cost term.)*

## 4. Operational Constraints

**1. Inventory Balance (for all $t \in T, i \in I$):**
$$
Inv_{t,i} = Inv_{t-1,i} + x_{t,i} - S_{t,i}
$$
To avoid introducing explicit $S_{t,i}$ variables, we use the sales bounds directly:
The amount sold $S_{t,i} = Inv_{t-1,i} + x_{t,i} - Inv_{t,i}$.
Constraint: $0 \le Inv_{t-1,i} + x_{t,i} - Inv_{t,i} \le D_{t,i}$

This splits into two linear inequalities:
$$
Inv_{t,i} - x_{t,i} - Inv_{t-1,i} \le 0 \quad (\text{Sales} \ge 0 \implies Inv_{t,i} \le Inv_{t-1,i} + x_{t,i})
$$
$$
x_{t,i} - Inv_{t,i} + Inv_{t-1,i} \le D_{t,i} \quad (\text{Sales} \le D_{t,i})
$$

**2. Machine Capacity Constraints (for all $t \in T, m \in M$):**
Total hours used by all products on machine $m$ in month $t$ cannot exceed available capacity $C_{t,m}$.
$$
\sum_{i=1}^{7} a_{m,i} x_{t,i} \le C_{t,m}, \quad \forall t \in T, m \in M
$$
Where $C_{t,m} = (N_m - M_{maint}(t, m)) \times 384$.

**3. Inventory Limits (for all $t \in T, i \in I$):**
$$
0 \le Inv_{t,i} \le 100
$$

**4. Final Inventory Requirement (for all $i \in I$):**
$$
Inv_{6,i} = 50
$$

**5. Non-negativity:**
$$
x_{t,i} \ge 0, \quad \forall t \in T, i \in I
$$
$$
Inv_{t,i} \ge 0, \quad \forall t \in T, i \in I
$$

### Parameter Calculation Details for Implementation:

**Capacities $C_{t,m}$ (Hours):**

*   **Jan ($t=1$):**
    *   Grinding ($m=1$): $(4-1) \times 384 = 3 \times 384 = 1152$
    *   Upright ($m=2$): $2 \times 384 = 768$
    *   Horizontal ($m=3$): $3 \times 384 = 1152$
    *   Boring ($m=4$): $1 \times 384 = 384$
    *   Planer ($m=5$): $1 \times 384 = 384$
*   **Feb ($t=2$):**
    *   Grinding ($m=1$): $4 \times 384 = 1536$
    *   Upright ($m=2$): $2 \times 384 = 768$
    *   Horizontal ($m=3$): $(3-2) \times 384 = 1 \times 384 = 384$
    *   Boring ($m=4$): $1 \times 384 = 384$
    *   Planer ($m=5$): $1 \times 384 = 384$
*   **Mar ($t=3$):**
    *   Grinding ($m=1$): $1536$
    *   Upright ($m=2$): $768$
    *   Horizontal ($m=3$): $1152$
    *   Boring ($m=4$): $(1-1) \times 384 = 0$
    *   Planer ($m=5$): $384$
*   **Apr ($t=4$):**
    *   Grinding ($m=1$): $1536$
    *   Upright ($m=2$): $(2-1) \times 384 = 384$
    *   Horizontal ($m=3$): $1152$
    *   Boring ($m=4$): $384$
    *   Planer ($m=5$): $384$
*   **May ($t=5$):**
    *   Grinding ($m=1$): $(4-1) \times 384 = 1152$
    *   Upright ($m=2$): $(2-1) \times 384 = 384$
    *   Horizontal ($m=3$): $1152$
    *   Boring ($m=4$): $384$
    *   Planer ($m=5$): $384$
*   **Jun ($t=6$):**
    *   Grinding ($m=1$): $1536$
    *   Upright ($m=2$): $768$
    *   Horizontal ($m=3$): $(3-1) \times 384 = 768$
    *   Boring ($m=4$): $384$
    *   Planer ($m=5$): $(1-1) \times 384 = 0$

**Objective Coefficients:**
*   Production $x_{t,i}$: Coefficient $p_i$.
*   Inventory $Inv_{t,i}$ (for $t=1..5$): Coefficient $-(p_i + 5)$.
*   Inventory $Inv_{6,i}$: Fixed to 50, so it does not appear in the variable part of the objective, but contributes a constant $-50(p_i+5)$ to the total Z (or simply calculated post-solve). In the solver formulation using the expanded objective $\sum p_i x_{t,i} - \sum (p_i+5)Inv_{t,i}$, the term for $t=6$ is $- (p_i+5) \times 50$. Since $Inv_{6,i}$ is fixed, this is a constant offset. It can be included in the objective function as a constant term or ignored if only relative values are needed, but for exact profit calculation, it should be accounted for.
    *   Actually, looking at the derived objective:
        $Z = \sum p_i x_{t,i} - \sum (p_i+h) Inv_{t,i} + \text{const}$
        The constant comes from the telescoping sum of $-p_i Inv_{t,i} + p_i Inv_{t-1,i}$.
        Sum of $-p_i Inv_{t,i}$ for $t=1..6$ plus $p_i Inv_{t-1,i}$ for $t=1..6$ (where $Inv_0=0$).
        $= -p_i(Inv_1 + ... + Inv_6) + p_i(Inv_0 + ... + Inv_5)$
        $= -p_i Inv_6 + p_i Inv_0$
        $= -50 p_i$.
        Plus the storage cost term $-5 \sum_{t=1}^6 Inv_{t,i}$.
        So the total objective is:
        $$ \max \sum_{t=1}^6 \sum_{i=1}^7 p_i x_{t,i} - \sum_{t=1}^6 \sum_{i=1}^7 5 Inv_{t,i} - \sum_{i=1}^7 50 p_i $$
        Wait, let's re-verify.
        Sales $S_{t,i} = Inv_{t-1,i} + x_{t,i} - Inv_{t,i}$.
        Revenue $R = \sum_{t,i} p_i S_{t,i} = \sum_{t,i} p_i (Inv_{t-1,i} + x_{t,i} - Inv_{t,i})$.
        Cost $C = \sum_{t,i} 5 Inv_{t,i}$.
        $Z = R - C = \sum_{t,i} p_i x_{t,i} + \sum_{t,i} p_i (Inv_{t-1,i} - Inv_{t,i}) - \sum_{t,i} 5 Inv_{t,i}$.
        The middle term telescopes: $\sum_{t=1}^6 (p_i Inv_{t-1,i} - p_i Inv_{t,i}) = p_i Inv_{0,i} - p_i Inv_{6,i} = 0 - 50 p_i = -50 p_i$.
        So, $Z = \sum_{t=1}^6 \sum_{i=1}^7 p_i x_{t,i} - \sum_{t=1}^6 \sum_{i=1}^7 5 Inv_{t,i} - \sum_{i=1}^7 50 p_i$.
        
        The constant term is $\sum_{i=1}^7 50 p_i = 50(100+60+80+40+110+90+30) = 50(510) = 25500$.
        So, Maximize $\sum_{t=1}^6 \sum_{i=1}^7 p_i x_{t,i} - \sum_{t=1}^6 \sum_{i=1}^7 5 Inv_{t,i}$.
        (The constant -25500 can be added at the end).

        **Final Objective for Solver:**
        Maximize $\sum_{t=1}^{6} \sum_{i=1}^{7} p_i x_{t,i} - \sum_{t=1}^{6} \sum_{i=1}^{7} 5 Inv_{t,i}$