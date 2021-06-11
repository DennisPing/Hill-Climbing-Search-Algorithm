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

## Why Use Numba?

Numba compiles Python code down to C level machine code.
This usually requires the Python code to be written with basic primitives, no objects, and no external modules.

Without numba, the simple `49_cities.txt` file takes about 4.5 minutes to calculate 10,000 iterations.  
With numba, the simple `49_cities.txt` file takes about 10 seconds to calculate 10,000 iterations.  
I did not want to wait 12 days for the `cities_full.txt` file to finish computing.

| Algorithm | Input File | Without Numba | With Numba | Improvement |
| ----------| ------------- | ----------- | ----------- | ---------|
| Gradient Descent | 49_cities.txt | 4.5 min | 10 sec | 27x     |
| Gradient Descent | cities_full.txt | 294 hr | 44 hr   | 6.6x     |
| Hill Climbing | 49_cities.txt | ... | 1.2 sec | ... |
| Hill Climbing | cities_full.txt | ... | 20 sec | ... |

*Note: Computation done on an AMD Ryzen 5600x. Performance may vary.*

## How to Run

`python hill_climbing.py`

`python gradient_descent.py`

## Example Output

**Gradient Search on 49_cities.txt**
```rtf
Best distance: 254814 km         Time taken: 2.571 seconds
Best distance: 262115 km         Time taken: 1.87 seconds
Best distance: 259326 km         Time taken: 1.877 seconds
Best distance: 248131 km         Time taken: 1.874 seconds
Best distance: 260561 km         Time taken: 1.847 seconds
```

## Example Plots

### Gradient Descent - 49 cities
![gradient_descent](https://i.imgur.com/44zzghk.png)