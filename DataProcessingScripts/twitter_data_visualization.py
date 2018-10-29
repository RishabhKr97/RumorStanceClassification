# DATA STATS AND VISUALIZATION

import csv
import itertools
import numpy as np
import matplotlib.pyplot as plt
import re
from collections import Counter
from matplotlib.ticker import FuncFormatter

'''
    VISUALIZE USING
    1) Histogram of number of words for each classification
    2) Bar graph between classification and number of tweets
    3) Words with highest frequency
'''

FILES = ['airfrance', 'cell', 'michelle', 'obama', 'palin']
COLORS = itertools.cycle(['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan'])
CLASSIFICATION = ['Support', 'Deny', 'Query', 'Comment']

def main():
    choice = int(input("""
    1) ENTER 1 FOR HISTOGRAM OF WORD COUNT IN TWEET FOR EACH CLASSIFICATION.
    2) ENTER 2 FOR BAR GRAPH OF CLASSIFICATION VS NUMBER OF TWEETS.
    3) ENTER 3 FOR PIE CHART OF HIGHEST WORD FREQUENCY FOR EACH CLASSIFICATION.
    4) ENTER 4 FOR HISTOGRAM OF TWEET WORD-NUMBER FEATURES FOR EACH CLASSIFICATION.
    5) ENTER 5 FOR ALL OVERALL STATS.
    """))

    if choice == 1:
        histogram()
    elif choice == 2:
        bar_graph()
    elif choice == 3:
        word_frequency()
    elif choice == 4:
        word_number_feature()
    elif choice == 5:
        histogram(overall_only=True)
        bar_graph(overall_only=True)
        word_frequency(overall_only=True)
        word_number_feature(overall_only=True)
    else:
        print("WRONG CHOICE!!")
        exit()

# HISTOGRAM OF TWEET LENGTH FOR EACH CLASSIFICATION IN EACH FILE AND OVERALL DATASET
def histogram(overall_only=False):
    # UTILITY FUNCTION FOR HISTOGRAM
    def to_percent(y, position):
        s = str(round(500*y,2))
        return s + '%'
    formatter = FuncFormatter(to_percent)

    overall_numbers = [[] for _ in range(4)]
    for file_name in FILES:
        source_path = '../Data/' + file_name + '.csv'
        source_file = open(source_path, 'r', newline='', encoding='utf-8')
        source_csv = csv.reader(source_file, delimiter=',')
        # SKIP HEADERS
        next(source_csv)

        numbers = [[] for _ in range(4)]
        for tweet in source_csv:
            numbers[int(tweet[9])-1].append(len(re.findall(r'\w+', tweet[0])))

        for i in range(4):
            overall_numbers[i] += numbers[i]
            if not overall_only:
                plt.hist(numbers[i], bins=np.arange(0,31,5), color=next(COLORS), label=CLASSIFICATION[i], alpha=0.5, density=True)
                plt.legend(loc='upper left')
                plt.title(file_name)
                plt.xlabel("tweet length")
                plt.ylabel("percentage of tweets (total = {})".format(len(numbers[i])))
                plt.gca().yaxis.set_major_formatter(formatter)
                plt.show()

        source_file.close()

    for i in range(4):
        plt.hist(overall_numbers[i], bins=np.arange(0,31,5), color=next(COLORS), label=CLASSIFICATION[i], alpha=0.5, density=True)
        plt.legend(loc='upper left')
        plt.title("Overall Dataset")
        plt.xlabel("tweet length")
        plt.ylabel("percentage of tweets (total = {})".format(len(overall_numbers[i])))
        plt.gca().yaxis.set_major_formatter(formatter)
        plt.show()

# BAR GRAPH BETWEEN CLASSIFICATION AND NUMBER OF TWEETS IN EACH FILE AND OVERALL DATASET
def bar_graph(overall_only=False):
    overall_numbers = [0]*4
    for file_name in FILES:
        source_path = '../Data/' + file_name + '.csv'
        source_file = open(source_path, 'r', newline='', encoding='utf-8')
        source_csv = csv.reader(source_file, delimiter=',')
        # SKIP HEADERS
        next(source_csv)

        numbers = [0]*4
        for tweet in source_csv:
            numbers[int(tweet[9])-1] += 1
        for j in range(4):
            overall_numbers[j] += numbers[j]
        if not overall_only:
            plt.bar(np.arange(5), numbers)
            plt.title(file_name)
            plt.xlabel("classification")
            plt.ylabel("number of tweets")
            plt.xticks(np.arange(4), CLASSIFICATION, rotation=30)
            plt.show()

        source_file.close()


    plt.bar(np.arange(4), overall_numbers)
    plt.title("Overall Dataset")
    plt.xlabel("classification")
    plt.ylabel("number of tweets")
    plt.xticks(np.arange(4), CLASSIFICATION, rotation=30)
    plt.show()

# PIE CHART OF WORDS WITH HIGHEST FREQUENCY IN EACH CLASS IN EACH FILE AND OVERALL DATASET
def word_frequency(overall_only=False):
    TOP_N = 20
    overall_words = [{}, {}, {}, {}]
    for file_name in FILES:
        source_path = '../Data/' + file_name + '.csv'
        source_file = open(source_path, 'r', newline='', encoding='utf-8')
        source_csv = csv.reader(source_file, delimiter=',')
        # SKIP HEADERS
        next(source_csv)

        words = [{}, {}, {}, {}]
        for tweet in source_csv:
            for word in tweet[0].split():
                if word not in words[int(tweet[9])-1]:
                    words[int(tweet[9])-1][word] = 1
                else:
                    words[int(tweet[9])-1][word] += 1

                if word not in overall_words[int(tweet[9])-1]:
                    overall_words[int(tweet[9])-1][word] = 1
                else:
                    overall_words[int(tweet[9])-1][word] += 1

        if not overall_only:
            for i in range(4):
                top_n = min(TOP_N, len(words[i]))
                stat_list = Counter(words[i]).most_common(top_n)
                word = []
                count = []
                for j in range(top_n):
                    word.append(stat_list[j][0])
                    count.append(stat_list[j][1])

                plt.pie(count, labels=word, colors=COLORS, counterclock=False, startangle=90)
                plt.title(file_name + " : " + CLASSIFICATION[i])
                plt.show()

    for i in range(4):
        top_n = min(TOP_N, len(words[i]))
        stat_list = Counter(overall_words[i]).most_common(top_n)
        word = []
        count = []
        for j in range(top_n):
            word.append(stat_list[j][0])
            count.append(stat_list[j][1])

        plt.pie(count, labels=word, colors=COLORS, counterclock=False, startangle=90)
        plt.title("OVERALL DATASET : " + CLASSIFICATION[i])
        plt.show()

# HISTOGRAM OF TWEET WORD-NUMBER FEATURE FOR EACH CLASS IN OVERALL DATASET
def word_number_feature(overall_only=True):
    # UTILITY FUNCTION FOR HISTOGRAM
    def to_percent(y, position):
        s = str(round(100*y,2))
        return s + '%'
    formatter = FuncFormatter(to_percent)

    labels = ['Number of mentions', 'Number of urls', 'Number of question marks', 'Number of exclaimation marks', 'Number of support words', 'Number of denial words', 'Number of query words', 'Number of negation words']
    overall_numbers = [[[] for __ in range(4)] for _ in range(len(labels))]
    for file_name in FILES:
        source_path = '../Data/' + file_name + '.csv'
        source_file = open(source_path, 'r', newline='', encoding='utf-8')
        source_csv = csv.reader(source_file, delimiter=',')
        # SKIP HEADERS
        next(source_csv)

        numbers = [[[] for __ in range(4)] for _ in range(len(labels))]
        for tweet in source_csv:
            for i in range(len(labels)):
                numbers[i][int(tweet[9])-1].append(int(tweet[i+1]))

        for i in range(len(labels)):
            for j in range(4):
                overall_numbers[i][j] += numbers[i][j]
                if not overall_only:
                    plt.hist(numbers[i][j], bins=np.arange(min(numbers[i][j]), max(numbers[i][j]) + 1, 1), color=next(COLORS), label=CLASSIFICATION[j], alpha=0.5, rwidth=0.5, align='left', density=True)
                    plt.legend(loc='upper right')
                    plt.title(file_name)
                    plt.xlabel(labels[i])
                    plt.ylabel("percentage of tweets (total = {})".format(len(numbers[i][j])))
                    plt.gca().yaxis.set_major_formatter(formatter)
                    plt.show()

        source_file.close()

    for i in range(len(labels)):
        for j in range(4):
            plt.hist(overall_numbers[i][j], bins=np.arange(min(overall_numbers[i][j]), max(overall_numbers[i][j]) + 1, 1), color=next(COLORS), label=CLASSIFICATION[j], alpha=0.5, rwidth=0.5, align='left', density=True)
            plt.legend(loc='upper right')
            plt.title("Overall Dataset")
            plt.xlabel(labels[i])
            plt.ylabel("percentage of tweets (total = {})".format(len(overall_numbers[i][j])))
            plt.gca().yaxis.set_major_formatter(formatter)
            plt.show()

main()