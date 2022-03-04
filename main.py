import enum
from random import choices, randint, random, randrange
from typing import List, Tuple

# Driver code
lines = [line.replace("\n", "") for line in open("input.txt").readlines()]

total_transactions = int(lines[0])

transactions: List[List[Tuple[int, int]]] = []

for line_num in range(total_transactions):
  transaction_type, transaction_amount = lines[line_num + 1].split(" ")
  transactions.append((transaction_type, int(transaction_amount)))

Chromosome = List[int]
Population = List[Chromosome]
PopulationFitness = List[int]

def generate_chromosome(genome_length: int) -> Chromosome:
  chromosome: List[int] = []
  total_one_count = 0

  while (total_one_count == 0):
    total_one_count = 0
    chromosome = []
    for _ in range(genome_length):
      genome = randint(0, 1)
      if (genome == 1):
        total_one_count +=1
      chromosome.append(genome)
  return chromosome


def fitness(chromosome: Chromosome) -> int:
  fitness_calc: int = 0
  for idx, val in enumerate(chromosome):
    if (val == 1):
      # If the amount was lent decrease the fitness function
      if (transactions[idx][0] == "l"):
        fitness_calc -= transactions[idx][1]
      else:
        fitness_calc += transactions[idx][1]
  # Absolute value of fitness
  return abs(fitness_calc)

def generate_population(population_size: int, genome_length: int) -> Population:
  population: Population = []

  for _ in range(population_size):
    population.append(generate_chromosome(genome_length))

  return population

def selection(population: Population, population_with_fitness: PopulationFitness):
  return choices(population = population, weights = [1 if fitness == 0 else (1 / fitness) for fitness in population_with_fitness])[0]

def crossover(parent1: Chromosome, parent2: Chromosome) -> Chromosome:
  random_genome = randint(0, len(parent1) - 1)
  return parent1[0: random_genome] + parent2[random_genome:]

def mutation(chromosome: Chromosome, mutation_threshold: int = 0.3):
  random_index1 = randrange(len(chromosome))
  random_index2 = randrange(len(chromosome))

  if (random() > mutation_threshold):
    random_index1_value = chromosome[random_index1]
    chromosome[random_index1] = chromosome[random_index2]
    chromosome[random_index2] = random_index1_value

def genetic_algorithm(population: Population, total_generations: int, fitness_target: int):
  found_chromosome_index = -1
  for _ in range(total_generations):
    population_with_fitness: PopulationFitness = []
    next_population = []

    for chromosome in population:
      population_with_fitness.append(fitness(chromosome))

    if (sorted(population_with_fitness)[0] == fitness_target):
      found_chromosome_index = population_with_fitness.index(0)
      break
    
    for _ in population:
      parent1 = selection(population, population_with_fitness)
      parent2 = selection(population, population_with_fitness)
      child = crossover(parent1, parent2)
      while "".join(str(genome) for genome in child) == "0" * len(population[0]):
        child = crossover(parent1, parent2)
      mutation(child)
      next_population.append(child)
    population = next_population

  return -1 if found_chromosome_index == -1 else "".join(str(genome) for genome in population[found_chromosome_index])

def main():
  start_population = 100
  total_generations = 50
  initial_population = generate_population(start_population, total_transactions)
  target_chromosome = genetic_algorithm(initial_population, total_generations, 0)
  print(target_chromosome)
main()
