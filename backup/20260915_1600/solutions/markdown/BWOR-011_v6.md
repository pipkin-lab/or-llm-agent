Model Type: LP

### Index Sets & Parameters

**Index Sets:**
*   $S = \{I, II\}$: Set of power stations.
*   $C = \{1, 2, 3\}$: Set of cities.

**Parameters:**
*   $Cap_s$: Maximum supply capacity of station $s$ (units).
    *   $Cap_I = 400$
    *   $Cap_{II} = 450$
    *   Total Supply $= 850$
*   $D_{min,c}$: Minimum required supply for city $c$ (units).
    *   $D_{min,1} = 290$ (320 - 30 reduction allowed)
    *   $D_{min,2} = 250$ (Fixed)
    *   $D_{min,3} = 270$
*   $D_{max,c}$: Maximum required supply for city $c$ (units).
    *   $D_{max,1} = 320$
    *   $D_{max,2} = 250$
    *   $D_{max,3} = 350$
*   $Cost_{s,c}$: Unit cost of supplying electricity from station $s$ to city $c$ (Yuan/unit).
    *   $Cost_{I,1} = 15$
    *   $Cost_{I,2} = 18$
    *   $Cost_{I,3} = 22$
    *   $Cost_{II,1} = 21$
    *   $Cost_{II,2} = 25$
    *   $Cost_{II,3} = 16$

### Decision Variables

*   $x_{s,c}$: Amount of electricity (units) supplied from station $s$ to city $c$.
    *   Domain: $x_{s,c} \in \mathbb{R}^+$ (Continuous, non-negative) for all $s \in S, c \in C$.

### Objective Function

Minimize the total cost of electricity distribution.

$$ \text{Minimize } Z = \sum_{s \in S} \sum_{c \in C} Cost_{s,c} \cdot x_{s,c} $$

Expanded:
$$ Z = 15 x_{I,1} + 18 x_{I,2} + 22 x_{I,3} + 21 x_{II,1} + 25 x_{II,2} + 16 x_{II,3} $$

### Operational Constraints

**1. Supply Capacity Constraints (Stations)**
The problem states the plan must "use up all available electricity from both stations". Thus, the total output from each station must equal its maximum capacity.

$$ \sum_{c \in C} x_{I,c} = 400 $$
$$ \sum_{c \in C} x_{II,c} = 450 $$

**2. Demand Constraints (Cities)**
The supply to each city must fall within its specific allowed range.

*   **City 1:** Supply can be reduced by up to 30 units from the 320 requirement.
    $$ \sum_{s \in S} x_{s,1} \ge 290 $$
    $$ \sum_{s \in S} x_{s,1} \le 320 $$

*   **City 2:** Supply must remain fixed at 250 units.
    $$ \sum_{s \in S} x_{s,2} = 250 $$

*   **City 3:** Supply must be at least 270 units, up to 350 units.
    $$ \sum_{s \in S} x_{s,3} \ge 270 $$
    $$ \sum_{s \in S} x_{s,3} \le 350 $$

**3. Non-negativity Constraints**
$$ x_{s,c} \ge 0 \quad \forall s \in S, c \in C $$