import wikipedia
import operator


# print(wikipedia.summary("Paris"))



def read_from_file(txt_file_path):
    with open(txt_file_path, 'r') as f:
        lines = f.read().split('\n')
    return lines


def get_page(word):  # we should definitely add input parameters here

    possible_result = wikipedia.search(word, results=1)
    print("Possible result:", possible_result)

    # Choose the first result
    res = str(possible_result).replace(" ", "_")
    print("res", res)

    # Get a page
    page = None
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

    return page


def category_count(str, list_of_words):
    count = 0
    for word in list_of_words:
        count = count + str.upper().count(word.upper())
    return count


def get_category(page):
    if page:
        categories = page.categories
        categories_str = ' '.join(categories)
        print(page.title, categories_str)
        COU_list = ['countries', 'states of']
        COU_count = category_count(categories_str, COU_list)
        CIT_list = ['cities', 'city', 'town', 'towns']
        CIT_count = category_count(categories_str, CIT_list)
        ANI_list = ['animal', 'animals', 'mammal', 'mammals', 'fish']
        ANI_count = category_count(categories_str, ANI_list)
        PER_list = ['person', 'persons', 'people'] # 'names'
        PER_count = category_count(categories_str, PER_list)
        SPO_list = ['sport', 'sports', 'ball games']
        SPO_count = category_count(categories_str, SPO_list)
        # 'Geography of' NAT - Natural places
        ORG_list = ['organization', 'organization', 'organisations', 'organisation', 'companies', 'company']
        ORG_count = category_count(categories_str, ORG_list)
        NAT_list = ['natural place', 'natural places',  'lake', 'lakes', 'mountain','mountains', 'volcano', 'volcanoes',
                    'river', 'rivers', 'sea',  'seas', 'ocean', 'oceans', 'forest', 'forests', 'waterfall', 'waterfalls']
        NAT_count = category_count(categories_str, NAT_list)
        ENT_list = ['books', 'magazines', 'films', 'songs', 'concerts', 'journals', 'movies', 'newspapers', 'radio', 'literature',
                    'book', 'magazine', 'film', 'song', 'concert', 'journal', 'movie', 'newspaper', 'series']
        ENT_count = category_count(categories_str, ENT_list)
        cat_dict = {'PER': PER_count, 'CIT': CIT_count, "COU": COU_count, 'ANI': ANI_count, 'SPO': SPO_count,
                    'ORG': ORG_count, 'NAT': NAT_count, 'ENT': ENT_count}
        print('COU count: ', COU_count, 'COU')
        print('CIT count: ', CIT_count, 'CIT')
        print('ANI count: ', ANI_count, 'ANI')
        print('PER count: ', PER_count, 'PER')
        print('SPO count: ', SPO_count, 'SPO')
        print('ORG count: ', ORG_count, 'ORG')
        print('NAT count: ', NAT_count, 'NAT')
        print('ENT count: ', ENT_count, 'ENT')
        # if (COU_count > 0) and (CIT_count > 0):
        if COU_count == 0 and CIT_count == 0 and ANI_count == 0 and PER_count == 0 and SPO_count == 0 \
                and ORG_count == 0 and NAT_count ==0 and ENT_count ==0:
            return None
        return max(cat_dict.items(), key=operator.itemgetter(1))[0]


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

interesting_entities = read_from_file('interesting_entities.txt')

for item in interesting_entities:
    page = get_page(item)
    cat = get_category(page)
    print('Cat: ', cat)

    is_geo = isGeo(page)
    if is_geo:
        print('Place!')
    print()

    # sections
    # List of section titles from the table of contents on the page.