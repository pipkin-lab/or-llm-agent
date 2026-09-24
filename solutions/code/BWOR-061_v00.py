# Sequential Interview Hiring Strategy - Expected Value Calculation
# The model is a deterministic enumeration over 4 discrete strategies.
# We compute the expected score for each strategy and select the maximum.

# Probabilities
P3 = 0.2  # P(S=3)
P2 = 0.5  # P(S=2)
P1 = 0.3  # P(S=1)

# Expected score of a random candidate
E_S = 3 * P3 + 2 * P2 + 1 * P1  # 0.6 + 1.0 + 0.3 = 1.9

# P(reach stage 2) = P(S1 in {1,2}) = P1 + P2 = 0.8
P_reach2 = P1 + P2  # 0.8

# P(reach stage 3) depends on strategy
# For D1=R: P_reach3 = P(S1 in {1,2}) * P(S2 in {1,2}) = 0.8 * 0.8 = 0.64
# For D1=H: P_reach3 = P(S1=1) * P(S2 in {1,2}) = 0.3 * 0.8 = 0.24

# Strategy 1: D1=R, D2=R
# Stop at 1: S1=3, prob=0.2, score=3
# Stop at 2: S1 in {1,2} and S2=3, prob=0.8*0.2=0.16, score=3
# Stop at 3: S1 in {1,2} and S2 in {1,2}, prob=0.8*0.8=0.64, E[S3]=1.9
Z1 = 3 * P3 + 3 * (P_reach2 * P3) + E_S * (P_reach2 * (P1 + P2))
# Z1 = 3*0.2 + 3*(0.8*0.2) + 1.9*(0.8*0.8) = 0.6 + 0.48 + 1.216 = 2.296

# Strategy 2: D1=R, D2=H
# Stop at 1: S1=3, prob=0.2, score=3
# Stop at 2: S1 in {1,2} and S2 in {2,3}, prob=0.8*(0.5+0.2)=0.8*0.7=0.56
#   - S2=3: prob=0.8*0.2=0.16, score=3
#   - S2=2: prob=0.8*0.5=0.40, score=2
# Stop at 3: S1 in {1,2} and S2=1, prob=0.8*0.3=0.24, E[S3]=1.9
Z2 = 3 * P3 + 3 * (P_reach2 * P3) + 2 * (P_reach2 * P2) + E_S * (P_reach2 * P1)
# Z2 = 0.6 + 0.48 + 0.8 + 0.456 = 2.336

# Strategy 3: D1=H, D2=R
# Stop at 1: S1 in {2,3}
#   - S1=3: prob=0.2, score=3
#   - S1=2: prob=0.5, score=2
# Stop at 2: S1=1 and S2=3, prob=0.3*0.2=0.06, score=3
# Stop at 3: S1=1 and S2 in {1,2}, prob=0.3*0.8=0.24, E[S3]=1.9
Z3 = 3 * P3 + 2 * P2 + 3 * (P1 * P3) + E_S * (P1 * (P1 + P2))
# Z3 = 0.6 + 1.0 + 0.18 + 0.456 = 2.236

# Strategy 4: D1=H, D2=H
# Stop at 1: S1 in {2,3}
#   - S1=3: prob=0.2, score=3
#   - S1=2: prob=0.5, score=2
# Stop at 2: S1=1 and S2 in {2,3}
#   - S2=3: prob=0.3*0.2=0.06, score=3
#   - S2=2: prob=0.3*0.5=0.15, score=2
# Stop at 3: S1=1 and S2=1, prob=0.3*0.3=0.09, E[S3]=1.9
Z4 = 3 * P3 + 2 * P2 + 3 * (P1 * P3) + 2 * (P1 * P2) + E_S * (P1 * P1)
# Z4 = 0.6 + 1.0 + 0.18 + 0.30 + 0.171 = 2.251

strategies = dict()
strategies[1] = Z1
strategies[2] = Z2
strategies[3] = Z3
strategies[4] = Z4

best_val = 0.0
for k in [1, 2, 3, 4]:
    if strategies[k] > best_val:
        best_val = strategies[k]

print("OPTIMAL_VALUE:", best_val)