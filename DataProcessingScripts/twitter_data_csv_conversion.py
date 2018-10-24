# CONVERT TXT DATASET TO CSV

from datetime import datetime
import csv

# CHANGE ONLY SOURCEFILE
SOURCEFILE = 'palin.txt'

SOURCEPATH = '../Data/' + SOURCEFILE
TARGETPATH = '../Data/' + SOURCEFILE[:-3] + 'csv'
FIELDS = ['tweet_id', 'username', 'timestamp', 'tweet', 'classification']

# OPEN SOURCE FILE AND TARGET FILE
source_file = open(SOURCEPATH, 'r', newline='', encoding='utf-8', errors='ignore')
source_csv = csv.reader(source_file, delimiter='\t')
source_csv = list(source_csv)
source_index = 0
source_file.close()
target_file = open(TARGETPATH, 'w', newline='', encoding='utf-8')
target_csv = csv.DictWriter(target_file, FIELDS)
target_csv.writeheader()


# CONSTRUCT OBJECT AND SAVE TO CSV
while source_index < len(source_csv):
    obj = {}
    obj['tweet_id'] = None
    obj['username'] = source_csv[source_index][1]
    obj['timestamp'] = int((datetime.strptime(source_csv[source_index][0], '%Y-%m-%d %H:%M:%S') - datetime(1970,1,1)).total_seconds())
    obj['tweet'] = source_csv[source_index][2]
    obj['classification'] = source_csv[source_index][3]

    target_csv.writerow(obj)
    source_index += 1

target_file.close()