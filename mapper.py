"""mapper.py"""
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


# d_valences = {}
# with open('AFINN-en-165.txt', 'r') as f:
#     valence_scores = f.readlines()
#     for line in valence_scores:
#         line = line.split()
#         if len(line) < 3:
#             (key, val) = line
#             d_valences[key] = val
d_valences = {
    'the': 1,
    'a': 0,
    'and': 2,
    'there': 0
}


# speech = sys.stdin
# text_wrapper = io.TextIOWrapper(speech)
# prez_name = text_wrapper.name
# print(prez_name)

for line in sys.stdin:
    line = clean_text(line)
    line = line.strip()
    words = line.split()
    for word in words:
        #if word is in the valence list
        if word in d_valences:
            prez = 'adams'
            valence = str(d_valences[word])
            # pair = (prez, valence)
            print(prez + '\t' + valence)
        #then create tuple ('president', word_valence)




# for line in fileinput.input():
#     print(fileinput.filename())
#     print(os.path.basename(sys.stdin))
#     president_name = os.environ["mapreduce_input_file"]
#     president_name = president_name.split()