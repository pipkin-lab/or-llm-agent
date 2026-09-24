# Mathematical Model for Student Q&A Duty Scheduling

## 1. Index Sets & Parameters

**Index Sets:**
- $I = \{1, 2, 3, 4, 5, 6\}$: Set of all students.
- $I_{UG} = \{1, 2, 3, 4\}$: Set of undergraduate students.
- $I_{GR} = \{5, 6\}$: Set of graduate students.
- $D = \{1, 2, 3, 4, 5\}$: Set of days (Monday to Friday).

**Parameters:**
- $w_i$: Hourly wage of student $i$ (yuan/hour).
  - $w_1=10.0, w_2=10.0, w_3=9.9, w_4=9.8, w_5=10.8, w_6=11.3$
- $M_{i,d}$: Maximum available work hours for student $i$ on day $d$.
  - **Day 1 (Mon):** $M_{1,1}=6, M_{2,1}=0, M_{3,1}=4, M_{4,1}=5, M_{5,1}=3, M_{6,1}=0$
  - **Day 2 (Tue):** $M_{1,2}=0, M_{2,2}=9, M_{3,2}=8, M_{4,2}=5, M_{5,2}=0, M_{6,2}=9$
  - **Day 3 (Wed):** $M_{1,3}=9, M_{2,3}=0, M_{3,3}=3, M_{4,3}=6, M_{5,3}=4, M_{6,3}=0$
  - **Day 4 (Thu):** $M_{1,4}=0, M_{2,4}=6, M_{3,4}=0, M_{4,4}=0, M_{5,4}=8, M_{6,4}=6$
  - **Day 5 (Fri):** $M_{1,5}=7, M_{2,5}=0, M_{3,5}=5, M_{4,5}=4, M_{5,5}=0, M_{6,5}=3$
- $H$: Required coverage hours per day.
  - $H = 14$ hours (8:00 AM to 10:00 PM).
- $L_{i}$: Minimum weekly work hours required for student $i$.
  - For $i \in I_{UG}$: $L_i = 8$ hours.
  - For $i \in I_{GR}$: $L_i = 7$ hours.

## 2. Decision Variables

- $x_{i,d}$: Continuous variable representing the number of hours student $i$ works on day $d$.
  - Domain: $x_{i,d} \ge 0 \quad \forall i \in I, d \in D$.
  - *Note: Since wages are linear and coverage is continuous time-based, continuous variables are appropriate unless specific shift blocks are enforced. Given "hours" are the unit and no discrete shift definitions are provided, continuous relaxation is standard for this type of linear programming formulation.*

## 3. Objective Function

Minimize the total weekly wage payment:

$$
\text{Minimize } Z = \sum_{i \in I} \sum_{d \in D} w_i x_{i,d}
$$

## 4. Operational Constraints

**1. Daily Coverage Constraint:**
The total hours worked by all students on any given day must equal the required coverage of 14 hours.

$$
\sum_{i \in I} x_{i,d} = 14 \quad \forall d \in D
$$

**2. Maximum Availability Constraint:**
The hours worked by a student on a specific day cannot exceed their maximum available hours for that day.

$$
x_{i,d} \le M_{i,d} \quad \forall i \in I, d \in D
$$

**3. Minimum Weekly Work Hours Constraint:**
Each student must work at least their required minimum hours over the 5-day week.

$$
\sum_{d \in D} x_{i,d} \ge L_i \quad \forall i \in I
$$
*(Where $L_i = 8$ for $i \in \{1,2,3,4\}$ and $L_i = 7$ for $i \in \{5,6\}$)*

**4. Non-negativity Constraint:**
$$
x_{i,d} \ge 0 \quad \forall i \in I, d \in D
$$