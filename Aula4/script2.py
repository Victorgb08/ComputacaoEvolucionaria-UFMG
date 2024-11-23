import random
import time

# Variáveis globais
TAMANHO_POPULACAO = [10,100,200]
GERACOES = 100
TAXA_MUTACAO = [0.03,0.03,0.03]

class AlgoritmoGenetico:
    def __init__(self, data, num_itens,TAXA_MUTACAO, TAMANHO_POPULACAO, peso_maximo=3000, geracoes=GERACOES):
        self.data = data
        self.num_itens = num_itens
        self.tamanho_populacao = TAMANHO_POPULACAO
        self.peso_maximo = peso_maximo
        self.taxa_mutacao = TAXA_MUTACAO
        self.geracoes = geracoes
        self.populacao_inicial = self.gerar_populacao()

    def gerar_individuo(self):
        return ''.join(random.choice('01') for _ in range(self.num_itens))

    def gerar_populacao(self):
        return [self.gerar_individuo() for _ in range(self.tamanho_populacao)]

    def calcular_fitness(self, individuo):
        peso_total = 0
        valor_total = 0
        
        for i, bit in enumerate(individuo):
            if bit == '1':
                peso_total += self.data["Peso (g)"][i]
                valor_total += self.data["Valor"][i]
                if peso_total > self.peso_maximo:
                    return 0, peso_total  # Excede o peso máximo permitido
        
        return valor_total, peso_total

    def selecao_por_torneio(self, populacao, k=0.75):
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

    def crossover(self, individuo1, individuo2, ponto_crossover):
        filho1 = individuo1[:ponto_crossover] + individuo2[ponto_crossover:]
        filho2 = individuo2[:ponto_crossover] + individuo1[ponto_crossover:]
        return filho1, filho2

    def mutacao(self, individuo):
        houve_mutacao = False
        individuo_mutado = ''.join(
            bit if random.random() > self.taxa_mutacao else '1' if bit == '0' else '0'
            for bit in individuo
        )
        if individuo != individuo_mutado:
            houve_mutacao = True
        return individuo_mutado, houve_mutacao

    def gerar_proxima_geracao(self, populacao):
        nova_geracao = []
        tamanho_populacao = len(populacao)
        
        # Garantir que a população tenha um número par de indivíduos
        if tamanho_populacao % 2 != 0:
            populacao.append(populacao[0])  # Adiciona um clone do primeiro indivíduo

        for i in range(0, tamanho_populacao, 2):
            pai1, pai2 = populacao[i][0], populacao[i+1][0]
            ponto_crossover = random.randint(1, self.num_itens - 1)
            
            filho1, filho2 = self.crossover(pai1, pai2, ponto_crossover)
            
            # Aplica mutação nos filhos
            filho1, _ = self.mutacao(filho1)
            filho2, _ = self.mutacao(filho2)
            
            nova_geracao.append(filho1)
            nova_geracao.append(filho2)
        return nova_geracao

    def executar(self):
        # Marca o tempo de início
        tempo_inicio = time.time()

        # Lista para armazenar o fitness total de cada geração
        fitness_total_por_geracao = []
        fitness_maximo = 0
        melhor_individuo = ""
        geracao_melhor_individuo = 0

        # Calcula o fitness da população inicial
        fitness_populacao = [(individuo, self.calcular_fitness(individuo)) for individuo in self.populacao_inicial]

        # Calcula o fitness total da população inicial
        fitness_total = sum(fitness for _, (fitness, _) in fitness_populacao)
        fitness_total_por_geracao.append(fitness_total)

        # Atualiza o fitness máximo
        for individuo, (fitness, _) in fitness_populacao:
            if fitness > fitness_maximo:
                fitness_maximo = fitness
                melhor_individuo = individuo
                geracao_melhor_individuo = 0

        # Executa o procedimento por 1000 gerações
        for geracao in range(1, self.geracoes + 1):
            # Realiza a seleção por torneio
            populacao_selecionada = self.selecao_por_torneio(fitness_populacao)
            
            # Gera a próxima geração
            proxima_geracao = self.gerar_proxima_geracao(populacao_selecionada)
            
            # Calcula o fitness da próxima geração
            fitness_populacao = [(individuo, self.calcular_fitness(individuo)) for individuo in proxima_geracao]

            # Calcula o fitness total da próxima geração
            fitness_total = sum(fitness for _, (fitness, _) in fitness_populacao)
            fitness_total_por_geracao.append(fitness_total)

            # Atualiza o fitness máximo
            for individuo, (fitness, _) in fitness_populacao:
                if fitness > fitness_maximo:
                    fitness_maximo = fitness
                    melhor_individuo = individuo
                    geracao_melhor_individuo = geracao

        # Marca o tempo de fim
        tempo_fim = time.time()

        # Calcula o tempo de execução
        tempo_execucao = tempo_fim - tempo_inicio

        # Exibe o fitness máximo encontrado, a sequência de bits correspondente e o tempo de execução
        print(f"\nFitness Máximo Encontrado: {fitness_maximo}")
        # print(f"Melhor Individuo: {melhor_individuo}")
        # print(f"Geracao do Melhor Individuo: {geracao_melhor_individuo}")
        print(f"Tempo de Execução: {tempo_execucao:.2f} segundos")
        print(f'População: {self.tamanho_populacao}')

# Dados de entrada
data = {
    "Item": list(range(1, 23)),
    "Peso (g)": [350, 250, 160, 120, 200, 100, 120, 220, 40, 80, 
                 100, 300, 180, 250, 220, 150, 280, 310, 120, 160, 
                 110, 210],
    "Valor": [300, 400, 450, 350, 250, 300, 200, 250, 150, 400, 
              350, 300, 450, 500, 350, 400, 200, 300, 250, 300, 
              150, 200]
}

num_itens = [22,22,22]

for j in range(0,3):
    for i in range(0,3):
        algoritmo_genetico = AlgoritmoGenetico(data, num_itens[i],TAXA_MUTACAO[i],TAMANHO_POPULACAO[i])
        algoritmo_genetico.executar()
