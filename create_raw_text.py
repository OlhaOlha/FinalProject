import os
import nltk

development_data = "development"

raw_text = ''
for root, dirs, files in os.walk(development_data):
    for file in files:
        if file == "en.tok.off.pos":
            with open(os.path.join(root, file), 'r') as input_file:
                for line in input_file:
                    if line != '':
                        # List of all words in line, for example
                        # ['4', '10', '1002', 'United', 'NNP', 'COU', 'https://en.wikipedia.org/wiki/United_States']
                        splitnstrip = [x.strip('\n') for x in line.split(' ')]

                        # Current word
                        word = splitnstrip[3]
                        raw_text = raw_text + word + ' '
# print(raw_text)

with  open('raw_text.text', 'w') as output_file:
    output_file.write(raw_text)
