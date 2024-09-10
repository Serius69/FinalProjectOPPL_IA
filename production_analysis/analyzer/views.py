from django.shortcuts import render
from django.http import JsonResponse
import base64

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
    file_path = 'data/raw_production_data.csv'
    data_generator.generate_sales_data(file_path)
    return JsonResponse({'message': 'Datos generados exitosamente'})


def run_etl(request):
    input_file = 'data/raw_production_data.csv'
    output_file = 'data/processed_production_data.csv'
    etl_process.etl_process(input_file, output_file)
    return JsonResponse({'message': 'Proceso ETL completado'})


def analyze_sensitivity(request):
    file_path = 'data/processed_production_data.csv'
    results = performance_analysis.__name__(file_path)
    return JsonResponse(results)


def improve_efficiency(request):
    file_path = 'data/processed_production_data.csv'
    budget = 100000  # Podría ser un parámetro de la solicitud
    results = efficiency_improvement.improve_efficiency(file_path, budget)
    return JsonResponse(results)


def visualize_data(request):
    file_path = 'data/processed_production_data.csv'
    optimization_results = improve_efficiency(request).json()

    # Generar visualizaciones
    data_visualization.generate_visualizations(file_path, optimization_results)

    # Cargar las imágenes generadas y convertirlas a base64
    images = {}
    for img_name in ['production_trends.png', 'efficiency_heatmap.png']:
        with open(f'static/analyzer/images/{img_name}', 'rb') as img_file:
            images[img_name] = base64.b64encode(img_file.read()).decode('utf-8')

    return render(request, 'analyzer/visualizations.html', {'images': images})


def analyze_performance(request):
    file_path = 'data/processed_production_data.csv'
    results = performance_analysis.perform_analysis(file_path)
    return render(request, 'analyzer/results.html', {'results': results})