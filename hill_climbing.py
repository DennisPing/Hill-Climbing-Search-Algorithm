#!/usr/bin/env python3
# coding=utf-8

import sys
from time import time
import numpy as np
from numba import njit
from matplotlib import pyplot as plt
from io_manager import IOManager
from tsp import build_cities_index, build_distance_map, random_solution, total_distance

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
    cities = ioManager.read_file(filename)
    
    print("\nStarting simple hill climbing search")
    startTime = time()
    citiesIdx = build_cities_index(cities)
    distanceMap, citiesMap = build_distance_map(cities, citiesIdx)

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
