import pandas as pd


def extract_data(file_path):
    return pd.read_csv(file_path)


def transform_data(df):
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Add month and year columns
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year

    # Round prices and total sales to 2 decimal places
    df['price'] = df['price'].round(2)
    df['total_sale'] = df['total_sale'].round(2)

    # Create a categorical column for price ranges
    df['price_category'] = pd.cut(df['price'], bins=[0, 100, 500, 1000], labels=['Low', 'Medium', 'High'])

    # Remove any duplicate rows
    df = df.drop_duplicates()

    return df


def load_data(df, output_file):
    df.to_csv(output_file, index=False)
    print(f"Transformed data saved to '{output_file}'")


def etl_process(input_file, output_file):
    raw_data = extract_data(input_file)
    transformed_data = transform_data(raw_data)
    load_data(transformed_data, output_file)


if __name__ == "__main__":
    etl_process('raw_sales_data.csv', 'transformed_sales_data.csv')