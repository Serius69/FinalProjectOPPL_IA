from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
import base64
from datetime import datetime, timedelta
from .models import LogisticProcess, Transaction
import json

from scripts import(
    data_generator,
    data_visualization,
    efficiency_improvement,
    etl_process,
    performance_analysis,
    visualization,
)

def index(request):
    return render(request, 'analyzer/index.html')

def generate_data(request):
    start_date = datetime.now().strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=100)).strftime('%Y-%m-%d')
    data_generator.main(1000, start_date, end_date)
    messages.success(request, 'Generación de datos completada')
    return redirect('index')

def run_etl(request):
    etl_process.etl_process()
    messages.success(request, 'Proceso ETL completado')
    return redirect('index')

def analyze_performance(request):
    results = performance_analysis.perform_analysis()
    return render(request, 'analyzer/results.html', {'results': results})

def improve_efficiency(request):
    # Obtener los parámetros de la solicitud
    logistic_process_id = request.GET.get('process_id', 1)
    budget = float(request.GET.get('budget', 100000))
    efficiency_improvement_value = float(request.GET.get('efficiency_improvement', 10))  # Mejora en eficiencia

    try:
        # Llamar a la función de mejora de eficiencia con los parámetros
        results = efficiency_improvement.improve_efficiency(logistic_process_id, budget, efficiency_improvement_value)

        # Mostrar mensaje de éxito con los resultados obtenidos
        messages.success(request, f"Mejora de eficiencia completada. Asignación óptima: {results['optimal_resource_allocation']}, Volumen máximo: {results['max_exchange_volume']}")

    except ValueError as e:
        # Capturar errores específicos y mostrar un mensaje de error
        messages.error(request, f"Error: {str(e)}")

    except Exception as e:
        # Capturar cualquier otro error inesperado
        messages.error(request, f"Ha ocurrido un error inesperado: {str(e)}")

    # Redirigir a la página de inicio
    return redirect('index')
def visualize_data(request):
    # Generar visualizaciones
    visualization.generate_visualizations()

    # Cargar las imágenes generadas y convertirlas a base64
    images = {}
    image_files = [
        'exchange_volume_trends.png',
        'efficiency_heatmap.png',
        'cost_breakdown.png',
        'resource_allocation.png'
    ]

    for img_name in image_files:
        try:
            with open(f'static/analyzer/images/{img_name}', 'rb') as img_file:
                images[img_name] = base64.b64encode(img_file.read()).decode('utf-8')
        except FileNotFoundError:
            images[img_name] = None  # Manejo de caso si el archivo no se encuentra
        except Exception as e:
            return JsonResponse({'error': f'Error al leer la imagen {img_name}: {str(e)}'}, status=500)

    return render(request, 'analyzer/visualizations.html', {'images': images})


def get_exchange_houses(request):
    exchange_houses = LogisticProcess.objects.values_list('currency_exchange_house__name', flat=True).distinct()
    return JsonResponse(list(exchange_houses), safe=False)

def get_currencies(request):
    currencies = Transaction.objects.values_list('from_currency__code', flat=True).distinct()
    return JsonResponse(list(currencies), safe=False)
