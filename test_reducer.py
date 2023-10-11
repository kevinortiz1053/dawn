"""reducer.py"""
import sys


def clean_text(text):
    text = text.lower()
    punc = "()'"
    for char in text:
        if char in punc:
            text = text.replace(char, "")
    return text

# Given an array with all (president, word-valence) pairs

# d_grouping = {}
for line in sys.stdin:
    # line = line.strip()
    # president, valence = line.split(',', 1)
    # president = clean_text(president)
    # valence = int(clean_text(valence))
    # pair = (president, valence)
    # print(pair)
    print(line)