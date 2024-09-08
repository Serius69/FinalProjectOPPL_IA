# performance_analysis.py

import pandas as pd
import numpy as np
from scipy import stats


def load_data(file_path):
    """
    Carga los datos de producción desde un archivo CSV.

    Args:
    file_path (str): Ruta al archivo CSV con los datos de producción.

    Returns:
    pd.DataFrame: DataFrame con los datos de producción.
    """
    return pd.read_csv(file_path)


def calculate_kpis(data):
    """
    Calcula los KPIs clave para el análisis de desempeño de producción.

    Args:
    data (pd.DataFrame): DataFrame con los datos de producción.

    Returns:
    dict: Diccionario con los KPIs calculados.
    """
    kpis = {
        'produccion_promedio': data['production'].mean(),
        'costo_total_promedio': data[['labor_cost', 'material_cost', 'overhead_cost']].sum(axis=1).mean(),
        'eficiencia_promedio': data['efficiency'].mean(),
        'tiempo_produccion_promedio': data['production_time'].mean(),
        'desperdicio_material_promedio': data['material_waste'].mean(),
    }
    return kpis


def analyze_correlations(data):
    """
    Analiza las correlaciones entre las variables clave de producción.

    Args:
    data (pd.DataFrame): DataFrame con los datos de producción.

    Returns:
    pd.DataFrame: Matriz de correlación.
    """
    variables = ['production', 'labor_cost', 'material_cost', 'overhead_cost', 'efficiency', 'production_time',
                 'material_waste']
    return data[variables].corr()


def compare_scenarios(data, scenario1, scenario2):
    """
    Compara dos escenarios de producción utilizando una prueba t.

    Args:
    data (pd.DataFrame): DataFrame con los datos de producción.
    scenario1 (str): Nombre de la columna para el escenario 1.
    scenario2 (str): Nombre de la columna para el escenario 2.

    Returns:
    dict: Resultados de la comparación, incluyendo estadísticas y valor p.
    """
    t_stat, p_value = stats.ttest_ind(data[scenario1], data[scenario2])
    return {
        'escenario1_media': data[scenario1].mean(),
        'escenario2_media': data[scenario2].mean(),
        'diferencia_media': data[scenario1].mean() - data[scenario2].mean(),
        'estadistica_t': t_stat,
        'valor_p': p_value
    }


def analyze_trends(data):
    """
    Analiza las tendencias en la producción y costos a lo largo del tiempo.

    Args:
    data (pd.DataFrame): DataFrame con los datos de producción.

    Returns:
    dict: Resultados del análisis de tendencias.
    """
    data['date'] = pd.to_datetime(data['date'])
    monthly_production = data.groupby(data['date'].dt.to_period('M'))['production'].mean()
    monthly_costs = data.groupby(data['date'].dt.to_period('M'))[['labor_cost', 'material_cost', 'overhead_cost']].sum()

    production_trend = np.polyfit(range(len(monthly_production)), monthly_production, 1)
    cost_trend = np.polyfit(range(len(monthly_costs)), monthly_costs.sum(axis=1), 1)

    return {
        'produccion_tendencia': production_trend[0],
        'costo_tendencia': cost_trend[0]
    }


def perform_analysis(input_file):
    """
    Realiza un análisis completo de desempeño de la producción.

    Args:
    input_file (str): Ruta al archivo CSV con los datos de producción.

    Returns:
    dict: Resultados completos del análisis de desempeño.
    """
    data = load_data(input_file)

    results = {
        'kpis': calculate_kpis(data),
        'correlaciones': analyze_correlations(data),
        'comparacion_escenarios': compare_scenarios(data, 'production_scenario1', 'production_scenario2'),
        'tendencias': analyze_trends(data)
    }

    return results

def print_analysis_results(results):
    """
    Imprime los resultados del análisis de desempeño de forma legible.

    Args:
    results (dict): Resultados del análisis de desempeño.
    """
    print("Análisis de Desempeño de Producción")
    print("===================================")

    print("\nKPIs:")
    for kpi, value in results['kpis'].items():
        print(f"  {kpi}: {value:.2f}")

    print("\nCorrelaciones principales:")
    corr_matrix = results['correlaciones']
    for var1 in corr_matrix.index:
        for var2 in corr_matrix.columns:
            if var1 != var2 and abs(corr_matrix.loc[var1, var2]) > 0.5:
                print(f"  {var1} vs {var2}: {corr_matrix.loc[var1, var2]:.2f}")

    print("\nComparación de Escenarios:")
    scenario_comp = results['comparacion_escenarios']
    print(f"  Diferencia media: {scenario_comp['diferencia_media']:.2f}")
    print(f"  Valor p: {scenario_comp['valor_p']:.4f}")

    print("\nTendencias:")
    trends = results['tendencias']
    print(f"  Tendencia de producción: {trends['produccion_tendencia']:.2f} unidades/mes")
    print(f"  Tendencia de costos: {trends['costo_tendencia']:.2f} $/mes")

if __name__ == "__main__":
    input_file = 'production_data.csv'
    results = perform_analysis(input_file)
    print_analysis_results(results)


