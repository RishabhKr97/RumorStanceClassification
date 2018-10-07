# REMOVE DUPLICATE TWEETS FROM DATA
import csv

# CHANGE ONLY SOURCEFILE
SOURCEFILE = 'airfrance.csv'

SOURCEPATH = 'Data/' + SOURCEFILE
TARGETPATH = 'Data/' + SOURCEFILE[:-3] + 'csv'
# FIELDS = ['username', 'timestamp', 'tweet', 'presenceOfMention', 'presenceOfUrl', 'classification']
FIELDS = ['tweet', 'presenceOfMention', 'presenceOfUrl', 'classification']

# OPEN SOURCE FILE AND TARGET FILE
source_file = open(SOURCEPATH, 'r', newline='', encoding='utf-8', errors='ignore')
source_csv = csv.reader(source_file, delimiter=',')
source_csv = list(source_csv)
source_index = 0
source_file.close()
target_file = open(TARGETPATH, 'w', newline='', encoding='utf-8')
target_csv = csv.DictWriter(target_file, FIELDS)

print("LENGTH BEFORE: {}".format(len(source_csv)))
total = 0
unique_tweets = set()
# CONSTRUCT UNIQUE OBJECT AND SAVE TO CSV
while source_index < len(source_csv):
    if source_csv[source_index][2] not in unique_tweets:
        obj = {}
        # obj['username'] = source_csv[source_index][0]
        # obj['timestamp'] = source_csv[source_index][1]
        obj['tweet'] = source_csv[source_index][2]
        obj['classification'] = source_csv[source_index][3]
        obj['presenceOfMention'] = source_csv[source_index][4]
        obj['presenceOfUrl'] = source_csv[source_index][5]
        target_csv.writerow(obj)
        unique_tweets.add(obj['tweet'])
        total += 1
    source_index += 1

print("LENGTH AFTER: {}".format(total))
target_file.close()