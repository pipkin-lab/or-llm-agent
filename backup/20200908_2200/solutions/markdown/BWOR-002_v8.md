# Diet Problem: Livestock Feed Optimization

## 1. Index Sets & Parameters

**Sets:**
- $F = \{1, 2, 3, 4, 5\}$: Set of feed types.
- $N = \{P, M, V\}$: Set of nutritional nutrients (Protein, Minerals, Vitamins).

**Parameters:**
Let $a_{n,f}$ be the amount of nutrient $n$ (in grams or milligrams) provided by 1 kg of feed $f$.
Let $c_f$ be the cost of 1 kg of feed $f$ (in dollars).
Let $R_n$ be the minimum daily requirement for nutrient $n$.

**Data from Table 1-22:**

| Feed ($f$) | Protein ($g$) $a_{P,f}$ | Minerals ($g$) $a_{M,f}$ | Vitamins ($mg$) $a_{V,f}$ | Cost ($/kg$) $c_f$ |
| :--- | :---: | :---: | :---: | :---: |
| 1 | 3 | 1.0 | 0.5 | 0.2 |
| 2 | 2 | 0.5 | 1.0 | 0.7 |
| 3 | 1 | 0.2 | 0.2 | 0.4 |
| 4 | 6 | 2.0 | 2.0 | 0.3 |
| 5 | 18 | 0.5 | 0.8 | 0.8 |

**Nutritional Requirements ($R_n$):**
- $R_P = 700$ g
- $R_M = 30$ g
- $R_V = 100$ mg

## 2. Decision Variables

Let $x_f$ be the amount of feed $f$ (in kg) to be used per day.

**Domain:**
$$ x_f \ge 0, \quad \forall f \in F $$
*(Note: Feed quantities are continuous variables; fractional kilograms are physically possible and standard for diet problems.)*

## 3. Objective Function

Minimize the total daily cost of the feed mix:

$$ \text{Minimize } Z = \sum_{f \in F} c_f x_f $$

Substituting the specific costs:
$$ Z = 0.2 x_1 + 0.7 x_2 + 0.4 x_3 + 0.3 x_4 + 0.8 x_5 $$

## 4. Operational Constraints

**Nutritional Constraints:**
The total intake of each nutrient must meet or exceed the minimum daily requirement.

1.  **Protein Constraint** (min 700 g):
    $$ 3 x_1 + 2 x_2 + 1 x_3 + 6 x_4 + 18 x_5 \ge 700 $$

2.  **Minerals Constraint** (min 30 g):
    $$ 1.0 x_1 + 0.5 x_2 + 0.2 x_3 + 2.0 x_4 + 0.5 x_5 \ge 30 $$

3.  **Vitamins Constraint** (min 100 mg):
    $$ 0.5 x_1 + 1.0 x_2 + 0.2 x_3 + 2.0 x_4 + 0.8 x_5 \ge 100 $$

**Non-negativity Constraints:**
$$ x_f \ge 0, \quad \forall f \in \{1, 2, 3, 4, 5\} $$