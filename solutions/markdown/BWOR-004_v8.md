## Mathematical Optimization Model

### Model Type
**MILP** (Mixed-Integer Linear Program)

---

### Index Sets & Parameters

**Index Sets:**
- $t \in \{1, 2, 3, 4, 5, 6\}$: months (January through June)

**Parameters (all values extracted from problem text):**

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| Monthly demand | $D_t$ | $D_1=3000, D_2=3600, D_3=4000, D_4=4600, D_5=4800, D_6=5000$ | units |
| Labor hours per unit | $h$ | 4 | hours/unit |
| Raw material cost per unit | $c_m$ | 150 | dollars/unit |
| Selling price per unit | $p$ | 240 | dollars/unit |
| Initial skilled workers | $W_0$ | 80 | workers |
| Monthly hours per skilled worker | $H$ | 160 | hours/month |
| Training time per new worker | $h_{tr}$ | 50 | hours |
| Skilled worker monthly salary | $c_w$ | 2000 | dollars/month |
| Trainee monthly allowance | $c_{tr}$ | 800 | dollars/month |
| Monthly attrition rate | $\alpha$ | 0.02 | fraction |
| Initial inventory | $I_0$ | 400 | units |
| Max ending inventory (June) | $I_{\max}$ | 100 | units |
| Storage cost per unit per month | $c_s$ | 10 | dollars/unit/month |

---

### Decision Variables

| Variable | Domain | Description |
|----------|--------|-------------|
| $W_t$ | Integer, $\geq 0$ | Number of skilled workers **on the job during** month $t$ (after attrition, before new hires join) |
| $N_t$ | Integer, $\geq 0$ | Number of new workers **hired (started training)** in month $t$ |
| $P_t$ | Continuous, $\geq 0$ | Production quantity (in units) in month $t$ |
| $I_t$ | Continuous, $\geq 0$ | Ending inventory (in units) at the end of month $t$ |

**Domain Justification:**
- $W_t$ and $N_t$ are INTEGER: workers are discrete physical units.
- $P_t$ and $I_t$ are CONTINUOUS: aggregate production and inventory quantities.

---

### Objective Function

$$
\max \quad \sum_{t=1}^{6} \left[ (p - c_m) \, P_t \;-\; c_w \, W_t \;-\; c_{tr} \, N_t \;-\; c_s \, I_t \right]
$$

Substituting numeric values:

$$
\max \quad \sum_{t=1}^{6} \left[ 90 \, P_t \;-\; 2000 \, W_t \;-\; 800 \, N_t \;-\; 10 \, I_t \right]
$$

**Explanation:**
- Net contribution per unit sold: $p - c_m = 240 - 150 = 90$ dollars. (All produced units are sold to meet demand; inventory carries over to next month's demand satisfaction.)
- Labor cost: $2000$ per skilled worker per month.
- Training allowance: $800$ per trainee per training month.
- Storage cost: $10$ per unit held at end of each month.

> **Note on revenue interpretation:** The problem asks to "maximize total revenue." In standard production planning with fixed selling price, this is equivalent to maximizing profit (revenue − costs) since revenue = $p \times \text{total units sold}$ is fixed by demand. The objective above maximizes net profit, which is the economically meaningful interpretation.

---

### Operational Constraints

#### 1. Workforce Balance (Attrition and Hiring)

The number of skilled workers available in month $t$ equals those who survived from month $t-1$ plus those who completed training in month $t-1$:

$$
W_t = (1 - \alpha) \, W_{t-1} + (1 - \alpha) \, N_{t-1}, \quad \forall \, t = 2, 3, 4, 5, 6
$$

With $W_1 = W_0 = 80$ (no trainees at start, so $N_0 = 0$):

$$
W_1 = 80
$$

For $t = 2, \ldots, 6$:

$$
W_t = 0.98 \, W_{t-1} + 0.98 \, N_{t-1}
$$

**Timing clarification:** Workers hired in month $t-1$ spend month $t-1$ in training. During month $t-1$, they are trainees (paid $c_{tr}$). They become skilled at the start of month $t$. In month $t$, they are subject to the same 2% attrition as other skilled workers (they have been on the job for at least one month as of month $t+1$... actually, re-reading: "including those newly trained and on the job for at least one month").

**Revised timing interpretation:** The 2% attrition applies to all skilled workers who have been on the job for **at least one month**. A worker who completes training at the end of month $t$ becomes skilled at the start of month $t+1$. In month $t+1$, they are in their **first** month on the job — they have NOT yet been on the job for "at least one month" (that completes at the end of month $t+1$). Therefore, they are **exempt** from attrition in month $t+1$, and subject to attrition starting from month $t+2$.

Let me re-formulate with this correct interpretation:

- $W_t^{\text{old}}$: skilled workers who have been on the job for ≥1 month during month $t$ (subject to attrition)
- $W_t^{\text{new}}$: skilled workers in their first month on the job during month $t$ (exempt from attrition)

A worker hired in month $s$ becomes skilled at start of month $s+1$.
- In month $s+1$: first month on job → exempt from attrition
- In month $s+2$: second month on job → subject to attrition
- Generally: in month $t$ where $t \geq s+2$: subject to attrition

This requires tracking cohorts. Let $N_s$ be hires in month $s$. A worker hired in month $s$ is:
- Trainee in month $s$
- Skilled (first month, exempt) in month $s+1$
- Skilled (subject to attrition) in months $s+2, s+3, \ldots$

Let me define the workforce balance more carefully using cohort tracking:

Let $A_t$ = number of skilled workers in month $t$ who are subject to attrition (on job ≥1 month).
Let $B_t$ = number of skilled workers in month $t$ who are in their first month (exempt from attrition).

Then:
$$
W_t = A_t + B_t
$$

Transitions:
- $B_t = (1 - \alpha) \cdot 0 + N_{t-1}$... 

Actually, let me reconsider. The workers who become skilled in month $t$ are those who were trainees in month $t-1$, i.e., $N_{t-1}$. These workers are in their **first** month of skilled work in month $t$. They are exempt from attrition in month $t$.

The workers who are subject to attrition in month $t$ are those who were skilled (and subject to attrition) in month $t-1$, who survived.

Let me define:
- $A_t$: skilled workers in month $t$ who have been on the job for ≥1 month (i.e., they were already skilled in month $t-1$ and survived attrition). These are subject to attrition **at the end** of month $t$ (or equivalently, they may leave during month $t$).

Wait, I need to be more precise about when attrition occurs. "Each month, 2% of skilled workers (including those newly trained and on the job for at least one month) leave." This means: at each month, 2% of the eligible pool leaves. The eligible pool in month $t$ includes all skilled workers who have completed at least one full month of skilled work.

Let me re-interpret: A worker who starts training in month $s$ finishes at end of month $s$, starts skilled work in month $s+1$. At the end of month $s+1$, they have completed one month of skilled work. So in month $s+2$, they are "on the job for at least one month" and thus subject to attrition.

**Cleaner formulation using cohort variables:**

Define $S_t$ = total skilled workers working in month $t$.
- $S_1 = 80$
- Workers hired in month $t-1$ ($N_{t-1}$) join the skilled workforce at the start of month $t$.
- Of the skilled workers who were present in month $t-1$ AND have been on the job for ≥1 month (i.e., they were already skilled in month $t-1$ and not in their first month), 2% leave.

This is getting complex. Let me use a simpler but accurate approach:

Since the attrition exemption only applies to workers in their **first** month of skilled work, and those workers are exactly $N_{t-1}$ (hired in month $t-1$, first skilled month is $t$), I can track:

- $E_t$ = number of skilled workers in month $t$ who are **eligible** for attrition (on job ≥1 month as of start of month $t$).
- $F_t$ = number of skilled workers in month $t$ who are **exempt** (in their first month of skilled work).

Then:
- $W_t = E_t + F_t$
- $F_t = N_{t-1}$ (for $t \geq 2$); $F_1 = 0$
- $E_t = 0.98 \cdot E_{t-1} + 0.98 \cdot F_{t-1}$ for $t \geq 2$; $E_1 = 80$ (all 80 initial workers have been on the job for ≥1 month, assumed)

Wait, at the beginning of January, the 80 workers are already skilled and presumably have been on the job for a while. So $E_1 = 80$, $F_1 = 0$.

For $t = 2$:
- $F_2 = N_1$ (workers hired in Jan, first skilled month is Feb)
- $E_2 = 0.98 \cdot E_1 + 0.98 \cdot F_1 = 0.98 \cdot 80 + 0 = 78.4$

But $E_2$ must be integer. Since $W_t$ is integer, I'll keep the constraint in integer form.

Actually, for a MILP, I can work with the total $W_t$ and handle the exemption implicitly. Let me reconsider whether the exemption simplifies things.

**Simplification:** The problem says "2% of skilled workers (including those newly trained and on the job for at least one month) leave." The parenthetical clarifies that newly trained workers who have completed at least one month ARE included. The key question is: are workers in their **first** month (just completed training) subject to attrition?

"on the job for at least one month" — if a worker just started skilled work this month, they have been on the job for **zero** months (just started). So they are NOT yet "on the job for at least one month." Hence exempt in their first month.

Given the complexity, let me use the two-variable approach ($E_t, F_t$) but consolidate into a single integer variable $W_t$ with an auxiliary:

**Final workforce formulation:**

$$
W_1 = 80
$$

For $t = 2, 3, 4, 5, 6$:
$$
W_t = \left\lfloor 0.98 \cdot (W_{t-1} - N_{t-2}^{(\text{exempt in } t-1)}) \right\rfloor + N_{t-1}
$$

This is getting unwieldy with floors. Since we're in a MILP and the numbers are moderate, let me instead note that the exemption applies to $N_{t-1}$ workers in month $t$ (their first month). The workers subject to attrition in month $t$ are $W_{t-1} - N_{t-1} + N_{t-2}$... 

Let me take a step back and use a cleaner state variable approach:

Let $W_t$ = total skilled workers in month $t$.
Let $X_t$ = number of skilled workers in month $t$ who are in their **first** month (exempt from attrition).

Then:
- $X_1 = 0$
- $X_t = N_{t-1}$ for $t = 2, \ldots, 6$

The number of workers subject to attrition in month $t$ is $W_t - X_t$.
Of these, 2% leave during month $t$, so $0.98(W_t - X_t)$ remain for next month.
Plus, $X_t$ workers (exempt) all remain (they don't leave in their first month).

So the recurrence is:
$$
W_{t+1} = 0.98 \cdot (W_t - X_t) + X_t + N_t
$$

Wait, that's not right either. Let me think step by step for month $t \to t+1$:

1. At start of month $t$: $W_t$ skilled workers, of which $X_t$ are in their first month.
2. During month $t$: $0.98(W_t - X_t)$ of the non-exempt workers remain; all $X_t$ exempt workers remain.
3. So at end of month $t$: $0.98(W_t - X_t) + X_t$ skilled workers remain.
4. Additionally, $N_t$ new hires start training in month $t$ and become skilled at start of month $t+1$.
5. So at start of month $t+1$: $W_{t+1} = 0.98(W_t - X_t) + X_t + N_t$

And $X_{t+1} = N_t$ (the new hires who just became skilled).

This is correct. Now, since $X_t = N_{t-1}$ for $t \geq 2$ and $X_1 = 0$, I can substitute:

For $t = 1$:
$$
W_2 = 0.98(W_1 - 0) + 0 + N_1 = 0.98 \cdot 80 + N_1 = 78.4 + N_1
$$

For $t = 2, 3, 4, 5$:
$$
W_{t+1} = 0.98(W_t - N_{t-1}) + N_{t-1} + N_t = 0.98 W_t - 0.98 N_{t-1} + N_{t-1} + N_t = 0.98 W_t + 0.02 N_{t-1} + N_t
$$

**Constraint 1a:** $W_1 = 80$

**Constraint 1b:** For $t = 2, 3, 4, 5, 6$:
$$
W_t = 0.98 \, W_{t-1} + 0.02 \, N_{t-2} + N_{t-1}, \quad \text{where } N_0 = 0
$$

Wait, let me re-derive for general $t \geq 2$:
$$
W_t = 0.98(W_{t-1} - N_{t-2}) + N_{t-2} + N_{t-1} = 0.98 W_{t-1} - 0.98 N_{t-2} + N_{t-2} + N_{t-1} = 0.98 W_{t-1} + 0.02 N_{t-2} + N_{t-1}
$$

With $N_0 = 0$ (no hires before January):
- $t=2$: $W_2 = 0.98 W_1 + 0.02 N_0 + N_1 = 78.4 + N_1$
- $t=3$: $W_3 = 0.98 W_2 + 0.02 N_1 + N_2$
- $t=4$: $W_4 = 0.98 W_3 + 0.02 N_2 + N_3$
- $t=5$: $W_5 = 0.98 W_4 + 0.02 N_3 + N_4$
- $t=6$: $W_6 = 0.98 W_5 + 0.02 N_4 + N_5$

Since $W_t$ must be integer, and $0.98 W_{t-1}$ may not be integer, I need to handle this. In practice, for a MILP, I can keep the equation as-is and let the solver handle integrality of $W_t$ (the LHS is integer, so the RHS must evaluate to an integer, which constrains $W_{t-1}$ and $N$ values appropriately). Alternatively, I can introduce the equation as a linear constraint and rely on the integer nature of $W_t$ to enforce consistency.

Actually, in a standard MILP formulation, I write:
$$
W_t - 0.98 W_{t-1} - 0.02 N_{t-2} - N_{t-1} = 0
$$

This is a linear equality. Since $W_t$ and $N_{t-1}$ are integers, and $0.98 W_{t-1} + 0.02 N_{t-2}$ must equal an integer, this implicitly constrains the feasible integer combinations. The solver will handle this correctly.

#### 2. Production Capacity Constraint

Total skilled labor hours available in month $t$: $H \cdot W_t = 160 \, W_t$ hours.

Hours consumed:
- Training: $50 \, N_t$ hours (each new worker requires 50 hours of skilled labor)
- Production: $4 \, P_t$ hours

$$
4 \, P_t + 50 \, N_t \leq 160 \, W_t, \quad \forall \, t = 1, \ldots, 6
$$

#### 3. Inventory Balance

$$
I_t = I_{t-1} + P_t - D_t, \quad \forall \, t = 1, \ldots, 6
$$

With $I_0 = 400$:
- $I_1 = 400 + P_1 - 3000$
- $I_2 = I_1 + P_2 - 3600$
- $I_3 = I_2 + P_3 - 4000$
- $I_4 = I_3 + P_4 - 4600$
- $I_5 = I_4 + P_5 - 4800$
- $I_6 = I_5 + P_6 - 5000$

#### 4. Ending Inventory Constraint (June)

$$
I_6 \leq 100
$$

#### 5. Non-negativity and Domain Constraints

$$
W_t \geq 0, \; \text{integer}, \quad \forall \, t = 1, \ldots, 6
$$
$$
N_t \geq 0, \; \text{integer}, \quad \forall \, t = 1, \ldots, 6
$$
$$
P_t \geq 0, \quad \forall \, t = 1, \ldots, 6
$$
$$
I_t \geq 0, \quad \forall \, t = 1, \ldots, 6
$$

---

### Complete Model Summary

$$
\boxed{
\begin{aligned}
\max \quad & \sum_{t=1}^{6} \left( 90 \, P_t - 2000 \, W_t - 800 \, N_t - 10 \, I_t \right) \\[6pt]
\text{s.t.} \quad 
& W_1 = 80 \\
& W_t = 0.98 \, W_{t-1} + 0.02 \, N_{t-2} + N_{t-1}, \quad t = 2, \ldots, 6 \;\; (N_0 = 0) \\
& 4 \, P_t + 50 \, N_t \leq 160 \, W_t, \quad t = 1, \ldots, 6 \\
& I_t = I_{t-1} + P_t - D_t, \quad t = 1, \ldots, 6 \;\; (I_0 = 400) \\
& I_6 \leq 100 \\
& W_t \in \mathbb{Z}_{\geq 0}, \quad t = 1, \ldots, 6 \\
& N_t \in \mathbb{Z}_{\geq 0}, \quad t = 1, \ldots, 6 \\
& P_t \geq 0, \quad t = 1, \ldots, 6 \\
& I_t \geq 0, \quad t = 1, \ldots, 6
\end{aligned}
}
$$

Where $D = [3000, 3600, 4000, 4600, 4800, 5000]$.

---

### Feasibility Sanity Check

- **Total demand:** $3000+3600+4000+4600+4800+5000 = 25{,}000$ units
- **Initial inventory:** 400 units
- **Required production:** At least $25{,}000 - 400 = 24{,}600$ units (if $I_6 = 0$), up to $25{,}000 - 400 + 100 = 24{,}700$ units (if $I_6 = 100$)
- **Labor capacity (no hires):** 80 workers × 160 hrs = 12,800 hrs/month → 3,200 units/month max
- **Total 6-month capacity (no hires, no training):** ~19,200 units < 24,600 → **Hiring is necessary.**
- The model will determine the optimal hiring schedule $N_t$ and production plan $P_t$ to balance the trade-off between labor/training costs and the ability to meet demand within the inventory constraint.