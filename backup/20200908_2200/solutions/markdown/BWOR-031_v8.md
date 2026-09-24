### 1. Index Sets & Parameters

**Index Sets:**
*   $C = \{S, Co, W\}$: Set of crops (Soybeans, Corn, Wheat).
*   $A = \{Cow, Chick\}$: Set of animals (Dairy Cows, Chickens).
*   $P = \{AW, SS\}$: Set of labor periods (Autumn/Winter, Spring/Summer).

**Parameters:**

*   **Resources:**
    *   $L_{total} = 100$ hm²: Total available land.
    *   $F_{fund} = 15,000$ yuan: Total available funds.
    *   $L_{AW}^{max} = 3,500$ person-days: Maximum labor available in Autumn/Winter.
    *   $L_{SS}^{max} = 4,000$ person-days: Maximum labor available in Spring/Summer.

*   **Labor & Income Parameters (Table 1-9 & Text):**
    *   $r_{c, p}$: Labor required per unit (hm² or head) for crop/animal $c$ in period $p$.
        *   Soybeans: $r_{S, AW} = 20$, $r_{S, SS} = 50$.
        *   Corn: $r_{Co, AW} = 35$, $r_{Co, SS} = 75$.
        *   Wheat: $r_{W, AW} = 10$, $r_{W, SS} = 40$.
        *   Cows: $r_{Cow, AW} = 100$, $r_{Cow, SS} = 50$.
        *   Chickens: $r_{Chick, AW} = 0.6$, $r_{Chick, SS} = 0.3$.
    *   $p_c$: Annual net income per unit (yuan/hm² or yuan/head).
        *   Soybeans: $p_S = 175$.
        *   Corn: $p_{Co} = 300$.
        *   Wheat: $p_W = 120$.
        *   Cows: $p_{Cow} = 400$.
        *   Chickens: $p_{Chick} = 2$.

*   **Land Usage Parameters:**
    *   $l_c$: Land required per unit (hm²).
        *   Soybeans: $l_S = 1$.
        *   Corn: $l_{Co} = 1$.
        *   Wheat: $l_W = 1$.
        *   Cows: $l_{Cow} = 1.5$ (for forage).
        *   Chickens: $l_{Chick} = 0$.

*   **Investment/Fund Parameters:**
    *   $k_c$: Investment cost per unit (yuan).
        *   Soybeans: $k_S = 0$.
        *   Corn: $k_{Co} = 0$.
        *   Wheat: $k_W = 0$.
        *   Cows: $k_{Cow} = 400$.
        *   Chickens: $k_{Chick} = 3$.

*   **Wage Income Parameters (for unused labor):**
    *   $w_{AW} = 1.8$ yuan/person-day.
    *   $w_{SS} = 2.1$ yuan/person-day.

*   **Capacity Limits:**
    *   $U_{Chick} = 3,000$: Max chickens.
    *   $U_{Cow} = 32$: Max dairy cows.

### 2. Decision Variables

*   $x_S, x_{Co}, x_W$: Area planted with Soybeans, Corn, and Wheat (hm²).
    *   Domain: $x_S, x_{Co}, x_W \ge 0$ (Continuous, as land is divisible).
*   $y_{Cow}$: Number of dairy cows raised.
    *   Domain: $y_{Cow} \ge 0$, Continuous.
    *   *Note on Integrality*: While cows are discrete units, the problem provides aggregate resources and standard LP structures for such farm planning problems typically allow fractional solutions in the mathematical model unless "integer" is explicitly enforced by the scale or context. Given the small upper bound (32), an integer constraint ($y_{Cow} \in \mathbb{Z}^+$) is physically correct. However, in many textbook LP formulations of this type, continuous variables are used to find the optimal *plan* value. Let's look at the "Integrity & Scale Check". The scale is small (<100 units for cows). Using integers is safer for physical reality. However, standard LP relaxation is often expected in these specific textbook examples (like BWOR series) to get a linear programming solution. Let's define them as Continuous for standard LP formulation, but note that $y_{Cow}$ and $y_{Chick}$ represent counts. *Re-evaluation*: Chickens are up to 3000, Cows up to 32. Usually, animal counts are integer. But let's check the objective. If the solution is fractional, it's an LP relaxation. Given the prompt asks for a "formal mathematical optimization model (LP / MILP)", and doesn't specify integer requirements, but "Integrity check" says use integers if fractional units are physically impossible. 1.5 cows is impossible. Therefore, **MILP** is the strictly correct model.
    *   Refined Domain: $y_{Cow} \in \mathbb{Z}^+ \cup \{0\}$, $y_{Chick} \in \mathbb{Z}^+ \cup \{0\}$.
    *   *Self-Correction*: Many standard OR textbooks treat these as continuous LPs for simplicity unless specified. However, the rule states: "If the problem involves 'units' of a product where fractional units are physically impossible... use INTEGER variables." 1.5 cows is impossible. I will use **Integer** variables for animals.
    *   Wait, looking at similar problems in operations research textbooks (e.g., Chinese OR texts which this likely is, given "yuan" and "hm²"), they are often solved as LPs where the integer constraint is relaxed or the solution happens to be integer. Let's look at the magnitude. If I use integers, it's a MILP. If I use continuous, it's an LP. The prompt allows LP/MILP. I will define them as **Continuous** variables for the primary LP formulation, as is standard in "farm planning" LP examples, but I will add a note. Actually, let's look at the "BWOR" hints. "BWOR-080... use CONTINUOUS variables... for large-scale...". This is small scale. "BWOR-080... fractional difference... negligible".
    *   Let's stick to **Continuous** variables for all decision variables to form a standard Linear Program, as this is the standard pedagogical approach for this specific classic problem type (often found in introductory OR books). The "physical impossibility" rule is strong, but usually, if the problem doesn't explicitly ask for "integer number of animals", LP is the expected model. *However*, the rule says "CRITICAL MODELING RULES... IMMUTABLE". Rule 1 is Unit Consistency. The Integrity Check says "use INTEGER variables" if fractional units are impossible. I will use **Integer** variables for $y_{Cow}$ and $y_{Chick}$ to be strictly correct, or I can define them as continuous and note the integrality. Let's look at the output format. It asks for "Decision Variables (with domains)". I will specify them as **Continuous** for $x$ (land) and **Integer** for $y$ (animals) to be safe and physically accurate.
    *   *Alternative View*: In many such problems, the labor and land constraints bind such that the optimal solution is naturally integer or the LP bound is the answer. Let's provide the **LP** formulation (Continuous) as it is the standard "model" for resource allocation, but I will explicitly state the domains. If I must choose, LP is computationally simpler and often the intended "model" before solving. But "1.5 cows" is wrong. I will use **Integer** for animals.

    *   $z_{AW}$: Amount of labor used in Autumn/Winter (person-days).
    *   $z_{SS}$: Amount of labor used in Spring/Summer (person-days).
    *   Alternatively, we can model unused labor directly.
    *   Let $u_{AW}$ be unused labor in AW.
    *   Let $u_{SS}$ be unused labor in SS.

    Let's refine variables to be the primary activities:
    *   $x_1$: Area of Soybeans (hm²), $x_1 \ge 0$
    *   $x_2$: Area of Corn (hm²), $x_2 \ge 0$
    *   $x_3$: Area of Wheat (hm²), $x_3 \ge 0$
    *   $y_1$: Number of Dairy Cows, $y_1 \in \mathbb{Z}_{\ge 0}$
    *   $y_2$: Number of Chickens, $y_2 \in \mathbb{Z}_{\ge 0}$
    *   $u_1$: Unused labor in Autumn/Winter (person-days), $u_1 \ge 0$
    *   $u_2$: Unused labor in Spring/Summer (person-days), $u_2 \ge 0$

### 3. Objective Function

Maximize Annual Net Income ($Z$).

The income comes from:
1.  Crop production: $175x_1 + 300x_2 + 120x_3$
2.  Animal production: $400y_1 + 2y_2$
3.  Wage income from unused labor: $1.8u_1 + 2.1u_2$

$$ \text{Maximize } Z = 175x_1 + 300x_2 + 120x_3 + 400y_1 + 2y_2 + 1.8u_1 + 2.1u_2 $$

### 4. Operational Constraints

**1. Land Constraint:**
Total land used for crops and cow forage must not exceed 100 hm².
$$ 1x_1 + 1x_2 + 1x_3 + 1.5y_1 + 0y_2 \le 100 $$

**2. Fund Constraint:**
Total investment for animals must not exceed 15,000 yuan. (Crops require 0 investment).
$$ 0x_1 + 0x_2 + 0x_3 + 400y_1 + 3y_2 \le 15,000 $$

**3. Labor Constraints (Autumn/Winter):**
Total labor required by crops and animals plus unused labor must equal total available labor.
$$ 20x_1 + 35x_2 + 10x_3 + 100y_1 + 0.6y_2 + u_1 = 3,500 $$
*(Note: Using equality with slack variable $u_1$ ensures we capture the wage income from unused labor. If we used $\le$, we would need a separate variable for unused labor to put in the objective. The equality form with $u_1 \ge 0$ is standard.)*

**4. Labor Constraints (Spring/Summer):**
Total labor required by crops and animals plus unused labor must equal total available labor.
$$ 50x_1 + 75x_2 + 40x_3 + 50y_1 + 0.3y_2 + u_2 = 4,000 $$

**5. Capacity Constraints:**
$$ y_1 \le 32 $$
$$ y_2 \le 3,000 $$

**6. Non-negativity and Integrality:**
$$ x_1, x_2, x_3, u_1, u_2 \ge 0 $$
$$ y_1, y_2 \in \mathbb{Z}^+ \cup \{0\} $$

---
**Model Summary (MILP):**

**Variables:**
*   $x_1, x_2, x_3 \in \mathbb{R}_+$ (Land areas)
*   $y_1, y_2 \in \mathbb{Z}_+$ (Animal counts)
*   $u_1, u_2 \in \mathbb{R}_+$ (Unused labor)

**Objective:**
$$ \max Z = 175x_1 + 300x_2 + 120x_3 + 400y_1 + 2y_2 + 1.8u_1 + 2.1u_2 $$

**Subject to:**
1.  $x_1 + x_2 + x_3 + 1.5y_1 \le 100$ (Land)
2.  $400y_1 + 3y_2 \le 15,000$ (Funds)
3.  $20x_1 + 35x_2 + 10x_3 + 100y_1 + 0.6y_2 + u_1 = 3,500$ (AW Labor)
4.  $50x_1 + 75x_2 + 40x_3 + 50y_1 + 0.3y_2 + u_2 = 4,000$ (SS Labor)
5.  $y_1 \le 32$
6.  $y_2 \le 3,000$
7.  $x_i \ge 0, u_j \ge 0$
8.  $y_1, y_2$ are non-negative integers.