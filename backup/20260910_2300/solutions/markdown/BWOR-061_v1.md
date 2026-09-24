### Index Sets & Parameters

**Sets:**
- $I = \{1, 2, 3\}$: Set of candidate positions in the interview sequence.
- $S = \{1, 2, 3\}$: Set of possible interview scores (1: Unsatisfactory, 2: Somewhat Satisfactory, 3: Satisfactory).
- $H = \{1, 2\}$: Set of positions where a "continue" decision is possible (i.e., not the last candidate).

**Parameters:**
- $p_s$: Probability of receiving score $s$.
  - $p_1 = 0.30$ (Unsatisfactory)
  - $p_2 = 0.50$ (Somewhat Satisfactory)
  - $p_3 = 0.20$ (Satisfactory)
- $v_s$: Value (Score) associated with hiring a candidate with interview score $s$.
  - $v_1 = 1, v_2 = 2, v_3 = 3$.
- $E_i^{\text{cont}}$: Expected score of the *subsequent* hiring process starting from candidate $i+1$. (This is a recursive parameter derived from the model structure, often solved via backward induction in decision problems, but here we define it to structure the LP/MDP formulation).

*Note on Problem Type:* This is a sequential decision problem (Markov Decision Process / Dynamic Programming) under uncertainty. It can be formulated as a linear programming problem if we expand the state space or use value functions. However, standard LP formulations for such problems usually involve defining the expected value of a policy. Given the small size, we can define decision variables representing the probability of choosing "Hire" vs "Continue" at each state.

Let's define the state by the current candidate index $i$ and the observed score $s$.
States: $(i, s)$ where $i \in \{1, 2\}$ are decision points.
- At $i=1$:
  - If $s=3$: Must/Should Hire (Optimal is always to hire 3).
  - If $s=2$: Decision: Hire (stop) or Continue.
  - If $s=1$: Must Continue (cannot hire if goal is max score? No, you *can* hire, but it's suboptimal. The problem says "If not satisfied... candidate is rejected". It implies you *must* reject 1s? "If not satisfied (scored 1 point), the candidate is rejected". This is a hard rule: You **cannot** hire a candidate with score 1. You must continue.
- At $i=2$:
  - If $s=3$: Hire.
  - If $s=2$: Decision: Hire or Continue.
  - If $s=1$: Reject/Continue to 3.
- At $i=3$:
  - Must hire regardless of score.

**Refined Parameters:**
- $C_{i,s}$: Binary indicator if we are at decision point $(i,s)$.
- Let $x_{i,s}$ be the binary decision variable: $1$ if we **Hire** candidate $i$ given score $s$, $0$ if we **Continue/Reject**.
  - Domain restrictions based on rules:
    - If $s=1$, $x_{i,1}$ is forced to 0 (must reject/continue) for $i=1,2$.
    - If $s=3$, $x_{i,3}$ is effectively forced to 1 in an optimal strategy (hiring 3 is always better than continuing to expect $\le 3$), but we can let the optimizer decide.
    - For $s=2$, $x_{i,2} \in \{0, 1\}$.

To formulate this as a standard Optimization Model (specifically a Linear Program or Mixed Integer Program), we need to define the objective as the expected value of the final hired candidate's score.

Let $V_{i,s}$ be the expected score from candidate $i$ onwards, given that candidate $i$ received score $s$ and we are at the decision point.
Actually, it is cleaner to define the decision variables directly in the objective function expansion.

Let:
- $y_{i,s}$: Probability that we hire candidate $i$ given score $s$. Since the policy is deterministic (or we can model the expected outcome of a specific deterministic policy), we use binary variables $z_{i,s} \in \{0,1\}$ indicating the action "Hire".
  - $z_{i,s} = 1$ if Hire candidate $i$ upon score $s$.
  - $z_{i,s} = 0$ if Reject/Continue candidate $i$ upon score $s$.

**Constraints on Actions:**
1. If $s=1$, we *must* reject. So $z_{i,1} = 0$ for $i=1,2$.
2. If $i=3$, we *must* hire. So $z_{3,s} = 1$ for all $s$.
3. For $i=1,2$ and $s \in \{2,3\}$, $z_{i,s} \in \{0,1\}$.

**Expected Value Calculation:**
The total expected score $E$ is the sum over all possible paths.
Path definition: A path is defined by the sequence of scores and decisions.
Since we stop as soon as we hire, the "hired" candidate is the first one for whom $z_{i,s}=1$ (or $i=3$).

Let's expand the expected value $E$ based on the first candidate's outcome:
$E = p_1 \cdot E[\text{Next} | \text{Score}_1=1] + p_2 \cdot E[\text{Outcome} | \text{Score}_1=2] + p_3 \cdot E[\text{Outcome} | \text{Score}_1=3]$

1. **Case $s_1 = 1$ (Prob 0.3):**
   Rule: Must reject. Proceed to candidate 2.
   Value = $E_2$ (Expected score starting from candidate 2).

2. **Case $s_1 = 2$ (Prob 0.5):**
   Decision $z_{1,2}$.
   - If $z_{1,2}=1$ (Hire): Score = 2.
   - If $z_{1,2}=0$ (Continue): Proceed to candidate 2. Value = $E_2$.
   Expected Value = $z_{1,2} \cdot 2 + (1 - z_{1,2}) \cdot E_2$.

3. **Case $s_1 = 3$ (Prob 0.2):**
   Decision $z_{1,3}$.
   - If $z_{1,3}=1$ (Hire): Score = 3.
   - If $z_{1,3}=0$ (Continue): Proceed to candidate 2. Value = $E_2$.
   Expected Value = $z_{1,3} \cdot 3 + (1 - z_{1,3}) \cdot E_2$.

So, $E = 0.3 E_2 + 0.5 [z_{1,2} \cdot 2 + (1 - z_{1,2}) E_2] + 0.2 [z_{1,3} \cdot 3 + (1 - z_{1,3}) E_2]$.

Now we need $E_2$ (Expected score starting from candidate 2).
$E_2 = p_1 E[\text{Next} | s_2=1] + p_2 E[\text{Outcome} | s_2=2] + p_3 E[\text{Outcome} | s_2=3]$.

1. **Case $s_2 = 1$ (Prob 0.3):**
   Rule: Must reject. Proceed to candidate 3.
   Value = $E_3$ (Expected score from candidate 3).

2. **Case $s_2 = 2$ (Prob 0.5):**
   Decision $z_{2,2}$.
   - If $z_{2,2}=1$ (Hire): Score = 2.
   - If $z_{2,2}=0$ (Continue): Proceed to candidate 3. Value = $E_3$.
   Expected Value = $z_{2,2} \cdot 2 + (1 - z_{2,2}) E_3$.

3. **Case $s_2 = 3$ (Prob 0.2):**
   Decision $z_{2,3}$.
   - If $z_{2,3}=1$ (Hire): Score = 3.
   - If $z_{2,3}=0$ (Continue): Proceed to candidate 3. Value = $E_3$.
   Expected Value = $z_{2,3} \cdot 3 + (1 - z_{2,3}) E_3$.

So, $E_2 = 0.3 E_3 + 0.5 [z_{2,2} \cdot 2 + (1 - z_{2,2}) E_3] + 0.2 [z_{2,3} \cdot 3 + (1 - z_{2,3}) E_3]$.

Now we need $E_3$ (Expected score from candidate 3).
Rule: Must hire candidate 3 regardless of score.
$E_3 = p_1(1) + p_2(2) + p_3(3) = 0.3(1) + 0.5(2) + 0.2(3) = 0.3 + 1.0 + 0.6 = 1.9$.
So, $E_3 = 1.9$.

Substitute $E_3$ into $E_2$:
$E_2 = 0.3(1.9) + 0.5 [2 z_{2,2} + (1 - z_{2,2}) 1.9] + 0.2 [3 z_{2,3} + (1 - z_{2,3}) 1.9]$
$E_2 = 0.57 + 0.5 [2 z_{2,2} + 1.9 - 1.9 z_{2,2}] + 0.2 [3 z_{2,3} + 1.9 - 1.9 z_{2,3}]$
$E_2 = 0.57 + 0.5 [1.9 + 0.1 z_{2,2}] + 0.2 [1.9 + 1.1 z_{2,3}]$
$E_2 = 0.57 + 0.95 + 0.05 z_{2,2} + 0.38 + 0.22 z_{2,3}$
$E_2 = 1.9 + 0.05 z_{2,2} + 0.22 z_{2,3}$

Now substitute $E_2$ into $E$:
$E = 0.3 E_2 + 0.5 [2 z_{1,2} + (1 - z_{1,2}) E_2] + 0.2 [3 z_{1,3} + (1 - z_{1,3}) E_2]$
Note that $0.5 [2 z_{1,2} + (1 - z_{1,2}) E_2] = 0.5 [2 z_{1,2} + E_2 - z_{1,2} E_2] = 0.5 E_2 + z_{1,2}(1 - 0.5 E_2)$.
Similarly for the other term.
Actually, it is simpler to just expand fully into a linear function of the binary variables $z_{i,s}$.

Let's expand $E$ fully:
Term 1 (from $s_1=1$): $0.3 E_2$
Term 2 (from $s_1=2$): $0.5 (2 z_{1,2} + (1 - z_{1,2}) E_2) = 0.5 (2 z_{1,2} + E_2 - z_{1,2} E_2) = 0.5 E_2 + z_{1,2} (1 - 0.5 E_2)$
Term 3 (from $s_1=3$): $0.2 (3 z_{1,3} + (1 - z_{1,3}) E_2) = 0.2 (3 z_{1,3} + E_2 - z_{1,3} E_2) = 0.2 E_2 + z_{1,3} (0.6 - 0.2 E_2)$

Total $E = (0.3 + 0.5 + 0.2) E_2 + z_{1,2} (1 - 0.5 E_2) + z_{1,3} (0.6 - 0.2 E_2)$
$E = 1.0 E_2 + z_{1,2} (1 - 0.5 E_2) + z_{1,3} (0.6 - 0.2 E_2)$

Substitute $E_2 = 1.9 + 0.05 z_{2,2} + 0.22 z_{2,3}$:
$E = 1.9 + 0.05 z_{2,2} + 0.22 z_{2,3} + z_{1,2} (1 - 0.5(1.9 + 0.05 z_{2,2} + 0.22 z_{2,3})) + z_{1,3} (0.6 - 0.2(1.9 + 0.05 z_{2,2} + 0.22 z_{2,3}))$

This expression contains products of binary variables (e.g., $z_{1,2} z_{2,2}$). This makes it a **Quadratic** or higher-order problem if expanded naively.
However, in standard OR modeling for such sequential decisions, we usually define the value function variables $V_i$ as continuous variables and link them to decisions. But since the policy is deterministic, the "expected value" is a linear combination of the terminal outcomes weighted by probabilities.
Wait, the product $z_{1,2} z_{2,2}$ appears because the decision at step 1 affects the probability of reaching step 2, and the decision at step 2 affects the outcome.
Actually, looking at the expansion:
$E = \sum_{\text{paths}} P(\text{path}) \cdot \text{Score}(\text{path})$.
The probability of a path depends on the decisions.
Example Path: $s_1=2, \text{Hire}$. Prob = $0.5$. Score = 2.
Example Path: $s_1=2, \text{Continue}, s_2=3, \text{Hire}$. Prob = $0.5 \times 1 \times 0.2 \times 1$ (if we decide to hire on 3 at step 2). Score = 3.
The decision $z_{1,2}$ determines if we take the path "Hire at 1" or "Continue to 2".
If we continue to 2, the subsequent decisions $z_{2,s}$ apply.

To linearize this, we can define auxiliary variables for the expected value of each state, but the "Hire/Continue" choices are binary.
Standard approach: This is a **Mixed Integer Linear Program (MILP)** if we define the expected values carefully or simply maximize the expanded linear form if we treat the "strategy" as the variables.
Actually, the term $z_{1,2} z_{2,2}$ is non-linear.
Is it?
$E_2$ depends on $z_{2,2}$.
The coefficient of $z_{1,2}$ is $(1 - 0.5 E_2)$.
So the term is $z_{1,2} (1 - 0.5 (1.9 + \dots z_{2,2} \dots))$.
Yes, it is non-linear.

However, we can reformulate the problem using **State-Action** variables in a standard way for MDPs, or simply recognize that for this specific small problem, we can list all possible deterministic strategies (policies) and calculate their expected values.
Number of decisions:
- $z_{1,2} \in \{0,1\}$
- $z_{1,3} \in \{0,1\}$ (Though logically 3 is always hire, let's keep it general)
- $z_{2,2} \in \{0,1\}$
- $z_{2,3} \in \{0,1\}$
Total $2^4 = 16$ strategies.
We can model this as an **Integer Program** where we select one strategy, or more elegantly, we can just define the variables and the objective as the expected value, acknowledging the non-linearity or linearizing it.

But wait, looking at the structure:
$E = \sum_{i=1}^3 \sum_{s} P(\text{Reach } i, s) \cdot z_{i,s} \cdot s + \text{Term for forced hire at 3 if not reached earlier?}$
No, it's simpler:
$E = \sum_{\text{all possible outcomes}} \text{Prob}(\text{outcome}) \times \text{Score}(\text{outcome})$.
The probability of hiring candidate $i$ with score $s$ is:
$P(\text{Hire } i, s) = P(s_i=s) \times P(\text{Accept all previous} | \text{scores}) $.
$P(\text{Hire } 1, s) = p_s \cdot z_{1,s}$.
$P(\text{Hire } 2, s) = p_s \cdot (1 - \sum_{s' \in \{2,3\}} z_{1,s'} p_{s'} \text{?? No.})$
Probability of reaching candidate 2 is:
$P(\text{Reach 2}) = 1 - P(\text{Hire 1}) = 1 - \sum_{s'} p_{s'} z_{1,s'}$.
Note: $z_{1,1}=0$. So $\sum p_{s'} z_{1,s'} = p_2 z_{1,2} + p_3 z_{1,3}$.
So $P(\text{Reach 2}) = 1 - 0.5 z_{1,2} - 0.2 z_{1,3}$.
Given we reach candidate 2, the probability we hire candidate 2 with score $s$ is:
$P(\text{Hire 2, } s | \text{Reach 2}) = p_s z_{2,s}$.
So $P(\text{Hire 2, } s) = P(\text{Reach 2}) \cdot p_s z_{2,s}$.
This creates a product of $(z_{1,2}, z_{1,3})$ and $(z_{2,s})$.

To avoid non-linear terms in a standard LP/MILP output, we often define **continuation variables** or use the fact that the problem is small enough to be solved by enumerating the 16 cases in the "Objective" description, or we can define the model as a **Quadratic Integer Program**. However, the prompt asks for an OR model. Usually, these are presented as MILPs. We can linearize the products $z_{1,s} z_{2,t}$ by introducing new variables $w_{1,s,2,t} = z_{1,s} z_{2,t}$ and adding linear constraints, but this is cumbersome.

Alternative: **Dynamic Programming Formulation as a System of Equations with Decision Variables**.
Let $V_i$ be the expected score from stage $i$.
$V_3 = 1.9$.
$V_2 = 0.3 V_3 + 0.5 (2 z_{2,2} + (1-z_{2,2}) V_3) + 0.2 (3 z_{2,3} + (1-z_{2,3}) V_3)$.
$V_1 = 0.3 V_2 + 0.5 (2 z_{1,2} + (1-z_{1,2}) V_2) + 0.2 (3 z_{1,3} + (1-z_{1,3}) V_2)$.
Objective: Maximize $V_1$.
Variables: $z_{1,2}, z_{1,3}, z_{2,2}, z_{2,3} \in \{0,1\}$.
$V_2, V_1$ are continuous variables.
This is a **Mixed Integer Non-Linear Program (MINLP)** because $V_1$ contains terms like $z_{1,2} V_2$, and $V_2$ contains $z_{2,2}$.
However, since $V_2$ is linear in $z_{2,\cdot}$ and $V_1$ is linear in $z_{1,\cdot}$ and $V_2$, we can substitute $V_2$ into $V_1$.
$V_1(z_{1,2}, z_{1,3}, z_{2,2}, z_{2,3})$ becomes a polynomial of degree 2.

Given the constraints of the prompt ("Construct a formal mathematical optimization model"), and the fact that this is a classic "Secretary Problem" variant, the most robust formal model is an **Integer Program** where we define the expected value explicitly. I will present the model using the Value Function approach, as it is the standard OR formulation for sequential decisions, noting the bilinear terms or simply presenting the expanded objective if linearity is strictly required (which would require the $w$ variables).

Let's stick to the cleanest **MILP** representation by defining the decision variables for the *policy* and calculating the objective. Since the non-linearity is inherent in the probability multiplication, I will formulate it as a **Quadratic Integer Program (QIP)** or simply an **Integer Program** with the expanded objective, as "LP/MILP" in prompts often loosely refers to the general class of discrete optimization models. I will explicitly define the variables and the objective function that results from the backward induction.

Actually, there is a simpler linear formulation if we define variables $x_{i,s}$ as the **probability of hiring** candidate $i$ given score $s$ in the optimal policy? No, the policy is deterministic.

Let's provide the **Backward Induction / Dynamic Programming** structure as the model, which is the correct OR framework.

**Decision Variables:**
$z_{1,2} \in \{0,1\}$: Hire candidate 1 if score is 2.
$z_{1,3} \in \{0,1\}$: Hire candidate 1 if score is 3.
$z_{2,2} \in \{0,1\}$: Hire candidate 2 if score is 2.
$z_{2,3} \in \{0,1\}$: Hire candidate 2 if score is 3.
*(Note: $z_{1,1}=0, z_{2,1}=0$ fixed by rules. $z_{3,s}=1$ fixed by rules.)*

**Auxiliary Variables (Expected Values):**
$V_3$: Expected score from candidate 3.
$V_2$: Expected score from candidate 2.
$V_1$: Expected score from candidate 1 (Objective).

**Model:**
Maximize $V_1$

Subject to:
1. $V_3 = 1.9$
2. $V_2 = 0.3 V_3 + 0.5 (2 z_{2,2} + (1 - z_{2,2}) V_3) + 0.2 (3 z_{2,3} + (1 - z_{2,3}) V_3)$
3. $V_1 = 0.3 V_2 + 0.5 (2 z_{1,2} + (1 - z_{1,2}) V_2) + 0.2 (3 z_{1,3} + (1 - z_{1,3}) V_2)$

This is a valid formal model. To make it a standard "optimization model" block, I will expand it slightly to show the dependencies clearly.

### Decision Variables (with explicit domains)

- $z_{1,2} \in \{0, 1\}$: Binary variable indicating whether to **Hire** the 1st candidate if the interview score is 2.
- $z_{1,3} \in \{0, 1\}$: Binary variable indicating whether to **Hire** the 1st candidate if the interview score is 3.
- $z_{2,2} \in \{0, 1\}$: Binary variable indicating whether to **Hire** the 2nd candidate if the interview score is 2.
- $z_{2,3} \in \{0, 1\}$: Binary variable indicating whether to **Hire** the 2nd candidate if the interview score is 3.

*(Implicitly, if score is 1, the decision is forced to "Reject/Continue", so no variable is needed. If it is the 3rd candidate, the decision is forced to "Hire".)*

- $V_3 \in \mathbb{R}$: Expected score obtained from the 3rd candidate onwards.
- $V_2 \in \mathbb{R}$: Expected score obtained from the 2nd candidate onwards.
- $V_1 \in \mathbb{R}$: Expected score obtained from the 1st candidate onwards (Total Expected Score).

### Objective Function

$$ \text{Maximize } V_1 $$

### Operational Constraints

1. **Base Case (3rd Candidate):**
   The 3rd candidate is always hired. The expected score is the weighted average of possible scores.
   $$ V_3 = 1(0.3) + 2(0.5) + 3(0.2) $$
   $$ V_3 = 1.9 $$

2. **Stage 2 Recursion (2nd Candidate):**
   $V_2$ is the expected value of the process starting at candidate 2.
   - If score is 1 (prob 0.3): Must reject, proceed to 3. Value = $V_3$.
   - If score is 2 (prob 0.5):
     - If $z_{2,2}=1$ (Hire): Value = 2.
     - If $z_{2,2}=0$ (Continue): Value = $V_3$.
     - Expected = $2 z_{2,2} + V_3 (1 - z_{2,2})$.
   - If score is 3 (prob 0.2):
     - If $z_{2,3}=1$ (Hire): Value = 3.
     - If $z_{2,3}=0$ (Continue): Value = $V_3$.
     - Expected = $3 z_{2,3} + V_3 (1 - z_{2,3})$.

   $$ V_2 = 0.3 V_3 + 0.5 [2 z_{2,2} + V_3 (1 - z_{2,2})] + 0.2 [3 z_{2,3} + V_3 (1 - z_{2,3})] $$

3. **Stage 1 Recursion (1st Candidate):**
   $V_1$ is the expected value of the process starting at candidate 1.
   - If score is 1 (prob 0.3): Must reject, proceed to 2. Value = $V_2$.
   - If score is 2 (prob 0.5):
     - If $z_{1,2}=1$ (Hire): Value = 2.
     - If $z_{1,2}=0$ (Continue): Value = $V_2$.
     - Expected = $2 z_{1,2} + V_2 (1 - z_{1,2})$.
   - If score is 3 (prob 0.2):
     - If $z_{1,3}=1$ (Hire): Value = 3.
     - If $z_{1,3}=0$ (Continue): Value = $V_2$.
     - Expected = $3 z_{1,3} + V_2 (1 - z_{1,3})$.

   $$ V_1 = 0.3 V_2 + 0.5 [2 z_{1,2} + V_2 (1 - z_{1,2})] + 0.2 [3 z_{1,3} + V_2 (1 - z_{1,3})] $$

4. **Bounds:**
   $$ z_{1,2}, z_{1,3}, z_{2,2}, z_{2,3} \in \{0, 1\} $$
   $$ V_1, V_2, V_3 \ge 0 $$