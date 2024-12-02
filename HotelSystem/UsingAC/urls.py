from django.urls import path
from . import views

urlpatterns = [
    path('api/temperature/', views.handle_temperature, name='handle_temperature'),
    path('api/power/', views.handle_power, name='handle_power'),
    path('api/fan-speed/', views.handle_fan_speed, name='handle_fan_speed'),
]