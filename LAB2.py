import random

# Parameters
population_size = 10
gene_length = 8
mutation_rate = 0.1
crossover_rate = 0.7
max_generations = 5

def generate_population(size, length):
    population = []
    for _ in range(size):
        gene = ''.join(random.choice('01') for _ in range(length))
        population.append(gene)
    return population

def decode_gene(gene):
    decimal_value = int(gene, 2)
    max_value = 2 ** len(gene) - 1
    return decimal_value / max_value  

def evaluate_fitness(solution):
    return 1 - 4 * (solution - 0.5) ** 2

def select_based_on_fitness(population, fitnesses):
    total_fitness = sum(fitnesses)
    if total_fitness == 0:
        return random.choice(population)

    pick = random.uniform(0, total_fitness)
    current = 0
    for gene, fitness in zip(population, fitnesses):
        current += fitness
        if current >= pick:
            return gene
    return population[-1] 

def crossover_at_random_point(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(gene, mutation_rate):
    new_gene = ''
    for bit in gene:
        if random.random() < mutation_rate:
            new_bit = '1' if bit == '0' else '0'
        else:
            new_bit = bit
        new_gene += new_bit
    return new_gene

def gene_expression_algorithm():
    population = generate_population(population_size, gene_length)
    best_solution = None
    best_fitness = float('-inf')

    for generation in range(max_generations):
        # Decode genes
        solutions = [decode_gene(g) for g in population]

        # Evaluate fitness
        fitnesses = [evaluate_fitness(s) for s in solutions]

        # Track best
        max_fit = max(fitnesses)
        if max_fit > best_fitness:
            best_fitness = max_fit
            best_solution = solutions[fitnesses.index(max_fit)]

        # Selection
        mating_pool = []
        while len(mating_pool) < population_size:
            selected = select_based_on_fitness(population, fitnesses)
            mating_pool.append(selected)

        # Crossover
        new_population = []
        for _ in range(population_size // 2):
            parent1 = random.choice(mating_pool)
            parent2 = random.choice(mating_pool)
            if random.random() < crossover_rate:
                child1, child2 = crossover_at_random_point(parent1, parent2)
            else:
                child1, child2 = parent1, parent2
            new_population.extend([child1, child2])

        # Mutation
        new_population = [mutate(g, mutation_rate) for g in new_population]

        # Replace population
        population = new_population

        # Print progress
        print(f"Generation {generation+1}: Best Fitness = {best_fitness:.5f}, Best Solution = {best_solution:.5f}")

    return best_solution, best_fitness

# Run the algorithm
best_sol, best_fit = gene_expression_algorithm()
print(f"\nBest solution found: {best_sol:.5f} with fitness: {best_fit:.5f}")
