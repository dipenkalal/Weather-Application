from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('chart/', views.chart),
    path('pollution/', views.pollution),
    path('get_by_id', views.get_by_id),
    path('get_all_elements', views.get_all_elements),
    path('get_by_id', views.get_by_id),
    path('get_all_pollutants', views.get_all_pollutants),
    path('pollution_index', views.pollution_index),

]
