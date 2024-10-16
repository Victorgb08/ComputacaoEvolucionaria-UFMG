import random

data = {
    "Item": list(range(1, 23)),
    "Peso (g)": [350, 250, 160, 120, 200, 100, 120, 220, 40, 80, 
                 100, 300, 180, 250, 220, 150, 280, 310, 120, 160, 
                 110, 210],
    "Valor": [300, 400, 450, 350, 250, 300, 200, 250, 150, 400, 
              350, 300, 450, 500, 350, 400, 200, 300, 250, 300, 
              150, 200]
}

def gerar_individuo():
    return ''.join(random.choice('01') for _ in range(22))

def gerar_populacao(tamanho=100):  # Alterado para 5
    return [gerar_individuo() for _ in range(tamanho)]

populacao_inicial = gerar_populacao()

def calcular_fitness(individuo, data, peso_maximo=3000):
    peso_total = 0
    valor_total = 0
    
    for i, bit in enumerate(individuo):
        if bit == '1':
            peso_total += data["Peso (g)"][i]
            valor_total += data["Valor"][i]
            if peso_total > peso_maximo:
                return 0, peso_total  # Excede o peso máximo permitido
    
    return valor_total, peso_total

def selecao_por_torneio(populacao, k=0.75):
    selecionados = []
    for _ in range(len(populacao)):
        # Seleciona dois indivíduos aleatoriamente
        indices = random.sample(range(len(populacao)), 2)
        individuo1, individuo2 = populacao[indices[0]], populacao[indices[1]]

        # Compara as aptidões e seleciona com base em k
        if random.random() < k:
            vencedor = max(individuo1, individuo2, key=lambda x: x[1][0])  # Seleciona pelo fitness
        else:
            vencedor = min(individuo1, individuo2, key=lambda x: x[1][0])  # Seleciona pelo fitness

        selecionados.append(vencedor)

    return selecionados

def crossover(individuo1, individuo2, ponto_crossover):
    filho1 = individuo1[:ponto_crossover] + individuo2[ponto_crossover:]
    filho2 = individuo2[:ponto_crossover] + individuo1[ponto_crossover:]
    return filho1, filho2

def mutacao(individuo, taxa_mutacao=0.01):
    houve_mutacao = False
    individuo_mutado = ''.join(
        bit if random.random() > taxa_mutacao else '1' if bit == '0' else '0'
        for bit in individuo
    )
    if individuo != individuo_mutado:
        houve_mutacao = True
    return individuo_mutado, houve_mutacao

def gerar_proxima_geracao(populacao):
    nova_geracao = []
    mutacoes = []
    tamanho_populacao = len(populacao)
    
    # Garantir que a população tenha um número par de indivíduos
    if tamanho_populacao % 2 != 0:
        populacao.append(populacao[0])  # Adiciona um clone do primeiro indivíduo

    for i in range(0, tamanho_populacao, 2):
        pai1, pai2 = populacao[i][0], populacao[i+1][0]
        ponto_crossover = random.randint(1, 21)
        
        filho1, filho2 = crossover(pai1, pai2, ponto_crossover)
        
        # Aplica mutação nos filhos
        filho1, mutacao1 = mutacao(filho1)
        filho2, mutacao2 = mutacao(filho2)
        
        nova_geracao.append(filho1)
        nova_geracao.append(filho2)
        mutacoes.append(mutacao1)
        mutacoes.append(mutacao2)
    return nova_geracao, mutacoes

# Calcula o fitness da população inicial
fitness_populacao = [(individuo, calcular_fitness(individuo, data)) for individuo in populacao_inicial]

# Exibe a população inicial e seus fitness
print("População Inicial:")
for individuo, (fitness, peso) in fitness_populacao:
    print(f'Indivíduo: {individuo}, Fitness: {fitness}, Peso Total: {peso}')

# Executa o procedimento por 1000 gerações
for geracao in range(1000):
    # Realiza a seleção por torneio
    populacao_selecionada = selecao_por_torneio(fitness_populacao)
    
    # Gera a próxima geração
    proxima_geracao, mutacoes = gerar_proxima_geracao(populacao_selecionada)
    
    # Calcula o fitness da próxima geração
    fitness_populacao = [(individuo, calcular_fitness(individuo, data)) for individuo in proxima_geracao]

# Exibe a última geração e seus fitness
print("\nÚltima Geração:")
for individuo, (fitness, peso), houve_mutacao in zip(proxima_geracao, fitness_populacao, mutacoes):
    print(f'Indivíduo: {individuo}, Fitness: {fitness}, Peso Total: {peso}, Houve Mutação: {houve_mutacao}')