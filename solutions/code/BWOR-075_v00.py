import heapq
import sys

# Distance matrix from Table 8-4 (1-indexed, wells 1 through 8)
# Based on the problem context, we need the distance values.
# Since the exact table values are not explicitly listed in the prompt text,
# I must infer them or raise an error. However, standard textbook problems
# of this type (Offshore Oil Pipeline, 8 wells) often have specific values.
# Looking at the prompt: "d_ij: Distance between well i and well j (from Table 8-4)."
# The prompt does NOT provide the actual numeric values for d_ij.
# Requirement 3: "Use ONLY parameter values explicitly present in the Math Model.
# If a value is marked [NOT_PROVIDED] or is absent, do NOT substitute a guess.
# Instead, raise a runtime error with a clear message."

# However, often in these prompts, the "Table 8-4" values are expected to be known
# or are part of a standard dataset. Let me re-read carefully.
# The prompt says "Convert this mathematical model...". It does not list the numbers.
# But wait, usually these prompts come with the data. If the data is missing,
# I should raise an error.

# Let's check if there are any hidden numbers.
# "d_coast = 5" is given.
# "d_ij ... from Table 8-4".
# No other numbers are provided in the text.

# Therefore, I must raise a ValueError.

raise ValueError("Parameter d_ij (distance matrix for wells 1-8) not provided in model. Please provide the values from Table 8-4.")