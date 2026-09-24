# Model Type: MILP (Mixed Integer Linear Programming)

## Index Sets & Parameters

**Sets:**
- $P = \{1, 2, 3\}$: Set of products, where $1$ = manuscript paper, $2$ = diaries, $3$ = exercise books.

**Parameters (converted to base units: kg, yuan, workers, units):**

| Parameter | Description | Value | Unit |
|-----------|-------------|-------|------|
| $W_0$ | Current number of workers | 100 | workers |
| $S$ | Monthly raw material supply | 30,000 | kg |
| $\lambda_1$ | Labor productivity for product 1 | 30 | bundles/worker/month |
| $\lambda_2$ | Labor productivity for product 2 | 30 | dozens/worker/month |
| $\lambda_3$ | Labor productivity for product 3 | 30 | boxes/worker/month |
| $a_1$ | Raw material consumption per bundle of manuscript paper | $3\frac{1}{3} = \frac{10}{3}$ | kg/bundle |
| $a_2$ | Raw material consumption per dozen of diaries | $13\frac{1}{3} = \frac{40}{3}$ | kg/dozen |
| $a_3$ | Raw material consumption per box of exercise books | $26\frac{2}{3} = \frac{80}{3}$ | kg/box |
| $\pi_1$ | Profit per bundle of manuscript paper | 2 | yuan/bundle |
| $\pi_2$ | Profit per dozen of diaries | 3 | yuan/dozen |
| $\pi_3$ | Profit per box of exercise books | 1 | yuan/box |
| $c_T$ | Wage cost per temporary worker | 40 | yuan/worker/month |

## Decision Variables

- $x_1 \in \mathbb{Z}_{\geq 0}$: Number of bundles of manuscript paper produced per month.
- $x_2 \in \mathbb{Z}_{\geq 0}$: Number of dozens of diaries produced per month.
- $x_3 \in \mathbb{Z}_{\geq 0}$: Number of boxes of exercise books produced per month.
- $T \in \mathbb{Z}_{\geq 0}$: Number of temporary workers to be hired per month.

## Objective Function

Maximize the net profit (total product profit minus temporary worker costs):

$$
\max Z = 2x_1 + 3x_2 + 1x_3 - 40T
$$

## Operational Constraints

**1. Raw Material Constraint:**
The total raw material consumed cannot exceed the monthly supply.
$$
\frac{10}{3}x_1 + \frac{40}{3}x_2 + \frac{80}{3}x_3 \leq 30000
$$
*(Simplified: $10x_1 + 40x_2 + 80x_3 \leq 90000$)*

**2. Labor Capacity Constraint:**
The total labor required for production cannot exceed the total available workers (permanent + temporary).
$$
\frac{x_1}{30} + \frac{x_2}{30} + \frac{x_3}{30} \leq 100 + T
$$
*(Simplified: $x_1 + x_2 + x_3 \leq 3000 + 30T$)*

## Feasibility & Sanity Check

1.  **Without temporary workers ($T=0$):**
    *   Labor constraint: $x_1 + x_2 + x_3 \leq 3000$.
    *   Material constraint: $\frac{10}{3}x_1 + \frac{40}{3}x_2 + \frac{80}{3}x_3 \leq 30000 \implies 10x_1 + 40x_2 + 80x_3 \leq 90000$.
    *   Let's check if labor is the binding constraint relative to material.
        *   Max units if only Labor binds: $3000$ units.
        *   Max units if only Material binds (worst case material usage is $10/3$ kg/unit for product 1): $30000 / (10/3) = 9000$ units.
        *   Since $3000 < 9000$, labor is the stricter constraint for the least material-intensive product.
        *   However, we must check profit per unit of resource.
            *   Product 1: Profit/Labor = $2/(1/30) = 60$ yuan/worker-unit. Profit/Material = $2/(10/3) = 0.6$ yuan/kg.
            *   Product 2: Profit/Labor = $3/(1/30) = 90$ yuan/worker-unit. Profit/Material = $3/(40/3) = 0.225$ yuan/kg.
            *   Product 3: Profit/Labor = $1/(1/30) = 30$ yuan/worker-unit. Profit/Material = $1/(80/3) = 0.0375$ yuan/kg.
    *   Product 2 has the highest profit per unit of labor. Product 1 has the highest profit per unit of material.
    *   Since labor is the scarce resource (3000 units max vs 9000 units max material capacity), we prioritize products with high profit per labor unit. Product 2 is best.
    *   If we produce only Product 2 with $T=0$: $x_2 = 3000$. Material used = $3000 \times \frac{40}{3} = 40,000$ kg.
    *   **Wait**, $40,000 > 30,000$. So material becomes the binding constraint if we produce too many diaries.
    *   Let's re-evaluate. We have two resources.
        *   Resource 1 (Labor): $\sum x_i / 30 \leq 100 + T$.
        *   Resource 2 (Material): $\sum a_i x_i \leq 30000$.
    *   If we set $T=0$, max labor units = 3000.
    *   Max material units (if all Prod 1) = 9000.
    *   Max material units (if all Prod 2) = $30000 / (40/3) = 2250$.
    *   Max material units (if all Prod 3) = $30000 / (80/3) = 1125$.
    *   So, if we try to maximize profit using Product 2 (highest labor profit), we are limited by material to 2250 dozens.
    *   Labor used for 2250 dozens = $2250/30 = 75$ workers. We have 100 workers. So we have 25 workers (750 unit-capacity) left.
    *   Can we use the remaining labor on Product 1?
        *   Remaining labor capacity: $3000 - 2250 = 750$ units.
        *   Remaining material capacity: $30000 - 2250 \times \frac{40}{3} = 30000 - 30000 = 0$.
        *   So no material left.
    *   Is it better to mix?
        *   Product 1 yields 2 yuan/unit labor. Product 2 yields 3 yuan/unit labor.
        *   However, Product 2 consumes 4x more material per unit labor than Product 1 ($40/3$ vs $10/3$).
        *   Since material is the bottleneck when producing high-profit Product 2, we might need to substitute with Product 1 to utilize remaining labor if material allows, or vice versa.
        *   Actually, let's look at the "shadow price" intuition.
        *   With $T=0$, we are limited by Material if we focus on Product 2.
        *   Let's check the corner points of the feasible region for $T=0$.
            *   Intersection of $x_1+x_2+x_3=3000$ and $\frac{10}{3}x_1 + \frac{40}{3}x_2 + \frac{80}{3}x_3 = 30000$.
            *   $x_1+x_2+x_3=3000$
            *   $10x_1+40x_2+80x_3=90000$
            *   Subtract 10*Eq1 from Eq2: $30x_2 + 70x_3 = 60000 \implies 3x_2 + 7x_3 = 6000$.
            *   Case A: $x_3=0 \implies 3x_2=6000 \implies x_2=2000$. Then $x_1 = 3000-2000=1000$.
                *   Profit: $2(1000) + 3(2000) + 0 = 2000 + 6000 = 8000$.
            *   Case B: $x_2=0 \implies 7x_3=6000 \implies x_3 \approx 857$. Then $x_1 = 3000-857=2143$.
                *   Profit: $2(2143) + 0 + 1(857) = 4286 + 857 = 5143$.
            *   Case C: Only Material binds (Labor slack).
                *   Max $x_2$ s.t. Material: $x_2 = 2250$. Labor used = 75. Profit = $2250 \times 3 = 6750$. (Less than 8000).
                *   Max $x_1$ s.t. Material: $x_1 = 9000$. Labor used = 300. But max labor is 300. So $x_1=3000$ is the max for Product 1 if only labor bounds it, but material allows 9000. So if we only make Product 1, we are labor constrained at 3000. Profit = $3000 \times 2 = 6000$.
            *   So for $T=0$, optimal mix is likely $x_1=1000, x_2=2000, x_3=0$ with Profit 8000.

2.  **With temporary workers ($T>0$):**
    *   Hiring a worker costs 40 yuan.
    *   A worker can produce 30 units.
    *   If we hire a worker, we can potentially produce more.
    *   The marginal profit of a new worker depends on what they produce and if material allows.
    *   At the $T=0$ optimum ($x_1=1000, x_2=2000$), both Labor and Material are binding (Labor: $1000+2000=3000$; Material: $10(1000)+40(2000)=90000$).
    *   To increase production, we need both more Labor AND more Material.
    *   But Material is fixed at 30,000 kg!
    *   **Crucial Insight:** The problem states "If the supply of white base paper remains unchanged".
    *   If Material is the ultimate bottleneck and we are already using all 30,000 kg in the $T=0$ optimum, hiring more workers **cannot** increase production because there is no more raw material to process.
    *   Let's verify if material is fully used in the $T=0$ optimum.
        *   $x_1=1000, x_2=2000$.
        *   Material = $\frac{10}{3}(1000) + \frac{40}{3}(2000) = \frac{10000+80000}{3} = 30,000$ kg.
        *   Yes, material is fully utilized.
    *   Therefore, any increase in labor capacity ($T$) is useless because there is no raw material to support the additional output.
    *   Consequently, hiring temporary workers will only add cost (40 yuan each) without increasing revenue.
    *   Thus, $T$ should be 0.

**Answer:** The factory should **not** hire temporary workers. The optimal number is 0.