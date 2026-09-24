**Model Type:** LP (Linear Program)

### 1. Index Sets & Parameters

**Index Sets:**
*   $I = \{1, 2, 3\}$: Set of origins (suppliers).
*   $J = \{A, B, C\}$: Set of destinations (demands).

**Parameters:**

*   **Transportation Costs ($c_{ij}$)**: Cost to ship one unit from origin $i$ to destination $j$.
    *   $c_{1A}=1, c_{1B}=2, c_{1C}=2$
    *   $c_{2A}=1, c_{2B}=4, c_{2C}=5$
    *   $c_{3A}=2, c_{3B}=3, c_{3C}=3$
*   **Supply Capacities ($S_i$)**: Maximum units available at origin $i$.
    *   $S_1 = 20$
    *   $S_2 = 40$
    *   $S_3 = 30$
*   **Demand Requirements ($D_j$)**: Required units at destination $j$.
    *   $D_A = 30$
    *   $D_B = 20$
    *   $D_C = 20$
*   **Unit Storage Costs ($h_i$)**: Cost incurred for each unit *not shipped* from origin $i$.
    *   $h_1 = 5$
    *   $h_2 = 4$
    *   $h_3 = 3$
*   **Minimum Shipment Constraints ($MinShip_i$)**:
    *   $MinShip_1 = 0$ (No minimum specified for origin 1)
    *   $MinShip_2 = 38$
    *   $MinShip_3 = 27$

**Total Supply** = $20 + 40 + 30 = 90$ units.
**Total Demand** = $30 + 20 + 20 = 70$ units.
Since Total Supply > Total Demand, there will be unsold inventory. The problem specifies a storage cost for unshipped units, which acts as a penalty for not shipping.

### 2. Decision Variables

Let $x_{ij}$ be the number of units shipped from origin $i$ to destination $j$.
*   $x_{ij} \in \mathbb{R}_{\ge 0}$ for all $i \in I, j \in J$.

*(Note: We do not need separate variables for unshipped units because the unshipped quantity from origin $i$ is implicitly determined by $S_i - \sum_{j \in J} x_{ij}$.)*

### 3. Objective Function

We want to minimize the **total cost**, which consists of:
1.  Transportation costs for shipped units.
2.  Storage costs for unshipped units.

For origin $i$, the amount shipped is $\sum_{j \in J} x_{ij}$.
The amount unshipped (stored) is $S_i - \sum_{j \in J} x_{ij}$.
The storage cost for origin $i$ is $h_i \left( S_i - \sum_{j \in J} x_{ij} \right)$.

Total Cost $Z$ to minimize:
$$
\text{Minimize } Z = \sum_{i \in I} \sum_{j \in J} c_{ij} x_{ij} + \sum_{i \in I} h_i \left( S_i - \sum_{j \in J} x_{ij} \right)
$$

Expanding the storage term:
$$
Z = \sum_{i \in I} \sum_{j \in J} c_{ij} x_{ij} + \sum_{i \in I} h_i S_i - \sum_{i \in I} \sum_{j \in J} h_i x_{ij}
$$

Since $\sum_{i \in I} h_i S_i$ is a constant ($5(20) + 4(40) + 3(30) = 100 + 160 + 90 = 350$), we can either keep it for clarity or drop it. It is safer to keep the full expression or combine coefficients.
The coefficient for each variable $x_{ij}$ in the objective function is effectively $(c_{ij} - h_i)$. However, keeping the structure explicit is less prone to error.

Let's write the objective in terms of the variables $x_{ij}$:
$$
\text{Minimize } Z = (c_{1A}-h_1)x_{1A} + (c_{1B}-h_1)x_{1B} + (c_{1C}-h_1)x_{1C} + (c_{2A}-h_2)x_{2A} + (c_{2B}-h_2)x_{2B} + (c_{2C}-h_2)x_{2C} + (c_{3A}-h_3)x_{3A} + (c_{3B}-h_3)x_{3B} + (c_{3C}-h_3)x_{3C} + 350
$$

Calculating the net coefficients $(c_{ij} - h_i)$:
*   **Origin 1** ($h_1=5$):
    *   $x_{1A}: 1 - 5 = -4$
    *   $x_{1B}: 2 - 5 = -3$
    *   $x_{1C}: 2 - 5 = -3$
*   **Origin 2** ($h_2=4$):
    *   $x_{2A}: 1 - 4 = -3$
    *   $x_{2B}: 4 - 4 = 0$
    *   $x_{2C}: 5 - 4 = 1$
*   **Origin 3** ($h_3=3$):
    *   $x_{3A}: 2 - 3 = -1$
    *   $x_{3B}: 3 - 3 = 0$
    *   $x_{3C}: 3 - 3 = 0$

So the objective is:
$$
\text{Minimize } Z = -4x_{1A} - 3x_{1B} - 3x_{1C} - 3x_{2A} + 0x_{2B} + 1x_{2C} - 1x_{3A} + 0x_{3B} + 0x_{3C} + 350
$$

### 4. Operational Constraints

**A. Supply Constraints (with explicit storage allocation):**
According to Rule 9, since Supply > Demand, we must account for all supply. The variables $x_{ij}$ represent shipped units. The unshipped units are implicitly $S_i - \sum x_{ij}$. We must ensure that the sum of shipped units does not exceed supply.
$$
\sum_{j \in J} x_{1A} + x_{1B} + x_{1C} \le 20
$$
$$
\sum_{j \in J} x_{2A} + x_{2B} + x_{2C} \le 40
$$
$$
\sum_{j \in J} x_{3A} + x_{3B} + x_{3C} \le 30
$$

**B. Demand Constraints:**
Demand must be met exactly (standard transportation assumption unless stated otherwise, and given specific "at least" constraints on origins, the destinations are usually hard requirements).
$$
x_{1A} + x_{2A} + x_{3A} = 30
$$
$$
x_{1B} + x_{2B} + x_{3B} = 20
$$
$$
x_{1C} + x_{2C} + x_{3C} = 20
$$

**C. Minimum Shipment Constraints:**
The problem states: "at least 38 units must be shipped from origin 2 and at least 27 units from origin 3."
$$
x_{2A} + x_{2B} + x_{2C} \ge 38
$$
$$
x_{3A} + x_{3B} + x_{3C} \ge 27
$$
(Origin 1 has no minimum shipment constraint specified, so it defaults to 0).

**D. Non-negativity:**
$$
x_{ij} \ge 0 \quad \forall i \in I, j \in J
$$

---

### Feasibility Sanity Check

1.  **Total Supply**: 90.
2.  **Total Demand**: 70.
3.  **Minimum Shipments**:
    *   Origin 2 min: 38.
    *   Origin 3 min: 27.
    *   Sum of mins: $38 + 27 = 65$.
    *   Remaining demand to be met by Origin 1: $70 - 65 = 5$.
    *   Origin 1 Supply: 20.
    *   Can Origin 1 ship 5? Yes ($5 \le 20$).
4.  **Consistency**:
    *   If Origin 2 ships 38 and Origin 3 ships 27, total shipped is 65.
    *   Origin 1 must ship the remaining 5 units to meet total demand of 70.
    *   Unshipped units:
        *   Origin 1: $20 - 5 = 15$.
        *   Origin 2: $40 - 38 = 2$.
        *   Origin 3: $30 - 27 = 3$.
    *   Total unshipped: $15 + 2 + 3 = 20$.
    *   Total shipped: $5 + 38 + 27 = 70$.
    *   Total units accounted for: $70 + 20 = 90$. Matches total supply.

The constraints are consistent and feasible.

### Final Formulation Summary

**Model Type:** LP

**Indices:**
*   $I = \{1, 2, 3\}$
*   $J = \{A, B, C\}$

**Parameters:**
*   $c_{ij}$:
    *   Row 1: 1, 2, 2
    *   Row 2: 1, 4, 5
    *   Row 3: 2, 3, 3
*   $S_i$: 20, 40, 30
*   $D_j$: 30, 20, 20
*   $h_i$: 5, 4, 3
*   $Min_i$: 0, 38, 27

**Variables:**
*   $x_{ij} \ge 0$ for all $i, j$

**Objective:**
$$
\text{Minimize } Z = \sum_{i \in I} \sum_{j \in J} (c_{ij} - h_i) x_{ij} + \sum_{i \in I} h_i S_i
$$
Substituting values:
$$
\text{Minimize } Z = -4x_{1A} - 3x_{1B} - 3x_{1C} - 3x_{2A} + 0x_{2B} + 1x_{2C} - 1x_{3A} + 0x_{3B} + 0x_{3C} + 350
$$

**Constraints:**
1.  **Supply Caps:**
    *   $x_{1A} + x_{1B} + x_{1C} \le 20$
    *   $x_{2A} + x_{2B} + x_{2C} \le 40$
    *   $x_{3A} + x_{3B} + x_{3C} \le 30$
2.  **Demand Requirements:**
    *   $x_{1A} + x_{2A} + x_{3A} = 30$
    *   $x_{1B} + x_{2B} + x_{3B} = 20$
    *   $x_{1C} + x_{2C} + x_{3C} = 20$
3.  **Minimum Shipments:**
    *   $x_{2A} + x_{2B} + x_{2C} \ge 38$
    *   $x_{3A} + x_{3B} + x_{3C} \ge 27$
4.  **Non-negativity:**
    *   $x_{ij} \ge 0$