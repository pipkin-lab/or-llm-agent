# Livestock Feed Formulation Optimization Model

## 1. Index Sets & Parameters

**Index Sets:**
- $F = \{1, 2, 3, 4, 5\}$: Set of feed types.
- $N = \{1, 2, 3\}$: Set of nutritional requirements (1: Protein, 2: Minerals, 3: Vitamins).

**Parameters:**
- $R_n$: Minimum daily nutritional requirement for nutrient $n$ (per animal).
  - $R_1 = 700$ (g protein)
  - $R_2 = 30$ (g minerals)
  - $R_3 = 100$ (mg vitamins)
- $c_f$: Unit cost of feed $f$ (dollars per kg).
  - $c_1 = 0.2, c_2 = 0.7, c_3 = 0.4, c_4 = 0.3, c_5 = 0.8$
- $a_{f,n}$: Amount of nutrient $n$ provided by 1 kg of feed $f$.
  - *Protein (g/kg):* $a_{1,1}=3, a_{2,1}=2, a_{3,1}=1, a_{4,1}=6, a_{5,1}=18$
  - *Minerals (g/kg):* $a_{1,2}=1.0, a_{2,2}=0.5, a_{3,2}=0.2, a_{4,2}=2.0, a_{5,2}=0.5$
  - *Vitamins (mg/kg):* $a_{1,3}=0.5, a_{2,3}=1.0, a_{3,3}=0.2, a_{4,3}=2.0, a_{5,3}=0.8$

## 2. Decision Variables

- $x_f$: Amount of feed $f$ (in kg) to be used per animal per day.
  - Domain: $x_f \in \mathbb{R}^+$ (Continuous, non-negative).
  - *Note:* Feed quantities are continuous resources (measured in kg), so integer constraints are not required.

## 3. Objective Function

Minimize the total daily feed cost per animal:

$$
\min Z = \sum_{f \in F} c_f x_f
$$

Expanded:
$$
\min Z = 0.2x_1 + 0.7x_2 + 0.4x_3 + 0.3x_4 + 0.8x_5
$$

## 4. Operational Constraints

**Nutritional Constraints:**
The total amount of each nutrient provided by the selected feeds must meet or exceed the minimum daily requirement.

1.  **Protein Constraint (g):**
    $$3x_1 + 2x_2 + 1x_3 + 6x_4 + 18x_5 \ge 700$$

2.  **Minerals Constraint (g):**
    $$1.0x_1 + 0.5x_2 + 0.2x_3 + 2.0x_4 + 0.5x_5 \ge 30$$

3.  **Vitamins Constraint (mg):**
    $$0.5x_1 + 1.0x_2 + 0.2x_3 + 2.0x_4 + 0.8x_5 \ge 100$$

**Non-negativity Constraints:**
$$x_f \ge 0, \quad \forall f \in F$$

## 5. Model Verification & Notes

- **Units Consistency:**
  - Protein is in grams (g) on both LHS (g/kg * kg) and RHS (g).
  - Minerals are in grams (g) on both LHS and RHS.
  - Vitamins are in milligrams (mg) on both LHS and RHS.
  - Cost is in dollars. All units are consistent.
- **Variable Type:** Continuous variables are appropriate because feed is measured in kilograms, a continuous quantity. There is no physical constraint forcing integer kilograms.
- **Objective Direction:** Minimization of cost is correctly specified.
- **Bounds:** Non-negativity is enforced. No upper bounds are specified in the problem, which is standard for diet problems where excess nutrients are allowed but not penalized beyond the cost of the feed itself.