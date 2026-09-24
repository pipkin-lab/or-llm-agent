# Mathematical Model: Production Allocation with Setup Costs

## Model Type: MILP (Mixed-Integer Linear Programming)

> The model is linear in both the objective and constraints, but requires binary variables to activate setup costs, making it a MILP.

---

## Cost Inventory (Pre-Modeling Step)

| Parameter | Machine A | Machine B | Machine C | Machine D |
|---|---|---|---|---|
| Setup Cost $f_i$ (Yuan) | 1000 | 920 | 800 | 700 |
| Unit Cost $c_i$ (Yuan/unit) | 20 | 24 | 16 | 28 |
| Max Capacity $U_i$ (units) | 900 | 1000 | 1200 | 1600 |

Total demand $D = 2000$ units.

**Objective parameter cross-reference:**
- $f_A = 1000$, $f_B = 920$, $f_C = 800$, $f_D = 700$ ✓
- $c_A = 20$, $c_B = 24$, $c_C = 16$, $c_D = 28$ ✓
- $U_A = 900$, $U_B = 1000$, $U_C = 1200$, $U_D = 1600$ ✓
- $D = 2000$ ✓

All objective and constraint parameters are fully specified.

---

## Index Sets & Parameters

**Index Set:**
- $i \in \mathcal{I} = \{A, B, C, D\}$: set of machines.

**Parameters:**

| Symbol | Description | Values |
|---|---|---|
| $f_i$ | Fixed setup cost for machine $i$ (Yuan) | $f_A=1000,\; f_B=920,\; f_C=800,\; f_D=700$ |
| $c_i$ | Variable unit production cost for machine $i$ (Yuan/unit) | $c_A=20,\; c_B=24,\; c_C=16,\; c_D=28$ |
| $U_i$ | Maximum production capacity of machine $i$ (units) | $U_A=900,\; U_B=1000,\; U_C=1200,\; U_D=1600$ |
| $D$ | Total required production (units) | $D = 2000$ |

---

## Decision Variables

| Variable | Domain | Description |
|---|---|---|
| $x_i \geq 0$ | Continuous, $\forall i \in \mathcal{I}$ | Number of units produced on machine $i$ |
| $y_i \in \{0, 1\}$ | Binary, $\forall i \in \mathcal{I}$ | $y_i = 1$ if machine $i$ is used (setup incurred); $y_i = 0$ otherwise |

---

## Objective Function

**Minimize total cost (setup costs + variable production costs):**

$$\min \sum_{i \in \mathcal{I}} f_i \, y_i + \sum_{i \in \mathcal{I}} c_i \, x_i$$

Expanded:

$$\min \; 1000\,y_A + 920\,y_B + 800\,y_C + 700\,y_D \;+\; 20\,x_A + 24\,x_B + 16\,x_C + 28\,x_D$$

---

## Operational Constraints

### 1. Demand Satisfaction (Equality)

All 2,000 units must be produced:

$$\sum_{i \in \mathcal{I}} x_i = 2000$$

Expanded:
$$x_A + x_B + x_C + x_D = 2000$$

### 2. Capacity Constraints (Linking Production to Setup)

Production on machine $i$ is zero if the machine is not set up, and cannot exceed its maximum capacity if it is used:

$$x_i \leq U_i \, y_i, \quad \forall i \in \mathcal{I}$$

Expanded:
$$x_A \leq 900 \, y_A$$
$$x_B \leq 1000 \, y_B$$
$$x_C \leq 1200 \, y_C$$
$$x_D \leq 1600 \, y_D$$

### 3. Non-negativity and Domain Bounds

$$x_i \geq 0, \quad \forall i \in \mathcal{I}$$
$$y_i \in \{0, 1\}, \quad \forall i \in \mathcal{I}$$

---

## Feasibility Sanity Check

- **Total capacity if all machines are used:** $900 + 1000 + 1200 + 1600 = 4700 \geq 2000$. ✓ Feasible.
- **Can a single machine meet demand?** No single machine has capacity $\geq 2000$ (max is $U_D = 1600$). At least two machines are required.
- **Two-machine combinations meeting demand (capacity $\geq 2000$):**
  - A+B: $900+1000=1900$ ✗
  - A+C: $900+1200=2100$ ✓
  - A+D: $900+1600=2500$ ✓
  - B+C: $1000+1200=2200$ ✓
  - B+D: $1000+1600=2600$ ✓
  - C+D: $1200+1600=2800$ ✓
- The model is feasible and well-posed.

---

## Objective Magnitude Sanity Check

Greedy solution check: Use the cheapest unit-cost machine first.
- Machine C has the lowest unit cost (16 Yuan/unit) and capacity 1200. Produce $x_C = 1200$.
- Remaining: $2000 - 1200 = 800$ units.
- Next cheapest unit cost is Machine A (20 Yuan/unit), capacity 900. Produce $x_A = 800$.
- Total cost = $1000 + 800 + 20(800) + 16(1200) = 1800 + 16000 + 19200 = 37000$ Yuan.

This is a reasonable magnitude (tens of thousands of Yuan for 2,000 units with setup costs). The model's objective scale is consistent with the problem's native units (Yuan). ✓