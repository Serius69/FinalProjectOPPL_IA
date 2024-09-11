#etl_process.py
import pandas as pd
from analyzer.models import LogisticProcess, CurrencyExchangeHouse, ProcessType, Transaction, ExchangeRate
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum

def extract_data():
    try:
        data = LogisticProcess.objects.select_related('currency_exchange_house', 'process_type').prefetch_related('transactions').all().values(
            'id', 'currency_exchange_house__name', 'process_type__name', 'start_date', 'end_date', 'status'
        )
        transactions = Transaction.objects.select_related('from_currency', 'to_currency', 'exchange_rate').values(
            'logistic_process_id', 'date', 'from_currency__code', 'to_currency__code', 'amount', 'exchange_rate__rate'
        )
        df_processes = pd.DataFrame(list(data))
        df_transactions = pd.DataFrame(list(transactions))
        return df_processes, df_transactions
    except ObjectDoesNotExist:
        print("No data found in the database.")
        return pd.DataFrame(), pd.DataFrame()

def transform_data(df_processes, df_transactions):
    df_processes['start_date'] = pd.to_datetime(df_processes['start_date'])
    df_processes['end_date'] = pd.to_datetime(df_processes['end_date'], errors='coerce')

    df_processes['duration'] = (df_processes['end_date'] - df_processes['start_date']).dt.days.fillna(-1)

    df_transactions['date'] = pd.to_datetime(df_transactions['date'])
    
    # Agregar métricas de transacciones a los procesos
    transaction_metrics = df_transactions.groupby('logistic_process_id').agg({
        'amount': ['sum', 'count'],
        'exchange_rate__rate': 'mean'
    })
    transaction_metrics.columns = ['total_amount', 'transaction_count', 'avg_exchange_rate']
    
    df_processes = df_processes.merge(transaction_metrics, left_on='id', right_index=True, how='left')

    df_processes = df_processes.drop_duplicates()

    return df_processes, df_transactions

def load_data(df_processes, df_transactions):
    for _, row in df_processes.iterrows():
        process_id = row.get('id')
        if process_id:
            process = LogisticProcess.objects.filter(id=process_id).first()
            if process:
                process.start_date = row['start_date']
                process.end_date = row['end_date']
                process.status = row['status']
                process.save()
            else:
                print(f"Process with ID {process_id} not found in the database.")
        else:
            print("Invalid data: Missing ID for process.")

    # Actualizar o crear nuevas transacciones
    for _, row in df_transactions.iterrows():
        transaction, created = Transaction.objects.update_or_create(
            logistic_process_id=row['logistic_process_id'],
            date=row['date'],
            defaults={
                'from_currency': ExchangeRate.objects.get(code=row['from_currency__code']),
                'to_currency': ExchangeRate.objects.get(code=row['to_currency__code']),
                'amount': row['amount'],
                'exchange_rate': ExchangeRate.objects.get(rate=row['exchange_rate__rate'])
            }
        )
        if created:
            print(f"New transaction created for process ID {row['logistic_process_id']}")
        else:
            print(f"Transaction updated for process ID {row['logistic_process_id']}")

def etl_process():
    raw_processes, raw_transactions = extract_data()
    if raw_processes.empty or raw_transactions.empty:
        print("No data to process.")
        return
    transformed_processes, transformed_transactions = transform_data(raw_processes, raw_transactions)
    load_data(transformed_processes, transformed_transactions)
    print("ETL process completed successfully.")

if __name__ == "__main__":
    etl_process()