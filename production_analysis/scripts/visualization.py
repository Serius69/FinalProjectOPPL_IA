import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from analyzer.models import LogisticProcess, Transaction, Optimization

def load_data():
    """
    Load logistic processes and transactions data from the database.

    Returns:
    pd.DataFrame: DataFrame with logistic processes and transactions data.
    """
    logistic_processes = pd.DataFrame(LogisticProcess.objects.all().values(
        'id', 'currency_exchange_house__name', 'process_type__name', 'start_date', 'end_date', 'status'
    ))
    transactions = pd.DataFrame(Transaction.objects.all().values(
        'logistic_process_id', 'date', 'from_currency__code', 'to_currency__code', 'amount', 'exchange_rate__rate'
    ))
    optimizations = pd.DataFrame(Optimization.objects.all().values(
        'logistic_process_id', 'efficiency_improvement', 'cost_reduction', 'processing_time_reduction'
    ))
    
    # Merge the dataframes
    df = (logistic_processes
          .merge(transactions, left_on='id', right_on='logistic_process_id')
          .merge(optimizations, left_on='id', right_on='logistic_process_id'))
    
    return df

def create_plot(data, plot_type, x, y, title, xlabel, ylabel, filename, output_dir, **kwargs):
    """
    Generic function to create and save plots.

    Args:
    data (pd.DataFrame): Data to plot
    plot_type (str): Type of plot ('line', 'bar', 'heatmap', 'scatter')
    x (str): Column name for x-axis
    y (str): Column name for y-axis
    title (str): Plot title
    xlabel (str): X-axis label
    ylabel (str): Y-axis label
    filename (str): Output filename
    output_dir (str): Directory to save the plot
    **kwargs: Additional arguments for specific plot types
    """
    plt.figure(figsize=(12, 6))
    
    if plot_type == 'line':
        sns.lineplot(x=x, y=y, data=data)
    elif plot_type == 'bar':
        sns.barplot(x=x, y=y, data=data)
    elif plot_type == 'heatmap':
        pivot_data = data.pivot_table(values=y, index=kwargs.get('index'), columns=kwargs.get('columns'), aggfunc='mean')
        sns.heatmap(pivot_data, annot=True, cmap='YlGnBu', fmt='.2f')
    elif plot_type == 'scatter':
        sns.scatterplot(x=x, y=y, data=data)
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

def generate_visualizations():
    """
    Generate all visualizations for the currency exchange process analysis.
    """
    data = load_data()

    # Ensure the output directory exists
    output_dir = 'static/analyzer/images'
    os.makedirs(output_dir, exist_ok=True)

    # Exchange Volume Trends
    daily_volume = data.groupby('date')['amount'].sum().reset_index()
    create_plot(daily_volume, 'line', 'date', 'amount', 
                'Exchange Volume Trends Over Time', 'Date', 'Exchange Volume', 
                'exchange_volume_trends.png', output_dir)

    # Efficiency Heatmap
    create_plot(data, 'heatmap', None, 'efficiency_improvement', 
                'Heatmap of Exchange Process Efficiency', 'Exchange House', 'Process Type', 
                'efficiency_heatmap.png', output_dir, 
                index='process_type__name', columns='currency_exchange_house__name')

    # Cost Breakdown
    cost_breakdown = data.groupby('currency_exchange_house__name')['amount'].sum().reset_index()
    create_plot(cost_breakdown, 'bar', 'currency_exchange_house__name', 'amount', 
                'Cost Breakdown', 'Exchange House', 'Total Cost', 
                'cost_breakdown.png', output_dir)

    # Resource Allocation
    create_plot(data, 'scatter', 'efficiency_improvement', 'cost_reduction', 
                'Optimal Resource Allocation', 'Efficiency Improvement', 'Cost Reduction', 
                'resource_allocation.png', output_dir)

    print("Visualizations generated and saved.")

if __name__ == "__main__":
    generate_visualizations()