# Mathematical Optimization Model for Farm Operational Planning

## Model Type: LP (Linear Programming)

All decision variables are continuous (hectares of land can be fractional, and while chickens/cows are discrete, standard textbook formulation treats them as continuous for LP purposes; note that the integer nature of animals is typically ignored in this classic problem unless explicitly stated otherwise).

## Index Sets & Parameters

**Sets:**
*   $C = \{1, 2, 3\}$: Set of crops (1: Soybeans, 2: Corn, 3: Wheat)
*   $A = \{cow, chick\}$: Set of animal types

**Parameters:**

**Global Resources:**
*   $L_{total} = 100$ hm²: Total available land
*   $F_{total} = 15,000$ yuan: Total available funds
*   $P_{aw} = 3,500$ person-days: Available labor in autumn/winter
*   $P_{ss} = 4,000$ person-days: Available labor in spring/summer

**Wage Rates (Income from unused labor):**
*   $w_{aw} = 1.8$ yuan/person-day: Wage in autumn/winter
*   $w_{ss} = 2.1$ yuan/person-day: Wage in spring/summer

**Crop Parameters (per hm²):**
*   **Labor:**
    *   Soybeans: $l_{1,aw} = 20$, $l_{1,ss} = 50$
    *   Corn: $l_{2,aw} = 35$, $l_{2,ss} = 75$
    *   Wheat: $l_{3,aw} = 10$, $l_{3,ss} = 40$
*   **Net Income:**
    *   Soybeans: $r_1 = 175$ yuan/hm²
    *   Corn: $r_2 = 300$ yuan/hm²
    *   Wheat: $r_3 = 120$ yuan/hm²
*   **Investment:** 0 yuan for all crops.

**Animal Parameters (per unit):**
*   **Investment:**
    *   Cow: $I_{cow} = 400$ yuan
    *   Chicken: $I_{chick} = 3$ yuan
*   **Land (Forage):**
    *   Cow: $L_{cow} = 1.5$ hm²
    *   Chicken: $L_{chick} = 0$ hm²
*   **Labor:**
    *   Cow: $l_{cow,aw} = 100$, $l_{cow,ss} = 50$ person-days
    *   Chicken: $l_{chick,aw} = 0.6$, $l_{chick,ss} = 0.3$ person-days
*   **Net Income:**
    *   Cow: $R_{cow} = 400$ yuan
    *   Chicken: $R_{chick} = 2$ yuan
*   **Capacity Limits:**
    *   Cowshed: $U_{cow} = 32$ cows
    *   Chicken House: $U_{chick} = 3,000$ chickens

## Decision Variables

Let:
*   $x_1$: Hectares of land allocated to Soybeans (Continuous, $\ge 0$)
*   $x_2$: Hectares of land allocated to Corn (Continuous, $\ge 0$)
*   $x_3$: Hectares of land allocated to Wheat (Continuous, $\ge 0$)
*   $y_1$: Number of dairy cows raised (Continuous, $\ge 0$)
*   $y_2$: Number of chickens raised (Continuous, $\ge 0$)
*   $z_{aw}$: Person-days of labor sent out to work in autumn/winter (Continuous, $\ge 0$)
*   $z_{ss}$: Person-days of labor sent out to work in spring/summer (Continuous, $\ge 0$)

## Objective Function

Maximize the total annual net income. This consists of:
1.  Income from crops: $175x_1 + 300x_2 + 120x_3$
2.  Income from animals: $400y_1 + 2y_2$
3.  Income from unused labor (wages): $1.8z_{aw} + 2.1z_{ss}$

$$
\text{Maximize } Z = 175x_1 + 300x_2 + 120x_3 + 400y_1 + 2y_2 + 1.8z_{aw} + 2.1z_{ss}
$$

## Operational Constraints

**1. Land Constraint:**
Total land used for crops plus land used for cow forage must not exceed total land.
$$
x_1 + x_2 + x_3 + 1.5y_1 \le 100
$$

**2. Fund Constraint:**
Total investment in animals must not exceed available funds.
$$
400y_1 + 3y_2 \le 15,000
$$

**3. Labor Constraints (Autumn/Winter):**
Labor used for crops and animals plus labor sent out must not exceed available labor.
$$
20x_1 + 35x_2 + 10x_3 + 100y_1 + 0.6y_2 + z_{aw} \le 3,500
$$

**4. Labor Constraints (Spring/Summer):**
Labor used for crops and animals plus labor sent out must not exceed available labor.
$$
50x_1 + 75x_2 + 40x_3 + 50y_1 + 0.3y_2 + z_{ss} \le 4,000
$$

**5. Capacity Constraints:**
Animal population limits.
$$
y_1 \le 32
$$
$$
y_2 \le 3,000
$$

**6. Non-negativity Constraints:**
$$
x_1, x_2, x_3, y_1, y_2, z_{aw}, z_{ss} \ge 0
$$

## Summary of Formulation

| Component | Expression |
| :--- | :--- |
| **Objective** | Max $175x_1 + 300x_2 + 120x_3 + 400y_1 + 2y_2 + 1.8z_{aw} + 2.1z_{ss}$ |
| **Land** | $x_1 + x_2 + x_3 + 1.5y_1 \le 100$ |
| **Funds** | $400y_1 + 3y_2 \le 15,000$ |
| **Labor (AW)** | $20x_1 + 35x_2 + 10x_3 + 100y_1 + 0.6y_2 + z_{aw} \le 3,500$ |
| **Labor (SS)** | $50x_1 + 75x_2 + 40x_3 + 50y_1 + 0.3y_2 + z_{ss} \le 4,000$ |
| **Cap (Cow)** | $y_1 \le 32$ |
| **Cap (Chick)** | $y_2 \le 3,000$ |
| **Bounds** | All variables $\ge 0$ |