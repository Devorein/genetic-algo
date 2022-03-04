import enum
from random import randint
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
generation_limit = 1

Chromosome = List[int]
Population = List[Chromosome]


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

def generate_population(population_size: int, genome_length: int, mutation_threshold: int) -> Population:
  population: Population = []

  for _ in range(population_size):
    population.append(generate_chromosome(genome_length))

  return population

def genetic_algorithm(generation_limit: int, population_size: int, genome_length: int, mutation_threshold: int):
  for generation_num in range(generation_limit):
    population = generate_population(population_size, genome_length, mutation_threshold)
    population_with_fitness: List[Tuple[int, int]] = []

    for chromosome_num, chromosome in enumerate(population):
      population_with_fitness.append((chromosome_num, fitness(chromosome)))

    print(population_with_fitness)

genetic_algorithm(generation_limit, start_population, total_transactions, mutation_threshold)
