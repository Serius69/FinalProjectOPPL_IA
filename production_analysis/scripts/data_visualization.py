# data_visualization.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_data(file_path):
    return pd.read_csv(file_path, parse_dates=['date'])


def monthly_sales_trend(df):
    monthly_sales = df.groupby(df['date'].dt.to_period('M'))['total_sale'].sum().reset_index()
    monthly_sales['date'] = monthly_sales['date'].dt.to_timestamp()

    plt.figure(figsize=(12, 6))
    plt.plot(monthly_sales['date'], monthly_sales['total_sale'])
    plt.title('Monthly Sales Trend')
    plt.xlabel('Month')
    plt.ylabel('Total Sales')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('monthly_sales_trend.png')
    plt.close()


def top_products_bar_chart(df):
    top_products = df.groupby('product_name')['total_sale'].sum().sort_values(ascending=False).head(10)

    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_products.index, y=top_products.values)
    plt.title('Top 10 Products by Total Sales')
    plt.xlabel('Product Name')
    plt.ylabel('Total Sales')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('top_products_bar_chart.png')
    plt.close()


def price_category_distribution(df):
    plt.figure(figsize=(8, 6))
    df['price_category'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Distribution of Price Categories')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('price_category_distribution.png')
    plt.close()


def generate_visualizations(input_file):
    df = load_data(input_file)
    monthly_sales_trend(df)
    top_products_bar_chart(df)
    price_category_distribution(df)
    print("Visualizations generated and saved as PNG files.")


if __name__ == "__main__":
    generate_visualizations('transformed_sales_data.csv')