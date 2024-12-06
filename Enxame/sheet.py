import numpy as np
import random

# Parâmetros
num_cidades = 5
num_formigas = 10
alfa = 1  # Importância do feromônio
beta = 2  # Importância da visibilidade
evaporação = 0.5
iteracoes = 100

# Matriz de custos (exemplo aleatório)
custos = np.random.randint(10, 100, size=(num_cidades, num_cidades))
np.fill_diagonal(custos, 0)

# Inicialização
feromonio = np.ones((num_cidades, num_cidades))

def calcular_visibilidade(custos):
    """Calcula a visibilidade, que é inversamente proporcional ao custo."""
    visibilidade = 1 / (custos + np.eye(num_cidades))
    np.fill_diagonal(visibilidade, 0)
    return visibilidade

def atualizar_feromonio(feromonio, caminhos, custos, evaporação):
    """Atualiza os níveis de feromônio com base nos caminhos percorridos."""
    feromonio *= (1 - evaporação)  # Evaporação
    for caminho, custo in zip(caminhos, custos):
        for i in range(len(caminho) - 1):
            feromonio[caminho[i], caminho[i+1]] += 1 / custo
    return feromonio

def escolher_proxima_cidade(feromonio, visibilidade, cidade_atual, visitadas):
    """Escolhe a próxima cidade com base na probabilidade."""
    probabilidade = (feromonio[cidade_atual] ** alfa) * (visibilidade[cidade_atual] ** beta)
    probabilidade[visitadas] = 0  # Evita cidades já visitadas
    soma = np.sum(probabilidade)
    return np.random.choice(range(num_cidades), p=probabilidade/soma)

# Algoritmo principal
visibilidade = calcular_visibilidade(custos)
melhor_custo = float('inf')
melhor_caminho = []

for _ in range(iteracoes):
    caminhos = []
    custos_caminhos = []
    for _ in range(num_formigas):
        caminho = [random.randint(0, num_cidades - 1)]
        while len(caminho) < num_cidades:
            cidade_atual = caminho[-1]
            proxima_cidade = escolher_proxima_cidade(feromonio, visibilidade, cidade_atual, caminho)
            caminho.append(proxima_cidade)
        caminho.append(caminho[0])  # Fechando o ciclo
        caminhos.append(caminho)
        custos_caminhos.append(sum(custos[caminho[i], caminho[i+1]] for i in range(len(caminho) - 1)))

    # Atualiza feromônios
    feromonio = atualizar_feromonio(feromonio, caminhos, custos_caminhos, evaporação)

    # Verifica o melhor caminho
    menor_custo_iteracao = min(custos_caminhos)
    if menor_custo_iteracao < melhor_custo:
        melhor_custo = menor_custo_iteracao
        melhor_caminho = caminhos[custos_caminhos.index(melhor_custo)]

print(f"Melhor custo: {melhor_custo}")
print(f"Melhor caminho: {melhor_caminho}")