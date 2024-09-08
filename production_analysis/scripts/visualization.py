# visualization.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go


def load_data(file_path):
    """
    Carga los datos de producción desde un archivo CSV.

    Args:
    file_path (str): Ruta al archivo CSV con los datos de producción.

    Returns:
    pd.DataFrame: DataFrame con los datos de producción.
    """
    return pd.read_csv(file_path)


def plot_production_trends(data):
    """
    Crea un gráfico de líneas para mostrar las tendencias de producción a lo largo del tiempo.

    Args:
    data (pd.DataFrame): DataFrame con los datos de producción.
    """
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='date', y='production', data=data)
    plt.title('Tendencias de Producción a lo Largo del Tiempo')
    plt.xlabel('Fecha')
    plt.ylabel('Producción')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('production_trends.png')
    plt.close()


def plot_cost_breakdown(data):
    """
    Crea un gráfico de torta interactivo para mostrar el desglose de costos.

    Args:
    data (pd.DataFrame): DataFrame con los datos de producción.

    Returns:
    plotly.graph_objs._figure.Figure: Figura de Plotly con el gráfico de torta.
    """
    cost_breakdown = data[['labor_cost', 'material_cost', 'overhead_cost']].sum()
    fig = px.pie(values=cost_breakdown.values, names=cost_breakdown.index, title='Desglose de Costos')
    return fig


def plot_efficiency_heatmap(data):
    """
    Crea un mapa de calor para visualizar la eficiencia de producción.

    Args:
    data (pd.DataFrame): DataFrame con los datos de producción.
    """
    pivot_data = data.pivot('labor_hours', 'material_amount', 'efficiency')
    plt.figure(figsize=(10, 8))
    sns.heatmap(pivot_data, annot=True, cmap='YlGnBu', fmt='.2f')
    plt.title('Mapa de Calor de Eficiencia de Producción')
    plt.xlabel('Cantidad de Material')
    plt.ylabel('Horas de Trabajo')
    plt.tight_layout()
    plt.savefig('efficiency_heatmap.png')
    plt.close()


def plot_resource_allocation(optimization_results):
    """
    Crea un gráfico de barras para mostrar la asignación óptima de recursos.

    Args:
    optimization_results (dict): Resultados de la optimización de eficiencia.

    Returns:
    plotly.graph_objs._figure.Figure: Figura de Plotly con el gráfico de barras.
    """
    resources = ['Labor', 'Material', 'Overhead']
    values = [optimization_results['optimal_labor'],
              optimization_results['optimal_material'],
              optimization_results['optimal_overhead']]

    fig = go.Figure(data=[go.Bar(x=resources, y=values)])
    fig.update_layout(title='Asignación Óptima de Recursos',
                      xaxis_title='Recurso',
                      yaxis_title='Cantidad Asignada')
    return fig


def generate_visualizations(input_file, optimization_results):
    """
    Genera todas las visualizaciones para el análisis de producción.

    Args:
    input_file (str): Ruta al archivo CSV con los datos de producción.
    optimization_results (dict): Resultados de la optimización de eficiencia.
    """
    data = load_data(input_file)

    plot_production_trends(data)
    cost_breakdown_fig = plot_cost_breakdown(data)
    cost_breakdown_fig.write_html("cost_breakdown.html")

    plot_efficiency_heatmap(data)

    resource_allocation_fig = plot_resource_allocation(optimization_results)
    resource_allocation_fig.write_html("resource_allocation.html")

    print("Visualizaciones generadas y guardadas.")


if __name__ == "__main__":
    input_file = 'production_data.csv'
    # Ejemplo de resultados de optimización (normalmente vendrían del script de mejoramiento de eficiencia)
    optimization_results = {
        'optimal_labor': 500,
        'optimal_material': 1000,
        'optimal_overhead': 200,
        'max_production': 5000,
        'total_cost': 90000
    }
    generate_visualizations(input_file, optimization_results)