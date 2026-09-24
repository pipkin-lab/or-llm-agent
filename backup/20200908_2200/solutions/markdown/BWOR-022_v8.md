### 1. Index Sets & Parameters

**Index Sets:**
- $k \in \{1, 2, 3\}$: Set of components ($A_1, A_2, A_3$).
- $j \in \{1, 2, 3\}$: Set of possible numbers of spare parts for each component (1, 2, or 3).

**Parameters:**
- $B = 8$: Total budget limit (thousand yuan).
- $R_{k,j}$: Reliability of component $k$ when $j$ spare parts are allocated.
  - $R_{1,1}=0.3, R_{1,2}=0.4, R_{1,3}=0.5$
  - $R_{2,1}=0.2, R_{2,2}=0.5, R_{2,3}=0.9$
  - $R_{3,1}=0.1, R_{3,2}=0.2, R_{3,3}=0.7$
- $C_{k,j}$: Cost of allocating $j$ spare parts to component $k$ (thousand yuan).
  - $C_{1,1}=1, C_{1,2}=2, C_{1,3}=3$
  - $C_{2,1}=3, C_{2,2}=5, C_{2,3}=6$
  - $C_{3,1}=2, C_{3,2}=3, C_{3,3}=4$
- $V_{k,j} = \ln(R_{k,j})$: Logarithm of the reliability (objective contribution).

### 2. Decision Variables

Let $x_{k,j}$ be a binary decision variable:
$$
x_{k,j} = 
\begin{cases} 
1 & \text{if } j \text{ spare parts are allocated to component } k \\
0 & \text{otherwise}
\end{cases}
$$
for all $k \in \{1, 2, 3\}$ and $j \in \{1, 2, 3\}$.

**Domain:**
$x_{k,j} \in \{0, 1\}$

### 3. Objective Function

The goal is to maximize the equipment's operational reliability. For components working in series, the total reliability is the product of individual reliabilities ($R_{total} = R_1 \cdot R_2 \cdot R_3$). Maximizing the product is equivalent to maximizing the sum of the natural logarithms of the reliabilities (since $\ln$ is a monotonic increasing function).

$$
\text{Maximize } Z = \sum_{k=1}^{3} \sum_{j=1}^{3} V_{k,j} x_{k,j}
$$

Where $V_{k,j} = \ln(R_{k,j})$.

### 4. Operational Constraints

**Constraint 1: Allocation Uniqueness**
For each component $k$, exactly one number of spare parts must be selected from the available options $\{1, 2, 3\}$.

$$
\sum_{j=1}^{3} x_{k,j} = 1, \quad \forall k \in \{1, 2, 3\}
$$

**Constraint 2: Budget Limit**
The total cost of the selected spare parts must not exceed the total investment limit of 8 thousand yuan.

$$
\sum_{k=1}^{3} \sum_{j=1}^{3} C_{k,j} x_{k,j} \le 8
$$

**Constraint 3: Non-negativity/Integrality**
$$
x_{k,j} \in \{0, 1\}, \quad \forall k \in \{1, 2, 3\}, \forall j \in \{1, 2, 3\}
$$

---

### Solution Analysis (Verification)

To verify the model, we can enumerate the feasible combinations or solve the MILP.

Let's calculate the objective values for feasible integer combinations $(j_1, j_2, j_3)$ where $j_k$ is the number of spares for component $k$.

**Feasibility Check (Cost $\le 8$):**

1.  **(1,1,1):** Cost $1+3+2=6 \le 8$.
    Objective: $\ln(0.3) + \ln(0.2) + \ln(0.1) = \ln(0.006) \approx -5.116$
2.  **(2,1,1):** Cost $2+3+2=7 \le 8$.
    Objective: $\ln(0.4) + \ln(0.2) + \ln(0.1) = \ln(0.008) \approx -4.828$
3.  **(1,2,1):** Cost $1+5+2=8 \le 8$.
    Objective: $\ln(0.3) + \ln(0.5) + \ln(0.1) = \ln(0.015) \approx -4.199$
4.  **(1,1,2):** Cost $1+3+3=7 \le 8$.
    Objective: $\ln(0.3) + \ln(0.2) + \ln(0.2) = \ln(0.012) \approx -4.423$
5.  **(2,2,1):** Cost $2+5+2=9 > 8$ (Infeasible)
6.  **(2,1,2):** Cost $2+3+3=8 \le 8$.
    Objective: $\ln(0.4) + \ln(0.2) + \ln(0.2) = \ln(0.016) \approx -4.135$
7.  **(1,2,2):** Cost $1+5+3=9 > 8$ (Infeasible)
8.  **(1,1,3):** Cost $1+3+4=8 \le 8$.
    Objective: $\ln(0.3) + \ln(0.2) + \ln(0.7) = \ln(0.042) \approx -3.170$
9.  **(2,1,3):** Cost $2+3+4=9 > 8$ (Infeasible)
10. **(3,1,1):** Cost $3+3+2=8 \le 8$.
    Objective: $\ln(0.5) + \ln(0.2) + \ln(0.1) = \ln(0.010) \approx -4.605$
11. **(3,1,2):** Cost $3+3+3=9 > 8$ (Infeasible)
12. **(3,2,1):** Cost $3+5+2=10 > 8$ (Infeasible)
13. **(1,3,1):** Cost $1+6+2=9 > 8$ (Infeasible)
14. **(2,3,1):** Cost $2+6+2=10 > 8$ (Infeasible)
15. **(3,3,1):** Cost $3+6+2=11 > 8$ (Infeasible)
16. **(1,3,2):** Cost $1+6+3=10 > 8$ (Infeasible)
17. **(2,3,2):** Cost $2+6+3=11 > 8$ (Infeasible)
18. **(3,3,2):** Cost $3+6+3=12 > 8$ (Infeasible)
19. **(1,3,3):** Cost $1+6+4=11 > 8$ (Infeasible)
20. **(2,3,3):** Cost $2+6+4=12 > 8$ (Infeasible)
21. **(3,3,3):** Cost $3+6+4=13 > 8$ (Infeasible)

Let's check remaining feasible ones:
- **(1, 1, 3)**: Cost 8. Obj $\ln(0.042) \approx -3.170$
- **(2, 1, 3)**: Cost 9 (Infeasible)
- **(3, 1, 1)**: Cost 8. Obj $\ln(0.010) \approx -4.605$
- **(1, 2, 1)**: Cost 8. Obj $\ln(0.015) \approx -4.199$
- **(2, 1, 2)**: Cost 8. Obj $\ln(0.016) \approx -4.135$

Comparing the feasible objective values:
- $Z(1,1,3) = \ln(0.3 \times 0.2 \times 0.7) = \ln(0.042) \approx -3.170$
- $Z(2,1,2) = \ln(0.4 \times 0.2 \times 0.2) = \ln(0.016) \approx -4.135$
- $Z(1,2,1) = \ln(0.3 \times 0.5 \times 0.1) = \ln(0.015) \approx -4.199$
- $Z(3,1,1) = \ln(0.5 \times 0.2 \times 0.1) = \ln(0.010) \approx -4.605$
- $Z(2,1,1) = \ln(0.4 \times 0.2 \times 0.1) = \ln(0.008) \approx -4.828$
- $Z(1,1,2) = \ln(0.3 \times 0.2 \times 0.2) = \ln(0.012) \approx -4.423$
- $Z(1,1,1) = \ln(0.3 \times 0.2 \times 0.1) = \ln(0.006) \approx -5.116$

The maximum value is obtained at $x_{1,1}=1, x_{2,1}=1, x_{3,3}=1$ (i.e., 1 spare for $A_1$, 1 spare for $A_2$, 3 spares for $A_3$).

**Optimal Solution:**
- $A_1$: 1 spare part
- $A_2$: 1 spare part
- $A_3$: 3 spare parts
- Total Cost: $1 + 3 + 4 = 8$ thousand yuan
- Max Log-Reliability: $\ln(0.042) \approx -3.170$
- Max Reliability: $0.042$