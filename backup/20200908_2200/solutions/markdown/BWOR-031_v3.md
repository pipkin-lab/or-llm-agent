## 1. Index Sets & Parameters

**Index Sets:**
*   $C = \{soy, corn, wheat\}$: Set of crop types.
*   $A = \{cow, chicken\}$: Set of animal types.
*   $T = \{AW, SS\}$: Set of time periods (Autumn-Winter, Spring-Summer).

**Parameters:**

*   **Resources:**
    *   $L_{total} = 100$ hm²: Total available land.
    *   $F_{total} = 15,000$ yuan: Total available funds.
    *   $L_{AW} = 3,500$ person-days: Available labor in Autumn-Winter.
    *   $L_{SS} = 4,000$ person-days: Available labor in Spring-Summer.

*   **Labor Costs/Income (for unused labor):**
    *   $w_{AW} = 1.8$ yuan/person-day: Wage income for unused AW labor.
    *   $w_{SS} = 2.1$ yuan/person-day: Wage income for unused SS labor.

*   **Crops ($c \in C$):**
    *   $land_{c}$: Land requirement per hm² (implicitly 1 hm² per unit of area planted).
    *   $lab_{c, AW}$: AW labor required per hm².
    *   $lab_{c, SS}$: SS labor required per hm².
    *   $income_{c}$: Net income per hm².
    *   Data from Table 1-9:
        *   Soybeans: $lab_{soy, AW}=20, lab_{soy, SS}=50, income_{soy}=175$.
        *   Corn: $lab_{corn, AW}=35, lab_{corn, SS}=75, income_{corn}=300$.
        *   Wheat: $lab_{wheat, AW}=10, lab_{wheat, SS}=40, income_{wheat}=120$.

*   **Animals ($a \in A$):**
    *   $cost_{a}$: Investment cost per unit.
    *   $land_{a}$: Land required per unit.
    *   $lab_{a, AW}$: AW labor required per unit.
    *   $lab_{a, SS}$: SS labor required per unit.
    *   $income_{a}$: Net income per unit.
    *   $U_{a}$: Capacity limit (maximum units).
    *   Data:
        *   Cows: $cost_{cow}=400, land_{cow}=1.5, lab_{cow, AW}=100, lab_{cow, SS}=50, income_{cow}=400, U_{cow}=32$.
        *   Chickens: $cost_{chicken}=3, land_{chicken}=0, lab_{chicken, AW}=0.6, lab_{chicken, SS}=0.3, income_{chicken}=2, U_{chicken}=3000$.

## 2. Decision Variables

*   $x_c$: Area planted with crop $c$ (hm²) for each $c \in C$.
*   $y_a$: Number of animals of type $a$ raised for each $a \in A$.
*   $u_{AW}$: Amount of unused labor in Autumn-Winter (person-days).
*   $u_{SS}$: Amount of unused labor in Spring-Summer (person-days).

**Domains:**
*   $x_c \ge 0, \quad \forall c \in C$
*   $y_a \ge 0, \quad \forall a \in A$
*   $u_{AW} \ge 0$
*   $u_{SS} \ge 0$

*(Note: While animal counts are technically integers, in large-scale agricultural LP models, they are often treated as continuous variables. Given the large scale (up to 3000 chickens), the fractional impact is negligible. If strict integrality is required, $y_a$ should be integer, making this a MILP. However, standard LP formulation is usually expected for this type of textbook problem unless specified otherwise. We will define them as continuous $\ge 0$ for the LP model, noting the integrality constraint if MILP is strictly required.)*

## 3. Objective Function

Maximize Total Annual Net Income ($Z$).

The total income consists of:
1.  Income from crops: $\sum_{c \in C} income_c \cdot x_c$
2.  Income from animals: $\sum_{a \in A} income_a \cdot y_a$
3.  Income from unused labor (wages): $w_{AW} \cdot u_{AW} + w_{SS} \cdot u_{SS}$

$$ \text{Maximize } Z = 175 x_{soy} + 300 x_{corn} + 120 x_{wheat} + 400 y_{cow} + 2 y_{chicken} + 1.8 u_{AW} + 2.1 u_{SS} $$

## 4. Operational Constraints

**1. Land Constraint:**
Total land used for crops and cow forage must not exceed total land.
$$ \sum_{c \in C} 1 \cdot x_c + \sum_{a \in A} land_a \cdot y_a \le L_{total} $$
$$ x_{soy} + x_{corn} + x_{wheat} + 1.5 y_{cow} + 0 y_{chicken} \le 100 $$

**2. Funds Constraint:**
Total investment for animals must not exceed available funds. (Crops require no special investment).
$$ \sum_{a \in A} cost_a \cdot y_a \le F_{total} $$
$$ 400 y_{cow} + 3 y_{chicken} \le 15000 $$

**3. Labor Constraints:**
The sum of labor used for production and unused labor (which generates wage income) must equal the total available labor for each period.

*Autumn-Winter Labor:*
$$ \sum_{c \in C} lab_{c, AW} \cdot x_c + \sum_{a \in A} lab_{a, AW} \cdot y_a + u_{AW} = L_{AW} $$
$$ 20 x_{soy} + 35 x_{corn} + 10 x_{wheat} + 100 y_{cow} + 0.6 y_{chicken} + u_{AW} = 3500 $$

*Spring-Summer Labor:*
$$ \sum_{c \in C} lab_{c, SS} \cdot x_c + \sum_{a \in A} lab_{a, SS} \cdot y_a + u_{SS} = L_{SS} $$
$$ 50 x_{soy} + 75 x_{corn} + 40 x_{wheat} + 50 y_{cow} + 0.3 y_{chicken} + u_{SS} = 4000 $$

**4. Capacity Constraints:**
The number of animals raised cannot exceed the facility limits.
$$ y_{cow} \le 32 $$
$$ y_{chicken} \le 3000 $$

**5. Non-negativity:**
$$ x_c \ge 0, \quad y_a \ge 0, \quad u_{AW} \ge 0, \quad u_{SS} \ge 0 $$

### Summary of the Mathematical Model

$$
\begin{aligned}
\text{Maximize } \quad & Z = 175 x_{soy} + 300 x_{corn} + 120 x_{wheat} + 400 y_{cow} + 2 y_{chicken} + 1.8 u_{AW} + 2.1 u_{SS} \\
\text{Subject to:} \quad & x_{soy} + x_{corn} + x_{wheat} + 1.5 y_{cow} \le 100 \\
& 400 y_{cow} + 3 y_{chicken} \le 15000 \\
& 20 x_{soy} + 35 x_{corn} + 10 x_{wheat} + 100 y_{cow} + 0.6 y_{chicken} + u_{AW} = 3500 \\
& 50 x_{soy} + 75 x_{corn} + 40 x_{wheat} + 50 y_{cow} + 0.3 y_{chicken} + u_{SS} = 4000 \\
& y_{cow} \le 32 \\
& y_{chicken} \le 3000 \\
& x_{soy}, x_{corn}, x_{wheat}, y_{cow}, y_{chicken}, u_{AW}, u_{SS} \ge 0
\end{aligned}
$$