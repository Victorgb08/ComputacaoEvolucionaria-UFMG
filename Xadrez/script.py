import random

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

# Seleção por torneio
def tournament_selection(population, k=3):
    selected = random.sample(population, k)
    selected.sort(key=lambda x: fitness(x))
    return selected[0]

# Cruzamento
def crossover(parent1, parent2):
    crossover_point = random.randint(0, 7)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    print(f"Crossover:\n  Parent1: {parent1}\n  Parent2: {parent2}\n  Point: {crossover_point}\n  Child: {child}")
    return child

# Mutação
def mutate(board):
    original_board = board[:]
    if random.random() < 0.05:  # Taxa de mutação de 5%
        i = random.randint(0, 7)
        board[i] = random.randint(0, 7)
    print(f"Mutate:\n  Original: {original_board}\n  Mutated: {board}")
    return board

# Algoritmo Genético
def genetic_algorithm():
    population_size = 100
    generations = 1000
    population = [create_board() for _ in range(population_size)]

    for generation in range(generations):
        population.sort(key=lambda x: fitness(x))
        current_fitness = fitness(population[0])
        print(f"Geração {generation}: Conflitos = {current_fitness}")
        if current_fitness == 0:
            return population[0]

        new_population = []
        for _ in range(population_size // 2):
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child1 = mutate(crossover(parent1, parent2))
            child2 = mutate(crossover(parent2, parent1))
            new_population.extend([child1, child2])

        population = new_population

    return None

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

# Executar o algoritmo
solution = genetic_algorithm()
if solution:
    print("Solução encontrada:", solution)
    print_board(solution)
else:
    print("Nenhuma solução encontrada.")