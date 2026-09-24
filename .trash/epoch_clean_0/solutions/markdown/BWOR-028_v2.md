### Mathematical Optimization Model: Nurse Staffing Scheduling

#### 1. Index Sets & Parameters

**Index Sets:**
- $K = \{1, 2, 3, 4, 5, 6\}$: Set of shift start times (and corresponding 4-hour periods).
  - $k=1$: Start 2:00
  - $k=2$: Start 6:00
  - $k=3$: Start 10:00
  - $k=4$: Start 14:00
  - $k=5$: Start 18:00
  - $k=6$: Start 22:00

**Parameters:**
- $D_k$: Minimum number of nurses required during the period starting at shift $k$.
  - $D_1 = 10$ (2:00–6:00)
  - $D_2 = 15$ (6:00–10:00)
  - $D_3 = 25$ (10:00–14:00)
  - $D_4 = 20$ (14:00–18:00)
  - $D_5 = 18$ (18:00–22:00)
  - $D_6 = 12$ (22:00–2:00)

- $S_{k,j}$: Binary indicator parameter where $S_{k,j} = 1$ if nurses starting shift $k$ are working during period $j$, and $0$ otherwise.
  - Since each nurse works 8 consecutive hours (covering 2 periods of 4 hours), a nurse starting at shift $k$ works during period $k$ and period $k+1$ (with wrap-around for the last shift).
  - Specifically:
    - $S_{k,j} = 1$ if $j = k$ or $j = (k \mod 6) + 1$.
    - $S_{k,j} = 0$ otherwise.

#### 2. Decision Variables

- $x_k$: The number of nurses assigned to start their shift at time $k$.
  - **Domain**: $x_k \in \mathbb{Z}_{\ge 0}$ for all $k \in K$.
  - *Note*: We use integer variables because nurses are discrete physical units.

#### 3. Objective Function

Minimize the total number of nurses scheduled:

$$ \text{Minimize } Z = \sum_{k=1}^{6} x_k $$

#### 4. Operational Constraints

For each period $j \in K$, the total number of nurses on duty must meet or exceed the demand $D_j$. The nurses on duty in period $j$ are those who started at $j$ and those who started at $j-1$ (the previous shift, wrapping around if $j=1$).

$$ \sum_{k=1}^{6} S_{k,j} x_k \ge D_j \quad \forall j \in K $$

Expanding these constraints explicitly for clarity:

1. **Period 1 (2:00–6:00)**: Covered by shifts starting at 22:00 ($k=6$) and 2:00 ($k=1$).
   $$ x_6 + x_1 \ge 10 $$

2. **Period 2 (6:00–10:00)**: Covered by shifts starting at 2:00 ($k=1$) and 6:00 ($k=2$).
   $$ x_1 + x_2 \ge 15 $$

3. **Period 3 (10:00–14:00)**: Covered by shifts starting at 6:00 ($k=2$) and 10:00 ($k=3$).
   $$ x_2 + x_3 \ge 25 $$

4. **Period 4 (14:00–18:00)**: Covered by shifts starting at 10:00 ($k=3$) and 14:00 ($k=4$).
   $$ x_3 + x_4 \ge 20 $$

5. **Period 5 (18:00–22:00)**: Covered by shifts starting at 14:00 ($k=4$) and 18:00 ($k=5$).
   $$ x_4 + x_5 \ge 18 $$

6. **Period 6 (22:00–2:00)**: Covered by shifts starting at 18:00 ($k=5$) and 22:00 ($k=6$).
   $$ x_5 + x_6 \ge 12 $$

**Non-negativity and Integrality Constraints:**
$$ x_k \in \mathbb{Z}^+ \cup \{0\} \quad \forall k \in \{1, 2, 3, 4, 5, 6\} $$