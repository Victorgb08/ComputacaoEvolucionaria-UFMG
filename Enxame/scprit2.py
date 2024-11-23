from pyswarm import pso
import numpy as np

# Definir a função objetivo
def objective_function(x):
    return sum(xi**2 for xi in x)

# Função PSO personalizada para registrar valores da função objetivo e variar omega
def pso_with_convergence_tracking(func, lb, ub, swarmsize=100, omega_min=0.1, omega_max=1.1, phip=0.5, phig=0.5, maxiter=100, minstep=1e-8, minfunc=1e-8, debug=False):
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
        convergence_history.append(fg)
        it += 1
    
    return g, fg, convergence_history

# Parâmetros do PSO
lb = [-1000] * 5  # Limite inferior para cada variável de decisão
ub = [1000] * 5   # Limite superior para cada variável de decisão
maxiter = 1000  # Número máximo de iterações
swarmsize = 50  # Tamanho da população (número de partículas)
phip = 2        # Coeficiente cognitivo
phig = 2        # Coeficiente social

# Executar o PSO personalizado
for i in range(0,10):
    best_position, best_value, convergence_history = pso_with_convergence_tracking(objective_function, lb, ub, swarmsize=swarmsize, maxiter=maxiter, phip=phip, phig=phig)
    # Exibir os resultados
    print(f"Melhor posição encontrada: {best_position}")
    print(f"Melhor valor da função objetivo: {best_value}")

    # Analisar a convergência
    convergence_threshold = 1e-6
    for i in range(1, len(convergence_history)):
        if abs(convergence_history[i] - convergence_history[i-1]) < convergence_threshold:
            print(f"Convergência detectada na iteração {i}")
            break