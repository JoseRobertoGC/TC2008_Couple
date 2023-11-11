import pandas as pd
import matplotlib.pyplot as plt
from model import CarModel

def run_model(width, height, n_agents, free_cell_percentage, max_time):
    model = CarModel(width, height, n_agents, free_cell_percentage, max_time)
    while model.running:
        model.step()
    return model.datacollector.get_model_vars_dataframe()

# Parámetros del modelo
width = 10
height = 10
n_agents = 3
free_cell_percentage = 80
max_time = 100
num_runs = 50  # Número de veces que desea ejecutar la simulación

# Almacenar los resultados de todas las ejecuciones
all_results = []

for i in range(num_runs):
    print(f"Running simulation {i+1}/{num_runs}")
    results = run_model(width, height, n_agents, free_cell_percentage, max_time)
    all_results.append(results.iloc[-1])  # Solo tomar el último valor de cada simulación

# Convertir a DataFrame
final_results = pd.DataFrame(all_results)


print(final_results)


# Graficar los resultados
plt.figure(figsize=(15, 5))

# Número de colisiones
plt.subplot(1, 3, 1)
plt.bar(range(num_runs), final_results['Number of Collisions'])
plt.title("Número de Colisiones")
plt.xlabel("Simulación")
plt.ylabel("Colisiones")

# Velocidad promedio
plt.subplot(1, 3, 2)
plt.bar(range(num_runs), final_results['Average Speed'])
plt.title("Velocidad Promedio")
plt.xlabel("Simulación")
plt.ylabel("Velocidad")

# Movimientos totales
plt.subplot(1, 3, 3)
plt.bar(range(num_runs), final_results['Total Movements'])
plt.title("Movimientos Totales")
plt.xlabel("Simulación")
plt.ylabel("Movimientos")

plt.tight_layout()
plt.show()