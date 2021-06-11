import os
import sys

class Prompt:
    """
    A class to prompt the user for input and check the input values.
    Supports quit functionality.
    """

    def __init__(self):
        pass

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
        cwd = os.getcwd()
        options = {
            '1':f"{cwd}/49_cities.txt",
            '2':f"{cwd}/cities_full.txt"
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