# Importing necessary libraries
import csv
from collections import defaultdict, Counter
from email.policy import default
import pandas as pd
from itertools import combinations
from matplotlib import pyplot as plt

# Reading movie data from CSV
moviesCSV = open("movies.csv", "r", encoding="utf8")
moviesRows = []
moviesFields = []
moviesReader = csv.reader(moviesCSV)
moviesFields = next(moviesReader)
for row in moviesReader:
    moviesRows.append(row)

# Reading ratings data from CSV
ratingsCSV = open("ratings.csv", "r", encoding="utf8")
ratingsRows = []
ratingsFields = []
ratingsReader = csv.reader(ratingsCSV)
ratingsFields = next(ratingsReader)
for row in ratingsReader:
    ratingsRows.append(row)

# Reading links data from CSV
linksCSV = open("links.csv", "r", encoding="utf8")
linksRows = []
linksFields = []
linksReader = csv.reader(linksCSV)
linksFields = next(linksReader)
for row in linksReader:
    linksRows.append(row)

# Reading tags data from CSV
tagsCSV = open("tags.csv", "r", encoding="utf8")
tagsRows = []
tagsFields = []
tagsReader = csv.reader(tagsCSV)
tagsFields = next(tagsReader)
for row in tagsReader:
    tagsRows.append(row)

# Function to convert movie ID to movie name
def idToMovieName(movieID):
    for movieRow in moviesRows:
        if movieRow[0] == movieID:
            return " ".join(movieRow[1].split(" ")[:-1])

# Filtering ratings data with ratings greater than 2
ratingsTDSDict = defaultdict(list)
for rating in ratingsRows:
    if float(rating[2]) > 2:
        ratingsTDSDict[rating[0]].append(idToMovieName(rating[1]))

# Removing users who rated fewer than 10 movies
fewerThan10 = []
for key, value in ratingsTDSDict.items():
    if len(value) <= 10:
        fewerThan10.append(key)
for key in fewerThan10:
    del ratingsTDSDict[key]

# Splitting data into training and test sets
ratingsTrainingSet = {}
ratingsTestSet = {}
for key, value in ratingsTDSDict.items():
    xrange = int(len(value) * 0.8)
    ratingsTrainingSet[key] = value[0:xrange]
    ratingsTestSet[key] = value[xrange:-1]

# Creating initial list of unique movies
data = []
for key, value in ratingsTrainingSet.items():
    data.append([key, value])
init = []
for i in data:
    for q in i[1]:
        if q not in init:
            init.append(q)
init = sorted(init)

# Setting minimum support and calculating support count
min_support = 0.0148
support = int(min_support * len(init))

# Initializing counters for current and next levels
current_counter = defaultdict(int)
for i in init:
    for d in data:
        if i in d[1]:
            current_counter[i] += 1

# Displaying current 1-itemsets
# print("Current 1:")
# for i in current_counter:
#     print(str([i]) + ": " + str(current_counter[i]))

# Generating next level 1-itemsets based on minimum support
next_counter = defaultdict(int)
for i in current_counter:
    if current_counter[i] >= support:
        next_counter[frozenset([i])] += current_counter[i]

# Displaying next level 1-itemsets
# print("Level (Next) 1:")
# for i in next_counter:
#     print(str(list(i)) + ": " + str(next_counter[i]))
# print()

# Initializing variables for current and final remaining itemsets
current_remaining = next_counter
final_remaining = 1

# Iterating through levels 2 to 6 for Apriori algorithm
for count in range(2, 7):
    # Generating candidate itemsets for the current level
    nc = set()
    temp = list(next_counter)
    for i in range(0, len(temp)):
        for j in range(i + 1, len(temp)):
            t = temp[i].union(temp[j])
            if len(t) == count:
                nc.add(temp[i].union(temp[j]))
    nc = list(nc)

    # Counting occurrences of candidate itemsets in the data
    current_counter = defaultdict(int)
    for i in nc:
        current_counter[i] = 0
        for q in data:
            temp = set(q[1])
            if i.issubset(temp):
                current_counter[i] += 1
    # Displaying current itemsets and counts
    # print("Current " + str(count) + ":")
    # for i in current_counter:
    #     print(str(list(i)) + ": " + str(current_counter[i]))
    # print()

    # Generating next level itemsets based on minimum support
    next_counter = defaultdict(int)
    for i in current_counter:
        if current_counter[i] >= support:
            next_counter[i] += current_counter[i]
    # Breaking if no frequent itemsets found in the next level
    if len(next_counter) == 0:
        break
    # Displaying next level itemsets and counts
    # print("Level (Next) " + str(count) + ":")
    # for i in next_counter:
    #     print(str(list(i)) + ": " + str(next_counter[i]))
    # print()

    current_remaining = next_counter
    final_remaining = count

# Displaying final result with remaining itemsets and counts
print("Result: ")
print("Level (Next) " + str(final_remaining) + ":")
for i in current_remaining:
    print(str(list(i)) + ": " + str(current_remaining[i]))
print()

# Initializing lists to store association rules based on confidence percentages
conf_100 = []
conf_no = []
conf_all = []

# Calculating association rules and storing them in respective lists
for next_counter in current_remaining:
    current_counter = [frozenset(q) for q in combinations(next_counter, len(next_counter) - 1)]
    mmax = 0
    for movie in current_counter:
        without_movie = next_counter - movie
        movie_counter = next_counter
        total_percentage = 0
        singular_percentage = 0
        plural_percentage = 0
        for q in data:
            temp = set(q[1])
            if movie.issubset(temp):
                singular_percentage += 1
            if without_movie.issubset(temp):
                plural_percentage += 1
            if movie_counter.issubset(temp):
                total_percentage += 1
        # Calculating and displaying association rule confidence percentages
        temp = total_percentage / singular_percentage * 100
        if temp > mmax:
            mmax = temp
        temp = total_percentage / plural_percentage * 100
        if temp > mmax:
            mmax = temp
        print(str(list(without_movie)) + " -> " + str(list(movie)) + " = " + str(
            total_percentage / plural_percentage * 100) + "%")
        listString = [without_movie, list(movie), total_percentage / plural_percentage * 100]
        conf_all.append(listString)
        if float(listString[-1]) > 35:
            conf_100.append(listString)
        else:
            conf_no.append(listString)
    curr = 1
    for movie in current_counter:
        without_movie = next_counter - movie
        movie_counter = next_counter
        total_percentage = 0
        singular_percentage = 0
        plural_percentage = 0
        for q in data:
            temp = set(q[1])
            if movie.issubset(temp):
                singular_percentage += 1
            if without_movie.issubset(temp):
                plural_percentage += 1
            if movie_counter.issubset(temp):
                total_percentage += 1
        temp = total_percentage / singular_percentage * 100
        curr += 1
        temp = total_percentage / plural_percentage * 100
        curr += 1
    print("\n")
