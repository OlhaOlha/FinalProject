import nltk
import re
# Read the text
txt_file_path = 'raw_text.text'
with open(txt_file_path) as file:
    rawText = file.read()


sentences = nltk.sent_tokenize(rawText)

for sent in sentences:
    print('Sentence: ', sent)
    rgx = re.compile(r'[A-Z][A-Za-z]*(?:[\s-][A-Z][A-Za-z]*)*')
    collocations = rgx.findall(sent)
    print('List: ', collocations)
    # for c in collocations:
    #         if len(c.split(' '))==1:
    #             pos = nltk.pos_tag([c])
    #             if pos=='DT':
    #                 print('delete: ', c , ' - ', pos)


