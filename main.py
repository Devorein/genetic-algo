from random import randint
from typing import List

Genome = List[int]
Population = List[Genome]

def generate_chromosome(genome_length: int) -> Genome:
  chromosome: List[int] = []

  for _ in range(genome_length):
    chromosome.append(randint(0, 1))

  return chromosome


def generate_population(population_size: int, genome_length: int) -> Population:
  population: Population = []

  for _ in range(population_size):
    population.append(generate_chromosome(genome_length))

  return population

def genetic_algorithm(population_size: int, genome_length: int):
  population = generate_population(population_size, genome_length)

  print(population)


# Driver code
lines = [line.replace("\n", "") for line in open("input.txt").readlines()]

total_transactions = int(lines[0])

transactions = []

for line_num in range(total_transactions):
  transactions.append(lines[line_num + 1])

start_population = 10
mutation_threshold = 0.3
genetic_algorithm(start_population, total_transactions)
