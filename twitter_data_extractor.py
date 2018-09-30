# SCRAPE TWITTER FOR TWEET TEXT

from bs4 import BeautifulSoup
import csv
import os
import re
import requests
import time

SOURCEFILE = 'cell-ids.txt'

SOURCEPATH = 'Data/' + SOURCEFILE
TARGETPATH = 'Data/' + SOURCEFILE[:-3] + 'csv'
FIELDS = ['tweet_id', 'username', 'timestamp', 'tweet', 'classification']

# OPEN SOURCE FILE AND TARGET FILE
source_file = open(SOURCEPATH, 'r', newline='', encoding='utf-8')
source_csv = csv.reader(source_file, delimiter='\t')
source_csv = list(source_csv)
source_index = -1
source_file.close()
target_file = open(TARGETPATH, 'a', newline='', encoding='utf-8')

# DETERMINE WHERE TO START IF RESUMING SCRIPT
if os.stat(TARGETPATH).st_size == 0:
    # OPEN FILE IN APPEND MODE AND WRITE HEADERS TO FILE
    last_tweet_id = None
    target_csv = csv.DictWriter(target_file, FIELDS)
    target_csv.writeheader()
else:
    # FIRST EXTRACT LAST MESSAGE ID THEN OPEN FILE IN APPEND MODE WITHOUT WRITING HEADERS
    target_file = open(TARGETPATH, 'r', newline='', encoding='utf-8')
    target_csv = csv.DictReader((line.replace('\0', '') for line in target_file))
    data = list(target_csv)
    data = data[-1]
    last_tweet_id = data['tweet_id']
    # UPDATE SOURCE INDEX
    for i in range(len(source_csv)):
        if source_csv[i][0] == last_tweet_id:
            source_index = i
            break
    target_file.close()
    target_file = open(TARGETPATH, 'a', newline='', encoding='utf-8')
    target_csv = csv.DictWriter(target_file, FIELDS)

# DATA EXTRACTION
twitter_url = "https://twitter.com/xxx/status/"
tweet_hits = 0
while source_index < len(source_csv):
    source_index += 1
    # DELAY TO PREVENT IP BLACKLISTING
    time.sleep(1)

    tweet_id = source_csv[source_index][0]
    classification = source_csv[source_index][1]

    # GET WEBPAGE AND PARSE TITLE AND TIMESTAMP
    response = requests.get(twitter_url+tweet_id)
    if response.status_code != 200:
        continue
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find("title").text
    timestamp = soup.find("span", {'data-time':True})['data-time']

    # PARSE TWEET AND USERNAME
    p = re.compile(r'(.*) on Twitter: "(.*)"')
    p = p.match(title)
    if not p:
        continue
    username = p.group(1)
    tweet = p.group(2)

    # WRITE TO FILE
    obj = {}
    obj['tweet_id'] = tweet_id
    obj['username'] = username
    obj['timestamp'] = timestamp
    obj['tweet'] = tweet
    obj['classification'] = classification
    target_csv.writerow(obj)
    target_file.flush()

    tweet_hits += 1
    print("tweet_hits = {}".format(tweet_hits))

target_file.close()
