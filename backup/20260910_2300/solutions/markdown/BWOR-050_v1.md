# Optimization Model: 200-meter Medley Relay Team Selection

## 1. Index Sets & Parameters

**Index Sets:**
*   $S$: Set of strokes in the medley relay.
    *   $S = \{ \text{Backstroke (B)}, \text{Breaststroke (Br)}, \text{Butterfly (Bu)}, \text{Freestyle (F)} \}$
    *   Index $j$ iterates over $S$.
*   $A$: Set of available athletes.
    *   $A = \{ \text{Zhao}, \text{Qian}, \text{Zhang}, \text{Wang}, \text{Zhou} \}$
    *   Index $i$ iterates over $A$.

**Parameters:**
*   $t_{ij}$: The 50-meter swimming time (in seconds) for athlete $i$ in stroke $j$.

**Data Table ($t_{ij}$):**

| Stroke ($j$) | Zhao (1) | Qian (2) | Zhang (3) | Wang (4) | Zhou (5) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Backstroke** | 37.7 | 32.9 | 33.8 | 37.0 | 35.4 |
| **Breaststroke** | 43.4 | 33.1 | 42.2 | 34.7 | 41.8 |
| **Butterfly** | 33.3 | 28.5 | 38.9 | 30.4 | 33.6 |
| **Freestyle** | 29.2 | 26.4 | 29.6 | 28.5 | 31.1 |

*Note: The medley relay consists of 4 legs of 50 meters each (Backstroke, Breaststroke, Butterfly, Freestyle). Each athlete can swim only one leg.*

## 2. Decision Variables

Let $x_{ij}$ be a binary decision variable defined as:
$$
x_{ij} = 
\begin{cases} 
1 & \text{if athlete } i \text{ is assigned to stroke } j \\
0 & \text{otherwise}
\end{cases}
$$
for all $i \in A, j \in S$.

**Domain:**
$$ x_{ij} \in \{0, 1\} \quad \forall i \in A, j \in S $$

## 3. Objective Function

The goal is to minimize the expected total time of the 200-meter medley relay. The total time is the sum of the times of the four assigned swimmers.

$$
\text{Minimize } Z = \sum_{i \in A} \sum_{j \in S} t_{ij} x_{ij}
$$

## 4. Operational Constraints

**1. Stroke Assignment Constraint:**
Each stroke $j$ in the medley must be swum by exactly one athlete.
$$
\sum_{i \in A} x_{ij} = 1 \quad \forall j \in S
$$

**2. Athlete Uniqueness Constraint:**
Each athlete $i$ can be assigned to at most one stroke (an athlete cannot swim multiple legs in a single relay).
$$
\sum_{j \in S} x_{ij} \le 1 \quad \forall i \in A
$$

**3. Non-negativity/Integrality:**
$$
x_{ij} \in \{0, 1\} \quad \forall i \in A, j \in S
$$

---

### Summary of the Formulation

$$
\begin{aligned}
\text{Minimize} \quad & \sum_{i=1}^{5} \sum_{j=1}^{4} t_{ij} x_{ij} \\
\text{Subject to:} \quad & \sum_{i=1}^{5} x_{ij} = 1, \quad \forall j \in \{1, 2, 3, 4\} \\
& \sum_{j=1}^{4} x_{ij} \le 1, \quad \forall i \in \{1, 2, 3, 4, 5\} \\
& x_{ij} \in \{0, 1\}, \quad \forall i \in \{1, \dots, 5\}, j \in \{1, \dots, 4\}
\end{aligned}
$$

*(Where stroke indices correspond to: 1=Backstroke, 2=Breaststroke, 3=Butterfly, 4=Freestyle, and athlete indices correspond to: 1=Zhao, 2=Qian, 3=Zhang, 4=Wang, 5=Zhou)*