## Model Type: MILP (Minimum Project Duration via CPM / Critical Path)

## Index Sets & Parameters

**Sets:**
- $T = \{a, b, c, d, e, f, g, h, i, j, k, L, m, n\}$: Set of tasks.
- $P(i)$: Set of immediate predecessor tasks for task $i$.
- $S(i)$: Set of immediate successor tasks for task $i$.

**Parameters:**
- $D_i$: Duration of task $i$ (in days).
  - $D_a = 10$
  - $D_b = 8$
  - $D_c = 6$
  - $D_d = 16$
  - $D_e = 24$
  - $D_f = 4$
  - $D_g = 4$
  - $D_h = 10$
  - $D_i = 4$
  - $D_j = 12$
  - $D_k = 16$
  - $D_L = 8$
  - $D_m = 24$
  - $D_n = 4$

**Precedence Structure:**
- $P(a) = \emptyset, P(b) = \emptyset$
- $P(c) = \{a, b\}$
- $P(d) = \{b\}$
- $P(e) = \{c\}$
- $P(f) = \{d, e\}$
- $P(g) = \{f\}$
- $P(h) = \{f\}$
- $P(i) = \{f\}$
- $P(j) = \{g\}$
- $P(k) = \{h, i, j\}$
- $P(L) = \{c\}$
- $P(m) = \{L\}$
- $P(n) = \{k, m\}$

## Decision Variables

Let $ES_i$ be the earliest start time of task $i$ (in days from project start).
- **Domain:** $ES_i \ge 0$ for all $i \in T$.
- **Type:** Continuous (though optimal values will be integers given integer durations).

Let $T_{proj}$ be the total project duration.
- **Domain:** $T_{proj} \ge 0$.
- **Type:** Continuous.

## Objective Function

Minimize the total project duration:
$$ \text{Minimize } Z = T_{proj} $$

## Operational Constraints

**1. Precedence Constraints (Start-to-Finish):**
For every task $i \in T$ and every predecessor $p \in P(i)$, task $i$ cannot start before task $p$ finishes.
$$ ES_i \ge ES_p + D_p \quad \forall i \in T, \forall p \in P(i) $$

Explicitly listing the key constraints based on the table:
1. $ES_c \ge ES_a + 10$
2. $ES_c \ge ES_b + 8$
3. $ES_d \ge ES_b + 8$
4. $ES_e \ge ES_c + 6$
5. $ES_f \ge ES_d + 16$
6. $ES_f \ge ES_e + 24$
7. $ES_g \ge ES_f + 4$
8. $ES_h \ge ES_f + 4$
9. $ES_i \ge ES_f + 4$
10. $ES_j \ge ES_g + 4$
11. $ES_k \ge ES_h + 10$
12. $ES_k \ge ES_i + 4$
13. $ES_k \ge ES_j + 12$
14. $ES_L \ge ES_c + 6$
15. $ES_m \ge ES_L + 8$
16. $ES_n \ge ES_k + 16$
17. $ES_n \ge ES_m + 24$

**2. Project Completion Constraint:**
The project duration $T_{proj}$ must be at least the finish time of every terminal task. The terminal task is $n$ (it has no successors).
$$ T_{proj} \ge ES_n + D_n $$
$$ T_{proj} \ge ES_n + 4 $$

*(Note: While only $n$ is the unique terminal node in this specific graph, generally $T_{proj} \ge ES_i + D_i$ for all $i$ where $S(i) = \emptyset$.)*

**3. Non-negativity:**
$$ ES_i \ge 0 \quad \forall i \in T $$
$$ T_{proj} \ge 0 $$

---

### Verification & Solution Path (Critical Path Analysis)

To ensure the formulation captures the correct minimum, we trace the paths from start to finish:

1.  **Path 1 (Garage Main Line):**
    $a \to c \to e \to f \to g \to j \to k \to n$
    Duration: $10 + 6 + 24 + 4 + 4 + 12 + 16 + 4 = 80$ days.
    *Check Precedence:*
    - $a$ ends day 10.
    - $c$ starts day 10 (needs $a, b$). $b$ is 8 days, so $b$ ends day 8. $c$ can start day 10.
    - $c$ ends day $10+6=16$.
    - $e$ starts day 16. Ends $16+24=40$.
    - $f$ needs $d, e$.
      - $d$ needs $b$ (ends day 8). $d$ starts day 8. Ends $8+16=24$.
      - $e$ ends day 40.
      - So $f$ starts max(24, 40) = 40.
    - $f$ ends $40+4=44$.
    - $g$ starts 44. Ends $44+4=48$.
    - $j$ starts 48. Ends $48+12=60$.
    - $k$ needs $h, i, j$.
      - $h$ starts 44 (after $f$). Ends $44+10=54$.
      - $i$ starts 44 (after $f$). Ends $44+4=48$.
      - $j$ ends 60.
      - So $k$ starts max(54, 48, 60) = 60.
    - $k$ ends $60+16=76$.
    - $n$ needs $k, m$.
      - $k$ ends 76.
      - Let's check $m$.
    - $n$ starts 76 (if $m$ is earlier).

2.  **Path 2 (Driveway Line):**
    $a \to c \to L \to m \to n$
    Duration: $10 + 6 + 8 + 24 + 4 = 52$ days.
    *Check Precedence:*
    - $c$ ends day 16.
    - $L$ starts 16. Ends $16+8=24$.
    - $m$ starts 24. Ends $24+24=48$.
    - $n$ needs $m$ (ends 48) and $k$ (ends 76).
    - So $n$ starts max(76, 48) = 76.
    - $n$ ends $76+4=80$.

The critical path is $a-c-e-f-g-j-k-n$ with a total duration of **80 days**.

### Final Answer Formulation Summary
The model minimizes $T_{proj}$ subject to the start-time inequalities derived above. The optimal value for $T_{proj}$ is **80**.