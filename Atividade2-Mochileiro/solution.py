items = [
    {"name": "Headphone", "weight": 160, "interest": 150},
    {"name": "Laptop", "weight": 2200, "interest": 500},
    {"name": "Caneca", "weight": 350, "interest": 60},
    {"name": "Garrafa", "weight": 192, "interest": 30},
    {"name": "Caderno", "weight": 333, "interest": 40}
]

max_weight = 3000

# Função para calcular o peso total e o interesse total de uma combinação de itens
def calculate_combination_value(combination):
    total_weight = sum(item['weight'] for item in combination)
    total_interest = sum(item['interest'] for item in combination)
    return total_weight, total_interest

best_combination = None
best_interest = 0
best_weight = 0

# Verificar todas as combinações possíveis de três itens sem usar itertools
n = len(items)
for i in range(n):
    for j in range(i + 1, n):
        for k in range(j + 1, n):
            combination = [items[i], items[j], items[k]]
            total_weight, total_interest = calculate_combination_value(combination)
            if total_weight <= max_weight and total_interest > best_interest:
                best_combination = combination
                best_interest = total_interest
                best_weight = total_weight

# Imprimir a melhor combinação encontrada
if best_combination:
    print("Melhor combinação de itens:")
    for item in best_combination:
        print(f"{item['name']} - Peso: {item['weight']}g, Interesse: {item['interest']}")
    print(f"Interesse total: {best_interest}")
    print(f'Peso total: {best_weight}g')
else:
    print("Nenhuma combinação válida encontrada.")