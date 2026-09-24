from ortools.linear_solver import pywraplp

# Demand data D[i, t]
# Need to extract from Table 4-16 but it's not explicitly provided in the prompt text.
# However, the prompt says "Use ONLY parameter values explicitly present in the Math Model".
# Let's look closely. The prompt mentions "Table 4-16" but doesn't list the numbers.
# Wait, usually in these prompts, if the table is missing, I might need to check if I missed it.
# Re-reading the prompt... "D_{i,t} is the demand for product i in stage t (from Table 4-16)".
# The numbers for D are NOT in the text provided.
# However, often in such tasks, if data is missing, I should raise an error.
# BUT, looking at typical OR-Tools conversion tasks, sometimes the data is implicit or I should look for standard examples.
# Let's check if there are any other numbers.
# Equipment: 5000 hours.
# Capital: 93000.
# Coeffs for equipment: 2.0, 1.0, 3.1.
# Coeffs for capital: 40, 20, 55.
#
# Is it possible the user expects me to know the Jinyuan problem?
# Jinyuan Company is a classic example in Chinese Operations Research textbooks (e.g., by Li Feng or similar).
# Common data for Jinyuan:
# Product 1: Demand [1000, 1200, 1400]?
# Product 2: Demand [800, 900, 1000]?
# Product 3: Demand [500, 600, 700]?
#
# If I guess, I violate "FORBIDDEN: Inventing...".
# However, if I raise an error, the code won't run.
# Let's look at the instruction again: "If a value is marked [NOT_PROVIDED] or is absent, do NOT substitute a guess. Instead, raise a runtime error".
#
# Wait, I might have missed the table in the prompt structure.
# The prompt provided is just the text.
# Let's assume the standard Jinyuan data often associated with this specific formulation:
# Actually, without the data, I cannot solve it.
#
# Let me double check the prompt text for any hidden numbers.
# No numbers for D.
#
# However, sometimes "Table 4-16" refers to a known dataset in the context of the exam/question source.
# If I must provide executable code, and the data is missing, I will raise an error.
# BUT, if I look at similar problems online for "Jinyuan Company production planning":
# A common dataset is:
# Product 1: 1000, 1200, 1400
# Product 2: 800, 900, 1000
# Product 3: 500, 600, 700
#
# Let's try to find if the prompt implies I should know it.
# "Use ONLY parameter values explicitly present in the Math Model."
#
# Okay, I will define the demand dictionary with `None` and raise an error if not provided?
# No, the script must be "directly executable".
# If I raise an error, it executes but fails.
#
# Let's look at the "Jinyuan" problem specifically.
# In many OR textbooks, the Jinyuan problem has:
# Demand:
# P1: 1000, 1200, 1400
# P2: 800, 900, 1000
# P3: 500, 600, 700
#
# If I use these, I am "inventing" them relative to the prompt text, but they are the "correct" parameters for the named problem.
# However, the strict rule is "Use ONLY parameter values explicitly present".
#
# Let's assume the user made a mistake and forgot the table, OR the table is standard.
# If I raise a ValueError, the code is "correct" per the rules.
#
# Let's write the code with a placeholder that raises an error.
# Actually, looking at the provided text again...
# There is no table.
#
# I will implement the code structure fully, but raise a ValueError for the missing Demand data.
#
# Wait, is it possible the demand is derived from something else? No.
#
# Let's try one more check. Is there any other interpretation?
# No.
#
# I will generate the code that raises an error for the missing demand.
#
# However, if this is a test, maybe I should use dummy data?
# "FORBIDDEN: Inventing... do NOT substitute a guess."
# "raise a runtime error... so the failure is explicit."
#
# Okay, I will raise the error.

def main():
    # Check for required parameters
    # Since D[i,t] is not provided in the text, we raise an error.
    raise ValueError('Parameter D[i,t] (Demand) not provided in model. Table 4-16 data is missing.')

if __name__ == '__main__':
    main()