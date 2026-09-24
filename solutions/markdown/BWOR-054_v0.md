# Shift Scheduling Optimization for University Computer Lab

## Model Type: LP (Linear Programming)

---

## Index Sets & Parameters

**Sets:**
- $I = \{1, 2, 3, 4, 5, 6\}$: set of students
- $I_{UG} = \{1, 2, 3, 4\}$: undergraduate students
- $I_{GR} = \{5, 6\}$: graduate students
- $D = \{1, 2, 3, 4, 5\}$: days of the week (Mon=1, Tue=2, Wed=3, Thu=4, Fri=5)

**Parameters (all values extracted from Table 5-9):**

| Parameter | Description | Values |
|---|---|---|
| $w_i$ | Hourly wage of student $i$ (yuan/h) | $w_1=10.0, w_2=10.0, w_3=9.9, w_4=9.8, w_5=10.8, w_6=11.3$ |
| $M_{i,d}$ | Max daily work hours for student $i$ on day $d$ (hours) | See table below |

**Maximum daily work hours matrix $M_{i,d}$:**

| Student | Mon ($d=1$) | Tue ($d=2$) | Wed ($d=3$) | Thu ($d=4$) | Fri ($d=5$) |
|---|---|---|---|---|---|
| 1 | 6 | 0 | 9 | 0 | 7 |
| 2 | 0 | 9 | 0 | 6 | 0 |
| 3 | 4 | 8 | 3 | 0 | 5 |
| 4 | 5 | 5 | 6 | 0 | 4 |
| 5 | 3 | 0 | 4 | 8 | 0 |
| 6 | 0 | 9 | 0 | 6 | 3 |

**Additional Parameters:**
- $H = 15$: Total operating hours per day (8:00 AM to 10:00 PM)
- $R_{UG} = 8$: Minimum weekly hours for each undergraduate student
- $R_{GR} = 7$: Minimum weekly hours for each graduate student
- $K = 2$: Maximum number of days a student can work per week
- $N_{max} = 3$: Maximum number of students on duty per day

---

## Decision Variables

For each student $i \in I$ and day $d \in D$:

- $x_{i,d} \in \{0, 1\}$: Binary variable, where $x_{i,d} = 1$ if student $i$ is scheduled for duty on day $d$, and $0$ otherwise.
- $h_{i,d} \geq 0$: Continuous variable representing the number of hours student $i$ works on day $d$.

**Domains:**
$$x_{i,d} \in \{0, 1\} \quad \forall i \in I, \forall d \in D$$
$$0 \leq h_{i,d} \leq M_{i,d} \cdot x_{i,d} \quad \forall i \in I, \forall d \in D$$

*(The upper bound coupling ensures that $h_{i,d} = 0$ when student $i$ is not scheduled on day $d$.)*

---

## Objective Function

**MINIMIZE** total weekly wage payment:

$$\min \quad Z = \sum_{i \in I} \sum_{d \in D} w_i \cdot h_{i,d}$$

**Unit verification:** $w_i$ is in yuan/hour, $h_{i,d}$ is in hours → $Z$ is in **yuan** (base unit). ✓

---

## Operational Constraints

### 1. Daily Coverage Constraint (exactly one student on duty at all times)
Since the lab requires **exactly one** student on duty for the full 15-hour day, and each scheduled student works up to their max hours, the total hours worked by all students on day $d$ must equal 15:

$$\sum_{i \in I} h_{i,d} = 15 \quad \forall d \in D$$

### 2. Binary–Hours Linking (already in domain definition)
$$h_{i,d} \leq M_{i,d} \cdot x_{i,d} \quad \forall i \in I, \forall d \in D$$

### 3. Maximum Days Worked Per Student
Each student can be assigned for duty **no more than 2 days** per week:

$$\sum_{d \in D} x_{i,d} \leq 2 \quad \forall i \in I$$

### 4. Maximum Students On Duty Per Day
No more than 3 students can be scheduled for duty per day:

$$\sum_{i \in I} x_{i,d} \leq 3 \quad \forall d \in D$$

### 5. Minimum Weekly Hours – Undergraduate Students
Each undergraduate student must work at least 8 hours per week:

$$\sum_{d \in D} h_{i,d} \geq 8 \quad \forall i \in I_{UG} = \{1, 2, 3, 4\}$$

### 6. Minimum Weekly Hours – Graduate Students
Each graduate student must work at least 7 hours per week:

$$\sum_{d \in D} h_{i,d} \geq 7 \quad \forall i \in I_{GR} = \{5, 6\}$$

### 7. Non-negativity and Bounds (explicit)
$$h_{i,d} \geq 0 \quad \forall i \in I, \forall d \in D$$
$$x_{i,d} \in \{0, 1\} \quad \forall i \in I, \forall d \in D$$

---

## Feasibility Sanity Check

**Total required coverage:** $5 \text{ days} \times 15 \text{ hrs/day} = 75$ total student-hours per week.

**Total available capacity** (sum of $M_{i,d}$ over all $i, d$):
- Student 1: $6+0+9+0+7 = 22$
- Student 2: $0+9+0+6+0 = 15$
- Student 3: $4+8+3+0+5 = 20$
- Student 4: $5+5+6+0+4 = 20$
- Student 5: $3+0+4+8+0 = 15$
- Student 6: $0+9+0+6+3 = 18$
- **Total capacity = 110 hours ≥ 75 hours** ✓

**Minimum required hours:** $4 \times 8 + 2 \times 7 = 32 + 14 = 46$ hours ≤ 75 ✓

**Per-day feasibility check:** Each day needs 15 hours from at most 3 students.
- Day 1 (Mon): Available students with $M>0$: {1(6), 3(4), 4(5), 5(3)} → 4 candidates, pick 3. Max from best 3: 6+5+4=15 ✓ (or 6+5+3=14, 6+4+3=13, 5+4+3=12). Using students 1,3,4: 6+4+5=15 ✓
- Day 2 (Tue): Available: {2(9), 3(8), 4(5), 6(9)} → pick 3. Best: 9+9+8=26 ≥ 15 ✓
- Day 3 (Wed): Available: {1(9), 3(3), 4(6), 5(4)} → pick 3. Best: 9+6+4=19 ≥ 15 ✓
- Day 4 (Thu): Available: {2(6), 4(0→excluded), 5(8), 6(6)} → students with $M>0$: {2(6), 5(8), 6(6)}. Only 3 candidates. Sum = 6+8+6 = 20 ≥ 15 ✓
- Day 5 (Fri): Available: {1(7), 3(5), 4(4), 6(3)} → pick 3. Best: 7+5+4=16 ≥ 15 ✓

All days are feasible. The model is structurally feasible.