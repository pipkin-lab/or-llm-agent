## Mathematical Model Formulation

### Model Type
**LP** (Linear Programming). All variables are continuous (hours can be fractional; the problem does not require integer hours).

### Index Sets & Parameters

**Index Sets:**
- $I = \{1, 2, 3, 4\}$: Set of undergraduate students.
- $G = \{5, 6\}$: Set of graduate students.
- $K = I \cup G = \{1, 2, 3, 4, 5, 6\}$: Set of all students.
- $D = \{1, 2, 3, 4, 5\}$: Set of days (1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri).

**Parameters:**
- $w_k$: Hourly wage for student $k$ (yuan/hour).
- $M_{k,d}$: Maximum available work hours for student $k$ on day $d$.
- $H$: Required hours of coverage per day = 14.
- $L_U$: Minimum weekly hours for undergraduates = 8.
- $L_G$: Minimum weekly hours for graduates = 7.

**Parameter Values (extracted from Table 5-9):**

| $k$ | $w_k$ | $M_{k,1}$ (Mon) | $M_{k,2}$ (Tue) | $M_{k,3}$ (Wed) | $M_{k,4}$ (Thu) | $M_{k,5}$ (Fri) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 10.0 | 6 | 0 | 9 | 0 | 7 |
| 2 | 10.0 | 0 | 9 | 0 | 6 | 0 |
| 3 | 9.9 | 4 | 8 | 3 | 0 | 5 |
| 4 | 9.8 | 5 | 5 | 6 | 0 | 4 |
| 5 | 10.8 | 3 | 0 | 4 | 8 | 0 |
| 6 | 11.3 | 0 | 9 | 0 | 6 | 3 |

### Decision Variables
Let $x_{k,d}$ be the number of hours student $k$ works on day $d$.

**Domain:**
$$x_{k,d} \ge 0, \quad \forall k \in K, \forall d \in D$$

### Objective Function
Minimize the total wage payment:
$$ \text{Minimize } Z = \sum_{k \in K} \sum_{d \in D} w_k x_{k,d} $$

### Operational Constraints

**1. Daily Coverage Constraint**
The lab must have exactly one student on duty for all 14 hours of operation each day. Therefore, the sum of hours worked by all students on any given day must equal 14.
$$ \sum_{k \in K} x_{k,d} = 14, \quad \forall d \in D $$

**2. Maximum Availability Constraint**
A student cannot work more than their maximum available hours on any given day.
$$ x_{k,d} \le M_{k,d}, \quad \forall k \in K, \forall d \in D $$

**3. Minimum Weekly Hours for Undergraduates**
Each undergraduate must work at least 8 hours per week.
$$ \sum_{d \in D} x_{k,d} \ge 8, \quad \forall k \in I $$

**4. Minimum Weekly Hours for Graduates**
Each graduate must work at least 7 hours per week.
$$ \sum_{d \in D} x_{k,d} \ge 7, \quad \forall k \in G $$