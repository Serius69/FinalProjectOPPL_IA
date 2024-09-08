# efficiency_improvement.py
import pandas as pd
import numpy as np
from scipy.optimize import minimize


def load_data(file_path):
    """
    Carga los datos de producción desde un archivo CSV.

    Args:
    file_path (str): Ruta al archivo CSV con los datos de producción.

    Returns:
    pd.DataFrame: DataFrame con los datos de producción.
    """
    return pd.read_csv(file_path)


def production_cost(x, data):
    """
    Calcula el costo total de producción basado en la asignación de recursos.

    Args:
    x (np.array): Array con la asignación de recursos.
    data (pd.DataFrame): DataFrame con los datos de producción.

    Returns:
    float: Costo total de producción.
    """
    labor_cost = x[0] * data['labor_rate'].mean()
    material_cost = x[1] * data['material_cost'].mean()
    overhead_cost = x[2] * data['overhead_rate'].mean()
    return labor_cost + material_cost + overhead_cost


def production_output(x, data):
    """
    Calcula la producción total basada en la asignación de recursos.

    Args:
    x (np.array): Array con la asignación de recursos.
    data (pd.DataFrame): DataFrame con los datos de producción.

    Returns:
    float: Producción total.
    """
    return x[0] * data['labor_productivity'].mean() + x[1] * data['material_efficiency'].mean()


def optimize_production(data, budget):
    """
    Optimiza la asignación de recursos para maximizar la producción dentro de un presupuesto.

    Args:
    data (pd.DataFrame): DataFrame con los datos de producción.
    budget (float): Presupuesto total disponible.

    Returns:
    tuple: Asignación óptima de recursos y producción máxima.
    """

    def objective(x):
        return -production_output(x, data)

    def constraint(x):
        return budget - production_cost(x, data)

    x0 = [100, 100, 100]  # Valores iniciales
    bounds = [(0, None), (0, None), (0, None)]  # Límites para cada variable
    cons = {'type': 'ineq', 'fun': constraint}

    result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=cons)

    return result.x, -result.fun


def improve_efficiency(input_file, budget):
    """
    Mejora la eficiencia de producción optimizando la asignación de recursos.

    Args:
    input_file (str): Ruta al archivo CSV con los datos de producción.
    budget (float): Presupuesto total disponible.

    Returns:
    dict: Resultados de la optimización.
    """
    data = load_data(input_file)
    optimal_allocation, max_production = optimize_production(data, budget)

    results = {
        'optimal_labor': optimal_allocation[0],
        'optimal_material': optimal_allocation[1],
        'optimal_overhead': optimal_allocation[2],
        'max_production': max_production,
        'total_cost': production_cost(optimal_allocation, data)
    }

    return results

if __name__ == "__main__":
    input_file = 'production_data.csv'
    budget = 100000  # Ejemplo de presupuesto
    results = improve_efficiency(input_file, budget)
    print("Resultados de la optimización:")
    for key, value in results.items():
        print(f"{key}: {value:.2f}")