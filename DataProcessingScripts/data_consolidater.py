# CONSOLIDATE WHOLE DATA IN A SINGLE FILE

import csv

FILES = ['airfrance', 'cell', 'michelle', 'obama', 'palin']
FIELDS = ['tweet', 'number_of_mentions', 'number_of_urls', 'number_of_question_marks', 'number_of_exclaimation_marks', 'number_of_support_words', 'number_of_denial_words', 'number_of_query_words', 'number_of_negation_words', 'classification']
TARGET_PATH = '../Data/consolidated_data.csv'

# OPEN TARGET FILE
target_file = open(TARGET_PATH, 'w', newline='', encoding='utf-8')
target_csv = csv.DictWriter(target_file, FIELDS)
target_csv.writeheader()
count = 0
for file_name in FILES:
    # OPEN SOURCE FILE
    source_path = '../Data/' + file_name + '.csv'
    source_file = open(source_path, 'r', newline='', encoding='utf-8')
    source_csv = csv.reader(source_file, delimiter=',')
    # SKIP HEADERS
    next(source_csv)
    source_csv = list(source_csv)
    source_file.close()

    print("NUMBER OF TWEETS IN {}.csv = {}".format(file_name, len(source_csv)))
    # CONSOLIDATE TWEETS
    for tweet in source_csv:
        obj = {}
        obj['tweet'] = tweet[0]
        obj['number_of_mentions'] = tweet[1]
        obj['number_of_urls'] = tweet[2]
        obj['number_of_question_marks'] = tweet[3]
        obj['number_of_exclaimation_marks'] = tweet[4]
        obj['number_of_support_words'] = tweet[5]
        obj['number_of_denial_words'] = tweet[6]
        obj['number_of_query_words'] = tweet[7]
        obj['number_of_negation_words'] = tweet[8]
        obj['classification'] = tweet[9]
        target_csv.writerow(obj)
        count += 1

    print("NUMBER OF TWEETS IN CONSOLIDATED FILE = {}".format(count))

target_file.close()