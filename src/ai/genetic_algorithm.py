class GeneticAlgorithm:
    def __init__(self):
        self.population = []
        self.fitness = 0
    
    def set_population(self, new_population):
        self.population = new_population
        
    def get_population(self):
        return self.population
        
    def calculate_fitness(self):
        """
        Calculates the fitness of each bird in the population.
        """
        for bird in self.population:
            bird.calculate_fitness()
            
            
    def get_new_generation(self):
        self.calculate_fitness()
