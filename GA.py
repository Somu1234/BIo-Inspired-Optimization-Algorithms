import string
import random

POPULATION_SIZE = 200
GENES =  string.ascii_lowercase + string.ascii_uppercase + ' 0123456789'
TARGET = 'I am Soumya Somani'

def fitness(chromosome):
    global TARGET
    fitness = 0
    for genes, genet in zip(chromosome, TARGET):
        if genes != genet:
            fitness += 1
    return fitness

def createPopulation():
    global TARGET
    pop_len = len(TARGET)
    return ''.join([mutation() for _ in range(pop_len)])

def selection(population):
    global POPULATION_SIZE
    s = int(0.1 * POPULATION_SIZE)
    new_population = {k : population[k] for k in list(population)[:s]}
    s = int(0.9 * POPULATION_SIZE)
    for _ in range(s):
        parent1 = random.choice(list(population)[:50])
        parent2 = random.choice(list(population)[50:])
        child = crossover(parent1, parent2)
        new_population[child] = fitness(child)
    return new_population

def mutation():
    global GENES
    gene = random.choice(GENES)
    return gene

def crossover(parent1, parent2):
    child_chromosome = []
    for gene1, gene2 in zip(parent1, parent2):
        p = random.random()
        if p < 0.45:
                child_chromosome.append(gene1)
        elif p < 0.90:
                child_chromosome.append(gene2)
        else:
            child_chromosome.append(mutation())
    return ''.join(child_chromosome)

if __name__ == '__main__':
    generation = 1
    convergence = False
    population = {}
    
    for _ in range(POPULATION_SIZE):
        chromosome = createPopulation()
        population[chromosome] = fitness(chromosome)

    while not convergence:
        population = dict(sorted(population.items(), key = lambda item: item[1]))
        
        if list(population.values())[0] <= 0:
            convergence = True
            print('{}\t\t Output: {} \t Fitness: {}'.format(generation, list(population.items())[0][0], list(population.items())[0][1]))
            break

        population = selection(population)
        print('{}\t\t Output: {} \t Fitness: {}'.format(generation, list(population.items())[0][0], list(population.items())[0][1]))
        generation += 1
