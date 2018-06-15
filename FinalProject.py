# import fileinput
import os
import nltk
from sklearn.metrics import classification_report
import wikipedia
import operator

# import bs4
# soup = bs4.BeautifulSoup(html, 'lxml')

# For testing
def read_from_file(txt_file_path):
    with open(txt_file_path, 'r') as f:
        lines = f.read().split('\n')
    return lines


def get_page_link(word):  # we should definitely add input parameters here
    page = None
    link = None
    possible_result = wikipedia.search(word, results=1)
    # print("Possible result:", possible_result)

    # Choose the first result
    res = str(possible_result).replace(" ", "_")
    # print("res", res)
    # Get a page
    try:
        try:
            page = wikipedia.page(res)
        except wikipedia.exceptions.DisambiguationError as e:
            options = e.options
            try:
                page = wikipedia.page(options[0])
            except wikipedia.exceptions.DisambiguationError as e1:
                options = e1.options
                try:
                    page = wikipedia.page(options[0])
                except wikipedia.exceptions.DisambiguationError:
                    page = None
    except wikipedia.exceptions.PageError:
        page = None
    if page:
            link = page.url
    return page, link


def category_count(str, list_of_words):
    count = 0
    for word in list_of_words:
        count = count + str.upper().count(word.upper())
    return count


def get_category(page):
    if page:
        categories = page.categories
        categories_str = ' '.join(categories)
        # print(page.title, categories_str)
        COU_list = ['countries', 'states of']
        COU_count = category_count(categories_str, COU_list)
        CIT_list = ['cities', 'city', 'town', 'towns', 'capitals', 'capital']
        CIT_count = category_count(categories_str, CIT_list)
        ANI_list = ['animal', 'animals', 'mammal', 'mammals', 'fish']
        ANI_count = category_count(categories_str, ANI_list)
        PER_list = ['person', 'persons', 'people']  # 'names'
        PER_count = category_count(categories_str, PER_list)
        SPO_list = ['sport', 'sports', 'ball games']
        SPO_count = category_count(categories_str, SPO_list)
        # 'Geography of' NAT - Natural places
        ORG_list = ['organization', 'organization', 'organisations', 'organisation', 'companies', 'company']
        ORG_count = category_count(categories_str, ORG_list)
        NAT_list = ['natural place', 'natural places', 'lake', 'lakes', 'mountain', 'mountains', 'volcano', 'volcanoes',
                    'river', 'rivers', 'sea', 'seas', 'ocean', 'oceans', 'forest', 'forests', 'waterfall', 'waterfalls']
        NAT_count = category_count(categories_str, NAT_list)
        ENT_list = ['books', 'magazines', 'films', 'songs', 'concerts', 'journals', 'movies', 'newspapers', 'radio',
                    'literature',
                    'book', 'magazine', 'film', 'song', 'concert', 'journal', 'movie', 'newspaper', 'series']
        ENT_count = category_count(categories_str, ENT_list)
        cat_dict = {'PER': PER_count, 'CIT': CIT_count, "COU": COU_count, 'ANI': ANI_count, 'SPO': SPO_count,
                    'ORG': ORG_count, 'NAT': NAT_count, 'ENT': ENT_count}
        # print('COU count: ', COU_count, 'COU')
        # print('CIT count: ', CIT_count, 'CIT')
        # print('ANI count: ', ANI_count, 'ANI')
        # print('PER count: ', PER_count, 'PER')
        # print('SPO count: ', SPO_count, 'SPO')
        # print('ORG count: ', ORG_count, 'ORG')
        # print('NAT count: ', NAT_count, 'NAT')
        # print('ENT count: ', ENT_count, 'ENT')
        # if (COU_count > 0) and (CIT_count > 0):
        if COU_count == 0 and CIT_count == 0 and ANI_count == 0 and PER_count == 0 and SPO_count == 0 \
                and ORG_count == 0 and NAT_count == 0 and ENT_count == 0:
            return None
        return max(cat_dict.items(), key=operator.itemgetter(1))[0]
    else:
        return None


def isGeo(page):
    if page:
        try:
            coordinates = page.coordinates
            # print('Coor: ', coordinates)
            return True
        except KeyError:
            return False
    else:
        return False

# Word/Sequence of words - > class and link
# Putiing all together
def get_class_link(word): # ADD A PARAMETR POS TAG

    # HERE WE SHOULD USE POS TAGS OF INPUT WORD




    # Returns WikipediaPage object, link or None
    page, link = get_page_link(word)

    # Not using it now, maybe later
    # is_geo = isGeo(page)
    # if is_geo:
    #     print('Place!')

    # Returns a class - one of the ['PER', 'CIT', 'COU', 'ANI', 'SPO','ORG', 'NAT', 'ENT'] or None
    cat = get_category(page)
    if cat:
        return cat, link









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




# Get the list of classes and the list of links from all files "en.tok.off.pos.ent"
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


# The most important processing
def main_processing(dev_data):
    target = ['VBG', 'NNPS', 'VBN', 'NN', 'NNP', 'JJ', 'NNS', 'VB']
    # Simple work with input file en.tok.off.pos and output en.tok.off.pos.my.ent
    for root, dirs, files in os.walk(dev_data):
        for file in files:
            if file == "en.tok.off.pos":

                file_lines = []
                count = 0

                with open(os.path.join(root, file), 'r') as input_file:  #, open(os.path.join(root, file) + '.ent', 'w') as output_file:

                    for line in input_file:
                        if line != '':
                            # List of all words in line, for example
                            # ['4', '10', '1002', 'United', 'NNP', 'COU', 'https://en.wikipedia.org/wiki/United_States']
                            splitnstrip = [x.strip('\n') for x in line.split(' ')]

                            # Current word
                            word = splitnstrip[3]
                            # Current part of speech tag
                            pos = splitnstrip[4]

                            splitnstrip_plus_number = splitnstrip[:]
                            if pos in target and str(word)[0].isupper():

                                if file_lines != [] and str(file_lines[-1][3][0]).isupper():
                                    splitnstrip_plus_number.append(str(count))
                                else:
                                    count += 1
                                    splitnstrip_plus_number.append(str(count))
                            else:
                                splitnstrip_plus_number.append(None)


                            file_lines.append(splitnstrip_plus_number)


                            #
                            # if is_entity(word, pos):
                            #
                            #     wordclass = get_class(word)  # we need to work on this function
                            #     link = get_link(word)  # we need to work on this function as well
                            #
                            #     if wordclass is not None:
                            #         splitnstrip.append(wordclass)  # class  here
                            #
                            #     if link is not None:
                            #         splitnstrip.append(link)  # link here

                        #     output_file.write(' '.join(splitnstrip) + '\n')
                        # else:
                        #     output_file.write(line)


                # for sublist in file_list:
                #     if sublist[5] is not None:
                #         word = sublist[3]
                #         print(word, get_class_link(word))

                # # Entities
                # max_num = max([int(sublist[5]) for sublist in file_list if sublist[5] is not None])
                # for i in range(0, max_num):
                #     string = ""
                #     for sublist in file_list:
                #         if sublist[5] == str(i):
                #             if string != "":
                #                 ar = " "
                #             else:
                #                 ar = ""
                #             string = string + ar + sublist[3]
                #     if string != '':
                #         print(string)

                # Entities
                max_num = max([int(sublist[5]) for sublist in file_lines if sublist[5] is not None])

                class_link_nums = []
                for i in range(0, max_num):
                    ent_list = []
                    num_list = []
                    for sublist in file_lines:
                        if sublist[5] == str(i):
                            ent_list.append(sublist[3])
                            num_list.append(sublist[2])
                    if ent_list != []:
                        ent_str = ' '.join(ent_list)
                        returned_object = get_class_link(ent_str)
                        if returned_object is not None:
                            current_class, current_link = returned_object

                            # for sublist in file_list:
                            #     if sublist[2] in num_list:

                            class_link_nums.append([current_class, current_link, num_list])

                with open(os.path.join(root, file), 'r') as pos_file, open(os.path.join(root, file) + '.ent', 'w') as ent_file:
                    for f_line in pos_file:
                        if f_line != '':
                            # List of all words in line, for example
                            # ['4', '10', '1002', 'United', 'NNP', 'COU', 'https://en.wikipedia.org/wiki/United_States']
                            splitnstrip = [x.strip('\n') for x in f_line.split(' ')]

                            id_num = splitnstrip[2]
                            # ???

                            for sublist in class_link_nums:
                                cur_class = sublist[0]
                                cur_link = sublist[1]
                                cur_num_list = sublist[2]
                                if id_num in cur_num_list:
                                    splitnstrip.append(cur_class)
                                    splitnstrip.append(cur_link)

                            print(splitnstrip)
                            ent_file.write(' '.join(splitnstrip) + '\n')
                        else:
                            ent_file.write(f_line)

                # for i in range(len(file_lines)):
                #     if file_lines[i] != '':
                #         if file_lines[i][5] is not None:
                #             word = file_lines[i][3]
                #             # pos = file_lines[i][4]
                #             num = file_lines[i][5]
                #             ent_list = []














# Comparision with gold standard
def compare(gold_standard, comp, gold_links, dev_links):

    # # Do not need it actually, but it can be used to get information
    # true_positives = nltk.Counter()
    # false_negatives = nltk.Counter()
    # false_positives = nltk.Counter()
    #
    # for i in labels:
    #     for j in labels:
    #         if i == j:
    #             true_positives[i] += cm[i, j]
    #         else:
    #             false_negatives[i] += cm[i, j]
    #             false_positives[j] += cm[i, j]
    #
    # print("true_positives:", true_positives)
    # print("false_negatives:", false_negatives)
    # print("false_positives:", false_positives)


    conf_matrix = nltk.ConfusionMatrix(gold_standard, comp)

    classidication_rep = classification_report(gold_standard, comp, list(set(gold_standard + comp)))

    correct_num = 0
    for i in range(len(gold_standard)):
        if gold_links[i] == dev_links[i]:
            correct_num += 1
    links_accuracy = correct_num / len(gold_standard)

    return conf_matrix, classidication_rep, links_accuracy



def main():

    # Folders names
    development_data = "development"
    goldstandard_data = "goldstandard"

    # The most important - part that creates output .ent
    # main_processing(development_data)


    # measures.py Preprocessing before the comparision with gold standard - get two lists of classes and links
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

