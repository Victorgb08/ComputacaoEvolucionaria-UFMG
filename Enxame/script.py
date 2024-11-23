from pyswarm import pso

# Definir a função objetivo
def objective_function(x):
    return sum(xi**2 for xi in x)

# Parâmetros do PSO
lb = [-10] * 5  # Limite inferior para cada variável de decisão
ub = [10] * 5   # Limite superior para cada variável de decisão
maxiter = 1000  # Número máximo de iterações
swarmsize = 5  # Tamanho da população (número de partículas)
omega = 0.1     # Fator de inércia
phip = 2        # Coeficiente cognitivo
phig = 2        # Coeficiente social

# Executar o PSO

# Exibir os resultados
for i in range (0,11):
    best_position, best_value = pso(objective_function, lb, ub, swarmsize=swarmsize, maxiter=maxiter, omega=omega, phip=phip, phig=phig)
    print("PSO para omega = ", omega)
    print(f"Melhor posição encontrada: {best_position}")
    print(f"Melhor valor da função objetivo: {best_value}\n")
    omega += 0.1
