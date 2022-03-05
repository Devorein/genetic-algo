from random import choices, randint, random, randrange
from typing import List, Tuple

# Driver code
lines = [line.replace("\n", "") for line in open("input.txt").readlines()]

total_transactions = int(lines[0])

transactions: List[Tuple[int, int]] = []

for line_num in range(total_transactions):
  # Split each line by space
  # First one contains the type of transaction l for lend and d for deposit
  # The second one contains the amount
  transaction_type, transaction_amount = lines[line_num + 1].split(" ")
  # Append the transaction type and the amount as a tuple
  transactions.append((transaction_type, int(transaction_amount)))

# Define types
Chromosome = List[int]
Population = List[Chromosome]
PopulationFitness = List[int]
PopulationFitnessWithIndex = List[Tuple[int, int]]

def generate_chromosome(genome_length: int) -> Chromosome:
  chromosome: Chromosome = []
  # Total number of ones encountered in the chromosome
  total_one_count = 0

  # This loop makes sure we don't have all 0's
  while (total_one_count == 0):
    total_one_count = 0
    chromosome = []
    # Loop until we reach the limit of genome length
    for _ in range(genome_length):
      # Generate a random integer between 0 and 1
      genome = randint(0, 1)
      # If genome is 1 increment the total_one_count variable
      if (genome == 1):
        total_one_count +=1
      # Add the genome to the chromosome
      chromosome.append(genome)
  return chromosome


def fitness(chromosome: Chromosome) -> int:
  fitness_calc: int = 0
  # Loop through each genome of the chromosome
  for idx, val in enumerate(chromosome):
    # If the genome is 1 we need to add the transaction amount
    if (val == 1):
      transaction_type, transaction_amount = transactions[idx]
      # If the amount was lent decrease the fitness calc
      if (transaction_type == "l"):
        fitness_calc -= transaction_amount
      else:
        fitness_calc += transaction_amount
  # Absolute value of fitness calculation as negative would interfere when sorting
  return abs(fitness_calc)

# Generate population of given size with each chromosome having genome_length number of genomes
def generate_population(population_size: int, genome_length: int) -> Population:
  population: Population = []
  for _ in range(population_size):
    population.append(generate_chromosome(genome_length))

  return population

# Randomly select one chromosome from population based on weights provided by fitness calculation
def selection(population: Population, weights: List[int]):
  # The weight is between 0 and 1
  # If the fitness value is 0, that means its weight should be maximum, ie 1
  # Else if its > 0, then its weight would be inverse of the value, to decrease its weight 
  return choices(population = population, weights = weights)[0]

def crossover(parent1: Chromosome, parent2: Chromosome) -> Chromosome:
  # Generate a random number between 0 and total genome of the chromosome 
  random_genome = randint(0, len(parent1) - 1)
  # Return the genome of first parent from 0 unto the index along with the genome of second parent from that index up to the end
  return parent1[0: random_genome] + parent2[random_genome:]

def mutation(chromosome: Chromosome, mutation_threshold: int = 0.5):
  # Get two random index of the chromosome
  random_index1 = randrange(len(chromosome))
  random_index2 = randrange(len(chromosome))

  # If the random value is greater than mutation threshold then mutate
  if (random() > mutation_threshold):
    # Swap the value of the first index with the second index
    random_index1_value = chromosome[random_index1]
    chromosome[random_index1] = chromosome[random_index2]
    chromosome[random_index2] = random_index1_value

def genetic_algorithm(population: Population, total_generations: int = 1, fitness_target: int = 0, mutation_threshold: int = 0.5):
  # Index of the target chromosome in the population
  target_chromosome = None
  # Run the algorithm until we reach total generation or we've found the target chromosome
  for _ in range(total_generations):
    # Fitness value of all chromosomes, without storing the index
    # This is used as weight when doing parent selection
    population_with_fitness: PopulationFitness = []
    # Fitness value of all chromosomes, along with their index in the population
    # This is used to get the best two chromosome in each generation and to enable elitism
    population_with_fitness_and_index = PopulationFitnessWithIndex = []

    # Store the max fitness value, this will be used to calculate the weights
    max_fitness_value = 0

    # For each chromosome in population
    for chromosome_num, chromosome in enumerate(population):
      # Calculate its fitness value
      fitness_value = fitness(chromosome)

      if (fitness_value > max_fitness_value):
        max_fitness_value = fitness_value
      # Append the fitness value
      population_with_fitness.append(fitness_value)
      # Append the fitness value along with the index of the chromosome
      population_with_fitness_and_index.append((chromosome_num, fitness_value))

    # Sort the list based on the fitness score
    sorted_population_with_fitness_and_index = sorted(population_with_fitness_and_index, key = lambda x: x[1] )
    # If we have reached the target fitness value
    if (sorted_population_with_fitness_and_index[0][1] == fitness_target):
      # Get the target chromosome
      target_chromosome = population[sorted_population_with_fitness_and_index[0][0]]
      # Break the loop, no need to continue further
      break
    
    # Enable elitism
    # The top two chromosome from the population will be present in the next generation
    next_population = [
      population[sorted_population_with_fitness_and_index[0][0]],
      population[sorted_population_with_fitness_and_index[1][0]],
    ]

    weights = [max_fitness_value - fitness_value for fitness_value in population_with_fitness]
    # Reduce looping by two as they are the elite of the population
    for _ in range(len(population) - 2):
      # Select two parents from population, the fitness would be used as weights
      parent1 = selection(population, weights)
      parent2 = selection(population, weights)
      # Create the child by crossing between the two parents
      child = crossover(parent1, parent2)
      # While the child only consists of 0, cross over the child again, until its not
      while "".join(str(genome) for genome in child) == "0" * len(population[0]):
        child = crossover(parent1, parent2)
      # Perform mutation of the child
      mutation(child, mutation_threshold)
      # Add the child to the next population
      next_population.append(child)
    # Next population would be the current population
    population = next_population
  # If no target chromosome was found return -1, else return the chromosome
  return -1 if target_chromosome == None else "".join(str(genome) for genome in target_chromosome)

def main():
  # Probability of mutation
  mutation_threshold = 0.5
  # Total chromosome in a single population
  total_chromosomes = 50
  # Total number of generation
  total_generations = 10
  # Generate the initial population, total_transaction would be the number of genome of a chromosome
  initial_population = generate_population(total_chromosomes, total_transactions)
  # Get the target chromosome, if not -1 is returned, 0 is used to indicated that fitness target is 0
  target_chromosome = genetic_algorithm(initial_population, total_generations, 0 ,mutation_threshold)
  print(target_chromosome)
main()
