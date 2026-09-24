# Timber Storage and Transportation Optimization Model

## Model Type: **LP** (Linear Programming)

## Index Sets & Parameters

**Index Sets:**
- $t \in \{1, 2, 3, 4\}$: Quarters, where $1=$ Winter, $2=$ Spring, $3=$ Summer, $4=$ Autumn.

**Parameters (all values extracted from Table 1-18):**

| Parameter | Description | $t=1$ (Winter) | $t=2$ (Spring) | $t=3$ (Summer) | $t=4$ (Autumn) |
|-----------|-------------|:---:|:---:|:---:|:---:|
| $p_t$ | Purchase price (thousand yuan / thousand m³) | 410 | 430 | 460 | 450 |
| $s_t$ | Selling price (thousand yuan / thousand m³) | 425 | 440 | 465 | 455 |
| $D_t$ | Max sales volume (thousand m³) | 100 | 140 | 200 | 160 |

**Other Parameters:**
- $C_{cap} = 20$ (thousand m³): Maximum warehouse storage capacity.
- $a = 70$ (yuan/m³): Base storage cost per m³ per quarter.
- $b = 100$ (yuan/m³/quarter): Incremental storage cost per m³ per additional quarter of storage.
- Storage cost for timber stored for $u$ quarters: $(a + b \cdot u)$ yuan/m³.

**Unit Conversion:**
- Prices are in thousand yuan / thousand m³.
- Volumes are in thousand m³.
- Storage cost is given in yuan/m³. Converting to consistent units:
  - $a = 70$ yuan/m³ = $0.07$ thousand yuan / thousand m³.
  - $b = 100$ yuan/m³/quarter = $0.1$ thousand yuan / thousand m³ / quarter.
- Storage cost for a unit (thousand m³) stored for $u$ quarters: $(0.07 + 0.1 \cdot u)$ thousand yuan.

## Decision Variables

Let:
- $x_t \geq 0$: Quantity of timber **purchased** at the beginning of quarter $t$ (thousand m³). Continuous.
- $y_t \geq 0$: Quantity of timber **sold** during quarter $t$ (thousand m³). Continuous.
- $z_t \geq 0$: Quantity of timber **stored in the warehouse at the end of quarter $t$** (thousand m³). Continuous.
- $w_{t,k} \geq 0$: Quantity of timber (thousand m³) that is purchased in quarter $t$ and stored for exactly $k$ quarters (i.e., sold in quarter $t+k$), where $k \geq 1$ and $t+k \leq 4$. Continuous.

**Variable Domains:**
- $x_t, y_t, z_t, w_{t,k} \geq 0$ for all valid indices.
- All variables are **continuous** (timber volume is a continuous resource).

## Objective Function

Maximize total annual profit (thousand yuan):

$$
\max \sum_{t=1}^{4} \left( s_t \cdot y_t - p_t \cdot x_t - \sum_{k=1}^{4-t} (0.07 + 0.1k) \cdot w_{t,k} \right)
$$

Expanded:
$$
\max \left[ 425 y_1 + 440 y_2 + 465 y_3 + 455 y_4 - 410 x_1 - 430 x_2 - 460 x_3 - 450 x_4 - \sum_{t=1}^{3} \sum_{k=1}^{4-t} (0.07 + 0.1k) w_{t,k} \right]
$$

## Operational Constraints

### 1. Warehouse Capacity Constraint
The total timber stored at the end of each quarter must not exceed the warehouse capacity:
$$
z_t \leq 20, \quad \forall t = 1, 2, 3
$$
Note: $z_4 = 0$ is enforced by the "all stored timber must be sold by end of autumn" constraint below.

### 2. Inventory Balance (Flow Conservation)
For each quarter $t$, the timber available (previous inventory + new purchase) must equal timber sold plus timber carried forward:

**Quarter 1 (Winter):**
$$
z_0 + x_1 = y_1 + z_1
$$
Since there is no initial inventory, $z_0 = 0$:
$$
x_1 = y_1 + z_1
$$

**Quarter 2 (Spring):**
$$
z_1 + x_2 = y_2 + z_2
$$

**Quarter 3 (Summer):**
$$
z_2 + x_3 = y_3 + z_3
$$

**Quarter 4 (Autumn):**
All stored timber must be sold by the end of autumn, so $z_4 = 0$:
$$
z_3 + x_4 = y_4
$$

### 3. Sales Volume Limits
Sales in each quarter cannot exceed the estimated maximum sales volume:
$$
y_t \leq D_t, \quad \forall t = 1, 2, 3, 4
$$
Specifically:
- $y_1 \leq 100$
- $y_2 \leq 140$
- $y_3 \leq 200$
- $y_4 \leq 160$

### 4. Storage Tracking Consistency
The total timber stored at the end of quarter $t$ equals the sum of all timber purchased in earlier quarters that is still in storage (to be sold in future quarters):

$$
z_t = \sum_{i=1}^{t-1} \sum_{k=t-i+1}^{4-i} w_{i,k}, \quad \forall t = 1, 2, 3, 4
$$

Equivalently, for each purchase quarter $i$, the total quantity purchased must equal quantity sold in the same quarter plus quantity stored for future quarters:
$$
x_i = y_i^{(i)} + \sum_{k=1}^{4-i} w_{i,k}, \quad \forall i = 1, 2, 3, 4
$$
where $y_i^{(i)}$ is the portion of purchase $x_i$ sold in the same quarter $i$. However, since we do not track which specific purchase lot is sold in which quarter separately from $y_t$, we use the inventory balance constraints above together with the definition that total sold $y_t$ comes from all available inventory.

**Simplified Approach:** Instead of tracking individual lots via $w_{t,k}$, we can compute storage cost directly from inventory levels. The storage cost in quarter $t$ is based on the inventory held during that quarter. A unit stored at the end of quarter $t$ has been in storage for one additional quarter.

Let us redefine storage cost more cleanly: The cost of storing $z_t$ thousand m³ for the quarter $t$ to quarter $t+1$ is based on how long each unit has been stored. To maintain linearity, we use the $w_{t,k}$ formulation:

For each quarter $t$ and storage duration $k$ (where $k$ is the number of quarters the timber is stored, i.e., purchased in $t$ and sold in $t+k$):
- $w_{t,k}$: amount purchased in quarter $t$ that is sold in quarter $t+k$.

**Linking constraints:**

**Purchase decomposition:**
$$
x_t = y_t^{\text{same}} + \sum_{k=1}^{4-t} w_{t,k}, \quad \forall t = 1, 2, 3, 4
$$
where $y_t^{\text{same}}$ is the amount of timber purchased in quarter $t$ and sold in quarter $t$. But since we don't distinguish which sales come from which purchases, we use inventory balance instead.

**Cleaner formulation using inventory and per-quarter storage cost:**

The storage cost in quarter $t$ for inventory $z_t$ depends on how long each unit has been in storage. To keep the model linear, we track the age of inventory using $w_{t,k}$ variables as defined.

**Final constraint set using $w_{t,k}$:**

**A. Purchase equals same-quarter sale portion + stored portions:**
Let $v_t$ be the quantity purchased in quarter $t$ and sold in quarter $t$ (no storage). Then:
$$
x_t = v_t + \sum_{k=1}^{4-t} w_{t,k}, \quad \forall t = 1, 2, 3, 4
$$

**B. Sales in quarter $t$ come from same-quarter purchase plus previously stored timber:**
$$
y_t = v_t + \sum_{i=1}^{t-1} w_{i, t-i}, \quad \forall t = 1, 2, 3, 4
$$
(where the sum is empty if $t=1$)

**C. Inventory at end of quarter $t$:**
$$
z_t = \sum_{i=1}^{t-1} \sum_{k=t-i+1}^{4-i} w_{i,k}, \quad \forall t = 1, 2, 3
$$
and $z_4 = 0$ (enforced by constraint B for $t=4$: all $w_{i,4-i}$ for $i<4$ are sold in quarter 4, so nothing remains).

**D. Capacity:**
$$
z_t \leq 20, \quad \forall t = 1, 2, 3
$$

**E. Sales limits:**
$$
y_t \leq D_t, \quad \forall t = 1, 2, 3, 4
$$

**F. Non-negativity:**
$$
x_t, y_t, v_t, z_t, w_{t,k} \geq 0
$$

### Valid $(t,k)$ pairs for $w_{t,k}$:
- $t=1$: $k \in \{1, 2, 3\}$ (sold in quarters 2, 3, 4)
- $t=2$: $k \in \{1, 2\}$ (sold in quarters 3, 4)
- $t=3$: $k \in \{1\}$ (sold in quarter 4)
- $t=4$: no $w_{4,k}$ (must be sold in same quarter, so $v_4 = x_4$)

## Feasibility Sanity Check

- Total maximum sales over 4 quarters: $100 + 140 + 200 + 160 = 600$ thousand m³.
- Total maximum purchase is not explicitly capped, but limited by sales capacity and storage.
- Storage capacity is 20 thousand m³ per quarter end, which is small relative to quarterly sales (100–200). This means the company can only carry at most 20 thousand m³ from one quarter to the next.
- The problem is feasible: e.g., buy and sell within each quarter with zero storage.
- The "all stored timber must be sold by end of autumn" constraint is naturally satisfied by the model structure ($z_4 = 0$).

## Summary of All Constraints (Compact Form)

$$
\begin{aligned}
&\text{Maximize} && \sum_{t=1}^{4} \left( s_t y_t - p_t x_t - \sum_{k=1}^{4-t} (0.07 + 0.1k) w_{t,k} \right) \\
&\text{Subject to:} && \\
&x_t = v_t + \sum_{k=1}^{4-t} w_{t,k} && \forall t = 1,2,3,4 \\
&y_t = v_t + \sum_{i=1}^{t-1} w_{i, t-i} && \forall t = 1,2,3,4 \\
&z_t = \sum_{i=1}^{t-1} \sum_{k=t-i+1}^{4-i} w_{i,k} && \forall t = 1,2,3 \\
&z_4 = 0 && \\
&z_t \leq 20 && \forall t = 1,2,3 \\
&y_t \leq D_t && \forall t = 1,2,3,4 \\
&x_t, y_t, v_t, z_t, w_{t,k} \geq 0 && \text{for all valid indices}
\end{aligned}
$$

This is a **Linear Programming** model with:
- 4 $x_t$ variables
- 4 $y_t$ variables
- 4 $v_t$ variables
- 3 $z_t$ variables ($z_4$ is fixed to 0)
- 6 $w_{t,k}$ variables: $(1,1),(1,2),(1,3),(2,1),(2,2),(3,1)$

Total: **21 continuous decision variables**.