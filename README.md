# Solving The 'Nurse Scheduling Problem' Using EC-KitY 
The problem we will solve using the tools provided by EC-KitY is the 'Nurse Scheduling Problem'.

Note: Our files are located in examples/vectorga/nurse_scheduling_problem

## About The Problem
Given a list of nurses and chief nurses, and how many are required per shift in a day, return a schedule that upholds all the constraints.
* We will schedule the nurses for the next 7 days.
* There are 3 shifts per day. Morning - 7AM-2PM. Afternoon - 2PM-9PM. Night - 9PM-7AM.

We separate our constraints in to two groups: hard constraints and soft constraints.

Hard constraints are more important and have a heavier weight than soft constraints.

Hard constraints:
1. No nurse is allowed to work 3 or more consecutive night shifts.
2. No nurse is allowed to work a morning shift after a night shift.
3. Each morning shift arrangement needs to contain least 1 chief nurse and at least 3 nurses. (Can be changed easily)
4. Each afternoon shift arrangement  needs to contain at least 2 chief nurses and at least 5 nurses. (Can be changed easily)
5. Each night shift arrangement  needs to contain at least 2 chief nurses and at least 7 nurses. (Can be changed easily)

Soft constraints:
1. Each nurse should have at least 1 day off per week.
2. Each nurse should work at most 3 night shifts per week.
3. Each nurse should'nt work 3 consecutive shifts.

## Our Solution
Using the tools provided by EC-KitY we solved 'Nurse Scheduling Problem'.

After reading the list of nurses from a txt file, we created a SimpleEvolution EC-KitY object using our custom evaluation method, and ran it.

After the successful execution the results are printed to the screen and to a txt file.

The problem we are solving is a minimization problem, we would like to minimize the total amount of constraints not held by the current schedule. consequently, our target fitness value is 0, the higher the fitness, the worse the schedule is.

Our population contains 200 individuals, each individual is a bit vector of length (total nurse amount) * (total shifts per week). The custom evaluation method we wrote evaluated an individual based on the above written constraints. As stated before, hard constraints are more important than soft constraints, which is why the default heavy weight is 10 and the default soft weight is 1.

We used two types of mutations:
1. Our custom K-Point-Crossover mutation, supported by EC-KitY. The reason we created a custom mutation is because the default K-Point-Crossover mutation chooses K points at random, while ours chooses K points with spaces equal to n*x between them (n is a parameter, x is a natural number). This custom mutation is more beneficial to this problem because it allows us to swap full shifts/days between schedules, and not random parts of them.
2. An N-Bit-Flip-Mutation. After many tests and parameter changes, we've decided that the best number of bits to flip is n=3.

## Results And Statistics 
In our example we used 30 total nurses (9 chief nurses and 21 nurses, Nurses.txt file is located in examples/vectorga/nurse_scheduling_problem).

Max generation = 1000

Population size = 200

After 20 executions (with random seeds), these are the results:

| Run # | Generation | Total time | Fitness |
| ----- | ---------- | ---------- | ------- |
| #1 | 522 | 127.7s | 0.0 |
| #2 | 1000 | 282s | 1.0 |
| #3 | 643 | 183s | 0.0 |
| #4 | 1000 | 290.5s | 1.0 |
| #5 | 219 | 56.7s | 0.0 |
| #6 | 1000 | 271s | 1.0 |
| #7 | 457 | 157.2s | 0.0 |
| #8 | 211 | 60s | 0.0 |
| #9 | 619 | 184.3s | 0.0 |
| #10 | 171 | 48.2s | 0.0 |
| #11 | 1000 | 296.4s | 1.0 |
| #12 | 210 | 61.1s | 0.0 |
| #13 | 1000 | 296s | 1.0 |
| #14 | 293 | 87.5s | 0.0 |
| #15 | 1000 | 296.3s | 1.0 |
| #16 | 550 | 162.8s | 0.0 |
| #17 | 154 | 40s | 0.0 |
| #18 | 1000 | 294.4s | 2.0 |
| #19 | 336 | 99.3s | 0.0 |
| #20 | 424 | 122.7s | 0.0 |

| Avg. generation | Avg. time | Avg. fitness |
| --------------- | --------- | ------------ |
| 590.45 | 170.85s | 0.4 |

Our worst run was #18, with a fitness score of 2.0. This result probably means that 2 soft constraints were not solved by the evolutionary algorithm.

Our best run was #17, with a fitness score of 0.0, a time of 40s and only 154 generations. This is the optimal fitness score, which means that the schedule holds all of the constraints.

As you can see, 13 out of the 20 executions resulted in a successful run, and an optimal schedule (fitness=0.0).

The average fitness was 0.4 which is lower than the default soft weight (1.0).

You can view a successful schedule in "Results.txt".

## Citation

```
@article{eckity2022,
    author = {Sipper, Moshe and Halperin, Tomer and Tzruia, Itai and  Elyasaf, Achiya},
    title = {{EC-KitY}: Evolutionary Computation Tool Kit in {Python}},
    publisher = {arXiv},
    year = {2022},
    url = {https://arxiv.org/abs/2207.10367},
    doi = {10.48550/ARXIV.2207.10367},
}

@misc{eckity2022git,
    author = {Sipper, Moshe and Halperin, Tomer and Tzruia, Itai and  Elyasaf, Achiya},
    title = {{EC-KitY}: Evolutionary Computation Tool Kit in {Python}},
    year = {2022},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {\url{https://www.eckity.org/} }
}

```

### Additional Sources
* http://www.columbia.edu/~cs2035/courses/ieor4405.S17/p23.pdf
* https://iopscience.iop.org/article/10.1088/1757-899X/166/1/012024/pdf
* https://en.wikipedia.org/wiki/Nurse_scheduling_problem
