Based on the problem description, this is a **Multi-knapsack / Resource Allocation** problem with **discrete choices**. Since the investment amounts are in thousand yuan units and the total capital is 4 thousand yuan, the variables represent discrete units of investment. We must use **binary variables** to represent the specific allocation choice for each project.

Here is the formal mathematical model:

### 1. Index Sets & Parameters

**Index Sets:**
*   $P = \{A, B, C\}$: Set of projects.
*   $K = \{0, 1, 2, 3, 4\}$: Set of possible investment levels (in thousand yuan).

**Parameters:**
*   $M = 4$: Total available capital (thousand yuan).
*   $V_{p, k}$: Benefit (thousand yuan) obtained from investing $k$ thousand yuan in project $p$.
    *   **Project A:** $V_{A,0}=0, V_{A,1}=41, V_{A,2}=48, V_{A,3}=60, V_{A,4}=66$
    *   **Project B:** $V_{B,0}=0, V_{B,1}=42, V_{B,2}=50, V_{B,3}=60, V_{B,4}=66$
    *   **Project C:** $V_{C,0}=0, V_{C,1}=64, V_{C,2}=68, V_{C,3}=78, V_{C,4}=76$

### 2. Decision Variables

Let $x_{p, k}$ be a binary decision variable:
$$
x_{p, k} = 
\begin{cases} 
1 & \text{if project } p \text{ is invested with } k \text{ thousand yuan} \\
0 & \text{otherwise}
\end{cases}
$$
for all $p \in P$ and $k \in K$.

*Domain:* $x_{p, k} \in \{0, 1\}$

### 3. Objective Function

Maximize the total benefit:
$$
\text{Maximize } Z = \sum_{p \in P} \sum_{k \in K} V_{p, k} \cdot x_{p, k}
$$

### 4. Operational Constraints

**Constraint 1: Single Allocation per Project**
Each project must be assigned exactly one investment level from the set $K$.
$$
\sum_{k \in K} x_{p, k} = 1 \quad \forall p \in P
$$

**Constraint 2: Capital Limitation**
The total investment across all projects cannot exceed the available capital $M$.
$$
\sum_{p \in P} \sum_{k \in K} k \cdot x_{p, k} \le M
$$
Substituting $M=4$:
$$
\sum_{p \in P} \sum_{k \in K} k \cdot x_{p, k} \le 4
$$

**Constraint 3: Non-negativity/Integrality**
$$
x_{p, k} \in \{0, 1\} \quad \forall p \in P, k \in K
$$

---

### Model Solution Analysis (Optional but requested "Formulate and solve")

To verify the model's logic, let's look at the optimal allocation.
We need to choose one $k_A, k_B, k_C \in \{0,1,2,3,4\}$ such that $k_A + k_B + k_C \le 4$ to maximize $V_A(k_A) + V_B(k_B) + V_C(k_C)$.

Let's evaluate marginal benefits or just check combinations summing to 4 (since benefits are generally increasing, we likely use all capital, though C drops at 4).

Possible integer partitions of 4 into 3 non-negative parts $(k_A, k_B, k_C)$:
1.  **(4, 0, 0):** $66 + 0 + 0 = 66$
2.  **(3, 1, 0):** $60 + 42 + 0 = 102$
3.  **(3, 0, 1):** $60 + 0 + 64 = 124$
4.  **(2, 2, 0):** $48 + 50 + 0 = 98$
5.  **(2, 1, 1):** $48 + 42 + 64 = 154$
6.  **(2, 0, 2):** $48 + 0 + 68 = 116$
7.  **(1, 3, 0):** $41 + 60 + 0 = 101$
8.  **(1, 2, 1):** $41 + 50 + 64 = 155$
9.  **(1, 1, 2):** $41 + 42 + 68 = 151$
10. **(1, 0, 3):** $41 + 0 + 78 = 119$
11. **(0, 4, 0):** $0 + 66 + 0 = 66$
12. **(0, 3, 1):** $0 + 60 + 64 = 124$
13. **(0, 2, 2):** $0 + 50 + 68 = 118$
14. **(0, 1, 3):** $0 + 42 + 78 = 120$
15. **(0, 0, 4):** $0 + 0 + 76 = 76$
16. **(1, 1, 1) sum=3:** $41+42+64 = 147$ (Leaves 1 unit unused. Is it better to add 1 to any?
    *   Add to A (2,1,1): 154
    *   Add to B (1,2,1): 155
    *   Add to C (1,1,2): 151
    *   So 147 is not optimal compared to using all 4.)
17. **(2, 2, 0) sum=4:** 98
18. **(0, 2, 1) sum=3:** $0+50+64=114$. Add 1 to A -> (1,2,1)=155. Add 1 to B -> (0,3,1)=124. Add 1 to C -> (0,2,2)=118.

Comparing the highest candidates using all 4 units:
*   Allocation (1, 2, 1): $V_A(1) + V_B(2) + V_C(1) = 41 + 50 + 64 = 155$
*   Allocation (2, 1, 1): $V_A(2) + V_B(1) + V_C(1) = 48 + 42 + 64 = 154$
*   Allocation (1, 1, 2): $V_A(1) + V_B(1) + V_C(2) = 41 + 42 + 68 = 151$

The maximum benefit is **155** thousand yuan.
This occurs when:
*   Project A receives **1** thousand yuan.
*   Project B receives **2** thousand yuan.
*   Project C receives **1** thousand yuan.

**Final Answer:**
The optimal allocation is **1 thousand yuan to Project A, 2 thousand yuan to Project B, and 1 thousand yuan to Project C**, resulting in a maximum total benefit of **155 thousand yuan**.