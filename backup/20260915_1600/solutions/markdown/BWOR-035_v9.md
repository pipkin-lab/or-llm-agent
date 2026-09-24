To formulate the optimization model for this strategic bombing problem, we must carefully analyze the physical constraints, resource limitations, and the probabilistic nature of the objective.

### 1. Problem Analysis & Parameter Extraction

**Objective:** Maximize the probability that **at least one** of the 4 key parts is destroyed.
Since the parts are independent (implied, as destroying any one is sufficient and no dependency is stated), the probability of destroying the target is:
$$ P(\text{Target Destroyed}) = 1 - P(\text{None Destroyed}) = 1 - \prod_{i=1}^{4} (1 - P_i) $$
where $P_i$ is the probability that part $i$ is destroyed.
To maximize this, we must **minimize** the product of survival probabilities:
$$ \text{Minimize } Z = \prod_{i=1}^{4} (1 - P_i) $$
This is a **Non-Linear** objective function.

**Decision Variables:**
Let $x_{ih}$ be the number of heavy bombs dropped on part $i$.
Let $x_{il}$ be the number of light bombs dropped on part $i$.
Since bombs are discrete units, these are **Integer** variables.

**Probability Model:**
The probability that a single bomb does **not** destroy part $i$ is:
- Heavy: $1 - p_{ih}$
- Light: $1 - p_{il}$

Assuming independent hits, the probability that part $i$ survives after receiving $x_{ih}$ heavy and $x_{il}$ light bombs is:
$$ S_i = (1 - p_{ih})^{x_{ih}} (1 - p_{il})^{x_{il}} $$
We aim to minimize $\prod S_i$.

**Constraints:**

1.  **Fuel Consumption:**
    Total fuel $\le 48,000$ liters.
    Fuel consumption depends on the distance to the target and the type of bomb carried.
    
    *Note on Mission Profile:* The problem states "fuel consumption for the round trip" and mentions specific rates for "carrying a heavy bomb," "carrying a light bomb," and "flying empty."
    
    Let's analyze the flight profile for a single sortie to part $i$ at distance $d_i$:
    -   **Outbound Leg (Loaded):** The plane carries bombs.
        -   If carrying heavy bombs: Rate = 2 km/L.
        -   If carrying light bombs: Rate = 3 km/L.
        -   *Ambiguity Resolution:* A plane cannot carry *only* heavy or *only* light bombs if it drops a mix on different parts? No, typically in these problems, a "sortie" is defined by the load. However, the variables $x_{ih}$ and $x_{il}$ imply we are deciding the *total* number of bombs of each type used on each part.
        
        Let's look at the structure. Usually, these problems assume a fleet of identical planes or a single plane making multiple runs? The text says "A fleet... is ordered...". It doesn't specify the number of planes. It gives total resource limits (48,000 L fuel, 48 heavy, 32 light). This implies we are allocating the **total inventory** of bombs to the targets.
        
        How is fuel calculated?
        "For each bombing sortie... fuel consumption for the round trip... plus 100L takeoff/landing."
        
        We need to define what constitutes a "sortie" in terms of bomb delivery.
        Standard interpretation for this class of OR problem (Knapsack-like with probabilistic objective):
        We decide how many heavy bombs ($H$) and light bombs ($L$) are sent to each target.
        However, a plane carries a specific load. Does a plane carry *only* heavy bombs or *only* light bombs?
        - If a plane carries heavy bombs, it flies at 2 km/L (outbound) and 4 km/L (return, empty).
        - If a plane carries light bombs, it flies at 3 km/L (outbound) and 4 km/L (return, empty).
        
        Can a plane carry a mix? The rates are defined "When carrying a heavy bomb" and "When carrying a light bomb". It does not provide a mixed-load rate. This strongly implies that **each sortie is dedicated to one bomb type**.
        
        Let $n_{ih}$ be the number of sorties carrying heavy bombs to part $i$.
        Let $n_{il}$ be the number of sorties carrying light bombs to part $i$.
        
        Wait, the variables $x_{ih}$ and $x_{il}$ are the *number of bombs*. If a plane carries multiple bombs, the fuel consumption per bomb is not simply additive if the plane carries $k$ bombs, because the rate is per liter of fuel, not per bomb.
        
        Let's re-read carefully: "When carrying a heavy bomb, each liter of fuel allows the aircraft to fly 2 km". This is a fuel efficiency rate.
        Fuel needed for one round trip to distance $d$ carrying heavy bombs:
        Outbound: $d / 2$ liters.
        Return: $d / 4$ liters.
        Takeoff/Landing: 100 liters.
        Total Fuel per Heavy Sortie to $i$: $F_{ih} = \frac{d_i}{2} + \frac{d_i}{4} + 100 = 0.75 d_i + 100$.
        
        Total Fuel per Light Sortie to $i$:
        Outbound: $d / 3$ liters.
        Return: $d / 4$ liters.
        Takeoff/Landing: 100 liters.
        Total Fuel per Light Sortie to $i$: $F_{il} = \frac{d_i}{3} + \frac{d_i}{4} + 100 = \frac{7 d_i}{12} + 100 \approx 0.5833 d_i + 100$.
        
        **Crucial Assumption:** How many bombs does one sortie carry?
        The problem does not state the bomb capacity of a single aircraft.
        However, it gives total limits: 48 heavy, 32 light.
        If the number of bombs per sortie is not 1, we cannot determine the fuel cost per bomb.
        Standard interpretation in such textbook problems where "number of bombs" is the variable and fuel is a constraint: **Assume 1 bomb per sortie** OR **Assume the "sortie" variable represents the delivery of one unit of that bomb type**.
        
        Let's check the magnitudes.
        Distance ~500 km.
        Fuel per heavy sortie ~ $0.75(500) + 100 = 475$ L.
        Fuel per light sortie ~ $0.583(500) + 100 = 391.6$ L.
        Total Fuel Limit: 48,000 L.
        Max sorties if all heavy: $48000 / 475 \approx 101$ sorties.
        Max bombs available: 48 Heavy + 32 Light = 80 bombs.
        If 1 bomb = 1 sortie, max fuel used $\approx 80 \times 500 = 40,000$ L, which is within the 48,000 limit.
        This suggests the fuel constraint might not be binding if we use all bombs, or it will bind if we prioritize distance.
        
        If the capacity per plane is $>1$, the fuel per bomb would be lower. But without that data, we must assume **1 bomb per sortie** or that the variables $x_{ih}, x_{il}$ represent the **number of sorties** which deliver 1 bomb each. Given the discrete nature of "bombs" and the lack of "plane capacity" parameter, the most robust model treats $x_{ih}$ and $x_{il}$ as the number of **bombs** allocated, and assumes the fuel cost is incurred **per bomb** (i.e., 1 bomb per flight).
        
        Let's verify this assumption. If a plane could carry 10 bombs, the fuel cost per bomb would be $\approx 47$ L. Total fuel for 80 bombs would be $\approx 3760$ L, well below 48,000. The fuel constraint would be irrelevant. In OR problems, usually all constraints are potentially binding. The fact that fuel is a hard limit (48,000) and comparable in magnitude to the total "flight fuel" for 80 single-bomb sorties ($\sim 40,000$) strongly supports the **1 bomb per sortie** interpretation.

        **Revised Variables:**
        $x_{ih} \in \mathbb{Z}_{\ge 0}$: Number of heavy bombs (sorties) assigned to part $i$.
        $x_{il} \in \mathbb{Z}_{\ge 0}$: Number of light bombs (sorties) assigned to part $i$.

2.  **Resource Constraints:**
    -   **Heavy Bombs:** $\sum_{i=1}^{4} x_{ih} \le 48$
    -   **Light Bombs:** $\sum_{i=1}^{4} x_{il} \le 32$
    -   **Fuel:** $\sum_{i=1}^{4} [x_{ih} F_{ih} + x_{il} F_{il}] \le 48,000$

    **Calculate Fuel Coefficients ($F$):**
    
    *   **Part 1 ($d=450$):**
        $F_{1h} = 0.75(450) + 100 = 337.5 + 100 = 437.5$
        $F_{1l} = \frac{7}{12}(450) + 100 = 262.5 + 100 = 362.5$
        
    *   **Part 2 ($d=480$):**
        $F_{2h} = 0.75(480) + 100 = 360 + 100 = 460$
        $F_{2l} = \frac{7}{12}(480) + 100 = 280 + 100 = 380$
        
    *   **Part 3 ($d=540$):**
        $F_{3h} = 0.75(540) + 100 = 405 + 100 = 505$
        $F_{3l} = \frac{7}{12}(540) + 100 = 315 + 100 = 415$
        
    *   **Part 4 ($d=600$):**
        $F_{4h} = 0.75(600) + 100 = 450 + 100 = 550$
        $F_{4l} = \frac{7}{12}(600) + 100 = 350 + 100 = 450$

3.  **Objective Function Details:**
    Minimize $Z = \prod_{i=1}^{4} S_i$
    
    $S_i = (1 - p_{ih})^{x_{ih}} (1 - p_{il})^{x_{il}}$
    
    Parameters $p$:
    -   Part 1: $p_{1h}=0.10, p_{1l}=0.08 \implies \text{Survival bases: } 0.90, 0.92$
    -   Part 2: $p_{2h}=0.20, p_{2l}=0.16 \implies \text{Survival bases: } 0.80, 0.84$
    -   Part 3: $p_{3h}=0.15, p_{3l}=0.12 \implies \text{Survival bases: } 0.85, 0.88$
    -   Part 4: $p_{4h}=0.25, p_{4l}=0.20 \implies \text{Survival bases: } 0.75, 0.80$

    Objective:
    $$ \text{Minimize } Z = \left[ (0.90)^{x_{1h}} (0.92)^{x_{1l}} \right] \cdot \left[ (0.80)^{x_{2h}} (0.84)^{x_{2l}} \right] \cdot \left[ (0.85)^{x_{3h}} (0.88)^{x_{3l}} \right] \cdot \left[ (0.75)^{x_{4h}} (0.80)^{x_{4l}} \right] $$

    This is a Non-Linear Integer Programming (NLIP) problem. It can be solved by converting to linear form using logarithms:
    Minimize $\ln(Z) = \sum x_{ih} \ln(1-p_{ih}) + \sum x_{il} \ln(1-p_{il})$
    Since $\ln(1-p) < 0$, minimizing $\ln(Z)$ is equivalent to maximizing the sum of negative logs (or minimizing the sum of logs).
    Actually, since we want to minimize the product of survival probabilities, and logs are monotonic, we can linearize the objective:
    $$ \text{Minimize } \sum_{i=1}^4 \left[ x_{ih} \ln(1-p_{ih}) + x_{il} \ln(1-p_{il}) \right] $$
    Note: The coefficients $\ln(1-p)$ are negative. Minimizing a sum of negative terms is equivalent to making them "more negative", i.e., increasing the destruction probability. This is a valid Linear Integer Programming (LIP) formulation for the solver.

    **Coefficients for Linearized Objective ($C_{ij} = \ln(1-p_{ij})$):**
    -   $C_{1h} = \ln(0.90) \approx -0.10536$
    -   $C_{1l} = \ln(0.92) \approx -0.08338$
    -   $C_{2h} = \ln(0.80) \approx -0.22314$
    -   $C_{2l} = \ln(0.84) \approx -0.17435$
    -   $C_{3h} = \ln(0.85) \approx -0.16252$
    -   $C_{3l} = \ln(0.88) \approx -0.12783$
    -   $C_{4h} = \ln(0.75) \approx -0.28768$
    -   $C_{4l} = \ln(0.80) \approx -0.22314$

### 2. Mathematical Model

**Model Type:** Mixed Integer Linear Programming (MILP)
*(Note: The original problem is non-linear, but the objective can be transformed into a linear one via logarithms, allowing the use of standard MILP solvers.)*

#### Index Sets & Parameters

**Sets:**
-   $I = \{1, 2, 3, 4\}$: Index for key parts.
-   $B = \{h, l\}$: Index for bomb types (Heavy, Light).

**Parameters:**

*Distances ($d_i$ in km):*
-   $d_1 = 450$
-   $d_2 = 480$
-   $d_3 = 540$
-   $d_4 = 600$

*Probabilities of Destruction ($p_{ib}$):*
-   Part 1: $p_{1h} = 0.10$, $p_{1l} = 0.08$
-   Part 2: $p_{2h} = 0.20$, $p_{2l} = 0.16$
-   Part 3: $p_{3h} = 0.15$, $p_{3l} = 0.12$
-   Part 4: $p_{4h} = 0.25$, $p_{4l} = 0.20$

*Fuel Consumption per Sortie ($F_{ib}$ in Liters):*
Calculated as $F_{ib} = d_i \times (\text{Outbound Rate}^{-1} + \text{Return Rate}^{-1}) + 100$.
Return rate is always 4 km/L (empty).
Outbound rate is 2 km/L for Heavy, 3 km/L for Light.

-   **Heavy ($h$):** Factor = $\frac{1}{2} + \frac{1}{4} = 0.75$
    -   $F_{1h} = 0.75(450) + 100 = 437.5$
    -   $F_{2h} = 0.75(480) + 100 = 460.0$
    -   $F_{3h} = 0.75(540) + 100 = 505.0$
    -   $F_{4h} = 0.75(600) + 100 = 550.0$

-   **Light ($l$):** Factor = $\frac{1}{3} + \frac{1}{4} = \frac{7}{12} \approx 0.58333$
    -   $F_{1l} = \frac{7}{12}(450) + 100 = 362.5$
    -   $F_{2l} = \frac{7}{12}(480) + 100 = 380.0$
    -   $F_{3l} = \frac{7}{12}(540) + 100 = 415.0$
    -   $F_{4l} = \frac{7}{12}(600) + 100 = 450.0$

*Resource Limits:*
-   Total Heavy Bombs: $H_{max} = 48$
-   Total Light Bombs: $L_{max} = 32$
-   Total Fuel: $Fuel_{max} = 48,000$

*Objective Coefficients ($C_{ib} = \ln(1 - p_{ib})$):*
-   $C_{1h} = \ln(0.90)$
-   $C_{1l} = \ln(0.92)$
-   $C_{2h} = \ln(0.80)$
-   $C_{2l} = \ln(0.84)$
-   $C_{3h} = \ln(0.85)$
-   $C_{3l} = \ln(0.88)$
-   $C_{4h} = \ln(0.75)$
-   $C_{4l} = \ln(0.80)$

#### Decision Variables

-   $x_{ih} \in \mathbb{Z}_{\ge 0}$: Number of heavy bombs assigned to part $i$.
-   $x_{il} \in \mathbb{Z}_{\ge 0}$: Number of light bombs assigned to part $i$.
    *(For all $i \in I$)*

#### Objective Function

Minimize the log of the joint survival probability (equivalent to maximizing destruction probability):

$$ \text{Minimize } Z = \sum_{i=1}^{4} \left( C_{ih} x_{ih} + C_{il} x_{il} \right) $$

*(Note: Since $C_{ib}$ are negative, this minimization drives $x$ to values that reduce the survival probability most efficiently. The final probability of success is $1 - \exp(Z^*)$.)*

#### Operational Constraints

1.  **Heavy Bomb Supply Constraint:**
    $$ \sum_{i=1}^{4} x_{ih} \le 48 $$

2.  **Light Bomb Supply Constraint:**
    $$ \sum_{i=1}^{4} x_{il} \le 32 $$

3.  **Fuel Consumption Constraint:**
    $$ \sum_{i=1}^{4} \left( F_{ih} x_{ih} + F_{il} x_{il} \right) \le 48,000 $$

    Expanded with values:
    $$ 437.5 x_{1h} + 362.5 x_{1l} + 460 x_{2h} + 380 x_{2l} + 505 x_{3h} + 415 x_{3l} + 550 x_{4h} + 450 x_{4l} \le 48,000 $$

4.  **Non-negativity and Integrality:**
    $$ x_{ih}, x_{il} \in \mathbb{Z}_{\ge 0} \quad \forall i \in \{1,2,3,4\} $$