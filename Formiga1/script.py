import csv
from pants import World, Solver

# Função para ler os dados do CSV e extrair os custos
def ler_dados_csv(arquivo_csv):
    custos = []
    with open(arquivo_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        linhas = list(reader)
        for i in range(14, 19):  # Linhas onde os custos estão localizados
            linha = linhas[i][1:6]  # Pegar apenas os valores de custo
            custos.append([float(valor.replace(',', '.')) for valor in linha])
    return custos

# Definir a função de comprimento (usando os custos extraídos)
def length(a, b):
    return custos[a][b]

# Ler os dados do CSV
arquivo_csv = 'dados.csv'
custos = ler_dados_csv(arquivo_csv)

# Definir os nós (cidades)
nodes = list(range(len(custos)))

# Criar o mundo com os nós e a função de comprimento
world = World(nodes, length)

# Configurar o solver
solver = Solver()

# Executar o solver para encontrar a melhor solução
solution = solver.solve(world)

# Imprimir a solução encontrada
print("Melhor rota encontrada:")
for node in solution.tour:
    print(node)
print(f"Distância total: {solution.distance}")