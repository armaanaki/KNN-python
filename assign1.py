#!/usr/bin/python

# Course: CS4267
# Student name: Armaan Esfahani 
# Student ID: 000764818
# Assignment #: #1
# Due Date: September 16, 2019
# Signature: A.E. 
# Score: _________________

# imports for our progam
import csv
import random
import math
import argparse


# method to load data from a dataset and split it data to use and data for  comparison
# compare_set: array used as training data (where the data set comapres against), defaults to a null array if none is set
# data_set: array of data to test against the compare_set (what our program will try to predict), defaults to null array if none is set
# split_amount: the fraction that our data will split into (how much of the data set goes into each array), defaults to 80% if none is set
# filename: File location of dataset to load, defaults to the iris data set if none is set
def load_data(compare_set, data_set, split_amount, filename):
    # open the file in read-only as a csv
    with open(filename, 'r') as csvfile:
        # load the csv into a list
        reader = csv.reader(csvfile)
        data = list(reader)

        # iterate all values from csv
        for index in range(len(data)-1):
            # set all numerical values to floats so they can be manipulated later
            for x in range(len(data[index]) - 1):
                data[index][x] = float(data[index][x])

            # roll a random number, if it is below the split amount add it to compare set, otherwise it goes to the data set
            if random.random() < split_amount:
                compare_set.append(data[index])
            else:
                data_set.append(data[index])

# method to get the distance between two data values 
# point1: one of the points to compare
# point2: the other point to compare
def distance(point1, point2):
    distance = 0

    # iterate through all values of each point and square their differences then add them together
    for x in range(len(point1) - 1):
        distance += pow((point1[x] - point2[x]), 2)

    # return the complete formula
    return math.sqrt(distance)

# method to guess the type based on k nearest neighbors
# compare_set: array used as training data (where the data set comapres against), defaults to a null array if none is set
# data_point: point to guess the value of 
# k: the amount of neighbors to search for
def guess_type(compare_set, data_point, k):
    # init variables that will be used
    distances = []
    neighbors = []
    type_votes = {}

    # get the distances between the current guess_point and all points in the compare_set
    for compare_point in compare_set:
        distances.append((compare_point, distance(data_point, compare_point)))

    # sort the array by distance
    distances.sort(key=lambda x:float(x[1]))

    # add the top k neighbors to a neighbors array
    for x in range(k):
        neighbors.append(distances[x][0])


    # add up the total of each type
    for neighbor in neighbors:
        if neighbor[-1] in type_votes:
            type_votes[neighbor[-1]] += 1
        else:
            type_votes[neighbor[-1]] = 1

    return sorted(type_votes.iteritems(), key=lambda x:int(x[1]))[-1][0]

# main function that holds the logic for printing guesses and accuracy
def main(k, filename, split):
    # variables used throughout function
    compare_set = []
    data_set = []
    correct = 0
    incorrect = 0

    # load data into our variables
    load_data(compare_set, data_set, split, filename)

    # iterate through each point in the data set and make a guess
    for data_point in data_set:
        point_guess = guess_type(compare_set, data_point , k)
        print("Point: " + str(data_point) + "\tGuess: " + point_guess)
        if point_guess == data_point[-1]:
            correct += 1
        else:
            incorrect += 1
    print("---------------------------------")

    # print total accuracy
    print("Correct Guesses: " + str(correct))
    print("Incorrect Guesses: " + str(incorrect))
    print("Accuracy: " + str(round(float(correct)/(correct+incorrect) * 100, 2)) + "%")


# parser arguments to make running the program easier
parser = argparse.ArgumentParser()
parser.add_argument("-k", "--kvalue", help="the value you wish to set k to (defaults to 3)")
parser.add_argument("-f", "--filename", help="the location of the data file (defaults to iris.data)")
parser.add_argument("-s", "--split", help="the amount of the dataset to be split into training data (the rest is used as guessing points, defaults to 0.8)")
args = parser.parse_args()

# use k if k was provided, if less than 1 exit
if args.kvalue:
    k = int(args.kvalue)
    if k < 1:
        print("k value may not be less than 1!")
        exit(1)
else:
    k = 3

# use filename if filename was provided
if args.filename:
    filename = args.filename
else:
    filename = "iris.data"

# use split if split was provided, exit if it does not fall between 1 and 0
if args.split:
    split = float(args.split)
    if split <= 0:
        print("split may not be 0 or less!")
        exit(1)
    if split >= 1:
        print("split may not be 1 or more!")
        exit(1)
else:
    split = 0.8

main(k, filename, split)
