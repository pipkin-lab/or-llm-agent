To solve this problem, we must formulate a mathematical model for three distinct scenarios. Since the scenarios have different structural constraints (number of tasks per person), we will define a base set of indices and parameters, then define the specific constraints and decision variables for each scenario (a), (b), and (c).

### 1. Index Sets & Parameters

**Index Sets:**
*   $I = \{X, Y, Z, R\}$: Set of persons. Let $i \in I$.
*   $J = \{A, B, C, D, F\}$: Set of tasks. Let $j \in J$.

**Parameters:**
*   $c_{ij}$: Time required for person $i$ to complete task $j$ (in units).
    *   $c_{X,A}=25, c_{X,B}=29, c_{X,C}=31, c_{X,D}=42, c_{X,F}=37$
    *   $c_{Y,A}=39, c_{Y,B}=38, c_{Y,C}=26, c_{Y,D}=20, c_{Y,F}=33$
    *   $c_{Z,A}=34, c_{Z,B}=27, c_{Z,C}=28, c_{Z,D}=40, c_{Z,F}=32$
    *   $c_{R,A}=24, c_{R,B}=42, c_{R,C}=36, c_{R,D}=23, c_{R,F}=45$

---

### Model Type Declaration
**Model Type:** MILP (Mixed Integer Linear Program)
*   The decision variables are binary (0 or 1).
*   The objective function is linear.
*   The constraints are linear.
*   *Note: Although the objective and constraints are linear, the variables are discrete, making it an Integer Linear Program (ILP), a subset of MILP.*

---

### Decision Variables (Common to all scenarios)

Let $x_{ij}$ be a binary decision variable:
$$
x_{ij} = \begin{cases} 
1 & \text{if person } i \text{ is assigned to task } j \\
0 & \text{otherwise}
\end{cases}
$$
Domain: $x_{ij} \in \{0, 1\} \quad \forall i \in I, j \in J$

---

### Objective Function

For all three scenarios, the goal is to minimize the total completion time.
$$
\text{Minimize } Z = \sum_{i \in I} \sum_{j \in J} c_{ij} x_{ij}
$$

---

### Operational Constraints

The constraints differ by scenario. We define them separately.

#### Scenario (a): One person takes two tasks, others take one.
*   **Task Assignment Constraint:** Each of the 5 tasks must be assigned to exactly one person.
    $$
    \sum_{i \in I} x_{ij} = 1 \quad \forall j \in J
    $$
*   **Person Load Constraint:** The total number of tasks assigned to each person must sum to 5 (since there are 5 tasks and 4 people, and the distribution is 2-1-1-1).
    $$
    \sum_{j \in J} x_{ij} \in \{1, 2\} \quad \forall i \in I
    $$
    *Note: This can be linearized as $1 \le \sum_{j \in J} x_{ij} \le 2$ for all $i$, combined with the total sum constraint below.*
    $$
    \sum_{i \in I} \sum_{j \in J} x_{ij} = 5
    $$
    *Alternatively, a more precise formulation for "one person has 2, three have 1" is to ensure no one has 3 or more, and the total is 5. Since $\sum x_{ij}$ per person is an integer, $1 \le \sum_j x_{ij} \le 2$ for all $i$ ensures the distribution is exactly $\{2,1,1,1\}$ because the sum of four integers each in $[1,2]$ must be 5.*

#### Scenario (b): Either X or Z takes two tasks; Y and R take one each.
*   **Task Assignment Constraint:** Each of the 5 tasks must be assigned to exactly one person.
    $$
    \sum_{i \in I} x_{ij} = 1 \quad \forall j \in J
    $$
*   **Specific Person Load Constraints:**
    *   Y takes exactly one task:
        $$
        \sum_{j \in J} x_{Yj} = 1
        $$
    *   R takes exactly one task:
        $$
        \sum_{j \in J} x_{Rj} = 1
        $$
    *   X takes either 1 or 2 tasks (but the logic "X or Z takes two" implies one of them has 2 and the other has 1, or we just enforce the specific counts below):
        *   Actually, the prompt says "Either X or Z must take on two tasks... and Y and R each take one." This implies the load distribution is fixed as $\{2,1,1,1\}$ where the person with 2 is either X or Z.
        *   Constraint for X:
            $$
            \sum_{j \in J} x_{Xj} \in \{1, 2\}
            $$
        *   Constraint for Z:
            $$
            \sum_{j \in J} x_{Zj} \in \{1, 2\}
            $$
        *   To enforce that *exactly one* of them has 2 (and the other has 1), we can use the total sum. Since $Y=1$ and $R=1$, the remaining tasks for X and Z is $5-1-1=3$. Thus, $\sum x_{Xj} + \sum x_{Zj} = 3$.
        *   Since $x$ are integers, if $X$ has 1, $Z$ must have 2, and if $X$ has 2, $Z$ must have 1. This naturally satisfies "Either X or Z takes two".
        *   So, explicit constraints are:
            $$
            \sum_{j \in J} x_{Xj} + \sum_{j \in J} x_{Zj} = 3
            $$
            $$
            1 \le \sum_{j \in J} x_{Xj} \le 2
            $$
            $$
            1 \le \sum_{j \in J} x_{Zj} \le 2
            $$

#### Scenario (c): Each person completes one task; A and B must be completed; one of C, D, F is unassigned.
*   **Task Assignment Constraint (Completed Tasks):**
    *   Task A must be assigned to exactly one person:
        $$
        \sum_{i \in I} x_{iA} = 1
        $$
    *   Task B must be assigned to exactly one person:
        $$
        \sum_{i \in I} x_{iB} = 1
        $$
    *   Tasks C, D, F: Exactly one of these is assigned, and the other two are not. Or simply, the sum of assignments for C, D, F across all people is 1 (since 4 people take 4 tasks total, 2 are fixed A,B, so 2 slots left for 3 people? No.
    *   Let's re-read: "Each person completes one task". There are 4 people. So exactly 4 tasks are performed in total.
    *   "Tasks A and B must be completed". So A and B are among the 4.
    *   "One among C, D, or F may be left unassigned". This implies 2 of {C, D, F} are completed, and 1 is not.
    *   Total tasks completed = $A + B + (\text{2 from } \{C,D,F\}) = 4$ tasks.
    *   This fits "Each person completes one task" (4 people, 4 tasks).
    *   Constraints:
        1.  Each person takes exactly one task:
            $$
            \sum_{j \in J} x_{ij} = 1 \quad \forall i \in I
            $$
        2.  Task A is assigned to exactly one person:
            $$
            \sum_{i \in I} x_{iA} = 1
            $$
        3.  Task B is assigned to exactly one person:
            $$
            \sum_{i \in I} x_{iB} = 1
            $$
        4.  Since A and B are taken by 2 distinct people (implied by "each person completes one task" and tasks are distinct entities assigned to people, plus sum over people = 1 for each task), the remaining 2 people must take 2 tasks from {C, D, F}.
        5.  The sum of assignments for tasks C, D, and F must be 2 (since 2 tasks remain to be assigned to the remaining 2 people):
            $$
            \sum_{i \in I} (x_{iC} + x_{iD} + x_{iF}) = 2
            $$
        *   *Check:* Does this guarantee that one of C, D, F is unassigned? Yes. If 2 tasks are chosen from a set of 3, one is left out.
        *   *Check:* Does this guarantee each person has one task? Yes, via $\sum_j x_{ij} = 1$.

### Summary of Formulation for Solver Implementation

**Global Data:**
*   $I = [X, Y, Z, R]$
*   $J = [A, B, C, D, F]$
*   $C_{ij}$ matrix as listed in Parameters.

**Scenario A Model:**
*   **Vars:** $x_{ij} \in \{0,1\}$
*   **Obj:** Min $\sum c_{ij} x_{ij}$
*   **Cons:**
    *   $\forall j \in J: \sum_{i \in I} x_{ij} = 1$
    *   $\forall i \in I: 1 \le \sum_{j \in J} x_{ij} \le 2$

**Scenario B Model:**
*   **Vars:** $x_{ij} \in \{0,1\}$
*   **Obj:** Min $\sum c_{ij} x_{ij}$
*   **Cons:**
    *   $\forall j \in J: \sum_{i \in I} x_{ij} = 1$
    *   $\sum_{j \in J} x_{Yj} = 1$
    *   $\sum_{j \in J} x_{Rj} = 1$
    *   $1 \le \sum_{j \in J} x_{Xj} \le 2$
    *   $1 \le \sum_{j \in J} x_{Zj} \le 2$
    *   $\sum_{j \in J} x_{Xj} + \sum_{j \in J} x_{Zj} = 3$ (Redundant if previous two and total sum 5 are present, but good for clarity. Actually, total sum is implied by task constraints. So $Sum_X + Sum_Z = 3$ is the key link.)

**Scenario C Model:**
*   **Vars:** $x_{ij} \in \{0,1\}$
*   **Obj:** Min $\sum c_{ij} x_{ij}$
*   **Cons:**
    *   $\forall i \in I: \sum_{j \in J} x_{ij} = 1$
    *   $\sum_{i \in I} x_{iA} = 1$
    *   $\sum_{i \in I} x_{iB} = 1$
    *   $\sum_{i \in I} (x_{iC} + x_{iD} + x_{iF}) = 2$

*(Note: In Scenario C, the constraint $\sum_{i \in I} x_{iA} = 1$ and $\sum_{i \in I} x_{iB} = 1$ combined with $\sum_{j} x_{ij}=1$ for all $i$ ensures A and B are assigned to different people, as one person cannot take two tasks.)*