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

d_grouping = {}
for line in sys.stdin:
    line = line.strip()
    president, valence = line.split('\t')
    valence = int(valence)
    # president = clean_text(president)
    # valence = int(clean_text(valence))
    if president in d_grouping:
        d_grouping[president] = (d_grouping[president][0] + valence, d_grouping[president][1] + 1)
    else:
        d_grouping[president] = (valence, 1)


final_output = {}
for key in d_grouping:
    final_output[key] = d_grouping[key][0] / d_grouping[key][1]
    print(key + '\t' + str(final_output[key]))
    # pair = (key, final_output[key])
    # print(pair)
    #computes the average valence of all the words said by each president (key)