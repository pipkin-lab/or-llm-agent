# Timber Storage and Transportation Optimization Model

## Model Type: LP (Linear Program)

---

## Index Sets & Parameters

**Index Sets:**
- $t = \{1, 2, 3, 4\}$: Quarters (1 = Winter, 2 = Spring, 3 = Summer, 4 = Autumn)

**Parameters (all values from Table 1-18):**

| Parameter | Description | $t=1$ | $t=2$ | $t=3$ | $t=4$ |
|-----------|-------------|-------|-------|-------|-------|
| $P_t$ | Purchase price (thousand yuan / thousand m³) | 410 | 430 | 460 | 450 |
| $S_t$ | Selling price (thousand yuan / thousand m³) | 425 | 440 | 465 | 455 |
| $D_t$ | Max sales volume (thousand m³) | 100 | 140 | 200 | 160 |

**Storage Parameters:**
- $K = 20$: Warehouse capacity (thousand m³)
- $a = 70$: Base storage cost (yuan per m³)
- $b = 100$: Incremental storage cost per quarter (yuan per m³ per quarter)

**Unit Conversion:**
- Prices are in **thousand yuan per thousand m³**, so revenue/cost per thousand m³ is directly in thousand yuan.
- Storage cost: $(a + b \cdot u)$ yuan per m³ = $(0.07 + 0.10 \cdot u)$ thousand yuan per thousand m³, where $u$ = number of quarters stored.

---

## Decision Variables

- $x_t \geq 0$: Timber purchased at the beginning of quarter $t$ (thousand m³), $\forall t \in \{1,2,3,4\}$
- $y_{t,s} \geq 0$: Timber purchased in quarter $t$ and sold in quarter $s$ (thousand m³), where $s \geq t$, $\forall t, s \in \{1,2,3,4\}$
- $I_t \geq 0$: Timber remaining in storage at the **end** of quarter $t$ (thousand m³), $\forall t \in \{1,2,3,4\}$

All variables are **CONTINUOUS** (timber is measured in thousand m³, a continuous quantity).

---

## Objective Function

**MAXIMIZE** total annual profit (thousand yuan):

$$\max \sum_{t=1}^{4} \sum_{s=t}^{4} \left[ S_s - P_t - (0.07 + 0.10 \cdot (s - t)) \right] \cdot y_{t,s}$$

**Expanded objective (explicit coefficients per unit flow):**

The profit per thousand m³ of timber bought in quarter $t$ and sold in quarter $s$ is:
$$\pi_{t,s} = S_s - P_t - (0.07 + 0.10(s-t))$$

Computing each $\pi_{t,s}$:

| $t \backslash s$ | $s=1$ | $s=2$ | $s=3$ | $s=4$ |
|---|---|---|---|---|
| $t=1$ | $425-410-0.07 = 14.93$ | $440-410-0.17 = 29.83$ | $465-410-0.27 = 54.73$ | $455-410-0.37 = 44.63$ |
| $t=2$ | — | $440-430-0.07 = 9.93$ | $465-430-0.17 = 34.83$ | $455-430-0.27 = 24.73$ |
| $t=3$ | — | — | $465-460-0.07 = 4.93$ | $455-460-0.17 = -5.17$ |
| $t=4$ | — | — | — | $455-450-0.07 = 4.93$ |

$$\max \; 14.93\,y_{1,1} + 29.83\,y_{1,2} + 54.73\,y_{1,3} + 44.63\,y_{1,4} + 9.93\,y_{2,2} + 34.83\,y_{2,3} + 24.73\,y_{2,4} + 4.93\,y_{3,3} - 5.17\,y_{3,4} + 4.93\,y_{4,4}$$

---

## Operational Constraints

### 1. Flow Conservation (Purchase-Sale Linkage)
Timber purchased in quarter $t$ is either sold in some quarter $s \geq t$ or remains in storage at the end of quarter $t$.

$$x_t = \sum_{s=t}^{4} y_{t,s} + I_t, \quad \forall \; t \in \{1, 2, 3, 4\}$$

### 2. Inventory Balance
The inventory at the end of quarter $t$ equals the inventory from the previous quarter plus new purchases, minus all sales in quarter $t$.

$$I_t = I_{t-1} + x_t - \sum_{\tau=1}^{t} y_{\tau,t}, \quad \forall \; t \in \{1, 2, 3, 4\}$$

with $I_0 = 0$.

Explicitly:
- $I_1 = x_1 - y_{1,1}$
- $I_2 = I_1 + x_2 - y_{1,2} - y_{2,2}$
- $I_3 = I_2 + x_3 - y_{1,3} - y_{2,3} - y_{3,3}$
- $I_4 = I_3 + x_4 - y_{1,4} - y_{2,4} - y_{3,4} - y_{4,4}$

### 3. Warehouse Capacity
Storage at the end of each quarter must not exceed warehouse capacity.

$$I_t \leq 20, \quad \forall \; t \in \{1, 2, 3, 4\}$$

### 4. Sales Volume Limits
Total timber sold in quarter $s$ (from all purchase quarters) cannot exceed the estimated maximum sales volume.

$$\sum_{t=1}^{s} y_{t,s} \leq D_s, \quad \forall \; s \in \{1, 2, 3, 4\}$$

Explicitly:
- $y_{1,1} \leq 100$
- $y_{1,2} + y_{2,2} \leq 140$
- $y_{1,3} + y_{2,3} + y_{3,3} \leq 200$
- $y_{1,4} + y_{2,4} + y_{3,4} + y_{4,4} \leq 160$

### 5. End-of-Year Clearance
All stored timber must be sold by the end of autumn (quarter 4). No timber may remain in storage.

$$I_4 = 0$$

### 6. Non-Negativity
$$x_t \geq 0, \quad y_{t,s} \geq 0, \quad I_t \geq 0, \quad \forall \; t, s \in \{1,2,3,4\}, \; s \geq t$$

---

## Feasibility Sanity Check

- **Total demand** = $100 + 140 + 200 + 160 = 600$ thousand m³.
- **Max storage** = 20 thousand m³, so at most 20 thousand m³ can be carried over between any two adjacent quarters.
- Since $D_t \leq 200$ for each quarter and storage is limited to 20, the binding constraint will be the per-quarter sales caps and the storage capacity, not a global supply shortage (the company can purchase any amount up to sales capacity each quarter).
- The problem is **feasible**: purchasing exactly $D_t$ in each quarter and selling it all in the same quarter (no storage) satisfies all constraints with $I_t = 0$ for all $t$.
- Note: $y_{3,4}$ has a negative profit coefficient ($-5.17$), so the optimal solution will set $y_{3,4} = 0$ unless forced by other constraints (it is not, since $y_{3,4}$ is not required to be positive).

---

## Objective Parameter Cross-Reference

| Parameter Symbol | Value | Source |
|---|---|---|
| $P_1$ | 410 | Table 1-18, Winter row |
| $P_2$ | 430 | Table 1-18, Spring row |
| $P_3$ | 460 | Table 1-18, Summer row |
| $P_4$ | 450 | Table 1-18, Autumn row |
| $S_1$ | 425 | Table 1-18, Winter row |
| $S_2$ | 440 | Table 1-18, Spring row |
| $S_3$ | 465 | Table 1-18, Summer row |
| $S_4$ | 455 | Table 1-18, Autumn row |
| $D_1$ | 100 | Table 1-18, Winter row |
| $D_2$ | 140 | Table 1-18, Spring row |
| $D_3$ | 200 | Table 1-18, Summer row |
| $D_4$ | 160 | Table 1-18, Autumn row |
| $K$ | 20 | Problem text |
| $a$ | 70 | Problem text |
| $b$ | 100 | Problem text |

All parameters are fully specified. No `[NOT_PROVIDED]` values.