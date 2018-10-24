# REMOVE DUPLICATE TWEETS FROM DATA
import csv

FILES = ['airfrance', 'cell', 'michelle', 'obama', 'palin']
FIELDS = ['tweet', 'number_of_mentions', 'number_of_urls', 'number_of_question_marks', 'number_of_exclaimation_marks', 'classification']

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
    unique_tweets = set()
    # CONSTRUCT UNIQUE OBJECT AND SAVE TO CSV
    for tweet in source_csv:
        if tweet[0] not in unique_tweets:
            obj = {}
            obj['tweet'] = tweet[0]
            obj['number_of_mentions'] = tweet[1]
            obj['number_of_urls'] = tweet[2]
            obj['number_of_question_marks'] = tweet[3]
            obj['number_of_exclaimation_marks'] = tweet[4]
            obj['classification'] = tweet[5]
            target_csv.writerow(obj)
            unique_tweets.add(obj['tweet'])
            count += 1

    print("NUMBER OF TWEETS IN OUTPUT {}.csv = {}".format(file_name, count))
    target_file.close()