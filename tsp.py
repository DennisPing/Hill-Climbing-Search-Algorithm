#!/usr/bin/env python3
# coding=utf-8

import sys
from numba import njit, types, typed
from time import time
import numpy as np
from geopy.distance import distance
from matplotlib import pyplot as plt
from io_manager import IOManager
import itertools

"""
Shared functions for the traveling salesman problem.
"""

def build_cities_index(cities):
    """
    Index the cities into a numpy array so we can refer to cities as integers.
    :param cities: A list of city tuples composed of (cityname, longitude, latitude).
    :return: A list of cities labeled as integers.
    """
    citiesIdx = np.arange(0, len(cities))
    return citiesIdx

def build_distance_map(cities, citiesIdx):
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

        coordA = (citiesMap[cityA][2], citiesMap[cityA][1]) # Get the city tuple from citiesMap
        coordB = (citiesMap[cityB][2], citiesMap[cityB][1])
        dist = distance(coordA, coordB).km
        distanceMap[each] = int(dist)
    print("SUCCESSFUL DISTANCE MAP BUILD")
    return distanceMap, citiesMap

@njit
def random_solution(citiesIdx):
    """
    Generate a random solution from a list of city indexes.
    :param citiesIdx: A list of city indexes.
    :return: A list of city indexes in random order for the Traveling Salesman to traverse.
    """
    solution = citiesIdx.copy() # Avoid nasty bug with object reference when you shuffle
    np.random.shuffle(solution)
    return solution

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
        cityB = solution[i + 1]
        buildKey = (cityA, cityB)
        totalDistance += distanceMap[buildKey]
    # Build the key to return home
    cityA = solution[-1]
    cityB = solution[0]
    goHome = (cityA, cityB)
    totalDistance += distanceMap[goHome]
    return totalDistance