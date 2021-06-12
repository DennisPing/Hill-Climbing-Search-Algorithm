import sys
import os
from numba import njit, types, typed
from time import time
import numpy as np
from geopy.distance import distance
from matplotlib import pyplot as plt
from io_manager import IOManager
import itertools

class Parser:
    """
    A class to parse the input file. Remove the first line.
    Reformats cities into tuples of (cityname, longititude, latitude)
    """
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

@njit
def random_solution(citiesIdx):
    """
    Generate a random solution from a list of city indexes.
    The home city is automatically added to the end of the list.
    :param citiesIdx: A list of city indexes.
    :return: A list of city indexes in random order for the Traveling Salesman to traverse.
    """
    solution = citiesIdx.copy() # Avoid nasty bug with object reference when you shuffle
    np.random.shuffle(solution)
    return solution

def build_cities_index(cities):
    """
    Index the cities into a numpy array so we can refer to cities as integers.
    :param cities: A list of city tuples composed of (cityname, longitude, latitude).
    :return: A list of cities labeled as integers.
    """
    citiesIdx = np.arange(0, len(cities))
    return citiesIdx # Initial build does not include return home!

def build_distance_map_redux(cities, citiesIdx):
    """
    Calculate all pairwise distances between cities and put them in a dictionary.
    Run this method one time before doing hill climbing iterations.
    :param cities: A list of city tuples composed of (cityname, longitude, latitude).
    :param citiesIdx: A list of cities labeled as integers.
    :return: A dictionary of all pairwise distances between cities.
    """
    citiesMap = {}
    for i, idxNum in enumerate(citiesIdx):
        citiesMap[idxNum] = cities[i]

    distanceMap = typed.Dict.empty(key_type=types.UniTuple(types.int64, 2), value_type=types.int64)
    # Note: permutations take up 2x more memory, but the eventual lookup is 2x faster.
    # This is because you don't need to stop, switch the tuple, and then lookup again.
    allPermutations = itertools.permutations(citiesIdx, 2)
    for i, each in enumerate(allPermutations):
        cityA = each[0] # These are the numeric values of cities
        cityB = each[1]

        coordA = (citiesMap[cityA][2], citiesMap[cityA][1]) # Get the city tuple from temp map
        coordB = (citiesMap[cityB][2], citiesMap[cityB][1])
        dist = distance(coordA, coordB).km
        distanceMap[each] = int(dist)
    print("SUCCESSFUL DISTANCE MAP BUILD")
    return distanceMap, citiesMap

@njit
def total_distance(solution, distanceMap):
    """
    Calculate the total distance among a solution of cities.
    Uses a dictionary to get lookup the each pairwise distance.
    :param solution: A list of cities in random order.
    :distanceMap: The dictionary lookup tool.
    :return: The total distance between all the cities.
    """
    totalDistance = 0
    for i, city in enumerate(solution[:-1]): # Stop at the second to last city.
        cityA = city
        cityB = solution[i+1]
        buildKey = (cityA, cityB)
        totalDistance += distanceMap[buildKey]
    # Build the key to return home
    cityA = solution[-1]
    cityB = solution[0]
    goHome = (cityA, cityB)
    totalDistance += distanceMap[goHome]
    return totalDistance

@njit
def find_best_neighbor(solution, distanceMap):
    """
    Create all possible neighbors by switching 1 pair of cities.
    Returns a better neighbor as soon as one is found.
    :param solution: A list of cities in random order.
    :param distanceMap: The dictionary lookup tool required to pass into total_distance function.
    :return: The a better neighbor as soon as one is found.
    """
    currentDistance = total_distance(solution, distanceMap)
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbor = solution.copy()
            neighbor[i], neighbor[j] = solution[j], solution[i]
            dist = total_distance(neighbor, distanceMap)
            if dist < currentDistance:
                return neighbor, dist # Better solution is automatically selected
    return solution, currentDistance

def main():
    """
    Initialize user prompt, parse the input file, and run the search algorithm.
    Plot the results.
    """
    ioManager = IOManager()
    filename, iterations, rounds = ioManager.prompt_input()

    parser = Parser()
    cities = parser.read_file(filename)
    
    print("\nStarting simple hill climbing search")
    startTime = time()
    citiesIdx = build_cities_index(cities)
    distanceMap, citiesMap = build_distance_map_redux(cities, citiesIdx)

    plt.style.use("ggplot")
    fig, ax = plt.subplots(figsize=(8,6))

    absBestDistance = sys.maxsize
    absBestSolution = None
    for r in range(rounds):
        t1 = time()
        distList = []
        iterList = []
        bestDist = sys.maxsize
        bestSolution = None
        for i in range(iterations):
            solution = random_solution(citiesIdx)
            bestNeighbor, shortestDist = find_best_neighbor(solution, distanceMap)
            if shortestDist < bestDist:
                bestDist = shortestDist
                bestSolution = bestNeighbor
            distList.append(bestDist)
            iterList.append(i + (r * iterations))

        # Track the absolute best solution and distance
        if bestDist < absBestDistance:
            absBestDistance = bestDist
            absBestSolution = bestSolution
        
        ax.plot(iterList, distList)
        t2 = time()
        duration = round(t2-t1, 3)
        print(f"Best distance in round {r}: {bestDist} km\t Time taken: {duration} sec")
    print(f"Total run time: {round(time() - startTime, 3)} sec")

    ioManager.write_file("hill_climbing", filename, absBestDistance, absBestSolution, citiesMap)
    
    plt.suptitle("Simple Hill Climbing Search Algorithm", fontsize=24)
    ax.set_title(f"Rounds: {rounds}     Iterations: {iterations}", fontsize=12)
    plt.xlabel("Iterations", fontsize=16)
    plt.ylabel("Shortest Distance (km)", fontsize=16)
    plt.tick_params(axis="both", which="major", labelsize=12)
    plt.xticks(np.arange(0, (rounds*iterations), 1000), rotation=40)

    plt.autoscale()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
