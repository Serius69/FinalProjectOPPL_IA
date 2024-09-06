import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_sales_data(num_records=1000):
    # Generate random dates
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    dates = [start_date + timedelta(days=np.random.randint((end_date - start_date).days)) for _ in range(num_records)]

    # Generate product IDs and names
    product_ids = np.random.randint(1, 101, num_records)
    product_names = [f"Product_{id}" for id in product_ids]

    # Generate quantities and prices
    quantities = np.random.randint(1, 11, num_records)
    prices = np.random.uniform(10, 1000, num_records).round(2)

    # Calculate total sales
    total_sales = quantities * prices

    # Generate customer IDs
    customer_ids = np.random.randint(1, 1001, num_records)

    # Create DataFrame
    df = pd.DataFrame({
        'date': dates,
        'product_id': product_ids,
        'product_name': product_names,
        'quantity': quantities,
        'price': prices,
        'total_sale': total_sales,
        'customer_id': customer_ids
    })

    return df


if __name__ == "__main__":
    sales_data = generate_sales_data()
    sales_data.to_csv('raw_sales_data.csv', index=False)
    print("Raw sales data generated and saved to 'raw_sales_data.csv'")