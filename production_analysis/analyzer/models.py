from django.db import models

class CurrencyExchangeHouse(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    foundation_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.name


class LogisticProcess(models.Model):
    currency_exchange_house = models.ForeignKey(CurrencyExchangeHouse, on_delete=models.CASCADE, related_name='processes')
    process_name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')])

    def __str__(self):
        return f"{self.process_name} - {self.currency_exchange_house.name}"


class Optimization(models.Model):
    logistic_process = models.ForeignKey(LogisticProcess, on_delete=models.CASCADE, related_name='optimizations')
    efficiency_improvement = models.FloatField(help_text="Percentage of improvement in operational efficiency")
    cost_reduction = models.FloatField(help_text="Percentage of reduction in operational costs")
    processing_time_reduction = models.FloatField(help_text="Percentage of reduction in processing time")
    implementation_date = models.DateField()
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Optimization of {self.logistic_process.process_name}"


class Outcome(models.Model):
    optimization = models.ForeignKey(Optimization, on_delete=models.CASCADE, related_name='outcomes')
    outcome_description = models.TextField()
    impact = models.CharField(max_length=50, choices=[('positive', 'Positive'), ('neutral', 'Neutral'), ('negative', 'Negative')])
    outcome_date = models.DateField()
    observations = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Outcome of {self.optimization.logistic_process.process_name}"


class Report(models.Model):
    logistic_process = models.ForeignKey(LogisticProcess, on_delete=models.CASCADE, related_name='reports')
    report_date = models.DateField()
    summary = models.TextField()
    details = models.TextField()
    created_by = models.CharField(max_length=100)

    def __str__(self):
        return f"Report {self.logistic_process.process_name} - {self.report_date}"


class GenerativeAI(models.Model):
    model_name = models.CharField(max_length=100)
    model_description = models.TextField()
    training_date = models.DateField()
    accuracy = models.FloatField(help_text="Percentage of model accuracy in process optimization")
    used_in_processes = models.ManyToManyField(LogisticProcess, related_name='ai_models')

    def __str__(self):
        return self.model_name

