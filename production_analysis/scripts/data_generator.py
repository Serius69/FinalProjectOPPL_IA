# data_generator.py
import os
import django
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project_name.settings")
django.setup()

from analyzer.models import (
    CurrencyExchangeHouse, Currency, ExchangeRate, ProcessType,
    LogisticProcess, Transaction, Optimization, Outcome, Report, GenerativeAI
)

def create_currency_exchange_house():
    return CurrencyExchangeHouse.objects.create(
        name="Tromay Exchange House",
        location="Main Financial District",
        foundation_date=datetime(2010, 1, 1).date(),
        description="Specialized in currency exchange and international transfers"
    )

def create_currencies():
    currencies = [
        ('USD', 'United States Dollar'),
    ]
    for code, name in currencies:
        Currency.objects.create(code=code, name=name)

def create_exchange_rates(start_date, end_date):
    currencies = Currency.objects.all()
    date_range = pd.date_range(start=start_date, end=end_date)
    
    for date in date_range:
        for from_currency in currencies:
            for to_currency in currencies:
                if from_currency != to_currency:
                    ExchangeRate.objects.create(
                        from_currency=from_currency,
                        to_currency=to_currency,
                        rate=round(random.uniform(0.5, 2), 4),
                        date=date
                    )

def create_process_types():
    process_types = [
        "Currency Exchange",
        "International Transfer",
        "Currency Hedging",
        "Foreign Currency Accounts Management",
        "Risk Assessment"
    ]
    for process_type in process_types:
        ProcessType.objects.create(
            name=process_type,
            description=f"Process for handling {process_type.lower()} operations"
        )

def create_logistic_processes(exchange_house):
    process_types = ProcessType.objects.all()
    for process_type in process_types:
        LogisticProcess.objects.create(
            currency_exchange_house=exchange_house,
            process_type=process_type,
            start_date=datetime.now().date() - timedelta(days=random.randint(30, 365)),
            end_date=None,
            status='in_progress'
        )

def generate_transactions(num_records, start_date, end_date):
    processes = LogisticProcess.objects.all()
    currencies = Currency.objects.all()
    date_range = pd.date_range(start=start_date, end=end_date)

    for _ in range(num_records):
        process = random.choice(processes)
        from_currency = random.choice(currencies)
        to_currency = random.choice([c for c in currencies if c != from_currency])
        date = random.choice(date_range)
        
        exchange_rate = ExchangeRate.objects.get(
            from_currency=from_currency,
            to_currency=to_currency,
            date=date
        )
        
        amount = round(random.uniform(100, 10000), 2)
        
        Transaction.objects.create(
            logistic_process=process,
            date=date,
            from_currency=from_currency,
            to_currency=to_currency,
            amount=amount,
            exchange_rate=exchange_rate
        )

def create_optimizations():
    processes = LogisticProcess.objects.all()
    for process in processes:
        Optimization.objects.create(
            logistic_process=process,
            efficiency_improvement=random.uniform(5, 30),
            cost_reduction=random.uniform(5, 25),
            processing_time_reduction=random.uniform(10, 40),
            implementation_date=datetime.now().date() - timedelta(days=random.randint(30, 180)),
            comments=f"AI-driven optimization for {process.process_type.name}"
        )

def create_outcomes():
    optimizations = Optimization.objects.all()
    for optimization in optimizations:
        Outcome.objects.create(
            optimization=optimization,
            description=f"Results of AI optimization for {optimization.logistic_process.process_type.name}",
            impact=random.choices(['positive', 'neutral', 'negative'], weights=[0.7, 0.2, 0.1])[0],
            date=optimization.implementation_date + timedelta(days=random.randint(30, 90)),
            observations=f"Significant improvements observed in {optimization.logistic_process.process_type.name}"
        )

def create_reports():
    processes = LogisticProcess.objects.all()
    for process in processes:
        Report.objects.create(
            logistic_process=process,
            date=datetime.now().date() - timedelta(days=random.randint(1, 30)),
            summary=f"Performance summary for {process.process_type.name} after AI optimization",
            details=f"Detailed analysis of efficiency gains, cost reductions, and processing time improvements in {process.process_type.name}",
            created_by="AI Analysis Team"
        )

def create_generative_ai_models():
    processes = LogisticProcess.objects.all()
    ai_models = [
        "Exchange Rate Predictor",
        "Risk Assessment AI",
        "Process Optimization AI",
        "Customer Behavior Analyzer",
        "Fraud Detection System"
    ]
    for model_name in ai_models:
        ai_model = GenerativeAI.objects.create(
            name=model_name,
            description=f"AI model for {model_name.lower()} in currency exchange operations",
            training_date=datetime.now().date() - timedelta(days=random.randint(30, 365)),
            accuracy=random.uniform(85, 99)
        )
        ai_model.used_in_processes.set(random.sample(list(processes), k=random.randint(2, len(processes))))

def main(num_records, start_date, end_date):
    print("Starting data generation...")
    
    # Crear una única casa de cambios
    exchange_house = create_currency_exchange_house()
    print("Currency Exchange House created.")
    
    # Crear monedas
    create_currencies()
    print("Currencies created.")
    
    # Crear tasas de cambio
    create_exchange_rates(start_date, end_date)
    print("Exchange rates created.")
    
    # Crear tipos de procesos
    create_process_types()
    print("Process types created.")
    
    # Crear procesos logísticos para la casa de cambios
    create_logistic_processes(exchange_house)
    print("Logistic processes created.")
    
    # Generar transacciones
    generate_transactions(num_records, start_date, end_date)
    print(f"{num_records} transactions generated.")
    
    # Crear optimizaciones
    create_optimizations()
    print("Optimizations created.")
    
    # Crear resultados
    create_outcomes()
    print("Outcomes created.")
    
    # Crear informes
    create_reports()
    print("Reports created.")
    
    # Crear modelos de IA generativa
    create_generative_ai_models()
    print("Generative AI models created.")
    
    print("Data generation completed successfully.")

if __name__ == "__main__":
    num_records = 1000  # Número de transacciones a generar
    start_date = "2023-01-01"  # Fecha de inicio
    end_date = "2023-12-31"  # Fecha de finalización
    
    main(num_records, start_date, end_date)