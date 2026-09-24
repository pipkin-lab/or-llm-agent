# Mathematical Optimization Model

## 1. Index Sets & Parameters

**Index Sets:**
- $I = \{1, 2, 3, 4, 5, 6, 7, 8\}$: Set of villages.
- $K = \{1, 2\}$: Set of schools to be built (identical facilities).

**Parameters:**
- $n_i$: Number of primary school students in village $i$.
  - $n = [60, 80, 100, 120, 80, 60, 40, 80]$ for $i=1$ to $8$.
- $x_i, y_i$: X and Y coordinates of village $i$.
  - $x = [0, 10, 12, 14, 16, 18, 8, 6]$
  - $y = [0, 3, 15, 13, 9, 6, 12, 10]$
- $d_{ij}$: Euclidean distance between village $i$ and village $j$.
  - Calculated as $d_{ij} = \sqrt{(x_i - x_j)^2 + (y_i - y_j)^2}$.
  - Note: $d_{ii} = 0$.

## 2. Decision Variables

**Binary Variables:**
- $z_{ik} \in \{0, 1\}$: Equals 1 if school $k$ is built in village $i$, 0 otherwise.
  - $i \in I, k \in K$.
- $a_{ik} \in \{0, 1\}$: Equals 1 if village $i$ is assigned to school $k$, 0 otherwise.
  - $i \in I, k \in K$.

## 3. Objective Function

Minimize the total walking distance for all students:

$$
\text{Minimize } Z = \sum_{i \in I} \sum_{j \in I} \sum_{k \in K} n_i \cdot d_{ij} \cdot a_{ik} \cdot z_{jk}
$$

**Linearization Note:**
The term $a_{ik} z_{jk}$ is non-linear. However, in a standard p-median problem where we assign villages to the *nearest* open facility, we can simplify the logic. Usually, we define assignment based on the open facility. A more standard linear formulation uses a third variable or relies on the fact that if a village is assigned to $k$, it must be assigned to the specific village $j$ hosting $k$.

Let's use a cleaner linear formulation with explicit assignment variables linked to facility location:

Let $y_{ij} \in \{0, 1\}$ be 1 if village $i$ is assigned to a school located in village $j$.
Let $z_j \in \{0, 1\}$ be 1 if a school is built in village $j$.

**Revised Decision Variables:**
- $z_j \in \{0, 1\}$ for $j \in I$: 1 if a school is built in village $j$.
- $a_{ij} \in \{0, 1\}$ for $i \in I, j \in I$: 1 if students from village $i$ are assigned to the school in village $j$.

**Revised Objective Function:**
$$
\text{Minimize } Z = \sum_{i \in I} \sum_{j \in I} n_i \cdot d_{ij} \cdot a_{ij}
$$

## 4. Operational Constraints

**1. School Location Constraints (Exactly 2 schools):**
$$
\sum_{j \in I} z_j = 2
$$

**2. Assignment to Open Schools Only:**
Students from village $i$ can only be assigned to village $j$ if a school is built in village $j$.
$$
a_{ij} \le z_j \quad \forall i \in I, j \in I
$$

**3. Each Village Assigned to Exactly One School:**
Every student in village $i$ must be assigned to exactly one school.
$$
\sum_{j \in I} a_{ij} = 1 \quad \forall i \in I
$$

**4. Non-negativity/Binary Bounds:**
$$
z_j \in \{0, 1\} \quad \forall j \in I
$$
$$
a_{ij} \in \{0, 1\} \quad \forall i \in I, j \in I
$$

### Verification of Model Integrity
- **Scale Check:** The problem involves 8 villages and 2 schools. This is a small-scale combinatorial problem. Integer/Binary variables are strictly required.
- **Logic Check:** The formulation ensures that exactly two locations are chosen. The constraint $a_{ij} \le z_j$ ensures no student is assigned to a non-existent school. The constraint $\sum_j a_{ij} = 1$ ensures every village's students are served.
- **Cost Calculation:** The objective sums the product of population, distance, and assignment indicator, correctly weighting the distance by the number of students walking it.