from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate_data/', views.generate_data, name='generate_data'),
    path('run_etl/', views.run_etl, name='run_etl'),
    path('analyze_sensitivity/', views.analyze_sensitivity, name='analyze_sensitivity'),
    path('improve_efficiency/', views.improve_efficiency, name='improve_efficiency'),
    path('visualize_data/', views.visualize_data, name='visualize_data'),
    path('analyze_performance/', views.analyze_performance, name='analyze_performance'),
]