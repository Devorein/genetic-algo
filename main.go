package main

import (
	"errors"
	"fmt"
	"math"
	"math/rand"
	"os"
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

func selection(population Population, populationWithFitness PopulationFitness) Chromosome {
	choices := []wr.Choice{}

	for index := 0; index < len(population); index += 1 {
		weight := uint(0)
		if populationWithFitness[index] == 0 {
			weight = 1
		} else {
			weight = uint(populationWithFitness[index])
		}
		choices = append(choices, wr.Choice{
			Weight: weight,
		})
	}

	chooser, _ := wr.NewChooser(choices)

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

		total_transactions, _ := strconv.Atoi(lines[0])
		for index := 0; index < total_transactions; index++ {
			transaction := lines[index+1]
			splitted := strings.Split(transaction, " ")
			transaction_amount, _ := strconv.Atoi(splitted[1])
			transactions = append(transactions, Transaction{direction: splitted[0], amount: transaction_amount})
		}

		totalChromosomes := 10

		initialPopulation := generatePopulation(totalChromosomes, total_transactions)

		fmt.Println(initialPopulation)

		wr.NewChooser(
			wr.Choice{Item: "🍒", Weight: 0},
			wr.Choice{Item: "🍋", Weight: 1},
			wr.Choice{Item: "🍊", Weight: 1},
			wr.Choice{Item: "🍉", Weight: 3},
			wr.Choice{Item: "🥑", Weight: 5},
		)
	}
}
