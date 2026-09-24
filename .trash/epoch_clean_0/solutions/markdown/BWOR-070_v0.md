## Index Sets & Parameters

**Index Sets:**
*   $i \in \{1, 2, 3, 4\}$: Set of goods types.

**Parameters:**
*   $w_i$: Weight per unit of goods type $i$ (tons).
    *   $w_1 = 2, w_2 = 3, w_3 = 4, w_4 = 5$
*   $v_i$: Volume per unit of goods type $i$ (cubic meters).
    *   $v_1 = 2, v_2 = 2, v_3 = 2, v_4 = 3$
*   $c_i$: Value per unit of goods type $i$ (thousand yuan).
    *   $c_1 = 3, c_2 = 4, c_3 = 5, c_4 = 6$
*   $W_{max}$: Maximum weight capacity of the truck (tons).
    *   $W_{max} = 15$
*   $V_{max}$: Maximum volume capacity of the truck (cubic meters).
    *   $V_{max} = 10$

## Decision Variables

*   $x_i$: The number of units of goods type $i$ loaded onto the truck.
    *   **Domain**: $x_i \in \mathbb{Z}_{\ge 0}$ for all $i \in \{1, 2, 3, 4\}$
    *   *Rationale*: Goods are discrete physical units, and the problem states there is "no limit on the number of items," implying we can load multiple identical units. Therefore, variables must be non-negative integers.

## Objective Function

Maximize the total value of the cargo:

$$ \text{Maximize } Z = \sum_{i=1}^{4} c_i x_i $$

Substituting the parameter values:

$$ \text{Maximize } Z = 3x_1 + 4x_2 + 5x_3 + 6x_4 $$

## Operational Constraints

**1. Weight Capacity Constraint**
The total weight of all goods loaded must not exceed the truck's maximum weight capacity.

$$ \sum_{i=1}^{4} w_i x_i \le W_{max} $$

Substituting the parameter values:

$$ 2x_1 + 3x_2 + 4x_3 + 5x_4 \le 15 $$

**2. Volume Capacity Constraint**
The total volume of all goods loaded must not exceed the truck's maximum volume capacity.

$$ \sum_{i=1}^{4} v_i x_i \le V_{max} $$

Substituting the parameter values:

$$ 2x_1 + 2x_2 + 2x_3 + 3x_4 \le 10 $$

**3. Non-negativity and Integrality Constraints**

$$ x_i \in \mathbb{Z}_{\ge 0}, \quad \forall i \in \{1, 2, 3, 4\} $$