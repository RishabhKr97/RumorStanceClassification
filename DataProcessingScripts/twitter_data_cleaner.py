"""
    1) Rename obama-ids.csv and cell-ids.csv to obama.csv and cell.csv (manually)
    2) Remove tweets with classification 0 and 2
    3) Remove tweet-id, username, timestamp column
    4) Map the classification 11, 12, 13, 14 to 1, 2, 3, 4
    5) Add numbers_of_mentions and number_of_urls column
    6) Remove "RT" and "via" from tweets
    7) Remove urls of http://, https://, www and .com format from tweets (some url anomalies were manually removed)
    8) Remove mentions starting from @
    9) Remove :, (, ), [, ] and |
    10) Remove extra spaces
    11) Remove duplicate tweets (separate script)
"""

import csv
import re

FILES = ['airfrance', 'cell', 'michelle', 'obama', 'palin']
FIELDS = ['tweet', 'number_of_mentions', 'number_of_urls', 'classification']
REG_MENTION = re.compile(r'@\w*')
REG_URL = re.compile(r'https?://.*?(?:$| )|www\.[\w-]+\.\w+.*?(?:$| )|[\w-]*\.com.*?(?:$| )', re.IGNORECASE)
REG_RT_AND_VIA = re.compile(r'\bRT\b|\bvia\b', re.IGNORECASE)
REG_EXTRA_CHARS = re.compile(r'\(|\)|:|\[|\]|\|')
REG_EXTRA_SPACES = re.compile(r'[ ]{2,}')

# TASKS 2-10
for file_name in FILES:
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
    for row in source_csv:
        if row[4] not in ['11','12','13','14']:
            continue
        obj = {}
        obj['tweet'] = row[3]
        obj['number_of_mentions'] = len(REG_MENTION.findall(obj['tweet']))
        obj['number_of_urls'] = len(REG_URL.findall(obj['tweet']))
        obj['classification'] = int(row[4])%10

        obj['tweet'] = re.sub(REG_MENTION, ' ', obj['tweet'])
        obj['tweet'] = re.sub(REG_URL, ' ', obj['tweet'])
        obj['tweet'] = re.sub(REG_RT_AND_VIA, ' ', obj['tweet'])
        obj['tweet'] = re.sub(REG_EXTRA_CHARS, ' ', obj['tweet'])
        obj['tweet'] = re.sub(REG_EXTRA_SPACES, '', obj['tweet'])

        count += 1
        target_csv.writerow(obj)

    print("NUMBER OF TWEETS IN OUTPUT {}.csv = {}".format(file_name, count))
    target_file.close()
