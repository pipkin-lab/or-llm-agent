### 1. Index Sets & Parameters

**Index Sets:**
*   $I = \{1, 2, 3, 4\}$: Set of supply sources (Origins $A1, A2, A3, A4$).
*   $J = \{1, 2, 3, 4, 5, 6\}$: Set of demand destinations ($B1, B2, B3, B4, B5, B6$).

**Parameters:**
*   $s_i$: Supply available at source $i$ ($i \in I$).
    *   $s_1 = 50$
    *   $s_2 = 40$
    *   $s_3 = 60$
    *   $s_4 = 31$
    *   Total Supply $S = \sum_{i \in I} s_i = 181$
*   $d_j$: Demand required at destination $j$ ($j \in J$).
    *   $d_1 = 30$
    *   $d_2 = 50$
    *   $d_3 = 20$
    *   $d_4 = 40$
    *   $d_5 = 30$
    *   $d_6 = 11$
    *   Total Demand $D = \sum_{j \in J} d_j = 181$
*   $c_{ij}$: Unit transportation cost from source $i$ to destination $j$.

**Cost Matrix $C = [c_{ij}]$:**

| $i \backslash j$ | 1 ($B1$) | 2 ($B2$) | 3 ($B3$) | 4 ($B4$) | 5 ($B5$) | 6 ($B6$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1 ($A1$)** | 2 | 1 | 3 | 3 | 3 | 5 |
| **2 ($A2$)** | 4 | 2 | 2 | 4 | 4 | 4 |
| **3 ($A3$)** | 3 | 5 | 4 | 2 | 4 | 1 |
| **4 ($A4$)** | 4 | 2 | 2 | 1 | 2 | 2 |

**Data Completeness Check:**
Total Supply ($181$) equals Total Demand ($181$). The problem is a **balanced** transportation problem. No dummy source or destination nodes are required.

### 2. Decision Variables

Let $x_{ij}$ be the quantity of goods transported from source $i$ to destination $j$.

*   **Domain:** $x_{ij} \geq 0$ for all $i \in I, j \in J$.
*   **Integrality Note:** While physical units often imply integrality, standard Transportation Problems are typically solved as Linear Programs (LP) because the constraint matrix is totally unimodular. Given that all supply and demand values are integers, the LP relaxation will yield integer optimal solutions naturally. Therefore, explicit integer constraints are not strictly necessary for correctness, but $x_{ij}$ represents physical units. We define them as continuous non-negative variables for the standard LP formulation, noting that the solution will be integral.

### 3. Objective Function

The objective is to **minimize** the total transportation cost.

$$ \text{Minimize } Z = \sum_{i=1}^{4} \sum_{j=1}^{6} c_{ij} x_{ij} $$

Expanding the objective function with given costs:

$$
\begin{aligned}
Z = \ & 2x_{11} + 1x_{12} + 3x_{13} + 3x_{14} + 3x_{15} + 5x_{16} \\
      + \ & 4x_{21} + 2x_{22} + 2x_{23} + 4x_{24} + 4x_{25} + 4x_{26} \\
      + \ & 3x_{31} + 5x_{32} + 4x_{33} + 2x_{34} + 4x_{35} + 1x_{36} \\
      + \ & 4x_{41} + 2x_{42} + 2x_{43} + 1x_{44} + 2x_{45} + 2x_{46}
\end{aligned}
$$

### 4. Operational Constraints

**Supply Constraints (Outflow from each source cannot exceed supply):**
Since the problem is balanced ($S=D$), these will act as equalities in the optimal solution, but are formally written as inequalities $\leq$.

1.  $x_{11} + x_{12} + x_{13} + x_{14} + x_{15} + x_{16} \leq 50$
2.  $x_{21} + x_{22} + x_{23} + x_{24} + x_{25} + x_{26} \leq 40$
3.  $x_{31} + x_{32} + x_{33} + x_{34} + x_{35} + x_{36} \leq 60$
4.  $x_{41} + x_{42} + x_{43} + x_{44} + x_{45} + x_{46} \leq 31$

**Demand Constraints (Inflow to each destination must meet demand):**
Since the problem is balanced, these are equalities.

1.  $x_{11} + x_{21} + x_{31} + x_{41} = 30$
2.  $x_{12} + x_{22} + x_{32} + x_{42} = 50$
3.  $x_{13} + x_{23} + x_{33} + x_{43} = 20$
4.  $x_{14} + x_{24} + x_{34} + x_{44} = 40$
5.  $x_{15} + x_{25} + x_{35} + x_{45} = 30$
6.  $x_{16} + x_{26} + x_{36} + x_{46} = 11$

**Non-negativity Constraints:**

$$ x_{ij} \geq 0 \quad \forall i \in \{1,2,3,4\}, j \in \{1,2,3,4,5,6\} $$