# performance_analysis.py
import pandas as pd
import numpy as np
from scipy import stats
from analyzer.models import LogisticProcess, Transaction, ExchangeRate, Optimization

def load_data():
    logistic_processes = LogisticProcess.objects.all().values(
        'id', 'currency_exchange_house__name', 'process_type__name', 'start_date', 'end_date', 'status'
    )
    transactions = Transaction.objects.all().values(
        'logistic_process_id', 'date', 'from_currency__code', 'to_currency__code', 'amount', 'exchange_rate__rate'
    )
    optimizations = Optimization.objects.all().values(
        'logistic_process_id', 'efficiency_improvement', 'cost_reduction', 'processing_time_reduction'
    )

    df_processes = pd.DataFrame(list(logistic_processes))
    df_transactions = pd.DataFrame(list(transactions))
    df_optimizations = pd.DataFrame(list(optimizations))

    # Convertir columnas a tipos numéricos
    df_transactions['amount'] = pd.to_numeric(df_transactions['amount'], errors='coerce')
    df_transactions['exchange_rate__rate'] = pd.to_numeric(df_transactions['exchange_rate__rate'], errors='coerce')
    df_optimizations['efficiency_improvement'] = pd.to_numeric(df_optimizations['efficiency_improvement'], errors='coerce')
    df_optimizations['cost_reduction'] = pd.to_numeric(df_optimizations['cost_reduction'], errors='coerce')
    df_optimizations['processing_time_reduction'] = pd.to_numeric(df_optimizations['processing_time_reduction'], errors='coerce')

    # Merge the dataframes
    df = pd.merge(df_processes, df_transactions, left_on='id', right_on='logistic_process_id')
    df = pd.merge(df, df_optimizations, left_on='id', right_on='logistic_process_id')

    return df

def calculate_kpis(data):
    """
    Calcula los KPIs clave para el análisis de desempeño de procesos de cambio de divisas.

    Args:
    data (pd.DataFrame): DataFrame con los datos de procesos y transacciones.

    Returns:
    dict: Diccionario con los KPIs calculados.
    """
    kpis = {
        'volumen_promedio_diario': data.groupby('date')['amount'].sum().mean(),
        'tasa_cambio_promedio': data['exchange_rate__rate'].mean(),
        'eficiencia_promedio': data['efficiency_improvement'].mean(),
        'reduccion_costos_promedio': data['cost_reduction'].mean(),
        'reduccion_tiempo_promedio': data['processing_time_reduction'].mean(),
    }
    return kpis

def analyze_correlations(data):
    """
    Analiza las correlaciones entre las variables clave de procesos de cambio de divisas.

    Args:
    data (pd.DataFrame): DataFrame con los datos de procesos y transacciones.

    Returns:
    pd.DataFrame: Matriz de correlación.
    """
    variables = ['amount', 'exchange_rate__rate', 'efficiency_improvement', 'cost_reduction', 'processing_time_reduction']
    return data[variables].corr()

def compare_currencies(data, currency1, currency2):
    """
    Compara el volumen de transacciones entre dos monedas utilizando una prueba t.

    Args:
    data (pd.DataFrame): DataFrame con los datos de procesos y transacciones.
    currency1 (str): Código de la primera moneda.
    currency2 (str): Código de la segunda moneda.

    Returns:
    dict: Resultados de la comparación, incluyendo estadísticas y valor p.
    """
    currency1_data = data[data['from_currency__code'] == currency1]['amount']
    currency2_data = data[data['from_currency__code'] == currency2]['amount']
    
    t_stat, p_value = stats.ttest_ind(currency1_data, currency2_data)
    return {
        'moneda1_volumen_medio': currency1_data.mean(),
        'moneda2_volumen_medio': currency2_data.mean(),
        'diferencia_media': currency1_data.mean() - currency2_data.mean(),
        'estadistica_t': t_stat,
        'valor_p': p_value
    }

def analyze_trends(data):
    """
    Analiza las tendencias en el volumen de transacciones y tasas de cambio a lo largo del tiempo.

    Args:
    data (pd.DataFrame): DataFrame con los datos de procesos y transacciones.

    Returns:
    dict: Resultados del análisis de tendencias.
    """
    data['date'] = pd.to_datetime(data['date'])
    daily_volume = data.groupby(data['date'].dt.to_period('D'))['amount'].sum()
    daily_rate = data.groupby(data['date'].dt.to_period('D'))['exchange_rate__rate'].mean()

    volume_trend = np.polyfit(range(len(daily_volume)), daily_volume, 1)
    rate_trend = np.polyfit(range(len(daily_rate)), daily_rate, 1)

    return {
        'volumen_tendencia': volume_trend[0],
        'tasa_cambio_tendencia': rate_trend[0]
    }

def perform_analysis():
    """
    Realiza un análisis completo de desempeño de procesos de cambio de divisas.

    Returns:
    dict: Resultados completos del análisis de desempeño.
    """
    data = load_data()

    results = {
        'kpis': calculate_kpis(data),
        'correlaciones': analyze_correlations(data),
        'comparacion_monedas': compare_currencies(data, 'USD', 'EUR'),  # Ejemplo con USD y EUR
        'tendencias': analyze_trends(data)
    }

    return results

def print_analysis_results(results):
    """
    Imprime los resultados del análisis de desempeño de forma legible.

    Args:
    results (dict): Resultados del análisis de desempeño.
    """
    print("Análisis de Desempeño de Procesos de Cambio de Divisas")
    print("=====================================================")

    print("\nKPIs:")
    for kpi, value in results['kpis'].items():
        print(f"  {kpi}: {value:.2f}")

    print("\nCorrelaciones principales:")
    corr_matrix = results['correlaciones']
    for var1 in corr_matrix.index:
        for var2 in corr_matrix.columns:
            if var1 != var2 and abs(corr_matrix.loc[var1, var2]) > 0.5:
                print(f"  {var1} vs {var2}: {corr_matrix.loc[var1, var2]:.2f}")

    print("\nComparación de Monedas (USD vs EUR):")
    currency_comp = results['comparacion_monedas']
    print(f"  Diferencia media en volumen: {currency_comp['diferencia_media']:.2f}")
    print(f"  Valor p: {currency_comp['valor_p']:.4f}")

    print("\nTendencias:")
    trends = results['tendencias']
    print(f"  Tendencia de volumen diario: {trends['volumen_tendencia']:.2f} unidades/día")
    print(f"  Tendencia de tasa de cambio: {trends['tasa_cambio_tendencia']:.4f} unidades/día")

if __name__ == "__main__":
    results = perform_analysis()
    print_analysis_results(results)