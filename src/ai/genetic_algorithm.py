class GeneticAlgorithm:
    def __init__(self):
        self.fitness = 0
        
    def calculate_fitness(self, population):
        """
        Calculates the fitness of each bird in the population.
        """
        for bird in population:
            bird.calculate_fitness()