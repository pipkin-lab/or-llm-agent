## Model Type Declaration
**Model Type:** MILP (Mixed Integer Linear Programming)

**Reasoning:** The problem involves assigning discrete entities (athletes) to discrete roles (strokes). The decision variables are binary (assignment or not). The objective function and constraints are linear.

## Index Sets & Parameters

**Index Sets:**
*   $I$: Set of athletes, $I = \{1, 2, 3, 4, 5\}$ corresponding to $\{Zhao, Qian, Zhang, Wang, Zhou\}$.
*   $J$: Set of strokes, $J = \{1, 2, 3, 4\}$ corresponding to $\{Backstroke, Breaststroke, Butterfly, Freestyle\}$.

**Parameters:**
*   $c_{ij}$: The 50-meter swimming time (in seconds) for athlete $i$ in stroke $j$.

**Data Table ($c_{ij}$):**

| Stroke $j \setminus$ Athlete $i$ | 1 (Zhao) | 2 (Qian) | 3 (Zhang) | 4 (Wang) | 5 (Zhou) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1 (Backstroke)** | 37.7 | 32.9 | 33.8 | 37.0 | 35.4 |
| **2 (Breaststroke)** | 43.4 | 33.1 | 42.2 | 34.7 | 41.8 |
| **3 (Butterfly)** | 33.3 | 28.5 | 38.9 | 30.4 | 33.6 |
| **4 (Freestyle)** | 29.2 | 26.4 | 29.6 | 28.5 | 31.1 |

## Decision Variables

Let $x_{ij}$ be a binary decision variable defined as:
$$
x_{ij} = 
\begin{cases} 
1 & \text{if athlete } i \text{ is assigned to stroke } j \\
0 & \text{otherwise}
\end{cases}
$$
**Domain:** $x_{ij} \in \{0, 1\} \quad \forall i \in I, j \in J$

## Objective Function

Minimize the total expected time for the 200-meter medley relay. Since the relay consists of four 50-meter legs (one for each stroke), the total time is the sum of the times of the assigned athletes.

$$
\text{Minimize } Z = \sum_{i \in I} \sum_{j \in J} c_{ij} x_{ij}
$$

## Operational Constraints

1.  **Each stroke must be assigned to exactly one athlete:**
    For every stroke $j \in J$, the sum of assignments across all athletes must equal 1.
    $$
    \sum_{i \in I} x_{ij} = 1 \quad \forall j \in J
    $$

2.  **Each athlete can be assigned to at most one stroke:**
    An athlete cannot swim multiple legs in a single relay race. For every athlete $i \in I$, the sum of assignments across all strokes must be less than or equal to 1.
    $$
    \sum_{j \in J} x_{ij} \le 1 \quad \forall i \in I
    $$

3.  **Binary Constraints:**
    $$
    x_{ij} \in \{0, 1\} \quad \forall i \in I, j \in J
    $$

## Feasibility Sanity Check

*   **Supply vs. Demand:** We have 5 athletes (supply) and 4 strokes (demand). Since Supply > Demand, it is feasible to assign a unique athlete to each stroke.
*   **Constraint Consistency:** The constraints ensure a one-to-one mapping from strokes to a subset of athletes. There are no conflicting lower bounds or capacities that would render the problem infeasible. The "at most one" constraint for athletes handles the surplus athlete (one athlete will remain unassigned).