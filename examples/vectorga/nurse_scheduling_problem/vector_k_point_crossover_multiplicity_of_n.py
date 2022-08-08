from random import sample

from eckity.genetic_operators.genetic_operator import GeneticOperator


class VectorKPointsCrossoverWithMultiplicity(GeneticOperator):
    def __init__(self, n, probability=1, arity=2, k=1, events=None):
        """
            Vector N Point Mutation With Equal Distance Between Points.

            Chooses N vector cells and performs a small change in their values.

            Parameters
            ----------
            n : int
                Each interval (length between 2 points) can be represented as: n*x where x is x a natural number.

            probability : float
                The probability of the mutation operator to be applied

            arity : int
                The number of individuals this mutation is applied on

            k : int
                Number of points to cut the vector for the crossover.

            events: list of strings
                Events to publish before/after the mutation operator
        """
        self.n = n
        self.individuals = None
        self.applied_individuals = None
        self.k = k
        self.points = None
        super().__init__(probability=probability, arity=arity, events=events)

    def apply(self, individuals):
        """
        Attempt to perform the mutation operator

        Parameters
        ----------
        individuals : list of individuals
            individuals to perform crossover on

        Returns
        ----------
        list of individuals
            individuals after the crossover
        """
        self.individuals = individuals
        intervals_amount = individuals[0].size() // self.n
        self.points = sorted(sample(range(1, intervals_amount), self.k)) * self.n

        start_index = 0
        for end_point in self.points:
            replaced_part = individuals[0].get_vector_part(start_index, end_point)
            replaced_part = individuals[1].replace_vector_part(replaced_part, start_index)
            individuals[0].replace_vector_part(replaced_part, start_index)
            start_index = end_point  # todo add last iter

        self.applied_individuals = individuals
        return individuals
