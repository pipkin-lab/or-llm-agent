# Model Type: MILP (Mixed Integer Linear Programming)

## Parameter Inventory (Cost/Profit Extraction)

**Objective Coefficient Derivation:**
The problem asks to maximize **total rental income**.
Rule: Rent = 20% of Annual Profit per store.
Therefore, Objective Coefficient $c_{i,k} = 0.2 \times \text{Profit}_{i,k}$.

**Profit Data (Table 5-12) & Derived Rent Coefficients (in thousand Yuan):**

| ID ($i$) | Type | Area ($a_i$) | Min ($L_i$) | Max ($U_i$) | Profit if 1 ($P_{i,1}$) | Rent if 1 ($c_{i,1}=0.2 P_{i,1}$) | Profit if 2 ($P_{i,2}$) | Rent if 2 ($c_{i,2}=0.2 P_{i,2}$) | Profit if 3 ($P_{i,3}$) | Rent if 3 ($c_{i,3}=0.2 P_{i,3}$) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | Jewelry | 250 | 1 | 3 | 9 | **1.8** | 8 | **1.6** | 7 | **1.4** |
| 2 | Shoes & Hats | 350 | 1 | 2 | 10 | **2.0** | 9 | **1.8** | \ | - | - |
| 3 | Dept Store | 800 | 1 | 3 | 27 | **5.4** | 21 | **4.2** | 20 | **4.0** |
| 4 | Bookstore | 400 | 0 | 2 | 16 | **3.2** | 10 | **2.0** | \ | - | - |
| 5 | Catering | 500 | 1 | 3 | 17 | **3.4** | 15 | **3.0** | 12 | **2.4** |

*Note: "\ " indicates the number of stores is not allowed for that category (exceeds Max).*

## Index Sets & Parameters

**Sets:**
- $I = \{1, 2, 3, 4, 5\}$: Set of store categories.
- $K = \{1, 2, 3\}$: Set of possible counts of stores for a given category.

**Parameters:**
- $A = 5000$: Total available area in $m^2$.
- $r = 0.2$: Rent rate (20% of profit).
- $a_i$: Area per store for category $i$ ($m^2$).
- $L_i$: Minimum number of stores for category $i$.
- $U_i$: Maximum number of stores for category $i$.
- $c_{i,k}$: Rental income (thousand Yuan) for category $i$ if exactly $k$ stores are opened. Defined as $0.2 \times P_{i,k}$.
    - $c_{1,1}=1.8, c_{1,2}=1.6, c_{1,3}=1.4$
    - $c_{2,1}=2.0, c_{2,2}=1.8$
    - $c_{3,1}=5.4, c_{3,2}=4.2, c_{3,3}=4.0$
    - $c_{4,1}=3.2, c_{4,2}=2.0$
    - $c_{5,1}=3.4, c_{5,2}=3.0, c_{5,3}=2.4$
    - $c_{i,k} = 0$ if $k > U_i$ or $k < L_i$ is not allowed (handled by variable bounds/domains).

## Decision Variables

Let $x_{i,k}$ be a binary variable:
$$
x_{i,k} = \begin{cases} 
1 & \text{if exactly } k \text{ stores of category } i \text{ are opened} \\
0 & \text{otherwise}
\end{cases}
$$
Domain: $x_{i,k} \in \{0, 1\}$ for all $i \in I, k \in K$ such that $L_i \le k \le U_i$.
For combinations where $k < L_i$ or $k > U_i$, $x_{i,k}$ is effectively forced to 0 by constraints or omitted. To be precise, we define the domain of $k$ for each $i$ as $K_i = \{k \in \mathbb{Z} \mid L_i \le k \le U_i\}$.

## Objective Function

Maximize total rental income $Z$:

$$
\text{Maximize } Z = \sum_{i \in I} \sum_{k \in K_i} c_{i,k} x_{i,k}
$$

Explicitly:
$$
Z = 1.8x_{1,1} + 1.6x_{1,2} + 1.4x_{1,3} + 2.0x_{2,1} + 1.8x_{2,2} + 5.4x_{3,1} + 4.2x_{3,2} + 4.0x_{3,3} + 3.2x_{4,1} + 2.0x_{4,2} + 3.4x_{5,1} + 3.0x_{5,2} + 2.4x_{5,3}
$$

## Operational Constraints

**1. Exclusivity Constraint (Exactly one count per category):**
For each category $i$, exactly one of the possible store counts must be selected.
$$
\sum_{k \in K_i} x_{i,k} = 1 \quad \forall i \in I
$$
Specifically:
- $x_{1,1} + x_{1,2} + x_{1,3} = 1$
- $x_{2,1} + x_{2,2} = 1$
- $x_{3,1} + x_{3,2} + x_{3,3} = 1$
- $x_{4,1} + x_{4,2} = 1$
- $x_{5,1} + x_{5,2} + x_{5,3} = 1$

**2. Area Constraint:**
The total area occupied by all stores must not exceed the available mall area.
$$
\sum_{i \in I} \sum_{k \in K_i} a_i \cdot k \cdot x_{i,k} \le A
$$
Substituting values ($A=5000$):
$$
250(1x_{1,1} + 2x_{1,2} + 3x_{1,3}) + 350(1x_{2,1} + 2x_{2,2}) + 800(1x_{3,1} + 2x_{3,2} + 3x_{3,3}) + 400(1x_{4,1} + 2x_{4,2}) + 500(1x_{5,1} + 2x_{5,2} + 3x_{5,3}) \le 5000
$$

**3. Variable Bounds:**
$$
x_{i,k} \in \{0, 1\} \quad \forall i \in I, k \in K_i
$$

## Feasibility Sanity Check

Let's check if a feasible solution exists.
Minimum area required (using min stores):
- Cat 1: $1 \times 250 = 250$
- Cat 2: $1 \times 350 = 350$
- Cat 3: $1 \times 800 = 800$
- Cat 4: $0 \times 400 = 0$ (Min is 0)
- Cat 5: $1 \times 500 = 500$
Total Min Area = $250 + 350 + 800 + 0 + 500 = 1900 m^2$.
Since $1900 \le 5000$, the minimum requirement is feasible.

Maximum area required (using max stores):
- Cat 1: $3 \times 250 = 750$
- Cat 2: $2 \times 350 = 700$
- Cat 3: $3 \times 800 = 2400$
- Cat 4: $2 \times 400 = 800$
- Cat 5: $3 \times 500 = 1500$
Total Max Area = $750 + 700 + 2400 + 800 + 1500 = 6150 m^2$.
Since $6150 > 5000$, we cannot open the maximum number of stores for all categories. The area constraint will be binding. The model is feasible because the minimum area requirement is below the capacity.

## Final Model Summary

**Model Type:** MILP

**Variables:**
$x_{i,k} \in \{0,1\}$ for all valid $(i,k)$ pairs.

**Objective:**
$\text{Max } Z = \sum_{i \in I} \sum_{k \in K_i} c_{i,k} x_{i,k}$

**Constraints:**
1. $\sum_{k \in K_i} x_{i,k} = 1, \quad \forall i \in I$
2. $\sum_{i \in I} \sum_{k \in K_i} a_i k x_{i,k} \le 5000$
3. $x_{i,k} \in \{0,1\}$