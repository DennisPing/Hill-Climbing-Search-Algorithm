import sys
from numba import njit, types, typed
from time import time
import numpy as np
from geopy.distance import distance
from matplotlib import pyplot as plt
from prompt import Prompt
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
    temp = citiesIdx.copy()
    np.random.shuffle(temp)
    home = citiesIdx[0]
    solution = np.append(temp, home) # Append home city
    return solution

def build_cities_index(cities):
    """
    Index the cities into a numpy array so we can refer to cities as integers.
    :param cities: A list of city tuples composed of (cityname, longitude, latitude).
    :return: A list of cities labeled as integers.
    """
    citiesIdx = np.arange(0, len(cities))
    return citiesIdx # Remember that cities idx does not include return home!

def build_distance_map(cities, citiesIdx):
    """
    Generate a matrix of all possible pairwise distances between cities.
    Run this method one time before doing hill climbing iterations.
    :param cities: A list of city tuples composed of (cityname, longitude, latitude).
    :param citiesIdx: A list of cities labeled as integers.
    :return: A dictionary of all pairwise distances between cities.
    """
    distanceMap = typed.Dict.empty(key_type=types.UniTuple(types.int64, 2), value_type=types.int64)
    home = cities[0] # Store the home tuple.
    longitude = []
    latitude = []
    for each in cities:
        longitude.append((each[1]))
        latitude.append((each[2]))
    longitude.append(home[1])
    latitude.append(home[2])
    citiesIdx = np.append(citiesIdx, citiesIdx[0])
    
    longitude = np.array(longitude)
    latitude = np.array(latitude)
    stacked = np.dstack((citiesIdx, latitude, longitude)) # LATITUDE THEN LONGITUDE
    del longitude
    del latitude

    coords = np.squeeze(stacked[...,1:], axis=0)
    allDistances = [distance(c1, c2).km for c1 in coords for c2 in coords]
    del stacked
    del coords

    xx, yy = np.meshgrid(citiesIdx, citiesIdx, indexing="ij")
    cityPairs = np.stack((xx.ravel(), yy.ravel()), axis=1)

    for i, each in enumerate(cityPairs):
        element = (each[0], each[1])
        distanceMap[element] = int(allDistances[i])
    print("SUCCESSFUL DISTANCE MAP BUILD")
    return distanceMap

def build_distance_map_redux(cities, citiesIdx):
    """
    Calculate all pairwise distances between cities and put them in a dictionary.
    Run this method one time before doing hill climbing iterations.
    :param cities: A list of city tuples composed of (cityname, longitude, latitude).
    :param citiesIdx: A list of cities labeled as integers.
    :return: A dictionary of all pairwise distances between cities.
    """
    home = cities[0]
    cities.append(home) # Append the home so that you can return home.
    citiesIdx = np.append(citiesIdx, 0) # Append home.
    tempMap = {}
    for i, each in enumerate(citiesIdx):
        tempMap[each] = cities[i]

    distanceMap = typed.Dict.empty(key_type=types.UniTuple(types.int64, 2), value_type=types.int64)
    allPermutations = itertools.permutations(citiesIdx, 2)
    for i, each in enumerate(allPermutations):
        cityA = each[0] # These are the numeric values of cities
        cityB = each[1]

        coordA = (tempMap[cityA][2], tempMap[cityA][1]) # Get the city tuple from temp map
        coordB = (tempMap[cityB][2], tempMap[cityB][1])
        dist = distance(coordA, coordB).km
        distanceMap[each] = int(dist)
    print("SUCCESSFUL DISTANCE MAP BUILD")
    return distanceMap

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
    return totalDistance

@njit
def find_best_neighbor(solution, distanceMap):
    """
    Create all possible neighbors by switching 1 pair of cities.
    Also checks to see if this new distance is better than the current distance.
    :param solution: A list of cities in random order.
    :param distanceMap: The dictionary lookup tool required to pass into total_distance function.
    :return: The best neighbor and best distance out of all possible neighbors.
    """
    bestDist = sys.maxsize
    bestNeighbor = None
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbor = solution.copy()
            neighbor[i], neighbor[j] = solution[j], solution[i]
            dist = total_distance(neighbor, distanceMap)
            if dist < bestDist:
                bestDist = dist
                bestNeighbor = neighbor
    return bestNeighbor, bestDist

def main():
    prompt = Prompt()
    filename, iterations, rounds = prompt.prompt_input()

    parser = Parser()
    cities = parser.read_file(filename)
    
    print("\nStarting simple hill climbing search")
    startTime = time()
    citiesIdx = build_cities_index(cities)
    distanceMap = build_distance_map_redux(cities, citiesIdx)

    plt.style.use("ggplot")
    fig, ax = plt.subplots(figsize=(8,6))

    for r in range(rounds):
        t1 = time()
        distList = []
        iterList = []
        bestDist = sys.maxsize
        for i in range(iterations):
            solution = random_solution(citiesIdx)
            bestNeighbor, shortestDist = find_best_neighbor(solution, distanceMap)
            if shortestDist < bestDist:
                bestDist = shortestDist
                bestSolution = bestNeighbor
            distList.append(bestDist)
            iterList.append(i + (r * iterations))
        ax.plot(iterList, distList)
        t2 = time()
        duration = round(t2-t1, 3)
        print(f"Best distance in round {r}: {bestDist} km\t Time taken: {duration} sec")
    print(f"Total run time: {round(time() - startTime, 3)} sec")
    
    plt.suptitle("Gradient Descent Search Algorithm", fontsize=24)
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
