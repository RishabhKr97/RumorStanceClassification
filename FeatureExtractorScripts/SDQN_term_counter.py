# FIND COUNT OF SUPPORT, DENIAL, QUERY AND NEGATION WORDS

import csv

SUPPORT_WORDS = ['true', 'exactly', 'yes', 'indeed', 'omg', 'know', 'agree', 'perfect', 'yeah']
DENIAL_WORDS = ['not', 'no', 'nobody', 'nothing', 'none', 'never', 'neither', 'nor', 'nowhere', 'hardly', 'scarcely', 'barely', 'impossible', 'false', 'shut', 'rumors', 'rumor']
QUERY_WORDS = ['would', 'doesnt', 'do', "hadn't", 'dont', "shouldn't", 'wouldnt', 'have', "who's", "haven't", "don't", 'has', 'will', 'why', 'shouldnt', 'can', 'Is', 'did', "aren't", "doesn't", 'isnt', 'what', 'does', "hasn't", "wasn't", 'when', 'how', 'are', "wouldn't", 'may', "where's", "why's", 'could', "what's", "couldn't", 'couldnt', "isn't", 'wasnt', "weren't", 'where']


FILES = ['airfrance', 'cell', 'michelle', 'obama', 'palin']
FIELDS = ['tweet', 'number_of_mentions', 'number_of_urls', 'number_of_question_marks', 'number_of_exclaimation_marks', 'number_of_support_words', 'number_of_denial_words', 'number_of_query_words', 'classification']

for file_name in FILES:
    # OPEN SOURCE FILE AND TARGET FILE
    source_path = '../Data/' + file_name + '.csv'
    target_path = '../Data/' + file_name + '.csv'
    source_file = open(source_path, 'r', newline='', encoding='utf-8')
    source_csv = csv.reader(source_file, delimiter=',')
    # SKIP HEADERS
    next(source_csv)
    source_csv = list(source_csv)
    source_file.close()
    target_file = open(target_path, 'w', newline='', encoding='utf-8')
    target_csv = csv.DictWriter(target_file, FIELDS)
    target_csv.writeheader()

    print("NUMBER OF TWEETS IN {}.csv = {}".format(file_name, len(source_csv)))
    # ADD COUNTS AS COLUMNS
    count = 0
    for tweet in source_csv:
        obj = {}
        obj['tweet'] = tweet[0]
        obj['number_of_mentions'] = tweet[1]
        obj['number_of_urls'] = tweet[2]
        obj['number_of_question_marks'] = tweet[3]
        obj['number_of_exclaimation_marks'] = tweet[4]
        obj['number_of_support_words'] = len([w for w in tweet[0].split() if w.lower() in SUPPORT_WORDS])
        obj['number_of_denial_words'] = len([w for w in tweet[0].split() if w.lower() in DENIAL_WORDS])
        obj['number_of_query_words'] = len([w for w in tweet[0].split() if (w.lower() in QUERY_WORDS or w == "Is")])
        obj['classification'] = tweet[5]
        target_csv.writerow(obj)
        count += 1

    print("NUMBER OF TWEETS IN OUTPUT {}.csv = {}".format(file_name, len(source_csv)))
    target_file.close()