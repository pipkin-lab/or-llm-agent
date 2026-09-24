This is an **Integer Linear Programming (ILP)** problem (a variant of the Assignment Problem). We will solve three separate scenarios based on the assignment constraints provided.

### 1. Index Sets & Parameters

**Index Sets:**
*   $P = \{X, Y, Z, R\}$: Set of persons.
*   $T = \{A, B, C, D, F\}$: Set of tasks.

**Parameters:**
$c_{p,t}$: Time required for person $p$ to complete task $t$ (extracted from Table 5-3).

| Person | Task A | Task B | Task C | Task D | Task F |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **X** | 25 | 29 | 31 | 42 | 37 |
| **Y** | 39 | 38 | 26 | 20 | 33 |
| **Z** | 34 | 27 | 28 | 40 | 32 |
| **R** | 24 | 42 | 36 | 23 | 45 |

### 2. Decision Variables

Let $x_{p,t}$ be a binary variable:
$$
x_{p,t} = \begin{cases} 
1 & \text{if person } p \text{ is assigned to task } t \\
0 & \text{otherwise}
\end{cases}
$$
for all $p \in P$ and $t \in T$.

### 3. Objective Function

For each scenario, the objective is to minimize the total completion time:
$$
\text{Minimize } Z = \sum_{p \in P} \sum_{t \in T} c_{p,t} x_{p,t}
$$

### 4. Operational Constraints

The constraints vary by scenario.

#### Scenario (a): One person takes on two tasks, the other three take one each.
1.  **Task Assignment:** Every task must be assigned to exactly one person.
    $$ \sum_{p \in P} x_{p,t} = 1 \quad \forall t \in T $$
2.  **Person Workload:**
    *   Total workload is 5 tasks (since there are 5 tasks and all are assigned).
    *   One person has workload 2, three persons have workload 1.
    *   We introduce binary variables $y_p$ to indicate if person $p$ is the one doing two tasks.
    *   $y_p = 1$ if person $p$ does 2 tasks, else 0.
    *   $\sum_{p \in P} y_p = 1$ (Exactly one person is the double-task worker).
    *   Workload constraint for each person $p$:
        $$ \sum_{t \in T} x_{p,t} = 1 + y_p \quad \forall p \in P $$

#### Scenario (b): Either X or Z takes on two tasks, Y and R take one each.
1.  **Task Assignment:** Every task must be assigned to exactly one person.
    $$ \sum_{p \in P} x_{p,t} = 1 \quad \forall t \in T $$
2.  **Person Workload:**
    *   Y takes exactly 1 task: $\sum_{t \in T} x_{Y,t} = 1$
    *   R takes exactly 1 task: $\sum_{t \in T} x_{R,t} = 1$
    *   X and Z together take the remaining 3 tasks. One takes 2, the other takes 1.
    *   Constraint for X: $\sum_{t \in T} x_{X,t} \in \{1, 2\}$
    *   Constraint for Z: $\sum_{t \in T} x_{Z,t} \in \{1, 2\}$
    *   Since total tasks for X and Z is 3 (5 total - 1 for Y - 1 for R), and they must be integers summing to 3, the condition "one is 2, one is 1" is automatically satisfied if we constrain:
        $$ \sum_{t \in T} x_{X,t} + \sum_{t \in T} x_{Z,t} = 3 $$
        $$ 1 \le \sum_{t \in T} x_{X,t} \le 2 $$
        $$ 1 \le \sum_{t \in T} x_{Z,t} \le 2 $$
    *(Note: The problem states "Either X or Z must take on two tasks". This implies the other takes one. The constraints above enforce that one is 2 and the other is 1, satisfying the condition.)*

#### Scenario (c): Each person completes one task, but tasks A and B must be completed, while one among C, D, or F may be left unassigned.
1.  **Task Assignment:**
    *   Tasks A and B must be assigned:
        $$ \sum_{p \in P} x_{p,A} = 1 $$
        $$ \sum_{p \in P} x_{p,B} = 1 $$
    *   Exactly one of C, D, F is assigned (since 4 people take 4 tasks total, and A, B are taken, one of C/D/F is taken, one is left unassigned? Wait. 4 people, 1 task each = 4 tasks assigned. Tasks A and B are assigned. That leaves 2 task-slots. There are 3 remaining tasks (C, D, F). So exactly 2 of {C, D, F} are assigned, and 1 is left unassigned.
    *   Let's re-read carefully: "Each person completes one task... one among C, D, or F may be left unassigned."
    *   Total tasks assigned = 4.
    *   Assigned tasks include A and B.
    *   Remaining slots = 2. Remaining tasks = C, D, F.
    *   So, exactly 2 of {C, D, F} are assigned, and 1 is NOT assigned.
    *   Constraints:
        $$ \sum_{p \in P} x_{p,C} + \sum_{p \in P} x_{p,D} + \sum_{p \in P} x_{p,F} = 2 $$
        $$ \sum_{p \in P} x_{p,t} \le 1 \quad \forall t \in \{C, D, F\} $$
        (Actually, since each person takes 1 task, and there are 4 people, the total sum of all $x$ is 4. The constraint $\sum_{t \in \{C,D,F\}} \sum_{p \in P} x_{p,t} = 2$ combined with A=1, B=1 ensures the structure.)
2.  **Person Workload:**
    *   Each person takes exactly 1 task:
        $$ \sum_{t \in T} x_{p,t} = 1 \quad \forall p \in P $$

### 5. Solution Derivation (Manual Calculation for Verification)

**Scenario (a): One person does 2 tasks, others do 1.**
Total tasks = 5.
Let's evaluate the "Double Tasker".
If X does 2:
X's best 2 tasks: A(25), B(29) -> Sum 54. Remaining tasks C, D, F for Y, Z, R.
Y->C(26), Z->D(40)? No.
Let's look at individual bests.
R is best at A(24).
Y is best at D(20).
X is best at A(25).
Z is best at B(27).

Let's try assigning the "Double" role to the person with the most flexible or efficient secondary task.
Option 1: X does 2.
X does A and B? Cost 25+29=54.
Remaining tasks C, D, F for Y, Z, R.
Y->C(26), Z->F(32), R->D(23). Total = 54 + 26 + 32 + 23 = 135.
Y->C(26), Z->D(40), R->F(45). Total = 54 + 26 + 40 + 45 = 165.
Y->F(33), Z->C(28), R->D(23). Total = 54 + 33 + 28 + 23 = 138.
Y->D(20), Z->C(28), R->F(45). Total = 54 + 20 + 28 + 45 = 147.
Best for X double (A,B) is 135.
Can X do other pairs?
X A, C (25+31=56). Rem B, D, F.
R->B(42) bad. Z->B(27). Y->D(20). R->F(45).
Z->B(27), Y->D(20), R->F(45). Sum = 56 + 27 + 20 + 45 = 148.
X A, F (25+37=62). Rem B, C, D.
Z->B(27), Y->C(26), R->D(23). Sum = 62 + 27 + 26 + 23 = 138.
X B, C (29+31=60). Rem A, D, F.
R->A(24), Y->D(20), Z->F(32). Sum = 60 + 24 + 20 + 32 = 136.
X B, F (29+37=66). Rem A, C, D.
R->A(24), Y->C(26), Z->D(40). Sum = 66 + 24 + 26 + 40 = 156.
X C, D (31+42=73). Too high.
So best for X double is 135 (X: A,B; Y: C; Z: F; R: D).

Option 2: Y does 2.
Y's best 2: D(20), C(26) -> 46. Rem A, B, F for X, Z, R.
R->A(24), Z->B(27), X->F(37). Sum = 46 + 24 + 27 + 37 = 134.
Check other combos for Y double (D,C):
R->A(24), X->B(29), Z->F(32). Sum = 46 + 24 + 29 + 32 = 131.
Z->A(34), R->B(42)... no.
Let's check Y doing D and F (20+33=53). Rem A, B, C.
R->A(24), Z->B(27), X->C(31). Sum = 53 + 24 + 27 + 31 = 135.
Y doing C and F (26+33=59). Rem A, B, D.
R->A(24), Z->B(27), X->D(42). Sum = 59 + 24 + 27 + 42 = 152.
Y doing C and D (26+20=46) was best so far.
Let's check Y doing A and D (39+20=59). Rem B, C, F.
Z->B(27), X->C(31), R->F(45). Sum = 59 + 27 + 31 + 45 = 162.
So best for Y double is 131 (Y: C,D; R: A; Z: B; X: F).
Assignment:
Y: C, D
R: A
Z: B
X: F
Cost: 26+20 + 24 + 27 + 37 = 134?
Wait, 26+20=46. 24+27+37=88. 46+88=134.
Let's re-calculate:
Y(C)=26, Y(D)=20. Sum=46.
R(A)=24.
Z(B)=27.
X(F)=37.
Total = 26+20+24+27+37 = 134.
Is there a better one?
Y(C)=26, Y(F)=33 (Sum 59).
R(A)=24, Z(B)=27, X(D)=42. Sum = 59+24+27+42 = 152.
Y(D)=20, Y(F)=33 (Sum 53).
R(A)=24, Z(B)=27, X(C)=31. Sum = 53+24+27+31 = 135.
So 134 is the best for Y double.

Option 3: Z does 2.
Z's best 2: B(27), C(28) -> 55. Rem A, D, F for X, Y, R.
R->A(24), Y->D(20), X->F(37). Sum = 55 + 24 + 20 + 37 = 136.
Z(B)=27, Z(C)=28.
X(A)=25, Y(D)=20, R(F)=45. Sum = 55 + 25 + 20 + 45 = 145.
Z(B)=27, Z(F)=32 (Sum 59). Rem A, C, D.
R->A(24), Y->C(26), X->D(42). Sum = 59 + 24 + 26 + 42 = 151.
Z(C)=28, Z(D)=40 (Sum 68). Too high.
Z(A)=34, Z(B)=27 (Sum 61). Rem C, D, F.
Y->C(26), Y->D(20)... wait, Y can only do 1.
Rem C, D, F for X, Y, R.
Y->D(20), X->C(31), R->F(45). Sum = 61 + 20 + 31 + 45 = 157.
So best for Z double is 136.

Option 4: R does 2.
R's best 2: A(24), D(23) -> 47. Rem B, C, F for X, Y, Z.
Z->B(27), Y->C(26), X->F(37). Sum = 47 + 27 + 26 + 37 = 137.
R(A)=24, R(D)=23.
X->B(29), Y->C(26), Z->F(32). Sum = 47 + 29 + 26 + 32 = 134.
R(A)=24, R(F)=45 (Sum 69). Too high.
R(B)=42... no.
So best for R double is 134.
Let's verify R double 134:
R: A, D (24+23=47)
X: B (29)
Y: C (26)
Z: F (32)
Total: 47 + 29 + 26 + 32 = 134.

Comparing Scenario (a) bests:
X double: 135
Y double: 134
Z double: 136
R double: 134

Minimum for (a) is **134**.
There are two optimal solutions with cost 134:
1. Y does C, D; R does A; Z does B; X does F.
2. R does A, D; X does B; Y does C; Z does F.

**Scenario (b): X or Z does 2 tasks. Y and R do 1 each.**
Case 1: X does 2. (Z does 1).
We need to assign 5 tasks.
Y takes 1, R takes 1, X takes 2, Z takes 1.
Let's test X's double task options again, but now Z is fixed to 1 task.
X(A,B) = 54. Rem C, D, F for Y, Z, R.
Y, Z, R take 1 each.
We need to assign C, D, F to Y, Z, R to minimize cost.
Matrix for Y,Z,R on C,D,F:
Y: 26, 20, 33
Z: 28, 40, 32
R: 36, 23, 45
Min assignment:
Y->D(20), Z->C(28), R->F(45) -> 20+28+45=93. Total 54+93=147.
Y->C(26), Z->F(32), R->D(23) -> 26+32+23=81. Total 54+81=135.
Y->F(33), Z->C(28), R->D(23) -> 33+28+23=84. Total 54+84=138.
Best for X(A,B) is 135.

X(A,C) = 56. Rem B, D, F for Y, Z, R.
Y: 38, 20, 33
Z: 27, 40, 32
R: 42, 23, 45
Min assignment:
Y->D(20), Z->B(27), R->F(45) -> 20+27+45=92. Total 56+92=148.
Y->F(33), Z->B(27), R->D(23) -> 33+27+23=83. Total 56+83=139.
Y->B(38)... no.
Best for X(A,C) is 139.

X(A,F) = 62. Rem B, C, D for Y, Z, R.
Y: 38, 26, 20
Z: 27, 28, 40
R: 42, 36, 23
Min assignment:
Y->C(26), Z->B(27), R->D(23) -> 26+27+23=76. Total 62+76=138.
Y->D(20), Z->B(27), R->C(36) -> 20+27+36=83. Total 62+83=145.
Y->B(38)... no.
Best for X(A,F) is 138.

X(B,C) = 60. Rem A, D, F for Y, Z, R.
Y: 39, 20, 33
Z: 34, 40, 32
R: 24, 23, 45
Min assignment:
Y->D(20), Z->F(32), R->A(24) -> 20+32+24=76. Total 60+76=136.
Y->F(33), Z->A(34), R->D(23) -> 33+34+23=90. Total 60+90=150.
Y->A(39)... no.
Best for X(B,C) is 136.

X(B,F) = 66. Rem A, C, D for Y, Z, R.
Y: 39, 26, 20
Z: 34, 28, 40
R: 24, 36, 23
Min assignment:
Y->C(26), Z->A(34), R->D(23) -> 26+34+23=83. Total 66+83=149.
Y->D(20), Z->A(34), R->C(36) -> 20+34+36=90. Total 66+90=156.
Y->A(39)... no.
Best for X(B,F) is 149.

X(C,D) = 73. Rem A, B, F.
Y: 39, 38, 33
Z: 34, 27, 32
R: 24, 42, 45
Min: R->A(24), Z->B(27), Y->F(33) -> 24+27+33=84. Total 73+84=157.

Best for Case 1 (X double) is **135** (X: A,B; Y: C; Z: F; R: D).

Case 2: Z does 2. (X does 1).
Z's double options:
Z(B,C) = 55. Rem A, D, F for X, Y, R.
X: 25, 42, 37
Y: 39, 20, 33
R: 24, 23, 45
Min assignment:
R->A(24), Y->D(20), X->F(37) -> 24+20+37=81. Total 55+81=136.
R->D(23), Y->F(33), X->A(25) -> 23+33+25=81. Total 55+81=136.
R->A(24), X->D(42)... no.
Best for Z(B,C) is 136.

Z(B,F) = 59. Rem A, C, D for X, Y, R.
X: 25, 31, 42
Y: 39, 26, 20
R: 24, 36, 23
Min assignment:
R->A(24), Y->D(20), X->C(31) -> 24+20+31=75. Total 59+75=134.
R->D(23), Y->C(26), X->A(25) -> 23+26+25=74. Total 59+74=133.
R->C(36)... no.
Best for Z(B,F) is 133.
Assignment: Z: B, F; R: D; Y: C; X: A.
Cost: 27+32 + 23 + 26 + 25 = 133.

Z(C,D) = 68. Rem A, B, F.
X: 25, 29, 37
Y: 39, 38, 33
R: 24, 42, 45
Min: R->A(24), X->B(29), Y->F(33) -> 24+29+33=86. Total 68+86=154.

Z(A,B) = 61. Rem C, D, F.
X: 31, 42, 37
Y: 26, 20, 33
R: 36, 23, 45
Min: Y->D(20), R->F(45)? No.
Y->C(26), R->D(23), X->F(37) -> 26+23+37=86. Total 61+86=147.
Y->D(20), X->C(31), R->F(45) -> 20+31+45=96. Total 61+96=157.
Y->F(33), X->C(31), R->D(23) -> 33+31+23=87. Total 61+87=148.
Best for Z(A,B) is 147.

Z(A,C) = 62. Rem B, D, F.
X: 29, 42, 37
Y: 38, 20, 33
R: 42, 23, 45
Min: Y->D(20), X->B(29), R->F(45) -> 20+29+45=94. Total 62+94=156.
Y->F(33), X->B(29), R->D(23) -> 33+29+23=85. Total 62+85=147.
Best for Z(A,C) is 147.

Z(A,F) = 66. Rem B, C, D.
X: 29, 31, 42
Y: 38, 26, 20
R: 42, 36, 23
Min: Y->D(20), X->C(31), R->B(42) -> 20+31+42=93. Total 66+93=159.
Y->C(26), X->B(29), R->D(23) -> 26+29+23=78. Total 66+78=144.
Best for Z(A,F) is 144.

Z(C,F) = 60. Rem A, B, D.
X: 25, 29, 42
Y: 39, 38, 20
R: 24, 42, 23
Min: R->A(24), Y->D(20), X->B(29) -> 24+20+29=73. Total 60+73=133.
R->D(23), Y->A(39)... no.
R->A(24), X->D(42)... no.
Best for Z(C,F) is 133.
Assignment: Z: C, F; R: A; Y: D; X: B.
Cost: 28+32 + 24 + 20 + 29 = 133.

Comparing Case 1 (X double) best 135 and Case 2 (Z double) best 133.
Minimum for (b) is **133**.
There are two optimal solutions with cost 133:
1. Z: B, F; R: D; Y: C; X: A.
2. Z: C, F; R: A; Y: D; X: B.

**Scenario (c): Each person does 1 task. A, B assigned. One of C, D, F unassigned.**
This is a standard assignment problem where we choose 4 tasks out of 5 (excluding one of C,D,F) and assign to 4 people.
Actually, it's easier to view it as: Assign 4 people to 4 tasks.
Tasks A and B are mandatory.
We must choose 2 tasks from {C, D, F} to assign.
So we have 3 sub-cases based on which task is left unassigned.

Case 1: F is unassigned. Tasks {A, B, C, D} assigned to {X, Y, Z, R}.
Matrix:
   A   B   C   D
X  25  29  31  42
Y  39  38  26  20
Z  34  27  28  40
R  24  42  36  23

Find min assignment.
R->A(24) is strong.
Y->D(20) is strong.
Z->B(27) is strong.
X->C(31) is left?
Let's check:
R-A (24), Y-D (20), Z-B (27), X-C (31).
Sum = 24+20+27+31 = 102.
Is there better?
X-A(25), Y-C(26), Z-B(27), R-D(23).
Sum = 25+26+27+23 = 101.
Check if valid:
X->A, Y->C, Z->B, R->D.
All distinct persons, all distinct tasks.
Cost 101.
Another:
X-A(25), Y-D(20), Z-B(27), R-C(36). Sum = 25+20+27+36 = 108.
X-C(31), Y-B(38)... no.
Z-A(34), Y-D(20), R-B(42)... no.
Let's check X-B(29), Y-C(26), Z-A(34), R-D(23). Sum = 29+26+34+23 = 112.
Let's check X-D(42)... no.
So for {A,B,C,D}, min is **101** (X:A, Y:C, Z:B, R:D).

Case 2: D is unassigned. Tasks {A, B, C, F} assigned to {X, Y, Z, R}.
Matrix:
   A   B   C   F
X  25  29  31  37
Y  39  38  26  33
Z  34  27  28  32
R  24  42  36  45

Min assignment:
R->A(24).
Z->B(27).
Y->C(26).
X->F(37).
Sum = 24+27+26+37 = 114.
Check alternatives:
X->A(25), Z->B(27), Y->C(26), R->F(45). Sum = 25+27+26+45 = 123.
X->C(31), Y->F(33), Z->B(27), R->A(24). Sum = 31+33+27+24 = 115.
X->B(29), Y->C(26), Z->F(32), R->A(24). Sum = 29+26+32+24 = 111.
X->B(29), Y->F(33), Z->C(28), R->A(24). Sum = 29+33+28+24 = 114.
So for {A,B,C,F}, min is **111** (X:B, Y:C, Z:F, R:A).

Case 3: C is unassigned. Tasks {A, B, D, F} assigned to {X, Y, Z, R}.
Matrix:
   A   B   D   F
X  25  29  42  37
Y  39  38  20  33
Z  34  27  40  32
R  24  42  23  45

Min assignment:
Y->D(20).
R->A(24).
Z->B(27).
X->F(37).
Sum = 20+24+27+37 = 108.
Check alternatives:
X->A(25), Y->D(20), Z->B(27), R->F(45). Sum = 25+20+27+45 = 117.
X->B(29), Y->D(20), Z->F(32), R->A(24). Sum = 29+20+32+24 = 105.
Check this one:
X->B (29)
Y->D (20)
Z->F (32)
R->A (24)
Sum = 29+20+32+24 = 105.
Is there lower?
X->A(25), Y->F(33), Z->B(27), R->D(23). Sum = 25+33+27+23 = 108.
X->F(37), Y->D(20), Z->B(27), R->A(24). Sum = 37+20+27+24 = 108.
So for {A,B,D,F}, min is **105** (X:B, Y:D, Z:F, R:A).

Comparing the three cases:
1. F unassigned: 101
2. D unassigned: 111
3. C unassigned: 105

Minimum for (c) is **101**.
Assignment: X: A, Y: C, Z: B, R: D. (Task F is unassigned).

### Final Answers

**Scenario (a)**
Minimum Total Time: **134**
Optimal Assignments (Two possible):
1.  **Y** takes **C** and **D**; **R** takes **A**; **Z** takes **B**; **X** takes **F**.
2.  **R** takes **A** and **D**; **X** takes **B**; **Y** takes **C**; **Z** takes **F**.

**Scenario (b)**
Minimum Total Time: **133**
Optimal Assignments (Two possible):
1.  **Z** takes **B** and **F**; **R** takes **D**; **Y** takes **C**; **X** takes **A**.
2.  **Z** takes **C** and **F**; **R** takes **A**; **Y** takes **D**; **X** takes **B**.

**Scenario (c)**
Minimum Total Time: **101**
Optimal Assignment:
**X** takes **A**; **Y** takes **C**; **Z** takes **B**; **R** takes **D**.
(Task **F** is left unassigned).