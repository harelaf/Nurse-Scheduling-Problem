# Solving The 'Nurse Scheduling Problem' With EC-KitY 
The problem we will solve using the tools provided by EC-KitY is the 'Nurse Scheduling Problem'.

Note:

Our files are located in examples/vectorga/nurse_scheduling_problem

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

Our problem is a minimization problem, we would like to minimize the total amount of constraints not held by the current schedule. Because of that, our target fitness value is 0, the higher the fitness, the worse the schedule is.

Our population contains 500 individuals, each individual is a bit vector of length (total nurse amount) * (total shifts per week). The custom evaluation method we wrote evaluated an individual based on the above written constraints. As stated before, hard constraints are more important than soft constraints, which is why the evaluation method adds a heavier weight to the fitness score when one is broken.

## Statistics And Results
WORK IN PROGRESS


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
