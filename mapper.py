"""mapper.py"""
import io
import os
import sys
import re
import string
import fileinput


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


# speech = sys.stdin
# text_wrapper = io.TextIOWrapper(speech)
# prez_name = text_wrapper.name
# print(prez_name)

map_array = []
count = 0
for line in sys.stdin:
# for line in fileinput.input():
#     print(fileinput.filename())
#     print(os.path.basename(sys.stdin))
    line = clean_text(line)
    line = line.strip()
    words = line.split()
    for word in words:
        #if word is in the valence list
        if word in d_valences:
            prez = 'adams'
            # temp = os.environ('sys.stdin')
            # print(temp)
            valence = d_valences[word]
            pair = (prez, valence)
            print(pair)
        #then create tuple ('president', word_valence)
        #all the mapper needs to do is create this tuple and output?
        #Then the reducer SAVES all the outputs, sorts/does it calculations


# print(map_array)