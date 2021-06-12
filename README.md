# Hill Climbing Search Algorithm

Dennis Ping  
Homework 3  
June 12, 2021  

## Purpose

Implement a simple hill climbing and steepest descent hill climbing algorithm for the traveling salesman problem.

For **gradient descent**, all possible successors are evaluated and the one with the highest/lowest 
objective function (greatest derivative) is chosen as the new state.  
For **simple hill climbing**, evaluate the possible successors at the current state and as soon as 
any better state is found, choose it as the new state and repeat.  

## Criteria

- Do random restart hill climbing at least 5 times for every 2000 iterations. This means that you restart each 
hill climbing algorithm after every 2000 iterations and run until 10,000 iterations is complete.
- Generate plots of results with iterations from 1 to 10,000.

## Python and Pip requirements

- Python 3
- numpy
- geopy
- matplotlib
- numba

## How to Run

`python hill_climbing.py`

`python gradient_descent.py`

## Why Use Numba?

Numba compiles Python code down to C level machine code.
This usually requires the Python code to be written with standard primitives, no objects, and no external modules.  

Numba is worse for small calculations because it requires extra compile time while native Python runs immediately.  
Numba is much better for repetitive calculations and large number sets.

Without numba for Gradient Descent search, the large `cities_full.txt` file takes an estimated 294 hours (12 days) to calculate 10,000 iterations.  
With numba for Gradient Descent search, the large `cities_full.txt` file took 13.5 hours to calculate 10,000 iterations.  

| Algorithm            | Input File      | Without Numba | With Numba | Improvement | Shortest Path |
| ---------------------| --------------- | -----------  | ----------- | ----------- | ------------- |
| Simple Hill Climbing | 49_cities.txt   | 0.83 sec     | 1.7 sec  | - 48 %         | 275,377       |
| Simple Hill Climbing | cities_full.txt | 63 sec       | 77 sec   | - 82 %         | 5,675,861     |
| Gradient Descent     | 49_cities.txt   | 4.5 min      | 11 sec   | + 2500 %       | 262,674       |
| Gradient Descent     | cities_full.txt | 294 hr (est) | 13.2 hr  | + 2200 %       | 5,518,089     |

*Note: Computation done on an AMD Ryzen 5600x. Performance may vary.*

## Is a complete brute force run worth it?

Heck no. Generating every possible neighbor from a random solution leads to testing a huge number of negligble solutions.

Among the full list of 754 cities, there are 283,881 unique pairs of cities which also means swapping is done that many times. For only 1 iteration.  
Thus, for 10k iterations, you are swapping 2,838,810,000 times.

Rather, you can achieve similar results by randomizing the swap positions and limiting the number of swaps to 500 per iteration.  
In fact, you often stumble into a better solution by sheer luck.  

## Example Input
Command Line Interface   
```
1. 49_cities.txt
2. cities_full.txt
Select input file to run: 2
Enter the number of iterations to run (default 2000): 2000
Enter the number of rounds to run (default 5): 5
```

## Example Output

**Simple Hill Climbing Search on `49_cities.txt`**
```
Starting simple hill climbing search
SUCCESSFUL DISTANCE MAP BUILD
Best distance in round 0: 281938 km      Time taken: 0.663 sec
Best distance in round 1: 285696 km      Time taken: 0.011 sec
Best distance in round 2: 287342 km      Time taken: 0.012 sec
Best distance in round 3: 292850 km      Time taken: 0.011 sec
Best distance in round 4: 285082 km      Time taken: 0.011 sec
Total run time: 1.709 sec
```

**Simple Hill Climbing Search on `cities_full.txt`**
```
Starting simple hill climbing search
SUCCESSFUL DISTANCE MAP BUILD
Best distance in round 0: 5738461 km     Time taken: 0.873 sec
Best distance in round 1: 5685514 km     Time taken: 0.191 sec
Best distance in round 2: 5758043 km     Time taken: 0.174 sec
Best distance in round 3: 5616965 km     Time taken: 0.18 sec
Best distance in round 4: 5741462 km     Time taken: 0.173 sec
Total run time: 77.152 sec
```

**Gradient Descent Search on `49_cities.txt`**
```
Starting gradient descent search
SUCCESSFUL DISTANCE MAP BUILD
Best distance in round 0: 262213 km      Time taken: 2.538 sec
Best distance in round 1: 257964 km      Time taken: 1.802 sec
Best distance in round 2: 254392 km      Time taken: 1.819 sec
Best distance in round 3: 258124 km      Time taken: 1.798 sec
Best distance in round 4: 233051 km      Time taken: 1.812 sec
Total run time: 10.773 sec
```

**Gradient Descent Search on `cities_full.txt`**
```
Starting gradient descent search
SUCCESSFUL DISTANCE MAP BUILD
Best distance: 5652943 km        Time taken: 9426.482 seconds
Best distance: 5632523 km        Time taken: 9412.132 seconds
Best distance: 5626032 km        Time taken: 9499.184 seconds
Best distance: 5614990 km        Time taken: 9503.708 seconds
Best distance: 5546086 km        Time taken: 9533.341 seconds
Total run time: 47454.847 seconds
```

**Gradient Descent Search on `cities_full.txt` limit of 500 swaps per iteration**
```
Starting gradient descent search
SUCCESSFUL DISTANCE MAP BUILD
Best distance in round 0: 5670616 km     Time taken: 17.476 sec
Best distance in round 1: 5587405 km     Time taken: 16.675 sec
Best distance in round 2: 5712330 km     Time taken: 16.782 sec
Best distance in round 3: 5707102 km     Time taken: 16.67 sec
Best distance in round 4: 5518089 km     Time taken: 16.688 sec
Total run time: 159.554 sec
```

## Example Plots

### Simple Hill Climbing - 49 cities
![hill climbing 49](https://i.imgur.com/e1XwfWG.png)

### Simple Hill Climbing - full cities
![hill climbing full](https://i.imgur.com/pOGUrKV.png)

### Gradient Descent - 49 cities
![gradient descent 49](https://i.imgur.com/FESNsyG.png)

### Gradient Descent - full cities
![gradient descent full](https://i.imgur.com/gjFDuKY.png)

### Gradient Descent - full cities limit of 500 swaps
![gradient descent full limit](https://i.imgur.com/k11Lx0A.png)