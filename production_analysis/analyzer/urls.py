from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate_data/', views.generate_data, name='generate_data'),
    path('run_etl/', views.run_etl, name='run_etl'),
    path('analyze_performance/', views.analyze_performance, name='analyze_performance'),
    path('improve_efficiency/', views.improve_efficiency, name='improve_efficiency'),
    path('visualize_data/', views.visualize_data, name='visualize_data'),
    path('get_exchange_houses/', views.get_exchange_houses, name='get_exchange_houses'),
    path('get_currencies/', views.get_currencies, name='get_currencies'),
    
]