from cs50 import get_string
from decimal import Decimal, getcontext

# Define counters
letters = 0.00
words = 0.00
sent = 0.00

# Get a text from a user
s = get_string("Text: ")

# Count for words
word_list = s.split()
words = len(word_list)

# Scan a text
for i in s:
    # Count for letters
    if i.isalpha():
        letters += 1
    # Count for sentences
    elif i == "." or i == "!" or i == "?":
        sent += 1

# Count L and P variables for the Coleman-Liau formula
L = letters * (100 / words)
P = sent * (100 / words)

# Count the final index
index = 0.0588 * L - 0.296 * P - 15.8

# Round the index
fin = round(index)

# Print results
if fin < 1:
    print("Before Grade 1")
elif fin >= 16:
    print("Grade 16+")
else:
    print(f"Grade {fin}")
