# efficiency_improvement.py
import numpy as np
from scipy.optimize import minimize
from analyzer.models import LogisticProcess, Optimization, ExchangeRate

def load_data():
    """
    Carga los datos de procesos logísticos desde la base de datos.

    Returns:
    QuerySet: Conjunto de datos de procesos logísticos.
    """
    return LogisticProcess.objects.all()

def load_optimization_data(logistic_process_id):
    """
    Carga los datos de optimización para un proceso logístico específico.

    Args:
    logistic_process_id (int): ID del proceso logístico.

    Returns:
    Optimization: Datos de optimización del proceso logístico.
    """
    return Optimization.objects.filter(logistic_process_id=logistic_process_id).first()

def exchange_cost(x, optimization, exchange_rate):
    """
    Calcula el costo total basado en la asignación de recursos y el tipo de cambio.

    Args:
    x (np.array): Array con la asignación de recursos.
    optimization (Optimization): Datos de optimización para el proceso logístico.
    exchange_rate (ExchangeRate): Tipo de cambio actual.

    Returns:
    float: Costo total.
    """
    return (1 - optimization.cost_reduction / 100) * x[0] * exchange_rate.rate

def exchange_volume(x, optimization):
    """
    Calcula el volumen de intercambio basado en la asignación de recursos.

    Args:
    x (np.array): Array con la asignación de recursos.
    optimization (Optimization): Datos de optimización para el proceso logístico.

    Returns:
    float: Volumen de intercambio total.
    """
    return x[0] * (1 + optimization.efficiency_improvement / 100)

def optimize_exchange(logistic_process_id, budget):
    """
    Optimiza la asignación de recursos para maximizar el volumen de intercambio dentro de un presupuesto.

    Args:
    logistic_process_id (int): ID del proceso logístico.
    budget (float): Presupuesto total disponible.

    Returns:
    tuple: Asignación óptima de recursos y volumen máximo de intercambio.
    """
    optimization = load_optimization_data(logistic_process_id)
    if not optimization:
        raise ValueError("Optimization data not found for the given logistic process.")

    logistic_process = LogisticProcess.objects.get(id=logistic_process_id)
    exchange_rate = ExchangeRate.objects.filter(
        from_currency=logistic_process.transactions.first().from_currency,
        to_currency=logistic_process.transactions.first().to_currency,
        date=logistic_process.start_date
    ).first()

    if not exchange_rate:
        raise ValueError("Exchange rate not found for the given currencies and date.")

    def objective(x):
        return -exchange_volume(x, optimization)

    def constraint(x):
        return budget - exchange_cost(x, optimization, exchange_rate)

    x0 = [1000]  # Valor inicial
    bounds = [(0, None)]  # Límite para la variable
    cons = {'type': 'ineq', 'fun': constraint}

    result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=cons)

    return result.x, -result.fun

def improve_efficiency(logistic_process_id, budget):
    """
    Mejora la eficiencia del proceso de cambio de divisas optimizando la asignación de recursos.

    Args:
    logistic_process_id (int): ID del proceso logístico.
    budget (float): Presupuesto total disponible.

    Returns:
    dict: Resultados de la optimización.
    """
    optimal_allocation, max_volume = optimize_exchange(logistic_process_id, budget)

    optimization = load_optimization_data(logistic_process_id)
    logistic_process = LogisticProcess.objects.get(id=logistic_process_id)
    exchange_rate = ExchangeRate.objects.filter(
        from_currency=logistic_process.transactions.first().from_currency,
        to_currency=logistic_process.transactions.first().to_currency,
        date=logistic_process.start_date
    ).first()

    results = {
        'optimal_resource_allocation': optimal_allocation[0],
        'max_exchange_volume': max_volume,
        'total_cost': exchange_cost(optimal_allocation, optimization, exchange_rate),
        'from_currency': exchange_rate.from_currency.code,
        'to_currency': exchange_rate.to_currency.code,
        'exchange_rate': exchange_rate.rate
    }

    return results

if __name__ == "__main__":
    logistic_process_id = 1  # ID del proceso logístico a optimizar
    budget = 100000  # Ejemplo de presupuesto
    results = improve_efficiency(logistic_process_id, budget)
    print("Resultados de la optimización:")
    for key, value in results.items():
        print(f"{key}: {value}")