"""
URLS py in the application

Author: Anestis
Date: December, 2023
"""
from django.urls import path
from . import views

# We must stick to lowercase to app_name. Django convention
app_name = 'simulation'

# url routes list
urlpatterns = [
    # path --> domain.com / simulation /
    # /my_apps --> PROJECT urls.py

    path('ajax/', views.calculate_power, name='calculate_power'),
    path('recalculation/', views.recalculate_pv_system_properties, 
         name='recalculate_pv_system_properties'),
    path('addbattery/', views.add_battery, name='add_battery'),
    path('calculator/', views.calculator_form_fields_handler, name='calculator'),
    path('dashboard/', views.dashboard_results, name='dashboard'),
    path('regulations/', views.regulations, name='regulations'),
    path('about/', views.about, name='about'),
    # path('signup/', views.signup, name='signup'),
]
