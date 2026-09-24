# Optimization Model: Course Selection Problem

## 1. Index Sets & Parameters

**Sets:**
*   $C$: Set of all available courses.
    *   $C = \{ \text{Calculus (Ca)}, \text{Operations Research (OR)}, \text{Data Structures (DS)}, \text{Managerial Statistics (MS)}, \text{Computer Simulation (CSim)}, \text{Computer Programming (CP)}, \text{Forecasting (F)} \}$
    *   Let indices be: $1=\text{Ca}, 2=\text{OR}, 3=\text{DS}, 4=\text{MS}, 5=\text{CSim}, 6=\text{CP}, 7=\text{F}$.
*   $K$: Set of course categories/requirements.
    *   $K = \{ \text{Math (M)}, \text{Ops Research (O)}, \text{Computer Science (CS)} \}$
*   $P$: Set of prerequisite pairs $(i, j)$ where course $i$ is a prerequisite for course $j$.
    *   $P = \{ (6, 5), (6, 3), (1, 4), (4, 7) \}$
    *   Meaning:
        *   CP (6) $\rightarrow$ CSim (5)
        *   CP (6) $\rightarrow$ DS (3)
        *   Ca (1) $\rightarrow$ MS (4)
        *   MS (4) $\rightarrow$ F (7)

**Parameters:**
*   $a_{ik}$: Binary parameter equal to 1 if course $i \in C$ satisfies requirement category $k \in K$, and 0 otherwise.
    *   **Math (M, $k=1$):**
        *   Ca (1): 1
        *   OR (2): 1
        *   DS (3): 1
        *   MS (4): 1
        *   CSim (5): 0
        *   CP (6): 0
        *   F (7): 1
    *   **Ops Research (O, $k=2$):**
        *   Ca (1): 0
        *   OR (2): 1
        *   DS (3): 0
        *   MS (4): 1
        *   CSim (5): 1
        *   CP (6): 0
        *   F (7): 1
    *   **Computer Science (CS, $k=3$):**
        *   Ca (1): 0
        *   OR (2): 0
        *   DS (3): 1
        *   MS (4): 0
        *   CSim (5): 1
        *   CP (6): 1
        *   F (7): 0

*   $r_k$: Minimum number of courses required for category $k$.
    *   $r_{\text{Math}} = 2$
    *   $r_{\text{OR}} = 2$
    *   $r_{\text{CS}} = 2$

## 2. Decision Variables

Let $x_i$ be a binary decision variable for each course $i \in C$:
$$
x_i = 
\begin{cases} 
1 & \text{if course } i \text{ is selected} \\
0 & \text{otherwise}
\end{cases}
$$
Domain: $x_i \in \{0, 1\} \quad \forall i \in C$

## 3. Objective Function

Minimize the total number of courses selected.

$$
\text{Minimize } Z = \sum_{i=1}^{7} x_i
$$

## 4. Operational Constraints

### A. Category Requirements
The student must select at least $r_k$ courses for each category $k$.

$$
\sum_{i \in C} a_{i, \text{Math}} x_i \ge 2
$$
$$
\sum_{i \in C} a_{i, \text{OR}} x_i \ge 2
$$
$$
\sum_{i \in C} a_{i, \text{CS}} x_i \ge 2
$$

*Expanded Form:*
1.  **Math:** $x_1 + x_2 + x_3 + x_4 + x_7 \ge 2$
2.  **OR:** $x_2 + x_4 + x_5 + x_7 \ge 2$
3.  **CS:** $x_3 + x_5 + x_6 \ge 2$

### B. Prerequisite Constraints
If a course with prerequisites is selected, its prerequisites must also be selected.
For each pair $(i, j) \in P$ where $i$ is the prerequisite for $j$:
$$
x_i \ge x_j
$$
*(This ensures that if $x_j = 1$, then $x_i$ must be 1. If $x_j = 0$, $x_i$ can be 0 or 1, but the objective function will push $x_i$ to 0 if it's not needed for other constraints.)*

Specific Constraints:
1.  **CSim requires CP:** $x_6 \ge x_5$
2.  **DS requires CP:** $x_6 \ge x_3$
3.  **MS requires Ca:** $x_1 \ge x_4$
4.  **F requires MS:** $x_4 \ge x_7$

### C. Domain Constraints
$$
x_i \in \{0, 1\} \quad \forall i \in \{1, 2, 3, 4, 5, 6, 7\}
$$

---

### Verification & Solution Analysis (Mental Check)

To ensure the model is correct, let's trace a potential solution.
We need 2 CS courses. The CS courses are DS(3), CSim(5), CP(6).
Both DS(3) and CSim(5) require CP(6).
Therefore, to get 2 CS courses, we **must** take CP(6).
So, $x_6 = 1$.
The second CS course must be either DS(3) or CSim(5).

**Case 1: Take DS(3)**
$x_3 = 1$.
CS Requirement Met: $\{CP, DS\}$.
Prereqs Met: CP is taken.
Math Requirement: Need 2. Current Math courses taken: DS (1). Need 1 more from $\{Ca, OR, MS, F\}$.
OR Requirement: Need 2. Current OR courses taken: None (DS is not OR). Need 2 from $\{OR, MS, CSim, F\}$.

If we take **OR(2)**:
$x_2 = 1$.
Math Count: $x_3 + x_2 = 1 + 1 = 2$. (Math Met)
OR Count: $x_2 = 1$. Need 1 more OR course.
Remaining candidates for OR: $\{MS, CSim, F\}$.
- If take **MS(4)**: Requires Ca(1).
  - Take $x_4=1, x_1=1$.
  - OR Count: $x_2 + x_4 = 2$. (OR Met)
  - Math Count: $x_3 + x_2 + x_4 + x_1 = 1+1+1+1 = 4 \ge 2$. (Math Met)
  - CS Count: $x_3 + x_6 = 2$. (CS Met)
  - Total Courses: $\{DS, CP, OR, MS, Ca\}$. Count = 5.
  - Check Prereqs:
    - DS req CP: Yes.
    - MS req Ca: Yes.
  - This is a valid solution with **5 courses**.

- Can we do better? (4 courses?)
  - We established CP is mandatory. (1 course)
  - We need 1 more CS: DS or CSim. Let's say DS. (2 courses)
  - We need 2 OR courses.
  - We need 2 Math courses.
  - Current set: $\{CP, DS\}$.
  - DS contributes to Math.
  - We need 1 more Math.
  - We need 2 OR.
  - If we pick OR(2) and MS(4):
    - OR count: 2 (OR, MS).
    - Math count: DS, OR, MS = 3.
    - But MS requires Ca(1).
    - Set: $\{CP, DS, OR, MS, Ca\}$. Count = 5.
  - If we pick OR(2) and F(7):
    - OR count: 2 (OR, F).
    - Math count: DS, OR, F = 3.
    - F requires MS(4). MS requires Ca(1).
    - Set: $\{CP, DS, OR, F, MS, Ca\}$. Count = 6.
  - If we pick MS(4) and F(7) as the 2 OR courses:
    - OR count: 2 (MS, F).
    - Math count: DS, MS, F = 3.
    - F requires MS. MS requires Ca.
    - Set: $\{CP, DS, MS, F, Ca\}$. Count = 5.
    - Check Math: DS, MS, F, Ca (4 math courses).
    - Check OR: MS, F (2 OR courses).
    - Check CS: CP, DS (2 CS courses).
    - This is also 5 courses.

Is 4 possible?
If we take CP and CSim (instead of DS).
Set: $\{CP, CSim\}$.
CSim is OR and CS. Not Math.
Need 2 Math.
Need 1 more OR (since CSim is 1).
Need 2 CS? No, CS is met by CP, CSim.
So we need 2 Math and 1 OR from remaining $\{Ca, OR, DS, MS, F\}$.
Note: If we pick DS, it adds CS (already met) and Math.
Let's try to fill the gaps with minimum additions.
Need: 2 Math, 1 OR.
Candidates:
- OR(2): 1 OR, 1 Math.
- Ca(1): 1 Math.
- MS(4): 1 OR, 1 Math. (Requires Ca)
- F(7): 1 OR, 1 Math. (Requires MS, Ca)
- DS(3): 1 Math. (Requires CP - already have)

If we pick OR(2) and Ca(1):
OR count: 1 (from CSim) + 1 (from OR) = 2. (Met)
Math count: 1 (from OR) + 1 (from Ca) = 2. (Met)
Set: $\{CP, CSim, OR, Ca\}$. Count = 4.
Let's verify this solution.
Courses: CP, CSim, OR, Ca.
1. **CS Req (2):** CP, CSim. (2 courses). **OK**.
2. **OR Req (2):** CSim, OR. (2 courses). **OK**.
3. **Math Req (2):** OR, Ca. (2 courses). **OK**.
4. **Prereqs:**
   - CSim requires CP. (CP is selected). **OK**.
   - OR has no prereqs listed. **OK**.
   - Ca has no prereqs listed. **OK**.
   
This solution has **4 courses**.

Can we do 3?
Min courses = 4?
Let's check if 3 is possible.
To get 2 CS, we need CP + (DS or CSim). That's 2 courses.
If we pick CP and CSim:
CS: 2.
OR: 1 (CSim).
Math: 0.
We have 1 slot left (total 3 courses).
We need 1 more OR and 2 Math.
One course cannot provide 2 Math and 1 OR simultaneously unless it's double counted? No, a course counts as 1 in each category it belongs to.
Does any course provide 2 Math? No.
So one course can provide at most 1 Math.
We need 2 Math. With 1 course left, we can get at most 1 Math.
So Math requirement (2) cannot be met with only 1 additional course.
Thus, 3 courses is impossible.

Therefore, the minimum is 4.

**Final Answer Formulation:**
The model correctly identifies that the minimum number of courses is 4. One such set is {Calculus, Operations Research, Computer Simulation, Computer Programming}. Another is {Calculus, Managerial Statistics, Computer Simulation, Computer Programming} (Check: CS: CP, CSim; OR: CSim, MS; Math: MS, Ca? No, Ca is Math, MS is Math. Yes. Prereqs: CSim<-CP, MS<-Ca. All good. Wait, MS requires Ca. So {Ca, MS, CP, CSim} works too).

The question asks for "the minimum number... and which courses". Since there might be multiple optimal solutions, the model finds the minimum number (4). The specific courses can be any subset satisfying the constraints with size 4.

**Model Summary:**
1.  **Sets**: Courses $C$, Categories $K$, Prereqs $P$.
2.  **Variables**: $x_i \in \{0,1\}$.
3.  **Objective**: Min $\sum x_i$.
4.  **Constraints**:
    *   $\sum a_{i,M} x_i \ge 2$
    *   $\sum a_{i,O} x_i \ge 2$
    *   $\sum a_{i,CS} x_i \ge 2$
    *   $x_{prereq} \ge x_{course}$ for all prereq pairs.

This is a Mixed Integer Linear Programming (MILP) problem (specifically a 0-1 IP).