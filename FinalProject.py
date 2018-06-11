# import fileinput

# Halyna's branch
import os
import nltk
from sklearn.metrics import classification_report
import wikipedia


# import bs4
# soup = bs4.BeautifulSoup(html, 'lxml')

# Simple check if a word with its pos-tag is an entity or not, output is True or False respectively
def is_entity(word, pos):

    # How to check if a word is an entity?

    if "NN" in pos and str(word)[0].isupper():
        return True
    else:
        return False


def get_class(word):  # we should definitely add input parameters here

    # ? How to get a class ?

    return "Class"


def get_link(word):  # we should definitely add input parameters here

    # STILL NEED TO WORK ON

    # Get possible options for a word
    possible_result = wikipedia.search(word, results=1)
    print("Possible result:", possible_result)

    # page = wikipedia.page(possible_result)
    # print("Page:", page)

    # Choose the first result
    res = str(possible_result).replace(" ", "_")
    print("res", res)

    # Get a url link
    link = None
    try:
        link = str(wikipedia.page(res).url)
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options
        print("options:", options)
        page = str(options[0]).replace(" ", "_")
        # try:
        #     link = wikipedia.page(page).url
    except wikipedia.exceptions.PageError:
            link = None


    print("Link:", link)
    #
    # # ? How to get a link properly ?
    #
    # return link

    return link





def get_classes_links(folder_data):
    list_of_classes = []
    list_of_links = []

    for root, dirs, files in os.walk(folder_data):
        for file in files:
            if file == "en.tok.off.pos.ent":
                with open(os.path.join(root, file), 'r') as input_file:
                    for line in input_file:
                        if line != '':
                            # List of all words in line, for example,
                            # ['4', '10', '1002', 'United', 'NNP', 'COU', 'https://en.wikipedia.org/wiki/United_States']
                            splitnstrip = [x.strip('\n') for x in line.split(' ')]

                            if len(splitnstrip) == 7:
                                # Append a class
                                list_of_classes.append(splitnstrip[5])
                                # Append a link
                                list_of_links.append(splitnstrip[6])
                            else:
                                # NO = Not interesting
                                list_of_classes.append('NO')
                                list_of_links.append('NO')
                            continue
    return list_of_classes, list_of_links


# Comparision with gold standard
def compare(gold_standard, comp, gold_links, dev_links):

    # Do not need it actually, but it can be used to get information
    #     true_positives = nltk.Counter()
    #     false_negatives = nltk.Counter()
    #     false_positives = nltk.Counter()
    #
    #     for i in labels:
    #         for j in labels:
    #             if i == j:
    #                 true_positives[i] += cm[i, j]
    #             else:
    #                 false_negatives[i] += cm[i, j]
    #                 false_positives[j] += cm[i, j]

    conf_matrix = nltk.ConfusionMatrix(gold_standard, comp)

    classidication_rep = classification_report(gold_standard, comp, list(set(gold_standard + comp)))

    correct_num = 0
    for i in range(len(gold_standard)):
        if gold_links[i] == dev_links[i]:
            correct_num += 1
    links_accuracy = correct_num / len(gold_standard)

    return conf_matrix, classidication_rep, links_accuracy


def main_processing(dev_data):
    # Simple work with input file en.tok.off.pos and output en.tok.off.pos.my.ent
    for root, dirs, files in os.walk(dev_data):
        for file in files:
            if file == "en.tok.off.pos":
                with open(os.path.join(root, file), 'r') as input_file, open(os.path.join(root, file) + '.ent', 'w') as output_file:
                    for line in input_file:
                        if line != '':
                            # List of all words in line, for example
                            # ['4', '10', '1002', 'United', 'NNP', 'COU', 'https://en.wikipedia.org/wiki/United_States']
                            splitnstrip = [x.strip('\n') for x in line.split(' ')]

                            # Current word
                            word = splitnstrip[3]
                            # Current part of speech tag
                            pos = splitnstrip[4]

                            if is_entity(word, pos):

                                wordclass = get_class(word)  # we need to work on this function
                                link = get_link(word)  # we need to work on this function as well

                                if wordclass is not None:
                                    splitnstrip.append(wordclass)  # class  here

                                if link is not None:
                                    splitnstrip.append(link)  # link here

                            output_file.write(' '.join(splitnstrip) + '\n')
                        else:
                            output_file.write(line)


def main():

    # Folders names
    development_data = "development"
    goldstandard_data = "goldstandard"

    # The most important - part that creates output .ent  
    main_processing(development_data)

    # Kind of processing that must be in measures.py

    # Preprocessing before the comparision with gold standard - get two lists of classes and links
    dev_list, links = get_classes_links(development_data)
    print("Development list:\n", dev_list)
    print("Development links:", links)

    gold_list, gold_links = get_classes_links(goldstandard_data)
    print("Gold list:\n", gold_list)
    print("Gold links:", gold_links)

    # Compare with gold standard
    confusion_matrix, classific_report, links_accuracy = compare(gold_list, dev_list, gold_links, links)
    print("Confusion matrix\n", confusion_matrix)
    print("Classification report\n", classific_report)
    print("Links accuracy:", links_accuracy)


main()

