# data_visualization.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from analyzer.models import LogisticProcess, Optimization, Outcome, Transaction, ExchangeRate

def load_optimization_data():
    optimization_data = Optimization.objects.select_related('logistic_process__process_type').prefetch_related('outcomes').all()
    df = pd.DataFrame(list(optimization_data.values('implementation_date', 'efficiency_improvement', 'cost_reduction', 'logistic_process__process_type__name')))
    df['implementation_date'] = pd.to_datetime(df['implementation_date'])
    return df

def load_transaction_data():
    transaction_data = Transaction.objects.select_related('logistic_process__process_type', 'from_currency', 'to_currency', 'exchange_rate').all()
    df = pd.DataFrame(list(transaction_data.values('date', 'amount', 'from_currency__code')))
    df['date'] = pd.to_datetime(df['date'])
    return df

def monthly_optimization_trend(df, *, synthetic=False):
    monthly_optimizations = df.groupby(df['implementation_date'].dt.to_period('M'))['efficiency_improvement'].mean().reset_index()
    monthly_optimizations['implementation_date'] = monthly_optimizations['implementation_date'].dt.to_timestamp()

    plt.figure(figsize=(12, 6))
    plt.plot(monthly_optimizations['implementation_date'], monthly_optimizations['efficiency_improvement'], marker='o')
    plt.title('Monthly Average Fixture Efficiency Improvement' if synthetic else 'Monthly Average Efficiency Improvement')
    if len(monthly_optimizations) == 1:
        plt.title('One monthly observation — no trend estimate')
        plt.xticks(monthly_optimizations['implementation_date'], rotation=45)
    plt.xlabel('Month')
    plt.ylabel('Average Efficiency Improvement (%)')
    plt.xticks(rotation=45)
    if synthetic:
        plt.suptitle('SYNTHETIC FIXTURES — not measured results or market data', fontsize=10)
    plt.tight_layout(rect=(0, 0, 1, 0.94) if synthetic else (0, 0, 1, 1))
    plt.savefig('monthly_optimization_trend.png')
    plt.close()

def top_processes_by_cost_reduction(df, *, synthetic=False):
    top_processes = df.groupby('logistic_process__process_type__name')['cost_reduction'].mean().sort_values(ascending=False).head(10)

    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_processes.values, y=top_processes.index)
    plt.title(f'Top {len(top_processes)} Process Types by Average Cost Reduction')
    plt.ylabel('Process Type')
    plt.xlabel('Average Cost Reduction (%)')
    if synthetic:
        plt.suptitle('SYNTHETIC FIXTURES — not measured results or market data', fontsize=10)
    plt.tight_layout(rect=(0, 0, 1, 0.94) if synthetic else (0, 0, 1, 1))
    plt.savefig('top_processes_by_cost_reduction.png')
    plt.close()

def outcome_distribution(*, synthetic=False):
    outcome_data = Outcome.objects.all()
    outcome_df = pd.DataFrame(list(outcome_data.values('impact')))
    outcome_counts = outcome_df['impact'].value_counts()

    plt.figure(figsize=(8, 6))
    outcome_counts.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Distribution of Outcome Impact')
    plt.ylabel('')
    if synthetic:
        plt.suptitle('SYNTHETIC FIXTURES — not measured results or market data', fontsize=10)
    plt.tight_layout(rect=(0, 0, 1, 0.94) if synthetic else (0, 0, 1, 1))
    plt.savefig('outcome_distribution.png')
    plt.close()

def transaction_volume_by_currency(df, *, synthetic=False):
    volume_by_currency = df.groupby('from_currency__code')['amount'].sum().sort_values(ascending=False)

    plt.figure(figsize=(12, 6))
    sns.barplot(x=volume_by_currency.index, y=volume_by_currency.values)
    plt.title('Transaction Amounts by Source Currency (not converted)')
    plt.xlabel('Currency')
    plt.ylabel('Amount in each source currency’s own units')
    plt.xticks(rotation=45)
    if synthetic:
        plt.suptitle('SYNTHETIC FIXTURES — not measured results or market data', fontsize=10)
    plt.tight_layout(rect=(0, 0, 1, 0.94) if synthetic else (0, 0, 1, 1))
    plt.savefig('transaction_volume_by_currency.png')
    plt.close()

def exchange_rate_trend(*, synthetic=False):
    exchange_rate_data = ExchangeRate.objects.filter(from_currency__code='USD', to_currency__code='EUR').order_by('date')
    exchange_rate_df = pd.DataFrame(list(exchange_rate_data.values('date', 'rate')))

    plt.figure(figsize=(12, 6))
    plt.plot(exchange_rate_df['date'], exchange_rate_df['rate'], marker='o')
    plt.title('USD to EUR Exchange Rates' if len(exchange_rate_df) > 1 else 'USD to EUR: one observation — no trend estimate')
    plt.xlabel('Date')
    if len(exchange_rate_df) == 1:
        plt.xticks(exchange_rate_df['date'], rotation=45)
    plt.ylabel('EUR per 1 USD')
    plt.xticks(rotation=45)
    if synthetic:
        plt.suptitle('SYNTHETIC FIXTURES — not measured results or market data', fontsize=10)
    plt.tight_layout(rect=(0, 0, 1, 0.94) if synthetic else (0, 0, 1, 1))
    plt.savefig('usd_eur_exchange_rate_trend.png')
    plt.close()

def generate_visualizations(*, synthetic=False):
    optimization_df = load_optimization_data()
    transaction_df = load_transaction_data()

    monthly_optimization_trend(optimization_df, synthetic=synthetic)
    top_processes_by_cost_reduction(optimization_df, synthetic=synthetic)
    outcome_distribution(synthetic=synthetic)
    transaction_volume_by_currency(transaction_df, synthetic=synthetic)
    exchange_rate_trend(synthetic=synthetic)

    print("Visualizations generated and saved as PNG files.")

if __name__ == "__main__":
    generate_visualizations()
