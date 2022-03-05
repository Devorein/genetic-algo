package main

import (
	"errors"
	"fmt"
	"math"
	"math/rand"
	"os"
	"sort"
	"strconv"
	"strings"
	"time"

	wr "github.com/mroth/weightedrand"
)

type Transaction struct {
	direction string
	amount    int
}

type PopulationFitnessStruct struct {
	index   int
	fitness int
}

type Chromosome []int
type Population []Chromosome
type PopulationFitness []int
type PopulationFitnessWithIndex []PopulationFitnessStruct

var transactions = []Transaction{}

func generateChromosome(genomeLength int) Chromosome {
	chromosome := Chromosome{}

	totalOneCount := 0

	for totalOneCount == 0 {
		totalOneCount = 0
		chromosome = Chromosome{}
		for index := 0; index < genomeLength; index += 1 {
			genome := rand.Intn(2)

			if genome == 1 {
				totalOneCount += 1
			}

			chromosome = append(chromosome, genome)
		}
	}

	return chromosome
}

func generatePopulation(populationSize int, genomeLength int) Population {
	population := Population{}

	for index := 0; index < populationSize; index += 1 {
		population = append(population, generateChromosome(genomeLength))
	}

	return population
}

func fitness(chromosome Chromosome) int {
	fitness_value := 0

	for index := 0; index < len(chromosome); index += 1 {
		if chromosome[index] == 1 {
			transaction := transactions[index]

			if transaction.direction == "l" {
				fitness_value -= transaction.amount
			} else {
				fitness_value += transaction.amount
			}
		}
	}

	return int(math.Abs(float64(fitness_value)))
}

func selection(population Population, weights []uint, totalChoices uint) []Chromosome {
	choices := []wr.Choice{}

	for index := 0; index < len(population); index += 1 {
		choices = append(choices, wr.Choice{
			Weight: weights[index],
			Item:   population[index],
		})
	}

	chooser, _ := wr.NewChooser(choices...)

	chosenChromosomes := []Chromosome{}

	for index := 0; index < int(totalChoices); index += 1 {
		chosenChromosomes = append(chosenChromosomes, chooser.Pick().(Chromosome))
	}

	return chosenChromosomes
}

func crossover(parent1 Chromosome, parent2 Chromosome) Chromosome {
	randomGenome := rand.Intn(len(parent1))
	chromosome := Chromosome{}
	parent1Slice := parent1[0:randomGenome]
	parent2Slice := parent2[randomGenome:]
	for index := 0; index < len(parent1Slice); index += 1 {
		chromosome = append(chromosome, parent1Slice[index])
	}

	for index := 0; index < len(parent2Slice); index += 1 {
		chromosome = append(chromosome, parent2Slice[index])
	}
	return chromosome
}

func mutation(chromosome Chromosome, mutationThreshold float32) {
	randomIndex1 := rand.Intn(len(chromosome))
	randomIndex2 := rand.Intn(len(chromosome))

	if rand.Float32() > mutationThreshold {
		randomIndex1Value := chromosome[randomIndex1]
		chromosome[randomIndex1] = chromosome[randomIndex2]
		chromosome[randomIndex2] = randomIndex1Value
	}
}

func geneticAlgorithm(population Population, totalGenerations int, fitnessTarget int, mutationThreshold float32) string {
	targetChromosome := Chromosome{}

	for generationNumber := 0; generationNumber < totalGenerations; generationNumber += 1 {
		populationWithFitness := PopulationFitness{}
		populationWithFitnessAndIndex := PopulationFitnessWithIndex{}
		maxFitnessValue := 0

		for chromosomeNumber := 0; chromosomeNumber < len(population); chromosomeNumber += 1 {
			chromosome := population[chromosomeNumber]

			fitnessValue := fitness(chromosome)

			if fitnessValue > maxFitnessValue {
				maxFitnessValue = fitnessValue
			}

			populationWithFitness = append(populationWithFitness, fitnessValue)
			populationWithFitnessAndIndex = append(populationWithFitnessAndIndex, PopulationFitnessStruct{
				index:   chromosomeNumber,
				fitness: fitnessValue,
			})
		}

		sort.Slice(populationWithFitnessAndIndex[:], func(i, j int) bool {
			return populationWithFitnessAndIndex[i].fitness < populationWithFitnessAndIndex[j].fitness
		})

		if populationWithFitnessAndIndex[0].fitness == fitnessTarget {
			targetChromosome = population[populationWithFitnessAndIndex[0].index]
			break
		}

		nextPopulation := Population{
			population[populationWithFitnessAndIndex[0].index],
			population[populationWithFitnessAndIndex[1].index],
		}

		weights := []uint{}

		for index := 0; index < len(populationWithFitness); index += 1 {
			weights = append(weights, uint(maxFitnessValue-populationWithFitness[index]))
		}

		for index := 0; index < len(population)-2; index += 1 {
			parents := selection(population, weights, 2)
			child := crossover(parents[0], parents[1])

			genomeSummation := 0

			for genomeNumber := 0; genomeNumber < len(child); genomeNumber += 1 {
				genomeSummation += child[genomeNumber]
			}

			for genomeSummation == 0 {
				genomeSummation = 0
				child = crossover(parents[0], parents[1])
				for genomeNumber := 0; genomeNumber < len(child); genomeNumber += 1 {
					genomeSummation += child[genomeNumber]
				}
			}

			mutation(child, mutationThreshold)

			nextPopulation = append(nextPopulation, child)
		}

		population = nextPopulation
	}

	if len(targetChromosome) == 0 {
		return "-1"
	}

	stringifiedChromosome := ""

	for genomeNumber := 0; genomeNumber < len(targetChromosome); genomeNumber += 1 {
		stringifiedChromosome = stringifiedChromosome + fmt.Sprint(targetChromosome[genomeNumber])
	}

	return stringifiedChromosome
}

func main() {
	rand.Seed(time.Now().UTC().UnixNano()) // always seed random!

	textContent, err := os.ReadFile("input.txt")
	// Check for error
	if err != nil {
		if errors.Is(err, os.ErrNotExist) {
			fmt.Println("Please provide input.txt file")
		} else {
			panic(err)
		}
	} else {
		lines := strings.Split(string(textContent), "\r\n")

		totalTransactions, _ := strconv.Atoi(lines[0])
		for index := 0; index < totalTransactions; index++ {
			transaction := lines[index+1]
			splitted := strings.Split(transaction, " ")
			transaction_amount, _ := strconv.Atoi(splitted[1])
			transactions = append(transactions, Transaction{direction: splitted[0], amount: transaction_amount})
		}

		totalChromosomes := 50
		totalGenerations := 25
		mutationThreshold := float32(0.5)

		totalRuns := 10
		totalCorrect := 0
		for runCount := 0; runCount < totalRuns; runCount += 1 {
			initialPopulation := generatePopulation(totalChromosomes, totalTransactions)
			targetChromosome := geneticAlgorithm(initialPopulation, totalGenerations, 0, mutationThreshold)
			if targetChromosome == "1011010" {
				totalCorrect += 1
			}
		}

		fmt.Println((float64(totalCorrect) / float64(totalRuns)) * 100)
	}
}
