# Operations Research Model: Student Scheduling

## Model Type
**LP** (Linear Program)

## Index Sets & Parameters

**Index Sets:**
- $I = \{1, 2, 3, 4\}$: Set of undergraduate students
- $G = \{5, 6\}$: Set of graduate students
- $J = I \cup G = \{1, 2, 3, 4, 5, 6\}$: Set of all students
- $D = \{1, 2, 3, 4, 5\}$: Set of days (1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri)

**Parameters:**
- $w_j$: Hourly wage of student $j$ (yuan/h)
  - $w_1 = 10.0, w_2 = 10.0, w_3 = 9.9, w_4 = 9.8, w_5 = 10.8, w_6 = 11.3$
- $M_{j,d}$: Maximum available hours for student $j$ on day $d$
  - Student 1: $M_{1,1}=6, M_{1,2}=0, M_{1,3}=9, M_{1,4}=0, M_{1,5}=7$
  - Student 2: $M_{2,1}=0, M_{2,2}=9, M_{2,3}=0, M_{2,4}=6, M_{2,5}=0$
  - Student 3: $M_{3,1}=4, M_{3,2}=8, M_{3,3}=3, M_{3,4}=0, M_{3,5}=5$
  - Student 4: $M_{4,1}=5, M_{4,2}=5, M_{4,3}=6, M_{4,4}=0, M_{4,5}=4$
  - Student 5: $M_{5,1}=3, M_{5,2}=0, M_{5,3}=4, M_{5,4}=8, M_{5,5}=0$
  - Student 6: $M_{6,1}=0, M_{6,2}=9, M_{6,3}=0, M_{6,4}=6, M_{6,5}=3$
- $H_d$: Required coverage hours per day $d$
  - $H_d = 14$ for all $d \in D$ (8:00 AM to 10:00 PM)
- $L_{min}^{UG} = 8$: Minimum weekly hours per undergraduate
- $L_{min}^{Grad} = 7$: Minimum weekly hours per graduate

## Decision Variables
- $x_{j,d}$: Number of hours student $j$ works on day $d$
  - **Domain**: $x_{j,d} \in \mathbb{R}_{\ge 0}$ for all $j \in J, d \in D$
  - *Note*: Continuous variables are appropriate here as work hours can be allocated in fractional increments (e.g., half-hours), and the problem does not specify integer hour constraints.

## Objective Function
Minimize total wage payment:
$$
\min Z = \sum_{j \in J} \sum_{d \in D} w_j \cdot x_{j,d}
$$
Expanded:
$$
Z = 10.0(x_{1,1} + x_{1,3} + x_{1,5}) + 10.0(x_{2,2} + x_{2,4}) + 9.9(x_{3,1} + x_{3,2} + x_{3,3} + x_{3,5}) + 9.8(x_{4,1} + x_{4,2} + x_{4,3} + x_{4,5}) + 10.8(x_{5,1} + x_{5,3} + x_{5,4}) + 11.3(x_{6,2} + x_{6,4} + x_{6,5})
$$
*(Terms with $M_{j,d}=0$ are omitted as $x_{j,d}=0$ is enforced by upper bounds)*

## Operational Constraints

### 1. Daily Coverage Constraints (Exactly One Student on Duty at All Times)
For each day $d \in D$, the sum of hours worked by all students must equal the total lab operating hours:
$$
\sum_{j \in J} x_{j,d} = 14 \quad \forall d \in D
$$
Explicitly:
- **Mon (d=1)**: $x_{1,1} + x_{3,1} + x_{4,1} + x_{5,1} = 14$
- **Tue (d=2)**: $x_{2,2} + x_{3,2} + x_{4,2} + x_{6,2} = 14$
- **Wed (d=3)**: $x_{1,3} + x_{3,3} + x_{4,3} + x_{5,3} = 14$
- **Thu (d=4)**: $x_{2,4} + x_{4,4} + x_{5,4} + x_{6,4} = 14$
- **Fri (d=5)**: $x_{1,5} + x_{3,5} + x_{4,5} + x_{6,5} = 14$

### 2. Maximum Availability Constraints
No student can work more than their maximum available hours on any day:
$$
x_{j,d} \le M_{j,d} \quad \forall j \in J, d \in D
$$
Non-zero upper bounds:
- $x_{1,1} \le 6, x_{1,3} \le 9, x_{1,5} \le 7$
- $x_{2,2} \le 9, x_{2,4} \le 6$
- $x_{3,1} \le 4, x_{3,2} \le 8, x_{3,3} \le 3, x_{3,5} \le 5$
- $x_{4,1} \le 5, x_{4,2} \le 5, x_{4,3} \le 6, x_{4,5} \le 4$
- $x_{5,1} \le 3, x_{5,3} \le 4, x_{5,4} \le 8$
- $x_{6,2} \le 9, x_{6,4} \le 6, x_{6,5} \le 3$
All other $x_{j,d} = 0$ (enforced by $M_{j,d}=0$).

### 3. Minimum Weekly Workload Constraints
**Undergraduates (each must work at least 8 hours per week):**
$$
\sum_{d \in D} x_{j,d} \ge 8 \quad \forall j \in I
$$
- Student 1: $x_{1,1} + x_{1,3} + x_{1,5} \ge 8$
- Student 2: $x_{2,2} + x_{2,4} \ge 8$
- Student 3: $x_{3,1} + x_{3,2} + x_{3,3} + x_{3,5} \ge 8$
- Student 4: $x_{4,1} + x_{4,2} + x_{4,3} + x_{4,5} \ge 8$

**Graduates (each must work at least 7 hours per week):**
$$
\sum_{d \in D} x_{j,d} \ge 7 \quad \forall j \in G
$$
- Student 5: $x_{5,1} + x_{5,3} + x_{5,4} \ge 7$
- Student 6: $x_{6,2} + x_{6,4} + x_{6,5} \ge 7$

### 4. Non-negativity
$$
x_{j,d} \ge 0 \quad \forall j \in J, d \in D
$$

## Feasibility Sanity Check
- **Total Demand**: $5 \text{ days} \times 14 \text{ hours/day} = 70$ hours total.
- **Total Supply (Max Capacity)**:
  - Student 1: $6+0+9+0+7 = 22$
  - Student 2: $0+9+0+6+0 = 15$
  - Student 3: $4+8+3+0+5 = 20$
  - Student 4: $5+5+6+0+4 = 20$
  - Student 5: $3+0+4+8+0 = 15$
  - Student 6: $0+9+0+6+3 = 18$
  - **Total Max Supply** = $22+15+20+20+15+18 = 110$ hours.
- Since $110 \ge 70$, total capacity exceeds demand.
- **Minimum Workload Sum**: $4 \times 8 + 2 \times 7 = 32 + 14 = 46$ hours. Since $46 \le 70$, the minimum workload constraints are compatible with the coverage constraints.
- The model is feasible.