"""mapper.py"""
import os
import sys
import re
import string


def clean_text(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
    text = re.sub('[\d\n]', ' ', text)
    return text


d_valences = {}
with open('valence_scores.txt', 'r') as f:
    valence_scores = f.readlines()
    for line in valence_scores:
        line = line.split()
        if len(line) < 3:
            (key, val) = line
            d_valences[key] = val

map_array = []
for line in sys.stdin:
    line = clean_text(line)
    line = line.strip()
    words = line.split()
    for word in words:
        #if word is in the valence list
        if word in d_valences:
            prez = 'adams'
            # prez = os.environ('sys.stdin')
            valence = d_valences[word]
            pair = (prez, valence)
            print(pair)
        #then create tuple ('president', word_valence)
        #all the mapper needs to do is create this tuple and output?
        #Then the reducer SAVES all the outputs, sorts/does it calculations


# print(map_array)