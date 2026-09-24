Model Type: MILP (Mixed Integer Linear Programming)

### MANDATORY COST INVENTORY
1. Technician wage: 100 yuan/week per technician.
2. Laborer wage: 80 yuan/week per laborer.
*Note: These are the only cost figures. They correspond to the decision variables (number of technicians and laborers).*

### Index Sets & Parameters

**Parameters:**
*   $W_T = 100$: Weekly wage per technician (yuan).
*   $W_L = 80$: Weekly wage per laborer (yuan).
*   $H_T = 42$: Effective weekly working hours per technician.
*   $H_L = 36$: Effective weekly working hours per laborer.
*   $D_1 = 10,000$: Total effective hours required for Task 1.
*   $D_2 = 20,000$: Total effective hours required for Task 2.
*   $D_3 = 30,000$: Total effective hours required for Task 3.
*   $Cap_T = 400$: Maximum number of technicians.
*   $Cap_L = 800$: Maximum number of laborers.

**Task Configuration Parameters (Hours per week per unit):**
*   **Task 1:**
    *   Option A (1 Technician): $h_{1,A}^T = 42$ hours/week, $h_{1,A}^L = 0$ hours/week.
    *   Option B (1 Technician + 2 Laborers): $h_{1,B}^T = 42$ hours/week, $h_{1,B}^L = 2 \times 36 = 72$ hours/week.
*   **Task 2:**
    *   Option A (1 Technician): $h_{2,A}^T = 42$ hours/week, $h_{2,A}^L = 0$ hours/week.
    *   Option B (1 Laborer): $h_{2,B}^T = 0$ hours/week, $h_{2,B}^L = 36$ hours/week.
*   **Task 3:**
    *   Option A (5 Laborers): $h_{3,A}^T = 0$ hours/week, $h_{3,A}^L = 5 \times 36 = 180$ hours/week.
    *   Option B (1 Technician + 3 Laborers): $h_{3,B}^T = 42$ hours/week, $h_{3,B}^L = 3 \times 36 = 108$ hours/week.

### Decision Variables

Let $x_{t,k}$ denote the number of worker-units (teams or individuals) configured for task $t$ using option $k$. Since workers are discrete entities, these must be integers.

*   $x_{1,A} \in \mathbb{Z}_{\ge 0}$: Number of single-technician units for Task 1.
*   $x_{1,B} \in \mathbb{Z}_{\ge 0}$: Number of (1T+2L) teams for Task 1.
*   $x_{2,A} \in \mathbb{Z}_{\ge 0}$: Number of single-technician units for Task 2.
*   $x_{2,B} \in \mathbb{Z}_{\ge 0}$: Number of single-laborer units for Task 2.
*   $x_{3,A} \in \mathbb{Z}_{\ge 0}$: Number of (5L) teams for Task 3.
*   $x_{3,B} \in \mathbb{Z}_{\ge 0}$: Number of (1T+3L) teams for Task 3.

### Objective Function

Minimize the total weekly wage cost. The cost is determined by the total number of technicians and laborers recruited.

Total Technicians ($T_{total}$) = $1 x_{1,A} + 1 x_{1,B} + 1 x_{2,A} + 0 x_{2,B} + 0 x_{3,A} + 1 x_{3,B}$
Total Laborers ($L_{total}$) = $0 x_{1,A} + 2 x_{1,B} + 0 x_{2,A} + 1 x_{2,B} + 5 x_{3,A} + 3 x_{3,B}$

$$ \text{Minimize } Z = 100 \left( x_{1,A} + x_{1,B} + x_{2,A} + x_{3,B} \right) + 80 \left( 2 x_{1,B} + x_{2,B} + 5 x_{3,A} + 3 x_{3,B} \right) $$

Simplifying the coefficients:
*   $x_{1,A}$: $100(1) = 100$
*   $x_{1,B}$: $100(1) + 80(2) = 100 + 160 = 260$
*   $x_{2,A}$: $100(1) = 100$
*   $x_{2,B}$: $80(1) = 80$
*   $x_{3,A}$: $80(5) = 400$
*   $x_{3,B}$: $100(1) + 80(3) = 100 + 240 = 340$

$$ \text{Minimize } Z = 100 x_{1,A} + 260 x_{1,B} + 100 x_{2,A} + 80 x_{2,B} + 400 x_{3,A} + 340 x_{3,B} $$

### Operational Constraints

**1. Task Completion Constraints (Effective Hours)**
The total effective hours provided by the recruited workers for each task must be at least the required hours for that task.

*   **Task 1:**
    $$ 42 x_{1,A} + 42 x_{1,B} \ge 10,000 $$
    *(Note: Laborers in Task 1 Option B contribute to the team's output, but the "effective working time" calculation in the problem implies the team as a whole generates the work. The constraint is on the total hours required. The hours provided by the team are the sum of individual effective hours. However, usually "effective working time required" refers to the total man-hours needed. Let's look closely at the wording: "total effective working time required per week is...". This implies the sum of individual effective hours must meet the demand.)*
    
    Correction on interpretation: The problem states "total effective working time required... is 10,000 hours". This is a demand for labor-hours. The supply is the sum of effective hours of the workers assigned.
    
    Task 1 Supply:
    From Option A: $1 \text{ tech} \times 42 \text{ h/tech} = 42$ hours per unit $x_{1,A}$.
    From Option B: $(1 \text{ tech} \times 42 \text{ h/tech}) + (2 \text{ lab} \times 36 \text{ h/lab}) = 42 + 72 = 114$ hours per unit $x_{1,B}$.
    
    Constraint:
    $$ 42 x_{1,A} + 114 x_{1,B} \ge 10,000 $$

*   **Task 2:**
    From Option A: $1 \text{ tech} \times 42 \text{ h/tech} = 42$ hours per unit $x_{2,A}$.
    From Option B: $1 \text{ lab} \times 36 \text{ h/lab} = 36$ hours per unit $x_{2,B}$.
    
    Constraint:
    $$ 42 x_{2,A} + 36 x_{2,B} \ge 20,000 $$

*   **Task 3:**
    From Option A: $5 \text{ lab} \times 36 \text{ h/lab} = 180$ hours per unit $x_{3,A}$.
    From Option B: $(1 \text{ tech} \times 42 \text{ h/tech}) + (3 \text{ lab} \times 36 \text{ h/lab}) = 42 + 108 = 150$ hours per unit $x_{3,B}$.
    
    Constraint:
    $$ 180 x_{3,A} + 150 x_{3,B} \ge 30,000 $$

**2. Recruitment Capacity Constraints**
The total number of technicians and laborers recruited cannot exceed the maximum available.

*   **Technician Capacity:**
    Total Techs = $x_{1,A} + x_{1,B} + x_{2,A} + x_{3,B}$
    $$ x_{1,A} + x_{1,B} + x_{2,A} + x_{3,B} \le 400 $$

*   **Laborer Capacity:**
    Total Laborers = $2 x_{1,B} + x_{2,B} + 5 x_{3,A} + 3 x_{3,B}$
    $$ 2 x_{1,B} + x_{2,B} + 5 x_{3,A} + 3 x_{3,B} \le 800 $$

**3. Non-negativity and Integrality**
$$ x_{1,A}, x_{1,B}, x_{2,A}, x_{2,B}, x_{3,A}, x_{3,B} \in \mathbb{Z}_{\ge 0} $$