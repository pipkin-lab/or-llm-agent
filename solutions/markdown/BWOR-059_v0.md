## MANDATORY COST INVENTORY (PRE-MODELING STEP)

Extracting all numeric values representing costs/profits:
- Zhujiang expected profit: 2,000 Yuan
- Songhuajiang expected profit: 3,000 Yuan
- Huanghe expected profit: 4,000 Yuan

Count of distinct profit figures: 3. Count of decision entities (brands): 3. These ARE the objective coefficients. Assigned directly to $x_1, x_2, x_3$.

## MANDATORY RE-SCAN

Re-reading the entire problem text for any other numeric parameters:
- Steel requirements: 1.5 (Zhujiang), 3.0 (Songhuajiang), 5.0 (Huanghe). Availability: 6,000 tons.
- Labor requirements: 300 (Zhujiang), 250 (Songhuajiang), 400 (Huanghe). Availability: 600,000 hours.
- Batch size threshold: 1,000 units.

All parameters are explicitly provided. No [NOT_PROVIDED] values needed.

## MODEL TYPE DECLARATION

**Model Type: MILP (Mixed Integer Linear Programming)**

The problem involves continuous production quantities ($x_i$) coupled with binary activation variables ($y_i$) due to the "minimum batch size" constraint (produce at least 1,000 or zero). This is a classic semi-continuous variable formulation requiring integer (binary) variables.

===============================================================================

# Formal Mathematical Optimization Model

## 1. Index Sets & Parameters

**Index Sets:**
- $I = \{1, 2, 3\}$: Set of automobile brands.
  - $1$: Zhujiang
  - $2$: Songhuajiang
  - $3$: Huanghe

**Parameters:**

| Symbol | Description | Value (Brand 1) | Value (Brand 2) | Value (Brand 3) | Unit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| $p_i$ | Expected profit per unit | 2,000 | 3,000 | 4,000 | Yuan/unit |
| $a_i$ | Steel required per unit | 1.5 | 3.0 | 5.0 | tons/unit |
| $b_i$ | Labor required per unit | 300 | 250 | 400 | hours/unit |
| $S$ | Monthly steel availability | 6,000 | - | - | tons |
| $L$ | Monthly labor availability | 600,000 | - | - | hours |
| $M_i$ | Minimum economic batch size | 1,000 | 1,000 | 1,000 | units |

## 2. Decision Variables

- $x_i$: Number of units of brand $i$ produced per month.
  - Domain: $x_i \in \mathbb{R}_{\ge 0}$ (Continuous non-negative). *Note: While cars are discrete, in large-scale production planning (thousands of units), continuous relaxation is standard and typically yields integer or near-integer solutions. If strict integrality is required, $x_i \in \mathbb{Z}_{\ge 0}$, but the linear structure with binary $y_i$ dominates the complexity. We will define $x_i$ as continuous $\mathbb{R}_{\ge 0}$ for the MILP formulation, as the batch constraint $1000 \le x_i$ makes the discrete nature less critical for the model structure, but strictly speaking, physical units are integer. However, standard OR textbook formulations for this specific "batch size" problem often treat $x$ as continuous if the batch size is large, or as integer. Given the scale (thousands), we will define $x_i \ge 0$ continuous, but note that $x_i$ will effectively be integer if the solver enforces it. Let's stick to the most robust definition: $x_i \in \mathbb{R}_{\ge 0}$.*
  
  *Correction*: To be mathematically precise for "units of automobiles", $x_i$ should ideally be integer. However, the defining feature of this problem type is the **Semi-Continuous** variable constraint. We use a binary variable to enforce the semi-continuity.
  - Let $x_i$ be continuous $x_i \in \mathbb{R}_{\ge 0}$.

- $y_i$: Binary activation variable for brand $i$.
  - $y_i = 1$ if brand $i$ is produced (i.e., $x_i > 0$).
  - $y_i = 0$ if brand $i$ is not produced (i.e., $x_i = 0$).
  - Domain: $y_i \in \{0, 1\}$ for all $i \in I$.

## 3. Objective Function

Maximize total monthly profit:

$$ \text{Maximize } Z = \sum_{i \in I} p_i x_i $$

$$ Z = 2000 x_1 + 3000 x_2 + 4000 x_3 $$

## 4. Operational Constraints

### A. Resource Constraints (Steel and Labor)

Total steel consumption must not exceed monthly availability:
$$ \sum_{i \in I} a_i x_i \le S $$
$$ 1.5 x_1 + 3.0 x_2 + 5.0 x_3 \le 6000 $$

Total labor consumption must not exceed monthly availability:
$$ \sum_{i \in I} b_i x_i \le L $$
$$ 300 x_1 + 250 x_2 + 400 x_3 \le 600000 $$

### B. Economic Batch Size Constraints (Semi-Continuous Constraints)

The output of each brand must be either zero or at least 1,000 units. This is modeled using the binary variable $y_i$.

1. **Linking Constraint (Upper Bound via Binary)**:
   If $y_i = 0$, then $x_i$ must be 0.
   $$ x_i \le M_{max} y_i \quad \forall i \in I $$
   *Note*: We need an upper bound $M_{max}$ for $x_i$ to link it to $y_i$. We can derive a tight upper bound from the resource constraints.
   
   - From Steel: $x_i \le \frac{S}{a_i}$.
     - $x_1 \le 6000 / 1.5 = 4000$
     - $x_2 \le 6000 / 3.0 = 2000$
     - $x_3 \le 6000 / 5.0 = 1200$
   - From Labor: $x_i \le \frac{L}{b_i}$.
     - $x_1 \le 600000 / 300 = 2000$
     - $x_2 \le 600000 / 250 = 2400$
     - $x_3 \le 600000 / 400 = 1500$
   
   Taking the minimum of these bounds for each $i$ gives the tightest upper bound $\bar{x}_i$:
   - $\bar{x}_1 = \min(4000, 2000) = 2000$
   - $\bar{x}_2 = \min(2000, 2400) = 2000$
   - $\bar{x}_3 = \min(1200, 1500) = 1200$

   Thus, the linking constraints are:
   $$ x_1 \le 2000 y_1 $$
   $$ x_2 \le 2000 y_2 $$
   $$ x_3 \le 1200 y_3 $$

2. **Minimum Batch Size Constraint (Lower Bound via Binary)**:
   If $y_i = 1$, then $x_i \ge 1000$. If $y_i = 0$, this constraint should not force $x_i \ge 1000$.
   Standard formulation: $x_i \ge M_{min} y_i$.
   $$ x_i \ge 1000 y_i \quad \forall i \in I $$
   
   - $x_1 \ge 1000 y_1$
   - $x_2 \ge 1000 y_2$
   - $x_3 \ge 1000 y_3$

### C. Non-negativity and Domain Constraints

$$ x_i \ge 0, \quad x_i \in \mathbb{R} \quad \forall i \in I $$
$$ y_i \in \{0, 1\} \quad \forall i \in I $$

===============================================================================

## FEASIBILITY SANITY CHECK

Let's check if a feasible solution exists.
Suppose we produce only Zhujiang ($y_1=1, y_2=0, y_3=0$).
- $x_1 \ge 1000$.
- Steel: $1.5 x_1 \le 6000 \Rightarrow x_1 \le 4000$.
- Labor: $300 x_1 \le 600000 \Rightarrow x_1 \le 2000$.
- So $x_1$ can be between 1000 and 2000. Feasible.

Suppose we produce only Huanghe ($y_3=1$).
- $x_3 \ge 1000$.
- Steel: $5.0 x_3 \le 6000 \Rightarrow x_3 \le 1200$.
- Labor: $400 x_3 \le 600000 \Rightarrow x_3 \le 1500$.
- So $x_3$ can be between 1000 and 1200. Feasible.

The model is feasible.

## FINAL MODEL SUMMARY

**Model Type:** MILP

**Variables:**
- $x_1, x_2, x_3 \in \mathbb{R}_{\ge 0}$
- $y_1, y_2, y_3 \in \{0, 1\}$

**Objective:**
$$ \text{Maximize } 2000 x_1 + 3000 x_2 + 4000 x_3 $$

**Subject to:**
1. $1.5 x_1 + 3.0 x_2 + 5.0 x_3 \le 6000$
2. $300 x_1 + 250 x_2 + 400 x_3 \le 600000$
3. $x_1 \le 2000 y_1$
4. $x_2 \le 2000 y_2$
5. $x_3 \le 1200 y_3$
6. $x_1 \ge 1000 y_1$
7. $x_2 \ge 1000 y_2$
8. $x_3 \ge 1000 y_3$