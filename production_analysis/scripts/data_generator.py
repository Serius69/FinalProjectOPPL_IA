import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_sales_data(num_records=1000, start_date="2023-01-01", end_date="2023-12-31"):
    """
    Genera un conjunto de datos de ventas ficticios.

    Args:
        num_records (int): Número de registros de ventas a generar.
        start_date (str): Fecha de inicio en formato 'YYYY-MM-DD'.
        end_date (str): Fecha de finalización en formato 'YYYY-MM-DD'.

    Returns:
        pd.DataFrame: DataFrame con los datos de ventas generados.
    """

    # Convertir las fechas de inicio y fin
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # Generar fechas aleatorias
    dates = [start_date + timedelta(days=np.random.randint((end_date - start_date).days)) for _ in range(num_records)]

    # Generar IDs y nombres de productos
    product_ids = np.random.randint(1, 101, num_records)
    product_names = [f"Product_{id}" for id in product_ids]

    # Generar cantidades y precios
    quantities = np.random.randint(1, 11, num_records)
    prices = np.random.uniform(10, 1000, num_records).round(2)

    # Calcular las ventas totales
    total_sales = quantities * prices

    # Generar IDs de clientes
    customer_ids = np.random.randint(1, 1001, num_records)

    # Crear DataFrame con los datos de ventas
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
    # Parámetros ajustables para la generación de datos
    num_records = 1000  # Número de registros a generar
    start_date = "2023-01-01"  # Fecha de inicio
    end_date = "2023-12-31"  # Fecha de finalización

    # Generar y guardar los datos de ventas
    sales_data = generate_sales_data(num_records=num_records, start_date=start_date, end_date=end_date)
    sales_data.to_csv('raw_sales_data.csv', index=False)
    print(f"{num_records} registros de datos de ventas generados y guardados en 'raw_sales_data.csv'.")
