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