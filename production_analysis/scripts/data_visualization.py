# data_visualization.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from django_pandas.io import read_frame
from analyzer.models import LogisticProcess, Optimization, Outcome, Transaction, ExchangeRate

def load_optimization_data():
    optimization_data = Optimization.objects.select_related('logistic_process__process_type').prefetch_related('outcomes').all()
    df = read_frame(optimization_data)
    df['implementation_date'] = pd.to_datetime(df['implementation_date'])
    return df

def load_transaction_data():
    transaction_data = Transaction.objects.select_related('logistic_process__process_type', 'from_currency', 'to_currency', 'exchange_rate').all()
    df = read_frame(transaction_data)
    df['date'] = pd.to_datetime(df['date'])
    return df

def monthly_optimization_trend(df):
    monthly_optimizations = df.groupby(df['implementation_date'].dt.to_period('M'))['efficiency_improvement'].mean().reset_index()
    monthly_optimizations['implementation_date'] = monthly_optimizations['implementation_date'].dt.to_timestamp()

    plt.figure(figsize=(12, 6))
    plt.plot(monthly_optimizations['implementation_date'], monthly_optimizations['efficiency_improvement'])
    plt.title('Monthly Average Optimization Efficiency Improvement Trend')
    plt.xlabel('Month')
    plt.ylabel('Average Efficiency Improvement (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('monthly_optimization_trend.png')
    plt.close()

def top_processes_by_cost_reduction(df):
    top_processes = df.groupby('logistic_process__process_type__name')['cost_reduction'].mean().sort_values(ascending=False).head(10)

    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_processes.index, y=top_processes.values)
    plt.title('Top 10 Process Types by Average Cost Reduction')
    plt.xlabel('Process Type')
    plt.ylabel('Average Cost Reduction (%)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('top_processes_by_cost_reduction.png')
    plt.close()

def outcome_distribution():
    outcome_data = Outcome.objects.all()
    outcome_df = read_frame(outcome_data)
    outcome_counts = outcome_df['impact'].value_counts()

    plt.figure(figsize=(8, 6))
    outcome_counts.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Distribution of Outcome Impact')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('outcome_distribution.png')
    plt.close()

def transaction_volume_by_currency(df):
    volume_by_currency = df.groupby('from_currency__code')['amount'].sum().sort_values(ascending=False)

    plt.figure(figsize=(12, 6))
    sns.barplot(x=volume_by_currency.index, y=volume_by_currency.values)
    plt.title('Transaction Volume by Currency')
    plt.xlabel('Currency')
    plt.ylabel('Total Transaction Amount')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('transaction_volume_by_currency.png')
    plt.close()

def exchange_rate_trend():
    exchange_rate_data = ExchangeRate.objects.filter(from_currency__code='USD', to_currency__code='EUR').order_by('date')
    exchange_rate_df = read_frame(exchange_rate_data)
    
    plt.figure(figsize=(12, 6))
    plt.plot(exchange_rate_df['date'], exchange_rate_df['rate'])
    plt.title('USD/EUR Exchange Rate Trend')
    plt.xlabel('Date')
    plt.ylabel('Exchange Rate')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('usd_eur_exchange_rate_trend.png')
    plt.close()

def generate_visualizations():
    optimization_df = load_optimization_data()
    transaction_df = load_transaction_data()
    
    monthly_optimization_trend(optimization_df)
    top_processes_by_cost_reduction(optimization_df)
    outcome_distribution()
    transaction_volume_by_currency(transaction_df)
    exchange_rate_trend()
    
    print("Visualizations generated and saved as PNG files.")

if __name__ == "__main__":
    generate_visualizations()