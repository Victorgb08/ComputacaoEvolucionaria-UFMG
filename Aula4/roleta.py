import random

def selecao_proporcional(populacao):
  """Implementa a seleção proporcional.

  Args:
    populacao: Uma lista de indivíduos, onde cada indivíduo é uma tupla (indivíduo, aptidão).

  Returns:
    Uma lista com os indivíduos selecionados.
  """

  # Calcula a soma total da aptidão
  soma_aptidao = sum(aptidao for _, aptidao in populacao)

  # Seleciona os indivíduos
  selecionados = []
  for _ in range(len(populacao)):
    r = random.uniform(0, soma_aptidao)
    soma_atual = 0
    for individuo, aptidao in populacao:
      soma_atual += aptidao
      if soma_atual >= r:
        selecionados.append(individuo)
        break

  return selecionados

# Exemplo de uso:
populacao = [
  ('Indivíduo A', 5),
  ('Indivíduo B', 3),
  ('Indivíduo C', 8),
  ('Indivíduo D', 2)
]

selecionados = selecao_proporcional(populacao)
print(selecionados)