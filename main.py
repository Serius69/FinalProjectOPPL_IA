from production_analysis.scripts.data_generator import generate_sales_data
from production_analysis.scripts.etl_process import etl_process
from production_analysis.scripts.efficiency_improvement import improve_efficiency
from production_analysis.scripts.data_visualization import generate_visualizations
from production_analysis.scripts.performance_analysis import perform_analysis, print_analysis_results

def main():
    # Configuración
    raw_data_file = 'raw_production_data.csv'
    processed_data_file = 'processed_production_data.csv'
    budget = 100000  # Ejemplo de presupuesto

    # Paso 1: Generación de datos
    print("Generando datos de producción...")
    generate_sales_data(raw_data_file)

    # Paso 2: Proceso ETL
    print("Realizando proceso ETL...")
    etl_process(raw_data_file, processed_data_file)

    # Paso 4: Mejoramiento de eficiencia
    print("Optimizando eficiencia de producción...")
    optimization_results = improve_efficiency(processed_data_file, budget)

    # Paso 5: Visualización de datos
    print("Generando visualizaciones...")
    generate_visualizations(processed_data_file, optimization_results)

    # Paso 6: Análisis de desempeño
    print("Realizando análisis de desempeño...")
    performance_results = perform_analysis(processed_data_file)
    print_analysis_results(performance_results)

    print("\nProceso completo. Revise los archivos de salida para ver los resultados.")

if __name__ == "__main__":
    main()