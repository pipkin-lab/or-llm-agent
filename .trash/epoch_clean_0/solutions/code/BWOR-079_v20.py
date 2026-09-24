from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

y = dict()
for d in range(1, 8):
    y[d] = solver.IntVar(0, INF, 'y_' + str(d))

# Objective: Minimize total nurses
obj = y[1] + y[2] + y[3] + y[4] + y[5] + y[6] + y[7]
solver.Minimize(obj)

# Requirements
R = dict()
R[1] = 18
R[2] = 20
R[3] = 19
R[4] = 17
R[5] = 12

# Helper to get the "start day" index for a shift s on day d (1-indexed, modulo 7)
# Shift s on day d is worked by nurses who started (s-1) days before d.
# start_day = ((d - (s - 1)) - 1) % 7 + 1
def start_day(d, s):
    return ((d - (s - 1)) - 1) % 7 + 1

# Add constraints for each day d in 1..7 and each time period t in 1..5
for d in range(1, 8):
    # For each time period t, the coverage is Shift t + Shift t+1 (with wrap-around for t=5 -> Shift 1)
    # Wait, let's re-verify the shift overlap logic from the prompt:
    # TP1 (6-10): Sh1 + Sh2
    # TP2 (10-14): Sh2 + Sh3
    # TP3 (14-18): Sh3 + Sh4
    # TP4 (18-22): Sh4 + Sh5
    # TP5 (22-6): Sh5 + Sh1
    
    # So for time period t, the shifts involved are s1 = t and s2 = t+1 (if t<5) or s1=5, s2=1 (if t=5).
    
    for t in range(1, 6):
        s1 = t
        if t < 5:
            s2 = t + 1
        else:
            s2 = 1
            
        # Get the start day indices for these shifts on day d
        idx1 = start_day(d, s1)
        idx2 = start_day(d, s2)
        
        # Constraint: y[idx1] + y[idx2] >= R[t]
        solver.Add(y[idx1] + y[idx2] >= R[t])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")