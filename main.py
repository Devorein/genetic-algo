import enum
from random import choices, randint
from typing import List, Tuple

# Driver code
lines = [line.replace("\n", "") for line in open("input.txt").readlines()]

total_transactions = int(lines[0])

transactions: List[List[Tuple[int, int]]] = []

for line_num in range(total_transactions):
  transaction_type, transaction_amount = lines[line_num + 1].split(" ")
  transactions.append((transaction_type, int(transaction_amount)))

start_population = 10
mutation_threshold = 0.3
total_generations = 1

Chromosome = List[int]
Population = List[Chromosome]
PopulationFitness = List[Tuple[int, int]]

def generate_chromosome(genome_length: int) -> Chromosome:
  chromosome: List[int] = []

  for _ in range(genome_length):
    chromosome.append(randint(0, 1))

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
  return choices(population = population, weights = [
    fitness[1] for fitness in population_with_fitness
  ])

def crossover(parent1: Chromosome, parent2: Chromosome) -> Chromosome:
  random_genome = randint(0, len(parent1))
  return parent1[0: random_genome] + parent2[random_genome:]


def genetic_algorithm(population: Population, total_generations: int):
  next_population: Population = population
  for _ in range(total_generations):
    population_with_fitness: PopulationFitness = []

    for chromosome_num, chromosome in enumerate(next_population):
      population_with_fitness.append((chromosome_num, fitness(chromosome)))

    # Sort the population based on the ascending order of fitness value
    population_with_fitness = sorted(population_with_fitness, key = lambda fitness: fitness[1])
    print(population_with_fitness)

    # keep the first two parent of the current generation based on their fitness value
    next_population = [
      population[population_with_fitness[0][0]],
      population[population_with_fitness[1][0]],
    ]
    
    # First two are the best fit chromosome from the previous generation
    for i in range(len(population) - 2):
      parent1 = selection(population, population_with_fitness)
      parent2 = selection(population, population_with_fitness)
      child = crossover(parent1, parent2)
      next_population+=child
      

def main():
  initial_population = generate_population(start_population, total_transactions)
  genetic_algorithm(initial_population, total_generations)
  

main()
