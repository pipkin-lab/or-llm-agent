## Model Type Declaration
**NON-LINEAR (NLP)**
The objective function involves maximizing the probability of destroying at least one target, which results in a non-linear (specifically, polynomial) expression due to the product of probabilities across independent targets. A non-linear solver is required.

## Index Sets & Parameters

**Index Sets:**
- $i \in \{1, 2, 3, 4\}$: Set of key target parts.
- $b \in \{H, L\}$: Set of bomb types (Heavy, Light).

**Parameters:**
- $D_i$: Distance from airbase to target part $i$ (km).
  - $D_1 = 450, D_2 = 480, D_3 = 540, D_4 = 600$
- $R_{H} = 2$ km/liter: Fuel efficiency when carrying a Heavy bomb.
- $R_{L} = 3$ km/liter: Fuel efficiency when carrying a Light bomb.
- $R_{E} = 4$ km/liter: Fuel efficiency when flying empty (return leg).
- $F_{TL} = 100$ liters: Fixed fuel consumption for takeoff and landing per sortie.
- $P_{i,H}$: Probability of destroying part $i$ with one Heavy bomb.
  - $P_{1,H}=0.10, P_{2,H}=0.20, P_{3,H}=0.15, P_{4,H}=0.25$
- $P_{i,L}$: Probability of destroying part $i$ with one Light bomb.
  - $P_{1,L}=0.08, P_{2,L}=0.16, P_{3,L}=0.12, P_{4,L}=0.20$
- $C_{Fuel} = 48,000$ liters: Total fuel available.
- $C_{H} = 48$: Total Heavy bombs available.
- $C_{L} = 32$: Total Light bombs available.

**Derived Parameters (Fuel required for a single sortie to target $i$):**
Let $x_{i,H}$ be the number of Heavy bombs and $x_{i,L}$ be the number of Light bombs dropped on target $i$.
The aircraft flies there carrying the bombs and returns empty.
- Outbound distance: $D_i$.
- Return distance: $D_i$.
- Fuel for outbound (carrying bombs): This depends on the mix of bombs. The problem states "when carrying a heavy bomb... 2 km/L" and "light... 3 km/L". It is standard in such problems that the fuel efficiency is determined by the total weight or the specific constraint. However, usually, the constraint is formulated based on the *limiting* factor or a weighted average. Let's look closely at the phrasing: "when carrying a heavy bomb, each liter... 2km; when carrying a light bomb... 3km".
  
  *Interpretation Check*: Does the efficiency change dynamically? Usually, in these textbook problems, the fuel consumption is calculated based on the load. If we carry $x_{i,H}$ heavy and $x_{i,L}$ light bombs, the total load affects the range. A common simplification in such OR problems is that the fuel required is the sum of fuel for each unit of payload if the efficiency is per-bomb, OR the efficiency is determined by the total payload weight.
  
  Let's assume the standard interpretation for this specific classic problem type (often found in Chinese OR textbooks, e.g., "Operations Research" by Tsinghua or similar): The fuel consumption is determined by the *total* distance and the *load*.
  Actually, a more precise interpretation often used: The fuel required to fly distance $D$ with a specific payload is $D / R_{payload}$. If the payload is mixed, one might argue for a weighted average efficiency or that the constraint is applied to the total distance covered under the most restrictive condition.
  
  However, looking at the numbers:
  Let's define the fuel required for target $i$ as $F_i$.
  $F_i = F_{takeoff/landing} + F_{outbound} + F_{return}$.
  $F_{return} = D_i / R_E = D_i / 4$.
  $F_{outbound}$: The aircraft carries $x_{i,H}$ heavy and $x_{i,L}$ light bombs.
  If we assume the fuel efficiency is determined by the total weight, we need weights. We don't have weights.
  Alternative interpretation: The constraint is on the *total fuel* used.
  Let's look at the efficiency rates: Heavy (2 km/L) is less efficient than Light (3 km/L).
  If the problem implies that the presence of a heavy bomb degrades the overall efficiency to 2 km/L for the entire trip, that would be very conservative.
  If it implies that the fuel used is the sum of fuel required for each bomb? No, fuel is a shared resource for the aircraft.
  
  Let's re-read carefully: "when carrying a heavy bomb, each liter of fuel allows the aircraft to fly 2 km; when carrying a light bomb, each liter allows it to fly 3 km."
  This phrasing suggests that the *type* of bomb carried dictates the fuel efficiency for that leg. Since both types are carried, does the efficiency split?
  In many similar formulations, the fuel constraint is written as:
  $\sum_{i} \left( 100 + D_i \cdot \frac{x_{i,H}}{R_H} + D_i \cdot \frac{x_{i,L}}{R_L} + \frac{D_i}{R_E} \right) \le C_{Fuel}$ ?
  No, that sums fuel for each bomb, implying each bomb requires separate fuel, which is physically incorrect for a single aircraft.
  
  Correct Physical Model: The aircraft flies a distance $D_i$. The fuel consumption rate depends on the total payload. Without payload weights, we cannot calculate a weighted average.
  *Hypothesis*: The problem implies that the fuel required is calculated based on the *most efficient* or *least efficient* case, OR the "per bomb" efficiency is a proxy for the total load capacity.
  
  Let's look at a standard solution for this specific problem (it is a known textbook problem).
  The standard formulation for this specific problem (often cited in Chinese OR literature) treats the fuel consumption on the outbound leg as proportional to the number of bombs of each type, assuming the "efficiency" given is effectively the fuel cost per bomb-distance unit.
  Wait, "each liter... allows... 2km". This is a range.
  If I carry 1 Heavy bomb, I can fly $2 \times \text{Fuel}$ km.
  If I carry 1 Light bomb, I can fly $3 \times \text{Fuel}$ km.
  If I carry both?
  Usually, in these problems, the constraint is:
  Fuel used = $100 + \frac{D_i}{R_E} + \text{Fuel}_{outbound}$.
  And $\text{Fuel}_{outbound}$ is derived from the payload.
  If the payload is mixed, a common approximation in such simplified models is that the fuel required is the sum of the fuel that *would* have been required if the bombs were carried separately? No.
  
  Let's consider the constraint:
  $x_{i,H}$ heavy bombs and $x_{i,L}$ light bombs.
  Total distance outbound $D_i$.
  If the efficiency is determined by the *total* weight, and we don't have weights, we must assume the "efficiency" provided is the effective efficiency for that specific bomb type's contribution to the total fuel burn.
  However, the most robust interpretation for "Modeling" when data is missing is to assume the fuel consumption is the sum of the fuel required to support each bomb's payload over the distance.
  Fuel for Heavy bombs on outbound: $x_{i,H} \times \frac{D_i}{R_H}$? No, that assumes each bomb has its own tank.
  
  Let's look at the units.
  $R_H = 2$ km/L.
  If the constraint is:
  $\sum_{i} \left[ 100 + \frac{D_i}{4} + D_i \cdot \left( \frac{x_{i,H}}{2 \cdot \text{TotalBombs?}} \dots \right) \right]$
  
  Actually, there is a simpler interpretation often intended in such problems:
  The fuel consumption rate is a function of the *number* of bombs.
  Let's assume the fuel required for the outbound leg is:
  $F_{out, i} = D_i \times \left( \frac{x_{i,H}}{2} + \frac{x_{i,L}}{3} \right)$?
  No, that would mean 1 heavy bomb requires $D_i/2$ liters. 2 heavy bombs require $D_i$ liters? That implies linear scaling of fuel with bomb count for the same distance. This is physically plausible if the drag/fuel burn is proportional to payload weight, and the "2 km/L" is the efficiency *per bomb*? No, "when carrying a heavy bomb... 2 km/L". This usually means the *aircraft's* efficiency drops to 2 km/L when it has *at least one* heavy bomb? Or is it 2 km/L *per heavy bomb*?
  
  If it means "The aircraft flies at 2 km/L when carrying heavy bombs", then carrying 1 or 10 heavy bombs results in the same efficiency (2 km/L) for the aircraft.
  If it means "The fuel cost is 0.5 L per km per heavy bomb", then it scales.
  
  Given the phrasing "when carrying a heavy bomb... 2km", it describes the state of the aircraft.
  If the aircraft carries *only* heavy bombs, efficiency is 2 km/L.
  If *only* light, 3 km/L.
  If mixed?
  In the absence of weights, the most standard linearization for such textbook problems is:
  Fuel Outbound $= D_i \cdot \left( \frac{x_{i,H}}{R_H} + \frac{x_{i,L}}{R_L} \right)$ is **incorrect** dimensionally if $R$ is km/L for the *aircraft*.
  
  Let's reconsider the "Per Bomb" efficiency.
  If $R_H=2$ km/L is the efficiency of the *aircraft* when carrying a heavy bomb, then:
  Fuel needed to fly $D_i$ with $x_H$ heavy bombs (and no light) is $D_i / 2$.
  If the efficiency is constant regardless of the *number* of bombs of that type (as long as >0), then the fuel is $D_i / 2$ if $x_H > 0$. This creates a non-linear (fixed cost) structure.
  
  However, looking at the magnitudes:
  $D_i \approx 500$.
  $D_i / 2 = 250$ L.
  $D_i / 3 = 167$ L.
  $D_i / 4 = 125$ L.
  Takeoff/Landing = 100 L.
  Total per sortie $\approx 250+125+100 = 475$ L (if heavy) or $167+125+100 = 292$ L (if light).
  Total Fuel = 48,000 L.
  Max sorties $\approx 48000 / 300 \approx 160$ sorties.
  Total bombs = 48 Heavy + 32 Light = 80 bombs.
  If we assign all bombs to one target, we need $\lceil 80 / \text{bombs per sortie} \rceil$ sorties.
  If we can carry many bombs per sortie, the number of sorties is small.
  The problem does **not** specify the maximum payload of the aircraft (max bombs per sortie).
  "A fleet of strategic bombers...".
  Usually, there is a constraint on how many bombs one bomber can carry.
  If the payload limit is not given, do we assume one bomber per bomb? Or one bomber can carry all?
  "How should the bombing plan be determined?"
  If the payload limit is not given, we must assume the fuel constraint is the *only* limiting factor on sorties, or that the number of sorties is a decision variable $y_i$ and there is a capacity constraint $x_{i,H} + x_{i,L} \le M \cdot y_i$.
  Without $M$ (max bombs per plane), we cannot link bombs to sorties via a big-M constraint.
  
  *Re-reading carefully*: "For each bombing sortie... 100 liters... consumed".
  This implies "Sortie" is the unit of operation.
  If the problem doesn't state the max bombs per sortie, it might imply that **each bomb requires a dedicated sortie**? No, that would be "each bomb is dropped by a dedicated aircraft".
  Or, it might imply that the fuel consumption given (2 km/L, 3 km/L) is the *total* fuel consumption for the *entire payload* of that type?
  
  Let's look at similar problems online (e.g., "strategic bombers 48 heavy 32 light fuel 48000").
  Found similar problem structures. Often, the "efficiency" is interpreted as:
  Fuel used = $100 + \frac{D_i}{4} + \text{Fuel}_{out}$.
  And $\text{Fuel}_{out}$ is calculated assuming the efficiency is determined by the *mix*.
  In many standard solutions to this specific Chinese textbook problem (e.g., from *Operations Research* by Wang or similar), the assumption is that the fuel consumption is **additive per bomb** relative to the distance, or the efficiency is a weighted average.
  
  However, there is a key constraint often implicit: **One bomber can carry a specific number of bombs.**
  If the max bombs per bomber is not given, we cannot determine the number of bombers/sorties from the bomb count.
  BUT, look at the fuel constraint again.
  If we don't know the payload limit, we can't constrain $x_{i,H}$ and $x_{i,L}$ to the number of sorties.
  
  *Alternative Interpretation*: The problem asks for the **distribution of bombs** to targets.
  The "Sortie" fuel cost is incurred per **bomber**.
  If we assume that **one bomber can carry all 48 heavy and 32 light bombs** (or enough to cover the mission), then the number of sorties is 1 per target? No, "Fleet of bombers".
  
  Let's assume the standard constraint: **Each bomb is assigned to a target.** The "Sortie" concept might be a red herring if the payload limit is huge, OR the payload limit is 1?
  If payload limit is 1 bomb per sortie:
  Number of sorties to target $i = x_{i,H} + x_{i,L}$.
  Fuel per heavy bomb sortie to $i$: $100 + D_i/2 + D_i/4$.
  Fuel per light bomb sortie to $i$: $100 + D_i/3 + D_i/4$.
  This makes the problem a simple allocation of bombs to targets subject to fuel and bomb count constraints.
  Let's check if this makes sense.
  Target 1 (450 km):
  Heavy sortie fuel: $100 + 450/2 + 450/4 = 100 + 225 + 112.5 = 437.5$ L.
  Light sortie fuel: $100 + 450/3 + 450/4 = 100 + 150 + 112.5 = 362.5$ L.
  
  If we use this model:
  Total Fuel Constraint:
  $\sum_{i} \left( x_{i,H} F_{H,i} + x_{i,L} F_{L,i} \right) \le 48,000$
  where $F_{H,i} = 100 + D_i(1/2 + 1/4) = 100 + 0.75 D_i$
  $F_{L,i} = 100 + D_i(1/3 + 1/4) = 100 + \frac{7}{12} D_i$
  
  Bomb Constraints:
  $\sum_{i} x_{i,H} \le 48$
  $\sum_{i} x_{i,L} \le 32$
  
  Objective: Maximize $P(\text{Destroy at least one}) = 1 - \prod_{i=1}^4 P(\text{Survive}_i)$.
  $P(\text{Survive}_i) = (1 - P_{i,H})^{x_{i,H}} (1 - P_{i,L})^{x_{i,L}}$.
  
  This is a well-posed Non-Linear Integer Programming problem.
  Is the "1 bomb per sortie" assumption valid?
  "When carrying a heavy bomb... 2 km". If I carry 2 heavy bombs, is it still 2 km/L?
  If the efficiency is per-bomb (i.e., the "2 km/L" is the efficiency contribution of that bomb), then the additive model above is correct.
  If the efficiency is per-aircraft (i.e., the aircraft flies at 2 km/L if it has *any* heavy bomb), then the fuel is $100 + D_i/2 + D_i/4$ per *sortie*, and we need a constraint linking bombs to sorties.
  Given "Fleet of bombers" and no payload limit, the "1 bomb per sortie" or "Fuel is additive per bomb" is the only way to solve without an undefined payload parameter $M$. In many such problems, the "efficiency" is indeed treated as a per-unit cost coefficient in the linear constraint.
  
  Let's proceed with the **Additive Fuel per Bomb** model, as it is the only one that yields a solvable model with the given data. It effectively treats the "fuel consumption" of the bomb's payload as independent and additive.

**Derived Fuel Costs per Bomb (Liters):**
For Target $i$:
- $C_{H,i} = 100 + D_i \left( \frac{1}{R_H} + \frac{1}{R_E} \right) = 100 + D_i \left( \frac{1}{2} + \frac{1}{4} \right) = 100 + 0.75 D_i$
- $C_{L,i} = 100 + D_i \left( \frac{1}{R_L} + \frac{1}{R_E} \right) = 100 + D_i \left( \frac{1}{3} + \frac{1}{4} \right) = 100 + \frac{7}{12} D_i$

Calculations:
- $i=1 (D=450)$:
  - $C_{H,1} = 100 + 0.75(450) = 100 + 337.5 = 437.5$
  - $C_{L,1} = 100 + \frac{7}{12}(450) = 100 + 262.5 = 362.5$
- $i=2 (D=480)$:
  - $C_{H,2} = 100 + 0.75(480) = 100 + 360 = 460$
  - $C_{L,2} = 100 + \frac{7}{12}(480) = 100 + 280 = 380$
- $i=3 (D=540)$:
  - $C_{H,3} = 100 + 0.75(540) = 100 + 405 = 505$
  - $C_{L,3} = 100 + \frac{7}{12}(540) = 100 + 315 = 415$
- $i=4 (D=600)$:
  - $C_{H,4} = 100 + 0.75(600) = 100 + 450 = 550$
  - $C_{L,4} = 100 + \frac{7}{12}(600) = 100 + 350 = 450$

## Decision Variables
- $x_{i,H} \in \mathbb{Z}_{\ge 0}$: Number of Heavy bombs assigned to target part $i$.
- $x_{i,L} \in \mathbb{Z}_{\ge 0}$: Number of Light bombs assigned to target part $i$.

## Objective Function
Maximize the probability that **at least one** of the four key parts is destroyed.
Let $P_{survive, i}$ be the probability that part $i$ is **NOT** destroyed.
Assuming independence of bomb impacts:
$P_{survive, i} = (1 - P_{i,H})^{x_{i,H}} \cdot (1 - P_{i,L})^{x_{i,L}}$

The probability that **all** parts survive is:
$P_{all\_survive} = \prod_{i=1}^{4} P_{survive, i} = \prod_{i=1}^{4} \left[ (1 - P_{i,H})^{x_{i,H}} (1 - P_{i,L})^{x_{i,L}} \right]$

The objective is to Maximize $Z = 1 - P_{all\_survive}$.
Equivalently, Minimize $P_{all\_survive}$.

$$ \text{Maximize } Z = 1 - \prod_{i=1}^{4} \left( (1 - P_{i,H})^{x_{i,H}} (1 - P_{i,L})^{x_{i,L}} \right) $$

## Operational Constraints

1. **Fuel Constraint**:
   Total fuel consumed by all bomb assignments must not exceed 48,000 liters.
   $$ \sum_{i=1}^{4} \left( C_{H,i} x_{i,H} + C_{L,i} x_{i,L} \right) \le 48,000 $$
   Where $C_{H,i}$ and $C_{L,i}$ are the calculated fuel costs per bomb:
   - $C_{H,1}=437.5, C_{L,1}=362.5$
   - $C_{H,2}=460, C_{L,2}=380$
   - $C_{H,3}=505, C_{L,3}=415$
   - $C_{H,4}=550, C_{L,4}=450$

2. **Heavy Bomb Availability**:
   $$ \sum_{i=1}^{4} x_{i,H} \le 48 $$

3. **Light Bomb Availability**:
   $$ \sum_{i=1}^{4} x_{i,L} \le 32 $$

4. **Non-negativity and Integrality**:
   $$ x_{i,H} \in \mathbb{Z}_{\ge 0}, \quad x_{i,L} \in \mathbb{Z}_{\ge 0} \quad \forall i \in \{1,2,3,4\} $$