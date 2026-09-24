# Nurse Scheduling Optimization Model

## 1. Index Sets & Parameters

**Index Sets:**
*   $S = \{1, 2, 3, 4, 5, 6\}$: The set of 4-hour time slots in a 24-hour day.
    *   $S_1$: 2:00 - 6:00
    *   $S_2$: 6:00 - 10:00
    *   $S_3$: 10:00 - 14:00
    *   $S_4$: 14:00 - 18:00
    *   $S_5$: 18:00 - 22:00
    *   $S_6$: 22:00 - 2:00 (next day)
*   $K = \{1, 2, 3, 4, 5, 6\}$: The set of 8-hour shift start times.
    *   $K_1$: Start 2:00 (Covers $S_1, S_2$)
    *   $K_2$: Start 6:00 (Covers $S_2, S_3$)
    *   $K_3$: Start 10:00 (Covers $S_3, S_4$)
    *   $K_4$: Start 14:00 (Covers $S_4, S_5$)
    *   $K_5$: Start 18:00 (Covers $S_5, S_6$)
    *   $K_6$: Start 22:00 (Covers $S_6, S_1$)

**Parameters:**
*   $R_s$: Minimum nurses required in slot $s \in S$.
    *   $R_1 = 10$
    *   $R_2 = 15$
    *   $R_3 = 25$
    *   $R_4 = 20$
    *   $R_5 = 18$
    *   $R_6 = 12$
*   $C_{ft}$: Hourly wage for full-time nurses = 10.
*   $C_{ct}$: Hourly wage for contract nurses = 15.
*   $H_{shift}$: Hours per shift = 8.
*   $Cost_{ft, shift} = C_{ft} \times H_{shift} = 80$.
*   $Cost_{ct, shift} = C_{ct} \times H_{shift} = 120$.

*Note on Coverage Mapping:*
A nurse starting at shift $k$ works for 8 hours, covering two consecutive 4-hour slots.
*   Shift 1 (2:00 start) covers slots 1 and 2.
*   Shift 2 (6:00 start) covers slots 2 and 3.
*   Shift 3 (10:00 start) covers slots 3 and 4.
*   Shift 4 (14:00 start) covers slots 4 and 5.
*   Shift 5 (18:00 start) covers slots 5 and 6.
*   Shift 6 (22:00 start) covers slots 6 and 1.

## 2. Decision Variables

Let:
*   $x_k$: Number of **full-time** nurses assigned to shift starting at $k \in K$.
*   $y_k$: Number of **contract** nurses assigned to shift starting at $k \in K$.

**Domains:**
*   $x_k \ge 0, \quad \forall k \in K$
*   $y_k \ge 0, \quad \forall k \in K$

*(Note: While nurse counts are physically integers, in standard aggregate LP formulations for staffing with large numbers, continuous variables are often used. However, given the relatively small scale (requirements < 30), integer constraints are appropriate. If strict integrality is required, add $x_k, y_k \in \mathbb{Z}^+$. For standard LP relaxation, $x_k, y_k \ge 0$. Given the prompt asks for a general OR model and "how many", we will specify non-negative continuous variables but note that integer values are expected in practice. Let's assume standard LP relaxation for solvability unless specified as MILP, but typically staffing is integer. Let's look at the "Integrity & Scale Check". The scale is small (<100). The prompt doesn't explicitly force integrality, but "how many" implies integers. However, standard linear programming textbooks often present this as an LP. I will define them as continuous $\ge 0$ to allow for a general LP solution, but note that in practice they are integers. If the problem implies an exact integer answer is needed, the solver should handle it. Let's stick to standard LP formulation first, as contract vs full-time is a mix. Actually, looking at similar problems, they are often solved as LPs. I will specify $x_k, y_k \ge 0$.)*

## 3. Objective Function

Minimize the total daily labor cost.

$$
\text{Minimize } Z = \sum_{k=1}^{6} (80 x_k + 120 y_k)
$$

Or expanded:
$$
Z = 80(x_1 + x_2 + x_3 + x_4 + x_5 + x_6) + 120(y_1 + y_2 + y_3 + y_4 + y_5 + y_6)
$$

## 4. Operational Constraints

The total number of nurses (full-time + contract) on duty in each 4-hour slot must meet or exceed the requirement $R_s$.

**Slot 1 (2:00 - 6:00):**
Covered by Shift 6 (ends 6:00) and Shift 1 (starts 2:00).
$$
x_6 + y_6 + x_1 + y_1 \ge 10
$$

**Slot 2 (6:00 - 10:00):**
Covered by Shift 1 (ends 10:00) and Shift 2 (starts 6:00).
$$
x_1 + y_1 + x_2 + y_2 \ge 15
$$

**Slot 3 (10:00 - 14:00):**
Covered by Shift 2 (ends 14:00) and Shift 3 (starts 10:00).
$$
x_2 + y_2 + x_3 + y_3 \ge 25
$$

**Slot 4 (14:00 - 18:00):**
Covered by Shift 3 (ends 18:00) and Shift 4 (starts 14:00).
$$
x_3 + y_3 + x_4 + y_4 \ge 20
$$

**Slot 5 (18:00 - 22:00):**
Covered by Shift 4 (ends 22:00) and Shift 5 (starts 18:00).
$$
x_4 + y_4 + x_5 + y_5 \ge 18
$$

**Slot 6 (22:00 - 2:00):**
Covered by Shift 5 (ends 2:00) and Shift 6 (starts 22:00).
$$
x_5 + y_5 + x_6 + y_6 \ge 12
$$

**Non-negativity:**
$$
x_k \ge 0, \quad y_k \ge 0, \quad \forall k \in \{1, \dots, 6\}
$$

### Model Verification & Analysis

1.  **Unit Consistency**: All variables are counts of nurses. Costs are in Yuan. Time is consistent.
2.  **Objective Direction**: Minimization of cost.
3.  **Bounds**: Non-negativity included.
4.  **Integrity Check**: The problem asks "Should the hospital hire contract nurses?".
    *   Full-time cost per 8h shift: 80.
    *   Contract cost per 8h shift: 120.
    *   Since full-time nurses are cheaper ($80 < 120$), the optimal solution to minimize cost will prioritize full-time nurses.
    *   The model allows $y_k > 0$ only if it helps satisfy constraints more "efficiently" in a way that full-time alone cannot, or if there are upper bounds on full-time nurses (which are not present here).
    *   Since there are no upper bounds on $x_k$, the optimal solution will set $y_k = 0$ for all $k$, because replacing any $y_k$ with $x_k$ reduces cost while maintaining the same coverage.
    *   **Conclusion from Model Structure**: The hospital should **not** hire contract nurses, as they are strictly more expensive and fulfill the same functional role (coverage) as full-time nurses. The optimal strategy is to hire only full-time nurses.

    *Self-Correction/Refinement*: Is there any constraint missing? "Nurses work in 6 shifts... each nurse works 8 consecutive hours." The model correctly maps shifts to slots. The cost difference is the only differentiator. Unless there is a limit on the number of full-time nurses the hospital *can* hire (not stated), $y_k$ will be zero.

    Let's double check if I missed any constraint. "The hospital can hire both...". No cap on FT. Therefore, the LP will drive all $y_k$ to 0.

    **Final Answer Formulation**:
    The mathematical model is defined as above. The solution to the model will yield $y_k = 0$ for all $k$. The number of contract nurses hired is 0.