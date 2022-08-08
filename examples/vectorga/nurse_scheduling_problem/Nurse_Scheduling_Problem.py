from SchedulingEvaluator import NurseSchedulingEvaluator
from SchedulingEvaluator import SHIFTS_PER_WEEK
from SchedulingEvaluator import SCHEDULING_DAYS
from SchedulingEvaluator import SHIFTS_PER_DAY
from SchedulingEvaluator import MORNING_SHIFT
from SchedulingEvaluator import AFTERNOON_SHIFT
from SchedulingEvaluator import NIGHT_SHIFT

from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.subpopulation import Subpopulation
from eckity.creators.ga_creators.bit_string_vector_creator import GABitStringVectorCreator
from eckity.genetic_operators.mutations.vector_random_mutation import BitStringVectorNFlipMutation
from eckity.genetic_operators.selections.tournament_selection import TournamentSelection
from eckity.breeders.simple_breeder import SimpleBreeder
from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics

from vector_k_point_crossover_multiplicity_of_n import VectorKPointsCrossoverWithMultiplicity

FILENAME = 'Nurses.txt'
RESULTS_FILE = 'Results.txt'
NURSE_LIST = []
CHIEF_LIST = []
POPULATION_SIZE = 500
MAX_GENERATION = 1000


def read_file():
    with open(FILENAME) as file:
        lines = file.readlines()
        for i in range(len(lines)):
            line = lines[i].strip()
            if line.startswith('//') or line.startswith(' '):
                continue
            elif line.startswith('nurses:'):
                for j in range(i + 1, len(lines)):
                    next_line = lines[j].strip()
                    if len(next_line) == 0 or next_line.startswith('chief nurses:'):
                        break
                    NURSE_LIST.append(next_line)
            elif line.startswith('chief nurses:'):
                for j in range(i + 1, len(lines)):
                    next_line = lines[j].strip()
                    if len(next_line) == 0 or next_line.startswith('nurses:'):
                        break
                    CHIEF_LIST.append(next_line)
            else:
                continue


def print_results(best_of_run):
    result = ''
    for day in range(1, SCHEDULING_DAYS + 1):
        result += 'Day ' + str(day) + '\n'
        result += '==========\n\n'
        result += 'Morning Shift - 7AM-2PM\n'
        result += '==========\n'
        result += get_shift(best_of_run, day, MORNING_SHIFT)
        result += '\n'
        result += 'Afternoon Shift - 2PM-9PM\n'
        result += '==========\n'
        result += get_shift(best_of_run, day, AFTERNOON_SHIFT)
        result += '\n'
        result += 'Night Shift - 9PM-7AM\n'
        result += '==========\n'
        result += get_shift(best_of_run, day, NIGHT_SHIFT)
        result += '\n'
    print(result)
    with open(RESULTS_FILE, 'w+') as file:
        file.write(result)


def get_shift(best_of_run, day, shift):
    total_nurses = (len(NURSE_LIST) + len(CHIEF_LIST))
    result = ''
    result += 'Chief nurses:\n'
    for nurse in range(len(CHIEF_LIST)):
        if best_of_run.cell_value(total_nurses * ((day - 1) * SHIFTS_PER_DAY + shift) + nurse):
            result += CHIEF_LIST[nurse] + '\n'
    result += '\n'
    result += 'Nurses:\n'
    for nurse in range(len(CHIEF_LIST), total_nurses):
        if best_of_run.cell_value(total_nurses * ((day - 1) * SHIFTS_PER_DAY + shift) + nurse):
            result += NURSE_LIST[nurse - len(CHIEF_LIST)] + '\n'
    return result


def main():
    read_file()
    bit_vector_length = SHIFTS_PER_WEEK * (len(NURSE_LIST) + len(CHIEF_LIST))
    algo = SimpleEvolution(
        Subpopulation(
            # A single bit vector represents the whole schedule, for all nurses.
            creators=GABitStringVectorCreator(length=bit_vector_length),
            population_size=POPULATION_SIZE,
            # For the evaluator, we will use our custom evaluator function.
            evaluator=NurseSchedulingEvaluator(nurse_amount=len(NURSE_LIST), chief_amount=len(CHIEF_LIST)),
            # This is a minimization problem, since we want to minimize the total amount of constraints broken.
            higher_is_better=False,
            elitism_rate=0.3,
            # 50% chance for a (SHIFTS_PER_WEEK - 1) point vector-crossover,
            # 20% chance for an N bit flip mutation with N=0.2*vector_length.
            operators_sequence=[
                VectorKPointsCrossoverWithMultiplicity(probability=0.8, n=(len(NURSE_LIST) + len(CHIEF_LIST)), k=3),
                #VectorKPointsCrossover(probability=0.7, k=(len(NURSE_LIST) + len(CHIEF_LIST))),
                BitStringVectorNFlipMutation(probability=0.8, n=2, probability_for_each=0.5)
            ],
            # Tournament selection with a probability of 1 and with tournament size of 5.
            selection_methods=[
                (TournamentSelection(tournament_size=16, higher_is_better=False), 1)
            ]
        ),
        breeder=SimpleBreeder(),
        max_workers=1,
        max_generation=MAX_GENERATION,
        statistics=BestAverageWorstStatistics(),
    )
    algo.evolve()
    print(algo.execute())
    print_results(algo.best_of_run_)


if __name__ == '__main__':
    main()