import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from myapp.models import LogisticProcess, Optimization, Outcome  # Import models from Django app
from django_pandas.io import read_frame  # To convert QuerySet to Pandas DataFrame

# Load data from the database using Django ORM
def load_data_from_db():
    # Query the Optimization table and prefetch related LogisticProcess and Outcome data
    optimization_data = Optimization.objects.select_related('logistic_process').prefetch_related('outcomes').all()
    
    # Convert QuerySet to a DataFrame using django_pandas read_frame
    df = read_frame(optimization_data)
    
    # Parse 'date' fields as datetime and handle missing data if necessary
    df['implementation_date'] = pd.to_datetime(df['implementation_date'])
    
    return df

# Monthly sales trend visualization (equivalent to tracking optimization over time)
def monthly_optimization_trend(df):
    # Group by month and sum efficiency improvement to simulate a "trend"
    monthly_optimizations = df.groupby(df['implementation_date'].dt.to_period('M'))['efficiency_improvement'].sum().reset_index()
    monthly_optimizations['implementation_date'] = monthly_optimizations['implementation_date'].dt.to_timestamp()

    plt.figure(figsize=(12, 6))
    plt.plot(monthly_optimizations['implementation_date'], monthly_optimizations['efficiency_improvement'])
    plt.title('Monthly Optimization Efficiency Improvement Trend')
    plt.xlabel('Month')
    plt.ylabel('Total Efficiency Improvement (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('monthly_optimization_trend.png')
    plt.close()

# Top logistic processes by cost reduction
def top_processes_by_cost_reduction(df):
    # Group by logistic process and sum total cost reduction
    top_processes = df.groupby('logistic_process')['cost_reduction'].sum().sort_values(ascending=False).head(10)

    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_processes.index, y=top_processes.values)
    plt.title('Top 10 Processes by Cost Reduction')
    plt.xlabel('Logistic Process')
    plt.ylabel('Total Cost Reduction (%)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('top_processes_by_cost_reduction.png')
    plt.close()

# Distribution of outcomes (positive, neutral, negative)
def outcome_distribution(df):
    outcome_counts = df['outcome'].value_counts()

    plt.figure(figsize=(8, 6))
    outcome_counts.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Distribution of Outcome Impact (Positive, Neutral, Negative)')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('outcome_distribution.png')
    plt.close()

def generate_visualizations():
    # Load data from the database
    df = load_data_from_db()
    
    # Generate the visualizations
    monthly_optimization_trend(df)
    top_processes_by_cost_reduction(df)
    outcome_distribution(df)
    
    print("Visualizations generated and saved as PNG files.")

if __name__ == "__main__":
    generate_visualizations()
