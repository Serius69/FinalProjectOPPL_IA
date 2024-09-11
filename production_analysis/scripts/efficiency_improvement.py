import numpy as np
from scipy.optimize import minimize
from analyzer.models import LogisticProcess, ExchangeRate, Transaction

def load_data():
    """
    Carga los datos de procesos logísticos desde la base de datos.
    
    Returns:
    QuerySet: Conjunto de datos de procesos logísticos.
    """
    return LogisticProcess.objects.all()

def load_transactions(logistic_process_id):
    """
    Carga las transacciones asociadas a un proceso logístico específico.

    Args:
    logistic_process_id (int): ID del proceso logístico.

    Returns:
    QuerySet: Conjunto de transacciones.
    """
    return Transaction.objects.filter(logistic_process_id=logistic_process_id)

def exchange_cost(x, exchange_rate):
    """
    Calcula el costo total basado en la asignación de recursos y el tipo de cambio.

    Args:
    x (np.array): Array con la asignación de recursos.
    exchange_rate (ExchangeRate): Tipo de cambio actual.

    Returns:
    float: Costo total.
    """
    return x[0] * exchange_rate.rate

def exchange_volume(x, efficiency_improvement):
    """
    Calcula el volumen de intercambio basado en la asignación de recursos y el porcentaje de mejora de eficiencia.

    Args:
    x (np.array): Array con la asignación de recursos.
    efficiency_improvement (float): Porcentaje de mejora de eficiencia.

    Returns:
    float: Volumen de intercambio total.
    """
    return x[0] * (1 + efficiency_improvement / 100)

def optimize_exchange(logistic_process_id, budget, efficiency_improvement):
    """
    Optimiza la asignación de recursos para maximizar el volumen de intercambio dentro de un presupuesto.

    Args:
    logistic_process_id (int): ID del proceso logístico.
    budget (float): Presupuesto total disponible.
    efficiency_improvement (float): Porcentaje de mejora de la eficiencia.

    Returns:
    tuple: Asignación óptima de recursos y volumen máximo de intercambio.
    """
    # Obtener el proceso logístico
    logistic_process = LogisticProcess.objects.get(id=logistic_process_id)
    
    # Obtener la primera transacción asociada para obtener el tipo de cambio
    transaction = logistic_process.transactions.first()
    
    if not transaction:
        raise ValueError("No transactions found for the given logistic process.")

    # Buscar el tipo de cambio para las monedas y la fecha
    exchange_rate = ExchangeRate.objects.filter(
        from_currency=transaction.from_currency,
        to_currency=transaction.to_currency,
        date__lte=logistic_process.start_date  # Permitir fechas anteriores o iguales
    ).order_by('-date').first()

    if not exchange_rate:
        raise ValueError(f"No exchange rate found for currencies {transaction.from_currency} to {transaction.to_currency} on or before date {logistic_process.start_date}.")

    def objective(x):
        return -exchange_volume(x, efficiency_improvement)

    def constraint(x):
        return budget - exchange_cost(x, exchange_rate)

    x0 = [1000]  # Valor inicial
    bounds = [(0, None)]  # Límite para la variable
    cons = {'type': 'ineq', 'fun': constraint}

    result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=cons)

    return result.x, -result.fun

def improve_efficiency(logistic_process_id, budget, efficiency_improvement):
    """
    Mejora la eficiencia del proceso de cambio de divisas optimizando la asignación de recursos.

    Args:
    logistic_process_id (int): ID del proceso logístico.
    budget (float): Presupuesto total disponible.
    efficiency_improvement (float): Porcentaje de mejora de la eficiencia.

    Returns:
    dict: Resultados de la optimización.
    """
    optimal_allocation, max_volume = optimize_exchange(logistic_process_id, budget, efficiency_improvement)

    # Volver a obtener la tasa de cambio para los resultados
    logistic_process = LogisticProcess.objects.get(id=logistic_process_id)
    transaction = logistic_process.transactions.first()
    exchange_rate = ExchangeRate.objects.filter(
        from_currency=transaction.from_currency,
        to_currency=transaction.to_currency,
        date__lte=logistic_process.start_date
    ).order_by('-date').first()

    results = {
        'optimal_resource_allocation': optimal_allocation[0],
        'max_exchange_volume': max_volume,
        'total_cost': exchange_cost(optimal_allocation, exchange_rate),
        'from_currency': exchange_rate.from_currency.code,
        'to_currency': exchange_rate.to_currency.code,
        'exchange_rate': exchange_rate.rate
    }

    return results
