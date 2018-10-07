# DATA STATS AND VISUALIZATION

import csv
import itertools
import numpy as np
import matplotlib.pyplot as plt
import re

'''
    VISUALIZE USING
    1) Histogram of number of words for each classification
    2) Bar graph between classification and number of tweets
'''

FILES = ['airfrance', 'cell', 'michelle', 'obama', 'palin']
COLORS = itertools.cycle(['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan'])
CLASSIFICATION = ['Support', 'Deny', 'Query', 'Comment']

def main():
    choice = int(input("""
    1) ENTER 1 FOR HISTOGRAM OF WORD COUNT IN TWEET FOR EACH CLASSIFICATION.
    2) ENTER 2 FOR BAR GRAPH OF CLASSIFICATION VS NUMBER OF TWEETS.
    3) ENTER 3 FOR BOTH.
    4) ENTER 4 FOR OVERALL STATS ONLY.
    """))

    if choice == 1:
        histogram()
    elif choice == 2:
        bar_graph()
    elif choice == 3:
        histogram()
        bar_graph()
    elif choice == 4:
        histogram(overall_only = True)
        bar_graph(overall_only = True)
    else:
        print("WRONG CHOICE!!")
        exit()

# HISTOGRAM OF TWEET LENGTH FOR EACH CLASSIFICATION IN EANCH FILE AND OVERALL DATASET
def histogram(overall_only = False):
    overall_numbers = [[] for _ in range(4)]
    for file_name in FILES:
        source_path = '../Data/' + file_name + '.csv'
        source_file = open(source_path, 'r', newline='', encoding='utf-8')
        source_csv = csv.reader(source_file, delimiter=',')
        # SKIP HEADERS
        next(source_csv)

        numbers = [[] for _ in range(4)]
        for tweet in source_csv:
            numbers[int(tweet[3])-1].append(len(re.findall(r'\w+', tweet[0])))

        for i in range(4):
            overall_numbers[i] += numbers[i]
            if not overall_only:
                plt.hist(numbers[i], bins=np.arange(0,31,5), color=next(COLORS), label=CLASSIFICATION[i], alpha=0.5)
                plt.legend(loc='upper left')
                plt.title(file_name)
                plt.xlabel("tweet length")
                plt.ylabel("number of tweets")
                plt.show()

        source_file.close()

    for i in range(4):
        plt.hist(overall_numbers[i], bins=np.arange(0,31,5), color=next(COLORS), label=CLASSIFICATION[i], alpha=0.5)
        plt.legend(loc='upper left')
        plt.title("Overall Dataset")
        plt.xlabel("tweet length")
        plt.ylabel("number of tweets")
        plt.show()

# BAR GRAPH BETWEEN CLASSIFICATION AND NUMBER OF TWEETS IN EACH FILE AND OVERALL DATASET
def bar_graph(overall_only = False):
    overall_numbers = [0]*4
    for file_name in FILES:
        source_path = '../Data/' + file_name + '.csv'
        source_file = open(source_path, 'r', newline='', encoding='utf-8')
        source_csv = csv.reader(source_file, delimiter=',')
        # SKIP HEADERS
        next(source_csv)

        numbers = [0]*4
        for tweet in source_csv:
            numbers[int(tweet[3])-1] += 1
        for j in range(4):
            overall_numbers[j] += numbers[j]
        if not overall_only:
            plt.bar(np.arange(4), numbers)
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

main()