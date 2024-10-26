import random

def selecao_por_torneio(populacao, k=0.75):
  """Implementa a seleção por torneio com probabilidade k de escolher o melhor.

  Args:
    populacao: Uma lista de indivíduos, onde cada indivíduo é uma tupla (indivíduo, aptidão).
    k: A probabilidade de escolher o melhor indivíduo (default: 0.75).

  Returns:
    Uma lista com os indivíduos selecionados.
  """

  selecionados = []
  for _ in range(len(populacao)):
    # Seleciona dois indivíduos aleatoriamente
    indices = random.sample(range(len(populacao)), 2)
    individuo1, individuo2 = populacao[indices[0]], populacao[indices[1]]

    # Compara as aptidões e seleciona com base em k
    if random.random() < k:
      selecionados.append(max(individuo1, individuo2, key=lambda x: x[1]))
    else:
      selecionados.append(min(individuo1, individuo2, key=lambda x: x[1]))

  return selecionados

# Exemplo de uso:
populacao = [
  ('Indivíduo A', 5),
  ('Indivíduo B', 3),
  ('Indivíduo C', 8),
  ('Indivíduo D', 2)
]

selecionados = selecao_por_torneio(populacao)
print(selecionados)