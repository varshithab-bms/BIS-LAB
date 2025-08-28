import random

POP_SIZE = 5
CHROM_LENGTH = 5
MAX_GENERATIONS = 5
MUTATION_RATE = 0.1

def fitness(chromosome):
    x = int(chromosome, 2)
    return x * x

def get_population_from_input():
    population = []
    print(f"Enter {POP_SIZE} chromosomes (each {CHROM_LENGTH} bits, only 0 or 1):")
    while len(population) < POP_SIZE:
        chrom = input(f"Chromosome {len(population) + 1}: ").strip()
        if len(chrom) == CHROM_LENGTH and all(c in '01' for c in chrom):
            population.append(chrom)
        else:
            print(f"Invalid chromosome! Please enter exactly {CHROM_LENGTH} bits (0 or 1).")
    return population

def select(population):
    fitnesses = [fitness(chrom) for chrom in population]
    total_fitness = sum(fitnesses)
    pick = random.uniform(0, total_fitness)
    current = 0
    for i, chrom in enumerate(population):
        current += fitnesses[i]
        if current > pick:
            return chrom

def crossover(parent1, parent2):
    point = random.randint(1, CHROM_LENGTH - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(chromosome):
    mutated = ''
    for bit in chromosome:
        if random.random() < MUTATION_RATE:
            mutated += '1' if bit == '0' else '0'
        else:
            mutated += bit
    return mutated

def genetic_algorithm():
    population = get_population_from_input()
    print(f"Initial Population: {population}")

    for generation in range(MAX_GENERATIONS):
        new_population = []
        while len(new_population) < POP_SIZE:
            parent1 = select(population)
            parent2 = select(population)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            new_population.extend([child1, child2])
       
        population = new_population[:POP_SIZE]

        best = max(population, key=fitness)
        print(f"Generation {generation + 1}: Best Chromosome = {best}, Fitness = {fitness(best)}")

    best_overall = max(population, key=fitness)
    print(f"\nBest solution after {MAX_GENERATIONS} generations: {best_overall} with fitness = {fitness(best_overall)}")

if __name__ == "__main__":
    genetic_algorithm()
