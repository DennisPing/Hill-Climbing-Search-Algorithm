#!/usr/bin/env python3
# coding=utf-8

import os
import sys

class IOManager:
    """
    A class to manage user input and file output.
    Supports quit functionality.
    """

    def __init__(self):
        self.cwd = os.getcwd()

    def prompt_input(self):
        print("Type 'q' or 'quit' anytime to quit.")
        prompts = []
        prompts.append(self.get_filename())
        prompts.append(self.get_iterations())
        prompts.append(self.get_rounds())
        answers = []
        for each in prompts:
            answers.append(each)
        return answers[0], answers[1], answers[2]
    
    def check_quit(self, userinput):
        if userinput.lower() == 'q' or userinput.lower() == 'quit':
            sys.exit()
        return
    
    def get_filename(self):
        file1 = f"{self.cwd}/49_cities.txt"
        file2 = f"{self.cwd}/cities_full.txt"
        if not os.path.exists(file1):
            raise FileNotFoundError("49_cities.txt is missing in current folder.")
        if not os.path.exists(file2):
            raise FileNotFoundError("cities_full.txt is missing in current folder.")
        options = {
            '1':file1,
            '2':file2
        }
        while True:
            try:
                print("1. 49_cities.txt \n2. cities_full.txt")
                selectedFile = input("Select input file to run: ")
                self.check_quit(selectedFile)
                return options[selectedFile]
            except KeyError:
                print("Error, invalid file selection.")
                print()
                continue

    def get_iterations(self):
        while True:
            try:
                numIterations = input("Enter the number of iterations to run (default 2000): ")
                self.check_quit(numIterations)
                numIterations = int(numIterations)
                if numIterations <= 0:
                    print()
                    print(f"Error, '{numIterations}' must be a positive integer.")
                    continue
                return numIterations
            except ValueError:
                print()
                print(f"Error, '{numIterations}' must be a positive integer.")
                continue

    def get_rounds(self):
        while True:
            try:
                numRounds = input("Enter the number of rounds to run (default 5): ")
                self.check_quit(numRounds)
                numRounds = int(numRounds)
                if numRounds <= 0:
                    print()
                    print(f"Error, '{numRounds}' must be a positive integer.")
                    continue
                return numRounds
            except ValueError:
                print()
                print(f"Error, '{numRounds}' must be a positive integer.")
                continue
    
    def read_file(self, filepath):
        """
        Read the input file. Remove the first line.
        :param filepath: The input file to read
        :return: A list of cities as tuples of (cityname, longititude, latitude)
        """
        with open(filepath) as data:
            cities = []
            lines = data.readlines()[1:]
            for line in lines:
                line = line.rstrip()
                arr = line.split(',')
                cities.append((arr[0], arr[1], arr[2]))
            return cities
    
    def write_file(self, algo, filename, absBestDistance, absBestSolution, citiesMap):
        """
        Write the absolute best solution to disk.
        :param algo: The type of algorithm used
        :param filename: The chosen input file
        :param absBestDistance: The absolute best distance in km
        :param absBestSolution: The absolute best arangement of cities for the TSP
        :param citiesMap: The int --> cities dictionary required for conversion 
        """
        pathSplit = os.path.split(filename) # split up absolute file path
        tail = pathSplit[1] # get the tail
        baseName = tail.split('.')[0] # split the period and get the base name
        outfile = open(f"{self.cwd}/{algo}_{baseName}_best_solution.txt", mode='w')
        outfile.write(f"Shortest path found: {absBestDistance} km\n")
        for eachCity in absBestSolution[:-1]:
            cityTuple = citiesMap[int(eachCity)]
            outfile.writelines(','.join(map(str, cityTuple)))
            outfile.write('\n')
        cityTuple = citiesMap[int(absBestSolution[-1])]
        outfile.writelines(','.join(map(str, cityTuple))) # Don't write a trailing new line
        outfile.close()