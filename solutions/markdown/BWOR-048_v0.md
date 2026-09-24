**Model Type:** MILP (Mixed Integer Linear Programming)

### 1. Index Sets & Parameters

**Index Sets:**
- $t \in \{1, 2, 3, 4, 5, 6\}$: Half-year periods (Period 1 is the next half-year, Period 6 is the end of the three-year horizon).
- $i \in \{1, 2, 3\}$: Repair lead time indices (not used directly in indices but helps clarify logic).

**Parameters (all costs in thousand yuan):**
- $D_t$: Demand for engine replacements in period $t$.
  - $D_1 = 100$
  - $D_2 = 70$
  - $D_3 = 80$
  - $D_4 = 120$
  - $D_5 = 150$
  - $D_6 = 140$
- $C_{new} = 10$: Cost to purchase one new engine (thousand yuan).
- $C_{fast} = 2$: Cost for fast repair per engine (thousand yuan).
- $C_{slow} = 10$: Cost for slow repair per engine (thousand yuan). *Note: The text says "10,000 yuan", which is 10 thousand yuan.*

**Derived Parameters / Constants:**
- Lead time for Fast Repair: 1 period (Sent in $t$, Available in $t+1$).
- Lead time for Slow Repair: 2 periods (Sent in $t$, Available in $t+2$).
- Horizon: 6 periods.
- Note: Engines sent for repair in the final periods such that they return after period 6 are useless because the aircraft are decommissioned. Therefore, Fast Repair can only be initiated in periods $t \in \{1, \dots, 5\}$, and Slow Repair can only be initiated in periods $t \in \{1, \dots, 4\}$.

### 2. Decision Variables

Let:
- $N_t$: Number of **new** engines purchased in period $t$. (Integer, $\ge 0$)
- $F_t$: Number of used engines sent for **fast** repair in period $t$. (Integer, $\ge 0$)
- $S_t$: Number of used engines sent for **slow** repair in period $t$. (Integer, $\ge 0$)

*Domain:*
- $N_t \in \mathbb{Z}_{\ge 0}, \quad t = 1, \dots, 6$
- $F_t \in \mathbb{Z}_{\ge 0}, \quad t = 1, \dots, 5$ (Fast repair initiated in $t$ is available in $t+1$; if $t=6$, it arrives at $t=7$ which is outside the horizon).
- $S_t \in \mathbb{Z}_{\ge 0}, \quad t = 1, \dots, 4$ (Slow repair initiated in $t$ is available in $t+2$; if $t=5$, it arrives at $t=7$; if $t=6$, it arrives at $t=8$. Both are outside the horizon).

*Note on Supply of Used Engines:* The problem states "repairing used engines". It implies that there is an available pool of used engines from previous replacements. Since the aircraft have been in service for 3 years (6 half-years) *before* the current planning horizon starts? Or does the planning horizon start *now*?
"Starting from the next half-year... over the next three years".
"Aircraft will be decommissioned after three years".
This implies the aircraft are currently in service. The engines currently installed were installed at some point. The problem doesn't explicitly state the *availability* of used engines for repair at the start. However, standard interpretation of such "replacement" problems where you can "repair used engines" implies that the engines being replaced *become* the used engines available for future repair, OR there is an initial stock.
Let's re-read carefully: "When replacing an engine, it can either be replaced with a new one, or with a repaired used engine."
Usually, in these problems, the "used engine" comes from the pool of engines that were removed in previous periods.
Let $R_t$ be the number of engines removed in period $t$ (which equals $D_t$).
The engines removed in period $t$ become available for repair in period $t$ (to be sent off) or later.
However, the problem asks "how many... should be sent for fast repair... in each period".
Crucially, can we repair an engine that is *currently* being replaced? Yes, that is the standard "repair-or-replace" or "overhaul" model. The engine removed in period $t$ is a "used engine". It can be sent for repair.
BUT, there is a supply constraint: The number of engines sent for repair in period $t$ cannot exceed the number of used engines available.
Where do used engines come from?
1. Engines removed in previous periods that were not repaired? No, if they weren't repaired, they are scrapped or stored. The problem says "engines will be scrapped after that [3 years]". It doesn't explicitly say we can store used engines indefinitely.
2. The most standard interpretation for this specific type of textbook problem (often found in OR textbooks): The "used engines" available for repair in period $t$ are the ones that were removed in period $t$ itself? No, you can't repair it and use it *in the same period* if the repair takes time.
Actually, looking at the lead times:
- Fast: Sent in $t$, Ready in $t+1$.
- Slow: Sent in $t$, Ready in $t+2$.

If I replace an engine in period 1, I get a used engine at the end of period 1. I can send it for repair in period 1. It will be ready in period 2 (Fast) or 3 (Slow).
So, the supply of used engines for repair in period $t$ is limited by the cumulative number of engines removed in periods up to $t$ (minus those already sent for repair).
However, there is a simpler interpretation often intended in these specific problems: **The decision variable $F_t$ and $S_t$ represents the number of engines *repaired* that are *available* in period $t$?**
No, the question asks "how many... should be **sent** for fast repair... in each period". This refers to the initiation of the repair process.

Let's look at the flow:
- Period $t$ Demand $D_t$ must be met by:
  1. New engines bought in $t$ ($N_t$).
  2. Repaired engines becoming available in $t$.
     - Fast repairs sent in $t-1$ ($F_{t-1}$).
     - Slow repairs sent in $t-2$ ($S_{t-2}$).

So the balance equation for meeting demand in period $t$ is:
$D_t = N_t + F_{t-1} + S_{t-2}$
(With $F_0=0, S_0=0, S_{-1}=0$, etc., for boundary conditions).

Is there a constraint on the *availability* of used engines to send for repair?
Yes. The number of engines sent for repair in period $t$ ($F_t + S_t$) cannot exceed the number of used engines available in period $t$.
Who are the used engines available in period $t$?
They are the engines that were removed in periods $1$ through $t$.
Total removed by end of period $t = \sum_{i=1}^t D_i$.
Total sent for repair in periods $1$ through $t-1 = \sum_{i=1}^{t-1} (F_i + S_i)$.
Therefore, the number of used engines available to send for repair in period $t$ is:
$\sum_{i=1}^t D_i - \sum_{i=1}^{t-1} (F_i + S_i)$.
So, the constraint is:
$F_t + S_t \le \sum_{i=1}^t D_i - \sum_{i=1}^{t-1} (F_i + S_i)$
Which simplifies to:
$\sum_{i=1}^t (F_i + S_i) \le \sum_{i=1}^t D_i$

This constraint ensures that we never send more engines for repair than we have removed from the fleet up to that point. This assumes that all removed engines are kept in inventory until sent for repair. The problem states "engines will be scrapped after that [3 years]". This implies they are kept for the 3 years. So this inventory constraint is valid.

### 3. Objective Function

Minimize Total Cost $Z$:
$$ Z = \sum_{t=1}^{6} C_{new} N_t + \sum_{t=1}^{5} C_{fast} F_t + \sum_{t=1}^{4} C_{slow} S_t $$

Substituting values:
$$ \text{Minimize } Z = 10 \sum_{t=1}^{6} N_t + 2 \sum_{t=1}^{5} F_t + 10 \sum_{t=1}^{4} S_t $$

### 4. Operational Constraints

**1. Demand Satisfaction Constraints (Balance Equations):**
For each period $t$, the demand $D_t$ must be met exactly by new engines purchased in $t$ and repaired engines delivered in $t$.

- **Period 1 ($t=1$):**
  $N_1 = D_1$
  (No repairs can be delivered in period 1 because the earliest repair (fast) sent in period 1 arrives in period 2. Assuming no initial stock of repaired engines is available at the start of period 1, as the plant "just received" the task. Even if there were, the problem doesn't specify initial inventory, so we assume $F_0=0, S_0=0$).
  $\Rightarrow N_1 = 100$

- **Period 2 ($t=2$):**
  $N_2 + F_1 = D_2$
  $\Rightarrow N_2 + F_1 = 70$

- **Period 3 ($t=3$):**
  $N_3 + F_2 + S_1 = D_3$
  $\Rightarrow N_3 + F_2 + S_1 = 80$

- **Period 4 ($t=4$):**
  $N_4 + F_3 + S_2 = D_4$
  $\Rightarrow N_4 + F_3 + S_2 = 120$

- **Period 5 ($t=5$):**
  $N_5 + F_4 + S_3 = D_5$
  $\Rightarrow N_5 + F_4 + S_3 = 150$

- **Period 6 ($t=6$):**
  $N_6 + F_5 + S_4 = D_6$
  $\Rightarrow N_6 + F_5 + S_4 = 140$

**2. Used Engine Availability Constraints (Inventory of Removed Engines):**
The cumulative number of engines sent for repair (fast + slow) in periods $1$ through $t$ cannot exceed the cumulative number of engines removed (demanded) in periods $1$ through $t$.
This ensures we don't repair engines we haven't taken out of the planes yet.

- **For $t=1$:**
  $F_1 + S_1 \le D_1$
  $\Rightarrow F_1 + S_1 \le 100$
  *(Note: $S_1$ is defined. $S_1$ engines sent in period 1 are available in period 3.)*

- **For $t=2$:**
  $F_1 + S_1 + F_2 + S_2 \le D_1 + D_2$
  $\Rightarrow F_1 + S_1 + F_2 + S_2 \le 170$

- **For $t=3$:**
  $F_1 + S_1 + F_2 + S_2 + F_3 + S_3 \le D_1 + D_2 + D_3$
  $\Rightarrow F_1 + S_1 + F_2 + S_2 + F_3 + S_3 \le 250$

- **For $t=4$:**
  $F_1 + S_1 + F_2 + S_2 + F_3 + S_3 + F_4 + S_4 \le D_1 + \dots + D_4$
  $\Rightarrow \sum_{i=1}^4 (F_i + S_i) \le 370$
  *(Note: $D_1+D_2+D_3+D_4 = 100+70+80+120 = 370$)*

- **For $t=5$:**
  $F_1 + S_1 + F_2 + S_2 + F_3 + S_3 + F_4 + S_4 + F_5 \le D_1 + \dots + D_5$
  *(Note: $S_5$ is not defined/allowed because slow repair sent in 5 arrives in 7, outside horizon. So only $F_5$ is added to the left side.)*
  $\Rightarrow \sum_{i=1}^4 (F_i + S_i) + F_5 \le 520$
  *(Note: $D_5 = 150$, Sum = 370 + 150 = 520)*

- **For $t=6$:**
  $F_1 + S_1 + F_2 + S_2 + F_3 + S_3 + F_4 + S_4 + F_5 \le D_1 + \dots + D_6$
  *(Note: No repairs sent in period 6 are useful.)*
  $\Rightarrow \sum_{i=1}^4 (F_i + S_i) + F_5 \le 660$
  *(Note: $D_6 = 140$, Sum = 520 + 140 = 660)*
  *Actually, this constraint is redundant if the demand constraints are equalities and we minimize cost, but it is structurally required for feasibility. Note that the LHS is the total number of engines sent for repair. The RHS is total engines removed. Since we must meet all demand, and repaired engines are just a subset of the "solutions", the total number of engines removed is fixed at 660. The constraint simply says we can't send more than 660 engines for repair, which is physically impossible anyway given the demand constraints.*

**3. Non-negativity and Integrality:**
- $N_t \in \mathbb{Z}_{\ge 0}, \quad t=1,\dots,6$
- $F_t \in \mathbb{Z}_{\ge 0}, \quad t=1,\dots,5$
- $S_t \in \mathbb{Z}_{\ge 0}, \quad t=1,\dots,4$

### Summary of the Model

**Minimize:**
$$ 10(N_1 + N_2 + N_3 + N_4 + N_5 + N_6) + 2(F_1 + F_2 + F_3 + F_4 + F_5) + 10(S_1 + S_2 + S_3 + S_4) $$

**Subject to:**
1. $N_1 = 100$
2. $N_2 + F_1 = 70$
3. $N_3 + F_2 + S_1 = 80$
4. $N_4 + F_3 + S_2 = 120$
5. $N_5 + F_4 + S_3 = 150$
6. $N_6 + F_5 + S_4 = 140$
7. $F_1 + S_1 \le 100$
8. $F_1 + S_1 + F_2 + S_2 \le 170$
9. $F_1 + S_1 + F_2 + S_2 + F_3 + S_3 \le 250$
10. $F_1 + S_1 + F_2 + S_2 + F_3 + S_3 + F_4 + S_4 \le 370$
11. $F_1 + S_1 + F_2 + S_2 + F_3 + S_3 + F_4 + S_4 + F_5 \le 520$
12. $F_1 + S_1 + F_2 + S_2 + F_3 + S_3 + F_4 + S_4 + F_5 \le 660$ (Redundant but included for completeness)

**Variables:**
$N_t, F_t, S_t$ are non-negative integers.