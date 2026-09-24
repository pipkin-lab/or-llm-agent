To formulate this problem, we first identify the decision variables, parameters, and constraints based on the provided text.

### 1. Index Sets & Parameters

**Products:**
Let $i$ index the three products:
- $i=1$: Manuscript paper (unit: bundle)
- $i=2$: Diaries (unit: dozen)
- $i=3$: Exercise books (unit: box)

**Resources:**
- Total Workers: $W = 100$
- Total Raw Material: $M = 30,000$ kg

**Labor Productivity (units per worker per month):**
- $p_1 = 30$ bundles/worker
- $p_2 = 30$ dozens/worker
- $p_3 = 30$ boxes/worker

*Note: Since productivity is uniform (30 units/worker for all products), the labor constraint can be simplified. Total labor capacity in terms of "worker-units" is $100 \times 30 = 3000$ units of production capacity. Alternatively, we can define labor required per unit.*

**Labor Requirement per Unit (worker-months per unit):**
- $l_1 = 1/30$ worker-months/bundle
- $l_2 = 1/30$ worker-months/dozen
- $l_3 = 1/30$ worker-months/box

**Raw Material Consumption per Unit (kg):**
- $m_1 = 3\frac{1}{3} = \frac{10}{3}$ kg/bundle
- $m_2 = 13\frac{1}{3} = \frac{40}{3}$ kg/dozen
- $m_3 = 26\frac{2}{3} = \frac{80}{3}$ kg/box

**Profit per Unit (yuan):**
- $\pi_1 = 2$ yuan/bundle
- $\pi_2 = 3$ yuan/dozen
- $\pi_3 = 1$ yuan/box

### 2. Decision Variables

Let $x_i$ be the number of units of product $i$ produced per month.
Since products are discrete physical items (bundles, dozens, boxes), these should ideally be integers. However, in large-scale production planning with such large capacities (30,000 kg), continuous relaxation is often acceptable if the problem implies aggregate flow, but strictly speaking, "bundles" and "boxes" are discrete. Given the standard nature of such LP textbook problems, we will define them as **Integer** variables to be precise, though the optimal solution to the LP relaxation is likely to be integer-valued or close enough. We will declare them as **INTEGER** to satisfy Rule 2.

- $x_1 \in \mathbb{Z}_{\ge 0}$: Number of bundles of manuscript paper.
- $x_2 \in \mathbb{Z}_{\ge 0}$: Number of dozens of diaries.
- $x_3 \in \mathbb{Z}_{\ge 0}$: Number of boxes of exercise books.

### 3. Objective Function

Maximize total profit $Z$:
$$ \text{Maximize } Z = 2x_1 + 3x_2 + 1x_3 $$

### 4. Operational Constraints

**Constraint 1: Labor Capacity**
The total labor used must not exceed the available worker-months.
Total labor required = $l_1 x_1 + l_2 x_2 + l_3 x_3$
Total available labor = $100$ workers.
$$ \frac{1}{30}x_1 + \frac{1}{30}x_2 + \frac{1}{30}x_3 \le 100 $$
Multiplying by 30 for simplicity:
$$ x_1 + x_2 + x_3 \le 3000 $$

**Constraint 2: Raw Material Capacity**
The total raw material used must not exceed the monthly supply.
Total material required = $m_1 x_1 + m_2 x_2 + m_3 x_3$
Total available material = $30,000$ kg.
$$ \frac{10}{3}x_1 + \frac{40}{3}x_2 + \frac{80}{3}x_3 \le 30000 $$
Multiplying by 3 for simplicity:
$$ 10x_1 + 40x_2 + 80x_3 \le 90000 $$
Dividing by 10:
$$ x_1 + 4x_2 + 8x_3 \le 9000 $$

**Constraint 3: Non-negativity and Integrality**
$$ x_1, x_2, x_3 \ge 0, \quad x_i \in \mathbb{Z} $$

### Model Type Declaration
**MILP** (Mixed Integer Linear Programming).
*Note: Since all variables are integer, it is specifically an Integer Linear Program (ILP).*

---

### Final Formulation

**Index Sets & Parameters**
- $I = \{1, 2, 3\}$ corresponding to Manuscript, Diaries, Exercise Books.
- Profit coefficients: $\pi = [2, 3, 1]$ (yuan)
- Labor coefficients (worker-months/unit): $L = [1/30, 1/30, 1/30]$
- Material coefficients (kg/unit): $M = [10/3, 40/3, 80/3]$
- Total Labor Capacity: $W_{tot} = 100$
- Total Material Capacity: $M_{tot} = 30000$

**Decision Variables**
- $x_1, x_2, x_3 \in \mathbb{Z}_{\ge 0}$

**Objective Function**
$$ \text{Maximize } Z = 2x_1 + 3x_2 + x_3 $$

**Constraints**
1. **Labor Constraint:**
   $$ \frac{1}{30}x_1 + \frac{1}{30}x_2 + \frac{1}{30}x_3 \le 100 \iff x_1 + x_2 + x_3 \le 3000 $$
2. **Material Constraint:**
   $$ \frac{10}{3}x_1 + \frac{40}{3}x_2 + \frac{80}{3}x_3 \le 30000 \iff x_1 + 4x_2 + 8x_3 \le 9000 $$
3. **Bounds:**
   $$ x_1 \ge 0, \quad x_2 \ge 0, \quad x_3 \ge 0 $$
   $$ x_i \in \mathbb{Z} \quad \forall i \in I $$