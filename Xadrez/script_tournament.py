import random
import matplotlib.pyplot as plt

# Representação do tabuleiro
def create_board():
    return [random.randint(0, 7) for _ in range(8)]

# Avaliação da aptidão
def fitness(board):
    conflicts = 0
    for i in range(len(board)):
        for j in range(i + 1, len(board)):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts

# Seleção por torneio com chance de 20% do indivíduo com menor aptidão ganhar
def tournament_selection(population, p=0.8):
    selected = random.sample(population, 2)
    if random.random() < p:
        return min(selected, key=lambda x: fitness(x))
    else:
        return max(selected, key=lambda x: fitness(x))

# Cruzamento
def crossover(parent1, parent2):
    crossover_point = random.randint(0, 7)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

# Mutação
def mutate(board):
    original_board = board[:]
    if random.random() < 0.05:  # Taxa de mutação de 5%
        i = random.randint(0, 7)
        board[i] = random.randint(0, 7)
    return board

# Algoritmo Genético
def genetic_algorithm(pop,gen):
    population_size = pop
    generations = gen
    population = [create_board() for _ in range(population_size)]
    fitness_over_time = []

    for generation in range(generations):
        population.sort(key=lambda x: fitness(x))
        current_fitness = fitness(population[0])
        fitness_over_time.append(current_fitness)
        if current_fitness == 0:
            return population[0], generation, fitness_over_time

        new_population = []
        for _ in range(population_size // 2):
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child1 = mutate(crossover(parent1, parent2))
            child2 = mutate(crossover(parent2, parent1))
            new_population.extend([child1, child2])

        population = new_population

    return None, generations, fitness_over_time

# Função para desenhar o tabuleiro
def print_board(board):
    for row in range(8):
        line = ""
        for col in range(8):
            if board[col] == row:
                line += "Q "
            else:
                line += ". "
        print(line)
    print("\n")

pop = [200, 300, 400, 500, 600, 700, 800, 900, 1000]
gen = [100,100,100,100,100,100,100,100,100]
# Executar o algoritmo e armazenar os dados para o gráfico
for i in range(len(pop)):
    solution, generation, fitness_over_time = genetic_algorithm(pop[i], gen[i])
    if solution:
        print(f"Geração {generation}: {solution}  (pop = {pop[i]})")
        # print_board(solution)
    else:
        print("Nenhuma solução encontrada.")
    
    # Plotar o gráfico
    plt.plot(range(len(fitness_over_time)), fitness_over_time, label=f'População {pop[i]}')

plt.xlabel('Gerações')
plt.ylabel('Fitness')
plt.title('Fitness ao longo das gerações')
plt.legend()
plt.show()