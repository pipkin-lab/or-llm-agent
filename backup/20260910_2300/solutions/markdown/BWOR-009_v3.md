Here is the formal mathematical optimization model for the production and storage scheduling problem.

### 1. Index Sets & Parameters

**Index Sets:**
*   $t \in \{1, 2, 3, 4\}$: Set of quarters.

**Parameters:**
*   $C_t$: Production capacity in quarter $t$ (units).
    *   $C_1 = 25$
    *   $C_2 = 35$
    *   $C_3 = 30$
    *   $C_4 = 20$
*   $D_t$: Required delivery quantity at the end of quarter $t$ (units).
    *   $D_1 = 15$
    *   $D_2 = 20$
    *   $D_3 = 25$
    *   $D_4 = 20$
*   $p_t$: Production cost per unit in quarter $t$ (thousand yuan/unit).
    *   $p_1 = 12.0$
    *   $p_2 = 11.0$
    *   $p_3 = 11.5$
    *   $p_4 = 12.5$
*   $h$: Holding (storage and maintenance) cost per unit per quarter (thousand yuan/unit/quarter).
    *   $h = 0.1$

### 2. Decision Variables

*   $x_t$: Number of units produced in quarter $t$.
    *   Domain: $x_t \in \mathbb{Z}_{\ge 0}$ for all $t \in \{1, 2, 3, 4\}$.
    *   *Note: Since equipment units are discrete physical items, integer variables are used.*
*   $I_t$: Number of units in inventory at the **end** of quarter $t$.
    *   Domain: $I_t \in \mathbb{Z}_{\ge 0}$ for all $t \in \{1, 2, 3, 4\}$.
    *   *Note: Inventory is assumed to be zero at the beginning of the year ($I_0 = 0$) and must be zero at the end of the year ($I_4 = 0$) to ensure all contracted deliveries are met without excess leftover stock.*

### 3. Objective Function

Minimize the total annual cost, which includes production costs and holding costs.

$$
\text{Minimize } Z = \sum_{t=1}^{4} (p_t x_t + h I_t)
$$

Substituting the specific parameter values:

$$
Z = 12.0 x_1 + 11.0 x_2 + 11.5 x_3 + 12.5 x_4 + 0.1(I_1 + I_2 + I_3 + I_4)
$$

### 4. Operational Constraints

**1. Inventory Balance Constraints:**
The inventory at the end of each quarter is equal to the previous inventory plus current production minus current delivery.
*   Timing Convention: Production occurs during quarter $t$, delivery is due at the end of quarter $t$. Holding cost is incurred on the inventory remaining at the end of quarter $t$ (which carries over to quarter $t+1$).

$$
I_t = I_{t-1} + x_t - D_t, \quad \forall t \in \{1, 2, 3, 4\}
$$
With $I_0 = 0$.

Explicitly:
*   $t=1: I_1 = 0 + x_1 - 15$
*   $t=2: I_2 = I_1 + x_2 - 20$
*   $t=3: I_3 = I_2 + x_3 - 25$
*   $t=4: I_4 = I_3 + x_4 - 20$

**2. Capacity Constraints:**
Production in any quarter cannot exceed the production capacity.

$$
x_t \le C_t, \quad \forall t \in \{1, 2, 3, 4\}
$$

Explicitly:
*   $x_1 \le 25$
*   $x_2 \le 35$
*   $x_3 \le 30$
*   $x_4 \le 20$

**3. Final Inventory Constraint:**
Assuming no requirement to hold stock beyond the contract period and that all deliveries must be met exactly by the end of their respective quarters (with no backlogging allowed as per standard interpretation of "delivery contract... at the end of each quarter"), the final inventory must be zero. If backlogging were allowed, the constraint would be different, but "storage fee" implies holding forward, and "meeting delivery contract" implies $I_t \ge 0$ is sufficient if we assume production can be delayed. However, typically in these problems, you produce to meet demand. Let's look at the phrasing: "If equipment produced in one quarter is not delivered during that quarter, a storage... fee is incurred." This implies you *can* produce early. It does not explicitly forbid backlogging, but standard production planning usually assumes demand must be met on time. Let's assume standard on-time delivery (no backorders).

Therefore:
$$
I_t \ge 0, \quad \forall t \in \{1, 2, 3, 4\}
$$
$$
I_4 = 0
$$
*(Note: The condition $I_4=0$ ensures that total production equals total demand. If the company could produce more than needed and keep it, $I_4$ would be $>0$, but since there is no salvage value and holding costs are positive, the optimizer will naturally drive $I_4$ to 0 if possible. However, explicitly stating $I_4=0$ or $I_4 \le 0$ combined with $I_4 \ge 0$ is safer. Given the problem asks for a schedule to meet the contract, excess production is wasteful. We enforce $I_4=0$.)*

**4. Non-negativity and Integrality:**
$$
x_t \ge 0, \quad x_t \in \mathbb{Z}
$$
$$
I_t \ge 0, \quad I_t \in \mathbb{Z}
$$