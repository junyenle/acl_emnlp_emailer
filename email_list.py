import os
from glob import glob
FIRSTNAME = 0
LASTNAME = 1
EMAIL = 2

def parse_file(filename, keywords):

    # read file
    ifile = open(filename, "r")
    lines = ifile.read().split('\n')
    
    # find abstract and authors
    abstract = None
    num_authors = 0
    authors = []
    for line in lines:
        # print(line)
        if len(line) >= 12 and line[0:12] == "Abstract#==#":
            abstract = line[12:]
            # print(line)
        if len(line) >= 7 and line[0:7] == "Author{":
            # print(line)
            authornumber = int(line[7])
            if authornumber > num_authors:
                authors.append([None, None, None])
                num_authors += 1
            digits = int(authornumber / 10) + 1
            authornumber -= 1
            if len(line) >= 8 + digits + 11 and line[8 + digits: 8 + digits + 11] == "{Firstname}":
                authors[authornumber][FIRSTNAME] = line[8 + digits + 11 + 5:]
            if len(line) >= 8 + digits + 10 and line[8 + digits: 8 + digits + 10] == "{Lastname}":
                authors[authornumber][LASTNAME] = line[8 + digits + 10 + 5:]       
            if len(line) >= 8 + digits + 7 and line[8 + digits: 8 + digits + 7] == "{Email}":
                authors[authornumber][EMAIL] = line[8 + digits + 7 + 5:]
    if abstract == None or len(authors) == 0:
        print("bad data")
        return False, []

    # search for keywords
    has_keyword = False
    for keyword in keywords:
        if abstract.find(keyword) != -1:
            has_keyword = True
            # print(keywords)
            # print(abstract)
            # print(authors)
            break
    return has_keyword, authors
    
keyword_lists = []
keyword_list_0 = ["morphology", "morphological"]
keyword_list_1 = ["phonology", "phonological"]
keyword_list_2 = ["typology", "typological", "multilingual", "cross-lingual", "low-resource"]
keyword_lists.append(keyword_list_0)
keyword_lists.append(keyword_list_1)
keyword_lists.append(keyword_list_2)


filenames = [y for x in os.walk("./data") for y in glob(os.path.join(x[0], '*.txt'))]
# print(filenames)

for i, keyword_list in enumerate(keyword_lists):
    # open each file
    hit_authors = []
    for filename in filenames:
        hit, authors = parse_file(filename, keyword_list)
        if hit:
            hit_authors = hit_authors + authors
    hit_authors_unique = [t for i, t in enumerate(hit_authors) if not any (t[EMAIL] == p[EMAIL] for p in hit_authors[:i])]
    # print(keyword_list)
    # print(hit_authors)
    print(len(hit_authors_unique))
    ofile = open("list_{}.csv".format(i), "w+")
    for word in keyword_list:
        ofile.write(word + ", ")
    ofile.write('\n')
    for author in hit_authors_unique:
        ofile.write(author[FIRSTNAME] + ',')
        ofile.write(author[LASTNAME] + ',')
        ofile.write(author[EMAIL])
        ofile.write('\n')
