from ortools.linear_solver import pywraplp

# Problem parameters
routes = [1, 2, 3, 4]
n_sailings = {1: 3, 2: 2, 3: 1, 4: 1}
origin = {1: 'E', 2: 'B', 3: 'A', 4: 'D'}
dest = {1: 'D', 2: 'C', 3: 'F', 4: 'B'}
sailing_time = {1: 17, 2: 3, 3: 7, 4: 13}
service_time = 1
frequency = {1: 1.0/3.0, 2: 1.0/2.0, 3: 1.0, 4: 1.0}

# Sailing times between all city pairs (symmetric, derived from problem context)
# Cities: A, B, C, D, E, F
# We need sailing times for repositioning between destinations and origins
# From the problem: F->B is 8 days, B->E is 8 days
# We need to infer or use standard distances. Let's define a matrix based on typical problem setup.
# Since exact times for all pairs are not explicitly given for all, we must assume a metric or use provided examples.
# Provided: F->B = 8, B->E = 8.
# Let's assume a complete graph with the following distances (days) based on standard OR problem examples of this type:
# A-B: 5, A-C: 4, A-D: 6, A-E: 7, A-F: 7 (Route 3 is A->F, 7 days)
# B-C: 3 (Route 2 is B->C, 3 days)
# B-D: 5, B-E: 8, B-F: 8
# C-D: 4, C-E: 6, C-F: 5
# D-E: 4, D-F: 6
# E-F: 5
# Note: Route 1 is E->D (17 days), Route 4 is D->B (13 days). These are route-specific durations, not just repositioning.
# Repositioning time is the sailing time between cities, which may differ from route durations if routes involve specific paths or are one-way specific.
# However, usually in these problems, the "sailing time" between two cities is a fixed parameter.
# Let's define a dictionary for repositioning times (days) between any two cities.
# We know:
# F->B = 8
# B->E = 8
# We need times for all (dest_r, origin_s) pairs.
# Let's construct a full matrix. If not provided, we must raise an error or make a reasonable assumption.
# The prompt says "If a value is marked [NOT_PROVIDED] or is absent, do NOT substitute a guess."
# However, the problem asks to solve the model. The model requires these times.
# Let's look at the "Feasibility Check Example" again.
# "Sailing F->B is 8 days".
# "Sailing B->E is 8 days".
# We are missing many. Let's assume the problem implies a standard set of distances or that we should define them.
# Actually, looking at the routes:
# R1: E->D (17 days)
# R2: B->C (3 days)
# R3: A->F (7 days)
# R4: D->B (13 days)
# These are the route durations. The repositioning time between any two cities is typically the shortest sailing time between them.
# In many textbook examples, a distance matrix is provided. Since it is not fully provided, but the task is to convert the model,
# and the model *requires* these parameters, I will define a placeholder matrix that matches the known values and
# fills in others with a consistent metric (e.g., Euclidean-like or standard shipping distances) ONLY IF the problem implies they are known.
# Wait, the instructions say: "Use ONLY parameter values explicitly present in the Math Model... If a value is... absent, do NOT substitute a guess. Instead, raise a runtime error".
# The Math Model section in the prompt *describes* the model but does *not* provide the full sailing time matrix for repositioning.
# It only provides:
# 1. Route durations (which are specific to the route, possibly including specific paths).
# 2. Two specific repositioning times: F->B (8 days) and B->E (8 days).
# 3. It does NOT provide A->B, A->C, etc. for repositioning.
# However, without these, the model cannot be solved.
# Re-reading the prompt: "Convert the provided mathematical model into... Python script."
# The "Math Model" is the text provided. The text says "Sailing F->B is 8 days" and "Sailing B->E is 8 days" in the explanation.
# It does not provide the rest.
# Is it possible the problem assumes the repositioning time is 0 or that we only need to check the provided ones? No, that would be incorrect.
# Let's look at the "Rough Estimate" part. It doesn't give more numbers.
# Perhaps the "Sailing Time" between cities is the same as the route duration if it were a route between them? No.
# Let's assume the standard interpretation for this specific classic OR problem (often found in textbooks):
# There is a known set of sailing times between the ports.
# Since I must not guess, I will check if the problem *implicitly* provides them.
# The problem states: "Sailing Time(d_r, o_s)".
# It gives an example: F->B is 8.
# It gives another: B->E is 8.
# It does not give the rest.
# However, in similar problems, the sailing times are often symmetric and small integers.
# Let's look at the constraints. If I raise an error, the code is not useful.
# But the rule is strict: "FORBIDDEN: Inventing... parameter... raise a runtime error".
# Let's check if the "Sailing Duration" given for the routes (17, 3, 7, 13) can be used as repositioning times?
# No, E->D is a route, not necessarily the shortest path or the repositioning time for other purposes.
# Actually, in this specific problem structure (Minimum Ship Deployment), the "Sailing Time" between ports is a fixed network parameter.
# If the text does not provide the full matrix, I cannot solve it.
# HOWEVER, looking at the provided text closely:
# "Sailing Duration: Route 1 (E->D): 17 days... Route 2 (B->C): 3 days..."
# These are the times for the *service*.
# For repositioning, we need the time to sail from one city to another.
# The example says "Sailing F->B is 8 days".
# It says "Sailing B->E is 8 days".
# It does not say anything else.
# I will define the known values and raise a ValueError for the missing ones to strictly follow the instructions.
# BUT, usually, in these prompts, if a matrix is not given, it might be that the repositioning time is assumed to be 0 or that the problem is simpler.
# Let's reconsider the "Rough Estimate".
# "Route 1 requires 3 ships if it were isolated".
# This implies the frequency and duration are the main drivers.
# Let's assume the repositioning times are NOT zero.
# If I must follow the rule strictly, I will implement the code to use a `sailing_time_matrix` dictionary.
# I will populate it with the known values:
# ('F', 'B'): 8
# ('B', 'E'): 8
# And for all other pairs, I will check if they are needed.
# If a pair is needed and not in the dict, I raise an error.

sailing_time_matrix = {
    ('F', 'B'): 8,
    ('B', 'E'): 8,
    # Add other known pairs if any. 
    # The problem does not provide others.
}

# Helper to get repositioning time
def get_reposition_time(from_city, to_city):
    if from_city == to_city:
        return 0
    key = (from_city, to_city)
    if key in sailing_time_matrix:
        return sailing_time_matrix[key]
    # Check reverse if symmetric? The problem doesn't state symmetry.
    # Let's assume symmetry for now but strictly we should not guess.
    # If not found, raise error.
    raise ValueError(f"Repositioning time from {from_city} to {to_city} not provided in model")

# Pre-calculate start and end times for each sailing
# We assume all sailings start at time 0? Or are they periodic?
# The problem says "Route 1: Every 1/3 day".
# To model this as a minimum fleet problem, we typically look at a steady state or a specific time window.
# The standard approach for "Minimum Fleet" with periodic schedules is to consider the "tightest" interval or use a time-expanded network over a common period.
# However, a simpler and more robust method for this specific type of problem (given the small numbers) is to treat each sailing instance as a node and check feasibility.
# Since the frequencies are different, the schedule is periodic with a period of LCM of frequencies.
# Frequencies: 1/3, 1/2, 1, 1.
# Periods: 3, 2, 1, 1. LCM(3, 2, 1, 1) = 6 days.
# In 6 days:
# R1: 6 * 3 = 18 sailings.
# R2: 6 * 2 = 12 sailings.
# R3: 6 * 1 = 6 sailings.
# R4: 6 * 1 = 6 sailings.
# Total sailings = 18 + 12 + 6 + 6 = 42.
# This is a manageable size for a MILP.

# Let's define the nodes.
# Node (r, k) represents the k-th sailing of route r within the period.
# We need start times and end times.
# Let's assume the first sailing of each route starts at t=0.
# For route r with frequency f_r (sailings per day), the k-th sailing starts at (k-1) / f_r.
# Wait, "Every 1/3 day" means 3 sailings per day.
# So start time of k-th sailing = (k-1) * (1/frequency).
# End time = Start time + Sailing Time + Service Time?
# The problem says: "t_{r, k}^{end} + LoadingTime + SailingTime(d_r, o_s) <= t_{s, m}^{start}"
# And "Service Time: 1 day (loading/unloading)".
# Usually, the ship must be at the destination, unload (1 day), then reposition, then load (1 day?) at the new origin.
# The formula in the model: `t_end + LoadingTime + SailingTime(dest, origin) <= t_start`
# It only adds "LoadingTime" once? Or is "Service Time" the unload?
# Let's stick to the formula: `t_end + 1 + reposition <= t_start`.
# Note: The ship is available at `t_end + 1` (after unloading). Then it sails to the new origin.
# Does it need to load at the new origin? The formula doesn't include a loading time at the new origin.
# It just says `t_end + LoadingTime + SailingTime <= t_start`.
# I will follow the formula exactly.

# Define all sailing instances
instances = []
for r in routes:
    f_r = frequency[r]
    n = n_sailings[r] # Wait, n_sailings in the problem description is "sailings n_1=3".
    # Is n_1 the number of sailings *per day* or *total in the period*?
    # "Route 1: E->D, sailings n_1=3". "Frequency: Route 1: Every 1/3 day (3 times a day)".
    # So n_r is the frequency (sailings per day).
    # In a period of P days, number of sailings = n_r * P.
    # Let's use P = 6 days.
    pass

# Let's re-evaluate the period.
# If we use a period of 6 days:
# R1: 3 sailings/day * 6 days = 18 sailings.
# R2: 2 sailings/day * 6 days = 12 sailings.
# R3: 1 sailing/day * 6 days = 6 sailings.
# R4: 1 sailing/day * 6 days = 6 sailings.

# However, the problem statement says "sailings n_1=3". It might mean there are only 3 specific sailings to schedule?
# "Route 1: E->D, sailings n_1=3".
# "Frequency: Route 1: Every 1/3 day (3 times a day)".
# This is slightly ambiguous. Does it mean there are exactly 3 sailings total, or 3 per day?
# "3 times a day" suggests frequency.
# But "sailings n_1=3" sounds like a count.
# If it's a count, the "Frequency" description is just explaining why there are 3 (maybe they are spaced 1/3 day apart).
# If it's a count, we don't need a period. We just have 3 specific sailings for R1.
# Let's assume the "n_r" values (3, 2, 1, 1) are the TOTAL number of sailings to be performed in the planning horizon.
# This simplifies the model significantly.
# If so, we don't need to expand by a period. We just have 3+2+1+1 = 7 sailings total.
# Let's check the "Rough Estimate": "Route 1 requires 3 ships if it were isolated (3 x 18 days coverage)".
# If there are only 3 sailings, one ship can do all 3 if it has enough time.
# 3 sailings, each 18 days. Total 54 days.
# If they are spaced 1/3 day apart, the ship can't do them all sequentially in 54 days if the schedule is tight?
# No, if they are 3 sailings total, the timing depends on when they happen.
# The "Frequency" info is crucial for the *schedule*.
# If I assume there are only 3 total sailings, I need their specific start times.
# The problem doesn't give specific dates, only frequency.
# This implies a periodic steady-state problem.
# The minimum fleet size in a periodic problem is the minimum number of ships to cover all sailings in one period, assuming the schedule repeats.
# So, using the period of 6 days is the correct approach for a periodic schedule.
# Total sailings in 6 days: 18 + 12 + 6 + 6 = 42.
# This is a small MILP.

# Let's build the network for the 6-day period.
# Nodes: (r, k) where r in [1..4], k in [1..n_r*6].
# We need start and end times for each.
# Assume first sailing of each route starts at t=0.
# Start time of k-th sailing of route r: t_start(r, k) = (k - 1) * (1 / frequency[r])
# End time: t_end(r, k) = t_start(r, k) + sailing_time[r] + service_time
# Wait, the formula for feasibility is: t_end(r, k) + 1 + reposition <= t_start(s, m).
# The "1" is the loading/unloading time.
# Does the end time include the service time?
# "t_{r, k}^{end}" is the completion time.
# Usually, completion time = start + sailing duration.
# Then the ship unloads for 1 day.
# So available time = t_end + 1.
# Let's assume t_end is just start + sailing_time.

# Let's refine the times.
# Sailing time for route r: sail_r
# Start time: t_s
# End time (arrival at dest): t_s + sail_r
# Time available for next task: t_s + sail_r + 1 (unload)
# Feasibility: t_s(r,k) + sail_r + 1 + rep(dest_r, origin_s) <= t_s(s,m)

# We need the repositioning times.
# Known: F->B (8), B->E (8).
# Missing: All others.
# I will raise an error for missing repositioning times.

# However, to make the code runnable and demonstrate the structure, I will define a full matrix
# by assuming the missing values are not provided and thus raising an error if accessed.
# But the user wants a "clean, self-contained Python script" that solves the model.
# If the model is unsolvable due to missing data, the script should raise an error.
# I will implement the full logic, but it will crash if a repositioning time is missing.
# To be helpful, I will assume that if a repositioning time is not provided, it might be 0 (if same city) or that the problem implies a specific set.
# Given the strict instruction "do NOT substitute a guess", I will strictly raise an error.

# Let's double check the "n_r" interpretation.
# If n_r is the frequency (sailings per day), then in a period of 6 days, we have many sailings.
# If n_r is the total count, we have few.
# "Route 1: E->D, sailings n_1=3".
# "Frequency: Route 1: Every 1/3 day (3 times a day)".
# This strongly suggests n_r is the frequency.
# I will proceed with the 6-day period expansion.

# Define period
period = 6

# Generate all sailing instances
# List of tuples: (route, index_in_period, start_time, end_time, origin, dest)
all_sailings = []
for r in routes:
    f_r = frequency[r]
    n_in_period = int(f_r * period)
    for k in range(1, n_in_period + 1):
        t_start = (k - 1) * (1.0 / f_r)
        t_end = t_start + sailing_time[r]
        all_sailings.append({
            'route': r,
            'index': k,
            'start': t_start,
            'end': t_end,
            'origin': origin[r],
            'dest': dest[r]
        })

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')
if not solver:
    raise RuntimeError("Could not create SCIP solver")

# Create variables for each arc in the flow network
# Nodes are the sailings themselves.
# Flow goes from one sailing to another if feasible.
# Also, flow from Source to Sailing (new ship) and Sailing to Sink (ship ends).
# We minimize the number of new ships (flow from Source).

# Variables:
# x[s1][s2]: flow from sailing s1 to sailing s2 (0 if not feasible, else 0/1)
# y[s]: flow from Source to sailing s (new ship starts here)
# z[s]: flow from sailing s to Sink (ship ends here)

# We use a dictionary for x
x = dict()
y = dict()
z = dict()

# Total number of sailings
N = len(all_sailings)
sailing_ids = list(range(N))

# Pre-calculate feasibility and create variables
for i in sailing_ids:
    s1 = all_sailings[i]
    # Arc from Source to s1
    y[i] = solver.IntVar(0, 1, f'y_{i}')
    # Arc from s1 to Sink
    z[i] = solver.IntVar(0, 1, f'z_{i}')
    
    for j in sailing_ids:
        s2 = all_sailings[j]
        # Check feasibility: s1 -> s2
        # s1 must finish, unload, reposition, and s2 must start
        # t_end(s1) + 1 + rep(dest_s1, origin_s2) <= t_start(s2)
        # Also, s1 must end before s2 starts (time order)
        if s1['end'] > s2['start']:
            # Not feasible, no variable needed
            continue
        
        rep_time = get_reposition_time(s1['dest'], s2['origin'])
        if s1['end'] + 1 + rep_time <= s2['start']:
            # Feasible
            x[(i, j)] = solver.IntVar(0, 1, f'x_{i}_{j}')
        else:
            # Not feasible
            # We don't create a variable, or we force it to 0.
            # To keep the model sparse, we just don't create it.
            # But we need to ensure flow conservation works.
            # If no variable exists, the flow is 0.
            pass

# Objective: Minimize sum of y[i] (new ships)
objective = solver.Sum(y[i] for i in sailing_ids)
solver.Minimize(objective)

# Constraints: Flow Conservation
# For each sailing i:
# Inflow = y[i] + sum(x[j, i] for all j where x[j, i] exists)
# Outflow = z[i] + sum(x[i, k] for all k where x[i, k] exists)
# Inflow must equal Outflow.
# Also, each sailing must be covered.
# The flow through sailing i (Inflow) must be 1.
# Because each sailing is performed by exactly one ship.
# So, y[i] + sum(x[j, i]) == 1 for all i.
# And z[i] + sum(x[i, k]) == 1 for all i.
# This implies Inflow = Outflow = 1.

for i in sailing_ids:
    # Inflow to i
    inflow_terms = [y[i]]
    for j in sailing_ids:
        if (j, i) in x:
            inflow_terms.append(x[(j, i)])
    
    # Outflow from i
    outflow_terms = [z[i]]
    for k in sailing_ids:
        if (i, k) in x:
            outflow_terms.append(x[(i, k)])
    
    # Constraint: Inflow == 1
    solver.Add(solver.Sum(inflow_terms) == 1)
    
    # Constraint: Outflow == 1
    solver.Add(solver.Sum(outflow_terms) == 1)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")

# Note: This code will raise a ValueError if a repositioning time is missing.
# To make it robust for demonstration, if I were allowed to guess, I would fill the matrix.
# But per instructions, I will leave it as is.
# However, the user might expect it to run.
# Let's check if there are other interpretations.
# Maybe the "Sailing Time" between cities is just the Euclidean distance?
# Or maybe the problem assumes 0 repositioning time if not specified?
# No, that would be a guess.
# I will add a comment in the code about the missing data.

# To prevent the script from crashing immediately if the user runs it with missing data,
# and since the instruction says "raise a runtime error with a clear message",
# the current implementation does exactly that via `get_reposition_time`.

# Final check: The problem might have a simpler interpretation where repositioning time is 0?
# "Sailing F->B is 8 days" is explicitly given, so it's not 0.
# I will stick to the strict interpretation.

# One more thing: The problem says "Minimum Number of Ships".
# The objective minimizes the number of new ships entering the system.
# In a periodic steady state, this equals the fleet size.
# The constraints ensure each sailing is covered.
# This is a correct formulation.

# To make the code "self-contained" and potentially runnable if the user provides the missing data,
# I will leave the `sailing_time_matrix` as is.

# If the user wants to test it, they can fill in the matrix.
# For the purpose of this response, the code is structurally correct.

# Let's add a fallback: If the problem intended for the repositioning time to be derived from the route durations?
# No, that's a guess.
# I will output the code as is.

# Wait, I can check if the problem is from a known source.
# "Minimum Ship Deployment" with routes E->D, B->C, A->F, D->B.
# This looks like a standard textbook problem.
# In many such problems, the sailing times between ports are given in a table.
# Since it's not here, I cannot solve it numerically without guessing.
# I will proceed with the error-raising approach.

# One minor optimization: Use a list of lists for x to make it faster, but dict is fine for small N.
# N = 42. N^2 = 1764. This is small.

# Final Code Structure:
# 1. Imports
# 2. Parameters
# 3. Sailing Time Matrix (with known values)
# 4. Helper function
# 5. Generate sailings
# 6. Solver setup
# 7. Variable creation
# 8. Objective
# 9. Constraints
# 10. Solve and print

# The code above follows this structure.

# Let's ensure the `get_reposition_time` function handles the case where the city is the same.
# If dest_r == origin_s, repositioning time is 0.
# This is already handled.

# I will now generate the final code block.