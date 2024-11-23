from pyswarm import pso
import numpy as np
import matplotlib.pyplot as plt
import time

# Definir a função objetivo para maximização (negativa para minimização)
def objective_function(x):
    return -sum(xi**3 for xi in x)

# Função PSO personalizada para registrar valores da função objetivo e variar omega
def pso_with_convergence_tracking(func, lb, ub, swarmsize=50, omega_min=0.1, omega_max=1.1, phip=2, phig=2, maxiter=1000):
    assert len(lb) == len(ub), 'Lower- and upper-bounds must be the same length'
    assert hasattr(func, '__call__'), 'Invalid function handle'
    lb = np.array(lb)
    ub = np.array(ub)
    assert np.all(ub > lb), 'All upper-bound values must be greater than lower-bound values'
    
    vhigh = np.abs(ub - lb)
    vlow = -vhigh
    
    obj = lambda x: func(x)
    
    S = swarmsize
    D = len(lb)
    x = np.random.rand(S, D)
    v = np.zeros_like(x)
    p = np.zeros_like(x)
    fp = np.zeros(S)
    g = []
    fg = 1e100
    
    for i in range(S):
        x[i, :] = lb + x[i, :] * (ub - lb)
        p[i, :] = x[i, :]
        fp[i] = obj(p[i, :])
        if i == 0:
            g = p[0, :].copy()
        if fp[i] < fg:
            fg = fp[i]
            g = p[i, :].copy()
        v[i, :] = vlow + np.random.rand(D) * (vhigh - vlow)
    
    it = 1
    convergence_history = []
    while it <= maxiter:
        omega = omega_min + (omega_max - omega_min) * (it / maxiter)
        rp = np.random.uniform(size=(S, D))
        rg = np.random.uniform(size=(S, D))
        for i in range(S):
            v[i, :] = omega * v[i, :] + phip * rp[i, :] * (p[i, :] - x[i, :]) + phig * rg[i, :] * (g - x[i, :])
            x[i, :] = x[i, :] + v[i, :]
            x[i, :] = np.clip(x[i, :], lb, ub)
            fx = obj(x[i, :])
            if fx < fp[i]:
                p[i, :] = x[i, :].copy()
                fp[i] = fx
                if fx < fg:
                    g = x[i, :].copy()
                    fg = fx
        convergence_history.append(-fg)  # Negate to get the actual max value
        it += 1
    
    return g, -fg, convergence_history  # Negate to get the actual max value

# Parâmetros do PSO
lb = [0] * 5  # Limite inferior para cada variável de decisão
ub = [35] * 5  # Limite superior para cada variável de decisão
maxiter = 1000  # Número máximo de iterações
swarmsize = 50  # Tamanho da população (número de partículas)
phip = 2  # Coeficiente cognitivo
phig = 2  # Coeficiente social

# Medir o tempo de execução
start_time = time.time()

# Executar o PSO personalizado
best_position, best_value, convergence_history = pso_with_convergence_tracking(objective_function, lb, ub, swarmsize=swarmsize, maxiter=maxiter, phip=phip, phig=phig)

# Medir o tempo de execução
end_time = time.time()
execution_time = end_time - start_time

# Exibir os resultados
print(f"Melhor posição encontrada: {best_position}")
print(f"Melhor valor da função objetivo: {best_value}")
print(f"Tempo de execução: {execution_time} segundos")

# Plotar a convergência
plt.plot(convergence_history)
plt.xlabel('Iteração')
plt.ylabel('Valor da Função Objetivo')
plt.title('Convergência do PSO')
plt.grid(True)
plt.show()