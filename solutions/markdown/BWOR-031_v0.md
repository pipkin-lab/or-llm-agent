# Operations Research Model: Farm Operational Planning

## Model Type
**LP** (Linear Program)

## Index Sets & Parameters

**Crops:**
- $i \in \{S, C, W\}$ (Soybeans, Corn, Wheat)

**Parameters (from problem statement):**

| Parameter | Symbol | Value | Unit |
|---|---|---|---|
| Total land | $L_{\text{total}}$ | 100 | hm² |
| Total funds | $F_{\text{total}}$ | 15,000 | yuan |
| Autumn/Winter labor available | $A_{\text{avail}}$ | 3,500 | person-days |
| Spring/Summer labor available | $S_{\text{avail}}$ | 4,000 | person-days |
| Wage income (Spring/Summer) | $w_S$ | 2.1 | yuan/person-day |
| Wage income (Autumn/Winter) | $w_A$ | 1.8 | yuan/person-day |
| Investment per cow | $I_{\text{cow}}$ | 400 | yuan/cow |
| Investment per chicken | $I_{\text{chick}}$ | 3 | yuan/chicken |
| Land per cow (forage) | $l_{\text{cow}}$ | 1.5 | hm²/cow |
| A/W labor per cow | $a_{\text{cow}}$ | 100 | person-days/cow |
| S/S labor per cow | $s_{\text{cow}}$ | 50 | person-days/cow |
| Net income per cow | $r_{\text{cow}}$ | 400 | yuan/cow |
| A/W labor per chicken | $a_{\text{chick}}$ | 0.6 | person-days/chicken |
| S/S labor per chicken | $s_{\text{chick}}$ | 0.3 | person-days/chicken |
| Net income per chicken | $r_{\text{chick}}$ | 2 | yuan/chicken |
| Max chickens | $M_{\text{chick}}$ | 3,000 | chickens |
| Max cows | $M_{\text{cow}}$ | 32 | cows |
| A/W labor per hm² (Soybeans) | $a_S$ | 20 | person-days/hm² |
| S/S labor per hm² (Soybeans) | $s_S$ | 50 | person-days/hm² |
| Net income per hm² (Soybeans) | $r_S$ | 175 | yuan/hm² |
| A/W labor per hm² (Corn) | $a_C$ | 35 | person-days/hm² |
| S/S labor per hm² (Corn) | $s_C$ | 75 | person-days/hm² |
| Net income per hm² (Corn) | $r_C$ | 300 | yuan/hm² |
| A/W labor per hm² (Wheat) | $a_W$ | 10 | person-days/hm² |
| S/S labor per hm² (Wheat) | $s_W$ | 40 | person-days/hm² |
| Net income per hm² (Wheat) | $r_W$ | 120 | yuan/hm² |

## Decision Variables

| Variable | Description | Domain |
|---|---|---|
| $x_S$ | Hectares planted with soybeans | $x_S \geq 0$ (continuous) |
| $x_C$ | Hectares planted with corn | $x_C \geq 0$ (continuous) |
| $x_W$ | Hectares planted with wheat | $x_W \geq 0$ (continuous) |
| $x_{\text{cow}}$ | Number of dairy cows | $x_{\text{cow}} \geq 0$ (continuous)* |
| $x_{\text{chick}}$ | Number of chickens | $x_{\text{chick}} \geq 0$ (continuous)* |
| $u_A$ | Unused autumn/winter labor (person-days) | $u_A \geq 0$ (continuous) |
| $u_S$ | Unused spring/summer labor (person-days) | $u_S \geq 0$ (continuous) |

*\*Note: While cows and chickens are discrete physical units, standard LP formulations for farm planning treat them as continuous variables. The optimal solution will typically be near-integer given the structure of this problem. If strict integrality is required, declare $x_{\text{cow}}, x_{\text{chick}} \in \mathbb{Z}_{\geq 0}$ to make this a MILP.*

## Objective Function

**MAXIMIZE** total annual net income:

$$\max \quad Z = 175 x_S + 300 x_C + 120 x_W + 400 x_{\text{cow}} + 2 x_{\text{chick}} + 1.8 u_A + 2.1 u_S$$

**Objective Parameter Cross-Reference:**
- $175 = r_S$ ✓ (Table 1-9)
- $300 = r_C$ ✓ (Table 1-9)
- $120 = r_W$ ✓ (Table 1-9)
- $400 = r_{\text{cow}}$ ✓ (text)
- $2 = r_{\text{chick}}$ ✓ (text)
- $1.8 = w_A$ ✓ (text)
- $2.1 = w_S$ ✓ (text)

## Operational Constraints

### 1. Land Constraint
Total land used (crops + cow forage) cannot exceed 100 hm²:
$$x_S + x_C + x_W + 1.5 x_{\text{cow}} \leq 100$$

### 2. Funds Constraint
Total investment (cows + chickens) cannot exceed 15,000 yuan (crops require no investment):
$$400 x_{\text{cow}} + 3 x_{\text{chick}} \leq 15{,}000$$

### 3. Autumn/Winter Labor Constraint
Labor used by crops + animals + unused labor must equal total available A/W labor:
$$20 x_S + 35 x_C + 10 x_W + 100 x_{\text{cow}} + 0.6 x_{\text{chick}} + u_A = 3{,}500$$

### 4. Spring/Summer Labor Constraint
Labor used by crops + animals + unused labor must equal total available S/S labor:
$$50 x_S + 75 x_C + 40 x_W + 50 x_{\text{cow}} + 0.3 x_{\text{chick}} + u_S = 4{,}000$$

### 5. Capacity Constraints
$$x_{\text{chick}} \leq 3{,}000$$
$$x_{\text{cow}} \leq 32$$

### 6. Non-negativity
$$x_S, x_C, x_W, x_{\text{cow}}, x_{\text{chick}}, u_A, u_S \geq 0$$

## Feasibility Sanity Check

- **Land:** 32 cows use $32 \times 1.5 = 48$ hm², leaving 52 hm² for crops. Feasible.
- **Funds:** 32 cows cost $32 \times 400 = 12{,}800$ yuan, leaving $2{,}200$ for chickens ($\approx 733$ chickens). Feasible.
- **A/W Labor:** 32 cows use $32 \times 100 = 3{,}200$ person-days, leaving 300 for crops/chickens. Feasible (tight).
- **S/S Labor:** 32 cows use $32 \times 50 = 1{,}600$ person-days, leaving 2,400 for crops/chickens. Feasible.
- The model is feasible. The labor constraints are equalities with slack variables $u_A, u_S$ that earn wage income, so unused labor is monetized.