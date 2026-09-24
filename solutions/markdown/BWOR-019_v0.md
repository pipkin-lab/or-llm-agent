**Model Type:** MILP (Mixed-Integer Linear Programming)

### Index Sets & Parameters

**Index Sets:**
*   $I = \{1, 2, 3, 4, 5, 6, 7, 8\}$: The set of available players.

**Parameters:**
*   $H_i$: Height of player $i$ in meters.
    *   $H_1 = 1.92$
    *   $H_2 = 1.90$
    *   $H_3 = 1.88$
    *   $H_4 = 1.86$
    *   $H_5 = 1.85$
    *   $H_6 = 1.83$
    *   $H_7 = 1.80$
    *   $H_8 = 1.78$
*   $Role_i$: Preferred position of player $i$.
    *   $C = \{1, 2\}$: Set of Centers.
    *   $F = \{3, 4, 5\}$: Set of Forwards.
    *   $G = \{6, 7, 8\}$: Set of Guards.
*   $N_{players} = 5$: Number of players to select.

**Decision Variables:**
*   $x_i \in \{0, 1\}$ for all $i \in I$:
    *   $x_i = 1$ if player $i$ is selected for the starting lineup.
    *   $x_i = 0$ otherwise.

### Objective Function

Maximize the total height of the selected lineup:

$$ \text{Maximize } Z = \sum_{i \in I} H_i x_i $$

$$ Z = 1.92x_1 + 1.90x_2 + 1.88x_3 + 1.86x_4 + 1.85x_5 + 1.83x_6 + 1.80x_7 + 1.78x_8 $$

### Operational Constraints

1.  **Lineup Size Constraint:**
    Exactly 5 players must be selected.
    $$ \sum_{i \in I} x_i = 5 $$

2.  **Center Constraint:**
    Exactly one center must be selected (Players 1 and 2 are centers).
    $$ x_1 + x_2 = 1 $$

3.  **Forward Constraint:**
    At least one forward must be selected (Players 3, 4, and 5 are forwards).
    $$ x_3 + x_4 + x_5 \ge 1 $$

4.  **Logical Constraint for Players 1, 4, and 6:**
    *   "If Player 1 or Player 4 is selected, then Player 6 must also be selected":
        $$ x_1 \le x_6 $$
        $$ x_4 \le x_6 $$
    *   "If Player 6 is selected, then neither Player 1 nor Player 4 can be selected":
        $$ x_1 + x_6 \le 1 $$
        $$ x_4 + x_6 \le 1 $$
    
    *Note: These four inequalities collectively enforce that exactly one of the set $\{1, 4, 6\}$ can be selected if we consider the interaction, but strictly speaking, they imply:
    - If $x_1=1 \implies x_6=1$. But $x_1+x_6 \le 1 \implies x_1=0$. So $x_1$ must be 0.
    - If $x_4=1 \implies x_6=1$. But $x_4+x_6 \le 1 \implies x_4=0$. So $x_4$ must be 0.
    - If $x_6=1 \implies x_1=0$ and $x_4=0$.
    - Actually, let's re-read carefully. "If Player 1 or Player 4 is selected, then Player 6 must also be selected" AND "if Player 6 is selected, then neither Player 1 nor Player 4 can be selected".
    - Let $A = (x_1=1 \lor x_4=1)$. Let $B = (x_6=1)$.
    - Condition 1: $A \implies B$.
    - Condition 2: $B \implies (\neg x_1 \land \neg x_4)$.
    - Combining: If $x_1=1$, then $x_6=1$, which implies $x_1=0$ (contradiction). Thus $x_1$ MUST be 0.
    - Similarly, if $x_4=1$, then $x_6=1$, which implies $x_4=0$ (contradiction). Thus $x_4$ MUST be 0.
    - So, $x_1 = 0$ and $x_4 = 0$ are forced.
    - The constraint $x_6$ can be 0 or 1 independently of 1 and 4 (since 1 and 4 are 0, the "if" parts are false, so the implications hold trivially, except we must ensure consistency).
    - Let's just write the logical implications as linear constraints to be safe and let the solver handle the logic, although the deduction above is strong.
    - $x_1 \le x_6$
    - $x_4 \le x_6$
    - $x_1 + x_6 \le 1$
    - $x_4 + x_6 \le 1$
    
    *Self-Correction/Refinement:* The prompt asks to formulate the model. I will list the linear inequalities derived from the logic.

5.  **Mutual Exclusion Constraint for Players 2 and 8:**
    Both Player 2 and Player 8 cannot be selected together.
    $$ x_2 + x_8 \le 1 $$

6.  **Non-negativity and Integrality:**
    $$ x_i \in \{0, 1\} \quad \forall i \in I $$