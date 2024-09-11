# visualization.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from analyzer.models import LogisticProcess, Transaction, ExchangeRate, Optimization

def load_data():
    """
    Carga los datos de procesos logísticos y transacciones desde la base de datos.

    Returns:
    pd.DataFrame: DataFrame con los datos de procesos logísticos y transacciones.
    """
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
    
    # Merge the dataframes
    df = pd.merge(df_processes, df_transactions, left_on='id', right_on='logistic_process_id')
    df = pd.merge(df, df_optimizations, left_on='id', right_on='logistic_process_id')
    
    return df

def plot_exchange_volume_trends(data):
    """
    Crea un gráfico de líneas para mostrar las tendencias de volumen de cambio a lo largo del tiempo.

    Args:
    data (pd.DataFrame): DataFrame con los datos de procesos y transacciones.
    """
    daily_volume = data.groupby('date')['amount'].sum().reset_index()
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='date', y='amount', data=daily_volume)
    plt.title('Tendencias de Volumen de Cambio a lo Largo del Tiempo')
    plt.xlabel('Fecha')
    plt.ylabel('Volumen de Cambio')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('exchange_volume_trends.png')
    plt.close()

def plot_currency_distribution(data):
    """
    Crea un gráfico de torta interactivo para mostrar la distribución de monedas cambiadas.

    Args:
    data (pd.DataFrame): DataFrame con los datos de procesos y transacciones.

    Returns:
    plotly.graph_objs._figure.Figure: Figura de Plotly con el gráfico de torta.
    """
    currency_distribution = data.groupby('from_currency__code')['amount'].sum()
    fig = px.pie(values=currency_distribution.values, names=currency_distribution.index, title='Distribución de Monedas Cambiadas')
    return fig

def plot_efficiency_heatmap(data):
    """
    Crea un mapa de calor para visualizar la eficiencia de los procesos de cambio.

    Args:
    data (pd.DataFrame): DataFrame con los datos de procesos y transacciones.
    """
    pivot_data = data.pivot_table(values='efficiency_improvement', index='process_type__name', columns='currency_exchange_house__name', aggfunc='mean')
    plt.figure(figsize=(10, 8))
    sns.heatmap(pivot_data, annot=True, cmap='YlGnBu', fmt='.2f')
    plt.title('Mapa de Calor de Eficiencia de Procesos de Cambio')
    plt.xlabel('Casa de Cambio')
    plt.ylabel('Tipo de Proceso')
    plt.tight_layout()
    plt.savefig('efficiency_heatmap.png')
    plt.close()

def plot_optimization_results(data):
    """
    Crea un gráfico de barras para mostrar los resultados de optimización.

    Args:
    data (pd.DataFrame): DataFrame con los datos de procesos y optimizaciones.

    Returns:
    plotly.graph_objs._figure.Figure: Figura de Plotly con el gráfico de barras.
    """
    avg_improvements = data[['efficiency_improvement', 'cost_reduction', 'processing_time_reduction']].mean()
    
    fig = go.Figure(data=[go.Bar(x=avg_improvements.index, y=avg_improvements.values)])
    fig.update_layout(title='Resultados Promedio de Optimización',
                      xaxis_title='Métrica',
                      yaxis_title='Porcentaje de Mejora')
    return fig

def generate_visualizations():
    """
    Genera todas las visualizaciones para el análisis de procesos de cambio de divisas.
    """
    data = load_data()

    plot_exchange_volume_trends(data)
    currency_distribution_fig = plot_currency_distribution(data)
    currency_distribution_fig.write_html("currency_distribution.html")

    plot_efficiency_heatmap(data)

    optimization_results_fig = plot_optimization_results(data)
    optimization_results_fig.write_html("optimization_results.html")

    print("Visualizaciones generadas y guardadas.")

if __name__ == "__main__":
    generate_visualizations()