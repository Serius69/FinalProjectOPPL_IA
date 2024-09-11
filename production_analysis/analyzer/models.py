# models.py
from django.db import models

class CurrencyExchangeHouse(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    foundation_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.name

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.code} - {self.name}"

class ExchangeRate(models.Model):
    from_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='from_rates')
    to_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='to_rates')
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    date = models.DateField()

    class Meta:
        unique_together = ('from_currency', 'to_currency', 'date')

    def __str__(self):
        return f"{self.from_currency.code}/{self.to_currency.code} - {self.rate} ({self.date})"

class ProcessType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class LogisticProcess(models.Model):
    currency_exchange_house = models.ForeignKey(CurrencyExchangeHouse, on_delete=models.CASCADE, related_name='processes')
    process_type = models.ForeignKey(ProcessType, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')])

    def __str__(self):
        return f"{self.process_type.name} - {self.currency_exchange_house.name}"

class Transaction(models.Model):
    logistic_process = models.ForeignKey(LogisticProcess, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateField()
    from_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='from_transactions')
    to_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='to_transactions')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    exchange_rate = models.ForeignKey(ExchangeRate, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.from_currency.code} to {self.to_currency.code} - {self.amount} ({self.date})"

class Optimization(models.Model):
    logistic_process = models.ForeignKey(LogisticProcess, on_delete=models.CASCADE, related_name='optimizations')
    efficiency_improvement = models.FloatField(help_text="Percentage of improvement in operational efficiency")
    cost_reduction = models.FloatField(help_text="Percentage of reduction in operational costs")
    processing_time_reduction = models.FloatField(help_text="Percentage of reduction in processing time")
    implementation_date = models.DateField()
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Optimization of {self.logistic_process.process_type.name}"

class Outcome(models.Model):
    optimization = models.ForeignKey(Optimization, on_delete=models.CASCADE, related_name='outcomes')
    description = models.TextField()
    impact = models.CharField(max_length=50, choices=[('positive', 'Positive'), ('neutral', 'Neutral'), ('negative', 'Negative')])
    date = models.DateField()
    observations = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Outcome of {self.optimization.logistic_process.process_type.name}"

class Report(models.Model):
    logistic_process = models.ForeignKey(LogisticProcess, on_delete=models.CASCADE, related_name='reports')
    date = models.DateField()
    summary = models.TextField()
    details = models.TextField()
    created_by = models.CharField(max_length=100)

    def __str__(self):
        return f"Report {self.logistic_process.process_type.name} - {self.date}"

class GenerativeAI(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    training_date = models.DateField()
    accuracy = models.FloatField(help_text="Percentage of model accuracy in process optimization")
    used_in_processes = models.ManyToManyField(LogisticProcess, related_name='ai_models')

    def __str__(self):
        return self.name