import os
from random import choice
from geopy.distance import distance
import itertools
import sys
from time import time
from matplotlib import pyplot as plt
import numpy as np

class Parser:
    def __init__(self):
        pass

    def read_file(self, filepath):
        with open(filepath) as data:

            cities = []
            lines = data.readlines()[1:]
            for line in lines:
                line = line.rstrip()
                arr = line.split(',')
                cities.append((arr[0], arr[1], arr[2]))
            return cities

class HillClimbing:
    def __init__(self, cities):
        self.cities = cities
        self.home = cities[0]
        self.distanceMap = None

    def random_solution(self):
        """
        Generate a random solution from a list of cities.
        The home city is automatically added to the end of the list.
        :return: A random list of tuples composed of (cityname, longitude, latitude)
        """
        solution = [self.home]
        # Cannot mutate lists while iterating. So make a copy of it.
        tempCities = self.cities[1:].copy()

        while len(solution) < len(self.cities):
            randomCity = choice(tempCities)
            solution.append(randomCity)
            tempCities.remove(randomCity)
        solution.append(self.home) # The traveling salesman must return home afterwards.
        return solution

    def total_distance(self, solution):
        """
        Calculate the total distance among a solution of cities.
        Uses a dictionary to get pairwise distances.
        :param solution: A random list of city tuples.
        :return: The total distance between all the cities.
        """
        totalDistance = 0
        for i, city in enumerate(solution[:-1]): # Stop at the second to last city.
            cityA = city
            cityB = solution[i+1]
            try:
                buildKey = (cityA, cityB)
                totalDistance += self.distanceMap[buildKey]
            except:
                buildKey = (cityB, cityA) # Check the opposite permutation.
                totalDistance += self.distanceMap[buildKey]
        return int(totalDistance)

    def generate_and_find_best_neighbors(self, solution): # this takes the 2nd longest time.
        """
        Generate all possible neighbors from a solution of cities.
        :param solution: A random list of city tuples.
        :return: All possible neighbors as a list.
        """
        bestDist = sys.maxsize
        bestNeighbor = None
        for i in range(len(solution)):
            for j in range(i + 1, len(solution)):
                neighbor = solution.copy()
                neighbor[i], neighbor[j] = solution[j], solution[i]
                dist = self.total_distance(neighbor)
                if dist < bestDist:
                    bestDist = dist
                    bestNeighbor = neighbor
        return bestNeighbor, bestDist

    def find_best_neighbor(self, allNeighbors): # this takes the longest time. Order it beforehand.
        """
        Find the best neighbor solution out of all possible neighbors.
        :param allNeighbors: All possible neighbors as a list.
        :return: The best neighbor which has the shortest total distance.
        """
        bestNeighbor = allNeighbors[0]
        shortestDist = self.total_distance(bestNeighbor) # Pick the first neighbor to start.
        for each in allNeighbors:
            eachDist = self.total_distance(each)
            if eachDist < shortestDist:
                shortestDist = eachDist
                bestNeighbor = each
        return bestNeighbor, shortestDist

    def build_distance_map(self, solution):
        """
        Generate a dictionary of all possible pairwise distances between cities.
        Run this method one time before doing hill climbing iterations.
        :param solution: A random list of city tuples.
        :return: A dictionary of all pairwise distances.
        """
        distanceMap = {}
        allCombinations = itertools.combinations(solution, 2) # For 50 cities, the num combinations is 1225.

        for each in allCombinations:
            cityA = each[0]
            cityB = each[1]

            coordA = (cityA[2], cityA[1])
            coordB = (cityB[2], cityB[1])

            dist = distance(coordA, coordB).km
            distanceMap[each] = int(dist) # Remember to use this tuple (cityA, cityB) when doing lookup.
        self.distanceMap = distanceMap

def main():
    cwd = os.getcwd()
    fileBuilder = f"{cwd}/49_cities.txt"
    parser = Parser()
    cities = parser.read_file(fileBuilder)
    
    hillclimb = HillClimbing(cities)
    solution = hillclimb.random_solution()
    print("Finished initial setup.")

    # First generate an arbitary solution and build the distance map.
    hillclimb.build_distance_map(solution)
    print(hillclimb.distanceMap[(('Shanghai', '121.47', '31.23'), ('Soul', '126.99', '37.56'))])
    print("Finished building distance map.")

    # Then do 2000 iterations of hill climbing.
    rounds = 5
    iterations = 2000
    bestSolution = None

    plt.style.use("seaborn")
    fig, ax = plt.subplots(figsize=(8,6))

    for r in range(rounds):

        t1 = time()
        distList = []
        iterList = []
        bestDist = sys.maxsize
        for i in range(iterations):
            tx = time()

            solution = hillclimb.random_solution()
            #print("Made a random solution.")

            bestNeighbor, shortestDist = hillclimb.generate_and_find_best_neighbors(solution)
            #print("Found the best neighbor.")

            if shortestDist < bestDist:
                bestDist = shortestDist
                bestSolution = bestNeighbor
            distList.append(bestDist)
            iterList.append(i + (r*iterations))
            #print(f"time for iteration #{i}: {time() - tx}")
        ax.plot(iterList, distList)
        t2 = time()
        duration = round(t2-t1, 2)
        print(f"Best distance: {bestDist} km\t Time taken: {duration} seconds")

    plt.title("Hill Climbing Search Algorithm", fontsize=24)
    plt.xlabel("Iterations", fontsize=14)
    plt.ylabel("Shortest Distance (km)", fontsize=14)
    plt.tick_params(axis="both", which="major", labelsize=14)

    plt.xticks(np.arange(0, (rounds*iterations), 100))

    plt.show()

if __name__ == "__main__":
    main()