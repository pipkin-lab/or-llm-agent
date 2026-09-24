## Model Type
**LP** (Linear Programming)

## Index Sets & Parameters

**Index Sets:**
- $M = \{1, 2, 3, 4\}$: Set of months.
- $D = \{1, 2, 3, 4\}$: Set of possible contract durations (in months).
- $S_{t,d} = \{k \in M \mid k \ge t\}$: Set of months covered by a contract of duration $d$ signed at the beginning of month $t$. Specifically, a contract signed at month $t$ with duration $d$ covers months $t, t+1, \dots, t+d-1$.

**Parameters:**
- $R_t$: Required warehouse area (m²) in month $t$.
  - $R_1 = 1500$
  - $R_2 = 1000$
  - $R_3 = 2000$
  - $R_4 = 1200$
- $C_d$: Total rental cost per m² for a contract of duration $d$ months. Note that this is the *total* cost for the entire duration, not per month.
  - $C_1 = 28$ yuan/m²
  - $C_2 = 45$ yuan/m²
  - $C_3 = 60$ yuan/m²
  - $C_4 = 73$ yuan/m²

## Decision Variables

- $x_{t,d}$: The amount of warehouse space (m²) rented via a contract of duration $d$ months signed at the beginning of month $t$.
  - Domain: $x_{t,d} \ge 0, \forall t \in M, d \in D, \text{ such that } t+d-1 \le 4$ (contract must end by month 4).
  - Valid $(t,d)$ pairs:
    - $t=1$: $d \in \{1, 2, 3, 4\}$ (covers up to month 4)
    - $t=2$: $d \in \{1, 2, 3\}$ (covers up to month 4)
    - $t=3$: $d \in \{1, 2\}$ (covers up to month 4)
    - $t=4$: $d \in \{1\}$ (covers month 4)

## Objective Function

Minimize the total rental cost:

$$
\text{Minimize } Z = \sum_{t \in M} \sum_{d \in D} C_d \cdot x_{t,d}
$$

Expanding with valid indices:
$$
Z = 28x_{1,1} + 45x_{1,2} + 60x_{1,3} + 73x_{1,4} + 28x_{2,1} + 45x_{2,2} + 60x_{2,3} + 28x_{3,1} + 45x_{3,2} + 28x_{4,1}
$$

## Operational Constraints

**1. Capacity Coverage Constraints:**
For each month $t$, the total area from all active contracts must meet the required area $R_t$. A contract $x_{t',d}$ is active in month $t$ if $t' \le t \le t'+d-1$.

- **Month 1:**
  $$x_{1,1} + x_{1,2} + x_{1,3} + x_{1,4} \ge 1500$$

- **Month 2:**
  $$x_{1,2} + x_{1,3} + x_{1,4} + x_{2,1} + x_{2,2} + x_{2,3} \ge 1000$$

- **Month 3:**
  $$x_{1,3} + x_{1,4} + x_{2,2} + x_{2,3} + x_{3,1} + x_{3,2} \ge 2000$$

- **Month 4:**
  $$x_{1,4} + x_{2,3} + x_{3,2} + x_{4,1} \ge 1200$$

**2. Non-negativity Constraints:**
$$x_{t,d} \ge 0 \quad \forall \text{ valid } (t,d)$$