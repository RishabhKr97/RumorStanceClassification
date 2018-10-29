# FIND COUNT OF SUPPORT, DENIAL, QUERY AND NEGATION WORDS

import csv

SUPPORT_WORDS = ['true', 'exactly', 'yes', 'indeed', 'omg', 'know']
DENIAL_WORDS = ['not true', 'don\'t agree','dont agree', 'impossible', 'false', 'shut', 'rumors', 'Rumor']
QUERY_WORDS = ['what', 'why', 'how', 'when', 'where', 'did', 'do', 'does', 'have', 'has', 'Is', 'Are', 'Can', 'could', 'may', 'would', 'will']
NEGATION_WORDS =  ['not', 'no', 'nobody', 'nothing', 'none', 'never', 'neither', 'nor', 'nowhere', 'hardly', 'scarcely', 'barely', 'don\'t', 'isn\'t', 'wasn\'t', 'shouldn\'t', 'wouldn\'t', 'couldn\'t', 'doesn\'t', 'dont', 'isnt', 'wasnt', 'shouldnt', 'wouldnt', 'couldnt', 'doesnt']

FILES = ['airfrance', 'cell', 'michelle', 'obama', 'palin']
FIELDS = ['tweet', 'number_of_mentions', 'number_of_urls', 'number_of_question_marks', 'number_of_exclaimation_marks', 'number_of_support_words', 'number_of_denial_words', 'number_of_query_words', 'number_of_negation_words', 'classification']

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
    count = 0
    # ADD COUNTS AS COLUMNS
    for tweet in source_csv:
        obj = {}
        obj['tweet'] = tweet[0]
        obj['number_of_mentions'] = tweet[1]
        obj['number_of_urls'] = tweet[2]
        obj['number_of_question_marks'] = tweet[3]
        obj['number_of_exclaimation_marks'] = tweet[4]
        obj['number_of_support_words'] = len([w for w in tweet[0].split() if w in SUPPORT_WORDS])
        obj['number_of_denial_words'] = len([w for w in tweet[0].split() if w in DENIAL_WORDS])
        obj['number_of_query_words'] = len([w for w in tweet[0].split() if w in QUERY_WORDS])
        obj['number_of_negation_words'] = len([w for w in tweet[0].split() if w in NEGATION_WORDS])
        obj['classification'] = tweet[5]
        target_csv.writerow(obj)
        count += 1

    print("NUMBER OF TWEETS IN OUTPUT {}.csv = {}".format(file_name, count))
    target_file.close()